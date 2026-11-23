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
├── plano.html                    ← plano das provas finais (gerado, versionado)
├── Revisao/revisao_*.html        ← uma página de revisão por prova (gerado, versionado)
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
│   ├── testar_markdown.js        ← checa o markdown do chat (e que HTML do modelo não vira tag)
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
node _scripts/testar_markdown.js Quizzes/quiz_disacusias.html      # markdown do chat
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

## ETAPA 6 — Plano das provas e páginas de revisão por prova

```bash
PYTHONIOENCODING=utf-8 "$PY" _scripts/montar_plano.py --rever   # Revisao/revisao_*.html + plano.html
PYTHONIOENCODING=utf-8 "$PY" _scripts/montar_plano.py           # só o plano.html
```

`plano.html` é a linha do tempo dia a dia até a última prova (feita em 23/11/2026 para a
AVG 2026.2: SAI 30/11, PED 03/12, GO 08/12, MFC 10/12; 3 h por dia). O plano em si — dias,
itens, tempos, pegadinhas — está escrito em `DIAS`, `SOBRAR` e `PEGADINHAS` dentro do
script; mudou a prova ou chegou material, edite ali e rode de novo. O script avisa se
algum material das pastas de uma prova ficou sem lugar no plano.

`--rever` gera uma página de revisão por prova em `Revisao/` usando o
`montar_fechamento.py` de `7sem/Nova pagina pra provas` (fora do repo), com `--chave`
por prova (cada uma tem a própria fila de erros no navegador). Os itens do plano abrem
essas páginas já no modo certo: `#treino=<slug>`, `#simulado=<slugs>&n=&min=`, `#revisao`.
Rode `--rever` sempre que um `aula_*.json` mudar — senão a revisão fica com o banco velho.

Material marcado **Referência** no eyebrow não tem slide de aula: foi escrito de
referência padrão (DSM-5-TR, AHA, PCDT, políticas do SUS) a pedido do usuário, para aulas
cujo arquivo ele não conseguiu. MFC inteira é assim.

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

A resposta vem em markdown e é **renderizada** (`mdChat`): negrito, itálico, `código`,
listas, títulos, citação, divisor, bloco de código e tabela. A ordem é o que dá segurança —
`esc()` escapa **tudo** primeiro e só depois a formatação é aplicada, então nenhuma tag
vinda do modelo vira HTML de verdade. Só a mensagem do modelo é renderizada; a sua e as
de erro continuam texto puro.

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

---

## Pipeline de vídeo — o resumo vira aula narrada com legenda

> **Desde 19/11/2026 o pipeline de vídeo mora FORA desta pasta, em `7sem/Videos/`**
> (`D:/Arquivos/Documentos/Faculdade/OSEC/7sem/Videos`), e nada dele vai para o git:
>
> ```
> 7sem/Videos/
> ├── _scripts/   narrar.py · montar_video.py · conferir_narracao.py · indice_videos.py
> │               servidor_videos.py  (servidor só dos vídeos, com Range)
> ├── _fundos/    os .mp4 de gameplay sorteados como fundo
> ├── [Matéria]/  prosa_*.md + narracao_*.mp3 + tempos_*.json + [tema].mp4 + [tema].json
> ├── videos.html · Servidor de Videos.bat · ProtocoloVideo.md · SEM-VIDEO.md
> ```
>
> Rode os comandos abaixo **de dentro de `7sem/Videos`**. A prosa nova é escrita em
> `7sem/Videos/[Matéria]/prosa_[tema].md`, lendo o `resumo_[tema].md` daqui. O vídeo
> renderizado cai na mesma pasta da matéria (não há mais subpasta `Videos/`). Os vídeos
> do TCC ficam em `7sem/TCC/video/`, e o simulador de OSCE em `7sem/SimuladorProvasOSCE/`.

Segundo produto da mesma matéria-prima. O `resumo_[tema].md` é reescrito em prosa
corrida, narrado por TTS gratuito e montado sobre o gameplay de Minecraft, com a
legenda aparecendo em blocos de 2–3 palavras, no ritmo da fala.

```
resumo_[tema].md
    ├─▶ ETAPA A — agente reescreve  →  prosa_[tema].md   (cada '## ' vira capítulo)
    ├─▶ ETAPA B — narrar.py         →  narracao_[tema].mp3 + tempos_[tema].json
    ├─▶ ETAPA C — montar_video.py   →  Videos/[Matéria]/[tema].mp4 + .json
    └─▶ ETAPA D — indice_videos.py  →  videos.html   ← ARQUIVO FINAL
```

Um vídeo por aula (na prática 19 a 45 min), com **capítulos clicáveis** no índice — não se picota
em dezenas de arquivos. `videos.html` guarda onde você parou em cada vídeo.

### O achado que sustenta tudo

O `edge-tts` emite um evento `WordBoundary` com **o tempo e a duração de cada palavra**
(só com `boundary="WordBoundary"`; o padrão é `SentenceBoundary` e não serve). Com isso
a legenda sai do próprio TTS, já sincronizada — **sem Whisper, sem alinhamento forçado,
sem transcrever nada**.

### Infraestrutura adicional

- **edge-tts** (`pip install edge-tts`) — vozes neurais pt-BR da Microsoft, **sem chave,
  sem conta e sem custo**: `pt-BR-AntonioNeural` (padrão), `FranciscaNeural`,
  `ThalitaMultilingualNeural`. Ritmo padrão `+10%` — validado como confortável para 15+ min.
- **ffmpeg** 9.0.2 (`winget install Gyan.FFmpeg`) — os scripts localizam o binário
  sozinhos, inclusive no caminho do WinGet quando não está no PATH.
- **Fundo:** qualquer `.mp4` solto na raiz entra no sorteio (hoje três gameplays de
  parkour, somando ~5 h). A cada render sorteia-se **o arquivo e o ponto de início**
  dentro dele — os dois juntos, porque só um dos dois ainda deixaria os vídeos
  parecidos. Prefere fundo que cubra a narração sem repetir; se nenhum cobrir, usa o
  mais longo em loop. O par escolhido fica gravado no `.json` do vídeo. Para acrescentar
  um fundo, basta copiar o arquivo para a raiz. O recorte 9:16 é calculado da resolução
  real, então um 1080p entra sem ajuste.

### ETAPA A — contrato da `prosa_[tema].md`

```markdown
# Título da Aula

## Nome do capítulo
Texto corrido, sem marcação nenhuma...
```

**A legenda na tela é exatamente o texto que o TTS recebe.** Então o que for escrito
precisa, ao mesmo tempo, *ler* bem e *soar* bem. Daí as regras:

- **Prosa corrida, nunca bullet.** É narração, não tópico. Tabela do resumo vira frase.
- **Nada de markdown** — negrito, lista, tabela e imagem são removidos antes de narrar.
- **Escreva por extenso o que o TTS erraria:** `IV` → "endovenosa", `VO` → "por via oral",
  `12/12h` → "de doze em doze horas", `Monif IV` → "estágio quatro", `37,5 °C` →
  "trinta e sete e meio". Número solto pode ficar como algarismo.
- **Capítulos: mínimo 5, sem teto.** São marcadores clicáveis no player, então
  capítulo extra é barato e ajuda a navegar. **Nunca funda dois assuntos para caber
  num número** — um teto de 11 já virou restrição real e cinco materiais seguidos
  pararam exatamente nele. Com o teto solto, os materiais passaram a sair com 13 a 19.
- **Tom de storytelling**, com gancho no início de cada capítulo — mas o dado clínico
  (dose, critério, número) entra inteiro. É material de prova, não entretenimento.
- **Analogia e repetição são obrigatórias, não enfeite.** Mecanismo difícil (fisiopatologia,
  ação de droga, critério que confunde) ganha uma comparação concreta — *"é como se..."*,
  *"pense num..."*. E cada capítulo fecha retomando, em uma ou duas frases, o que não pode
  ser esquecido dali. **Repetir é recurso didático aqui**, e vale alongar o vídeo por isso:
  é a diferença entre ouvir e aprender. A analogia serve o dado, nunca o substitui.
- **Não existe teto de palavras.** O tamanho é consequência do material, não meta: um
  resumo denso em tabela gera prosa longa porque tabela vira frase, e frase é mais
  comprida que célula. Pôr um teto faz o agente enxugar justamente a camada didática —
  já aconteceu de um comprimir as retomadas e de outro **fundir dois capítulos** só para
  caber. O piso útil é ~1,5× as palavras do resumo-fonte; acima disso, deixe correr.

### ETAPAS B, C e D

```bash
cd "D:/Arquivos/Documentos/Faculdade/OSEC/7sem/Videos"
PYTHONIOENCODING=utf-8 "$PY" _scripts/narrar.py "GO/prosa_dip.md"            # --voz, --rate
PYTHONIOENCODING=utf-8 "$PY" _scripts/montar_video.py "GO/tempos_dip.json"   # --formato, --crf
PYTHONIOENCODING=utf-8 "$PY" _scripts/conferir_narracao.py GO                # audita as narrações
PYTHONIOENCODING=utf-8 "$PY" _scripts/indice_videos.py                       # sempre por último
```

**Rode o `conferir_narracao.py` antes de renderizar.** Ele compara, capítulo a capítulo,
o que foi falado com o que foi mandado falar — é a única checagem que pega stream truncado,
e renderizar 30 minutos de vídeo em cima de um áudio incompleto custa caro.

O `narrar.py` imprime **`desvio tempos x audio`** ao final. Esse número é o controle de
qualidade da sincronia: abaixo de 0,5 s está bom, acima disso a legenda desgarra da fala.

`--formato vertical` (720×1280, padrão) ou `landscape` (1280×720). O vertical recorta o
centro do gameplay; como o recorte tem só 405 px de largura, **não adianta subir para
1080×1920** — não há detalhe para revelar, só arquivo maior.

> **Atenção ao montar a fila:** o `tempos_*.json` leva o nome do **título** da prosa,
> não o nome do arquivo `prosa_*.md`. Eles coincidem quase sempre, e é justamente por
> isso que a exceção escapa: `OFTALMO/prosa_olho_vermelho.md` tem o título
> `# Diagnóstico Diferencial do Olho Vermelho`, então o tempos é
> `tempos_diagnostico_diferencial_do_olho_vermelho.json`. Montar a fila a partir do nome
> da prosa faz o render morrer com `ERRO: nao encontrei` — e, numa fila de sete itens
> com a saída filtrada, isso passa despercebido até alguém contar os vídeos. **Monte a
> fila listando os `tempos_*.json` que existem**, nunca derivando do nome da prosa:
>
> ```bash
> ls OFTALMO/tempos_*.json
> ```

### Os dois estilos de legenda — PERGUNTE ANTES DE RENDERIZAR

Existem dois, e o usuário escolhe. **Nunca renderize uma leva sem perguntar qual ele
quer** — refazer custa o encode inteiro de novo, e é a pergunta mais barata do pipeline.

| | **Limpo** (padrão) | **Com caixa** (`--caixa`) |
|---|---|---|
| Fundo | gameplay nítido | gameplay **desfocado** (sigma 8) |
| Atrás do texto | nada | retângulo arredondado claro, 50% de opacidade |
| Legenda | branca, contorno preto | **branca, contorno preto — igual** |
| Quando usa | o gameplay faz parte do apelo | quando a ênfase tem que estar no texto |

```bash
PYTHONIOENCODING=utf-8 "$PY" _scripts/montar_video.py "OFTALMO/tempos_glaucoma.json"
PYTHONIOENCODING=utf-8 "$PY" _scripts/montar_video.py "OFTALMO/tempos_glaucoma.json" --caixa
```

O estilo usado fica gravado no `.json` ao lado do vídeo, no campo `estilo`
(`"limpo"` ou `"caixa"`), então dá para saber depois o que cada vídeo recebeu e
re-renderizar só o que destoa.

**O texto continua branco nos dois.** Isso é contraintuitivo — caixa clara pede texto
escuro, e foi o que eu sugeri. O usuário assistiu aos dois renders de teste e discordou:
em movimento, o branco com contorno preto lê melhor sobre a caixa do que o texto escuro.
Quadro parado engana; vídeo rodando é o teste que vale. **Não "corrija" isso.**

A geometria da caixa está em `CAIXAS` no `montar_video.py` (640×190 raio 46 no vertical),
e ela é FIXA no centro — não acompanha o tamanho do texto. Legenda curta deixa a caixa
com folga nas laterais, e isso é esperado.

### Cinco armadilhas que já custaram caro

1. **`pont in ".!?;:"` é sempre verdadeiro quando `pont` é vazio** — string vazia é
   substring de qualquer string. O efeito foi cada palavra virar um bloco de legenda
   (64 palavras → 64 blocos). Tem que ser `pont and pont in "..."`.
2. **Não emende MP3 com bytes zerados.** Zero não é quadro MP3 válido: a pausa de 0,55 s
   saiu com ~1,9 s e a legenda desgarrou um pouco mais a cada capítulo. O jeito certo é
   gerar silêncio real no mesmo formato (24 kHz mono) e emendar com o `concat` do ffmpeg,
   calculando o offset de cada capítulo pela duração **medida** de cada trecho.
3. **Esticar o recorte infla o arquivo sem ganhar nitidez.** Subir 405 px para 1080
   triplicou o bitrate e dobrou o tamanho sem acrescentar um pixel de informação.
4. **O `desvio` NÃO detecta capítulo truncado — e o stream do edge-tts trunca.**
   Esta é a pior das cinco, porque falha em silêncio. Quando o stream corta no meio de
   uma seção, o áudio **e** os tempos das palavras param juntos: a soma continua coerente,
   o desvio fica em 0,33 s e o script imprime `ok`. Já saiu capítulo com **55% do texto**
   passando por esse check — sumiram epidemiologia, uma controvérsia inteira e o recap,
   e nada acusou. O desvio valida a *emenda* entre capítulos, não se o capítulo veio
   inteiro. O `narrar.py` agora compara a **última palavra falada** com a última palavra
   da seção e refaz a seção até 4 vezes, abortando se não conseguir; e o
   `conferir_narracao.py` audita narrações já feitas.
   Dois detalhes que custaram falso positivo: **não use contagem de palavras como
   critério** (o edge-tts agrupa número e sigla de outro jeito, e capítulo intacto
   aparece com 91%), e **compare por sufixo**, porque ele emite `"3 centímetros"` como
   um token só enquanto a prosa separa em duas palavras.
5. **Nunca indexe um render em andamento.** O `.mp4` existe desde o primeiro quadro, mas
   só vira arquivo válido no fim (o `+faststart` reescreve tudo, e sem o átomo `moov` o
   vídeo nem abre). Se houver um `.json` de um render anterior ao lado, o índice publica
   um vídeo truncado com **capítulos de outra versão** — e o erro é silencioso, porque
   a página carrega normalmente. O `indice_videos.py` agora pula a entrada quando o
   `.ass` ainda existe (o `montar_video.py` só o apaga ao terminar bem) ou quando o
   `.mp4` é mais novo que o `.json`. Pelo mesmo motivo, **não conclua que um render
   terminou só porque o `.mp4` está lá**: confira o `.ass` ou o `.json`.

### Assistir no celular — servidor da rede local

Duplo clique em **`Servidor de Videos.bat`**. Ele mostra o endereço; abra no navegador do
celular, no mesmo wi-fi. Fechar a janela (ou Ctrl+C) encerra.

```bash
cd "D:/Arquivos/Documentos/Faculdade/OSEC/7sem/Videos"
PYTHONIOENCODING=utf-8 "$PY" _scripts/servidor_videos.py              # porta 8000
PYTHONIOENCODING=utf-8 "$PY" _scripts/servidor_videos.py --porta 8080
```

**Não troque por `python -m http.server`.** O servidor embutido do Python não implementa
**Range requests**, e sem Range o navegador não consegue pular no meio do vídeo: clicar
num capítulo de um arquivo de 300 MB obriga a baixar tudo antes de tocar. Como capítulo
clicável é justamente o ponto do `videos.html`, o `servidor_videos.py` implementa Range
(responde `206` com a fatia pedida) e anuncia `Accept-Ranges: bytes`.

Ele serve **só a pasta `7sem/Videos`**: os quizzes, o TCC e o `deepseek_key.js` não estão
embaixo da raiz servida. Até 19/11 o mesmo `servidor.py` servia vídeos e simulador de OSCE,
e a trava do OSCE (visitante de fora só alcança o simulador) barrava o `videos.html` no
celular — por isso foram separados. O servidor do OSCE está em
`7sem/SimuladorProvasOSCE/_scripts/servidor.py`.

Na primeira execução o Windows pergunta sobre o firewall: permita em **redes privadas**.

### Espaço em disco

Um vídeo sai com ~11 MB por minuto no `--crf 32` padrão — um de 40 min dá ~450 MB (era 286 MB no crf 26; o gameplay de parkour é movimento rápido em tela cheia, o pior caso para compressão — e a legenda, por ser alto contraste, não sofre com CRF alto). Os 71 resumos, se todos virarem vídeo, passam
de 10 GB — por isso `Videos/`, `videos.html`, `narracao_*.mp3` e `tempos_*.json` estão
no `.gitignore`. **Tudo do pipeline de vídeo fica fora do repo** — inclusive as
`prosa_[tema].md`, os scripts (`narrar.py`, `montar_video.py`, `indice_videos.py`,
`conferir_narracao.py`), o `Servidor de Videos.bat` e os runbooks. Decisão do usuário
(19/11/2026): os vídeos existem só nesta máquina. Nunca faça commit de nada disso.

### Briefing do agente de prosa (reutilizar)

> Você vai transformar UM resumo em prosa narrada. Não altere `_template/` nem `_scripts/`.
> Shell: sempre Bash. Python: `PYTHONIOENCODING=utf-8 "$PY" ...`
>
> **Passo 1** — leia o `resumo_[tema].md` INTEIRO. Ele é a fonte; não invente conteúdo e
> não busque nada fora dele.
> **Passo 2** — escreva `prosa_[tema].md` seguindo o contrato acima. Mantenha todo dado
> clínico (dose, critério, número, nome de agente); o que muda é a forma, não o conteúdo.
> Tabela vira frase; bullet vira oração. Lembre que a legenda na tela é o seu texto.
> Use analogia onde o mecanismo for difícil e feche cada capítulo retomando o essencial.
> **Não enxugue para caber em tamanho nenhum** — não há teto, e cortar aqui corta didática.
> **Passo 3** — rode `narrar.py` e confira o `desvio` no fim. Acima de 0,5 s, reporte.
> **Passo 4** — rode `montar_video.py` e confirme que o `.mp4` e o `.json` foram criados.
> **Passo 5** — reporte: capítulos, palavras, duração, desvio, tamanho do arquivo e
> qualquer trecho do resumo que você não conseguiu converter sem perder informação.

## Notas

- **Bash only** — nunca PowerShell.
- O `.md` extraído é a fonte de verdade. Quiz raso quase sempre é `.md` ruim: volte à ETAPA 1.
- Nada aqui toca banco, GitHub ou Nexo Hub.
- Ao mexer no `quiz.html`, teste o JS antes de entregar: extraia o `<script>` final e rode
  `node --check`, e simule o fluxo com um DOM falso (o shuffle já quebrou o campo `image`
  uma vez — só o teste pegou).
