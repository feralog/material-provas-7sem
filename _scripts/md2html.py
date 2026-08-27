#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2html.py — conversor de markdown para o HTML do resumo.

Subconjunto suportado (proposital — tudo o que o resumo precisa e nada mais):
    ## / ### / ####      cabecalhos  (## vira secao, contada na tela inicial)
    paragrafos
    - / * / 1.           listas, com um nivel de aninhamento
    | a | b |            tabelas GFM (com linha de separacao)
    > texto              callout (bloco azul destacado)
    ---                  divisor
    **negrito**  *italico*  `codigo`

Nao suporta HTML cru embutido — por seguranca, `<` `>` `&` sao escapados.
"""

import html
import re


def _inline(t: str) -> str:
    t = html.escape(t, quote=False)
    # codigo primeiro, para nao processar negrito/italico dentro dele
    marcas = []

    def guarda(m):
        marcas.append(m.group(1))
        return "\x00%d\x00" % (len(marcas) - 1)

    t = re.sub(r"`([^`]+)`", guarda, t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: "<code>%s</code>" % marcas[int(m.group(1))], t)
    return t


def _tabela(linhas):
    def celulas(l):
        l = l.strip()
        if l.startswith("|"):
            l = l[1:]
        if l.endswith("|"):
            l = l[:-1]
        return [c.strip() for c in l.split("|")]

    cab = celulas(linhas[0])
    corpo = [celulas(l) for l in linhas[2:]]
    out = ['<div class="tbl"><table><thead><tr>']
    out += ["<th>%s</th>" % _inline(c) for c in cab]
    out.append("</tr></thead><tbody>")
    for linha in corpo:
        out.append("<tr>")
        out += ["<td>%s</td>" % _inline(c) for c in linha]
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


_LI = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
_IMG = re.compile(r"^!\[(.*?)\]\(img:([\w]+)\)$")
_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")


def _lista(linhas):
    """Monta uma lista com no maximo um nivel de aninhamento."""
    raiz_ord = None
    out, aberto_sub = [], False
    for l in linhas:
        m = _LI.match(l)
        if not m:
            continue
        indent, marca, texto = len(m.group(1)), m.group(2), m.group(3)
        ordenada = marca not in ("-", "*")
        if raiz_ord is None:
            raiz_ord = ordenada
            out.append("<ol>" if raiz_ord else "<ul>")
        if indent >= 2:
            if not aberto_sub:
                out.append("<ul>")
                aberto_sub = True
            out.append("<li>%s</li>" % _inline(texto))
        else:
            if aberto_sub:
                out.append("</ul>")
                aberto_sub = False
            out.append("<li>%s</li>" % _inline(texto))
    if aberto_sub:
        out.append("</ul>")
    out.append("</ol>" if raiz_ord else "</ul>")
    return "".join(out)


def md2html(md: str) -> str:
    linhas = md.replace("\r\n", "\n").split("\n")
    out, i, n = [], 0, len(linhas)

    while i < n:
        l = linhas[i]
        s = l.strip()

        if not s:
            i += 1
            continue

        if s.startswith("####"):
            out.append("<h4>%s</h4>" % _inline(s.lstrip("#").strip())); i += 1; continue
        if s.startswith("###"):
            out.append("<h3>%s</h3>" % _inline(s.lstrip("#").strip())); i += 1; continue
        if s.startswith("##"):
            out.append("<h2>%s</h2>" % _inline(s.lstrip("#").strip())); i += 1; continue
        if s.startswith("#"):
            # h1 vira h2 — o titulo da pagina ja esta no cabecalho
            out.append("<h2>%s</h2>" % _inline(s.lstrip("#").strip())); i += 1; continue

        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            out.append("<hr>"); i += 1; continue

        # imagem: ![legenda](img:pgNN) numa linha sozinha
        m = re.fullmatch(r"!\[(.*?)\]\(img:([\w]+)\)", s)
        if m:
            legenda, chave = m.group(1).strip(), m.group(2)
            fig = '<figure class="fig"><img src="@@IMG:%s@@" alt="%s">' % (chave, html.escape(legenda, quote=True))
            if legenda:
                fig += "<figcaption>%s</figcaption>" % _inline(legenda)
            out.append(fig + "</figure>")
            i += 1
            continue

        # tabela: linha com | seguida de linha separadora
        if "|" in s and i + 1 < n and _SEP.match(linhas[i + 1]):
            bloco = [linhas[i], linhas[i + 1]]
            i += 2
            while i < n and "|" in linhas[i] and linhas[i].strip():
                bloco.append(linhas[i]); i += 1
            out.append(_tabela(bloco)); continue

        # callout
        if s.startswith(">"):
            bloco = []
            while i < n and linhas[i].strip().startswith(">"):
                bloco.append(linhas[i].strip().lstrip(">").strip()); i += 1
            texto = " ".join(x for x in bloco if x)
            out.append('<blockquote><p>%s</p></blockquote>' % _inline(texto)); continue

        # lista
        if _LI.match(l):
            bloco = []
            while i < n and (_LI.match(linhas[i]) or (linhas[i].strip() and linhas[i].startswith("   "))):
                bloco.append(linhas[i]); i += 1
            out.append(_lista(bloco)); continue

        # paragrafo
        bloco = []
        while i < n and linhas[i].strip() and not _LI.match(linhas[i]) \
                and not _IMG.match(linhas[i].strip()) \
                and not linhas[i].strip().startswith(("#", ">", "|")) \
                and not re.fullmatch(r"-{3,}|\*{3,}|_{3,}", linhas[i].strip()):
            bloco.append(linhas[i].strip()); i += 1
        if bloco:
            out.append("<p>%s</p>" % _inline(" ".join(bloco)))
        else:
            i += 1

    return "\n".join(out)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    print(md2html(Path(sys.argv[1]).read_text(encoding="utf-8")))
