"""
resumos_para_pdf.py — junta os resumos de uma disciplina num PDF para leitura
(ou para alimentar NotebookLM, que aceita PDF como fonte).

    python _scripts/resumos_para_pdf.py Neurologia OFTALMO Otorrino
    python _scripts/resumos_para_pdf.py Otorrino --saida "C:/Users/.../Desktop"
    python _scripts/resumos_para_pdf.py OFTALMO --separado    # 1 PDF por aula

Reaproveita o md2html.py do pipeline, então o PDF sai com as mesmas tabelas,
callouts e figuras do resumo que aparece no quiz. As imagens vêm do
imagens_*.json correspondente, embutidas em base64.

Precisa do Chrome (usa --headless --print-to-pdf). Não instala nada.
"""
import argparse
import base64
import html as H
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from md2html import md2html  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent

CHROME = next((p for p in [
    Path(r"C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path(r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path(r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
    Path(r"C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
] if p.exists()), None)

NOMES = {
    "Neurologia": "Neurologia", "OFTALMO": "Oftalmologia",
    "Otorrino": "Otorrinolaringologia", "PED": "Pediatria",
    "GO": "Ginecologia e Obstetrícia", "Geriatria": "Geriatria",
    "Psiquiatria": "Psiquiatria", "SAI": "Saúde do Adulto e do Idoso",
    "CIR": "Cirurgia", "MFC": "Medicina de Família e Comunidade",
}

# CSS de impressão: serifada no corpo, tabela que não parte no meio,
# cada aula começando em página nova.
CSS = """
@page { size: A4; margin: 18mm 16mm 16mm; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt;
       line-height: 1.55; color: #1c2230; margin: 0; }
.capa { text-align: center; padding: 70mm 0 0; page-break-after: always; }
.capa .disc { font-family: Arial, sans-serif; font-size: 10pt; letter-spacing: .18em;
              text-transform: uppercase; color: #6b7280; margin-bottom: 10mm; }
.capa h1 { font-size: 30pt; font-weight: 400; margin: 0 0 6mm; letter-spacing: -.5pt; }
.capa .sub { font-size: 11pt; color: #4b5563; }
.capa .lista { margin: 16mm auto 0; max-width: 120mm; text-align: left;
               font-size: 10pt; color: #374151; }
.capa .lista li { margin: 2mm 0; }
.aula { page-break-before: always; }
.aula > .titulo { font-size: 19pt; font-weight: 400; margin: 0 0 2mm;
                  padding-bottom: 3mm; border-bottom: 2px solid #1f3a8a; }
.aula > .rotulo { font-family: Arial, sans-serif; font-size: 8.5pt; letter-spacing: .14em;
                  text-transform: uppercase; color: #6b7280; margin: 0 0 4mm; }
h2 { font-size: 14pt; font-weight: 600; margin: 8mm 0 3mm; padding-top: 3mm;
     border-top: 1px solid #dcdfe5; page-break-after: avoid; }
h3 { font-size: 11.5pt; font-weight: 600; margin: 6mm 0 2mm; page-break-after: avoid; }
h4 { font-family: Arial, sans-serif; font-size: 8.5pt; font-weight: 700;
     letter-spacing: .12em; text-transform: uppercase; color: #1f3a8a;
     margin: 5mm 0 2mm; page-break-after: avoid; }
p { margin: 0 0 3mm; text-align: justify; }
ul, ol { margin: 0 0 3mm; padding-left: 7mm; }
li { margin-bottom: 1.4mm; }
strong { font-weight: 700; color: #0f1626; }
code { font-family: Consolas, monospace; font-size: .9em; background: #f1f2f5;
       border: 1px solid #e2e4ea; border-radius: 3px; padding: 0 3px; }
hr { border: 0; border-top: 1px solid #dcdfe5; margin: 6mm 0; }
blockquote { margin: 0 0 4mm; padding: 3mm 4mm; background: #f4f7fd;
             border-left: 3px solid #1f3a8a; page-break-inside: avoid; }
blockquote p:last-child { margin-bottom: 0; }
.tbl { margin: 0 0 4mm; page-break-inside: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; line-height: 1.4; }
th { text-align: left; font-family: Arial, sans-serif; font-size: 8pt;
     text-transform: uppercase; letter-spacing: .06em; color: #4b5563;
     background: #f4f5f8; padding: 2mm 2.5mm; border: 1px solid #dcdfe5; }
td { padding: 2mm 2.5mm; border: 1px solid #e6e8ed; vertical-align: top; }
.key { background: #f4f7fd; border: 1px solid #ccd9f2; border-radius: 3mm;
       padding: 3mm 4mm; margin: 0 0 4mm; page-break-inside: avoid; }
.key > *:last-child { margin-bottom: 0; }
figure.fig { margin: 0 0 5mm; page-break-inside: avoid; text-align: center; }
figure.fig img { max-width: 100%; max-height: 105mm; height: auto;
                 border: 1px solid #dcdfe5; border-radius: 2mm; }
figure.fig figcaption { font-family: Arial, sans-serif; font-size: 8pt; color: #6b7280;
                        margin-top: 1.5mm; }
"""

PAGINA = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>{titulo}</title><style>{css}</style></head><body>{corpo}</body></html>"""


def titulo_de(caminho: Path) -> str:
    """Título da aula: usa o do aula_*.json quando existir; senão, o nome do arquivo."""
    j = caminho.parent / ("aula_" + caminho.stem[len("resumo_"):] + ".json")
    if j.exists():
        try:
            return json.loads(j.read_text(encoding="utf-8"))["titulo"]
        except Exception:
            pass
    return caminho.stem[len("resumo_"):].replace("_", " ").title()


def acervo_de(pasta: Path, resumo: Path, corpo: str) -> dict:
    """Carrega o imagens_*.json cujas chaves cobrem as usadas por este resumo."""
    usadas = set(re.findall(r"@@IMG:(\w+)@@", corpo))
    if not usadas:
        return {}
    candidatos = sorted(pasta.glob("imagens_*.json"))
    # o de nome mais parecido primeiro, depois qualquer um que cubra as chaves
    alvo = resumo.stem[len("resumo_"):]
    candidatos.sort(key=lambda p: -len(set(p.stem) & set(alvo)))
    for c in candidatos:
        try:
            ac = json.loads(c.read_text(encoding="utf-8"))
        except Exception:
            continue
        if usadas <= set(ac):
            return ac
    return {}


def corpo_de(resumo: Path) -> tuple[str, int, int]:
    """Devolve (html da aula, nº de seções, nº de figuras resolvidas)."""
    md = resumo.read_text(encoding="utf-8")
    corpo = md2html(md)
    acervo = acervo_de(resumo.parent, resumo, corpo)
    faltando = []

    def uri(m):
        k = m.group(1)
        if k in acervo:
            return "data:image/jpeg;base64," + acervo[k]
        faltando.append(k)
        return ""

    corpo = re.sub(r"@@IMG:(\w+)@@", uri, corpo)
    if faltando:
        # figura sem imagem vira nada, em vez de <img src=""> quebrado
        corpo = re.sub(r'<figure class="fig"><img src=""[^>]*>.*?</figure>', "", corpo, flags=re.S)
    figs = corpo.count('<figure class="fig">')
    return corpo, corpo.count("<h2>"), figs, len(set(faltando))


def gerar_pdf(html: str, destino: Path) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        origem = Path(tmp) / "doc.html"
        origem.write_text(html, encoding="utf-8")
        destino.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run([
            str(CHROME), "--headless", "--disable-gpu", "--no-sandbox",
            "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=20000",
            f"--print-to-pdf={destino}", origem.as_uri(),
        ], capture_output=True, timeout=240)
    if not destino.exists() or destino.stat().st_size < 1000:
        print("   ERRO:", (r.stderr or b"").decode("utf-8", "replace")[:300])
        return False
    return True


def paginas(pdf: Path) -> int:
    try:
        import fitz
        with fitz.open(pdf) as d:
            return d.page_count
    except Exception:
        return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pastas", nargs="+")
    ap.add_argument("--saida", default=str(RAIZ / "PDFs"))
    ap.add_argument("--separado", action="store_true", help="um PDF por aula")
    a = ap.parse_args()

    if not CHROME:
        sys.exit("ERRO: Chrome/Edge nao encontrado — necessario para gerar PDF.")
    saida = Path(a.saida)

    for nome in a.pastas:
        pasta = RAIZ / nome
        if not pasta.is_dir():
            print(f"!! {nome}: pasta nao existe"); continue
        resumos = sorted(pasta.glob("resumo_*.md"))
        if not resumos:
            print(f"!! {nome}: nenhum resumo_*.md"); continue

        disc = NOMES.get(nome, nome)
        print(f"\n>> {disc}  ({len(resumos)} resumo(s))")
        aulas = []
        for r in resumos:
            corpo, secs, figs, falt = corpo_de(r)
            t = titulo_de(r)
            aulas.append((t, corpo))
            aviso = f"  ({falt} figura(s) sem imagem no acervo)" if falt else ""
            print(f"   {t:<46s} {secs} secoes · {figs} figuras{aviso}")

        if a.separado:
            for t, corpo in aulas:
                slug = re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")
                doc = f'<div class="aula" style="page-break-before:auto">' \
                      f'<p class="rotulo">{H.escape(disc)}</p>' \
                      f'<h1 class="titulo">{H.escape(t)}</h1>{corpo}</div>'
                dest = saida / nome / f"resumo_{slug}.pdf"
                if gerar_pdf(PAGINA.format(titulo=H.escape(t), css=CSS, corpo=doc), dest):
                    print(f"   OK  {dest.relative_to(RAIZ) if RAIZ in dest.parents else dest}"
                          f"  ({dest.stat().st_size/1024/1024:.1f} MB, {paginas(dest)} pgs)")
            continue

        itens = "".join(f"<li>{H.escape(t)}</li>" for t, _ in aulas)
        capa = (f'<div class="capa"><p class="disc">{H.escape(disc)}</p>'
                f'<h1>Resumos de estudo</h1>'
                f'<p class="sub">{len(aulas)} aula{"s" if len(aulas) != 1 else ""} · 7º semestre de Medicina</p>'
                f'<ol class="lista">{itens}</ol></div>')
        corpo = capa + "".join(
            f'<div class="aula"><p class="rotulo">{H.escape(disc)}</p>'
            f'<h1 class="titulo">{H.escape(t)}</h1>{c}</div>' for t, c in aulas)

        dest = saida / f"Resumos - {disc}.pdf"
        if gerar_pdf(PAGINA.format(titulo=H.escape(disc), css=CSS, corpo=corpo), dest):
            print(f"   OK  {dest}  ({dest.stat().st_size/1024/1024:.1f} MB, {paginas(dest)} paginas)")


if __name__ == "__main__":
    main()
