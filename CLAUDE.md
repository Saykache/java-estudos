# java-estudos

Site estático de estudos da playlist **Maratona Java Virado no Jiraya** (DevDojo).
Publicado via GitHub Pages (branch `main`, pasta raiz). Tudo em português do Brasil.

## Estrutura
- `index.html` — lista de aulas (um `<li>` por aula, em ordem).
- `aulas/NN-titulo-da-aula.html` — uma página por aula (ou `NN-MM-slug.html` para aulas agrupadas).
- `css/style.css` — estilo compartilhado (claro/escuro automático). Não duplicar CSS nas aulas.
- `js/app.js` — componentes de flashcards e quiz. Não duplicar JS nas aulas.

## Como adicionar uma aula
1. Copiar `aulas/02-como-java-funciona.html` para `aulas/NN-slug.html`.
2. Trocar título, link do vídeo, seções (Resumo, Material de estudo) e o objeto `window.AULA` no fim da página:
   - `flashcards`: array de `[frente, verso]` (10 a 25 cartões, frente em forma de pergunta).
   - `quiz`: 10 questões, fácil → difícil, misturando:
     - `{ tipo: 'multipla', pergunta, opcoes: [4 itens], correta: índice, explicacao }`
     - `{ tipo: 'vf', pergunta, correta: 0 (Verdadeiro) | 1 (Falso), explicacao }`
     - `{ tipo: 'discursiva', pergunta, explicacao }` (explicacao = resposta esperada)
3. Adicionar o `<li>` correspondente no `index.html`.
4. Commit `Aula NN - Título` e push.

## Conteúdo de cada aula
Seções: Resumo (visão geral, conceitos-chave, "Atenção" com pegadinhas, paralelo com PHP quando útil),
Flashcards, Quiz, Material de estudo (mapa mental, glossário, prática, revisão espaçada 1/3/7/14 dias, perguntas para aprofundar).
Ser fiel à transcrição da aula quando fornecida; se o material vier só do tema, manter o aviso no topo da página.

## Agrupamento das aulas
Aulas que são partes do mesmo tema viram uma página só: `aulas/NN-MM-slug.html`, selo `NN–MM` no `index.html`,
commit `Aulas NN-MM - Título`. Exercícios e resoluções ficam junto da teoria. Só gerar a página com as transcrições
do bloco inteiro (o autor pode mandar em partes). Aulas avulsas continuam `NN-slug.html`.

Feitas: 02 · 03–07 · 08 · 09 · 10–14 · 15–19 · 20–24 · 25–26 · 27–31 · 32–34 · 36–38 · 39–43 · 44–47 · 48–51 · 52–53 · 54–57 · 58–59 · 60–63.

Plano (títulos da playlist; a aula 35 não aparece nela):
- 10–14 Tipos primitivos (convenções, declaração/memória, casting, Strings, exercício)
- 15–19 Operadores (aritméticos, relacionais, AND, OR, atribuição)
- 20–24 Condicionais: if, else if, ternário, tabela verdade, exercício e resolução
- 25–26 Switch + exercício
- 27–31 Estruturas de repetição (while/do while/for, break, continue + exercícios)
- 32–34 Arrays
- 36–38 Arrays multidimensionais (foreach, inicialização)
- 39–43 OO: classes, coesão, exercício, referência de objetos
- 44–47 Métodos: parâmetros e retorno
- 48–51 Parâmetros primitivo × referência e `this`
- 52–53 Varargs + exercício
- 54–57 `private`, get/set e sobrecarga de métodos
- 58–59 Construtores
- 60–63 Blocos de inicialização e `static`
- 64–70 Associação (64–67, 70) + leitura do teclado (68–69)
- 71–75 Herança
- 76 Sobrescrita de `toString`
- 77–79 Modificador `final`
- 80–83 Enumeração
- 84–86 Classes abstratas
- 87–89 Interfaces
- 90–94 Polimorfismo
- 95+ Exceções (planejar o restante quando chegar lá)

## Transcrições
`ferramentas/transcricao.py` baixa as legendas pelo navegador (Playwright, janela aberta; headless vem vazio):
`ferramentas/.venv/bin/python ferramentas/transcricao.py --aulas 20-24` → `transcricoes/NN-*.txt` (fora do git).
Setup: `ferramentas/instalar.sh` (precisa de sudo).

## Contexto do autor
O autor é desenvolvedor PHP/Laravel aprendendo Java; comparações com PHP ajudam.
