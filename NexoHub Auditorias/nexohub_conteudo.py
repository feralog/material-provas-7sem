#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nexohub_conteudo.py — o seletor e o extrator do conteúdo JÁ PUBLICADO no Nexo Hub.

    python nexohub_conteudo.py                    # menu de disciplinas
    python nexohub_conteudo.py --materiais 2      # o que há dentro
    python nexohub_conteudo.py --json 2 5         # questões normalizadas, para auditar
    python nexohub_conteudo.py --extrair 2        # grava um .json por disciplina em extraido/

De onde vem o conteúdo:

O catálogo (Disciplina → Especialidade → Tópico) é lido de `prisma/seed.ts`. As questões
vêm dos repositórios `[Tema]-quiz` clonados localmente, casados com o tópico pelo
`quizUrl`. É esse HTML que o Hub serve hoje: o `content_seed.json` nunca foi gerado, o
banco não tem `quizJson`, então `hasQuiz` é falso e a UI cai no `quizUrl`.

Dois cuidados que o importador do Hub não teve:

1. A variável mudou de nome entre templates — 55 repos usam `rawQuestions`, 1 usa `rawQ`.
   O `migrate_content.py` procura só `rawQ` e por isso lê 1 de 59.
2. Os campos também divergem: quase tudo é `question/options/explanation`, e um repo usa
   `stem/alts/correct/explain`. Aqui os dois dialetos são normalizados.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HUB = Path("D:/Arquivos/Documentos/Faculdade/OSEC/Github/Repos/OSEC-HUBPROTOTYPE")
REPOS = Path("D:/Arquivos/Documentos/Faculdade/OSEC/Github/Repos")
SEED = HUB / "prisma" / "seed.ts"
EXTRAIDO = Path(__file__).resolve().parent / "extraido"


# ── catálogo ─────────────────────────────────────────────────────────────────

def ler_catalogo():
    """[(disciplina, [(especialidade, [(topico, quizUrl)])])] a partir de seed.ts."""
    if not SEED.exists():
        sys.exit(f"ERRO: nao achei {SEED}")
    src = SEED.read_text(encoding="utf-8")

    disciplinas, disc_atual, esp_atual = [], None, None
    # o arquivo e regular o bastante para uma varredura linha a linha
    for linha in src.split("\n"):
        s = linha.strip()

        m = re.match(r"name:\s*'([^']+)',$", s)
        if m:
            indent = len(linha) - len(linha.lstrip())
            if indent <= 4:                       # disciplina
                disc_atual = (m.group(1), [])
                disciplinas.append(disc_atual)
                esp_atual = None
            elif disc_atual is not None:          # especialidade
                esp_atual = (m.group(1), [])
                disc_atual[1].append(esp_atual)
            continue

        m = re.match(r"\{\s*name:\s*'([^']+)'.*?\}", s)
        if m and esp_atual is not None:
            topico = m.group(1)
            u = re.search(r"quizUrl:\s*'([^']+)'", s)
            esp_atual[1].append((topico, u.group(1) if u else None))

    return [d for d in disciplinas if any(esp[1] for esp in d[1])]


def repo_da_url(url):
    """https://feralog.github.io/Meningites-quiz -> pasta local do repo."""
    if not url:
        return None
    nome = url.rstrip("/").split("/")[-1]
    p = REPOS / nome
    return p if (p / "index.html").exists() else None


# ── extração das questões ────────────────────────────────────────────────────

LEITOR = Path(__file__).resolve().parent / "ler_quiz_publicado.js"


def extrair_questoes(index_html: Path):
    """Devolve (questoes, aviso). Quem interpreta o array e o Node.

    O array e um literal JavaScript. Converter para JSON com regex corrompe
    qualquer string que contenha ", palavra:" no meio — e explicacao clinica tem
    isso o tempo todo. O helper avalia num contexto vazio do vm e devolve JSON.
    """
    try:
        r = subprocess.run(["node", str(LEITOR), str(index_html)],
                           capture_output=True, text=True, encoding="utf-8", timeout=60)
    except FileNotFoundError:
        return [], "node nao encontrado no PATH"
    except subprocess.TimeoutExpired:
        return [], "leitura demorou demais"

    if r.returncode != 0:
        return [], f"leitor falhou: {(r.stderr or '').strip()[:80]}"
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return [], "leitor devolveu saida invalida"

    if "erro" in d:
        return [], d["erro"]
    return d["questoes"], None


def levantar():
    """[(disciplina, [material...])] — só o que tem quiz publicado e legível."""
    out = []
    for disciplina, especialidades in ler_catalogo():
        mats = []
        for especialidade, topicos in especialidades:
            for topico, url in topicos:
                if not url:
                    continue
                repo = repo_da_url(url)
                if repo is None:
                    mats.append({"topico": topico, "especialidade": especialidade,
                                 "url": url, "repo": None, "questoes": [],
                                 "aviso": "repo nao clonado localmente"})
                    continue
                questoes, aviso = extrair_questoes(repo / "index.html")

                # alguns repos sao coletanea: o index e so a capa e cada quiz
                # mora num quiz_*.html ao lado
                if not questoes:
                    partes = sorted(repo.glob("quiz_*.html"))
                    if partes:
                        juntas, lidas = [], 0
                        for parte in partes:
                            qs, _ = extrair_questoes(parte)
                            if qs:
                                lidas += 1
                                for q in qs:
                                    q["parte"] = parte.stem
                                juntas += qs
                        if juntas:
                            questoes = juntas
                            aviso = (None if lidas == len(partes)
                                     else f"coletanea: {lidas} de {len(partes)} partes lidas")

                mats.append({"topico": topico, "especialidade": especialidade,
                             "url": url, "repo": repo.name,
                             "questoes": questoes, "aviso": aviso})
        if mats:
            out.append((disciplina, mats))
    return out


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Conteudo publicado no Nexo Hub")
    ap.add_argument("--materiais", nargs="*", type=int, metavar="N")
    ap.add_argument("--json", nargs="*", type=int, metavar="N")
    ap.add_argument("--extrair", nargs="*", type=int, metavar="N")
    args = ap.parse_args()

    achados = levantar()
    if not achados:
        sys.exit("Nenhum conteudo publicado encontrado.")

    escolha = next((x for x in (args.json, args.extrair, args.materiais) if x is not None), None)

    if escolha is None:
        print("\nDisciplinas publicadas no Nexo Hub:\n")
        tm = tq = tp = 0
        for i, (disc, mats) in enumerate(achados, 1):
            q = sum(len(m["questoes"]) for m in mats)
            probl = sum(1 for m in mats if m["aviso"])
            tm += len(mats); tq += q; tp += probl
            alerta = f"   ({probl} sem leitura)" if probl else ""
            print(f"  [{i}] {disc:<30} {len(mats):>2} tópicos · {q:>4} questões{alerta}")
        print(f"\n  [0] Todas{'':<26} {tm:>2} tópicos · {tq:>4} questões"
              + (f"   ({tp} sem leitura)" if tp else ""))
        print("\nResponda com os números separados por espaço (ex.: 1 3) ou 0 para todas.")
        return

    if not escolha:
        escolha = list(range(1, len(achados) + 1))
    ruins = [n for n in escolha if not (1 <= n <= len(achados))]
    if ruins:
        sys.exit(f"ERRO: opção inexistente: {ruins}. Válidas: 1 a {len(achados)}.")
    sel = [achados[n - 1] for n in escolha]

    if args.json is not None:
        print(json.dumps([{"disciplina": d, "materiais": m} for d, m in sel],
                         ensure_ascii=False, indent=2))
        return

    if args.extrair is not None:
        EXTRAIDO.mkdir(exist_ok=True)
        for disc, mats in sel:
            nome = re.sub(r"[^\w]+", "_", disc.lower()).strip("_")
            p = EXTRAIDO / f"nexohub_{nome}.json"
            p.write_text(json.dumps({"disciplina": disc, "materiais": mats},
                                    ensure_ascii=False, indent=2), encoding="utf-8")
            q = sum(len(m["questoes"]) for m in mats)
            print(f"  {p.name:<44} {len(mats):>2} tópicos · {q:>4} questões")
        print(f"\nOK  em {EXTRAIDO}")
        return

    for disc, mats in sel:
        q = sum(len(m["questoes"]) for m in mats)
        print(f"\n{disc}  ({len(mats)} tópicos · {q} questões)")
        for m in mats:
            if m["aviso"]:
                print(f"   ! {m['topico']:<42} — {m['aviso']}")
            else:
                print(f"   • {m['topico']:<42} {len(m['questoes']):>3} questões"
                      f"   [{m['especialidade']}]")


if __name__ == "__main__":
    main()
