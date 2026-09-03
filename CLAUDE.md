# CLAUDE.md — Material para Provas (aula → quiz + resumo, num HTML local)

## O que este projeto faz

Pipeline **local e offline**. Nada de banco, GitHub Pages ou Nexo Hub.

```
Aula (PDF / PPTX / DOCX)
    │
    ├─▶ ETAPA 1 — extrair       →  conteudo_[tema].md  +  imagens_[tema].json
    │
    ├─▶ ETAPA 2 — 1 agente por aula, escrevendo:
    │                              aula_[tema].json    (metadados + questões)
    │                              resumo_[tema].md    (resumo de estudo)
    │
    ├─▶ ETAPA 3 — montar        →  Quizzes/quiz_[tema].html   ← ARQUIVO FINAL
    │
    └─▶ ETAPA 4 — index.html    →  índice clicável de todos os materiais
```

Cada HTML final é **autocontido**: abre com duplo clique e traz na tela inicial um
**seletor — Quiz ou Resumo**. As imagens vão embutidas em base64, então funciona
sem internet (só as fontes vêm do Google Fonts, com fallback para as do sistema).

**Toda aula processada daqui em diante sai com resumo e com imagens** — não são
extras opcionais, fazem parte do contrato e o build recusa material sem resumo.

---

## Saudação inicial obrigatória

Ao ser iniciado nesta pasta, exibir:

```
Material para provas — aula vira quiz + resumo num HTML local.

Me diga a aula (ou a pasta) que você quer processar.
Ex.: "PED/Aula 4 - Distúrbios da tireoide.pdf"  ou  "PED" (a pasta inteira)

Prontos: [listar Quizzes/*.html, ou "nenhum ainda"]
```

---

## Estrutura da pasta

```
Material para provas/
├── CLAUDE.md
├── index.html                    ← índice online   (gerado, versionado)
├── index_local.html              ← índice local    (gerado, NÃO versionado)
├── deepseek_key.js               ← chave do tutor  (NÃO versionado)
├── _template/
│   ├── quiz.html                 ← template real, vanilla JS, standalone
│   ├── Quiz Interativo.dc.html   ← design de origem (Claude Design) — REFERÊNCIA
│   ├── support.js / uploads/     ← runtime e insumos do Claude Design — NÃO usar
│   └── *.zip / .thumbnail
├── _scripts/
│   ├── extrair.py                ← aula → .md + imagens_*.json
│   ├── ver_pagina.py             ← acervo → .jpg de uma página, para a tool Read
│   ├── md2html.py                ← markdown do resumo → HTML
│   ├── montar_quiz.py            ← aula.json + resumo.md → HTML final
│   ├── testar_quiz.js            ← roda o HTML gerado num DOM falso e checa invariantes
│   ├── testar_chat.js            ← checa o tutor local (e que ele some sem a chave)
│   ├── testar_nav.js             ← checa voltar ao índice, sair e retomar sem perder nada
│   └── atualizar_indice.py       ← regenera index.html
├── Quizzes/
│   └── quiz_[tema].html          ← abrir e estudar
└── PED/  (e outras disciplinas)
    ├── Aula N - ....pdf          ← original
    ├── conteudo_[tema].md        ← texto extraído       (gerado)
    ├── imagens_[tema].json       ← acervo base64        (gerado, ~5 MB, não vai inteiro pro HTML)
    ├── aula_[tema].json          ← metadados + questões (escrito pelo agente)
    └── resumo_[tema].md          ← resumo               (escrito pelo agente)
```

---

## Infraestrutura

- **Python:** `C:/Users/Fernando/AppData/Local/Programs/Python/Python314/python.exe`
- **Libs:** `pdfplumber`, `PyMuPDF` (fitz), `python-docx`, `python-pptx` — todas instaladas.
- **REGRA DE SHELL:** sempre **Bash tool**, nunca PowerShell.
- Rodar com `PYTHONIOENCODING=utf-8` para não quebrar em acento.

```bash
cd "D:/Arquivos/Documentos/Faculdade/OSEC/7sem/Material para provas"
PY="C:/Users/Fernando/AppData/Local/Programs/Python/Python314/python.exe"
```

---

## ETAPA 1 — Extrair texto e imagens

```bash
PYTHONIOENCODING=utf-8 "$PY" _scripts/extrair.py "PED/Aula 4 - Tireoide.pdf"
PYTHONIOENCODING=utf-8 "$PY" _scripts/extrair.py "PED" --por-arquivo   # 1 par por aula

# vários arquivos = UM material só (slides + handout da mesma aula)
PYTHONIOENCODING=utf-8 "$PY" _scripts/extrair.py \
  "PED/Aula 7 - Diabetes.pptx" "PED/Aula 7 - Diabetes.pdf" --titulo "Diabetes Tipos 1 e 2"
```

Gera dois arquivos por material:

| Arquivo | Conteúdo |
|---|---|
| `conteudo_[tema].md` | texto por página/slide, com marcador `<!-- IMG:chave -->` ao fim de cada um |
| `imagens_[tema].json` | `{"chave": "<base64 JPEG>", ...}` — o acervo |

Flags: `--titulo` · `--sem-imagens` · `--largura 1600` · `--saida` · `--por-arquivo`.

### PDF × PPTX — prefira o PPTX

Quando a aula existir nos dois formatos, **extraia do `.pptx`**. A extração de PDF
embaralha slides de múltiplas colunas e perde tabelas inteiras; a de PPTX lê a estrutura
real do arquivo e sai muito mais limpa:

| | PDF | PPTX |
|---|---|---|
| Texto | por página, colunas frequentemente intercaladas | por shape, em ordem de leitura, com níveis de bullet |
| Tabelas | viram texto solto ou somem | saem como **tabela markdown** |
| Notas do apresentador | não existem | **extraídas** — costumam trazer o raciocínio clínico |
| Imagens | página inteira renderizada (1200 px) | figuras embutidas, já normalizadas para 1200 px |

Não é preciso converter PPTX para PDF. E **passe também o handout**, quando houver:
material que não é a aula ainda é referência de estudo, e às vezes traz o critério fechado
que o slide só menciona.

### As duas famílias de chave de imagem

| Chave | Origem |
|---|---|
| `pgNN` | página NN de um **PDF**, renderizada inteira |
| `sNNiK` | K-ésima imagem embutida no **slide NN** de um PPTX |

As duas convivem no mesmo acervo sem colidir. O extrator de PPTX ainda: percorre grupos
recursivamente, ordena as shapes por posição, **descarta imagem repetida em 4+ slides**
(logo/marca d'água), **deduplica** por hash e **reduz** cada figura para 1200 px em JPEG —
sem isso o HTML final passaria de 10 MB.

**O acervo de imagens é grande (~5 MB) de propósito** — extrai tudo, e o `montar_quiz.py`
embute no HTML final só as que forem referenciadas. Não tente economizar aqui.

**Leia os AVISOS.** Páginas listadas como sem texto nativo são slides-imagem: o conteúdo
delas só existe na imagem. Veja abaixo como olhá-las.

### Como VER uma página (importante)

⚠️ **A tool `Read` NÃO renderiza PDF neste ambiente** — falha com
`pdftoppm is not installed` (poppler-utils ausente). Não perca tempo tentando.

Use o helper, que decodifica a página já renderizada no acervo:

```bash
# aceita número de página, intervalo e chave de slide
PYTHONIOENCODING=utf-8 "$PY" _scripts/ver_pagina.py "PED/imagens_tireoide.json" 16 33 15-18
PYTHONIOENCODING=utf-8 "$PY" _scripts/ver_pagina.py "PED/imagens_diabetes.json" s16i1 pg03
```

Ele grava os `.jpg` e imprime os caminhos — aí sim use a tool `Read` **nos .jpg**.
`--listar` mostra as chaves disponíveis; `--out` escolhe a pasta.

Isso não é contorno improvisado: o `extrair.py` já renderizou tudo, o helper só
decodifica. É o caminho padrão para conferir slide de tabela, fluxograma ou coluna
que a extração de texto embaralhou.

---

## ETAPA 2 — Um agente por aula

Para várias aulas, dispare **um agente por aula, em paralelo**, com o briefing abaixo.
Cada agente escreve dois arquivos e roda o build até passar. O agente NÃO altera
`_template/` nem `_scripts/`.

### Contrato — `PED/aula_[tema].json`

```json
{
  "titulo":    "Distúrbios da Tireoide",
  "eyebrow":   "Pediatria · Endocrinologia",
  "subtitulo": "Frase de 6 a 12 palavras que abre a tela inicial",
  "intro":     "1 a 3 linhas dizendo o que o material cobre",
  "questoes": [
    {
      "question":     "Enunciado completo?",
      "options":      ["ALTERNATIVA CORRETA", "distrator", "distrator", "distrator"],
      "correctIndex": 0,
      "explanation":  "Por que a correta está certa (2 a 4 frases, com o dado concreto).",
      "image":        "pg30",
      "imageCaption": "Fluxograma diagnóstico"
    }
  ]
}
```

Regras — **25 a 30 questões** por aula (35 a 45 se for material de revisão ampla):

- A correta é **SEMPRE `options[0]`**, `correctIndex: 0`. O navegador embaralha na exibição.
- 4 ou 5 alternativas, consistente dentro da mesma aula.
- **Equalização:** nenhuma alternativa pode passar de **130% do comprimento da mais curta
  do grupo**. O build bloqueia. Correta longa → jogue a justificativa no `explanation`.
  Distrator curto → espelhe a estrutura da correta com valores errados.
- Distratores clinicamente plausíveis. Alternativa absurda transforma 5 opções em 2.
- Mesmo estilo sintático no grupo — nunca frase completa misturada com fragmento.
- `explanation` nunca vazio (o build recusa).
- **Independente da aula** — quem estuda pelo quiz não assistiu à aula. Nada de
  "segundo a aula", "no slide", "no gabarito", "o professor destaca", "no material".
  Traga o dado para dentro do enunciado: *"A iatrogenia é classificada em quatro
  tipos"*, não *"A aula organiza a iatrogenia em quatro tipos"*. Vale para enunciado,
  alternativa e explicação — o build bloqueia (`validar_independencia`). Se a questão
  só existe como "o que a aula disse", sem valor clínico próprio, remova.

Imagens nas questões (`image` + `imageCaption`, opcionais):
- **4 a 8 questões** com imagem, só onde a imagem **é o objeto da pergunta**: fluxograma,
  curva, tabela, estadiamento, escala, sinal clínico. Nunca em slide decorativo.
- Chave = página do PDF, com zero à esquerda: página 7 → `"pg07"`.
- **Confirme a página com `Read` antes de referenciar** — chave errada é erro de build,
  mas imagem errada passa despercebida.
- A questão tem que ser respondível olhando a imagem.

### Contrato — `PED/resumo_[tema].md`

Texto corrido, como capítulo de livro, com densidade de prova. Não é bullet solto.

Markdown suportado (`_scripts/md2html.py` — só isto, nada de HTML cru):

| Sintaxe | Vira |
|---|---|
| `## Seção` | seção — **5 a 9 por aula**, e é o que a tela inicial conta |
| `### Sub` / `#### Rótulo` | subtítulo / rótulo mono azul |
| `- item` / `1. item` | lista (um nível de aninhamento) |
| `\| a \| b \|` + `\| --- \|` | tabela |
| `> texto` | callout azul destacado — use para ponto-chave e pegadinha |
| `---` | divisor |
| `**negrito**` `*itálico*` `` `código` `` | inline |
| `![legenda](img:pg30)` sozinha na linha | figura da página 30 — **3 a 6 por resumo** |

### Briefing do agente (reutilizar)

> Você vai produzir o material de estudo de UMA aula. Não altere `_template/` nem `_scripts/`.
> Shell: sempre Bash. Python: `PYTHONIOENCODING=utf-8 "$PY" ...`
>
> **Passo 1** — leia o `conteudo_[tema].md` INTEIRO; é a fonte de verdade. Onde o texto
> estiver truncado, com colunas embaralhadas ou marcado `_(slide sem texto)_`, gere o
> `.jpg` da página com `_scripts/ver_pagina.py <acervo> <páginas>` e leia esse `.jpg`
> com a tool `Read`. **Não tente `Read` no PDF — falha por falta de poppler.**
> Não invente conteúdo.
> **Passo 2** — escreva `aula_[tema].json` (contrato acima).
> **Passo 3** — escreva `resumo_[tema].md` (contrato acima).
> **Passo 4** — rode o `montar_quiz.py` e **itere até sair `OK`**. Não use `--forcar`.
> **Passo 5** — reporte questões, seções, imagens, tamanho e quais páginas você teve
> que ler pelo PDF porque a extração falhou.

---

## ETAPA 3 — Montar o HTML

```bash
PYTHONIOENCODING=utf-8 "$PY" _scripts/montar_quiz.py \
  "PED/aula_tireoide.json" "PED/resumo_tireoide.md" \
  --imagens "PED/imagens_aula_4_disturbios_da_tireoide.json"
```

`--imagens` é necessário quando o nome do acervo não bate com `imagens_<snake(titulo)>.json`
(quase sempre, porque o título é limpo e o nome do arquivo original não). Na dúvida, passe.

O script **valida e aborta** se houver: alternativas fora de 4–6, `correctIndex ≠ 0`,
alternativas duplicadas, enunciado ou explicação vazios, **referência à aula**
("segundo a aula", "no slide", "no gabarito"), resumo sem nenhuma seção `##`,
chave de imagem inexistente, placeholder não substituído. Desequilíbrio de comprimento
sai como *aviso* que também bloqueia — liberável com `--forcar`, mas o certo é corrigir.

Saída: `Quizzes/quiz_[titulo_snake].html`, tipicamente 1–3 MB com as imagens embutidas.

---

## ETAPA 4 — Testar o HTML gerado

```bash
node _scripts/testar_quiz.js Quizzes/*.html      # fluxo do quiz, resumo, gabarito
node _scripts/testar_chat.js Quizzes/quiz_disacusias.html   # o tutor local
node _scripts/testar_nav.js  Quizzes/quiz_disacusias.html --file   # voltar/sair/retomar
```

Roda o quiz num DOM falso e checa: sintaxe do JS, seletor na tela inicial, seções e
figuras do resumo, fluxo completo do quiz, aviso de questões em branco, contadores,
os quatro filtros do gabarito, imagem sobrevivendo ao embaralhamento e gabarito
íntegro em 30 embaralhamentos. Sai com código 1 se algum arquivo falhar.

**Rode sempre.** Foi assim que apareceu o bug do embaralhamento descartando o campo
`image` — visualmente o quiz parecia certo, só as figuras sumiam.

O `testar_chat.js` checa o que mais importa no tutor: **sem a chave o chat não é
renderizado** (é isso que mantém a versão publicada limpa), com a chave ele só aparece
quando a questão foi errada, o payload leva o contexto certo da questão, o streaming
remonta a resposta e o histórico sobrevive à navegação.

---

## ETAPA 5 — Atualizar os índices

São **dois**, e os dois saem do mesmo script:

```bash
PYTHONIOENCODING=utf-8 "$PY" _scripts/atualizar_indice.py            # index.html       (online)
PYTHONIOENCODING=utf-8 "$PY" _scripts/atualizar_indice.py --local    # index_local.html (máquina)
```

Sempre por último. `index_local.html` é ignorado pelo git — é o arquivo que se abre
por duplo clique em casa; `index.html` é o que vai para o GitHub Pages.

---

## O tutor DeepSeek — só na máquina, nunca no site

Respondeu a questão? Abaixo da explicação aparece um chat para perguntar a um modelo —
tanto no erro quanto no acerto (acertar chutando também rende dúvida). Ele manda o
enunciado, as alternativas, a correta, o que você marcou e a explicação que já existe,
então a resposta vem em cima da sua dúvida, não do zero. O contexto entra **uma vez**,
na abertura da conversa: nas mensagens seguintes você escreve só a pergunta e o modelo
continua enxergando a questão. Trocar de questão abre um chat novo, sem memória do anterior.

O tom se adapta: no erro a chamada é *"Ainda com dúvida?"* e o system prompt diz que o
estudante errou; no acerto é *"Quer ir mais fundo?"* e diz que ele acertou mas ficou com
dúvida — evita que o modelo explique como se ele tivesse errado.

**A chave nunca entra no HTML.** O quiz carrega `<script src="../deepseek_key.js">`,
um arquivo que existe só localmente e está no `.gitignore`:

```js
window.DEEPSEEK_KEY = "sk-...";
```

Online esse arquivo dá 404, `dsOn()` vira `false` e o chat simplesmente não é
renderizado. **Um único conjunto de HTMLs serve aos dois mundos** — não há build
duplicado nem risco de publicar a chave por engano.

| | Local | Publicado |
|---|---|---|
| `deepseek_key.js` | existe (ignorado pelo git) | 404 |
| Chat ao errar | aparece | não existe |
| Arquivos de quiz | **os mesmos** | **os mesmos** |

Detalhes: modelo `deepseek-v4-flash`, endpoint `https://api.deepseek.com/chat/completions`,
resposta em streaming (a API devolve CORS com `access-control-allow-origin` refletido,
então funciona até de `file://`). O histórico vive em `S.chat[idDaQuestão]` e sobrevive
ao re-render do stage — dá para sair da questão e voltar sem perder a conversa. O
atalho de teclado `1`–`6` é ignorado enquanto o foco está no campo de texto.

Trocar a chave = editar `deepseek_key.js`. Não precisa regerar nada.

---

## O que o HTML final entrega

Tela inicial com **seletor: Quiz ou Resumo**.

A barra do topo traz sempre **← Materiais**, que volta para o índice — `index_local.html`
quando o arquivo foi aberto por duplo clique (`file://`), `index.html` quando veio da web.
Durante o quiz há também **Sair**, que devolve à tela inicial **sem perder as respostas**:
a tela inicial passa a oferecer *Retomar* (mesma questão, mesma ordem, mesmas respostas) e,
como saída explícita, *recomeçar do zero*.

**Quiz** — navegação livre (não é linear): trilha clicável no topo com uma marca por
questão (verde/vermelho/cinza), setas ← →, teclas 1–6 para responder, Enter para avançar,
explicação imediata ao responder, aviso antes de finalizar com questões em branco.
Resultado com contadores, **gabarito comentado** filtrável (todas / erradas / certas /
em branco), acordeão por questão e "abrir no quiz" para voltar a qualquer uma.

**Resumo** — texto corrido com tipografia serifada, tabelas, callouts e figuras.

Clique em qualquer figura abre em tela cheia (Esc fecha).

---

## Sobre o template

`_template/quiz.html` é uma **porta vanilla JS** do design em `Quiz Interativo.dc.html`.
O `.dc.html` original é um componente do Claude Design: depende de `support.js`, que
baixa React 18 + ReactDOM + Babel do unpkg.com em tempo de execução — ou seja, **não abre
offline e não é standalone**. Por isso ele fica só como referência de design; o arquivo
que o pipeline usa é o `quiz.html`.

Três placeholders, mais o bloco do resumo:

| Placeholder | Vira |
|---|---|
| `__TITLE__` `__EYEBROW__` `__SUBTITLE__` `__INTRO__` | textos da tela inicial e do topo |
| `__QUIZ__` | array JSON das questões |
| `__RESUMO__` | HTML do resumo, dentro de `<script type="text/html" id="resumoSrc">` |

Mudança de layout se faz **no template, uma vez**, e depois é só regerar os HTMLs — os
`aula_*.json` e `resumo_*.md` ficam salvos justamente para isso.

---

## Notas

- **Bash only** — nunca PowerShell.
- O `.md` extraído é a fonte de verdade. Quiz raso quase sempre é `.md` ruim: volte à ETAPA 1.
- Nada aqui toca banco, GitHub ou Nexo Hub.
- Ao mexer no `quiz.html`, teste o JS antes de entregar: extraia o `<script>` final e rode
  `node --check`, e simule o fluxo com um DOM falso (o shuffle já quebrou o campo `image`
  uma vez — só o teste pegou).
