#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ver_pagina.py — extrai paginas do acervo de imagens para arquivos .jpg legiveis
pela tool Read.

POR QUE ISSO EXISTE: a tool Read nao consegue renderizar PDF neste ambiente
(`pdftoppm is not installed` — poppler-utils ausente). Mas o extrair.py JA
renderizou todas as paginas para o `imagens_[tema].json`. Este script so
decodifica o base64 de volta para arquivo — nao precisa de poppler.

Uso:
    python _scripts/ver_pagina.py "PED/imagens_aula_4_disturbios_da_tireoide.json" 16 33
    python _scripts/ver_pagina.py "PED/imagens_aula_4_...json" 15-18
    python _scripts/ver_pagina.py "PED/imagens_aula_4_...json" --listar

Depois use a tool Read nos .jpg que ele imprimir.

Saida padrao: pasta de scratchpad da sessao, ou --out.
"""

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

PADRAO_OUT = Path(
    os.environ.get("TEMP", "/tmp")
) / "paginas"


def expandir(specs):
    """Aceita numero de pagina, intervalo ou chave crua.

    '16'      -> ['pg16']              pagina de PDF
    '15-18'   -> ['pg15'..'pg18']      intervalo de paginas
    's09i1'   -> ['s09i1']             imagem de slide de PPTX
    'pg07'    -> ['pg07']              chave ja escrita por extenso
    """
    chaves = []
    for s in specs:
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", s)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            chaves += [f"pg{n:02d}" for n in range(min(a, b), max(a, b) + 1)]
        elif s.isdigit():
            chaves.append(f"pg{int(s):02d}")
        elif re.fullmatch(r"\w+", s):
            chaves.append(s)
        else:
            sys.exit(f"ERRO: '{s}' não é página, intervalo nem chave (ex.: 16, 15-18, s09i1)")
    vistos, saida = set(), []
    for k in chaves:
        if k not in vistos:
            vistos.add(k)
            saida.append(k)
    return saida


def main():
    ap = argparse.ArgumentParser(description="Extrai páginas do acervo para .jpg")
    ap.add_argument("acervo", help="arquivo imagens_[tema].json")
    ap.add_argument("paginas", nargs="*", help="números e/ou intervalos (ex.: 16 20 33-35)")
    ap.add_argument("--listar", action="store_true", help="só listar as chaves disponíveis")
    ap.add_argument("--out", help="pasta de saída")
    args = ap.parse_args()

    p = Path(args.acervo)
    if not p.exists():
        sys.exit(f"ERRO: não encontrei {p}")
    acervo = json.loads(p.read_text(encoding="utf-8"))

    if args.listar or not args.paginas:
        chaves = sorted(acervo)
        print(f"{len(chaves)} páginas em {p.name}: {chaves[0]} .. {chaves[-1]}")
        if not args.paginas and not args.listar:
            sys.exit("\nInforme as páginas. Ex.: ver_pagina.py <acervo> 16 33  |  15-18")
        return

    out = Path(args.out) if args.out else PADRAO_OUT / p.stem
    out.mkdir(parents=True, exist_ok=True)

    faltando = []
    for chave in expandir(args.paginas):
        if chave not in acervo:
            faltando.append(chave)
            continue
        alvo = out / f"{chave}.jpg"
        alvo.write_bytes(base64.b64decode(acervo[chave]))
        print(f"{alvo}   ({alvo.stat().st_size/1024:.0f} KB)")

    if faltando:
        chaves = sorted(acervo)
        print(f"\nAVISO: não existem no acervo: {faltando}", file=sys.stderr)
        print(f"       disponível: {chaves[0]} .. {chaves[-1]}", file=sys.stderr)


if __name__ == "__main__":
    main()
