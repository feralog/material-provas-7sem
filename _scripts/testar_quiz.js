#!/usr/bin/env node
/**
 * testar_quiz.js — roda o quiz gerado num DOM falso e checa os invariantes.
 *
 * Uso:
 *   node _scripts/testar_quiz.js Quizzes/quiz_tireoide.html
 *   node _scripts/testar_quiz.js Quizzes/*.html
 *
 * Checa: sintaxe do JS, tela inicial com seletor, resumo (seções/tabelas/figuras),
 * fluxo do quiz, aviso de questões em branco, contadores, filtros do gabarito,
 * imagens sobrevivendo ao embaralhamento e integridade do gabarito após shuffle.
 *
 * Sai com código 1 se qualquer arquivo falhar.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

function testar(arquivo) {
  const src = fs.readFileSync(arquivo, 'utf8');
  const mJs = src.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/);
  const mRs = src.match(/<script type="text\/html" id="resumoSrc">([\s\S]*?)<\/script>/);
  if (!mJs) throw new Error('bloco <script> principal não encontrado');
  if (!mRs) throw new Error('bloco do resumo não encontrado');
  const js = mJs[1], resumo = mRs[1];

  // sintaxe
  new vm.Script(js, { filename: arquivo });

  // DOM falso
  const els = {};
  const mk = (id) => els[id] || (els[id] = {
    innerHTML: '', textContent: id === 'resumoSrc' ? resumo : '',
    className: '', firstElementChild: { src: '' }
  });
  const ctx = {
    window: { scrollTo() {}, addEventListener() {} },
    document: { addEventListener() {}, getElementById: mk },
    console,
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);

  const harness = `
    (function(){
      var out = {};
      function stage(){ return document.getElementById('stage').innerHTML; }
      function hdr(){ return document.getElementById('hdr').innerHTML; }
      function ok(c,m){ if(!c) throw new Error(m); }

      out.questoes = QUIZ.length;
      out.comImagem = QUIZ.filter(function(q){return q.image}).length;

      // tela inicial
      ok(/Quiz/.test(stage()) && /Resumo/.test(stage()), 'tela inicial sem o seletor quiz/resumo');
      ok(/data-act="start"/.test(stage()), 'sem botão de começar o quiz');
      ok(/data-act="resumo"/.test(stage()), 'sem botão de ler o resumo');

      // resumo
      A.resumo();
      var r = stage();
      out.secoes = (r.match(/<h2>/g)||[]).length;
      out.figurasResumo = (r.match(/<figure class="fig"/g)||[]).length;
      ok(out.secoes > 0, 'resumo sem nenhuma seção');
      ok(/data-act="home"/.test(hdr()), 'resumo sem botão de voltar');
      ok(!/@@IMG:/.test(r), 'sobrou marcador @@IMG:  não resolvido no resumo');
      ok(!/__[A-Z_]+__/.test(r), 'sobrou placeholder no resumo');

      // quiz
      A.home(); A.start();
      ok(/Questão 01/.test(hdr()), 'trilha/contador não renderizou');
      ok(S.order.length === QUIZ.length, 'deck com tamanho errado');

      // imagem sobrevive ao embaralhamento
      if (out.comImagem > 0) {
        var i = S.order.findIndex(function(q){ return q.image; });
        ok(i >= 0, 'as imagens sumiram no embaralhamento');
        A.go(i);
        ok(/<figure class="fig qfig"/.test(stage()), 'figura não renderizou na questão');
        ok(/data:image\\/jpeg;base64,/.test(stage()), 'imagem não é data URI');
        A.go(0);
      }

      // responde tudo menos 3, para disparar o aviso de branco
      var n = S.order.length, deixar = Math.min(3, n - 1);
      for (var k = 0; k < n - deixar; k++) {
        A.pick(k % 2 === 0 ? S.order[S.i].correctIndex : (S.order[S.i].correctIndex === 0 ? 1 : 0));
        if (S.i < n - 1) A.go(S.i + 1);
      }
      A.go(n - 1); A.finish();
      ok(/em branco/.test(stage()), 'não avisou sobre questões em branco');
      A.force();

      var c = counts();
      out.certas = c.hit; out.erradas = c.miss; out.branco = c.blank;
      ok(c.hit + c.miss + c.blank === n, 'contadores não fecham');
      ok(/Gabarito comentado/.test(stage()), 'sem gabarito comentado');

      // filtros
      A.filter('wrong'); ok(reviewList().length === c.miss, 'filtro erradas divergente');
      A.filter('right'); ok(reviewList().length === c.hit, 'filtro certas divergente');
      A.filter('blank'); ok(reviewList().length === c.blank, 'filtro branco divergente');
      A.filter('all');   ok(reviewList().length === n, 'filtro todas divergente');

      A.toggleAll();
      ok(/Por quê/.test(stage()), 'expandir tudo não abriu as explicações');

      A.jump(0);
      ok(!S.finished && S.i === 0, 'abrir-no-quiz não voltou para a questão');

      // gabarito íntegro após 30 embaralhamentos
      for (var t = 0; t < 30; t++) {
        var o = build();
        if (!o.every(function(q){ return q.options[q.correctIndex] === QUIZ[q.id].options[0]; }))
          throw new Error('embaralhamento quebrou o gabarito');
      }
      return out;
    })()
  `;
  return vm.runInContext(js + '\n' + harness, ctx);
}

const alvos = process.argv.slice(2);
if (!alvos.length) { console.error('uso: node _scripts/testar_quiz.js <arquivo.html> ...'); process.exit(2); }

let falhou = 0;
for (const f of alvos) {
  const nome = path.basename(f);
  try {
    const o = testar(f);
    const mb = (fs.statSync(f).size / 1048576).toFixed(1);
    console.log(`PASSOU  ${nome}`);
    console.log(`        ${o.questoes} questões (${o.comImagem} com imagem) · ` +
                `${o.secoes} seções · ${o.figurasResumo} figuras no resumo · ${mb} MB`);
  } catch (e) {
    falhou++;
    console.log(`FALHOU  ${nome}`);
    console.log(`        ${e.message}`);
  }
}
process.exit(falhou ? 1 : 0);
