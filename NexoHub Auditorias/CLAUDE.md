# CLAUDE.md — NexoHub Auditorias

Esta pasta serve a **um** propósito: revisar conteúdo de quiz já produzido, matéria por
matéria. Aqui não se cria material nem se altera o pipeline — **audita-se**.

Quem roda aqui é o **DeepSeek** (os `.bat` trocam o endpoint). A ideia é ter um segundo
leitor, independente de quem escreveu as questões.

---

## Dois alvos, dois launchers

| Launcher | Alvo | O que audita |
|---|---|---|
| **`Auditar NexoHub.bat`** | `AUDITAR_ALVO=nexohub` | os **58 tópicos já publicados** no Nexo Hub — 1.566 questões |
| **`Auditar 7sem.bat`** | `AUDITAR_ALVO=7sem` | os **32 materiais do 7º semestre** — 1.123 questões, ainda não publicados |

**Primeira coisa a fazer:** descobrir por qual launcher você foi aberto.

```bash
echo "${AUDITAR_ALVO:-nao definido}"
```

Se a variável não existir, **pergunte** qual dos dois antes de seguir. Não adivinhe: são
acervos diferentes, e auditar o errado desperdiça a sessão inteira.

### Confirme que é o DeepSeek

O `.bat` já checa o endpoint antes de abrir e imprime `OK - respondendo como
deepseek-v4-pro`. Se não viu essa linha, ou se `/status` dentro da sessão mostrar um
modelo da Anthropic, **pare e avise** — auditar com o modelo que escreveu as questões
anula o propósito de ter um segundo leitor.

---

## Saudação inicial obrigatória

Rodar o seletor do alvo correto e exibir a saída, seguida do menu.

**Alvo `nexohub`:**
```bash
PYTHONIOENCODING=utf-8 "C:/Users/Fernando/AppData/Local/Programs/Python/Python314/python.exe" \
  "NexoHub Auditorias/nexohub_conteudo.py"
```

**Alvo `7sem`:**
```bash
cd ..
PYTHONIOENCODING=utf-8 "C:/Users/Fernando/AppData/Local/Programs/Python/Python314/python.exe" \
  "NexoHub Auditorias/listar_materiais.py"
```

```
NexoHub Auditorias — segundo leitor · alvo: [nexohub | 7sem]

[a saída do seletor, com as matérias numeradas]

Responda com os números (ex.: 1 3) ou 0 para todas.
Depois eu pergunto a profundidade.
```

Recebida a escolha, perguntar a profundidade e começar. **Não pedir nova sessão.**

```
Profundidade:
  [R] Rápida    — só o que é objetivo e verificável (roda o validador)
  [C] Clínica   — lê questão por questão e confere o mérito  (padrão)
  [F] Fundo     — clínica + confere contra o conteúdo extraído da aula
```

---

## Infraestrutura

```bash
cd "D:/Arquivos/Documentos/Faculdade/OSEC/7sem/Material para provas"
PY="C:/Users/Fernando/AppData/Local/Programs/Python/Python314/python.exe"
```

Shell: **sempre Bash**. Sempre `PYTHONIOENCODING=utf-8`.

### De onde vem o conteúdo em cada alvo

**`nexohub`** — `nexohub_conteudo.py` monta o acervo publicado:

- o catálogo Disciplina → Especialidade → Tópico sai de `prisma/seed.ts` do Hub;
- as questões saem dos repositórios `[Tema]-quiz` clonados em `OSEC\Github\Repos`,
  casados com o tópico pelo `quizUrl`.

É esse HTML que o Hub serve **hoje**: o `content_seed.json` nunca foi gerado, o banco não
tem `quizJson`, então `hasQuiz` é falso e a UI cai no `quizUrl`.

```bash
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Auditorias/nexohub_conteudo.py" --json 2      # para ler
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Auditorias/nexohub_conteudo.py" --extrair 2   # grava em extraido/
```

Em disciplina grande, prefira `--extrair` e depois leia o arquivo: `--json` joga tudo no
terminal e queima contexto à toa.

**`7sem`** — os arquivos-fonte, direto: `[Disc]/aula_[tema].json` (questões),
`[Disc]/resumo_[tema].md` (resumo) e `[Disc]/conteudo_[tema].md` (a aula extraída, que é
a fonte de verdade da profundidade **F**).

```bash
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Auditorias/listar_materiais.py" --json 1 4
```

### Duas coisas que o acervo publicado tem e o do 7º semestre não

- **A correta nem sempre está no índice 0.** No material do 7º semestre isso é regra
  imposta pelo build; nos quizzes antigos, não. Leia o campo `correct` de cada questão —
  não presuma.
- **Formato irregular entre repos.** O nome da variável mudou de template
  (`rawQuestions` em 55, `rawQ` em 1) e os campos também (`question/options/explanation`
  contra `stem/alts/correct/explain`). O extrator já normaliza tudo, e ainda junta os
  repos-coletânea, em que o `index.html` é só a capa e cada quiz mora num `quiz_*.html`
  ao lado. Você recebe sempre `question · options · correct · explain · image`.

---

## O que auditar

### Rápida — o que a máquina já decide

```bash
# alvo 7sem
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Pubs/exportar_para_nexohub.py"
PYTHONIOENCODING=utf-8 "$PY" \
  "D:/Arquivos/Documentos/Faculdade/OSEC/Github/Repos/OSEC-HUBPROTOTYPE/scripts/validar_quiz.py" \
  "NexoHub Pubs/saida/content_seed.json"

# alvo nexohub: extraia e valide o arquivo gerado
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Auditorias/nexohub_conteudo.py" --extrair 2
```

O validador cobre, sem julgamento: correta fora do índice 0, alternativa duplicada,
explicação vazia, desequilíbrio acima de 130%, referência à aula e imagem fora do padrão.

**Não gaste leitura com isso.** Se o validador passa, esses defeitos não existem — vá
direto ao que exige critério clínico.

### Clínica — o que só um leitor decide

Questão por questão, procurando:

1. **Erro de mérito** — a alternativa marcada como correta está clinicamente errada, ou
   há mais de uma defensável. É o achado mais grave: reporte sempre, com a fonte.
2. **Valor ou critério errado** — dose, ponto de corte, faixa etária, tempo, percentual.
   Confira os números; é onde mais aparece defeito.
3. **Explicação que não sustenta** — repete o enunciado, é vaga ("por definição"), ou
   justifica outra alternativa.
4. **Distrator inútil** — absurdo ou eliminável sem saber o assunto. Transforma 5 opções
   em 2 e infla a nota falsamente.
5. **Ambiguidade** — enunciado que admite mais de uma leitura, ou que depende de um dado
   que ele não fornece.
6. **Desatualização** — conduta ou nomenclatura superada por diretriz recente. No acervo
   publicado isso pesa mais: parte dele tem mais de um ano.
7. **Redundância** — duas questões que cobram exatamente a mesma coisa no mesmo tópico.

No resumo (só no alvo `7sem`), além disso: afirmação sem respaldo, tabela com valor
divergente do texto e tema que as questões cobram mas o resumo não explica.

### Fundo — contra a origem

O mesmo da clínica, mais o `conteudo_[tema].md` para conferir se a questão reflete o que
a aula ensinou. Divergência entre aula e literatura não é necessariamente erro — mas tem
que estar sinalizada na explicação, não escondida.

⚠️ Só existe no alvo **`7sem`**. O acervo publicado não guarda o material de origem;
naquele alvo, a referência é a literatura.

---

## Como reportar

Um arquivo por disciplina em `relatorios/`, nomeado
`auditoria_[alvo]_[disciplina]_[AAAA-MM-DD].md`.

```markdown
# Auditoria — [Disciplina]
Alvo · data · tópicos auditados · questões lidas · profundidade

## Resumo
[3 a 5 linhas: o estado geral e o padrão dos problemas, se houver]

## Achados

### [GRAVE] Hiperprolactinemia · Q7
**Problema:** a correta afirma que o TRH inibe a prolactina; o TRH estimula.
**Onde:** `Hiperprolactinemia-quiz`, questão 7
**Sugestão:** trocar a correta para "inibição pela dopamina" e ajustar a explicação.

### [MÉDIO] ...
### [MENOR] ...

## Sem achados
[tópicos lidos em que nada foi encontrado — dizer explicitamente]
```

Severidade: **GRAVE** = ensina errado (gabarito ou valor incorreto) · **MÉDIO** = prejudica
o estudo (explicação fraca, ambiguidade, distrator inútil) · **MENOR** = cosmético.

---

## Regras da auditoria

- **Não altere nada.** Nem `aula_*.json`, nem `resumo_*.md`, nem os repos `*-quiz`.
  Auditoria propõe; a correção é decidida depois, com o material aberto. Relatório é a
  entrega — e vale dobrado aqui, porque o modelo que audita não é o que escreveu.
- **Não mexa em `_scripts/`, `_template/` nem em `NexoHub Pubs/`.**
- **Toda acusação precisa de fundamento.** "Parece errado" não é achado. Diga qual é o
  valor certo e de onde vem. Na dúvida, marque como *dúvida*, não como erro — um falso
  positivo custa mais tempo do que um achado a menos.
- **Diga o que está certo.** Um relatório só com defeitos não informa se o material tem
  qualidade. Liste explicitamente o que foi lido e passou.
- **Não reescreva as questões.** Aponte e sugira em uma linha.

> Sobre volume: são 1.566 questões publicadas e 1.123 no 7º semestre. Auditar tudo de uma
> vez rende um relatório que ninguém lê, e estoura o contexto no meio. Uma disciplina por
> vez — é para isso que existe o seletor.
