#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atualizar_indice.py — varre Quizzes/*.html e (re)gera o index.html da raiz.

Uso:
    python _scripts/atualizar_indice.py

Le titulo, eyebrow, nº de questoes, nº de secoes do resumo e nº de imagens NAS
QUESTOES de cada HTML gerado (as figuras do resumo não entram na contagem).
Rodar sempre depois de montar_quiz.py.
"""

import html as H
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
QUIZZES = RAIZ / "Quizzes"
INDEX = RAIZ / "index.html"


NOMES = {
    "PED": "Pediatria",
    "GO": "Ginecologia e Obstetrícia",
    "Geriatria": "Geriatria",
    "Neurologia": "Neurologia",
    "Psiquiatria": "Psiquiatria",
    "Otorrino": "Otorrinolaringologia",
    "OFTALMO": "Oftalmologia",
    "SAI": "Saúde do Adulto e do Idoso",
    "CIR": "Cirurgia",
    "MFC": "Medicina de Família e Comunidade",
}


def ler_meta(p: Path):
    src = p.read_text(encoding="utf-8")
    # so a cabeca do arquivo interessa para titulo/eyebrow
    t = re.search(r'var TITLE\s*=\s*"(.*?)";', src)
    e = re.search(r'var EYEBROW\s*=\s*"(.*?)";', src)
    d = re.search(r'var DISCIPLINA\s*=\s*"(.*?)";', src)
    resumo = re.search(r'<script type="text/html" id="resumoSrc">([\s\S]*?)</script>', src)
    corpo = resumo.group(1) if resumo else ""
    sigla = (d.group(1) if d else "") or "?"
    return {
        "arquivo": p.name,
        "titulo": (t.group(1) if t else p.stem).replace('\\"', '"'),
        "eyebrow": (e.group(1) if e else "").replace('\\"', '"'),
        "sigla": sigla,
        "disciplina": NOMES.get(sigla, sigla if sigla != "?" else "Sem disciplina"),
        "q": len(re.findall(r'^\s*"question":', src, re.M)),
        "sec": corpo.count("<h2>"),
        "img": len(re.findall(r'"image": "data:image/jpeg;base64,', src)),
        "mb": p.stat().st_size / 1024 / 1024,
    }


PAGINA = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Material para provas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;450;500;600&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:#f5f3ef;color:#121a2b;font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
  a{color:inherit;text-decoration:none}
  .wrap{max-width:720px;margin:0 auto;padding:56px 16px 80px}
  .eyebrow{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#2b57cc;margin-bottom:16px}
  h1{font-family:'Newsreader',Georgia,serif;font-size:40px;line-height:1.08;font-weight:400;letter-spacing:-.025em;margin:0 0 16px}
  .sub{font-size:15.5px;line-height:1.65;color:#5b6478;margin:0 0 30px;max-width:52ch}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(108px,1fr));gap:1px;background:#e4e0d8;border:1px solid #e4e0d8;border-radius:14px;overflow:hidden;margin-bottom:32px}
  .stats div{background:#faf9f6;padding:16px 14px}
  .stats .v{font-family:'IBM Plex Mono',monospace;font-size:22px;font-weight:500;letter-spacing:-.03em}
  .stats .l{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#8a8578;margin-top:3px}
  .disc{margin-bottom:34px}
  .disc h2{font-family:'Newsreader',Georgia,serif;font-size:25px;font-weight:500;letter-spacing:-.02em;margin:0 0 4px}
  .disc .cnt{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:#8a8578;margin-bottom:14px}
  .grid{display:flex;flex-direction:column;gap:10px}
  .card{display:flex;align-items:center;gap:16px;background:#fff;border:1px solid #e4e0d8;border-radius:16px;padding:18px 20px;transition:border-color .16s ease,transform .14s ease;box-shadow:0 1px 2px rgba(18,26,43,.04)}
  .card:hover{border-color:#121a2b;transform:translateY(-2px)}
  .card .n{font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;color:#8a8578;min-width:24px}
  .card .body{flex:1;min-width:0}
  .card .t{font-family:'Newsreader',Georgia,serif;font-size:21px;font-weight:500;letter-spacing:-.015em;line-height:1.2}
  .card .e{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.06em;color:#8a8578;margin-top:4px}
  .card .tags{display:flex;gap:6px;flex-shrink:0;flex-wrap:wrap;justify-content:flex-end}
  .tag{font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:#5b6478;background:#faf9f6;border:1px solid #e4e0d8;border-radius:99px;padding:4px 10px;white-space:nowrap}
  .empty{border:1px dashed #ddd8ce;border-radius:14px;padding:38px;text-align:center;color:#8a8578}
  .foot{margin-top:34px;padding-top:22px;border-top:1px solid #e4e0d8;font-family:'IBM Plex Mono',monospace;font-size:11px;color:#8a8578}
  @media(max-width:560px){.card{flex-wrap:wrap}.card .tags{justify-content:flex-start;width:100%}}
</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow">Material para provas</div>
  <h1>7º semestre</h1>
  <p class="sub">__SUB__</p>
  <div class="stats">__STATS__</div>
__CARDS__
  <div class="foot">Cada arquivo tem quiz e resumo, escolhidos na tela inicial. Gerado por _scripts/atualizar_indice.py</div>
</div>
</body>
</html>
"""


def main():
    QUIZZES.mkdir(exist_ok=True)
    metas = [ler_meta(p) for p in sorted(QUIZZES.glob("quiz_*.html"))]

    if metas:
        grupos = {}
        for m in metas:
            grupos.setdefault(m["disciplina"], []).append(m)

        blocos, n = [], 0
        for disc in sorted(grupos):
            itens = sorted(grupos[disc], key=lambda x: x["titulo"])
            linhas = []
            for m in itens:
                n += 1
                linhas.append(
                    '      <a class="card" href="Quizzes/{f}">'
                    '<span class="n">{i:02d}</span>'
                    '<span class="body"><span class="t">{t}</span><br><span class="e">{e}</span></span>'
                    '<span class="tags"><span class="tag">{q} questões</span>'
                    '<span class="tag">{s} seções</span>'
                    '<span class="tag">{g} imagens</span></span></a>'.format(
                        f=H.escape(m["arquivo"]), i=n, t=H.escape(m["titulo"]),
                        e=H.escape(m["eyebrow"]), q=m["q"], s=m["sec"], g=m["img"]))
            tot_q = sum(x["q"] for x in itens)
            blocos.append(
                f'  <div class="disc">\n    <h2>{H.escape(disc)}</h2>\n'
                f'    <div class="cnt">{len(itens)} materiais · {tot_q} questões</div>\n'
                f'    <div class="grid">\n' + "\n".join(linhas) + "\n    </div>\n  </div>")
        cards = "\n".join(blocos)

        cell = lambda v, l: f'<div><div class="v">{v}</div><div class="l">{l}</div></div>'
        stats = (cell(len(grupos), "Disciplinas") +
                 cell(len(metas), "Materiais") +
                 cell(sum(m["q"] for m in metas), "Questões") +
                 cell(sum(m["img"] for m in metas), "Imagens"))
        sub = "Cada material abre com um seletor: fazer o quiz ou ler o resumo. Tudo offline, num arquivo só."
    else:
        cards = ('  <div class="empty">Nenhum material ainda.<br>'
                 'Rode <code>_scripts/montar_quiz.py</code> para gerar o primeiro.</div>')
        stats = ""
        sub = "Nenhum material gerado ainda."

    INDEX.write_text(
        PAGINA.replace("__CARDS__", cards).replace("__SUB__", sub).replace("__STATS__", stats),
        encoding="utf-8")
    print(f"OK  {len(metas)} material(is) -> {INDEX}")
    for m in sorted(metas, key=lambda x: (x["disciplina"], x["titulo"])):
        print(f"    [{m['sigla']:>3}] {m['titulo']}: {m['q']} questões, {m['sec']} seções, "
              f"{m['img']} imagens, {m['mb']:.1f} MB")


if __name__ == "__main__":
    main()
