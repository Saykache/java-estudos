// Componentes reutilizáveis: flashcards e quiz.
// Cada página de aula define window.AULA = { flashcards: [...], quiz: [...] }.

function iniciarFlashcards(cards, raiz) {
  if (!raiz || !cards.length) return;
  let i = 0;

  raiz.innerHTML = `
    <div class="card" tabindex="0" aria-label="Clique para virar">
      <div class="card-inner">
        <div class="card-face card-frente"><small>Pergunta</small><span class="txt-frente"></span></div>
        <div class="card-face card-verso"><small>Resposta</small><span class="txt-verso"></span></div>
      </div>
    </div>
    <div class="flash-controles">
      <button class="ant">← Anterior</button>
      <span class="flash-contador"></span>
      <button class="prox primario">Próximo →</button>
    </div>
    <p style="text-align:center;margin:10px 0 0">
      <button class="embaralhar">Embaralhar</button>
    </p>`;

  const card = raiz.querySelector('.card');
  const frente = raiz.querySelector('.txt-frente');
  const verso = raiz.querySelector('.txt-verso');
  const contador = raiz.querySelector('.flash-contador');
  const ant = raiz.querySelector('.ant');
  const prox = raiz.querySelector('.prox');

  function mostrar() {
    card.classList.remove('virado');
    frente.textContent = cards[i][0];
    verso.textContent = cards[i][1];
    contador.textContent = `${i + 1} / ${cards.length}`;
    ant.disabled = i === 0;
    prox.disabled = i === cards.length - 1;
  }

  const virar = () => card.classList.toggle('virado');
  card.addEventListener('click', virar);
  card.addEventListener('keydown', e => {
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); virar(); }
  });
  ant.addEventListener('click', () => { if (i > 0) { i--; mostrar(); } });
  prox.addEventListener('click', () => { if (i < cards.length - 1) { i++; mostrar(); } });
  raiz.querySelector('.embaralhar').addEventListener('click', () => {
    for (let j = cards.length - 1; j > 0; j--) {
      const k = Math.floor(Math.random() * (j + 1));
      [cards[j], cards[k]] = [cards[k], cards[j]];
    }
    i = 0;
    mostrar();
  });

  mostrar();
}

function iniciarQuiz(questoes, raiz) {
  if (!raiz || !questoes.length) return;
  const objetivas = questoes.filter(q => q.tipo !== 'discursiva').length;
  let respondidas = 0;
  let acertos = 0;

  const placar = document.createElement('div');
  placar.className = 'placar';

  function atualizarPlacar() {
    placar.textContent = respondidas < objetivas
      ? `Acertos: ${acertos} de ${respondidas} respondidas (${objetivas} objetivas)`
      : `Resultado: ${acertos} de ${objetivas} nas objetivas`;
  }

  questoes.forEach((q, n) => {
    const box = document.createElement('div');
    box.className = 'questao';

    const enunciado = document.createElement('p');
    enunciado.className = 'enunciado';
    enunciado.textContent = `${n + 1}. ${q.pergunta}`;
    box.appendChild(enunciado);

    const explicacao = document.createElement('div');
    explicacao.className = 'explicacao';
    explicacao.textContent = q.explicacao;

    if (q.tipo === 'discursiva') {
      const ta = document.createElement('textarea');
      ta.placeholder = 'Escreva sua resposta antes de conferir…';
      const btn = document.createElement('button');
      btn.textContent = 'Ver resposta esperada';
      btn.addEventListener('click', () => {
        explicacao.classList.add('visivel');
        btn.disabled = true;
      });
      box.append(ta, btn);
    } else {
      const opcoes = q.tipo === 'vf' ? ['Verdadeiro', 'Falso'] : q.opcoes;
      const wrap = document.createElement('div');
      wrap.className = 'opcoes';
      const botoes = opcoes.map((texto, idx) => {
        const b = document.createElement('button');
        b.className = 'opcao';
        b.textContent = q.tipo === 'vf' ? texto : `${'abcd'[idx]}) ${texto}`;
        b.addEventListener('click', () => {
          botoes.forEach(x => (x.disabled = true));
          botoes[q.correta].classList.add('certa');
          if (idx === q.correta) acertos++;
          else b.classList.add('errada');
          respondidas++;
          explicacao.classList.add('visivel');
          atualizarPlacar();
        });
        wrap.appendChild(b);
        return b;
      });
      box.appendChild(wrap);
    }

    box.appendChild(explicacao);
    raiz.appendChild(box);
  });

  atualizarPlacar();
  raiz.appendChild(placar);
}

document.addEventListener('DOMContentLoaded', () => {
  const aula = window.AULA;
  if (!aula) return;
  iniciarFlashcards(aula.flashcards || [], document.getElementById('flashcards-app'));
  iniciarQuiz(aula.quiz || [], document.getElementById('quiz-app'));
});
