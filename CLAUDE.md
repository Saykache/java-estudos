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

Feitas: 02 · 03–07 · 08 · 09 · 10–14 · 15–19 · 20–24 · 25–26 · 27–31 · 32–34 · 35 · 36–38 · 39–43 · 44–47 · 48–51 · 52–53 · 54–57 · 58–59 · 60–63 · 64–70 · 71–75 · 76 · 77–79 · 80–83 · 84–86 · 87–89 · 90–94 · 95–99 · 100–105 · 106–107 · 108–111 · 112–118 · 119–124 · 125–130 · 131–136 · 137–143 · 144–148 · 149–153 · 154–158 · 159–165 · 166–174 · 175–182 · 183–188.

Plano (títulos no README do professor; a aula 35 não está na playlist, é o vídeo cl47iLWalUw — o script aceita a URL direta):
- 10–14 Tipos primitivos (convenções, declaração/memória, casting, Strings, exercício)
- 15–19 Operadores (aritméticos, relacionais, AND, OR, atribuição)
- 20–24 Condicionais: if, else if, ternário, tabela verdade, exercício e resolução
- 25–26 Switch + exercício
- 27–31 Estruturas de repetição (while/do while/for, break, continue + exercícios)
- 32–34 Arrays
- 35 Arrays pt 04 (inicialização e foreach)
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
- 95–99 Exceções: Error, RuntimeException, Exception, lançando unchecked e checked
- 100–105 Exceções: finally, múltiplos catch, multi-catch, try-with-resources, customizada, regras de sobrescrita
- 106–107 Wrappers
- 108–111 Strings (pool, métodos, desempenho, StringBuilder)
- 112–118 Datas legadas: Date, Calendar, DateFormat, Locale (datas, números, moeda), SimpleDateFormat
- 119–124 java.time: LocalDate, LocalTime, LocalDateTime, Instant, Duration, Period
- 125–130 java.time: ChronoUnit, TemporalAdjusters, ZonedDateTime, DateTimeFormatter + ResourceBundle
- 131–136 Regex (Pattern e Matcher)
- 137–143 Scanner (tokens e delimitadores) + IO (File, FileWriter/Reader, Buffered, diretórios)
- 144–148 NIO: Path, Paths, Files, normalize, resolve, relativize
- 149–153 NIO: BasicFileAttributes, Dos/PosixFileAttributes, DirectoryStream
- 154–158 NIO: SimpleFileVisitor, PathMatcher, ZipOutputStream
- 159–165 Serialization + Coleções: equals, hashCode, Big-O
- 166–174 Coleções: List, sorting (Comparable/Comparator), binarySearch, conversão, Iterator
- 175–182 Coleções: Set/TreeSet, Map/HashMap/TreeMap, Queue/PriorityQueue
- 183–188 Generics
- 189–194 Classes internas + parametrizando comportamentos
- 195–202 Lambdas, method reference, Optional
- 203–219 Streams (dividir: 203–210, 211–219)
- 220–228 Threads; 229+ Concorrência (planejar quando chegar lá)

## Transcrições
`ferramentas/transcricao.py` baixa as legendas pelo navegador (Playwright, janela aberta; headless vem vazio):
`ferramentas/.venv/bin/python ferramentas/transcricao.py --aulas 20-24` → `transcricoes/NN-*.txt` (fora do git).
Setup: `ferramentas/instalar.sh` (precisa de sudo).
Se a legenda vier em outro idioma (o YouTube às vezes erra o reconhecimento; ex.: aula 156 em romeno), use o código do professor e avise na página.

## Código do professor
Repositório oficial: https://github.com/devdojobr/maratona-java-virado-no-jiraya (branch `videoNN` = projeto acumulado
até a aula NN; o README lista os títulos das 284 aulas). Código exato de uma aula: `git diff origin/videoNN-1 origin/videoNN`.
Faltam algumas branches (ex.: não existe `video106`); nesse caso, diff a partir da anterior que existir (`video105..video107`).
Usar para conferir nomes de classes/pacotes (ex.: testes são `XxxTest01`, pacotes `javacore.Aintroducaoclasses`,
`Bintroducaometodos`, ... `Gassociacao`, `Hheranca`) e valores dos exemplos, em vez de adivinhar pelo áudio.

## Contexto do autor
O autor é desenvolvedor PHP/Laravel aprendendo Java; comparações com PHP ajudam.
