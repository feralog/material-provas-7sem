# Checagem pelo DeepSeek

Segunda opiniao automatica. **Cada item abaixo é pista, não veredito** —
o modelo erra, e parte do conteúdo foi expandido além da fonte de
propósito (está declarado nos resumos).

42 material(is) checado(s) · 0 tokens de entrada · 0 de saída

## Pulados

- **parkinsonismo** — fonte protegida (esta no .gitignore)
- **transtorno_afetivo_bipolar** — fonte protegida (esta no .gitignore)

## Por material

### aga
*Material globalmente fiel à fonte: todos os cortes e classificações conferíveis (Katz, Lawton, MEEM de Brucki, relógio, fluência verbal, GDS-15, Cornell, MNA, perda de peso, caidor crônico) batem com o texto, e quiz e resumo não divergem entre si; restam apenas deslizes menores e uma contradição interna do próprio protocolo do Katz sobre comadre/papagaio.*

- `baixa` **fonte_suspeita** em resumo — tabela do Katz (item uso do vaso sanitário) e quiz Q7 (explicação): O próprio protocolo do Katz se contradiz sobre comadre/papagaio: a alternativa de independência admite comadre ou urinol à noite, mas o texto de instrução diz que quem usa papagaio/comadre é dependente. Quiz e resumo adotam apenas a segunda leitura.
  - na fonte: ""...pode utilizar comadre ou urinol à noite, esvaziando por si mesmo pela manhã). (I)" / "Aqueles que utilizam 'papagaios' ou 'comadres' também são considerados dependentes.""
  - sugestão: Explicitar a ambiguidade do instrumento: quem usa urinol/comadre à noite mas o esvazia sozinho é classificado como independente na descrição do item, e dependente na instrução geral. Não afirmar categoricamente que comadre = dependente.
- `baixa` **erro_factual** em quiz Q19 (explicação) e resumo — tabela de instrumentos de humor: Afirma que o PHQ-9 tem escore até 30 pontos; o PHQ-9 tem 9 itens de 0 a 3, portanto máximo de 27 pontos.
  - sugestão: Corrigir para 'escore de 0 a 27' no resumo e na explicação do quiz.
- `baixa` **erro_factual** em resumo — seção comunicação (Teste de Snellen): Diz que o Snellen é aplicado a '5-6 metros', mas a fonte registra 6 metros.
  - na fonte: ""Teste de Snellen: distância de 6 metros. A acuidade visual normal é considerada 20/20 (linha 8).""
  - sugestão: Padronizar para 6 metros.
- `baixa` **fora_da_fonte** em resumo — tabela de humor, linha 'Critérios do DSM-5': Atribui aos critérios do DSM-5 um escore '0 a 9' e chama isso de 'diagnóstico formal'; a fonte apenas menciona que se pode usar também os critérios do DSM-5, sem escala numérica.
  - na fonte: ""Escala GDS é a mais usada para rastreio de depressão, mas pode usar critérios do DMS-5 também.""
  - sugestão: Retirar a coluna de escore dessa linha (ou descrever os critérios sem atribuir pontuação de 0 a 9).

### delirium
*Material no geral fiel à fonte, com boa correspondência de números e critérios; os problemas se limitam a uma classificação farmacológica imprecisa no quiz, uma alternativa do CAM que também estaria tecnicamente correta e uma comparação de letalidade acrescentada pelo resumo.*

- `media` **erro_factual** em quiz Q12: A alternativa correta chama a ranitidina de anticolinérgica, mas a fonte atribui o risco pró-delirium dos antagonistas H2 ao bloqueio histaminérgico central (H1/H2), mecanismo distinto do anticolinérgico; a explicação repete o erro ao dizer que a ranitidina 'reduz a transmissão colinérgica'.
  - na fonte: "Antagonistas centrais de H1 e H2 têm potencial pró-delirium."
  - sugestão: Trocar o exemplo por um anticolinérgico clássico (a própria difenidramina citada no resumo) ou reescrever a alternativa como 'anticolinérgicos e antagonistas H2', separando os dois mecanismos.
- `media` **ambigua** em quiz Q16: A alternativa B ('início agudo e desatenção, ambos somados a torpor') descreve a combinação 1+2+4, que também fecha o diagnóstico pelo CAM; ela só é 'menos correta' por não enunciar a regra completa. Um aluno que raciocine pelo algoritmo pode escolhê-la com lógica.
  - sugestão: Reformular B para uma combinação realmente insuficiente, por exemplo 'desatenção e torpor, sem início agudo' ou 'início agudo e torpor, sem desatenção'.
- `baixa` **fora_da_fonte** em resumo, box da seção 'O que é delirium e por que ele importa': O resumo afirma letalidade 'comparável à do infarto agudo do miocárdio e da sepse' — comparação que a fonte não faz em nenhum ponto.
  - na fonte: "Mortalidade 22-76% nos pacientes hospitalizados / Mortalidade após um ano: 35-40%"
  - sugestão: Retirar a comparação ou substituí-la pelos números absolutos que a fonte traz.

### demencia
*Material globalmente fiel à fonte: doses, cortes do MoCA, prevalências, escala de Scheltens, critérios de demência/CCL/DCS e o manejo das demências não Alzheimer reproduzem o texto sem contradição; o que não é verificável vem quase todo de slides que existem apenas como figura.*

- `baixa` **possivelmente_na_imagem** em quiz Q5 e Q6; resumo, seção "Os três Ds": o perfil clínico do delirium (início agudo, curso flutuante, desatenção cardinal, alteração do nível de consciência) e o padrão da depressão ("queixa desproporcional ao déficit", responder "não sei") não estão no texto extraído; a fonte só cita delirium como critério de exclusão e como item a revisar
  - na fonte: "Este declínio não pode ser explicado por delirium ou transtorno psiquiátrico maior."
  - sugestão: confirmar esses pontos contra a figura da página correspondente (provável slide de diferencial entre os três quadros); se não houver figura com esse conteúdo, reduzir as explicações ao que a fonte sustenta
- `baixa` **possivelmente_na_imagem** em quiz Q27 e Q28; resumo, seção "O protocolo do Ministério da Saúde": critérios de inclusão do PCDT (início entre 40 e 90 anos, MEEM 8-21 para até 4 anos e 12-24 para 4 anos ou mais, CDR 1 ou 2) e o intervalo de 3 a 4 meses até a primeira reavaliação, com reavaliações a cada 6 meses, não constam do texto — o slide do protocolo é apenas fluxograma em imagem
  - na fonte: "Fluxograma de tratamento da DA do Protocolo Clínico e Diretrizes Terapêuticas do Ministério da Saúde"
  - sugestão: manter, desde que os números tenham sido conferidos no fluxograma; caso contrário, retirar MEEM/CDR e prazos das alternativas e da explicação
- `baixa` **possivelmente_na_imagem** em quiz Q33, Q34 e Q35; resumo, seções "Comportamento, cuidador e prevenção": a lista de BPSD que não respondem à medicação, o dado de até 50% de depressão entre cuidadores e a fração de 40% da prevalência atribuída a fatores modificáveis (com os pesos de 8% para perda auditiva e 7% para baixa escolaridade) não aparecem no texto extraído
  - na fonte: "Sobrecarga do cuidador / Como prevenir? 2 cópias do alelo E4 da ApoE >> risco 8-10x maior de DA"
  - sugestão: confirmar os números nas figuras das páginas 44, 45 e 60; se a figura não trouxer o valor exato, substituir por alternativa qualitativa

### depressao_no_idoso
*Material globalmente fiel à fonte, com boa correspondência entre quiz e resumo; os pontos a corrigir são o enunciado da Q1, que declara normais exames com achados descritos na fonte, e o teto de dose da desvenlafaxina no resumo.*

- `media` **erro_factual** em quiz Q1 (enunciado): O enunciado afirma que endoscopia e tomografia 'vieram normais', mas a fonte descreve achados na EDA (hérnia de hiato, esofagite leve, gastrite de antro) e na TC (aumento prostático, degeneração lombossacra). Além disso, o distrator B cita 'gastrite de antro', que o próprio enunciado declarou inexistente — inconsistência interna da questão.
  - na fonte: "EDA: hérnia de hiato, esofagite leve e gastrite enantemática leve de antro. / TC abdôme: discreto aumento prostático e alterações degenerativas de coluna lombossacra"
  - sugestão: Trocar 'vieram normais' por 'sem achado que explique a dor' e reformular o distrator B para que não remeta a um achado que o enunciado negou.
- `media` **erro_factual** em resumo (doses dos duais): O resumo fixa a desvenlafaxina em '50 mg/dia (máx. 100)', mas a tabela da fonte traz faixa e teto diferentes (50–400 mg, bula 200 mg). É a única dose do resumo que não fecha com o texto da fonte — pode ser leitura divergente do slide de primeira linha.
  - na fonte: "Doses 50-400mg (bula 200mg)"
  - sugestão: Conferir o slide de primeira linha (pg25/pg33) e alinhar o teto da desvenlafaxina ao valor da fonte, ou explicitar que se trata de dose usual e não de teto de bula.
- `baixa` **possivelmente_na_imagem** em quiz Q28 (bupropiona no tabagismo): A indicação de bupropiona como preferência no tabagismo associado, com dose 150–450 mg/dia, não aparece em nenhum trecho de texto da fonte; pode estar no slide de classes ou de mecanismos alternativos, que são só imagem.
  - sugestão: Se o slide de classes (pg41/pg34) não trouxer essa indicação, remover a questão ou marcá-la como conteúdo externo declarado.

### fragilidade_e_sarcopenia
*Quiz e resumo são fiéis à fonte nos conceitos, cortes, doses e classificações que o texto permite conferir, sem divergências entre si; as ressalvas são de verificação de figuras (SARC-CalF, teste da cadeira e diagnósticos diferenciais), não de conteúdo equivocado.*

- `baixa` **fonte_suspeita** em fonte pg12 (SARC-F) / quiz Q14: A fonte escreve "Se >10" logo abaixo do SARC-F, mas o escore do SARC-F vai de 0 a 10; o corte >10 (isto é, ≥11) só faz sentido para o SARC-CalF, que é justamente o valor usado no quiz.
  - na fonte: "SARC-F Identificar (não diagnosticar) indivíduos risco com aumentado para Sarcopenia Se >10"
  - sugestão: Conferir as figuras pg12/pg14 e, se o corte >10 pertencer ao SARC-CalF, deixar isso explícito, para não sugerir que o SARC-F pode pontuar acima de 10.
- `baixa` **possivelmente_na_imagem** em quiz Q19 (sentar e levantar 5 vezes): O ponto de corte "acima de 15 segundos" não aparece no texto extraído; a pg19 descreve apenas a técnica e a tentativa única.
  - na fonte: "Posição correta para o teste: Indivíduo sentado, com as costas apoiadas numa cadeira e os braços cruzados sobre o tronco... Considere uma única tentativa."
  - sugestão: Confirmar o corte na figura da pg19; se a figura trouxer outro valor, corrigir alternativa e explicação.
- `baixa` **possivelmente_na_imagem** em quiz Q17 (outras causas de força baixa): A lista de diagnósticos diferenciais da força reduzida (depressão, AVC, doença vascular periférica) não está no texto extraído da aula.
  - sugestão: Confirmar na figura da pg19/pg20 que esse diferencial é realmente apresentado na aula; caso contrário, retirar a questão.

### iatrogenia
*Material fiel à fonte e bem construído: as alternativas corretas reproduzem com precisão os números, classificações e casos da aula, sem erro factual relevante; restam apenas dois ajustes finos — um distrator defensável no caso clínico e um superlativo indevido no resumo.*

- `media` **ambigua** em quiz Q20: O distrator "diabetes de longa data descompensado, ainda sem diagnóstico formal" é defensável com os próprios dados do caso (HbGlic 11,7), mas a explicação o descarta apenas porque o paciente "negava diabetes" — negar não exclui, e a HbA1c elevada confirma diabetes não diagnosticada.
  - na fonte: "HbGlic:11,7 (exames de 3/4/18); "Negava: Etilismo / DM / Antecedente familiar de hipertrigliceridemia""
  - sugestão: Reescrever o distrator (por exemplo, "diabetes já conhecida e em tratamento regular") ou ajustar a explicação: admitir que a HbGlic 11,7 revela DM não diagnosticada, mas que ela não explica a magnitude de TG 12.468 nem a normalidade do exame do ano anterior.
- `baixa` **divergencia** em resumo — seção "Os quatro tipos de iatrogenia": O resumo afirma que a falha de comunicação é "a mais comum" entre os quatro tipos; o quiz (Q11) diz "uma das causas mais comuns", e a fonte também não a elege como a mais frequente.
  - na fonte: ""É uma das causas mais comuns e evitáveis de erros médicos." (slide "Iatrogenia por falha no processo de comunicação"); no material de origem consta apenas "É a mais evitável"."
  - sugestão: Trocar "a mais comum" por "uma das mais comuns", preservando "a mais evitável".

### polifarmacia
*Material fiel à fonte: a definição da OMS, os números (5/dia, 13-58-82%, 6,3 mL/min/década, 31,5%, 30-40%), as cinco listas de Beers, o MAI e o caso da Dona Esmeralda conferem com o texto; restam uma ambiguidade no quiz Q5, uma inversão de sentido na explicação do Q9 e um detalhe etário do resumo — apenas ajustar, sem retrabalho, a referência interna a 'o resumo' nos enunciados Q13 e Q17.*

- `media` **ambigua** em quiz Q5: O enunciado pede fatores 'ligados ao próprio paciente', mas a alternativa C (hepatopatia, doença renal crônica, ILPI) reproduz literalmente o bloco 'vulnerabilidade pessoal' da fonte, que também é um fator ligado ao paciente; só o gabarito desfaz a confusão ao dizer que C pertence a outro bloco.
  - na fonte: "Fatores contribuintes: paciente • Multimorbidades • Automedicação... • Fragmentação dos cuidados // Fatores contribuintes: vulnerabilidade pessoal • Idosos (> 65 anos)... • Renais crônicos • Hepatopat"
  - sugestão: Reescrever o enunciado como 'Entre os fatores do bloco assistencial/paciente (e não os de vulnerabilidade pessoal)...' ou trocar a alternativa C por itens claramente alheios (ex.: prescrição eletrônica, cascata iatrogênica).
- `baixa` **erro_factual** em quiz Q9 (explicação): A explicação afirma que a queda do fluxo esplâncnico 'reduz o efeito de primeira passagem, aumentando a biodisponibilidade', enquanto a fonte descreve o mesmo fenômeno como 'queda de absorção' de fármacos de primeira passagem; a direção do efeito está invertida entre os dois textos.
  - na fonte: "queda de absorção de nutrientes lipossolúveis (vitaminas A, D, E e K) e de medicamentos dependentes da primeira passagem pelo fígado, como o propranolol, em razão da redução do fluxo sanguíneo esplêni"
  - sugestão: Alinhar a explicação à redação da fonte ('redução da absorção de fármacos de primeira passagem, como o propranolol') ou explicitar que a fonte trata o efeito como redução de absorção/biodisponibilidade.
- `baixa` **possivelmente_na_imagem** em resumo · tabela de considerações do envelhecimento (linha Renal): O resumo afirma 'perda de tecido renal após os 50 anos'; o texto extraído só diz 'diminuição dos rins e da capacidade de ampliar a concentração das urinas', sem marco etário.
  - sugestão: Se a figura das considerações do envelhecimento não trouxer o corte de 50 anos, retirar a idade e manter apenas a perda de massa renal.

### sindrome_do_imobilismo
*Quiz e resumo são fiéis ao texto extraído, sem contradição entre si nem número divergente da fonte; as ressalvas são de baixa gravidade e se concentram em conteúdo que só existe nas figuras (que não pude ver) e na forma como a cifra de 1,5%/dia é rotulada.*

- `baixa` **fonte_suspeita** em quiz Q11 e resumo (tabela "O relógio das perdas", linha Muscular) frente a pg06 e pg29: A fonte atribui a perda de 1,5% ao dia à FORÇA em pg06 ("da total", logo após a queda de 20% de força em 6 semanas), mas em pg29 chama o mesmo dado de perda de MASSA muscular (1-2%/dia). O quiz e o resumo fixam a segunda leitura, e as duas não fecham entre si: 1,5%/dia equivaleria a ~60% em 6 semanas, e não aos 20% de queda descritos para o mesmo prazo.
  - na fonte: "Com 6 semanas a força dos MMII declina 20% e a dos MMSS 10%, alguns estudos mostram perda diária de até 1,5% da total, ou seja, 10% por semana / Sarcopenia catabólica (perda 1-2% massa muscular/dia)"
  - sugestão: Manter a cifra (é a que a fonte dá), mas apresentá-la como perda funcional de força/massa e deixar claro que os 10%/semana vêm de estudos isolados e não se somam linearmente até as 6 semanas — hoje o resumo e o quiz vendem 1,5%/dia como perda de massa estabelecida.
- `baixa` **ambigua** em quiz Q27 (domínios da escala de Braden): O enunciado pede os domínios pontuados "de 1 a 4" e a alternativa correta lista cinco; a explicação, porém, acrescenta fricção/cisalhamento e afirma que "cada item" vai de 1 a 4 — o que tornaria a própria alternativa correta incompleta.
  - sugestão: Harmonizar enunciado, alternativa e explicação: ou retirar fricção/cisalhamento da explicação, ou dizer expressamente que esse é um item com pontuação própria, distinta dos demais.
- `baixa` **possivelmente_na_imagem** em quiz Q15, Q20, Q21, Q22, Q23, Q26, Q27, Q28, Q29 e trechos do resumo (bloco metabólico, 90% gastrointestinal, líquido sinovial/pannus, alterações de pele, Braden, pontos de pressão, tabela de estadiamento de LPP e mudança de decúbito 2/2h): Esses conteúdos não aparecem no texto extraído: vêm de slides cujo corpo está vazio ou reduzido a um título (pg08, pg10, pg17, pg19, pg20, pg21, pg22). São exatamente o tipo de material que costuma existir só na figura — critérios, faixas de pontuação, tabelas de estadiamento e números fechados.
  - sugestão: Conferir cada uma dessas passagens contra as figuras originais antes da publicação; o que a figura não sustentar deve sair, sobretudo os números fechados (90% gastrointestinal, faixas <12/13-15/16-18/>19 da Braden, intervalo de 2/2h).

### diabetes_mellitus_gestacional
*Material fiel ao texto da fonte, sem erros factuais relevantes; as ressalvas são conteúdos provavelmente sustentados pelas figuras e a coexistência de metas glicêmicas diferentes dentro da própria fonte.*

- `baixa` **fonte_suspeita** em fonte pg46 × quiz Q12 e Q13 × resumo (tabela de metas): A própria fonte traz três conjuntos distintos de metas glicêmicas (pg46: antes 70-90 e 1 h após 70-120; pg61: jejum <95, 1 h <140, 2 h <120; pg64: 70-95 e 90-140), e quiz e resumo usam dois deles sem deixar claro o contexto de cada um.
  - na fonte: ""Antes: 70 - 90" / "1 hora após: 70 - 120" (pg46); "METAS: PRE-REFEIÇÕES 70-95 MG/DL E 1H APÓS 90-140 MG/DL" (pg64); "meta glicêmica jejum < 95, 1hpp<140 ou 2hpp<120" (pg61)"
  - sugestão: Explicitar em cada questão e no resumo qual conjunto corresponde ao ambulatório, qual à automonitorização e qual ao intraparto, ou padronizar um único conjunto.
- `baixa` **possivelmente_na_imagem** em quiz Q28: O perfil de ação da insulina asparte (início 5-15 min, pico 0,5-2 h, duração 3-5 h) e os tempos da regular e da NPH não aparecem no texto extraído; vêm de tabela.
  - na fonte: ""Tipos de insulina e principal efeito sobre o controle glicêmico" (pg50)"
  - sugestão: Confirmar os valores na figura da pg50 antes de publicar.
- `baixa` **possivelmente_na_imagem** em quiz Q25 e resumo (malformações): Síndrome de regressão caudal como marcadora, anencefalia e transposição das grandes artérias não constam do texto extraído.
  - na fonte: ""Malformações fetais associadas ao Diabetes / Incidência 3 vezes maior do que na população geral / Fator etiológico responsável : mau controle glicêmico entre 6-8 semanas" (pg32)"
  - sugestão: Conferir a lista de malformações na figura da pg32.
- `baixa` **possivelmente_na_imagem** em quiz Q35 e resumo (tabela de reclassificação pós-parto): Os cortes usados para classificar o TOTG pós-parto (jejum 100-125 com 2 h <140 = glicemia de jejum alterada; 2 h 140-199 = intolerância) não estão no texto extraído.
  - na fonte: ""Repetir GTTO 75g 6-12 sem após o parto. Se GTTO normal – seguimento com retestagem glicêmica em 1-3 anos... Se alterado – tratamento/acompanhamento endocrinológico" (pg62)"
  - sugestão: Confirmar os cortes nos fluxogramas das páginas 29 e 30.

### distopia_genital
*Material no geral fiel à fonte, com números, doses, cortes e classificações convergentes entre quiz e resumo; o único reparo relevante é a inclusão da fáscia endopélvica entre os "cabos" da suspensão em uma questão.*

- `media` **divergencia** em quiz Q10: A alternativa correta coloca as fáscias junto aos ligamentos como os "cabos sob tensão" (suspensão), enquanto a fonte e o próprio resumo classificam a fáscia endopélvica no aparelho de SUSTENTAÇÃO, junto ao elevador do ânus; só os ligamentos compõem a suspensão.
  - na fonte: "Aparelho de sustentação - Músculo elevador do ânus - Fáscia endopélvica / Aparelho de suspensão - Ligamentos (slide 24). No resumo: "Sustentação — os pilares ... A esse conjunto soma-se a fáscia endop"
  - sugestão: Conferir a figura s22i1; se a analogia da figura não puser a fáscia entre os cabos, trocar a alternativa correta para "Os ligamentos pélvicos" (deixando a fáscia como distratora do lado da musculatura) e manter quiz e resumo com a mesma classificação.

### doenca_inflamatoria_pelvica
*Material globalmente fiel à fonte: doses, esquemas do PCDT 2020, estadiamento de Monif, critérios diagnósticos e números de sequelas conferem; os problemas são pontuais e de baixa gravidade (uma explicação de quiz mal redigida e um prazo de seguimento inconsistente no resumo).*

- `baixa` **erro_factual** em quiz Q25 (explicação): A explicação afirma que 'a alternativa troca a ceftriaxona por cefotaxima 500 mg IM', mas nenhuma das alternativas traz cefotaxima: a errada (B) mantém a ceftriaxona e troca doxiciclina/metronidazol por azitromicina/fluconazol; a D troca por penicilina e encurta para 7 dias.
  - na fonte: "AMBULATORIAL • Ceftriaxona 500 mg IM (dose única) MAIS Doxiciclina 100 mg VO de 12/12h (14 dias) MAIS Metronidazol 250 mg (2 comp = 500 mg) VO de 12/12h (14 dias) / SEGUNDA OPÇÃO: Cefotaxima 500 mg IM"
  - sugestão: Corrigir a explicação para apontar o desvio real da alternativa errada (troca de doxiciclina/metronidazol por azitromicina/fluconazol) e reservar a cefotaxima para a menção à segunda opção do PCDT.
- `baixa` **divergencia** em resumo — seção Tratamento antimicrobiano (seguimento): O resumo manda reavaliar em 72 h, mas depois afirma que 'o seguimento ambulatorial é feito na primeira semana', prazo que o quiz e a fonte não sustentam.
  - na fonte: "Reavalie pacientes ambulatoriais em 72h. Orienta-se abstinência sexual por 30 dias"
  - sugestão: Padronizar o prazo de reavaliação em 72 horas e retirar (ou qualificar) a menção a 'primeira semana'.
- `baixa` **fonte_suspeita** em fonte pg21 vs pg22 (Monif II): A própria fonte diverge sobre a conduta no estágio II: a tabela da pg21 diz 'Individualizar / frequentemente hospitalar', enquanto a pg22 crava 'INTERNAÇÃO HOSPITALAR'.
  - na fonte: "II Endometrite/salpingite Com peritonite Individualizar / frequentemente hospitalar | ESTÁGIO II (MONIF II) Conduta Indicada: INTERNAÇÃO HOSPITALAR"
  - sugestão: Manter a redação do quiz/resumo como 'habitualmente hospitalar' (como já faz a explicação de Q20) e, se possível, sinalizar a divergência ao autor da fonte.

### endometriose_e_algia_pelvica
*Material globalmente fiel à fonte: definições, números, classificações ASRM e conduta batem com o texto; o ajuste necessário é a frase do resumo que exclui a dor leve da definição de dor pélvica crônica, além de sinalizar o que vem só de imagem (AAGL) e o que é expansão clínica (ressalvas terapêuticas).*

- `media` **divergencia** em resumo — bloco "Dor pélvica crônica: o que é, quanto dói e quanto pesa" (frase final) × quiz Q3: O resumo afirma que "dor que incomoda mas não muda a vida da mulher não entra nessa definição", mas o próprio quiz (Q3) trata essa dor como DPC leve, e a fonte a classifica como grau leve da síndrome.
  - na fonte: "Leve: • Incomoda mas não deixa de fazer suas atividades"
  - sugestão: Reescrever: o critério de intensidade da definição admite a dor leve — a graduação leve/moderada/grave é feita por critério funcional, e a dor que só incomoda é DPC leve, não ausência de DPC.
- `baixa` **possivelmente_na_imagem** em quiz Q22 e resumo (seção "Classificações: ASRM e AAGL 2021"): Os cortes da AAGL 2021 (estágio 1 até 8, 2 de 9–15, 3 de 16–21, 4 acima de 21) e a lista de sítios pontuados não aparecem no texto extraído; dependem inteiramente da figura pg40.
  - sugestão: Conferir a tabela na imagem pg40; se ela não trouxer esses cortes, retirar a questão ou marcá-la como complemento externo à aula.
- `baixa` **fora_da_fonte** em resumo — tabela de tratamento (colunas "Quando indicar" e "Ressalva"): Ressalvas como contraindicação do ACO por risco tromboembólico, sangramento de escape, hipoestrogenismo com perda de massa óssea, GnRH como preparo pré-operatório e risco de lesão ureteral/redução de reserva ovariana não constam da fonte, que apenas lista as opções.
  - na fonte: "Clínico • Anti-inflamatório/Analgésicos • ACOH • Progesteronas • Análogo de GnRH • Anti-aromatase Cirúrgico • Exérese • Reconstituição da Anatomia • Histerectomia / Ooforectomia"
  - sugestão: Sinalizar essas colunas como complemento clínico (não da aula) ou reduzi-las ao que a fonte sustenta.

### incontinencia_urinaria
*O quiz está fiel à fonte na quase totalidade dos itens (definições, números de cura, doses e classificações conferem); o problema real é o resumo, que troca para T10–L2 a origem do simpático que a fonte situa em T11–L2/T12–L2 — inconsistência que, aliás, já existe entre dois slides da própria fonte.*

- `baixa` **fonte_suspeita** em fonte — páginas 7 e 8: A própria fonte diverge sobre o nível de origem do simpático: T11–L2 na página 7 e T12–L2 na página 8.
  - na fonte: "ARMAZENAMENTO —SN SIMPÁTICO (T11–L2) … N. HIPOGÁSTRICO Simpático—T12–L2"
  - sugestão: Adotar um dos valores de forma consistente nos materiais derivados e, se possível, conferir o slide original.
- `baixa` **possivelmente_na_imagem** em resumo — seção 'Controle central': Afirmações anatômicas específicas — centro pontino na 'substância reticular pontomesencefálica', aferências do sistema límbico e do cerebelo, córtex com 'corpo caloso' e a frase de que 'todos os estímulos aferentes e eferentes passam por ali' — não aparecem no texto extraído; se não estiverem nas figuras (pg05/pg09/pg24), devem ser revistas.
  - na fonte: "Centro pontino coordena o reflexo miccional … SNC pode inibir ou iniciar voluntariamente … A região frontal direita exerce ação inibitória sobre o reflexo da micção"
  - sugestão: Conferir as figuras citadas e, na dúvida, reduzir a formulação ao que a fonte sustenta (centro pontino coordena o reflexo; córtex inibe ou inicia voluntariamente).
- `média` **erro_factual** em resumo — seção 'Neurofisiologia' (título 'Armazenamento — simpático' e tabela de nervos): O resumo situa a origem do simpático vesical em T10–L2, duas vezes; a fonte diz T11–L2 e, em outro slide, T12–L2. Nenhum trecho da fonte traz T10.
  - na fonte: "ANATOMIA DA BEXIGA E URETRA PROXIMAL ⟳ ARMAZENAMENTO —SN SIMPÁTICO (T11–L2) … N. HIPOGÁSTRICO Simpático—T12–L2"
  - sugestão: Padronizar com a fonte (T11–L2) ou registrar explicitamente a variação T11–L2/T12–L2 apresentada nos dois slides; retirar T10–L2.

### sindromes_hipertensivas_na_gestacao
*O material é majoritariamente fiel à fonte, mas o quiz tem uma contradição relevante sobre corticoterapia no HELLP e uma imprecisão numérica; a fonte ainda apresenta divergência interna no corte da fita de proteinúria.*

- `media` **erro_factual** em quiz Q24: A alternativa correta afirma que o parto nunca é adiado pela corticoterapia, mas a fonte admite excepcionalmente retardar o parto em 48 h em paciente estável entre 23 e 34 semanas.
  - na fonte: "Excepcionalmente retardar o parto em 48h, para corticoterapia antenatal, entre 23-34 semanas, em pacientes estáveis, pode ser recomendado"
  - sugestão: Reescrever a alternativa para refletir a exceção: a corticoterapia não posterga o parto em situação materna grave, mas pode adiar 48 h se a paciente estiver estável entre 23 e 34 semanas.
- `media` **fonte_suspeita** em fonte, páginas 35 e 89: A fonte diverge sobre o critério de proteinúria por fita: em uma página exige 2+ e em outra aceita 1+ em amostra isolada; o resumo adota 2+ sem sinalizar a divergência.
  - na fonte: ""fita ≥ 2+ (se indisponível)" (pg35) e "≥ 1+ em amostra isolada" (pg89)"
  - sugestão: Padronizar o critério na fonte e, no resumo, registrar a divergência ou indicar qual página prevalece.
- `baixa` **erro_factual** em quiz Q7: A alternativa correta diz 'cerca de 25%', enquanto a fonte diz 'até 25%', que é um limite superior e não uma estimativa central.
  - na fonte: "até 25% dessas gestantes apresentarão sinais e/ou sintomas relacionados à pré-eclâmpsia"
  - sugestão: Trocar 'Cerca de 25%' por 'Até 25%'.

### alzheimer_e_demencias
*Material globalmente fiel ao texto da fonte no conceito, epidemiologia, rastreio, classificação, subtipos e tratamento; o desvio relevante é a ampliação sobre demência com corpos de Lewy (cinco questões e uma seção do resumo), clinicamente correta mas não verificável no capítulo.*

- `baixa` **fora_da_fonte** em quiz Q40 a Q44 (e, no resumo, a seção "Corpos de Lewy em detalhe" e a tabela de cronologia): Bloco inteiro de critérios da demência com corpos de Lewy que o capítulo não traz: diagnóstico definitivo só por tecido cerebral com inclusões de alfa-sinucleína (possível/provável em vida), memória normal no início com rendimento visuoespacial como domínio mais informativo, alucinações bem formadas contrapostas aos "vultos" do Alzheimer, regra do intervalo de um ano entre cognição e parkinsonismo, parkinsonismo-plus com lentidão sobre tremor e resposta apenas parcial à levodopa.
  - na fonte: ""Na demência com inclusão dos corpos de Lewy ocorrem flutuações dos déficits cognitivos, por vezes chegando a verdadeiros quadros de delirium, além de parkinsonismo (usualmente, síndromes rígido-aciné"
  - sugestão: O conteúdo é clinicamente correto, mas não é sustentado pela fonte e não corresponde a nenhuma figura do capítulo (as imagens são tabelas de prevalência/exames/drogas, o fluxograma de classificação e as neuroimagens). Ou reduzir essas cinco questões ao que o texto afirma (flutuação, parkinsonismo simétrico, alucinações visuais, hipersensibilidade a neurolépticos, resposta aos anticolinesterásicos), ou declarar explicitamente que o material foi ampliado além da fonte.
- `baixa` **fora_da_fonte** em resumo, seção "Demência vascular": O resumo afirma que a demência vascular é "a única forma passível de prevenção primária e secundária"; a fonte diz apenas que ela é uma forma passível de prevenção, sem excluir outras.
  - na fonte: ""Por ser condição secundária a acometimento cerebrovascular, a DV é forma de demência passível de prevenção, primária e secundária.""
  - sugestão: Retirar o "única" e escrever "é forma de demência passível de prevenção primária e secundária".

### miastenia_gravis_e_guillain_barre
*Quiz e resumo são internamente consistentes entre si e com os números repetidos (15/85%, 85% de anti-AChR, AIDP 90%, IVIG 2 g/kg em 5 dias), mas a fonte disponível é composta apenas de imagens sem texto, o que impede qualquer conferência factual contra os slides; o único reparo possível é a comparação conceitualmente imprecisa entre prevalência da miastenia e incidência do Guillain-Barré.*

- `baixa` **erro_factual** em quiz Q5 (explicação) e resumo, seção "A junção neuromuscular": Compara a prevalência da miastenia (20–30/100.000) com a incidência anual do Guillain-Barré (1–2/100.000 por ano) como se fossem grandezas equivalentes, e conclui que a miastenia é "dez a vinte vezes mais prevalente"; são medidas diferentes (estoque vs. casos novos por ano) e a razão apresentada não tem esse sentido dimensional.
  - sugestão: Explicitar que se trata de ordens de grandeza distintas (prevalência vs. incidência anual) ou comparar prevalência com prevalência; no resumo, trocar "dez a vinte vezes mais prevalente" por uma formulação que não misture as duas medidas.

### alteracoes_palpebrais
*Material globally fiel à fonte: não há contradição factual, número ou classificação divergente entre quiz, resumo e slides; os pontos apontados são conteúdo provavelmente contido nas figuras ou pequenas expansões didáticas de baixo risco.*

- `baixa` **possivelmente_na_imagem** em quiz Q4, Q5 e resumo (tabela de lamelas e de músculos): A divisão da pálpebra em lamela anterior (pele + orbicular) e posterior (tarso + conjuntiva tarsal) e o músculo de Müller (2 mm, inervação simpática) não aparecem no texto extraído; só podem vir dos esquemas dos slides 2 e 3.
  - sugestão: Confirmar nas figuras s02i1/s02i2 e s03i1/s03i2 se lamela e Müller estão realmente representados; se não estiverem, suavizar a cobrança desses itens ou marcá-los como complemento.
- `baixa` **possivelmente_na_imagem** em quiz Q16 e resumo (ptose): A medida objetiva da ptose pela distância margem-reflexo (normal 4 a 5 mm) e a excursão do levantador não constam do texto extraído.
  - sugestão: Verificar se a figura do slide 18 traz a técnica de medida; caso contrário, manter como complemento declarado.
- `baixa` **fora_da_fonte** em resumo — tumores benignos (verruga vulgar e xantelasma): O resumo atribui origem viral (HPV) à verruga vulgar e associação com dislipidemia ao xantelasma; a fonte apenas lista os diagnósticos, sem etiologia nem correlação sistêmica.
  - na fonte: "Verruga vulgar / XANTELASMA"
  - sugestão: Manter as associações, mas apresentá-las como acréscimo didático, não como conteúdo da aula.

### ambliopia
*Material fiel e bem alinhado à fonte — nenhum erro factual, dose ou classificação divergente; os únicos pontos são a sobreposição numérica herdada da própria fonte (2 linhas) e duas afirmações de baixo risco que vão além do texto extraído.*

- `baixa` **fonte_suspeita** em quiz Q18 e Q19 (e resumo, seção 'Diagnóstico e graus'): A fonte dá dois cortes que se sobrepõem: o critério diagnóstico é 'diferença maior que 2 linhas', mas a classificação leve é '2 a 3 linhas' — ou seja, uma diferença de exatamente 2 linhas seria simultaneamente ambliopia leve e não-ambliopia. Quiz e resumo reproduzem os dois números sem notar a tensão.
  - na fonte: "'(diferença de AV entre AO maior que 2 linhas)' (slide 17) e 'Ambliopia leve: diferença de 2 a 3 linhas de visão' (slide 18)"
  - sugestão: Manter os dois dados, mas explicitar a leitura adotada (por exemplo: 'o corte é acima de 2 linhas; a faixa leve vai de pouco mais de 2 até 3 linhas') para que o aluno não fique com duas regras conflitantes.
- `baixa` **possivelmente_na_imagem** em quiz Q28: O mecanismo atribuído ao nistagmo (oscilação impedindo fixação foveal estável) e a afirmação de que a perda é habitualmente bilateral não aparecem no texto; o slide 16 traz apenas o título, sem corpo de texto e sem marcador de imagem.
  - na fonte: "'Ambliopia POR NISTAGMO' (slide 16, único conteúdo extraído)"
  - sugestão: Se a explicação veio de outra fonte, sinalizar; caso contrário, manter, pois é inferência clinicamente trivial a partir do próprio nome da forma — mas não é sustentada pelo material extraído.
- `baixa` **fora_da_fonte** em resumo, seção 'Por que a triagem precoce decide o desfecho': O resumo afirma que a ambliopia é 'a principal causa evitável de baixa visão monocular na infância' — dado epidemiológico que não aparece em nenhum ponto da fonte.
  - sugestão: Retirar o superlativo ou reformular como 'uma das principais causas evitáveis', deixando claro que é acréscimo externo ao material.

### ametropias
*Material fiel e bem alinhado à fonte: os erros de maior gravidade estão ausentes, restando um provável erro de digitação na própria fonte (eixo 'próximo de 30°'), uma atribuição imprecisa das 40 dioptrias no slide 2 e pequenos acréscimos que só podem vir das figuras.*

- `baixa` **fonte_suspeita** em fonte, slide 19 (Astigmatismo — a favor da regra): O texto diz que, no astigmatismo a favor da regra, o eixo negativo fica a 180° 'ou próximo de 30°', o que se contradiz com a própria definição seguinte e com o padrão real (eixo próximo de 180°).
  - na fonte: "A Favor da Regra - Quando o eixo negativo está a 180° ou próximo de 30°. Quando a curva vertical da córnea é mais acentuada do que a horizontal."
  - sugestão: Tratar o '30°' como erro de digitação (o correto é próximo de 180°). Quiz e resumo já adotaram 180°, então nada precisa mudar neles; só vale não memorizar o '30°'.
- `baixa` **fonte_suspeita** em fonte, slide 2 (Óptica e o olho) x quiz Q5: A fonte atribui as 40 dioptrias ao humor aquoso e descreve a córnea apenas como quem 'molda o humor aquoso'; o quiz atribui as 40 dioptrias à córnea. A leitura do quiz é a fisiologicamente correta, mas não é literalmente o que o slide escreve.
  - na fonte: "Córnea: molda o humor aquoso / Humor Aquoso => 40di / Cristalino : índice de refração variável => 19di"
  - sugestão: Manter o quiz como está (a explicação já diz 'a córnea, com o humor aquoso que a acompanha'), mas registrar que o slide isola mal o valor; o texto extraído parece ter perdido a linha de ligação entre córnea e 40 di.
- `baixa` **divergencia** em resumo, seção 'As quatro ametropias lado a lado' x quiz Q2: O resumo define ametropia como abrangendo apenas miopia, hipermetropia e astigmatismo (e diz que a presbiopia não é erro do comprimento do olho), mas depois intitula a tabela comparativa 'As quatro ametropias' incluindo a presbiopia — o quiz segue a definição de três.
  - na fonte: "Ametropia: os raios de luz paralelos não chegam focados na retina. / ERROS DE REFRAÇÃO - Hipermetropia - Miopia - Astigmatismo - Presbiopia"
  - sugestão: Uniformizar: ou trocar o título da tabela para 'Os quatro erros de refração', ou acrescentar uma nota de que a presbiopia entra no rol didático da aula embora não seja ametropia no sentido estrito.
- `baixa` **possivelmente_na_imagem** em quiz Q12 (cicloplegia): Os fármacos ciclopentolato e tropicamida não aparecem em nenhum ponto do texto extraído; só o termo 'após dilatação' aparece, no exemplo do slide 11.
  - na fonte: "Após dilatação: refração com +5,00 DE"
  - sugestão: Nenhuma mudança necessária se os nomes constarem de figura do slide 11; caso contrário, manter por ser conteúdo de rotina, mas ciente de que é expansão além do texto.
- `baixa` **possivelmente_na_imagem** em quiz Q25 e resumo (leitura da receita): O conceito de 'adição' (valor positivo somado ao grau de longe) e a categoria 'astigmatismo oblíquo' não estão no texto extraído: o slide 24 só lista DE, DC e os sinais, e o slide 18 lista apenas regular/irregular, simétrico/assimétrico e a favor/contra a regra.
  - na fonte: "Receita: Dioptrias Esféricas (DE) / Dioptrias Cilíndricas (DC) / Miopia : - / Hipermetropia: + / Astigmatismo: - ou +  ||  Regular ou irregular / Simétrico ou assimétrico / A favor da regra ou contra "
  - sugestão: Presumivelmente vêm das figuras s24i1 e s18i1/s18i2; se não vierem, marcar como acréscimo declarado do material, sem prejuízo ao estudo.

### catarata
*Material bastante fiel: nenhuma contradição factual com o texto da fonte, definição, prevalência, quadro clínico, tipos, conduta cirúrgica e complicações conferem; restam apenas duas ou três afirmações que provavelmente vêm das figuras e uma possível troca de chave de imagem no resumo.*

- `baixa` **divergencia** em resumo, seção "Cortical" (e quiz Q5): o resumo ilustra a catarata cortical com a chave img:s02i1, que pertence ao slide 2 (anatomia do cristalino), enquanto o quiz atribui o mesmo achado (opacidades em cunha radiais) à chave s09i1; uma das duas referências está trocada
  - na fonte: "### Slide 2

CRISTALINO

<!-- IMG:s02i1 -->"
  - sugestão: conferir no arquivo de imagens qual chave mostra as cunhas corticais e corrigir a legenda do resumo
- `baixa` **possivelmente_na_imagem** em quiz Q28: a questão e a explicação atribuem ao diabetes a via do sorbitol no cristalino, mas o texto da fonte não cita diabetes em nenhum ponto — a lista de causas sistêmicas nomeia apenas galactosemia, rubéola congênita e as trissomias
  - na fonte: "CAUSAS:
 - ENVELHECIMENTO
 - TRAUMA
 - DOENÇAS SISTÊMICAS
 - (Galactosemia, rubéola congênita, sínd Down / Patau / Edwards / Turner)"
  - sugestão: se o diabetes e o mecanismo do sorbitol estiverem em figura da página 4, manter; caso contrário, sinalizar como conteúdo de outra fonte
- `baixa` **possivelmente_na_imagem** em quiz Q7: a forma morfológica induzida pelo corticoide (subcapsular posterior) não aparece no texto extraído; o slide apenas lista "Corticoides" entre os fármacos, sem dizer qual tipo de catarata produzem
  - na fonte: "Principais remédios que podem causar a catarata medicamentosa
- Corticoides"
  - sugestão: confirmar na figura da página 5 antes de manter a afirmação como se estivesse no texto

### doencas_da_cornea
*Material fiel: quiz e resumo coincidem entre si e com o texto dos slides, sem erros factuais ou ambiguidades relevantes; apenas dois pequenos acréscimos superlativos no resumo que a fonte não sustenta.*

- `baixa` **fora_da_fonte** em resumo — seção Distrofias corneanas, subitem Epiteliais: Atribui à distrofia de Cogan o superlativo 'a mais comum' entre as distrofias epiteliais; a fonte lista apenas os nomes, sem qualquer dado de frequência.
  - na fonte: "DISTROFIA DE COGAN (slide 18, sem informação de prevalência)"
  - sugestão: Retirar 'a mais comum' ou confirmar a informação em outra referência antes de mantê-la.
- `baixa` **fora_da_fonte** em resumo — abertura, 'A córnea normal e por que ela é transparente': Afirma que a córnea é 'o maior tecido avascular do corpo', hierarquia de tamanho que a fonte não estabelece.
  - na fonte: "AUSÊNCIA DE VASCULARIZAÇÃO (slide 2)"
  - sugestão: Trocar por 'tecido avascular' sem o superlativo de tamanho.

### estrabismo
*Material muito fiel à fonte: as definições, os números (6 meses, 35Δ, 30–35Δ, 1–3 anos, 2–4 anos, 5 anos, 6 meses/15 dias) e as classificações conferem com os slides, sem erro factual relevante; os poucos pontos sinalizados são de baixa gravidade e provavelmente sustentados por figuras não visíveis.*

- `baixa` **possivelmente_na_imagem** em quiz Q6: O pseudoestrabismo por epicanto amplo com reflexos centrados e cover-test negativo não aparece no texto extraído; o raciocínio diagnóstico e a conduta de apenas acompanhar não estão na fonte textual.
  - sugestão: Conferir se a figura da página de propedêutica (observação desarmada/identificação do paciente) traz o pseudoestrabismo; se não trouxer, manter como conteúdo complementar declarado.
- `baixa` **possivelmente_na_imagem** em quiz Q22: A origem do nervo abducente na ponte, o trajeto intracraniano e a passagem pela fissura orbitária superior não constam do texto; só seriam sustentados por figura do trajeto do VI nervo.
  - sugestão: Checar a figura do trajeto do VI nervo (s33i1/s35i*); se ela não mostrar a origem e o trajeto, reduzir a assertiva da explicação.
- `baixa` **fonte_suspeita** em fonte, slide 40 (repercutido no quiz Q26 e Q27): A fonte afirma ao mesmo tempo que a paralisia completa do III preserva o reto lateral e o oblíquo superior e que há 'ausência de movimentos verticais' — se o oblíquo superior funciona, algum movimento vertical (e a intorção) deveria existir.
  - na fonte: "Completa => pior prognostico (preserva o RL e OS) ... Ausência de mov. verticais ... Intorção"
  - sugestão: Manter o quiz fiel à fonte, mas registrar na explicação que a motilidade vertical é mínima/gravemente reduzida, e não nula, para não gerar contradição interna.

### glaucoma
*Quiz e resumo são fiéis à fonte — nenhuma dose, corte, percentual ou classificação diverge do texto —, restando apenas pontos de baixa gravidade que dependem de conferir as figuras (sobretudo o esquema de tratamento da crise aguda e a tabela de achados do disco).*

- `baixa` **possivelmente_na_imagem** em resumo — seção 'Crise aguda de ângulo fechado': Afirma que o tratamento clínico 'resolve cerca de 90% dos casos nas primeiras 12 a 24 horas' — percentual e janela temporal que não aparecem em nenhum texto da fonte.
  - na fonte: "GLAUCOMA AGUDO: TRATAMENTO CLINICO (slide 10, sem texto — todo o conteúdo está na imagem)"
  - sugestão: Conferir o dado na imagem do slide 10; se não estiver lá, retirar o percentual e as horas.
- `baixa` **possivelmente_na_imagem** em resumo — tabela 'Achado no disco / Interpretação': Chanfradura (notching) do anel neural, hemorragia de borda do disco e fosseta adquirida são descritos com interpretação e prognóstico, mas nada disso consta do texto extraído.
  - na fonte: "ESCAVAÇÃO FISIOLOGICA : 0,1 A 0,5"
  - sugestão: Confirmar nas imagens de disco/OCT (s06i1, s08i1, s09i1) antes de manter; se não estiverem lá, marcar como complemento externo.
- `baixa` **divergencia** em quiz Q3 vs. resumo (tabela do disco) e vs. o próprio comentário do Q3: O Q3 define a relação escavação/disco fisiológica como '0,1 a 0,5, sem assimetria entre os dois olhos', mas o comentário da mesma questão e o resumo aceitam assimetria de até 0,2 como não patológica.
  - na fonte: "ESCAVAÇÃO FISIOLOGICA : 0,1 A 0,5"
  - sugestão: Reescrever a alternativa para 'assimetria menor que 0,2 entre os olhos', alinhando-a ao critério usado no resto do material.
- `baixa` **ambigua** em quiz Q11: A alternativa correta diz 'ilha central de visão preservada, com perda de todo o resto', mas o comentário da própria questão admite 'crescente temporal poupado' — ou seja, não se perde todo o resto.
  - na fonte: "DEFEITO DE CAMPO VISUAL: CAMPO TUBULAR"
  - sugestão: Ajustar para 'perda de toda a periferia, podendo restar um crescente temporal'.

### inflamacoes_da_via_lacrimal
*Material globalmente fiel à fonte: as 28 questões e o resumo reproduzem sem contradições os pontos da aula (agentes, quadro clínico, tratamento e cirurgia de cada nível de obstrução); o único reparo é a lateralidade atribuída à obstrução congênita, que a fonte não menciona.*

- `baixa` **fora_da_fonte** em quiz Q23: A alternativa correta acrescenta 'em geral unilateral' ao quadro da obstrução congênita da via lacrimal — dado de lateralidade que a fonte não traz (ela só marca unilateralidade para dacriocistite e canaliculite) e que pode induzir o aluno a excluir a forma bilateral.
  - na fonte: "QC: epífora, secreção e crostas nos cílios"
  - sugestão: Retirar o qualificador de lateralidade da alternativa (ou trocá-lo por 'unilateral ou bilateral'), deixando a distinção recair sobre epífora/secreção/crostas com olho calmo.

### olho_vermelho
*Material fiel à fonte: doses, incubações, prazos, agentes e classificações conferem com o texto dos slides; os únicos pontos de atenção são uma inconsistência interna sobre o padrão de hiperemia no glaucoma agudo e conteúdos que só podem existir em figuras não extraídas.*

- `baixa` **divergencia** em quiz Q30 (explicação) x resumo (tabela mestra): O quiz afirma que a hiperemia ciliar/pericorneana é típica do glaucoma agudo, mas a tabela mestra do resumo classifica a injeção conjuntival do glaucoma agudo como 'difusa', em contraste com a uveíte ('principalmente pericorneana').
  - na fonte: "DIAGNÓTICO DIFERENCIAL DE OLHO VERMELHO (slide 40, sem texto além do título; padrão de injeção não descrito no texto extraído)"
  - sugestão: Uniformizar: indicar no resumo que o glaucoma agudo também cursa com hiperemia ciliar/pericorneana, ou retirar 'glaucoma agudo' da explicação do quiz sobre injeção pericorneana.
- `baixa` **possivelmente_na_imagem** em quiz Q31 e Q32; resumo (tabela mestra e caixa de sinais de alarme): Todo o bloco de glaucoma agudo (córnea embaçada, midríase média fixa, pressão intraocular elevada) não aparece em nenhum trecho do texto extraído da fonte, que não menciona glaucoma em nenhum slide.
  - sugestão: Confirmar se a tabela de diferencial do olho vermelho existe como imagem (provavelmente no slide 40, que não traz marcador de imagem). Se não existir, sinalizar o glaucoma agudo como conteúdo complementar declarado.
- `baixa` **fonte_suspeita** em fonte, slide 25: O slide da ceratoconjuntivite papilar gigante traz a anotação 'PAPILAS FINAS', contradizendo o próprio nome do quadro e o slide 24, que descreve papilas gigantes na forma vernal; parece erro de cópia do slide da ceratoconjuntivite atópica.
  - na fonte: "CERATOCONJUNITITE PAPILAR GIGANTE ... PAPILAS FINAS"
  - sugestão: Corrigir a anotação na fonte. O quiz e o resumo não replicam o erro (o resumo diz apenas 'papilas na conjuntiva tarsal'), o que está adequado.

### retinopatia_diabetica
*Material fiel e consistente nos pontos que o texto extraído cobre (epidemiologia, fisiopatologia, classificação, fatores de risco, encaminhamento e prognóstico); as eventuais extrapolações concentram-se em rastreamento e detalhes terapêuticos que provavelmente estão nas figuras, além de um pequeno desalinhamento de urgência na tabela do resumo.*

- `baixa` **possivelmente_na_imagem** em quiz Q26, Q27 e Q28; resumo (tabela "Rastreamento e encaminhamento"): Todo o calendário de rastreamento (5 anos após diagnóstico no tipo 1 a partir da puberdade; no diagnóstico no tipo 2; trimestral na gestante com diabetes prévio) não aparece em nenhum trecho de texto da fonte — só a menção genérica de que rastreamento regular é essencial.
  - na fonte: "Rastreamento regular é essencial, pois a doença pode ser assintomática mesmo em estágios avançados"
  - sugestão: Se o cronograma estiver em imagem (s35i1/s43i1), manter; caso contrário, sinalizar no material que esse ponto é complementar à aula.
- `baixa` **possivelmente_na_imagem** em quiz Q18, Q19, Q30 e Q31; resumo (seção "Tratamento e prognóstico"): A fonte lista apenas as quatro modalidades terapêuticas, sem dizer que anti-VEGF é primeira linha no edema macular central, que corticosteroide fica para casos refratários/pseudofácicos nem que a OCT é o exame de escolha para quantificar o edema.
  - na fonte: "OPÇÕES TERAPÊUTICAS - AGENTES ANTI-VEGF (Injeções Intravítreas) - FOTOCOAGULAÇÃO A LASER - CORTICOSTEROIDES INTRAVÍTREOS - VITRECTOMIA"
  - sugestão: Confirmar se as indicações por primeira linha estão nas figuras de tratamento/prognóstico; se não, marcar como conteúdo complementar.
- `baixa` **possivelmente_na_imagem** em quiz Q4, Q14 e Q15 (e subtítulo do quiz): Perda de pericitos como evento inicial, definição da mancha algodonosa como microinfarto da camada de fibras nervosas e do exsudato duro como depósito lipoproteico não estão no texto; a fonte só nomeia os achados.
  - na fonte: "Dano microvascular / Formação de microaneurismas"
  - sugestão: Manter se sustentado pelas imagens de fisiopatologia e de fundo de olho; do contrário, assumir como extrapolação didática.
- `baixa` **divergencia** em resumo — tabela "Classificação por estágios", linha RDNP moderada: O resumo coloca para a RDNP moderada "encaminhamento ao oftalmologista; reavaliação em 6 meses", enquanto o quiz e a própria fonte tratam a moderada como situação de encaminhamento urgente.
  - na fonte: "ENCAMINHAMENTO URGENTE AO OFTALMOLOGISTA - Encaminhar prontamente pacientes com - Qualquer nível de edema macular diabético - RDNP moderada ou grave - Qualquer RD proliferativa"
  - sugestão: Alinhar a linha da tabela ao texto do próprio resumo ("encaminhamento urgente"), retirando o intervalo de 6 meses como conduta inicial.

### semiologia_ocular
*Material globalmente fiel à fonte, com números, doses, escalas de acuidade e o caso clínico batendo com os slides; as ressalvas são dois blocos de conteúdo (buraco estenopeico e reflexos pupilares) sem âncora no texto extraído, provavelmente apoiados em figuras, e um pequeno desalinhamento entre quiz e resumo sobre o tonômetro de Pascal.*

- `baixa` **possivelmente_na_imagem** em quiz Q16 e Q17; resumo (seção "Buraco estenopeico"); intro do quiz: Todo o tópico do buraco estenopeico (melhora com estenopeico = causa refracional; redução do círculo de difusão) não aparece em nenhum trecho de texto da fonte, e rende duas questões mais um bloco do resumo.
  - sugestão: Confirmar se há figura de oclusor estenopeico nas páginas de acuidade visual (slides 6 a 10, ricos em imagens). Se não houver, retirar as duas questões e o bloco do resumo, ou marcá-los como conteúdo complementar declarado.
- `baixa` **possivelmente_na_imagem** em quiz Q29 e Q30; resumo (seção "Exame externo", parágrafo sobre pupilas): Reflexo fotomotor direto e consensual, defeito pupilar aferente relativo e lanterna oscilante não são mencionados no texto extraído; a explicação ainda detalha a decussação parcial das fibras pupilares no quiasma e nos núcleos pré-tectais.
  - sugestão: Verificar se os slides de motilidade ocular (18 e 19) trazem figura de reflexos pupilares/DPAR. Sem essa figura, reduzir a duas questões sobre um tema sem qualquer apoio na fonte é expansão não declarada — retirar ou sinalizar como complemento.
- `baixa` **divergencia** em quiz Q23 (explicação) x resumo (seção Tonometria): O quiz enumera como portáteis apenas Perkins, Tonopen e Icare; o resumo inclui o Pascal entre os portáteis. As duas peças tratam o mesmo instrumento de formas diferentes.
  - na fonte: "PERKINS / PASCAL / TONOPEN / ICARE"
  - sugestão: Alinhar as duas peças: ou o Pascal entra na lista de portáteis nas duas, ou sai das duas.
- `baixa` **fonte_suspeita** em quiz Q26 (e tabela de fundoscopia do resumo) x slide 22: Os blocos de características da fundoscopia no slide 22 não estão rotulados por coluna, e o item "exame de toda a retina (até periferia)" aparece no bloco com "grande aumento de imagem / visão de detalhes", que o material atribui à biomicroscopia de fundo — enquanto o quiz usa o alcance da periferia como vantagem da fundoscopia indireta.
  - na fonte: "- GRANDE AUMENTO DE IMAGEM - BOA ESTEREOPSIA - VISAO DE DETALHES - EXAME DE TODA A RETINA ( ATÉ PERIFERIA)"
  - sugestão: Sustentar o gabarito da Q26 apenas pelo rótulo "mapeamento de retina" e por "grande área examinada por vez", sem atribuir à indireta o item de periferia como se fosse texto explícito do slide.

### disacusias
*O quiz é bastante fiel à fonte e não apresenta erro que leve a conduta equivocada; os ajustes necessários concentram-se no resumo, na simetria da otosclerose e na nomenclatura otospongiose/otosclerose.*

- `media` **divergencia** em resumo — abertura da seção Otospongiose e otosclerose: O resumo separa os termos: otospongiose seria a fase inicial e otosclerose, a fase tardia compactada. O quiz (Q7) e a fonte tratam otosclerose como o nome da própria osteodistrofia em que o osso denso vira esponjoso.
  - na fonte: "Otosclerose : doença focal primária da cápsula labiríntica (osteodistrofia) onde o osso denso (endocondral) é substituído por osso esponjoso"
  - sugestão: Apresentar otospongiose e otosclerose como sinônimos da doença e reservar 'espongiótica' e 'esclerótica' para as fases histológicas.
- `media` **erro_factual** em resumo — epidemiologia da otosclerose: Afirma que a otosclerose é bilateral em 70-85% 'geralmente iniciando por um lado', quando a fonte diz que geralmente é simétrica.
  - na fonte: "Bilateral em 70 a 85% dos casos • Geralmente é simétrica"
  - sugestão: Trocar por 'geralmente simétrica', como está na fonte e no restante do material.
- `baixa` **fora_da_fonte** em quiz Q26 (explicação) e resumo — sífilis congênita: As idades de 5, 10 ou 12 anos para as manifestações tardias da sífilis congênita não constam da fonte, e a página correspondente não tem imagem associada.
  - na fonte: "Sífilis congênita: • Tratamento: pelo menos até 30 dias antes do nascimento • Manifestações tardias"
  - sugestão: Remover as idades ou apresentá-las explicitamente como dado externo à aula.
- `baixa` **possivelmente_na_imagem** em quiz Q16: A paracusia de Willis não aparece no texto extraído; é achado que caberia na figura do quadro clínico da otosclerose, que não é visível para o revisor.
  - sugestão: Confirmar o fenômeno na imagem pg14; se não estiver lá, sinalizar como complemento externo à fonte.

### otites
*Material muito fiel à fonte: doses, cortes temporais e critérios de antibiótico versus observação conferem integralmente; só há ajustes menores de compressão na tabela do resumo e de conteúdo provavelmente existente nas figuras.*

- `baixa` **divergencia** em resumo — tabela da abertura (linha 'Otite média com efusão'): A tabela resume a conduta como 'Observar 3 meses, depois tubo', como se o tubo fosse automático após 3 meses, enquanto o quiz (Q24) e o próprio texto do resumo condicionam a cirurgia a critérios
  - na fonte: "OME ≥ 3 meses → Realizar avaliação auditiva, caso ainda não realizada. Considerar tratamento cirúrgico se: OME bilateral + perda auditiva; Sintomas atribuíveis à OME; Retração/atelectasia da MT; OMA r"
  - sugestão: Trocar a célula por 'Observar 3 meses; cirurgia se critérios' para não sugerir tubo indiscriminado
- `baixa` **possivelmente_na_imagem** em quiz Q36: O sinal descrito (pavilhão deslocado para frente e para fora, apagamento do sulco retroauricular) e a conduta afirmada (antibiótico endovenoso e avaliação cirúrgica imediata) não aparecem no texto extraído; a página traz apenas a palavra 'Mastoidite' ao lado de uma imagem
  - na fonte: "Mastoidite
2021
<!-- IMG:pg58 -->"
  - sugestão: Conferir a figura pg58; se o sinal clínico e a conduta não estiverem nela, remover a explicação ou ancorar em outra referência
- `baixa` **possivelmente_na_imagem** em resumo — seção 'Orelha externa: aguda, crônica e maligna': A menção a 'tecido de granulação no conduto' no quadro de otite externa maligna não consta do texto extraído
  - na fonte: "Otalgia intensa / Otorréia purulenta / Obstrução do MAE / Paralisia dos pares cranianos? / TC orelhas: Osteomielite"
  - sugestão: Confirmar nas imagens de pg10/pg11 ou retirar o detalhe

### otoscopia
*Material no geral fiel e tecnicamente sólido; os pontos a corrigir são um número incoerente no resumo (parte tensa × parte flácida), a lógica furada da questão de lateralidade e a dúvida sobre lavagem de grão, que depende das figuras das páginas 16-17.*

- `baixa` **fonte_suspeita** em quiz Q17 e resumo (contraindicação da lavagem para grão) / fonte páginas 15-17: O quiz afirma que a lavagem é contraindicada para grão vegetal, mas a fonte traz, na sequência 'Lavagem' (pg15) → 'Lavagem de grão' (pg16) → 'Remoção de grão' (pg17), rótulos que sugerem justamente uma lavagem de grão. Como o texto é só legenda de imagem, não dá para saber se o material da aula ensina a lavar grão ou se o rótulo é apenas descritivo.
  - na fonte: "Lavagem de grão (página 16) / Remoção de grão (página 17)"
  - sugestão: Conferir as imagens pg16-17; se a aula realmente mostra lavagem para grão, suavizar a contraindicação absoluta do quiz e do resumo (ou explicitar que a conduta depende do tipo/tamanho do grão).
- `média` **erro_factual** em resumo — tabela 'Membrana timpânica normal': Diz que a parte tensa é 'cerca de 90%' da membrana e, na linha seguinte, que a parte flácida é 'aproximadamente 1/5' (20%) — os dois números não fecham entre si nem com a fonte, que atribui 1/5 à parte flácida (logo, parte tensa ≈ 4/5).
  - na fonte: "Parte tensa: maior parte da membrana / Parte flácida: 1/5 da membrana"
  - sugestão: Trocar 'cerca de 90%' por 'cerca de 80% (4/5)', deixando o par tensa/flácida coerente com a fonte.
- `média` **ambigua** em quiz Q26: O critério dado ('cabo do martelo e cone de luz apontam para a frente do crânio') vale para as duas orelhas, porque em ambas essas estruturas apontam anteriormente; o que define a lateralidade é para que lado do campo visual elas apontam (direita ou esquerda do observador), informação que o enunciado não fornece. A explicação repete o mesmo salto lógico ('apontando para a frente, é a orelha esquerda').
  - sugestão: Reformular o enunciado para informar a direção no campo visual (por exemplo, 'no campo visual, o cabo do martelo e o cone de luz apontam para a direita do examinador') e corrigir a explicação: anteriormente apontam sempre; o lado do campo é que define direita ou esquerda.

### rinites_e_rinossinusites
*Material globalmente fiel à fonte: o quiz reproduz corretamente definição, ARIA, fisiopatologia, exames, tratamento e rinossinusites, e o resumo acompanha o quiz; as ressalvas são pontuais e de baixa gravidade (uma ambiguidade no critério de gravidade da ARIA e duas expansões do resumo).*

- `baixa` **ambigua** em quiz Q5: A alternativa correta traz o conjunto completo da forma moderada-grave, mas a opção B ('sono normal, prejuízo das atividades diárias e sintomas incômodos') também preenche dois dos quatro critérios de gravidade — e, se a regra for 'qualquer item presente', ela igualmente classificaria o quadro como moderada-grave.
  - na fonte: "LEVE MODERADA - GRAVE / - Sono alterado / - Comprometimento ativ. / diárias: esporte, lazer, etc. / - Alteração escola e/ou trabalho / - Com sintomas incômodos"
  - sugestão: Reescrever o enunciado como 'que conjunto completo de achados define a forma moderada-grave' ou trocar os distratores por inversões de um único item, evitando combinações parcialmente compatíveis.
- `baixa` **possivelmente_na_imagem** em resumo — Rinossinusites: anatomia: O resumo afirma que os óstios desembocam 'em sua maioria, no meato médio, na região do processo uncinado e do hiato semilunar'; esse detalhe anatômico não aparece no texto extraído, apenas na figura da página.
  - na fonte: "Nariz e seios paranasais / Corte coronal Corte sagital <!-- IMG:pg27 -->"
  - sugestão: Manter, se a figura pg27 realmente rotular o complexo ostiomeatal; caso contrário, retirar o detalhe.
- `baixa` **fora_da_fonte** em resumo — Tratamento: O resumo hierarquiza o tratamento em degraus e atribui mecanismo a cada classe (anti-histamínico cobre a fase imediata; corticoide tópico nasal cobre a fase tardia e a obstrução; imunoterapia é 'a única que atua na sensibilização'), e propõe suspender o vasoconstritor e 'cobrir o rebote' com corticoide tópico — nada disso está na fonte, que apenas lista as opções terapêuticas.
  - na fonte: "Tratamento: Higiene ambiental / Lavagem nasal com SF / Anti-histamínicos orais ou tópicos / Corticóides tópicos / Descongestionantes sistêmicos / Corticóides orais / Estabilizadores de membrana de mas"
  - sugestão: Sinalizar essas passagens como extrapolação clínica do autor ou reduzir ao que a fonte lista, sem atribuir mecanismo nem conduta de retirada.

### zumbido_e_tontura
*Material globalmente fiel à fonte, sem erros factuais relevantes no quiz; as ressalvas são de baixa gravidade (uma imprecisão sobre a origem das otocônias no enunciado e detalhes ilustrativos do resumo não presentes no texto extraído), e a expansão semiológica do resumo final está explicitamente declarada.*

- `baixa` **divergencia** em quiz Q26: A alternativa correta diz que as otocônias se deslocam "do utrículo" para os canais semicirculares, enquanto a fonte (e o próprio comentário da questão e o resumo) falam do complexo sáculo-utrículo.
  - na fonte: "Tontura ocasionada pelo deslocamento dos otólitos (otocônias) do complexo sáculo-utrículo para os canais semicirculares"
  - sugestão: Trocar "do utrículo" por "do complexo sáculo-utrículo" na alternativa, alinhando-a ao comentário e ao resumo.
- `baixa` **possivelmente_na_imagem** em resumo, seção Período crítico: O resumo detalha que o bezerro anda em poucas horas e o bebê leva um ano; o texto extraído da pg05 só traz "Bezerro x bebê: mielinização", sem esses detalhes.
  - na fonte: "Bezerro x bebê: mielinização"
  - sugestão: Conferir a figura da pg05; se o detalhe não estiver lá, suavizar para "comparação entre bezerro e bebê ilustra o grau de maturação ao nascer".

### alergia_e_atopia
*Material globalmente fiel à fonte: os tipos de Gell e Coombs, os subtipos IIa/IIb e IVa-IVd, os números de atopia e da marcha atópica, os fatores de risco/proteção e o diferencial das dermatites batem com o texto; os problemas encontrados são pequenas divergências de intervalo entre quiz e resumo, sem erro que leve a conduta errada.*

- `baixa` **divergencia** em quiz Q6 (explicação) x resumo (seção Gell e Coombs): O quiz diz que o intervalo da hipersensibilidade tipo III é de 'dias a uma semana'; o resumo diz 'dias a semanas', com a doença do soro em 'cerca de 1 a 3 semanas'. São faixas diferentes para o mesmo quadro.
  - na fonte: "Slide 5: 'III | Ag-Ac (IC) → Ativação do complemento e recruta células inflamatórias | Doença do soro...' (a fonte não define o intervalo)"
  - sugestão: Unificar a faixa nos dois materiais (por exemplo, 'dias a poucas semanas, tipicamente 1 a 2 semanas para a doença do soro') e usar o mesmo texto na explicação do quiz e na tabela do resumo.
- `baixa` **divergencia** em quiz Q36 (alternativa sobre repetição) x resumo (bloco de conduta na anafilaxia): O quiz apresenta a repetição da adrenalina 'em cinco minutos' como conduta adequada; o resumo orienta repetir 'a cada 5 a 15 minutos'. O aluno lê duas regras de repetição diferentes.
  - sugestão: Padronizar a redação do intervalo (por exemplo, 'repetir a cada 5 minutos, podendo espaçar até 15 minutos enquanto houver resposta insuficiente') nos dois materiais.

### imunidade
*Quiz e resumo são internamente coerentes e sem erro factual relevante, com alternativas corretas claramente superiores; o problema é de escopo — o bloco neonatal (Q27–Q32 e a seção correspondente do resumo) e alguns detalhes de complemento e imunoglobulinas vão além do que a fonte textual sustenta.*

- `media` **fora_da_fonte** em quiz Q27 a Q32 e resumo (seção "A imunidade do recém-nascido e do lactente"): Todo o bloco neonatal — IgG placentária via FcRn no 3º trimestre, IgM fetal nas infecções congênitas, IgA secretora do colostro, nadir de IgG entre 3 e 6 meses, imunidade passiva pós-exposição e vacinas conjugadas — não tem apoio no texto da fonte, que termina na tolerância central/periférica e só cita 'a classe do AC' de passagem. O subtítulo do quiz anuncia esse conteúdo como se fosse da aula.
  - sugestão: Manter o bloco, mas sinalizar como complemento de outra fonte (ou como 'particularidades do lactente' fora do escopo da aula 1), para não dar a entender que foi cobrado na aula.
- `baixa` **possivelmente_na_imagem** em resumo (seção "Sistema complemento") e quiz Q10/Q11: As três vias de ativação (clássica via C1q, das lectinas via MBL/MASP, alternativa), as convertases e os reguladores (fator H, CD55, CD46, CD59) não aparecem no texto; a fonte só descreve os produtos C3b, C3a/C5a e MAC. Caberia numa figura da cascata em s15i1, mas não é possível confirmar.
  - na fonte: "C3b favorece a opsonização; C3a e C5a contribuem para inflamação; O complexo de ataque à membrana (MAC) causa lise celular"
  - sugestão: Se a figura s15i1 não trouxer as vias, marcar o trecho como complemento externo ou reduzi-lo ao que a fonte sustenta.
- `baixa` **possivelmente_na_imagem** em resumo (quadro do complemento) e quiz Q11 (explicação): A associação entre deficiência de C5–C9 e infecção invasiva de repetição por Neisseria é afirmada como 'dado de anamnese que muda a conduta', mas a fonte não menciona nenhum déficit de complemento nem Neisseria.
  - na fonte: "O complexo de ataque à membrana (MAC) causa lise celular"
  - sugestão: Tratar como correlação clínica acrescentada, não como conteúdo da fonte; se quiser manter o destaque, indicar a origem.

### imunidade_parte_2
*Material fiel e bem alinhado ao texto dos slides, com resumo e quiz consistentes entre si; o único ponto relevante é a reprodução, pelo quiz, de uma associação provavelmente equivocada da própria fonte entre doença granulomatosa crônica e neutropenia.*

- `media` **fonte_suspeita** em fonte slide 31 (e quiz Q29, que a reproduz): A fonte coloca a doença granulomatosa crônica como exemplo de defeito fagocítico cujo achado é neutropenia no hemograma; o quiz repete isso como resposta correta. A DGC é defeito qualitativo da explosão oxidativa, com número de neutrófilos normal — quem estuda por essa frase espera neutropenia em uma doença que não a tem.
  - na fonte: "Defeitos fagocíticos ➜ Neutropenia (ex.: doença granulomatosa crônica, neutropenia)."
  - sugestão: Separar as duas entidades: neutropenia como defeito quantitativo e DGC como defeito qualitativo (diagnóstico por DHR/citometria, não por contagem). Se o quiz mantiver a pergunta, restringi-la às neutropenias congênitas.
- `baixa` **possibly_na_imagem** em resumo — tabela 'Tipo, clínica e exame inicial' (linha Defeitos fagocíticos): O resumo atribui aos defeitos fagocíticos a clínica de 'abscessos, infecções bacterianas e fúngicas'; o texto da fonte só traz 'doença granulomatosa crônica, neutropenia' e 'neutropenia no hemograma'.
  - na fonte: "Defeitos fagocíticos - ex.: doença granulomatosa crônica, neutropenia"
  - sugestão: Conferir a figura s07i1; se a descrição clínica não estiver lá, remover a coluna ou limitá-la a 'infecções bacterianas e fúngicas de repetição'.

### imunodeficiencias
*Material bastante fiel: o quiz reproduz com precisão números, classificações e condutas da fonte e não há divergência entre quiz e resumo; os únicos reparos são duas extrapolações (vacinas vivas na SCID e idades de início na tabela do resumo) e um mecanismo que depende de figura.*

- `baixa` **fora_da_fonte** em quiz Q17 (e resumo, bloco "Contraindicação absoluta de vacina de agente vivo"): A suspensão de vacinas de agentes vivos na SCID não é abordada na fonte: o slide de tratamento cita apenas suporte, antimicrobianos, IgG e transplante, e essa página não tem figura de onde o dado pudesse vir.
  - na fonte: "Tratamento: Suporte, antimicrobianos e substituição de IgG. Terapia definitiva: Tx células-tronco hematopoiéticas (HSCT) mais rápido possível."
  - sugestão: A conduta está clinicamente correta, mas é extrapolação: ou retirar a questão, ou sinalizar no material que esse ponto vai além do que foi dado em aula.
- `baixa` **fora_da_fonte** em resumo — tabela "Os cinco compartimentos": A tabela acrescenta idades de início ("depois do 6º mês, quando a IgG materna se esgota", "escolar e adolescente" no complemento, "pré-escolar na ALPS") e germes/achados específicos (fungos filamentosos, abscessos profundos e granulomas nos fagócitos) que não constam do texto extraído; essas páginas (8, 10, 14) não têm figura.
  - na fonte: "Defeitos fagocíticos ➜ Neutropenia (ex.: doença granulomatosa crônica, neutropenia)."
  - sugestão: Manter como complemento, mas marcar que é acréscimo e não conteúdo da aula, para o leitor não cobrar de si esse detalhe.
- `baixa` **possivelmente_na_imagem** em quiz Q5: O enunciado afirma que a AIRE comanda a seleção negativa no timo e a conversão de clones em Treg; o texto só diz que APECED é alteração de AIRE, sem descrever o mecanismo.
  - na fonte: "APECED – alteração AIRE"
  - sugestão: Confirmar contra a figura s03i1; se o esquema não trouxer o mecanismo, reformular o enunciado para se apoiar apenas na associação AIRE–APECED.

### saude_sexual_do_adolescente
*O material é fiel à fonte nos eixos centrais (pilares da consulta, sigilo e suas exceções, HEADSSS/5 Ps, prevenção combinada, DIP, PrEP/PEP, violência e gestação); o que destoa é o bloco de contracepção detalhada e o detalhamento legal, que vão além do texto extraído e deveriam ser declarados como complementares.*

- `baixa` **fora_da_fonte** em quiz Q37 e resumo (seção 'Dever legal'): A obrigação de comunicar o Conselho Tutelar e de notificar compulsoriamente à vigilância epidemiológica não aparece no texto; a fonte fala apenas em acionar a rede/fluxo de proteção
  - na fonte: ""Acionar a rede de proteção conforme fluxo local" / "Acionar rede/fluxo""
  - sugestão: Manter a conduta, mas ancorá-la na formulação genérica da fonte ou marcá-la como acréscimo ao material
- `baixa` **erro_factual** em resumo — tabela de confidencialidade, linha 'Necessidade de internação hospitalar': A tabela classifica a internação como 'sigilo mantido, autorização necessária', mas a fonte condiciona a internação à autorização do responsável legal, o que implica necessariamente contato com a família
  - na fonte: ""Em casos de internação hospitalar, será necessária a autorização de pai-mãe-responsável legal, o que não impedirá qualquer conduta de emergência.""
  - sugestão: Reescrever a linha: a internação exige autorização do responsável (a família é necessariamente envolvida), preservando-se o sigilo sobre o conteúdo da consulta na medida do possível
- `média` **fora_da_fonte** em quiz Q25 a Q31 e resumo (seções 'Contracepção na adolescência' e 'Vacinação'): Doses, esquemas, mecanismos e comparação de métodos (LARC como primeira linha, levonorgestrel 1,5 mg até 5 dias, DIU de cobre como CE mais eficaz, injetável trimestral e massa óssea, dupla proteção, esquema de HPV em dose única 9–14 anos) não constam do texto da fonte
  - na fonte: ""Contracepção (inclui emergência quando indicado)" e "Vacinas (HPV/Hep B)" — não há no texto nenhum esquema, dose ou comparação de métodos"
  - sugestão: Sinalizar esse bloco como conteúdo complementar (a fonte só sustenta a existência da contracepção, inclusive de emergência, e das vacinas de HPV/Hep B) ou reduzi-lo ao que a fonte declara

### prescricao_medica
*Material no geral fiel e bem ancorado na fonte, com questões e resumo coerentes entre si; os problemas encontrados são um erro aritmético herdado da fonte ('10x' em vez de 3x na dose de levotiroxina) e uma receita-modelo da aula que contraria a própria regra de interação anlodipino-sinvastatina.*

- `média` **fonte_suspeita** em quiz Q35 e resumo (seção 'Erros de prescrição que se repetem') — erro herdado da fonte (exercicios_receituario, caso 2): A troca de levotiroxina de 50 mcg para 150 mcg é descrita como 'erro de dose dez vezes maior', mas 150/50 corresponde a 3 vezes, não a 10. O quiz usa esse número na alternativa correta e o resumo o repete.
  - na fonte: "Erro não intencional de dose (10x maior), com risco de tireotoxicose."
  - sugestão: Corrigir para 'erro de dose três vezes maior' no quiz e no resumo (e, se possível, apontar a inconsistência da fonte, já que 50 mcg e 150 mcg constam do mesmo caso).
- `média` **fonte_suspeita** em fonte (slide 49, receita-modelo do Cenário 5) em contraste com slide 31 — repercute no quiz Q33: A receita considerada correta no Cenário 5 mantém sinvastatina 40 mg/dia junto ao anlodipino 5 mg, contrariando a regra da própria aula de limitar a sinvastatina a 20 mg/dia nessa associação. O quiz Q33 adota corretamente o limite de 20 mg/dia, mas o aluno que estudar pela receita-modelo pode aprender o oposto.
  - na fonte: "Anlodipino + Sinvastatina — ↑ risco de miopatia — Limitar sinvastatina a 20 mg/dia | Receita do Cenário 5: 'Sinvastatina 40mg _____________ Uso contínuo / Tomar 1 comprimido via oral, 1 vez ao dia, ap"
  - sugestão: Manter no quiz e no resumo o limite de 20 mg/dia (sustentado pelo slide 31 e pelo caso 10 dos exercícios) e sinalizar que a receita-modelo do slide 49 está inconsistente com a tabela de interações.

### exame_psiquico
*Material bastante fiel à fonte: o quiz reproduz corretamente definições, escalas, classificações e exemplos da aula, e o resumo não diverge dele; o único ponto que merece conferência é a classificação da Síndrome de Ekbom, herdada da própria fonte.*

- `baixa` **fonte_suspeita** em quiz Q17 (e fonte, seção 5 — Senso percepção): A fonte classifica a Síndrome de Ekbom como alucinação tátil, mas a descreve como crença ('passo a acreditar que tem múltiplos insetos caminhando sobre o meu corpo'), o que é classicamente descrito como delírio de parasitose; o quiz repete fielmente a classificação da fonte.
  - na fonte: "alucinação tátil (como na Síndrome de Ekbom, que é quando eu passo a acreditar que tem múltiplos insetos caminhando sobre o meu corpo)"
  - sugestão: Manter a alternativa como está, por fidelidade à aula, mas vale conferir com o professor: se a prova seguir a literatura clássica, Ekbom é delírio (parasitose delirante), não alucinação tátil.

### impulsividade_e_compulsividade
*Material globalmente fiel à fonte: alternativas corretas, doses, cortes e classificações conferem com os slides, e os poucos problemas estão em generalizações da tabela comparativa do resumo, de baixa gravidade.*

- `baixa` **erro_factual** em resumo — tabela impulsividade × compulsividade: A tabela afirma que, na compulsividade, "não há prazer direto no ato", generalizando para todo comportamento compulsivo o que a fonte diz apenas do TOC; a própria fonte descreve comportamentos repetitivos focados no corpo com satisfação e recompensa.
  - na fonte: "Não há prazer direto algum na realização destes atos inúteis (TOC) — mas, sobre a escoriação de pele: "Sofrimento + satisfação, alívio e recompensa""
  - sugestão: Restringir a afirmação ao TOC/rituais e ressalvar que nos comportamentos repetitivos focados no corpo e na cleptomania o ato produz alívio e satisfação, ainda que seguidos de culpa.
- `baixa` **divergencia** em resumo — tabela, linha "Direção do erro" vs quiz Q6/Q7: O resumo atribui a pressão "de baixo para cima" apenas à impulsividade, deixando para a compulsividade somente "hábito automatizado, rigidez cognitiva"; o quiz e a fonte dizem que a pressão excessiva vinda de baixo vale para as duas — do estriado ventral na impulsividade e do dorsal na compulsividade.
  - na fonte: "falha nos sistemas de inibição de resposta – insuficiente controle cognitivo de cima para baixo – ou muita pressão vinda de baixo para cima do estriado ventral para impulsividade ou do estriado dorsal"
  - sugestão: Reescrever a célula da compulsividade incluindo também a hipótese de pressão excessiva de baixo para cima a partir do estriado dorsal, como faz a explicação do Q7.
- `baixa` **fora_da_fonte** em resumo — seção Sexualidade: O resumo exemplifica a hipersexualidade como sintoma da mania; a fonte apenas diz que é sintoma presente em outras patologias, sem nomear a mania.
  - na fonte: "Hipersexualidade — Sintoma presente em outras patologias / Ou uma manifestação de dependência"
  - sugestão: Retirar o exemplo "mania" ou marcá-lo como exemplo clínico do autor do resumo, não da aula.

### transtorno_depressivo
*Material globalmente fiel à fonte no que ela traz em texto (prevalência, números de impacto, exame psíquico, fases do tratamento, kindling, trauma, suicídio); os pontos a ajustar são a divergência sobre os dois sintomas cardinais e o grande bloco farmacológico e de especificadores que a fonte textual não sustenta.*

- `baixa` **erro_factual** em quiz Q2 (e resumo, seção "Critérios do episódio depressivo maior"): O gabarito diz que "pelo menos um" dos dois sintomas cardinais precisa estar presente; a fonte afirma que os dois primeiros são obrigatórios.
  - na fonte: "Cinco ou mais dos seguintes sintomas durante um mesmo período de 2 semanas (sendo os 2 primeiros obrigatórios): Humor deprimido na maior parte do dia... Perda do interesse ou prazer por todas ou quase"
  - sugestão: Alinhar a explicação de Q2 e a frase do resumo ao texto da fonte ("os dois primeiros são obrigatórios") ou registrar explicitamente que se adota o critério do DSM-5 (basta um dos dois), para que quiz e resumo não contradigam o slide.
- `baixa` **fora_da_fonte** em quiz Q15 a Q18, Q22, Q23, Q24 e tabela de antidepressivos do resumo: Todo o bloco farmacológico (ISRS, IRSN, tricíclicos, IMAO, bupropiona, mirtazapina, latência de 4–8 semanas, esquema de troca/potencialização, indicações de ECT, manutenção por anos) não aparece no texto extraído da aula, que só lista classes de fármacos sem detalhá-las; não há marcador de imagem nos slides correspondentes.
  - na fonte: "Psicofarmacoterapia - Antidepressivos - Estabilizadores do Humor - Benzodiazepínicos - Hormônios tireoideanos - Neurolépticos (?)"
  - sugestão: Manter o conteúdo (é clinicamente correto), mas sinalizar na introdução do quiz/resumo que esse trecho foi complementado com diretrizes externas, ou conferir se essas informações constam de slides/figuras não capturados.
- `baixa` **possivelmente_na_imagem** em quiz Q5 a Q10, Q13 e Q28; resumo, seção "Formas clínicas e especificadores": Critérios de transtorno depressivo persistente (dois anos), características melancólicas, atípicas, psicóticas, padrão sazonal, blues puerperal e sinais de bipolaridade não constam do texto extraído; os slides 6, 7, 8, 40 e 49 não têm marcador de imagem, então não é possível confirmar a origem.
  - na fonte: "Possíveis Apresentações - Psicótica X neurótica - Endógena X Reativa - Primária X Secundária - Maior X Distimia - Unipolar X Bipolar"
  - sugestão: Confirmar esses trechos contra os slides originais; se vieram de fora da aula, declarar a fonte complementar.

### transtornos_alimentares
*Material fiel à fonte, sem erro factual, ambiguidade ou divergência entre quiz e resumo; as únicas ressalvas são duas inconsistências internas da própria fonte (CID-10 vs. CID-11 e 1990 vs. 1994) e detalhes de dose que só podem ser confirmados nas figuras.*

- `baixa` **fonte_suspeita** em fonte, slide 22 vs. slides 32 e 38 (e resumo, 1º parágrafo): A fonte cita o rol de transtornos como 'CID-10 e DSM-V', mas usa códigos da CID-11 (6B81, 6B8Y/6B82) nas páginas seguintes; o resumo adotou 'DSM-5 e CID-11' sem sinalizar a troca.
  - na fonte: ""CID – 10 e DSM-V: Anorexia Nervosa (AN), Bulimia Nervosa (BN), Transtorno de Compulsão Alimentar Periódica" / "CID 11 Bulimia nervosa 6B81" / "Transtorno da Compulsão Alimentar TCA ou Binge Eating 6B"
  - sugestão: Padronizar a classificação (CID-11) em todo o material e confirmar com o professor qual versão a prova cobra.
- `baixa` **fonte_suspeita** em fonte, slide 18 (título vs. bullet) e resumo, seção de neurobiologia: O ano da leptina aparece como 1990 no bullet e como 1994 no título do mesmo slide; o resumo fixa 1994 ('clonada em 1994').
  - na fonte: ""A descoberta do hormônio peptídico e do fator de saciedade Leptina em 1994" / "1990, Jeffrey Friedman e colegas da Universidade Rockefeller clonaram o gene que codifica a leptina""
  - sugestão: Escolher um único ano e corrigir o bullet do slide (o resumo já está coerente com o título).
- `baixa` **possivelmente_na_imagem** em quiz Q12 e Q13: 'Olanzapina em dose baixa' e 'fluoxetina em doses de até 60 mg por dia' não constam do texto extraído; só o nome dos fármacos aparece.
  - na fonte: ""Tratamento Psicofarmacoterapia/psicoterapia: ISRS/ Olanzapina" (slide 29) / "Tratamento Psicofarmacoterapia/psicoterapia: ISRS - Fluoxetina" (slide 35)"
  - sugestão: Conferir as figuras s29i1 e s31i1-4; se a dose não estiver nelas, retirar o valor numérico ou marcá-lo como acréscimo do autor.
