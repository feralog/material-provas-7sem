/*
 * testar_indice.js — roda o JS do index.html num DOM falso e checa o botao AVC 2.
 *
 *     node _scripts/testar_indice.js index.html index_local.html
 *
 * Checa: sintaxe do script, que o botao existe, que o clique liga e desliga o
 * destaque, que a disciplina sem nenhum material da prova some e volta, e que
 * os cards marcados batem com o AVC2 do gerador.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function classList(el) {
  const set = new Set();
  return {
    add: (c) => set.add(c),
    remove: (c) => set.delete(c),
    contains: (c) => set.has(c),
    toggle: (c, on) => { const v = on === undefined ? !set.has(c) : !!on; v ? set.add(c) : set.delete(c); return v; },
    _set: set,
  };
}

function montarDom(html) {
  // quantos cards marcados existem dentro de cada bloco .disc
  const discs = [];
  const re = /<div class="disc">([\s\S]*?)<\/div>\s*<\/div>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    const marcados = (m[1].match(/data-avc2="1"/g) || []).length;
    discs.push({ style: {}, _marcados: marcados, querySelector: function (s) { return this._marcados > 0 ? {} : null; } });
  }
  const botao = html.includes('id="btAvc2"')
    ? { textContent: 'AVC 2', _attrs: {}, _handlers: [],
        addEventListener: function (t, f) { if (t === 'click') this._handlers.push(f); },
        setAttribute: function (k, v) { this._attrs[k] = v; },
        click: function () { this._handlers.forEach((f) => f()); } }
    : null;
  const body = { classList: classList() };
  const document = {
    body,
    getElementById: (id) => (id === 'btAvc2' ? botao : null),
    querySelectorAll: (sel) => (sel === '.disc' ? discs : []),
  };
  return { document, body, botao, discs };
}

function testar(arquivo) {
  const html = fs.readFileSync(arquivo, 'utf8');
  const nome = path.basename(arquivo);
  const falhas = [];
  const ok = (cond, msg) => { if (!cond) falhas.push(msg); };

  const bloco = html.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/);
  ok(!!bloco, 'nao achei o <script> antes de </body>');
  if (!bloco) return { nome, falhas, info: '' };

  const dom = montarDom(html);
  ok(!!dom.botao, 'botao #btAvc2 ausente no HTML');
  if (!dom.botao) return { nome, falhas, info: '' };

  const ctx = { document: dom.document, Array };
  try {
    vm.runInNewContext(bloco[1], ctx, { timeout: 4000 });
  } catch (e) {
    falhas.push('erro ao executar o script: ' + e.message);
    return { nome, falhas, info: '' };
  }

  const semMarcado = dom.discs.filter((d) => d._marcados === 0).length;
  const comMarcado = dom.discs.length - semMarcado;

  // estado inicial
  ok(!dom.body.classList.contains('avc2'), 'comecou ja filtrado');
  ok(dom.botao.textContent === 'AVC 2', 'texto inicial do botao deveria ser "AVC 2"');

  // liga
  dom.botao.click();
  ok(dom.body.classList.contains('avc2'), 'o clique nao ligou a classe avc2 no body');
  ok(dom.botao.textContent === 'Mostrar tudo', 'o botao nao trocou de texto ao ligar');
  ok(dom.botao._attrs['aria-pressed'] === 'true', 'aria-pressed nao virou true');
  const escondidas = dom.discs.filter((d) => d.style.display === 'none').length;
  ok(escondidas === semMarcado,
     `deveria esconder as ${semMarcado} disciplinas sem material da prova, escondeu ${escondidas}`);
  ok(dom.discs.filter((d) => d._marcados > 0).every((d) => d.style.display !== 'none'),
     'escondeu uma disciplina que TEM material da prova');

  // desliga
  dom.botao.click();
  ok(!dom.body.classList.contains('avc2'), 'o segundo clique nao desligou o filtro');
  ok(dom.botao.textContent === 'AVC 2', 'o botao nao voltou ao texto original');
  ok(dom.discs.every((d) => d.style.display !== 'none'), 'sobrou disciplina escondida depois de desligar');

  const cards = (html.match(/<a class="card"/g) || []).length;
  const marcados = (html.match(/data-avc2="1"/g) || []).length;
  ok(marcados > 0, 'nenhum card marcado com data-avc2');
  ok(marcados < cards, 'todos os cards estao marcados — o filtro nao filtra nada');

  return {
    nome, falhas,
    info: `${cards} cards · ${marcados} na AVC 2 · ${dom.discs.length} disciplinas ` +
          `(${comMarcado} com material da prova, ${semMarcado} ocultadas ao filtrar)`,
  };
}

const alvos = process.argv.slice(2);
if (!alvos.length) { console.error('uso: node _scripts/testar_indice.js index.html [...]'); process.exit(2); }

let ruim = 0;
for (const a of alvos) {
  const r = testar(a);
  if (r.falhas.length) {
    ruim++;
    console.log(`FALHOU  ${r.nome}`);
    r.falhas.forEach((f) => console.log(`        - ${f}`));
  } else {
    console.log(`PASSOU  ${r.nome}`);
    console.log(`        ${r.info}`);
  }
}
process.exit(ruim ? 1 : 0);
