#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
checar_deepseek.py — segunda opiniao sobre os materiais, feita pelo DeepSeek.

    python _scripts/checar_deepseek.py --avc2            # so o que cai na AVC 2
    python _scripts/checar_deepseek.py --limite 3        # piloto
    python _scripts/checar_deepseek.py tireoide otites   # materiais escolhidos
    python _scripts/checar_deepseek.py --todos

Para cada material manda ao DeepSeek o trio (conteudo extraido + quiz + resumo)
e pede uma conferencia factual. Grava um .json por material em _checagem/ e um
relatorio consolidado em _checagem/RELATORIO.md.

NAO corrige nada. O que volta e PISTA para conferencia humana, nao veredito: o
modelo erra, e em varios materiais o conteudo correto foi deliberadamente
expandido alem da fonte (e esta declarado nos resumos).

Fontes protegidas (capitulo de livro, anotacao de terceiro) sao PULADAS: elas
estao no .gitignore justamente por nao poderem circular, e mandar para uma API
externa seria publica-las. Use --incluir-protegidas para forcar.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "_checagem"
CHAVE = RAIZ / "deepseek_key.js"
ENDPOINT = "https://api.deepseek.com/chat/completions"
MODELO = "deepseek-v4-flash"

SISTEMA = """Você é um revisor técnico de material didático de medicina. Recebe três
peças sobre a MESMA aula e confere se o quiz e o resumo são fiéis à fonte.

Trabalhe apenas com o que está na FONTE. Não use conhecimento próprio para dizer
que algo está errado: use-o apenas para marcar algo como "não está na fonte".

Convenções do formato que você vai ler:
- No quiz, a alternativa correta é SEMPRE a primeira da lista ("options[0]") e
  "correctIndex" é sempre 0. Isso é proposital — a página embaralha na exibição.
  NUNCA reporte isso como problema.
- O resumo é escrito para quem não assistiu à aula, então não cita "a aula" nem
  "o slide". Isso também é proposital.

LIMITAÇÃO SUA, E ELA É GRANDE: a FONTE que você recebe é só o TEXTO extraído
dos slides. As figuras NÃO vêm junto. Onde você vê um marcador
`<!-- IMG:pg07 -->` ou `<!-- IMG:s12i1 -->`, havia uma imagem que você não
enxerga — e nestes materiais é comum que tabelas, fluxogramas, critérios,
doses e classificações inteiras existam SÓ na imagem. Quem escreveu o quiz
abriu essas figuras; você não.

Portanto: "não está no texto" NÃO significa "não está na fonte". Antes de
marcar algo como "fora_da_fonte", pergunte-se se aquilo é o tipo de conteúdo
que estaria numa figura da página citada. Se for, use o tipo
"possivelmente_na_imagem" com gravidade "baixa" — ou simplesmente não reporte.
Reserve "fora_da_fonte" para afirmação que não caberia em nenhuma figura da
aula (por exemplo, um protocolo inteiro num material cuja fonte sequer toca no
assunto). Expandir além da fonte é permitido quando o material declara.

Seu valor está em 1, 2 e 3 abaixo. Não encha o relatório de 4.

Procure, em ordem de importância:
1. "erro_factual"   — a alternativa correta contradiz a fonte, ou um número,
                      dose, corte ou classificação diverge do que a fonte diz.
2. "ambigua"        — mais de uma alternativa é defensável, ou a correta não é
                      claramente melhor que as outras.
3. "divergencia"    — o resumo afirma uma coisa e o quiz outra.
4. "fora_da_fonte"  — afirmação do quiz ou do resumo que a fonte não sustenta.
5. "possivelmente_na_imagem" — a afirmação não está no texto, mas caberia numa
                      figura da aula. Gravidade sempre "baixa".
6. "fonte_suspeita" — a própria fonte se contradiz ou tem erro evidente.

Responda SOMENTE com JSON válido, sem comentário fora dele, neste formato:

{"achados":[{"tipo":"erro_factual","onde":"quiz Q12","gravidade":"alta",
"o_que":"frase curta do problema","na_fonte":"trecho literal da fonte, ou null",
"sugestao":"o que fazer"}],"veredito":"uma frase sobre o material como um todo"}

Use gravidade "alta" só quando estudar por aquilo levaria a errar na prova ou na
clínica. Se não encontrar nada, devolva {"achados":[],"veredito":"..."}.
Escreva em português."""


def ler_chave():
    if not CHAVE.exists():
        sys.exit(f"chave nao encontrada: {CHAVE}")
    m = re.search(r"""['"](sk-[^'"]+)['"]""", CHAVE.read_text(encoding="utf-8"))
    if not m:
        sys.exit("nao achei uma chave sk-... dentro de deepseek_key.js")
    return m.group(1)


def ignorado_pelo_git(p: Path) -> bool:
    """O .gitignore e a nossa lista de material que nao pode circular."""
    r = subprocess.run(["git", "check-ignore", "-q", str(p)], cwd=RAIZ)
    return r.returncode == 0


def materiais():
    """Devolve (tema, disciplina, conteudo, json do quiz, resumo) de cada material."""
    for j in sorted(RAIZ.glob("*/aula_*.json")):
        tema = j.name[5:-5]
        d = j.parent
        c, r = d / f"conteudo_{tema}.md", d / f"resumo_{tema}.md"
        if c.exists() and r.exists():
            yield tema, d.name, c, j, r


def temas_avc2():
    """Le o AVC2 do atualizar_indice.py para nao duplicar a lista aqui."""
    txt = (RAIZ / "_scripts" / "atualizar_indice.py").read_text(encoding="utf-8")
    bloco = re.search(r"AVC2 = \{(.*?)\n\}", txt, re.S)
    if not bloco:
        return set()
    return {m[5:-5] for m in re.findall(r'"(quiz_[^"]+\.html)"', bloco.group(1))}


def perguntar(chave, fonte, quiz, resumo, tentativas=3):
    corpo = (f"## FONTE (texto extraído da aula — é a referência)\n\n{fonte}\n\n"
             f"## QUIZ (JSON)\n\n{quiz}\n\n"
             f"## RESUMO\n\n{resumo}")
    dados = json.dumps({
        "model": MODELO,
        "messages": [{"role": "system", "content": SISTEMA},
                     {"role": "user", "content": corpo}],
        # e modelo de raciocinio: os reasoning_tokens saem do mesmo teto, entao
        # 8000 truncava o JSON no meio e o parse falhava
        "max_tokens": int(os.environ.get("CHECAR_MAX_TOKENS", "20000")),
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request(ENDPOINT, data=dados, headers={
        "Authorization": "Bearer " + chave, "Content-Type": "application/json"})

    for n in range(tentativas):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                resp = json.load(r)
            esc = resp["choices"][0]
            txt = esc["message"]["content"]
            fim = esc.get("finish_reason")
            uso = resp.get("usage", {})
            try:
                return json.loads(txt), uso, None
            except json.JSONDecodeError:
                m = re.search(r"\{.*\}", txt, re.S)
                if m:
                    try:
                        return json.loads(m.group(0)), uso, None
                    except json.JSONDecodeError:
                        pass
                if fim == "length" and n < tentativas - 1:
                    continue           # truncou: tenta de novo
                (SAIDA / "_bruto.txt").write_text(txt, encoding="utf-8")
                return None, uso, (f"resposta nao era JSON (finish_reason={fim}, "
                                   f"{len(txt)} chars; bruto em _checagem/_bruto.txt)")
        except urllib.error.HTTPError as e:
            det = e.read().decode()[:200]
            if e.code in (429, 500, 502, 503) and n < tentativas - 1:
                time.sleep(12 * (n + 1))
                continue
            return None, {}, f"HTTP {e.code}: {det}"
        except Exception as e:
            if n < tentativas - 1:
                time.sleep(8)
                continue
            return None, {}, f"{type(e).__name__}: {e}"
    return None, {}, "falhou apos as tentativas"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("temas", nargs="*", help="temas a checar (padrao: todos)")
    ap.add_argument("--avc2", action="store_true", help="so os materiais da AVC 2")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--limite", type=int, default=0, help="para piloto")
    ap.add_argument("--incluir-protegidas", action="store_true")
    ap.add_argument("--refazer-relatorio", action="store_true",
                    help="so remonta o RELATORIO.md a partir dos .json ja salvos")
    a = ap.parse_args()

    SAIDA.mkdir(exist_ok=True)
    if a.refazer_relatorio:
        # checar um tema avulso sobrescreve o relatorio com so aquele tema;
        # isto o remonta a partir de tudo que ja esta salvo em _checagem/
        res, pul = [], []
        for tema, disc, c, j, r in materiais():
            f = SAIDA / f"{tema}.json"
            if f.exists():
                res.append(json.loads(f.read_text(encoding="utf-8")))
            elif ignorado_pelo_git(c):
                pul.append((tema, "fonte protegida (esta no .gitignore)"))
        relatorio(res, pul, 0, 0)
        print(f"relatorio remontado com {len(res)} material(is)")
        return

    chave = ler_chave()
    alvo_avc2 = temas_avc2() if a.avc2 else None

    fila, pulados = [], []
    for tema, disc, c, j, r in materiais():
        if a.temas and tema not in a.temas:
            continue
        if alvo_avc2 is not None and tema not in alvo_avc2:
            continue
        if ignorado_pelo_git(c) and not a.incluir_protegidas:
            pulados.append((tema, "fonte protegida (está no .gitignore)"))
            continue
        fila.append((tema, disc, c, j, r))
    if a.limite:
        fila = fila[:a.limite]

    print(f"{len(fila)} material(is) para checar; {len(pulados)} pulado(s)\n")
    for tema, motivo in pulados:
        print(f"  PULADO  {tema}: {motivo}")
    if pulados:
        print()

    tot_in = tot_out = 0
    resultados = []
    for i, (tema, disc, c, j, r) in enumerate(fila, 1):
        destino = SAIDA / f"{tema}.json"
        print(f"[{i}/{len(fila)}] {tema} ... ", end="", flush=True)
        achado, uso, erro = perguntar(
            chave, c.read_text(encoding="utf-8"),
            j.read_text(encoding="utf-8"), r.read_text(encoding="utf-8"))
        tot_in += uso.get("prompt_tokens", 0)
        tot_out += uso.get("completion_tokens", 0)
        if erro:
            print(f"ERRO: {erro}")
            resultados.append({"tema": tema, "disciplina": disc, "erro": erro})
        else:
            n = len(achado.get("achados", []))
            altas = sum(1 for x in achado["achados"] if x.get("gravidade") == "alta")
            print(f"{n} achado(s), {altas} de gravidade alta")
            achado.update(tema=tema, disciplina=disc)
            resultados.append(achado)
        # grava a cada passo: se o limite de API cair, nao se perde o que ja foi
        destino.write_text(json.dumps(resultados[-1], ensure_ascii=False, indent=2),
                           encoding="utf-8")

    relatorio(resultados, pulados, tot_in, tot_out)
    print(f"\ntokens: {tot_in} de entrada, {tot_out} de saida")
    print(f"relatorio -> {SAIDA / 'RELATORIO.md'}")


def relatorio(resultados, pulados, tot_in, tot_out):
    ordem = {"alta": 0, "media": 1, "baixa": 2}
    L = ["# Checagem pelo DeepSeek", "",
         "Segunda opiniao automatica. **Cada item abaixo é pista, não veredito** —",
         "o modelo erra, e parte do conteúdo foi expandido além da fonte de",
         "propósito (está declarado nos resumos).", "",
         f"{len(resultados)} material(is) checado(s) · {tot_in} tokens de entrada · "
         f"{tot_out} de saída", ""]

    if pulados:
        L += ["## Pulados", ""]
        L += [f"- **{t}** — {m}" for t, m in pulados] + [""]

    altas = [(r, x) for r in resultados for x in r.get("achados", [])
             if x.get("gravidade") == "alta"]
    if altas:
        L += ["## Gravidade alta — olhar primeiro", ""]
        for r, x in altas:
            L += [f"- **{r['tema']} · {x.get('onde','?')}** — {x.get('o_que','')}",
                  f"  - sugestão: {x.get('sugestao','—')}"]
            if x.get("na_fonte"):
                L.append(f"  - na fonte: \"{x['na_fonte'][:200]}\"")
        L.append("")

    L += ["## Por material", ""]
    for r in resultados:
        L.append(f"### {r['tema']}")
        if r.get("erro"):
            L += [f"Não foi checado: `{r['erro']}`", ""]
            continue
        L += [f"*{r.get('veredito','')}*", ""]
        if not r.get("achados"):
            L += ["Nenhum achado.", ""]
            continue
        for x in sorted(r["achados"], key=lambda y: ordem.get(y.get("gravidade"), 3)):
            L.append(f"- `{x.get('gravidade','?')}` **{x.get('tipo','?')}** em "
                     f"{x.get('onde','?')}: {x.get('o_que','')}")
            if x.get("na_fonte"):
                L.append(f"  - na fonte: \"{x['na_fonte'][:200]}\"")
            if x.get("sugestao"):
                L.append(f"  - sugestão: {x['sugestao']}")
        L.append("")
    (SAIDA / "RELATORIO.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
