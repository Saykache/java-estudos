#!/usr/bin/env python3
"""Baixa a transcrição de vídeos do YouTube abrindo o navegador de verdade.

Nada de API: o script abre o vídeo num Chromium controlado pelo Playwright, liga as legendas
(CC) e lê a legenda que o próprio player baixou. Se isso falhar, clica em "...mais" >
"Mostrar transcrição" e copia o texto do painel, como você faria na mão.
No modo --headless o YouTube costuma entregar a legenda vazia; prefira com a janela aberta.
O navegador usa um perfil próprio que fica salvo, então se você fizer login no Google
uma vez, nas próximas execuções ele já abre logado.

Exemplos:
    python ferramentas/transcricao.py https://www.youtube.com/watch?v=XXXX
    python ferramentas/transcricao.py --aulas 15-19          # pega as aulas pela playlist do curso
    python ferramentas/transcricao.py --aulas 20 --headless  # sem abrir janela
    python ferramentas/transcricao.py --login                # só abre o navegador para você logar

Os arquivos vão para transcricoes/ (fora do git), um .txt por vídeo, no formato "0:07 texto".
"""

import argparse
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

PLAYLIST = "https://www.youtube.com/playlist?list=PL62G310vn6nFIsOCC0H-C2infYgwm8SWW"
RAIZ = Path(__file__).resolve().parent.parent
SAIDA_PADRAO = RAIZ / "transcricoes"
TENTATIVAS = 3
PERFIL_PADRAO = Path.home() / ".cache" / "java-estudos" / "perfil-navegador"
# Título de cada vídeo na playlist: layout novo (lockup) e antigo.
SEL_TITULO_PLAYLIST = "a.ytLockupMetadataViewModelTitle, ytd-playlist-video-renderer a#video-title"


def abrir_navegador(pw, perfil, headless, cdp):
    """Conecta num Chrome já aberto (--cdp) ou abre um com perfil persistente."""
    if cdp:
        navegador = pw.chromium.connect_over_cdp(cdp)
        contexto = navegador.contexts[0] if navegador.contexts else navegador.new_context()
        return contexto, navegador.close
    # O perfil guarda cookies e sessões do navegador: só o seu usuário pode ler.
    perfil.mkdir(parents=True, exist_ok=True)
    perfil.chmod(0o700)
    contexto = pw.chromium.launch_persistent_context(
        str(perfil),
        headless=headless,
        locale="pt-BR",
        viewport={"width": 1280, "height": 900},
        # Sem a barra "Chrome está sendo controlado por software automatizado".
        ignore_default_args=["--enable-automation"],
        args=["--disable-blink-features=AutomationControlled", "--mute-audio"],
    )
    return contexto, contexto.close


def aceitar_cookies(page):
    for nome in ("Aceitar tudo", "Accept all", "Rejeitar tudo", "Reject all"):
        botao = page.get_by_role("button", name=nome)
        if botao.count() and botao.first.is_visible():
            botao.first.click()
            page.wait_for_load_state("domcontentloaded")
            return


def pausar_video(page):
    """Pausa o vídeo e pula anúncios, para o player não atrapalhar os cliques."""
    for _ in range(30):
        pular = page.locator(".ytp-skip-ad-button, .ytp-ad-skip-button, .ytp-ad-skip-button-modern")
        if pular.count() and pular.first.is_visible():
            pular.first.click()
        em_anuncio = page.locator(".ad-showing").count() > 0
        page.evaluate("() => { const v = document.querySelector('video'); if (v) { v.muted = true; v.pause(); } }")
        if not em_anuncio:
            return
        time.sleep(1)


def clicar_se_existir(locator, timeout=3000):
    try:
        locator.first.wait_for(state="visible", timeout=timeout)
        locator.first.click()
        return True
    except PWTimeout:
        return False


def abrir_painel_transcricao(page):
    # Layout atual: expandir a descrição e clicar em "Mostrar transcrição".
    clicar_se_existir(page.locator("#description-inline-expander #expand, tp-yt-paper-button#expand"))
    botao = page.locator("ytd-video-description-transcript-section-renderer button")
    if clicar_se_existir(botao) or clicar_se_existir(page.get_by_role("button", name=re.compile(r"transcri", re.I))):
        return True
    # Layout antigo: menu "..." embaixo do vídeo > "Mostrar transcrição".
    if clicar_se_existir(page.locator("ytd-watch-metadata #button-shape button, ytd-menu-renderer yt-button-shape button[aria-label]").last):
        return clicar_se_existir(page.get_by_role("menuitem", name=re.compile(r"transcri", re.I)))
    return False


LER_SEGMENTOS = """() => {
  const linhas = [];
  const segs = document.querySelectorAll('ytd-transcript-segment-renderer, transcript-segment-view-model');
  for (const s of segs) {
    const tempo = s.querySelector('.segment-timestamp, [class*="timestamp"]');
    const texto = s.querySelector('.segment-text, [class*="segment-text"], yt-formatted-string, span[role="text"]');
    const t = (texto ? texto.innerText : s.innerText).replace(/\\s+/g, ' ').trim();
    if (t) linhas.push(((tempo ? tempo.innerText.trim() : '') + ' ' + t).trim());
  }
  if (linhas.length) return linhas;
  const painel = document.querySelector('ytd-engagement-panel-section-list-renderer[target-id*="transcript"]');
  return painel ? painel.innerText.split('\\n').map(l => l.trim()).filter(Boolean) : [];
}"""


def ler_transcricao(page):
    try:
        page.locator("ytd-transcript-segment-renderer, transcript-segment-view-model").first.wait_for(timeout=15000)
    except PWTimeout:
        pass
    # Espera o número de segmentos parar de crescer (o painel carrega aos poucos).
    anterior, linhas = -1, []
    for _ in range(10):
        linhas = page.evaluate(LER_SEGMENTOS)
        if len(linhas) == anterior:
            break
        anterior = len(linhas)
        time.sleep(0.7)
    return linhas


def formatar_tempo(ms):
    seg = int(ms) // 1000
    h, resto = divmod(seg, 3600)
    return f"{h}:{resto // 60:02d}:{resto % 60:02d}" if h else f"{resto // 60}:{resto % 60:02d}"


def linhas_das_legendas(dados):
    """Converte a legenda que o player baixou (formato json3) em linhas "0:07 texto"."""
    linhas = []
    for ev in dados.get("events", []):
        texto = "".join(s.get("utf8", "") for s in ev.get("segs") or []).replace("\n", " ").strip()
        if texto:
            linhas.append(f"{formatar_tempo(ev.get('tStartMs', 0))} {' '.join(texto.split())}")
    return linhas


def ligar_legendas(page):
    """Liga o botão CC do player; é isso que faz o navegador baixar a legenda."""
    botao = page.locator("button.ytp-subtitles-button")
    try:
        botao.wait_for(state="attached", timeout=10000)
    except PWTimeout:
        return
    if botao.get_attribute("aria-pressed") != "true":
        page.locator("#movie_player").hover()
        botao.click(force=True)


def transcrever(contexto, url):
    """Tenta primeiro a legenda que o player baixa; se não vier, usa o painel "Mostrar transcrição"."""
    page = contexto.new_page()
    legendas = []
    id_video = parse_qs(urlparse(url).query).get("v", [None])[0]

    def ao_receber(resposta):
        # Ignora legendas de anúncios (outro v=) e traduções automáticas (tlang=).
        params = parse_qs(urlparse(resposta.url).query)
        if (
            "/api/timedtext" in resposta.url
            and "tlang" not in params
            and (id_video is None or params.get("v", [None])[0] == id_video)
            and resposta.ok
        ):
            try:
                legendas.append(resposta.json())
            except Exception:
                pass  # corpo vazio ou em outro formato

    page.on("response", ao_receber)
    try:
        page.goto(url, wait_until="domcontentloaded")
        aceitar_cookies(page)
        page.locator("h1.ytd-watch-metadata, #title h1").first.wait_for(timeout=20000)
        pausar_video(page)
        titulo = page.locator("h1.ytd-watch-metadata, #title h1").first.inner_text().strip()

        ligar_legendas(page)
        for _ in range(30):
            linhas = next((l for l in map(linhas_das_legendas, legendas) if l), None)
            if linhas:
                return titulo, linhas
            time.sleep(0.5)

        if abrir_painel_transcricao(page):
            linhas = ler_transcricao(page)
            if linhas:
                return titulo, linhas
        raise RuntimeError(
            "não consegui a transcrição (sem legenda no player e o painel veio vazio). "
            "Rode sem --headless e, se continuar, faça login com --login"
        )
    finally:
        page.close()


def videos_da_playlist(contexto, inicio, fim):
    """Lê a playlist no navegador e devolve [(numero, titulo, url)] das aulas pedidas."""
    page = contexto.new_page()
    try:
        page.goto(PLAYLIST, wait_until="domcontentloaded")
        aceitar_cookies(page)
        itens = page.locator(SEL_TITULO_PLAYLIST)
        itens.first.wait_for(timeout=20000)
        encontrados = {}
        for _ in range(15):  # rola a página até carregar a última aula pedida
            maior = -1
            for titulo, href in page.evaluate(
                "sel => [...document.querySelectorAll(sel)].map(a => [a.title || a.innerText, a.href])",
                SEL_TITULO_PLAYLIST,
            ):
                m = re.match(r"\s*(\d+)\s*-", titulo)
                if not m:
                    continue
                n = int(m.group(1))
                maior = max(maior, n)
                if inicio <= n <= fim:
                    encontrados[n] = (titulo.strip(), href.split("&")[0])
            if maior >= fim:
                break
            page.mouse.wheel(0, 20000)
            time.sleep(1.5)
        faltando = [n for n in range(inicio, fim + 1) if n not in encontrados]
        if faltando:
            print(f"Aviso: aulas não encontradas na playlist: {faltando}", file=sys.stderr)
        return [(n, *encontrados[n]) for n in sorted(encontrados)]
    finally:
        page.close()


def nome_arquivo(titulo, numero=None):
    base = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    base = re.sub(r"[^\w\s-]", "", base).strip().lower()
    base = re.sub(r"[\s_-]+", "-", base)[:80]
    return f"{numero:02d}-{base}.txt" if numero is not None and not re.match(r"\d", base) else f"{base}.txt"


def faixa(texto):
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", texto)
    if not m:
        raise argparse.ArgumentTypeError("use um número (15) ou uma faixa (15-19)")
    inicio = int(m.group(1))
    return inicio, int(m.group(2) or inicio)


def main():
    ap = argparse.ArgumentParser(description="Baixa transcrições do YouTube usando o navegador.")
    ap.add_argument("urls", nargs="*", help="links de vídeos do YouTube")
    ap.add_argument("--aulas", type=faixa, help="aulas da playlist do curso, ex.: 15-19")
    ap.add_argument("--saida", type=Path, default=SAIDA_PADRAO, help=f"pasta de saída (padrão: {SAIDA_PADRAO})")
    ap.add_argument("--perfil", type=Path, default=PERFIL_PADRAO, help="pasta do perfil do navegador")
    ap.add_argument("--headless", action="store_true", help="não mostra a janela do navegador")
    ap.add_argument("--cdp", help="conectar num Chrome já aberto com --remote-debugging-port (ex.: http://localhost:9222)")
    ap.add_argument("--login", action="store_true", help="abre o YouTube para você fazer login e espera Enter")
    args = ap.parse_args()

    if not (args.urls or args.aulas or args.login):
        ap.error("informe links de vídeo, --aulas ou --login")

    args.saida.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        contexto, fechar = abrir_navegador(pw, args.perfil, args.headless and not args.login, args.cdp)
        try:
            if args.login:
                contexto.new_page().goto("https://www.youtube.com")
                input("Faça login no navegador que abriu e aperte Enter aqui para fechar...")
                return

            alvos = [(None, None, u) for u in args.urls]
            if args.aulas:
                alvos += videos_da_playlist(contexto, *args.aulas)

            falhas = 0
            for numero, titulo_playlist, url in alvos:
                rotulo = titulo_playlist or url
                print(f"→ {rotulo}", flush=True)
                for tentativa in range(1, TENTATIVAS + 1):
                    try:
                        titulo, linhas = transcrever(contexto, url)
                        break
                    except Exception as erro:
                        print(f"  tentativa {tentativa} falhou: {erro}", file=sys.stderr, flush=True)
                else:  # segue para o próximo vídeo
                    falhas += 1
                    continue
                arquivo = args.saida / nome_arquivo(titulo_playlist or titulo, numero)
                arquivo.write_text(f"{titulo}\n{url}\n\n" + "\n".join(linhas) + "\n", encoding="utf-8")
                print(f"  {len(linhas)} trechos → {arquivo}", flush=True)
        finally:
            fechar()
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
