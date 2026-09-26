# Estudos de Java

Material de estudo da playlist **[Maratona Java Virado no Jiraya](https://www.youtube.com/playlist?list=PL62G310vn6nFIsOCC0H-C2infYgwm8SWW)**, da DevDojo, escrito do ponto de vista de quem vem do PHP/Laravel.

**Site:** https://saykache.github.io/java-estudos/

O curso está completo: as **284 aulas** estão reunidas em **58 páginas**, agrupadas por tema.

## O que tem em cada página

- **Resumo** da aula ou do bloco de aulas, com o código do professor, uma seção **Atenção** (pegadinhas, erros do vídeo ou do repositório e correções) e um **paralelo com PHP/Laravel**.
- **Flashcards** (10 a 25 cartões) para revisar.
- **Quiz** de 10 questões (múltipla escolha, verdadeiro/falso e discursivas), do fácil ao difícil.
- **Material de estudo**: mapa mental, prática no terminal (WSL/Linux) com a saída esperada, exercícios, glossário, revisão espaçada (1, 3, 7 e 14 dias) e perguntas para aprofundar.

Os itens marcados como "extra" não estão nos vídeos: são complementos ou correções.

## Módulos

| Módulo | Aulas |
|---|---|
| Introdução | 02–09 |
| Fundamentos da linguagem | 10–38 |
| Orientação a objetos | 39–94 |
| Exceções | 95–105 |
| APIs essenciais (wrappers, Strings, datas, regex) | 106–136 |
| IO e NIO | 137–158 |
| Coleções e generics | 159–188 |
| Programação funcional (lambdas, Optional, Streams) | 189–219 |
| Threads e concorrência | 220–245 |
| Padrões de projeto | 246–251 |
| Banco de dados com JDBC | 252–279 |
| Testes e Java moderno (JUnit, records, pattern matching) | 280–284 |

A lista completa de páginas está no [índice do site](https://saykache.github.io/java-estudos/).

## Estrutura do repositório

```
index.html              índice: sumário e páginas agrupadas por módulo
aulas/                  uma página por aula ou bloco (NN-slug.html ou NN-MM-slug.html)
css/style.css           estilo compartilhado (tema claro/escuro automático)
js/app.js               componentes de flashcards e quiz
ferramentas/            script que baixa as legendas dos vídeos
CLAUDE.md               convenções para criar e manter as páginas
```

O site é HTML estático, sem build. Cada página declara os flashcards e o quiz num objeto `window.AULA` no fim do arquivo, e o `js/app.js` monta os componentes.

Para ver localmente:

```bash
python3 -m http.server 8000
```

e abrir http://localhost:8000.

## Como o conteúdo foi feito

1. **Legendas**: `ferramentas/transcricao.py` abre cada vídeo num Chromium controlado pelo Playwright, liga as legendas e salva o texto em `transcricoes/` (fora do git). Se a legenda não vier, ele recarrega a página e tenta o painel "Mostrar transcrição".
2. **Código**: os nomes de classes, pacotes e valores foram conferidos no [repositório do professor](https://github.com/devdojobr/maratona-java-virado-no-jiraya) (uma branch `videoNN` por aula; o diff entre duas branches mostra o código de uma aula).
3. **Página**: resumo, flashcards, quiz e material de estudo escritos a partir das legendas e do código.

Algumas aulas não têm legenda no YouTube (206, 213, 216 e 243) ou vieram em outro idioma (156 e 221). Nessas, a página avisa no topo de onde veio o conteúdo.

### Usando o script de legendas

```bash
ferramentas/instalar.sh                                          # uma vez: venv, Playwright e Chromium (usa sudo)
ferramentas/.venv/bin/python ferramentas/transcricao.py --aulas 20-24
ferramentas/.venv/bin/python ferramentas/transcricao.py https://www.youtube.com/watch?v=...
ferramentas/.venv/bin/python ferramentas/transcricao.py --login  # abre o navegador para fazer login no Google
```

Rode com a janela aberta: no modo `--headless` o YouTube costuma entregar a legenda vazia.

## Créditos

Todo o conteúdo das aulas é do curso gratuito **Maratona Java Virado no Jiraya**, de William Suane / [DevDojo](https://github.com/devdojobr). Este repositório é só um material de estudo pessoal feito a partir dele.
