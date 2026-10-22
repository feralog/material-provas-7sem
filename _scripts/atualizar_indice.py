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
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
QUIZZES = RAIZ / "Quizzes"
INDEX = RAIZ / "index.html"
INDEX_LOCAL = RAIZ / "index_local.html"
CHAVE = RAIZ / "deepseek_key.js"


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
    "Práticas": "Práticas Profissionais",
}


# Conteudo cobrado na AVC 2. A chave e o nome do arquivo em Quizzes/ porque o
# titulo muda; o valor e o tema como ele aparece na lista da prova, que nem
# sempre bate com o titulo do material (ex.: "Transtorno do impulso" virou
# "Impulsividade e Compulsividade"). MFC esta fora: nao ha material da materia.
AVC2 = {
    # Ginecologia e Obstetricia
    "quiz_distopia_genital.html": "Distopia genital e POP-Q",
    "quiz_incontinencia_urinaria.html": "Incontinência urinária",
    "quiz_diabetes_mellitus_gestacional.html": "DMG",
    "quiz_endometriose_e_algia_pelvica.html": "Endometriose",
    "quiz_doenca_inflamatoria_pelvica.html": "DIP",
    "quiz_sindromes_hipertensivas_na_gestacao.html": "Síndromes hipertensivas na gestação",
    # Psiquiatria
    "quiz_impulsividade_e_compulsividade.html": "Transtorno do impulso",
    "quiz_transtorno_depressivo.html": "Transtorno depressivo",
    "quiz_transtorno_afetivo_bipolar.html": "Transtorno bipolar",
    # Geriatria
    "quiz_delirium.html": "Delirium",
    "quiz_demencia.html": "Demência",
    "quiz_depressao_no_idoso.html": "Depressão",
    "quiz_fragilidade_e_sarcopenia.html": "Fragilidade e sarcopenia",
    "quiz_sindrome_do_imobilismo.html": "Síndrome do imobilismo",
    # Neurologia
    "quiz_alzheimer_e_demencias.html": "Demência e Doença de Alzheimer",
    "quiz_neuropatias_perifericas.html": "Doenças do SNP",
    "quiz_miastenia_gravis_e_guillain_barre.html": "Doenças do SNP",
    # Otorrinolaringologia
    "quiz_otites.html": "Otites",
    "quiz_disacusias.html": "Disacusias parte 2",
    "quiz_zumbido_e_tontura.html": "Zumbidos e tontura",
    "quiz_rinites_e_rinossinusites.html": "Rinites",
    # Oftalmologia
    "quiz_diagnostico_diferencial_do_olho_vermelho.html": "Olho vermelho",
    "quiz_catarata.html": "Catarata",
    "quiz_glaucoma.html": "Glaucoma",
    "quiz_retinopatia_diabetica.html": "Retinopatia diabética",
    "quiz_doencas_da_cornea.html": "Córnea",
    # Pediatria
    "quiz_saude_sexual_do_adolescente.html": "Saúde sexual do adolescente",
    "quiz_imunidade_parte_2.html": "Doenças imunomediadas",
    "quiz_imunodeficiencias.html": "Imunodeficiências",
    "quiz_alergia_e_atopia.html": "Alergias",
}

# Entram no filtro da AVC 2 mas NAO sao tema da prova: sao simulado, e contar
# um simulado como tema faria o contador dizer "30 de 30" sem que exista um
# conteudo novo coberto.
AVC2_EXTRA = {
    "quiz_simulado_avc_2_ped.html",
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
  .avc2bar{display:flex;align-items:center;gap:13px;flex-wrap:wrap;margin:-16px 0 28px}
  .avc2bar button{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.13em;text-transform:uppercase;font-weight:600;color:#2b57cc;background:#eef2fd;border:1px solid #c9d6f7;border-radius:99px;padding:9px 19px;cursor:pointer;transition:background .15s ease,border-color .15s ease,color .15s ease}
  .avc2bar button:hover{border-color:#2b57cc}
  body.avc2 .avc2bar button{background:#2b57cc;border-color:#2b57cc;color:#fff}
  .avc2info{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.05em;color:#8a8578}
  .avc2falta{display:none;font-family:'IBM Plex Mono',monospace;font-size:11px;line-height:1.6;color:#8a5a1f;background:#fdf4e6;border:1px solid #f0dcbc;border-radius:11px;padding:11px 14px;margin:-14px 0 26px}
  body.avc2 .avc2falta{display:block}
  body.avc2 .card:not([data-avc2]){opacity:.28;filter:grayscale(1)}
  body.avc2 .card:not([data-avc2]):hover{transform:none;border-color:#e4e0d8}
  body.avc2 .card[data-avc2]{border-color:#2b57cc;box-shadow:0 0 0 2px rgba(43,87,204,.13),0 1px 2px rgba(18,26,43,.04)}
  .tutor{display:flex;gap:10px;align-items:flex-start;background:#eef2fd;border:1px solid #c9d6f7;border-radius:13px;padding:13px 15px;margin:-14px 0 30px}
  .tutor b{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#2b57cc;font-weight:600}
  .tutor p{margin:4px 0 0;font-size:13px;line-height:1.55;color:#39404f}
  .tutor code{font-family:'IBM Plex Mono',monospace;font-size:11.5px;background:#fff;border:1px solid #c9d6f7;border-radius:5px;padding:1px 5px}
  .foot{margin-top:34px;padding-top:22px;border-top:1px solid #e4e0d8;font-family:'IBM Plex Mono',monospace;font-size:11px;color:#8a8578}
  @media(max-width:560px){.card{flex-wrap:wrap}.card .tags{justify-content:flex-start;width:100%}}
</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow">Material para provas</div>
  <h1>7º semestre</h1>
  <p class="sub">__SUB__</p>
__TUTOR__
  <div class="stats">__STATS__</div>
__AVC2BAR__
__CARDS__
  <div class="foot">Cada arquivo tem quiz e resumo, escolhidos na tela inicial. Gerado por _scripts/atualizar_indice.py</div>
</div>
<script>
(function(){
  var b = document.getElementById('btAvc2');
  if (!b) return;
  var discs = Array.prototype.slice.call(document.querySelectorAll('.disc'));
  b.addEventListener('click', function(){
    var on = !document.body.classList.contains('avc2');
    document.body.classList.toggle('avc2', on);
    // esconde a disciplina inteira quando nenhum material dela cai na prova
    discs.forEach(function(d){
      d.style.display = (on && !d.querySelector('.card[data-avc2]')) ? 'none' : '';
    });
    b.textContent = on ? 'Mostrar tudo' : 'AVC 2';
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
})();
</script>
</body>
</html>
"""


def main():
    local = "--local" in sys.argv
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
                marca = (' data-avc2="1"'
                         if m["arquivo"] in AVC2 or m["arquivo"] in AVC2_EXTRA
                         else "")
                linhas.append(
                    '      <a class="card"{a} href="Quizzes/{f}">'
                    '<span class="n">{i:02d}</span>'
                    '<span class="body"><span class="t">{t}</span><br><span class="e">{e}</span></span>'
                    '<span class="tags"><span class="tag">{q} questões</span>'
                    '<span class="tag">{s} seções</span>'
                    '<span class="tag">{g} imagens</span></span></a>'.format(
                        a=marca, f=H.escape(m["arquivo"]), i=n, t=H.escape(m["titulo"]),
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

        # botao AVC 2: destaca o que cai na prova e apaga o resto
        existem = {m["arquivo"] for m in metas}
        tem = [m for m in metas
               if m["arquivo"] in AVC2 or m["arquivo"] in AVC2_EXTRA]
        q_avc2 = sum(m["q"] for m in tem)
        # conta TEMAS, nao arquivos: "Doencas do SNP" sao dois materiais
        temas_ok = {AVC2[a] for a in AVC2 if a in existem}
        faltam = sorted(set(AVC2.values()) - temas_ok)
        aviso = ""
        if faltam:
            aviso = ('  <div class="avc2falta">Sem material ainda: '
                     + H.escape(" · ".join(faltam)) + "</div>")
        avc2bar = (
            '  <div class="avc2bar">'
            '<button id="btAvc2" type="button" aria-pressed="false">AVC 2</button>'
            f'<span class="avc2info">{len(temas_ok)} de {len(set(AVC2.values()))} temas da prova '
            f'· {len(tem)} materiais · {q_avc2} questões</span></div>\n' + aviso)
    else:
        avc2bar = ""
        cards = ('  <div class="empty">Nenhum material ainda.<br>'
                 'Rode <code>_scripts/montar_quiz.py</code> para gerar o primeiro.</div>')
        stats = ""
        sub = "Nenhum material gerado ainda."

    if local:
        alvo = INDEX_LOCAL
        tutor = '  <div class="tutor"><div><b>Versao local</b><p>Errou uma questao? Abaixo da explicacao aparece um chat para perguntar ao DeepSeek. A chave fica em <code>deepseek_key.js</code>, que nao vai para o repositorio — por isso o tutor nao existe na versao publicada.</p></div></div>' if CHAVE.exists() else '  <div class="tutor"><div><b>Versao local — tutor desligado</b><p>Crie <code>deepseek_key.js</code> na raiz definindo <code>window.DEEPSEEK_KEY</code> para ativar o chat.</p></div></div>'
    else:
        alvo, tutor = INDEX, ""

    alvo.write_text(
        PAGINA.replace("__CARDS__", cards).replace("__SUB__", sub)
              .replace("__STATS__", stats).replace("__TUTOR__", tutor)
              .replace("__AVC2BAR__", avc2bar),
        encoding="utf-8")
    print(f"OK  {len(metas)} material(is) -> {alvo}")
    for m in sorted(metas, key=lambda x: (x["disciplina"], x["titulo"])):
        print(f"    [{m['sigla']:>3}] {m['titulo']}: {m['q']} questões, {m['sec']} seções, "
              f"{m['img']} imagens, {m['mb']:.1f} MB")


if __name__ == "__main__":
    main()
