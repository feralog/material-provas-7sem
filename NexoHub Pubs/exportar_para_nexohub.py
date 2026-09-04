#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exportar_para_nexohub.py — leva os materiais do 7º semestre para o Nexo Hub.

    python "NexoHub Pubs/exportar_para_nexohub.py"                  # tudo
    python "NexoHub Pubs/exportar_para_nexohub.py" --disciplina PED  # só uma
    python "NexoHub Pubs/exportar_para_nexohub.py" --so-listar       # não escreve nada

Lê os `aula_*.json` + `resumo_*.md` (o dado estruturado, não o HTML montado) e
escreve dois arquivos em `NexoHub Pubs/saida/`:

    content_seed.json   →  copiar para a raiz do NexoHub e rodar `npx prisma db seed`
    catalogo.ts         →  trecho para colar em prisma/seed.ts (Pass 1)

Por que não reaproveitar o migrate_content.py do Hub: ele recupera as questões
extraindo `const rawQ = [...]` do HTML publicado com regex. O nome da variável
mudou de template em algum momento e hoje ele lê 1 repo de 59. Aqui a fonte é o
JSON — o HTML é produto descartável, não fonte.

Contrato de saída (o que src/app/quiz/[slug]/page.tsx lê):
    question · options · correct · explain
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "_scripts"))
from md2html import md2html  # noqa: E402

SAIDA = Path(__file__).resolve().parent / "saida"

DISCIPLINAS = {
    "PED": "Pediatria",
    "GO": "Ginecologia e Obstetrícia",
    "Geriatria": "Geriatria",
    "Neurologia": "Neurologia",
    "Psiquiatria": "Psiquiatria",
    "Otorrino": "Otorrinolaringologia",
    "OFTALMO": "Oftalmologia",
}


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    return re.sub(r"[\s_]+", "-", s).strip("-") or "topico"


def especialidade(eyebrow: str, disciplina: str) -> str:
    """'Pediatria · Endocrinologia' -> 'Endocrinologia'."""
    partes = [p.strip() for p in eyebrow.split("·")]
    return partes[-1] if len(partes) > 1 and partes[-1] else disciplina


def resumo_para_html(md_path: Path):
    """Resumo -> HTML do relatório. Devolve (html, nº de figuras descartadas).

    As figuras do resumo são chaves do acervo local, que viram base64 no HTML
    offline. No Hub isso seria base64 dentro de uma coluna do Postgres — as
    figuras saem, e a imagem só volta quando forem para o Vercel Blob.
    """
    html = md2html(md_path.read_text(encoding="utf-8"))
    html, n = re.subn(r"<figure class=\"fig\">.*?</figure>", "", html, flags=re.S)
    return html, n


def coletar(disciplina_filtro=None):
    itens, avisos = [], []

    for aula_json in sorted(RAIZ.glob("*/aula_*.json")):
        pasta = aula_json.parent.name
        if pasta not in DISCIPLINAS:
            continue
        if disciplina_filtro and pasta != disciplina_filtro:
            continue

        resumo_md = aula_json.parent / aula_json.name.replace("aula_", "resumo_").replace(".json", ".md")
        if not resumo_md.exists():
            avisos.append(f"{aula_json.name}: sem resumo correspondente — pulado")
            continue

        d = json.loads(aula_json.read_text(encoding="utf-8"))
        titulo = d["titulo"]
        disciplina = DISCIPLINAS[pasta]

        questoes, com_img = [], 0
        for q in d["questoes"]:
            if q.get("image"):
                com_img += 1
            # 'correct' é o campo que a rota lê primeiro; 'correctIndex' ela ignora
            questoes.append({
                "question": q["question"],
                "options": q["options"],
                "correct": 0,
                "explain": q["explanation"],
            })

        html, figs = resumo_para_html(resumo_md)

        if com_img:
            avisos.append(f"{titulo}: {com_img} questões perderam a imagem "
                          f"(QuestoesClient.tsx ainda não renderiza figura)")
        if figs:
            avisos.append(f"{titulo}: {figs} figuras saíram do relatório "
                          f"(base64 não entra em coluna do Postgres — usar Vercel Blob)")

        itens.append({
            "slug": slugify(titulo),
            "nome": titulo,
            "disciplina": disciplina,
            "especialidade": especialidade(d["eyebrow"], disciplina),
            "quizJson": questoes,
            "relatorioHtml": html,
        })

    return itens, avisos


def montar_catalogo(itens) -> str:
    """Trecho de prisma/seed.ts (Pass 1), agrupado por disciplina e especialidade."""
    arvore = {}
    for it in itens:
        arvore.setdefault(it["disciplina"], {}).setdefault(it["especialidade"], []).append(it["nome"])

    linhas = ["// ── 7º semestre — gerado por NexoHub Pubs/exportar_para_nexohub.py ──",
              "// Sem relatorioUrl/quizUrl: o conteúdo vem do banco, via content_seed.json.",
              ""]
    for disc in sorted(arvore):
        linhas.append("{")
        linhas.append(f"  name: {json.dumps(disc, ensure_ascii=False)},")
        linhas.append("  specialties: [")
        for esp in sorted(arvore[disc]):
            linhas.append("    {")
            linhas.append(f"      name: {json.dumps(esp, ensure_ascii=False)},")
            linhas.append("      topics: [")
            for nome in sorted(arvore[disc][esp]):
                linhas.append(f"        {{ name: {json.dumps(nome, ensure_ascii=False)} }},")
            linhas.append("      ],")
            linhas.append("    },")
        linhas.append("  ],")
        linhas.append("},")
    return "\n".join(linhas) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Exporta os materiais do 7º semestre para o Nexo Hub")
    ap.add_argument("--disciplina", help="sigla da pasta (PED, GO, OFTALMO, Otorrino...)")
    ap.add_argument("--so-listar", action="store_true", help="mostra o que sairia, sem escrever")
    args = ap.parse_args()

    if args.disciplina and args.disciplina not in DISCIPLINAS:
        sys.exit(f"ERRO: disciplina '{args.disciplina}' desconhecida. "
                 f"Use uma de: {', '.join(sorted(DISCIPLINAS))}")

    itens, avisos = coletar(args.disciplina)
    if not itens:
        sys.exit("ERRO: nenhum material encontrado")

    print(f"{'disciplina':<26} {'especialidade':<30} {'q':>3}  tópico")
    print("-" * 92)
    for it in sorted(itens, key=lambda x: (x["disciplina"], x["especialidade"], x["nome"])):
        print(f"{it['disciplina']:<26} {it['especialidade'][:30]:<30} "
              f"{len(it['quizJson']):>3}  {it['nome']}")

    total_q = sum(len(i["quizJson"]) for i in itens)
    print("-" * 92)
    print(f"{len(itens)} tópicos · {total_q} questões")

    if avisos:
        print(f"\nAVISOS ({len(avisos)}):")
        for a in avisos:
            print("  ! " + a)

    if args.so_listar:
        print("\n(--so-listar: nada foi escrito)")
        return

    SAIDA.mkdir(exist_ok=True)

    seed = [{"slug": i["slug"], "quizJson": i["quizJson"], "relatorioHtml": i["relatorioHtml"]}
            for i in itens]
    p_seed = SAIDA / "content_seed.json"
    p_seed.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding="utf-8")

    p_cat = SAIDA / "catalogo.ts"
    p_cat.write_text(montar_catalogo(itens), encoding="utf-8")

    print(f"\nOK  {p_seed}  ({p_seed.stat().st_size/1024/1024:.1f} MB)")
    print(f"    {p_cat}")
    print("\nPróximo passo, no repositório do Hub:")
    print("  1. cole o conteúdo de catalogo.ts na árvore de prisma/seed.ts")
    print("  2. copie content_seed.json para a raiz do NexoHub")
    print("  3. python scripts/validar_quiz.py content_seed.json")
    print("  4. npx prisma db seed")


if __name__ == "__main__":
    main()
