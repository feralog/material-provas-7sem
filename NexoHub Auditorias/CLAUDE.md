# CLAUDE.md — NexoHub Auditorias

Esta pasta serve a **um** propósito: revisar o conteúdo já produzido, matéria por matéria,
antes de ele virar produto no Nexo Hub. Aqui não se cria material nem se altera o
pipeline — **audita-se**.

Quem roda aqui é o DeepSeek (o `.bat` desta pasta troca o endpoint). A ideia é ter um
segundo leitor, independente de quem escreveu as questões.

---

## Saudação inicial obrigatória

Ao ser iniciado nesta pasta, rodar o seletor e exibir a saída dele, seguida do menu:

```bash
cd ..
PYTHONIOENCODING=utf-8 "C:/Users/Fernando/AppData/Local/Programs/Python/Python314/python.exe" \
  "NexoHub Auditorias/listar_materiais.py"
```

```
NexoHub Auditorias — segundo leitor do conteúdo.

[a saída do seletor, com as matérias numeradas]

Responda com os números (ex.: 1 4 6) ou 0 para todas.
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

O seletor entrega os caminhos prontos, em JSON, para você não adivinhar nome de arquivo:

```bash
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Auditorias/listar_materiais.py" --json 1 4
```

Cada material tem dois arquivos: `[Disc]/aula_[tema].json` (as questões) e
`[Disc]/resumo_[tema].md` (o resumo). O conteúdo extraído da aula, quando existir, está
em `[Disc]/conteudo_[tema].md` — é a fonte de verdade para a profundidade **F**.

---

## O que auditar

### Rápida — o que a máquina já decide

```bash
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Pubs/exportar_para_nexohub.py" --so-listar
PYTHONIOENCODING=utf-8 "$PY" \
  "D:/Arquivos/Documentos/Faculdade/OSEC/Github/Repos/OSEC-HUBPROTOTYPE/scripts/validar_quiz.py" \
  "NexoHub Pubs/saida/content_seed.json"
```

Isso já cobre, sem julgamento: correta fora do índice 0, alternativa duplicada, explicação
vazia, desequilíbrio acima de 130%, referência à aula e imagem fora do padrão.

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
6. **Desatualização** — conduta ou nomenclatura superada por diretriz recente.
7. **Redundância** — duas questões que cobram exatamente a mesma coisa dentro do material.

No resumo, além disso: afirmação sem respaldo, tabela com valor divergente do texto e
lacuna de tema que as questões cobram mas o resumo não explica.

### Fundo — contra a origem

O mesmo da clínica, mais: abrir `conteudo_[tema].md` e conferir se a questão **reflete o
que a aula ensinou**. Divergência entre aula e literatura não é necessariamente erro —
mas tem que estar sinalizada na explicação, não escondida.

---

## Como reportar

Um arquivo por matéria em `relatorios/`, nomeado `auditoria_[disciplina]_[AAAA-MM-DD].md`.

```markdown
# Auditoria — [Disciplina]
Data · materiais auditados · questões lidas · profundidade

## Resumo
[3 a 5 linhas: o estado geral e o padrão dos problemas, se houver]

## Achados

### [GRAVE] Distúrbios da Tireoide · Q12
**Problema:** a correta afirma TSH > 20 mU/L; o corte do PNTN é > 10 mU/L.
**Onde:** `PED/aula_tireoide.json`, questão 12
**Sugestão:** trocar para "> 10 mU/L" e ajustar a explicação.

### [MÉDIO] ...
### [MENOR] ...

## Sem achados
[materiais lidos em que nada foi encontrado — dizer explicitamente]
```

Severidade: **GRAVE** = ensina errado (gabarito ou valor incorreto) · **MÉDIO** = prejudica
o estudo (explicação fraca, ambiguidade, distrator inútil) · **MENOR** = cosmético.

---

## Regras da auditoria

- **Não altere `aula_*.json` nem `resumo_*.md`.** Auditoria propõe; a correção é decidida
  depois, com o material aberto. Relatório é a entrega.
- **Não mexa em `_scripts/`, `_template/` nem em `NexoHub Pubs/`.**
- **Toda acusação precisa de fundamento.** "Parece errado" não é achado. Diga qual é o
  valor certo e de onde vem. Se estiver em dúvida, marque como *dúvida*, não como erro —
  um falso positivo custa mais tempo do que um achado a menos.
- **Diga o que está certo.** Um relatório só com defeitos não informa se o material tem
  qualidade. Liste explicitamente o que foi lido e passou.
- **Não reescreva as questões.** Aponte e sugira em uma linha.

> Sobre volume: são 1.123 questões em 32 materiais. Auditar tudo de uma vez rende um
> relatório que ninguém lê. Prefira uma matéria por vez — por isso o seletor.
