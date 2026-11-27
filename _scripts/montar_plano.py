# -*- coding: utf-8 -*-
"""Plano de estudo das provas finais (AVG 2026.2) -> plano.html na raiz.

    PYTHONIOENCODING=utf-8 "$PY" _scripts/montar_plano.py
    PYTHONIOENCODING=utf-8 "$PY" _scripts/montar_plano.py --rever   # (re)gera as paginas de revisao antes

O plano e uma linha do tempo, um dia por bloco, com o tempo de cada item. Cada item
aponta para o quiz (resumo) e para a pagina de revisao da prova (Revisao/revisao_*.html),
ja aberta no treino do tema, no simulado com os temas marcados ou na fila de erros.

As paginas de revisao saem do montar_fechamento.py, que mora em
7sem/Nova pagina pra provas (fora do repo); --rever chama ele com --chave por prova,
para que cada prova tenha a propria fila no navegador.

Regras do plano (decididas com o usuario em 23/11/2026):
  - 3 h por dia, todos os dias; prova as 13:30, entao a manha da prova conta ~1h30.
  - Primeiro o que e antigo (AVC 1) e o que veio depois da AVC 2 (nunca estudado);
    o que caiu na AVC 2 fica por ultimo, em simulado misto (foi estudado ha um mes).
  - "Ler + treinar" so para o que tem mais peso; o resto e so treino, e o resumo
    entra pela consulta da propria questao.

O script confere a cobertura: todo material das pastas de cada prova tem de aparecer
num dia ou em "se sobrar tempo". Falta algum -> aviso. Item que ainda nao existe
(material em preparo) sai sem link, marcado "em preparo".
"""
import argparse, html, json, re, subprocess, sys, unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
QUIZZES = RAIZ / "Quizzes"
REVISAO = RAIZ / "Revisao"
FECHAMENTO = RAIZ.parent / "Nova pagina pra provas" / "montar_fechamento.py"
PY = sys.executable

MODOS = {
    "L": ("Ler + treinar", "Resumo: só tabelas e quadros azuis. Depois o treino do tema."),
    "T": ("Treinar", "Direto às questões. Errou: “Consultar no resumo” na própria questão."),
    "S": ("Simulado", "Bloco misto com tempo; a correção vem no fim."),
    "F": ("Fila de erros", "O que você errou ou acertou na dúvida, até sair com 2 acertos confiantes."),
    "P": ("Pegadinhas", "Lista no fim desta prova: onde a aula diverge da referência."),
}

# ---------------------------------------------------------------- provas
PROVAS = {
    "sai": {"sigla": "SAI III", "nome": "Saúde do Adulto e do Idoso III", "data": "2026-11-30",
            "pastas": ["Geriatria", "Psiquiatria", "Neurologia", "Otorrino", "OFTALMO", "Práticas"],
            "simulados": "Simulados/aula_simulado_sai_*.json",
            "detalhe": "Geriatria · Psiquiatria · Neurologia · Otorrino · Oftalmo · Práticas — ~120 questões"},
    "ped": {"sigla": "SCA III", "nome": "Saúde da Criança e do Adolescente III", "data": "2026-12-03",
            "pastas": ["PED"], "simulados": "Simulados/aula_simulado_ped.json", "detalhe": "Pediatria"},
    "go": {"sigla": "SM III", "nome": "Saúde da Mulher III", "data": "2026-12-08",
           "pastas": ["GO"], "simulados": "Simulados/aula_simulado_go.json", "detalhe": "Ginecologia e Obstetrícia"},
    "mfc": {"sigla": "MC VII", "nome": "Medicina e Comunidade VII", "data": "2026-12-10",
            "pastas": ["MFC"], "simulados": "Simulados/aula_simulado_mfc.json", "detalhe": "Medicina de Família e Comunidade — todo o material é de referência"},
}

# Temas que vieram DEPOIS da AVC 2 (aula dada, nunca cobrada em prova)
NOVAS = {
    "tontura_no_idoso", "deficits_sensoriais_no_idoso", "cefaleias", "coma_e_estados_alterados_de_consciencia",
    "epilepsias", "descolamento_de_retina_e_oclusoes_vasculares", "urgencias_oftalmologicas",
    "faringotonsilites_e_saos", "disfonias", "emergencias_psiquiatricas", "psicofarmacoterapia",
    "protocolo_abcde_e_dispositivos", "arritmias", "sindromes_glomerulares", "avaliacao_da_funcao_renal",
    "hemorragias_da_primeira_e_segunda_metade_da_gestacao", "massas_anexiais_e_cancer_de_ovario",
    "ulceras_genitais", "pratica_de_sindromes_hipertensivas",
}

AVC2_GERPSI = ["delirium", "demencia", "depressao_no_idoso", "fragilidade_e_sarcopenia",
               "sindrome_do_imobilismo", "impulsividade_e_compulsividade", "transtorno_depressivo",
               "transtorno_afetivo_bipolar"]
AVC2_NEUOTO = ["alzheimer_e_demencias", "neuropatias_perifericas", "miastenia_gravis_e_guillain_barre",
               "otites", "disacusias", "zumbido_e_tontura", "rinites_e_rinossinusites"]
AVC2_OFT = ["diagnostico_diferencial_do_olho_vermelho", "catarata", "glaucoma", "retinopatia_diabetica",
            "doencas_da_cornea"]
SAI_BASE = ["exame_psiquico", "investigacao_e_avaliacao_psiquiatrica", "fundamentos_e_historia_da_psiquiatria",
            "semiologia_neurologica", "esclerose_lateral_amiotrofica", "otoscopia",
            "anatomo_fisiologia_do_sistema_auditivo", "introducao_a_audiologia", "semiologia_ocular",
            "anatomia_e_fisiologia_ocular_i", "anatomia_e_fisiologia_ocular_ii",
            "analise_critica_de_artigos_cientificos"]
AVC2_PED = ["alergia_e_atopia", "imunidade_parte_2", "imunodeficiencias", "saude_sexual_do_adolescente",
            "simulado_avc_2_ped"]
GO_OBST = ["diabetes_mellitus_gestacional", "sindromes_hipertensivas_na_gestacao"]
GO_GINE = ["distopia_genital", "incontinencia_urinaria", "endometriose_e_algia_pelvica",
           "doenca_inflamatoria_pelvica"]
MFC_TODOS = ["saude_da_populacao_negra", "tontura_na_atencao_primaria", "migracao_refugio_e_apatridia",
             "saude_da_pessoa_com_deficiencia", "saude_do_homem", "transtorno_mental_comum",
             "alcool_e_outras_drogas_na_aps", "saude_da_populacao_em_situacao_de_rua",
             "saude_baseada_em_evidencias"]


def L(q, m, p, **kw): return dict(modo="L", quiz=q, min=m, prova=p, **kw)
def T(q, m, p, **kw): return dict(modo="T", quiz=q, min=m, prova=p, **kw)
def S(temas, n, mins, m, p, rotulo, **kw): return dict(modo="S", temas=temas, n=n, tempo=mins, min=m, prova=p, rotulo=rotulo, **kw)
def F(m, p, **kw): return dict(modo="F", min=m, prova=p, **kw)
def P(m, p, **kw): return dict(modo="P", min=m, prova=p, **kw)


DIAS = [
    ("2026-11-23", "Neurologia: o antigo e o que veio depois da AVC 2", None, [
        L("avc_isquemico_e_hemorragico", 40, "sai"),
        T("parkinsonismo", 20, "sai"),
        L("cefaleias", 40, "sai"),
        L("epilepsias", 40, "sai"),
        L("coma_e_estados_alterados_de_consciencia", 40, "sai"),
    ]),
    ("2026-11-24", "Emergência na véspera da OSCE, e a psicofarmacologia da aula de hoje", None, [
        L("protocolo_abcde_e_dispositivos", 40, "sai"),
        L("arritmias", 40, "sai", nota="o material segue a AHA onde a aula diverge — veja as pegadinhas"),
        L("parada_cardiorrespiratoria", 30, "sai"),
        T("declaracao_de_obito", 20, "sai"),
        L("psicofarmacoterapia", 40, "sai"),
    ]),
    ("2026-11-25", "Psiquiatria", None, [
        L("emergencias_psiquiatricas", 40, "sai"),
        L("transtornos_de_ansiedade", 30, "sai"),
        L("esquizofrenia_e_outras_psicoses", 30, "sai"),
        L("transtornos_por_uso_de_substancias", 30, "sai"),
        T("toc_e_tept", 20, "sai"),
        T("transtornos_alimentares", 20, "sai"),
    ]),
    ("2026-11-26", "Geriatria", None, [
        L("tontura_no_idoso", 40, "sai"),
        L("quedas_no_idoso", 30, "sai"),
        L("osteoporose", 30, "sai"),
        T("deficits_sensoriais_no_idoso", 25, "sai"),
        T("polifarmacia", 20, "sai"),
        T("iatrogenia", 20, "sai"),
    ]),
    ("2026-11-27", "Otorrino e as urgências do olho", None, [
        L("faringotonsilites_e_saos", 40, "sai"),
        L("urgencias_em_otorrinolaringologia", 30, "sai"),
        T("disfonias", 20, "sai"),
        L("urgencias_oftalmologicas", 40, "sai", nota="na OACR o slide e a referência divergem — veja as pegadinhas"),
        T("descolamento_de_retina_e_oclusoes_vasculares", 20, "sai"),
        T("alteracoes_palpebrais", 20, "sai"),
    ]),
    ("2026-11-28", "Sono, neuropsiquiatria, EM e o 1º simulado de prova", None, [
        T("medicina_do_sono", 20, "sai"),
        T("neuropsiquiatria", 20, "sai"),
        T("esclerose_multipla", 20, "sai"),
        S(["simulado_sai_iii_1"], 60, 90, 105, "sai", "Simulado SAI III · 1 — 60 questões novas",
          nota="como na prova: 90 min, sem consulta; depois leia a explicação de cada erro (+15 min)"),
    ]),
    ("2026-11-29", "2º simulado de prova e AVC 2", None, [
        S(["simulado_sai_iii_2"], 60, 90, 105, "sai", "Simulado SAI III · 2 — 60 questões novas",
          nota="90 min sem consulta, depois os erros"),
        S(AVC2_GERPSI + AVC2_NEUOTO + AVC2_OFT, 40, 45, 50, "sai", "AVC 2 · todas as áreas",
          nota="você estudou há um mês; os simulados também cobram estes temas"),
        F(30, "sai"),
    ]),
    ("2026-11-30", "Manhã da prova: 3º simulado e pegadinhas", "Prova de SAI III às 13:30", [
        S(["simulado_sai_iii_3"], 60, 90, 105, "sai", "Simulado SAI III · 3 — 60 questões novas",
          nota="comece cedo; se o tempo apertar, faça 40 em 60 min"),
        P(20, "sai"),
        F(30, "sai", opcional=True),
    ]),
    ("2026-11-30", "Noite, depois da prova", None, [
        T("revisao_global_de_pediatria", 30, "ped", n=30, opcional=True,
          nota="diagnóstico rápido do conteúdo da AVC 1"),
    ]),
    ("2026-12-01", "Pediatria: o que veio depois da AVC 2 e a oncologia", None, [
        L("sindromes_glomerulares", 40, "ped"),
        L("avaliacao_da_funcao_renal", 40, "ped", nota="quatro constantes de Schwartz — veja as pegadinhas"),
        L("tumores_solidos_de_torax_e_abdome", 30, "ped"),
        L("doencas_musculoesqueleticas", 30, "ped"),
        T("cancer_em_pediatria", 20, "ped", n=20),
        T("emergencias_oncologicas_em_pediatria", 20, "ped", n=20),
    ]),
    ("2026-12-02", "Pediatria da AVC 1: endócrino, adolescência e saúde mental", None, [
        T("disturbios_da_tireoide", 22, "ped", n=20),
        T("disturbios_do_eixo_e_puberdade", 22, "ped", n=20),
        T("diabetes_tipos_1_e_2", 22, "ped", n=20),
        T("sindrome_metabolica_e_obesidade", 20, "ped", n=20),
        T("disturbios_alimentares", 22, "ped", n=20),
        T("saude_mental_na_adolescencia", 22, "ped", n=20),
        T("particularidades_da_adolescencia", 22, "ped", n=20),
        T("imunidade", 20, "ped", n=20),
    ]),
    ("2026-12-03", "Manhã da prova: simulado e fila", "Prova de SCA III às 13:30", [
        S(["simulado_sca_iii"], 40, 60, 70, "ped", "Simulado SCA III — 40 questões novas",
          nota="como na prova: 60 min, sem consulta; depois leia a explicação de cada erro"),
        F(30, "ped"),
        P(10, "ped"),
        S(AVC2_PED, 25, 30, 35, "ped", "AVC 2 · Pediatria", opcional=True,
          nota="o simulado já cobra estes temas; faça se sobrar tempo"),
    ]),
    ("2026-12-04", "GO: hemorragias e as práticas novas", None, [
        L("hemorragias_da_primeira_e_segunda_metade_da_gestacao", 40, "go"),
        T("hemorragias_da_primeira_metade_e_gestacao_ectopica", 25, "go", n=25,
          nota="material antigo: onde divergir, vale o do internato (pegadinhas)"),
        L("massas_anexiais_e_cancer_de_ovario", 40, "go"),
        L("ulceras_genitais", 40, "go"),
        T("pratica_de_sindromes_hipertensivas", 20, "go"),
    ]),
    ("2026-12-05", "Gineco do começo do semestre, violência e sexualidade", None, [
        L("infertilidade_conjugal", 35, "go"),
        L("diferenciacao_sexual_e_malformacoes_uterinas", 35, "go"),
        L("doencas_mamarias_benignas", 35, "go"),
        T("imagem_em_mama", 20, "go"),
        L("violencia_sexual", 30, "go"),
        T("sexualidade_feminina", 15, "go"),
    ]),
    ("2026-12-06", "AVC 2 de GO", None, [
        S(GO_OBST, 40, 45, 50, "go", "AVC 2 · DMG e síndromes hipertensivas"),
        S(GO_GINE, 50, 55, 60, "go", "AVC 2 · distopia, incontinência, endometriose, DIP"),
        F(40, "go"),
    ]),
    ("2026-12-07", "Fila de GO e começo de MFC: as aulas de agosto e a mais nova", None, [
        F(40, "go"),
        L("saude_da_populacao_negra", 25, "mfc"),
        L("migracao_refugio_e_apatridia", 25, "mfc"),
        L("saude_da_pessoa_com_deficiencia", 25, "mfc"),
        L("tontura_na_atencao_primaria", 25, "mfc"),
        L("saude_baseada_em_evidencias", 25, "mfc"),
    ]),
    ("2026-12-08", "Manhã da prova: simulado, fila e pegadinhas de GO", "Prova de SM III às 13:30", [
        S(["simulado_sm_iii"], 40, 60, 70, "go", "Simulado SM III — 40 questões novas",
          nota="como na prova: 60 min, sem consulta; depois leia a explicação de cada erro"),
        F(35, "go"),
        P(20, "go"),
    ]),
    ("2026-12-08", "Noite, depois da prova", None, [
        T("saude_do_homem", 20, "mfc", opcional=True),
    ]),
    ("2026-12-09", "MFC: os temas da AVC 2, que você já revisou", None, [
        T("saude_do_homem", 20, "mfc",
          nota="seu Resumo_MFC_Prova.pdf (18/10, na pasta) cobre este e os três seguintes — releia junto"),
        T("transtorno_mental_comum", 25, "mfc"),
        T("alcool_e_outras_drogas_na_aps", 25, "mfc"),
        T("saude_da_populacao_em_situacao_de_rua", 20, "mfc"),
        S(MFC_TODOS, 40, 45, 50, "mfc", "MFC · todos os temas"),
        F(30, "mfc"),
    ]),
    ("2026-12-10", "Manhã da prova: simulado e fila de MFC", "Prova de MC VII às 13:30", [
        S(["simulado_mc_vii"], 40, 60, 70, "mfc", "Simulado MC VII — 40 questões novas",
          nota="como na prova: 60 min, sem consulta; depois leia a explicação de cada erro"),
        F(30, "mfc"),
    ]),
]

SOBRAR = {
    "sai": SAI_BASE + ["inflamacoes_da_via_lacrimal", "ametropias", "estrabismo", "ambliopia",
                       "avaliacao_geriatrica_ampla", "prescricao_medica"],
    "ped": ["simulado", "revisao_global_de_pediatria"],
    "go": [],
    "mfc": [],
}

PEGADINHAS = {
    "sai": [
        "<b>Arritmias</b> — TV polimórfica instável: <b>desfibrilar</b>, sem sincronizar (a aula diz sincronizada). Amiodarona é <b>150 mg EV em 10 min</b>. Cargas de cardioversão pela AHA (a aula usa 100 J para tudo).",
        "<b>Oclusão da artéria central da retina</b> — o slide de urgências manda massagem ocular, acetazolamida e paracentese; a referência atual diz que não têm benefício comprovado e trata como AVC (encaminhar para avaliar trombólise).",
        "<b>Neurite óptica</b> — pulso de metilprednisolona EV acelera a recuperação, mas não muda a visão final; prednisona oral isolada em dose baixa aumentou recorrências (ONTT).",
        "<b>Morte encefálica</b> — vale a CFM 2.173/2017: dois exames clínicos por médicos diferentes e exame complementar obrigatório (o capítulo de coma usa a resolução de 1991).",
        "<b>Epilepsia</b> — etossuximida só trata ausência; carbamazepina e fenitoína pioram ausência e mioclonia.",
        "<b>Tontura</b> — ondansetrona é anti-5-HT3, não antidopaminérgico; VPPB se trata com manobra, não com supressor vestibular.",
        "<b>Psicofármacos</b> — bupropiona é dopaminérgica + noradrenérgica; BZD <b>aumenta</b> o tempo de reação; lítio no 1º trimestre é contraindicação relativa.",
        "<b>Emergência psiquiátrica</b> — contenção mecânica é último recurso, não “menos efeitos que a medicamentosa”.",
        "<b>Depressão</b> — o DSM-5 exige humor deprimido <b>ou</b> anedonia (o slide pedia os dois).",
        "<b>Fragilidade</b> — a aula usa a escala FRAIL, não o fenótipo de Fried; o SARC-F vai até 10 (o “&gt; 10” é do SARC-CalF).",
        "<b>Faringotonsilite</b> — hiperplasia de tonsila dá voz <b>abafada</b> (“batata quente”), não hipernasal.",
        "<b>AVC isquêmico</b> — o material de AVC tem trechos antigos: hoje a trombólise EV vai até <b>4,5 h</b> (não 3 h); sem trombólise, tolera-se PA até 220/120; para trombolisar, PA &lt; 185/110 (AHA/ASA 2019).",
        "<b>Demência</b> — as aulas de Geriatria e Neurologia exigem 2 ou mais domínios cognitivos; o transtorno neurocognitivo maior do DSM-5-TR exige 1 só (e memória não é obrigatória). Responda pelo critério que a questão citar.",
        "<b>Surdez súbita</b> — a aula de disacusias trata com prednisona + pentoxifilina + valaciclovir; a diretriz AAO-HNS 2019 deixa só o corticoide (antiviral e vasoativo não são de rotina), idealmente nas 2 primeiras semanas.",
        "<b>Osteoporose</b> — rastreio com DXA a partir dos 65 anos (mulher) e 70 (homem), antes se houver fator de risco; o intervalo de repetição é individual (a aula de AGA fala em “a cada 2 anos”).",
    ],
    "ped": [
        "<b>Schwartz</b> — a constante atual é 0,413 (CKiD bedside); o k antigo 0,55 superestima a TFG e esconde a perda de função.",
        "<b>Síndrome nefrótica</b> — proteinúria ≥ 40 mg/m²/<b>hora</b> (o slide escreve “em 24 h”).",
        "<b>Doença granulomatosa crônica</b> — neutrófilos em número <b>normal</b>; o defeito é qualitativo (DHR/NBT).",
        "<b>Anafilaxia</b> — adrenalina 0,01 mg/kg IM (1:1000) na coxa, máx. 0,3 mg na criança, repetir a cada 5–15 min.",
        "<b>GNPE</b> — penicilina benzatina mesmo se a faringite já passou (o material adotou a página 94).",
    ],
    "go": [
        "<b>β-hCG</b> — na gestação viável sobe pelo menos ~35–50% em 48 h; “duplicar” é pegadinha (o material antigo cobra duplicar).",
        "<b>Aborto incompleto</b> estável — expectante, misoprostol ou AMIU (não “sempre esvaziar”). Ameaça de aborto: repouso e progesterona de rotina sem benefício estabelecido.",
        "<b>Síndromes hipertensivas</b> — cortes de 2025: plaquetas &lt; 100 mil, TGO/TGP &gt; 70, creatinina &gt; 1,1, proteinúria em fita ≥ 2+ (os de 2023 aparecem como distratores).",
        "<b>Sulfato de magnésio</b> — a prática suspende com FR &lt; 12; o teórico, com &lt; 16. Veja a tabela no resumo da prática.",
        "<b>DIP</b> — reavaliar em 72 h.",
        "<b>Cancro mole</b> — azitromicina 1 g dose única é a 1ª linha.",
        "<b>Massas anexiais</b> — o maligno é o cistoadeno<b>carcinoma</b>; coriocarcinoma é germinativo, não estromal.",
    ],
    "mfc": [
        "Todo o material de MFC é de referência (políticas do SUS e diretrizes), sem slide da aula. Se a prova cobrar algo específico da aula, é lacuna conhecida.",
        "<b>Fumante</b> — abordagem breve (mínima, ~3 min) é o <b>PAAP</b>: perguntar, avaliar, aconselhar, preparar. Com o <b>acompanhar</b> vira PAAPA, a abordagem básica.",
        "<b>Internação involuntária</b> — comunicada ao Ministério Público em 72 h (Lei 10.216/2001); na dependência química (Lei 13.840/2019) dura no máximo 90 dias.",
        "<b>Tiamina</b> no etilista — antes ou junto da glicose, sem atrasar a correção da hipoglicemia.",
        "<b>Câncer de próstata</b> — o Ministério da Saúde e o INCA não recomendam rastreio populacional; é decisão compartilhada.",
    ],
}


# ---------------------------------------------------------------- utilidades
def snake(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s\-]+", "_", s)
    return re.sub(r"_+", "_", s).strip("_") or "quiz"


def slugificar(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower() or "tema"


def bancos():
    """quiz (sem prefixo) -> dados do aula_*.json que o gera."""
    out = {}
    for p in sorted(RAIZ.glob("*/aula_*.json")):
        if p.parent.name in ("Quizzes", "_template", "_scripts", "Revisao"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        if not (QUIZZES / ("quiz_%s.html" % snake(d["titulo"]))).exists():
            continue        # banco sem quiz montado ainda (agente no meio do trabalho)
        out[snake(d["titulo"])] = {
            "titulo": d["titulo"], "pasta": p.parent.name, "q": len(d["questoes"]),
            "slug": slugificar(p.stem.replace("aula_", "")),
            "ref": "Referência" in (d.get("eyebrow") or ""),
        }
    return out


def rever():
    for pid, pv in PROVAS.items():
        # so banco com quiz montado: aula_*.json pela metade (agente trabalhando) fica de fora
        aulas = []
        globs = ["%s/aula_*.json" % x for x in pv["pastas"]]
        if pv.get("simulados"):
            globs.append(pv["simulados"])      # simulados de prova entram como tema da revisao
        for g in globs:
            for a in sorted(RAIZ.glob(g)):
                t = json.loads(a.read_text(encoding="utf-8")).get("titulo", "")
                if (QUIZZES / ("quiz_%s.html" % snake(t))).exists():
                    aulas.append(str(a))
        if not aulas:
            print("  ~ %s: nenhum material ainda, sem revisao" % pid)
            continue
        cmd = [PY, str(FECHAMENTO), *aulas, "--fonte", str(RAIZ),
               "--titulo", "Revisão · " + pv["sigla"],
               "--eyebrow", "%s · prova em %s" % (pv["nome"], fmt(pv["data"])),
               "--chave", pid, "--voltar", "../plano.html|Plano de estudo",
               "--saida", str(REVISAO / ("revisao_%s.html" % pid))]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
        if r.returncode:
            sys.exit("falhou a revisao de %s:\n%s%s" % (pid, r.stdout, r.stderr))
        resumo = [l for l in r.stdout.splitlines() if "questões ·" in l]
        print("  revisao_%s.html  %s" % (pid, resumo[0].strip() if resumo else ""))


DSEM = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


def fmt(s):
    y, m, d = map(int, s.split("-"))
    return "%02d/%02d" % (d, m)


def fmt_dia(s):
    y, m, d = map(int, s.split("-"))
    return "%s %02d/%02d" % (DSEM[date(y, m, d).weekday()], d, m)


def e(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- pagina
CSS = """
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{background:#f5f3ef;color:#121a2b;font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:#2b57cc}
.wrap{max-width:760px;margin:0 auto;padding:48px 16px 80px}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#2b57cc;margin-bottom:14px}
.eyebrow a{color:inherit;text-decoration:none}
h1{font-family:'Newsreader',Georgia,serif;font-size:38px;line-height:1.08;font-weight:400;letter-spacing:-.025em;margin:0 0 14px}
.sub{font-size:15px;line-height:1.65;color:#5b6478;margin:0 0 26px;max-width:58ch}
.provas{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-bottom:26px}
.pv{display:block;background:#fff;border:1px solid #e4e0d8;border-radius:14px;padding:14px 15px;text-decoration:none;color:inherit}
.pv:hover{border-color:#121a2b}
.pv .s{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#8a8578}
.pv .d{font-family:'Newsreader',Georgia,serif;font-size:24px;font-weight:500;margin:2px 0}
.pv .f{font-family:'IBM Plex Mono',monospace;font-size:11px;color:#2b57cc}
.pv .bar{height:5px;background:#eee9df;border-radius:9px;margin-top:9px;overflow:hidden}
.pv .bar i{display:block;height:100%;background:#2b57cc;width:0}
.pv.past{opacity:.5}
details.como{background:#eef2fd;border:1px solid #c9d6f7;border-radius:13px;padding:12px 15px;margin-bottom:30px}
details.como summary{cursor:pointer;font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#2b57cc;font-weight:600}
details.como ul{margin:10px 0 2px;padding-left:18px}details.como li{margin:5px 0;color:#39404f;font-size:13.5px}
.dia{margin:0 0 22px;scroll-margin-top:16px}
.dia h2{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;font-family:'Newsreader',Georgia,serif;font-size:22px;font-weight:500;letter-spacing:-.015em;margin:0 0 3px}
.dia h2 .dt{font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#8a8578}
.dia .meta{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.06em;color:#8a8578;margin-bottom:10px}
.dia.hoje h2 .dt{color:#fff;background:#2b57cc;border-radius:99px;padding:2px 10px}
.dia.passado{opacity:.62}
.itens{background:#fff;border:1px solid #e4e0d8;border-radius:16px;overflow:hidden}
.dia.hoje .itens{border-color:#2b57cc;box-shadow:0 0 0 2px rgba(43,87,204,.12)}
.it{display:flex;gap:12px;align-items:flex-start;padding:12px 15px;border-top:1px solid #efebe4}
.it:first-child{border-top:0}
.it input{margin-top:3px;width:17px;height:17px;accent-color:#2b57cc;flex-shrink:0}
.it .c{flex:1;min-width:0}
.it .t{font-size:15px;font-weight:500;line-height:1.35}
.it.feito .t{text-decoration:line-through;color:#8a8578}
.it .sub2{font-size:12.5px;color:#6b7385;margin-top:2px}
.chip{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.06em;text-transform:uppercase;border-radius:99px;padding:2px 8px;margin-right:6px;vertical-align:1px;border:1px solid #e4e0d8;color:#5b6478;background:#faf9f6}
.chip.L{background:#121a2b;border-color:#121a2b;color:#fff}
.chip.S{background:#eef2fd;border-color:#c9d6f7;color:#2b57cc}
.chip.F{background:#fdf4e6;border-color:#f0dcbc;color:#8a5a1f}
.tg{font-family:'IBM Plex Mono',monospace;font-size:10px;color:#8a8578;margin-left:4px}
.tg.nova{color:#1b7a4b}.tg.ref{color:#8a5a1f}.tg.avc2{color:#2b57cc}
.acts{display:flex;gap:6px;flex-wrap:wrap;margin-top:7px}
.acts a{font-family:'IBM Plex Mono',monospace;font-size:11px;text-decoration:none;color:#121a2b;border:1px solid #d9d4ca;border-radius:9px;padding:4px 10px;background:#faf9f6}
.acts a:hover{border-color:#121a2b}
.acts a.pri{background:#2b57cc;border-color:#2b57cc;color:#fff}
.acts span.off{font-family:'IBM Plex Mono',monospace;font-size:11px;color:#a39d90;border:1px dashed #d9d4ca;border-radius:9px;padding:4px 10px}
.it .mn{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:#8a8578;white-space:nowrap;margin-top:2px}
.prova{display:flex;align-items:center;gap:10px;background:#121a2b;color:#fff;border-radius:14px;padding:12px 16px;margin:4px 0 26px;font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.06em}
.prova b{font-family:'Newsreader',Georgia,serif;font-size:19px;font-weight:500;letter-spacing:0}
details.peg{background:#fff;border:1px solid #e4e0d8;border-radius:14px;padding:12px 15px;margin:-14px 0 14px}
details.peg summary{cursor:pointer;font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:#8a5a1f;font-weight:600}
details.peg li{margin:7px 0;font-size:13.5px;line-height:1.55;color:#39404f}
details.peg ul{padding-left:18px;margin:8px 0 2px}
.sobra{font-size:13px;color:#5b6478;margin:-14px 0 14px}
.sobra a{font-family:'IBM Plex Mono',monospace;font-size:11px}
.foot{margin-top:34px;padding-top:20px;border-top:1px solid #e4e0d8;font-family:'IBM Plex Mono',monospace;font-size:11px;color:#8a8578;line-height:1.7}
@media(max-width:560px){h1{font-size:31px}.it{gap:10px;padding:11px 12px;flex-wrap:wrap}.it .c{flex-basis:calc(100% - 30px)}.it .mn{width:100%;padding-left:27px;margin-top:-4px}}
"""

JS = r"""
(function(){
  var K = 'plano-avg-2026-2', feitos = {};
  try { feitos = JSON.parse(localStorage.getItem(K) || '{}') || {}; } catch (e) { feitos = {}; }
  function salvar(){ try { localStorage.setItem(K, JSON.stringify(feitos)); } catch (e) {} }
  var d = new Date(), hoje = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  var boxes = document.querySelectorAll('.it input[type=checkbox]');
  function atualizar(){
    var tot = {}, ok = {};
    Array.prototype.forEach.call(boxes, function(b){
      var it = b.closest('.it'), p = it.getAttribute('data-prova'), m = +it.getAttribute('data-min');
      if (it.getAttribute('data-opc')) return;
      tot[p] = (tot[p] || 0) + m; if (b.checked) ok[p] = (ok[p] || 0) + m;
    });
    Object.keys(tot).forEach(function(p){
      var el = document.querySelector('.pv[data-prova="' + p + '"]');
      if (!el) return;
      var pct = Math.round((ok[p] || 0) / tot[p] * 100);
      el.querySelector('.bar i').style.width = pct + '%';
      el.querySelector('.f').textContent = pct + '% feito';
    });
  }
  Array.prototype.forEach.call(boxes, function(b){
    var it = b.closest('.it'), id = it.getAttribute('data-id');
    b.checked = !!feitos[id]; it.classList.toggle('feito', b.checked);
    b.addEventListener('change', function(){
      if (b.checked) feitos[id] = 1; else delete feitos[id];
      it.classList.toggle('feito', b.checked); salvar(); atualizar();
    });
  });
  var alvo = null;
  Array.prototype.forEach.call(document.querySelectorAll('.dia'), function(el){
    var dt = el.getAttribute('data-dia');
    if (dt < hoje) el.classList.add('passado');
    if (dt === hoje) { el.classList.add('hoje'); if (!alvo) alvo = el; }
    if (!alvo && dt > hoje) alvo = el;
  });
  Array.prototype.forEach.call(document.querySelectorAll('.pv'), function(el){
    if (el.getAttribute('data-dia') < hoje) el.classList.add('past');
  });
  atualizar();
  if (alvo && !location.hash) setTimeout(function(){ alvo.scrollIntoView({ block: 'start' }); }, 60);
})();
"""


def montar(bc):
    faltam, usados = [], {pid: set() for pid in PROVAS}
    corpo = []
    total = {pid: 0 for pid in PROVAS}
    prova_fechada = set()

    def rev(pid):
        return "Revisao/revisao_%s.html" % pid

    def tem_rev(pid):
        return (REVISAO / ("revisao_%s.html" % pid)).exists()

    def item(i, k, dia):
        modo, pid = i["modo"], i["prova"]
        rot, dica = MODOS[modo]
        opc = i.get("opcional")
        if not opc:
            total[pid] += i["min"]
        tags, acts, titulo, sub = [], [], "", i.get("nota", "")
        if modo in "LT":
            q = i["quiz"]
            usados[pid].add(q)
            b = bc.get(q)
            if b:
                titulo = e(b["titulo"])
                n = i.get("n")
                qtxt = ("%d de %d questões" % (n, b["q"])) if n and n < b["q"] else ("%d questões" % b["q"])
                if b["ref"]:
                    tags.append('<span class="tg ref">referência</span>')
                elif q in NOVAS:
                    tags.append('<span class="tg nova">depois da AVC 2</span>')
                else:
                    tags.append('<span class="tg">antigo</span>')
                quiz = "Quizzes/quiz_%s.html" % q
                treino = "%s#treino=%s%s" % (rev(pid), b["slug"], ("&n=%d" % n) if n and n < b["q"] else "")
                if modo == "L":
                    acts.append('<a href="%s">Resumo</a>' % e(quiz))
                if tem_rev(pid):
                    acts.append('<a class="pri" href="%s">Treinar · %s</a>' % (e(treino), qtxt))
                else:
                    acts.append('<a class="pri" href="%s">Quiz · %s</a>' % (e(quiz), qtxt))
                if modo == "T":
                    acts.append('<a href="%s">Resumo</a>' % e(quiz))
            else:
                faltam.append(q)
                titulo = e(q.replace("_", " ").capitalize())
                acts.append('<span class="off">em preparo</span>')
        elif modo == "S":
            for q in i["temas"]:
                usados[pid].add(q)
            ok = [bc[q] for q in i["temas"] if q in bc]
            for q in i["temas"]:
                if q not in bc:
                    faltam.append(q)
            titulo = e(i["rotulo"])
            nq = sum(b["q"] for b in ok)
            sub = sub or "%d questões de %d temas, %d min de prova" % (i["n"], len(ok), i["tempo"])
            if any(q in AVC2_GERPSI + AVC2_NEUOTO + AVC2_OFT + AVC2_PED + GO_OBST + GO_GINE for q in i["temas"]):
                tags.append('<span class="tg avc2">AVC 2</span>')
            if ok and tem_rev(pid):
                href = "%s#simulado=%s&n=%d&min=%d" % (rev(pid), ",".join(b["slug"] for b in ok), i["n"], i["tempo"])
                acts.append('<a class="pri" href="%s">Abrir simulado</a>' % e(href))
            else:
                acts.append('<span class="off">em preparo</span>')
        elif modo == "F":
            titulo = "Fila de erros e dúvidas"
            sub = sub or "o que você errou ou acertou na dúvida nesta prova"
            if tem_rev(pid):
                acts.append('<a class="pri" href="%s#revisao">Abrir a fila</a>' % e(rev(pid)))
            else:
                acts.append('<span class="off">em preparo</span>')
        elif modo == "P":
            titulo = "Pegadinhas: onde a aula diverge da referência"
            sub = "a lista logo abaixo"
            acts.append('<a href="#peg-%s">Ver a lista</a>' % pid)
        sig = PROVAS[pid]["sigla"]
        chip = '<span class="chip %s" title="%s">%s</span>' % (modo, e(dica), rot)
        if opc:
            chip += '<span class="chip">se der tempo</span>'
        # id estavel: reordenar o dia nao troca o que ja foi marcado
        idd = "%s-%s-%s" % (dia, pid, i.get("quiz") or snake(i.get("rotulo", "")) or i["modo"])
        return ('<div class="it" data-id="%s" data-prova="%s" data-min="%d"%s>'
                '<input type="checkbox" aria-label="feito">'
                '<div class="c"><div class="t">%s%s%s</div>%s<div class="acts">%s</div></div>'
                '<div class="mn">%d min · %s</div></div>'
                % (e(idd), pid, i["min"], ' data-opc="1"' if opc else "", chip, titulo, "".join(tags),
                   ('<div class="sub2">%s</div>' % e(sub)) if sub else "", "".join(acts), i["min"], sig))

    for dia, titulo, prova_txt, itens in DIAS:
        mins = sum(i["min"] for i in itens if not i.get("opcional"))
        h = ['<section class="dia" data-dia="%s">' % dia,
             '<h2><span class="dt">%s</span>%s</h2>' % (fmt_dia(dia), e(titulo)),
             '<div class="meta">%d min%s</div>' % (mins, " · " + e(prova_txt) if prova_txt else ""),
             '<div class="itens">']
        for k, i in enumerate(itens):
            h.append(item(i, k, dia))
        h.append("</div></section>")
        corpo.append("\n".join(h))
        if prova_txt:
            pid = [p for p, v in PROVAS.items() if v["data"] == dia][0]
            pv = PROVAS[pid]
            corpo.append('<div class="prova" id="prova-%s">Prova · <b>%s</b> · %s às 13:30</div>'
                         % (pid, e(pv["nome"]), fmt_dia(dia)))
            corpo.append('<details class="peg" id="peg-%s"><summary>Pegadinhas de %s</summary><ul>%s</ul></details>'
                         % (pid, pv["sigla"], "".join("<li>%s</li>" % x for x in PEGADINHAS[pid])))
            sob = [q for q in SOBRAR[pid] if q in bc and q not in usados[pid]]
            sob_links = []
            for q in sob:
                usados[pid].add(q)
                href = ("%s#treino=%s" % (rev(pid), bc[q]["slug"])) if tem_rev(pid) else "Quizzes/quiz_%s.html" % q
                sob_links.append('<a href="%s">%s</a>' % (e(href), e(bc[q]["titulo"])))
            for q in SOBRAR[pid]:
                usados[pid].add(q)
            if sob_links:
                corpo.append('<p class="sobra">Se sobrar tempo: %s</p>' % " · ".join(sob_links))
            prova_fechada.add(pid)

    # cobertura: todo material das pastas da prova aparece em algum lugar
    avisos = []
    for pid, pv in PROVAS.items():
        da_prova = {q for q, b in bc.items() if b["pasta"] in pv["pastas"]}
        fora = sorted(da_prova - usados[pid])
        if fora:
            avisos.append("%s sem lugar no plano: %s" % (pv["sigla"], ", ".join(fora)))

    cards = []
    for pid, pv in PROVAS.items():
        cards.append('<a class="pv" href="#prova-%s" data-prova="%s" data-dia="%s"><div class="s">%s · %s</div>'
                     '<div class="d">%s</div><div class="f">0%% feito</div><div class="bar"><i></i></div></a>'
                     % (pid, pid, pv["data"], e(pv["sigla"]), e(pv["detalhe"].split(" — ")[0]),
                        fmt_dia(pv["data"]), ))
    revs = " · ".join('<a href="%s">%s</a>' % (e(rev(p)), e(PROVAS[p]["sigla"])) for p in PROVAS if tem_rev(p))

    como = """
<details class="como"><summary>Como usar este plano</summary><ul>
<li><b>3 h por dia.</b> Primeiro o que é antigo e o que veio depois da AVC 2; o que caiu na AVC 2 fica para o fim, em simulado misto, porque você estudou há um mês.</li>
<li><b>Ler + treinar:</b> abra o resumo e leia só as tabelas e os quadros azuis (é onde estão os critérios e as pegadinhas). Depois, “Treinar”.</li>
<li><b>Treinar:</b> vai direto às questões, na página de revisão da prova. Errou? O botão “Consultar no resumo” abre o trecho exato.</li>
<li><b>Marque “estou em dúvida” quando chutar.</b> Acerto no chute também entra na fila de erros, e é a fila que você revisa na manhã da prova.</li>
<li><b>Atrasou?</b> Não empurre o dia seguinte. Pule um “Treinar” e mantenha os “Ler + treinar”; o que ficou para trás aparece na fila e nos simulados.</li>
<li>O progresso fica salvo neste navegador: o do celular e o do computador são separados.</li>
</ul></details>"""

    hoje = date.today()
    pagina = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Plano das provas finais</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;450;500;600&display=swap" rel="stylesheet">
<style>%s</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow"><a href="index.html" id="voltaIdx">← Materiais</a> · AVG 2026.2</div>
  <h1>Plano das provas finais</h1>
  <p class="sub">Quatro provas em onze dias, três horas por dia. Cada item abre o treino ou o simulado certo
  na página de revisão da prova, e cada prova tem a própria fila de erros.</p>
  <div class="provas">%s</div>
%s
%s
  <div class="foot">Páginas de revisão: %s<br>Gerado em %02d/%02d/%d por _scripts/montar_plano.py</div>
</div>
<script>
// aberto por duplo clique, "Materiais" volta ao indice local
if (location.protocol === 'file:') document.getElementById('voltaIdx').href = 'index_local.html';
%s
</script>
</body>
</html>
""" % (CSS, "".join(cards), como, "\n".join(corpo), revs or "ainda não geradas",
       hoje.day, hoje.month, hoje.year, JS)
    return pagina, faltam, avisos, total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rever", action="store_true", help="(re)gera Revisao/revisao_*.html antes do plano")
    a = ap.parse_args()
    if a.rever:
        REVISAO.mkdir(exist_ok=True)
        if not FECHAMENTO.exists():
            sys.exit("Nao achei o montar_fechamento.py em %s" % FECHAMENTO)
        rever()
    bc = bancos()
    pagina, faltam, avisos, total = montar(bc)
    (RAIZ / "plano.html").write_text(pagina, encoding="utf-8", newline="\n")
    print("plano.html  " + " · ".join("%s %dh%02d" % (PROVAS[p]["sigla"], t // 60, t % 60) for p, t in total.items()))
    for dia, titulo, _, itens in DIAS:
        m = sum(i["min"] for i in itens if not i.get("opcional"))
        if m > 185:
            print("  aviso: %s passa de 3 h (%d min)" % (fmt_dia(dia), m))
    if faltam:
        print("  em preparo (%d): %s" % (len(set(faltam)), ", ".join(sorted(set(faltam)))))
    for x in avisos:
        print("  aviso: " + x)


if __name__ == "__main__":
    main()
