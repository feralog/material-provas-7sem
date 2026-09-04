/**
 * ler_quiz_publicado.js — extrai o array de questões de um quiz publicado.
 *
 *   node ler_quiz_publicado.js <caminho/index.html>
 *
 * Imprime JSON no stdout, ou {"erro": "..."}.
 *
 * Por que Node e não regex em Python: o array é um literal JavaScript (chaves sem
 * aspas, aspas simples, vírgula sobrando). Tentar convertê-lo para JSON com regex
 * corrompe qualquer string que contenha ", palavra:" no meio do texto — e explicação
 * clínica tem isso o tempo todo. Aqui quem interpreta JS é o JS.
 *
 * A avaliação acontece num contexto vazio do módulo `vm`: sem require, sem process,
 * sem rede. O array é dado, não programa.
 */
const fs = require('fs');
const vm = require('vm');

function main() {
  const arquivo = process.argv[2];
  if (!arquivo) return { erro: 'uso: node ler_quiz_publicado.js <index.html>' };

  let html;
  try { html = fs.readFileSync(arquivo, 'utf8'); }
  catch (e) { return { erro: 'nao consegui ler o arquivo: ' + e.message }; }

  // o nome da variavel mudou entre templates: rawQuestions (55 repos), rawQ (1)
  const m = html.match(/(?:const|var|let)\s+(rawQuestions|rawQ|QUIZ|questions)\s*=\s*(\[[\s\S]*?\])\s*;/);
  if (!m) return { erro: 'nenhum array de questoes reconhecido' };

  let dados;
  try {
    dados = vm.runInNewContext('(' + m[2] + ')', Object.create(null), { timeout: 5000 });
  } catch (e) {
    return { erro: `array em '${m[1]}' nao pode ser avaliado: ` + e.message };
  }
  if (!Array.isArray(dados)) return { erro: 'o que foi encontrado nao e um array' };

  // normaliza os dois dialetos de campo
  const questoes = dados.filter(q => q && typeof q === 'object').map(q => ({
    question: q.question ?? q.stem ?? '',
    options:  q.options  ?? q.alts ?? [],
    correct:  q.correct ?? q.answer ?? q.correctIndex ?? 0,
    explain:  q.explain ?? q.explanation ?? '',
    image:    q.image ?? q.imageKey ?? null,
  }));

  return { variavel: m[1], questoes };
}

process.stdout.write(JSON.stringify(main()));
