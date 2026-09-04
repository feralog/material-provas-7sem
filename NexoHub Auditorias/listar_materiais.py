#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
listar_materiais.py — o seletor da auditoria.

    python "NexoHub Auditorias/listar_materiais.py"              # menu de matérias
    python "NexoHub Auditorias/listar_materiais.py" --materiais 1 4   # o que há dentro
    python "NexoHub Auditorias/listar_materiais.py" --json 1 4        # para o agente ler

A numeração sai daqui, e não de uma lista escrita à mão, justamente para nunca
divergir do que existe em disco.
"""

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

DISCIPLINAS = {
    "PED": "Pediatria",
    "GO": "Ginecologia e Obstetrícia",
    "Geriatria": "Geriatria",
    "Neurologia": "Neurologia",
    "Psiquiatria": "Psiquiatria",
    "Otorrino": "Otorrinolaringologia",
    "OFTALMO": "Oftalmologia",
}


def levantar():
    """[(sigla, nome, [material...])] — só disciplinas que têm material."""
    achados = []
    for sigla, nome in DISCIPLINAS.items():
        mats = []
        for aula in sorted((RAIZ / sigla).glob("aula_*.json")) if (RAIZ / sigla).exists() else []:
            try:
                d = json.loads(aula.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  ! {aula.name}: JSON ilegível ({e})", file=sys.stderr)
                continue
            resumo = aula.parent / aula.name.replace("aula_", "resumo_").replace(".json", ".md")
            mats.append({
                "titulo": d.get("titulo", aula.stem),
                "eyebrow": d.get("eyebrow", ""),
                "questoes": len(d.get("questoes", [])),
                "com_imagem": sum(1 for q in d.get("questoes", []) if q.get("image")),
                "aula": str(aula.relative_to(RAIZ)).replace("\\", "/"),
                "resumo": str(resumo.relative_to(RAIZ)).replace("\\", "/") if resumo.exists() else None,
            })
        if mats:
            achados.append((sigla, nome, mats))
    return sorted(achados, key=lambda x: x[1])


def main():
    ap = argparse.ArgumentParser(description="Seletor de matérias para auditoria")
    ap.add_argument("--materiais", nargs="*", type=int, metavar="N",
                    help="detalha os materiais das matérias escolhidas")
    ap.add_argument("--json", nargs="*", type=int, metavar="N",
                    help="mesma coisa, em JSON (para o agente consumir)")
    args = ap.parse_args()

    achados = levantar()
    if not achados:
        sys.exit("Nenhum material encontrado.")

    escolha = args.json if args.json is not None else args.materiais

    if escolha is not None:
        if not escolha:                       # sem número = todas
            escolha = list(range(1, len(achados) + 1))
        invalidos = [n for n in escolha if not (1 <= n <= len(achados))]
        if invalidos:
            sys.exit(f"ERRO: opção inexistente: {invalidos}. Válidas: 1 a {len(achados)}.")

        sel = [achados[n - 1] for n in escolha]

        if args.json is not None:
            print(json.dumps([{"sigla": s, "disciplina": d, "materiais": m}
                              for s, d, m in sel], ensure_ascii=False, indent=2))
            return

        for sigla, nome, mats in sel:
            print(f"\n{nome}  ({len(mats)} materiais · {sum(m['questoes'] for m in mats)} questões)")
            for m in mats:
                falta = "" if m["resumo"] else "   [SEM RESUMO]"
                img = f" · {m['com_imagem']} com imagem" if m["com_imagem"] else ""
                print(f"   • {m['titulo']:<44} {m['questoes']:>3} questões{img}{falta}")
        return

    # menu
    print("\nMatérias disponíveis para auditoria:\n")
    tot_m = tot_q = 0
    for i, (sigla, nome, mats) in enumerate(achados, 1):
        q = sum(m["questoes"] for m in mats)
        tot_m += len(mats); tot_q += q
        print(f"  [{i}] {nome:<28} {len(mats):>2} materiais · {q:>4} questões")
    print(f"\n  [0] Todas{'':<24} {tot_m:>2} materiais · {tot_q:>4} questões")
    print("\nResponda com os números separados por espaço (ex.: 1 4 6) ou 0 para todas.")


if __name__ == "__main__":
    main()
