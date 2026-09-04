/**
 * testar_chat.js — verifica o comportamento do chatbox do DeepSeek num DOM falso.
 *
 *   node testar_chat.js <quiz.html>
 *
 * Checa, com e sem a chave:
 *   1. sem chave (versao publicada): o chat NUNCA aparece
 *   2. com chave, acertando: nao aparece
 *   3. com chave, errando: aparece, com input e botao de enviar
 *   4. o historico sobrevive a sair da questao e voltar
 *   5. o envio monta o payload certo e a resposta entra no log
 */
const fs = require('fs');
const vm = require('vm');

const arquivo = process.argv[2];
const src = fs.readFileSync(arquivo, 'utf8');
const js = src.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/)[1];
const resumo = src.match(/<script type="text\/html" id="resumoSrc">([\s\S]*?)<\/script>/)[1];

function montar(chave, fetchImpl) {
  const els = {};
  const mkEl = (id) => els[id] || (els[id] = novoEl(id));
  function novoEl(id) {
    return {
      id,
      innerHTML: '',
      textContent: id === 'resumoSrc' ? resumo : '',
      className: '',
      value: '',
      style: {},
      attrs: {},
      firstElementChild: { src: '' },
      setAttribute(k, v) { this.attrs[k] = v; },
      getAttribute(k) { return this.attrs[k] !== undefined ? this.attrs[k] : null; },
      removeAttribute(k) { delete this.attrs[k]; },
      insertAdjacentHTML(_, html) { this.innerHTML += html; },
    };
  }
  const ctx = {
    window: { scrollTo() {}, addEventListener() {}, DEEPSEEK_KEY: chave },
    document: { addEventListener() {}, getElementById: mkEl },
    console,
    fetch: fetchImpl,
    TextDecoder: require('util').TextDecoder,
    setTimeout, JSON, Math, String, Array, Object, parseInt, isNaN,
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(js, ctx);
  return { ctx, els, mkEl };
}

function ok(c, m) { if (!c) { console.error('FALHOU: ' + m); process.exit(1); } }

const stage = (els) => els['stage'].innerHTML;

// ── 1) sem chave: o chat nunca deve existir ────────────────────────────────
{
  const { ctx, els } = montar(undefined, () => { throw new Error('nao deveria chamar fetch'); });
  ctx.A.start();
  const q = ctx.S.order[0];
  const errada = q.correctIndex === 0 ? 1 : 0;
  ctx.A.pick(errada);
  ok(!/id="ds"/.test(stage(els)), 'sem chave, o chat apareceu (vazaria na versao online)');
  ok(/Por quê/.test(stage(els)), 'a explicacao sumiu');
  ctx.A.go(3);
  ok(!/id="ds"/.test(stage(els)), 'questao ainda nao respondida nao deveria ter chat');
  console.log('  ok  sem chave -> nenhum chat (versao publicada limpa)');
}

// ── 2 e 3) com chave: so aparece quando erra ──────────────────────────────
{
  const { ctx, els } = montar('sk-teste-12345678901234567890', () => { throw new Error('nao chamou ainda'); });
  ctx.A.start();
  let q = ctx.S.order[0];
  ctx.A.pick(q.correctIndex);
  ok(/id="ds"/.test(stage(els)), 'acertou e o chat nao apareceu');
  ok(/Quer ir mais fundo\?/.test(stage(els)), 'no acerto a chamada do chat deveria ser a de aprofundar');
  console.log('  ok  com chave + acerto -> chat presente, com tom de aprofundar');

  ctx.A.go(1);
  q = ctx.S.order[1];
  const errada = q.correctIndex === 0 ? 1 : 0;
  ctx.A.pick(errada);
  ok(/id="ds"/.test(stage(els)), 'errou e o chat nao apareceu');
  ok(/Ainda com dúvida\?/.test(stage(els)), 'no erro a chamada do chat deveria ser a de duvida');
  ok(/id="dsIn"/.test(stage(els)), 'chat sem campo de digitacao');
  ok(/data-act="dsSend"/.test(stage(els)), 'chat sem botao de enviar');
  console.log('  ok  com chave + erro  -> chat com input e botao');
}

// ── 4 e 5) envio: payload correto, streaming e historico ──────────────────
{
  let capturado = null;
  const corpo =
    'data: {"choices":[{"delta":{"content":"Porque a "}}]}\n' +
    'data: {"choices":[{"delta":{"content":"curva e plana."}}]}\n' +
    'data: [DONE]\n';

  const fakeFetch = (url, opts) => {
    capturado = { url, opts };
    const bytes = Buffer.from(corpo, 'utf8');
    let enviado = false;
    return Promise.resolve({
      ok: true,
      body: { getReader: () => ({
        read: () => Promise.resolve(enviado ? { done: true } : (enviado = true, { done: false, value: bytes }))
      }) }
    });
  };

  const { ctx, els, mkEl } = montar('sk-teste-12345678901234567890', fakeFetch);
  ctx.A.start();
  ctx.A.go(2);
  const q = ctx.S.order[2];
  const errada = q.correctIndex === 0 ? 1 : 0;
  ctx.A.pick(errada);

  // o DOM falso nao parseia innerHTML, entao registramos os elementos do chat na mao
  mkEl('ds').setAttribute('data-qid', String(q.id));
  mkEl('dsIn').value = 'por que a minha esta errada?';
  mkEl('dsLog').innerHTML = '';

  ctx.A.dsSend();

  ok(capturado, 'nao chamou a API');
  ok(capturado.url.indexOf('api.deepseek.com') > -1, 'URL da API errada: ' + capturado.url);
  ok(capturado.opts.headers.Authorization === 'Bearer sk-teste-12345678901234567890', 'header de autorizacao errado');
  const payload = JSON.parse(capturado.opts.body);
  ok(payload.model === 'deepseek-v4-flash', 'modelo errado: ' + payload.model);
  ok(payload.stream === true, 'streaming desligado');
  const ctxMsg = payload.messages[1].content;
  ok(ctxMsg.indexOf(q.question) > -1, 'o enunciado nao foi enviado no contexto');
  ok(ctxMsg.indexOf(q.options[q.correctIndex]) > -1, 'a alternativa correta nao foi enviada');
  ok(ctxMsg.indexOf(q.options[errada]) > -1, 'a marcacao do estudante nao foi enviada');
  ok(payload.messages[payload.messages.length - 1].content === 'por que a minha esta errada?', 'a pergunta nao foi enviada');
  ok(mkEl('dsIn').value === '', 'o campo nao foi limpo apos enviar');
  console.log('  ok  envio -> payload com modelo, streaming, contexto da questao e pergunta');

  setTimeout(() => {
    // agora a bolha recebe markdown renderizado, entao a checagem e no innerHTML
    const saida = mkEl('dsTxt').innerHTML;
    ok(saida.indexOf('Porque a curva e plana.') > -1,
       'a resposta em streaming nao foi montada: ' + JSON.stringify(saida));
    ok(saida.indexOf('<p') > -1, 'a resposta nao passou pelo renderizador de markdown');
    const hist = ctx.S.chat[q.id];
    ok(hist.length === 2 && hist[1].role === 'assistant', 'historico nao guardou a resposta');
    console.log('  ok  streaming -> resposta montada e guardada em S.chat');

    // volta para a questao: o historico tem que reaparecer
    ctx.A.go(0); ctx.A.go(2);
    ok(/Porque a curva e plana\./.test(stage(els)), 'o historico nao sobreviveu a navegacao');
    console.log('  ok  historico sobrevive a sair da questao e voltar');
    console.log('PASSOU  ' + arquivo);
  }, 60);
}
