# CLAUDE.md — NexoHub Pubs

Esta pasta é a **linha de produção**: aula bruta → quiz + resumo → publicado no Nexo Hub.

O pipeline de verdade vive um nível acima (`../CLAUDE.md` e `../_scripts/`). Aqui fica
só o que é específico de **publicar no Hub** — a etapa que faltava.

---

## Saudação inicial obrigatória

Ao ser iniciado nesta pasta, rodar o levantamento e exibir:

```bash
cd ..
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Pubs/exportar_para_nexohub.py" --so-listar
```

```
NexoHub Pubs — da aula ao Nexo Hub.

[1] Processar aula nova     (extrair → quiz + resumo → HTML local)
[2] Exportar para o Hub     (gerar content_seed.json + catalogo.ts)
[3] Só conferir             (o que existe e o que sairia)

Prontos: [N] materiais · [Q] questões
```

Receber a escolha e seguir o caminho correspondente. Não pedir nova sessão.

---

## Infraestrutura

```bash
cd "D:/Arquivos/Documentos/Faculdade/OSEC/7sem/Material para provas"
PY="C:/Users/Fernando/AppData/Local/Programs/Python/Python314/python.exe"
```

Shell: **sempre Bash**, nunca PowerShell. Sempre com `PYTHONIOENCODING=utf-8`.

⚠️ Caminho com acento em argumento de Python quebra neste ambiente. Use glob do shell
(`GO/Aula\ 4*`) em vez de digitar o nome do arquivo.

---

## [1] Processar aula nova

Idêntico ao pipeline da pasta mãe — leia `../CLAUDE.md`, seção ETAPA 1 a 5. Em resumo:

```bash
PYTHONIOENCODING=utf-8 "$PY" _scripts/extrair.py "PED/Aula 9 - Tema.pptx" --titulo "Tema"
# agente escreve PED/aula_tema.json e PED/resumo_tema.md
PYTHONIOENCODING=utf-8 "$PY" _scripts/montar_quiz.py "PED/aula_tema.json" "PED/resumo_tema.md" \
  --imagens "PED/imagens_tema.json"
node _scripts/testar_quiz.js Quizzes/quiz_tema.html
PYTHONIOENCODING=utf-8 "$PY" _scripts/atualizar_indice.py
PYTHONIOENCODING=utf-8 "$PY" _scripts/atualizar_indice.py --local
```

As regras de elaboração (correta no índice 0, 130%, independência da aula, 4–8 imagens)
estão no `../CLAUDE.md` e o build as **recusa** quando violadas. Não reescreva as regras
aqui — um contrato em dois lugares vira dois contratos.

---

## [2] Exportar para o Hub

```bash
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Pubs/exportar_para_nexohub.py"
PYTHONIOENCODING=utf-8 "$PY" "NexoHub Pubs/exportar_para_nexohub.py" --disciplina PED
```

Sai em `NexoHub Pubs/saida/`:

| Arquivo | Para quê |
|---|---|
| `content_seed.json` | copiar para a raiz do NexoHub → Pass 2 do seed |
| `catalogo.ts` | colar na árvore de `prisma/seed.ts` → Pass 1 |

Depois, **no repositório do Hub** (`OSEC\Github\Repos\OSEC-HUBPROTOTYPE`):

```bash
python scripts/validar_quiz.py content_seed.json    # recusa antes de sujar o banco
npx prisma db seed
```

### Como o mapeamento é feito

| 7º semestre | Nexo Hub |
|---|---|
| pasta (`PED`, `OFTALMO`…) | **Disciplina** |
| `eyebrow` depois do `·` | **Especialidade** |
| `titulo` | **Tópico** |
| `aula_*.json` → `questoes[]` | `quizJson` |
| `resumo_*.md` → HTML | `relatorioHtml` |

A fonte é o **JSON**, nunca o HTML montado. O importador antigo do Hub
(`scripts/migrate_content.py`) fazia o contrário — recuperava as questões com regex de
`const rawQ = [...]` dentro do HTML publicado. O nome da variável mudou de template em
algum momento e hoje ele lê **1 repo de 59**. Foi exatamente por isso que aqui os
`aula_*.json` são a fonte e o HTML é produto descartável.

### Não crie repositório `[Tema]-quiz`

Era o fluxo antigo (um repo por tópico no GitHub Pages). O Hub hoje renderiza do banco:
`href={r.hasQuiz ? '/quiz/${slug}' : r.quizUrl}`, com `hasQuiz = quizJson !== null`.
O `quizUrl` é só fallback dos ~58 tópicos legados.

---

## Duas perdas conhecidas na exportação

O exportador **avisa** em cada caso, e as duas têm a mesma raiz: o Hub ainda não tem
para onde mandar imagem.

**1. Imagem nas questões some.** `src/app/quiz/[slug]/QuestoesClient.tsx` não renderiza
figura — o tipo `Question` não tem o campo e não há `<img>` no componente. Enquanto isso
não mudar, exportar questão com imagem entrega uma pergunta que fala de uma figura que
não aparece. O exportador tira o campo e conta quantas perdeu.

**2. Figura do resumo sai.** No HTML local a figura é base64 embutido; no Hub o
`relatorioHtml` é uma coluna do Postgres. Base64 ali incharia o banco e o payload.

Para recuperar as duas: subir as imagens para o **Vercel Blob** (o Hub já faz isso nos
relatórios antigos), guardar a URL absoluta e implementar o render. Até lá, o material
vai para o Hub em texto — o que ainda é o conteúdo inteiro das questões sem figura.

---

## Antes de publicar: procedência

O Hub é **produto**. Vale mais rigor do que no material local:

- **Foto de paciente** com autorização restrita ("uso estritamente acadêmico", "proibido
  reproduzir") não vai. Já aconteceu em Câncer em Pediatria — o material foi gerado sem
  imagem nenhuma, com vinhetas clínicas escritas no lugar.
- **Capítulo de livro e caderno de colega** são referência para escrever, nunca conteúdo
  publicado. O texto do tópico é original.
- Confira o `.gitignore` da pasta mãe antes de mover qualquer coisa.
