# Material para provas — 7º semestre

Quiz e resumo de cada aula, num arquivo HTML só, que abre offline no navegador.

**→ [Abrir](https://feralog.github.io/material-provas-7sem/)**

---

## O que tem

| Disciplina | Materiais | Questões |
|---|---|---|
| Pediatria | 8 | 356 |
| Ginecologia e Obstetrícia | 5 | 170 |
| Oftalmologia | 5 | 152 |
| Otorrinolaringologia | 4 | 127 |
| Geriatria | 3 | 98 |
| Psiquiatria | 3 | 89 |
| Neurologia | 2 | 60 |
| **Total** | **30** | **1052** |

Mais 261 seções de resumo e 194 imagens nas questões.

Cada material abre com um seletor: **fazer o quiz** ou **ler o resumo**.

O quiz tem navegação livre — trilha clicável com uma marca por questão, setas para
andar, teclas `1`–`6` para responder, `Enter` para avançar. A explicação aparece assim
que você responde, e no fim há um gabarito comentado filtrável por certas, erradas e
em branco. As questões e as alternativas são embaralhadas a cada execução.

O resumo é texto corrido com tabelas, destaques e figuras. Clicar numa figura amplia.

---

## Como é gerado

```
Aula (PDF / PPTX)
    │
    ├─▶ extrair.py        →  conteudo_[tema].md  +  imagens_[tema].json
    │
    ├─▶ (redação)         →  aula_[tema].json    +  resumo_[tema].md
    │
    ├─▶ montar_quiz.py    →  Quizzes/quiz_[tema].html   ← arquivo final
    │
    ├─▶ testar_quiz.js    →  checa o HTML gerado
    │
    └─▶ atualizar_indice.py → index.html
```

O passo de redação lê o `.md` extraído e as figuras das páginas que a extração de texto
não alcança — em várias aulas, tabelas e fluxogramas inteiros só existem como imagem.

`CLAUDE.md` traz o pipeline completo, com os contratos de dados e as regras de
elaboração das questões.

## O que não está aqui

Os PDFs e PPTXs originais das aulas e os acervos `imagens_*.json` ficam fora do
repositório — são 135 MB e regeneráveis. Os HTMLs publicados já trazem as imagens
embutidas, então funcionam sozinhos.

Para regerar do zero é preciso ter o material original e rodar o `extrair.py`.
