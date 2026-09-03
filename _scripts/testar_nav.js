/**
 * testar_nav.js — navegacao: voltar ao indice, sair do quiz e retomar.
 *
 *   node testar_nav.js <quiz.html> [--file]
 *
 * --file simula abertura por duplo clique (location.protocol === 'file:').
 */
const fs = require('fs');
const vm = require('vm');

const arquivo = process.argv[2];
const comoArquivo = process.argv.includes('--file');
const src = fs.readFileSync(arquivo, 'utf8');
const js = src.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/)[1];
const resumo = src.match(/<script type="text\/html" id="resumoSrc">([\s\S]*?)<\/script>/)[1];

const els = {};
const mk = (id) => els[id] || (els[id] = {
  id, innerHTML: '', textContent: id === 'resumoSrc' ? resumo : '',
  className: '', value: '', style: {}, attrs: {}, firstElementChild: { src: '' },
  setAttribute(k, v) { this.attrs[k] = v; },
  getAttribute(k) { return this.attrs[k] !== undefined ? this.attrs[k] : null; },
  removeAttribute(k) { delete this.attrs[k]; },
  insertAdjacentHTML(_, h) { this.innerHTML += h; },
});

const ctx = {
  window: { scrollTo() {}, addEventListener() {} },
  document: { addEventListener() {}, getElementById: mk },
  location: { protocol: comoArquivo ? 'file:' : 'https:' },
  console, JSON, Math, String, Array, Object, parseInt, isNaN, setTimeout,
};
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(js, ctx);

const A = ctx.A, S = ctx.S;
const hdr = () => els['hdr'].innerHTML;
const stage = () => els['stage'].innerHTML;
function ok(c, m) { if (!c) { console.error('FALHOU: ' + m); process.exit(1); } }

const alvo = comoArquivo ? '../index_local.html' : '../index.html';

// 1) link do indice presente em toda tela
ok(hdr().includes('href="' + alvo + '"'), 'home sem link para o indice (' + alvo + ')');
ok(/Materiais/.test(hdr()), 'o link do indice nao esta rotulado');
A.resumo();
ok(hdr().includes('href="' + alvo + '"'), 'resumo sem link para o indice');
A.home();
A.start();
ok(hdr().includes('href="' + alvo + '"'), 'quiz sem link para o indice');
console.log('  ok  link para o indice em todas as telas -> ' + alvo);

// 2) botao de sair durante o quiz
ok(/data-act="sair"/.test(hdr()), 'quiz sem botao de sair');
console.log('  ok  botao Sair presente durante o quiz');

// 3) sair preserva as respostas
A.go(0); A.pick(S.order[0].correctIndex);
A.go(1); A.pick(S.order[1].correctIndex === 0 ? 1 : 0);
A.go(2);
const respostasAntes = S.answers.slice();
const ordemAntes = S.order.map(q => q.id);
const iAntes = S.i;

A.sair();
ok(S.view === 'home', 'Sair nao voltou para a tela inicial');
ok(JSON.stringify(S.answers) === JSON.stringify(respostasAntes), 'Sair apagou as respostas');
console.log('  ok  Sair volta para a inicial sem perder respostas');

// 4) a home oferece retomar, e nao "comecar"
ok(/data-act="retomar"/.test(stage()), 'a tela inicial nao oferece retomar');
ok(/Em andamento/.test(stage()), 'a tela inicial nao sinaliza quiz em andamento');
ok(/recomeçar do zero/.test(stage()), 'faltou a saida para recomecar do zero');
console.log('  ok  tela inicial mostra Retomar + recomecar do zero');

// 5) retomar volta exatamente de onde parou, com a mesma ordem
A.retomar();
ok(S.view === 'quiz' && S.started, 'Retomar nao voltou para o quiz');
ok(S.i === iAntes, 'Retomar mudou a questao atual: ' + S.i + ' != ' + iAntes);
ok(JSON.stringify(S.answers) === JSON.stringify(respostasAntes), 'Retomar apagou as respostas');
ok(JSON.stringify(S.order.map(q => q.id)) === JSON.stringify(ordemAntes), 'Retomar reembaralhou o quiz');
console.log('  ok  Retomar mantem questao, respostas e ordem');

// 6) recomecar do zero realmente zera
A.start();
ok(S.answers.every(a => a === null), 'recomecar do zero nao limpou as respostas');
console.log('  ok  recomecar do zero limpa tudo');

// 7) sem nada respondido, a home volta a oferecer "Comecar"
A.sair();
ok(/data-act="start"/.test(stage()) && !/data-act="retomar"/.test(stage()),
   'quiz zerado ainda aparece como em andamento');
console.log('  ok  quiz zerado volta a oferecer Comecar');

console.log('PASSOU  ' + arquivo + (comoArquivo ? '  [file://]' : '  [https]'));
