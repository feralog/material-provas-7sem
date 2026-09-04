/**
 * testar_markdown.js — checa o renderizador de markdown do chat.
 *
 *   node _scripts/testar_markdown.js Quizzes/quiz_disacusias.html
 *
 * O texto vem de um modelo externo, entao o que mais importa aqui e que HTML
 * dentro da resposta NUNCA vire tag de verdade. O resto e formatacao.
 */
const fs = require('fs');
const vm = require('vm');

const arquivo = process.argv[2] || 'Quizzes/quiz_disacusias.html';
const src = fs.readFileSync(arquivo, 'utf8');
const js = src.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/)[1];

const els = {};
const mk = (id) => els[id] || (els[id] = {
  id, innerHTML: '', textContent: '', className: '', value: '', style: {}, attrs: {},
  firstElementChild: { src: '' },
  setAttribute(k, v) { this.attrs[k] = v; },
  getAttribute(k) { return this.attrs[k] !== undefined ? this.attrs[k] : null; },
  removeAttribute(k) { delete this.attrs[k]; },
  insertAdjacentHTML(_, h) { this.innerHTML += h; },
});
const ctx = {
  window: { scrollTo() {}, addEventListener() {} },
  document: { addEventListener() {}, getElementById: mk },
  location: { protocol: 'file:' },
  console, JSON, Math, String, Array, Object, RegExp, parseInt, isNaN, setTimeout,
};
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(js, ctx);
const md = ctx.mdChat;

let falhas = 0;
function ok(cond, msg) { if (!cond) { console.error('  FALHOU: ' + msg); falhas++; } }
function contem(html, trecho, msg) { ok(html.indexOf(trecho) > -1, msg + '\n     saiu: ' + html.slice(0, 220)); }

// ── 1) SEGURANCA: nada que venha do modelo pode virar tag ──────────────────
{
  const perigo = 'Cuidado <script>alert(1)</script> e <img src=x onerror=alert(1)> aqui.';
  const h = md(perigo);
  ok(h.indexOf('<script') === -1, 'tag <script> da resposta sobreviveu');
  ok(h.indexOf('<img') === -1, 'tag <img> da resposta sobreviveu');
  contem(h, '&lt;script&gt;', 'o script deveria aparecer escapado, como texto');
  console.log('  ok  HTML vindo do modelo e escapado, nao interpretado');
}

// ── 2) negrito, italico e codigo ───────────────────────────────────────────
{
  const h = md('O filoides **nao tem calcificacoes** e e *solido*, use `pgNN`.');
  contem(h, '<strong>nao tem calcificacoes</strong>', 'negrito nao virou <strong>');
  contem(h, '<em>solido</em>', 'italico nao virou <em>');
  contem(h, '<code', 'codigo inline nao virou <code>');
  ok(h.indexOf('**') === -1, 'sobraram asteriscos de negrito na saida');
  console.log('  ok  **negrito**, *italico* e `codigo`');
}

// ── 3) o texto real que o DeepSeek devolveu ────────────────────────────────
{
  const real = 'Claro:\n\n' +
    '**A)** Cistos simples com reforco acustico definem lesao cistica anecoica. ' +
    'Tumor filoides e **solido**, nao cistico.\n\n' +
    '**B)** Microcalcificacoes agrupadas sao marcadores de **carcinoma** (ex.: CDIS).\n\n' +
    '**C)** Calcificacoes em pipoca sao a assinatura de **fibroadenoma em involucao**.\n\n' +
    'Ou seja: A descreve cisto, B descreve cancer, C descreve fibroadenoma.';
  const h = md(real);
  ok((h.match(/<strong>/g) || []).length === 6, 'esperava 6 negritos, veio ' + (h.match(/<strong>/g) || []).length);
  ok((h.match(/<p /g) || []).length === 5, 'esperava 5 paragrafos, veio ' + (h.match(/<p /g) || []).length);
  ok(h.indexOf('**') === -1, 'sobrou ** na resposta real');
  console.log('  ok  resposta real do DeepSeek: 6 negritos em 5 paragrafos, sem ** solto');
}

// ── 4) listas ──────────────────────────────────────────────────────────────
{
  const h = md('Sinais:\n- palidez\n- febre\n- petequias');
  contem(h, '<ul', 'lista com hifen nao virou <ul>');
  ok((h.match(/<li /g) || []).length === 3, 'esperava 3 itens');
  const o = md('Passos:\n1. hemograma\n2. esfregaco\n3. mielograma');
  contem(o, '<ol', 'lista numerada nao virou <ol>');
  ok((o.match(/<li /g) || []).length === 3, 'esperava 3 itens numerados');
  console.log('  ok  listas com hifen e numeradas');
}

// ── 5) titulo, citacao e divisor ───────────────────────────────────────────
{
  contem(md('## Resumo\ntexto'), 'font-weight:600', 'titulo ## nao ficou destacado');
  contem(md('> ponto-chave'), 'border-left', 'citacao > nao virou callout');
  contem(md('a\n\n---\n\nb'), '<hr', 'divisor --- nao virou <hr>');
  console.log('  ok  titulo, citacao (>) e divisor');
}

// ── 6) tabela ──────────────────────────────────────────────────────────────
{
  const h = md('| Tipo | Achado |\n| --- | --- |\n| Filoides | solido |\n| Cisto | anecoico |');
  contem(h, '<table', 'tabela nao renderizou');
  ok((h.match(/<th /g) || []).length === 2, 'esperava 2 colunas no cabecalho');
  ok((h.match(/<td /g) || []).length === 4, 'esperava 4 celulas no corpo');
  console.log('  ok  tabela markdown vira <table>');
}

// ── 7) bloco de codigo protege o conteudo ──────────────────────────────────
{
  const h = md('Exemplo:\n```\nver_pagina.py **nao** vira negrito\n```');
  contem(h, '<pre', 'bloco ``` nao virou <pre>');
  contem(h, '**nao**', 'o ** dentro do bloco de codigo foi formatado (nao deveria)');
  console.log('  ok  bloco de codigo preserva o conteudo literal');
}

// ── 8) streaming: markdown pela metade nao pode quebrar ────────────────────
{
  const completo = 'O achado e **muito importante** para o diagnostico.';
  for (let i = 1; i <= completo.length; i++) {
    let h;
    try { h = md(completo.slice(0, i)); }
    catch (e) { ok(false, 'quebrou com ' + i + ' caracteres: ' + e.message); break; }
    ok(h.indexOf('<script') === -1, 'injecao em prefixo de ' + i + ' caracteres');
  }
  console.log('  ok  todos os prefixos do streaming renderizam sem erro');
}

// ── 9) texto simples continua simples ──────────────────────────────────────
{
  const h = md('Uma frase direta, sem formatacao nenhuma.');
  contem(h, 'Uma frase direta', 'texto simples sumiu');
  ok(h.indexOf('<strong') === -1 && h.indexOf('<ul') === -1, 'texto simples ganhou formatacao indevida');
  console.log('  ok  texto sem markdown sai como paragrafo limpo');
}

if (falhas) { console.error('\n' + falhas + ' falha(s)'); process.exit(1); }
console.log('PASSOU  ' + arquivo);
