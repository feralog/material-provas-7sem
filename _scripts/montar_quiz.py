#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
montar_quiz.py — junta quiz + resumo num unico HTML local autocontido.

Uso:
    python _scripts/montar_quiz.py "PED/aula_tireoide.json" "PED/resumo_tireoide.md"

Entrada 1 — aula_[tema].json:
    {
      "titulo":    "Distúrbios da Tireoide",
      "eyebrow":   "Pediatria · Endocrinologia",
      "subtitulo": "Frase longa que abre a tela inicial",
      "intro":     "Parágrafo de abertura, 1 a 3 linhas.",
      "questoes": [
        {
          "question":     "Enunciado completo?",
          "options":      ["CORRETA", "distrator", "distrator", "distrator"],
          "correctIndex": 0,
          "explanation":  "Por que a correta está certa."
        }
      ]
    }

Entrada 2 — resumo_[tema].md: markdown (ver _scripts/md2html.py para o subconjunto).

Saida:
    Quizzes/quiz_[titulo_snake].html

Valida antes de gerar e ABORTA se encontrar:
    - menos de 4 ou mais de 6 alternativas
    - correctIndex != 0            (o embaralhamento acontece no navegador)
    - alternativas duplicadas / enunciado vazio / explicacao vazia
    - alternativa acima de 130% do comprimento da mais curta do grupo
Use --forcar para gerar mesmo com avisos de comprimento.
"""

import argparse
import base64
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md2html import md2html  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATE = RAIZ / "_template" / "quiz.html"
SAIDA_DIR = RAIZ / "Quizzes"

LIMITE_RAZAO = 1.30
MIN_ALT, MAX_ALT = 4, 6


def snake(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s\-]+", "_", s)
    return re.sub(r"_+", "_", s).strip("_") or "quiz"


def validar(questoes):
    erros, avisos = [], []
    for i, q in enumerate(questoes, 1):
        stem = (q.get("question") or "").strip()
        alts = q.get("options") or []
        expl = (q.get("explanation") or "").strip()

        if not stem:
            erros.append(f"Q{i}: enunciado vazio")
        if not expl:
            erros.append(f"Q{i}: explicação vazia")
        if not (MIN_ALT <= len(alts) <= MAX_ALT):
            erros.append(f"Q{i}: {len(alts)} alternativas (esperado {MIN_ALT}–{MAX_ALT})")
            continue
        if q.get("correctIndex", 0) != 0:
            erros.append(f"Q{i}: correctIndex={q.get('correctIndex')} (deve ser 0)")
        if len(set(a.strip().lower() for a in alts)) != len(alts):
            erros.append(f"Q{i}: alternativas duplicadas")

        tam = [len(a) for a in alts]
        menor, maior = min(tam), max(tam)
        if menor and maior / menor > LIMITE_RAZAO:
            j = tam.index(maior)
            marca = "  <-- é a CORRETA" if j == 0 else ""
            avisos.append(f"Q{i}: alt {j} tem {maior} chars vs {menor} da mais curta "
                          f"({maior/menor:.0%}){marca}")
    return erros, avisos


def main():
    ap = argparse.ArgumentParser(description="Gera o HTML local com quiz + resumo")
    ap.add_argument("aula", help="arquivo aula_[tema].json")
    ap.add_argument("resumo", help="arquivo resumo_[tema].md")
    ap.add_argument("--imagens", help="acervo imagens_[tema].json (padrão: ao lado do aula.json)")
    ap.add_argument("--disciplina", help="rótulo da disciplina para o índice "
                                         "(padrão: nome da pasta do aula.json, ex.: PED, GO)")
    ap.add_argument("--saida", help="caminho do .html de saida")
    ap.add_argument("--forcar", action="store_true", help="gerar apesar dos avisos de comprimento")
    args = ap.parse_args()

    if not TEMPLATE.exists():
        sys.exit(f"ERRO: template nao encontrado em {TEMPLATE}")

    dados = json.loads(Path(args.aula).read_text(encoding="utf-8"))
    for campo in ("titulo", "eyebrow", "subtitulo", "intro", "questoes"):
        if not dados.get(campo):
            sys.exit(f"ERRO: campo '{campo}' ausente ou vazio em {args.aula}")

    questoes = dados["questoes"]
    if not isinstance(questoes, list) or len(questoes) < 5:
        sys.exit("ERRO: 'questoes' deve ser uma lista com pelo menos 5 itens")

    erros, avisos = validar(questoes)
    for a in avisos:
        print("  ! " + a)
    if erros:
        print("\nERROS (bloqueiam a geração):")
        for e in erros:
            print("  X " + e)
        sys.exit(1)
    if avisos and not args.forcar:
        print(f"\n{len(avisos)} aviso(s) de equalização. Ajuste as alternativas "
              f"ou rode de novo com --forcar.")
        sys.exit(1)

    md = Path(args.resumo).read_text(encoding="utf-8")
    resumo_html = md2html(md)
    if "</script" in resumo_html.lower():
        sys.exit("ERRO: o resumo contém '</script' — isso quebraria o HTML gerado")
    n_secoes = resumo_html.count("<h2>")
    if n_secoes == 0:
        sys.exit("ERRO: o resumo não tem nenhuma seção '## ' — a tela inicial conta essas seções")

    # ── imagens: embute só as referenciadas ──────────────────────────────────
    acervo = {}
    ij = Path(args.imagens) if args.imagens else Path(args.aula).parent / (
        "imagens_" + snake(dados["titulo"]) + ".json")
    if ij.exists():
        acervo = json.loads(ij.read_text(encoding="utf-8"))
    usadas, faltando = {}, []

    naojpeg = []

    def uri(chave):
        if chave not in acervo:
            faltando.append(chave)
            return ""
        # o data URI declara image/jpeg — se o blob nao for JPEG, o navegador
        # mostra figura quebrada e nada acusa. EMF/WMF vem assim de PPTX.
        if base64.b64decode(acervo[chave][:8])[:3] != b"\xff\xd8\xff":
            naojpeg.append(chave)
            return ""
        usadas[chave] = acervo[chave]
        return "data:image/jpeg;base64," + acervo[chave]

    resumo_html = re.sub(r"@@IMG:(\w+)@@", lambda m: uri(m.group(1)), resumo_html)

    saida_q = []
    for q in questoes:
        item = {"question": q["question"], "options": q["options"],
                "correctIndex": 0, "explanation": q["explanation"]}
        if q.get("image"):
            u = uri(q["image"])
            if u:
                item["image"] = u
                item["imageCaption"] = q.get("imageCaption", "")
        saida_q.append(item)

    if faltando:
        alvo = f" (procurei em {ij.name})" if not acervo else ""
        print(f"\nERRO: chaves de imagem inexistentes{alvo}: {sorted(set(faltando))}")
        if acervo:
            print(f"      o acervo tem {len(acervo)} chaves: "
                  f"{sorted(acervo)[0]} .. {sorted(acervo)[-1]}")
        sys.exit(1)

    if naojpeg:
        print(f"\nERRO: estas imagens não são JPEG e apareceriam quebradas no navegador "
              f"(formato vetorial EMF/WMF vindo do PPTX): {sorted(set(naojpeg))}")
        print("      escolha outra imagem para essas questões/figuras.")
        sys.exit(1)

    raw = json.dumps(saida_q, ensure_ascii=False, indent=2)

    def js(s):
        return json.dumps(str(s), ensure_ascii=False)[1:-1]

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__QUIZ__", raw)
    html = html.replace("__RESUMO__", resumo_html)
    disciplina = args.disciplina or Path(args.aula).resolve().parent.name
    for chave, valor in (("__TITLE__", dados["titulo"]), ("__EYEBROW__", dados["eyebrow"]),
                         ("__SUBTITLE__", dados["subtitulo"]), ("__INTRO__", dados["intro"]),
                         ("__DISCIPLINA__", disciplina)):
        html = html.replace(chave, js(valor))

    sobrou = re.findall(r"__[A-Z_]+__", html)
    if sobrou:
        sys.exit(f"ERRO: placeholder não substituído: {sorted(set(sobrou))}")

    out = Path(args.saida) if args.saida else SAIDA_DIR / f"quiz_{snake(dados['titulo'])}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    mb = sum(len(v) for v in usadas.values()) / 1024 / 1024
    img_txt = f", {len(usadas)} imagens ({mb:.1f} MB)" if usadas else ", sem imagens"
    print(f"\nOK  {len(questoes)} questões + resumo com {n_secoes} seções{img_txt}")
    print(f"    {out}  ({len(html)/1024/1024:.1f} MB)")
    if acervo and not usadas:
        print(f"    aviso: o acervo tem {len(acervo)} imagens e nenhuma foi usada")


if __name__ == "__main__":
    main()
