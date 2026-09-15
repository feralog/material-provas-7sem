## Por que a leitura crítica precisa vir antes da prática

Um paciente que traz uma notícia, um post de influenciador ou uma resposta de chatbot não está errado em perguntar — mas "eu acho", "eu li" e "eu vi um caso" não têm o mesmo peso que uma evidência bem produzida. Um relato isolado de melhora (ou de piora) não permite nenhuma inferência sobre causa e efeito, porque não existe grupo de comparação nem controle de variáveis. A pergunta que sustenta toda a análise crítica de um artigo não é "o influenciador está mentindo?", mas sim **o desenho do estudo é capaz de responder à pergunta clínica em questão?** — a conclusão pode estar tecnicamente correta e, ainda assim, vir de um estudo incapaz de sustentá-la com rigor.

Para classificar um artigo, cinco perguntas básicas orientam a leitura:

1. É um estudo original ou uma síntese de outros estudos?
2. Quem é o público-alvo — a amostra reflete a população que me interessa?
3. O delineamento está bem escolhido para a pergunta que pretende responder?
4. Foram usadas ferramentas para reduzir viés sistemático?
5. O número de pacientes e o tempo de seguimento foram suficientes para o desfecho avaliado?

Nem toda pergunta clínica tem um estudo perfeito disponível — doenças raras, por exemplo, dificilmente terão um ensaio clínico randomizado de milhares de pacientes. Isso não inviabiliza usar o que existe, mas exige explicitar as limitações ao aplicar o resultado.

## PICO: decompondo a pergunta clínica

Antes de escolher um artigo, é preciso saber exatamente qual pergunta ele deve responder. O **PICO** é a estrutura padrão para isso, decompondo qualquer dúvida clínica em quatro componentes:

- **P — Paciente ou Problema**: quem é a população de interesse (idade, diagnóstico, gravidade)?
- **I — Intervenção**: qual exposição, tratamento ou procedimento está sendo testado?
- **C — Comparação**: contra o que a intervenção é comparada (placebo, outro fármaco, nenhuma intervenção)?
- **O — Outcome (resultado)**: qual desfecho está sendo medido, e em que prazo?

Um artigo só é capaz de responder a uma pergunta clínica quando seu PICO corresponde ao PICO da dúvida original. Um estudo com excelente metodologia, mas conduzido numa população, intervenção ou desfecho diferentes do que se quer saber, simplesmente não responde à pergunta — por melhor que seja o desenho.

## Os delineamentos de estudo e a classificação de Oxford

A classificação de Oxford (CEBM — Oxford Centre for Evidence-Based Medicine) organiza os delineamentos mais comuns por características, exemplo típico e vantagem principal:

| Tipo de estudo | Características | Exemplo | Vantagem principal |
| --- | --- | --- | --- |
| ECR (ensaio clínico randomizado) | Randomização, grupo controle, cegamento | Teste de nova droga vs. placebo | Padrão-ouro para causalidade e eficácia |
| Coorte | Observa exposição → desfecho, prospectiva ou retrospectiva | Tabagistas vs. não tabagistas e incidência de câncer | Ótimo para incidência e história natural da doença |
| Caso-controle | Parte do desfecho → busca exposição prévia | Pacientes com IAM vs. sem IAM e uso prévio de AINE | Eficiente para doenças raras ou de longa latência |
| Transversal | Foto única, mede prevalência | Prevalência de osteoporose em mulheres > 60 anos | Rápido, barato, ótimo para prevalência |
| Série de casos / relato | Descrição de casos clínicos, sem grupo comparação | 10 pacientes com lúpus e miocardite | Identifica doenças novas ou efeitos colaterais raros |
| Revisão sistemática / metanálise | Integra múltiplos estudos com métodos reprodutíveis | Revisão Cochrane sobre corticoide na artrite | Maior nível de evidência para decisão clínica |

### Estudos de intervenção × observacionais

A diferença central entre essas duas famílias não é sutil: em um **estudo de intervenção** (ECR, estudos cruzados, ensaios de campo), o pesquisador **controla ativamente** a exposição, o que permite avaliar relação de causa-efeito, eficácia e efetividade. Já em um **estudo observacional** (coorte, caso-controle, transversal, série de casos), o pesquisador **apenas observa** a realidade, sem interferir no curso dos eventos — servindo para descrever fenômenos, encontrar associações e gerar hipóteses.

| Critério | Estudos de intervenção | Estudos observacionais |
| --- | --- | --- |
| Papel do pesquisador | Controla ativamente a exposição | Apenas observa, sem interferir |
| Objetivo principal | Causa-efeito, eficácia, efetividade | Descrever, associar, gerar hipóteses |
| Limitação típica | Caros, complexos, barreiras éticas | Suscetíveis a viés de confundimento |
| Quando usar | Provar que um tratamento funciona (fase III) | Entender frequência/risco de uma exposição |

> Um resultado observacional pode ser real e ainda assim estar distorcido por um fator externo não medido — o confundimento. Isso não invalida o estudo, mas exige cautela redobrada antes de afirmar causalidade.

## Limitações metodológicas específicas de cada delineamento

Mesmo com o delineamento certo escolhido, é preciso olhar fatores específicos de viés dentro dele. Para ensaios clínicos randomizados de superioridade, cinco falhas costumam comprometer o resultado:

1. **Ausência de sigilo da alocação** — quem recruta consegue prever o próximo grupo por uma randomização previsível (por dia da semana, por exemplo), o que permite selecionar quem entra em cada braço.
2. **Ausência de mascaramento (cegamento)** — pacientes, cuidadores, coletores de dados ou avaliadores de desfecho sabem qual tratamento foi dado, o que pode enviesar a interpretação do resultado.
3. **Seguimento incompleto** — perda de pacientes randomizados ao longo do estudo, sem análise por intenção de tratar.
4. **Relato seletivo de desfechos** — resultados desfavoráveis ou secundários simplesmente não são publicados.
5. **Outras limitações** — como interrupção precoce do estudo por benefício aparente, ou uso de desfechos substitutos sem validação.

Para estudos observacionais, as limitações mais características são a **seleção e inclusão inadequada de participantes** (pareamento ruim entre casos e controles, ou populações de origem diferentes entre expostos e não expostos), a **ausência de mascaramento** na avaliação da exposição ou do desfecho (por exemplo, viés de recordação) e a **falha em controlar adequadamente os fatores de confusão** — quando fatores prognósticos conhecidos não são medidos com precisão.

![Quadro 6 e 7 — limitações específicas de ensaios randomizados e de estudos observacionais](img:pg09)

## Ferramentas de avaliação de qualidade: GRADE, AMSTAR-2 e RoB 2

Delineamento adequado não é garantia de estudo confiável — por isso existem ferramentas específicas para auditar a qualidade de um artigo. Cada uma tem um alvo diferente, e confundi-las é um erro comum:

| Ferramenta | O que avalia |
| --- | --- |
| **GRADE** | Qualidade geral da evidência clínica e força das recomendações, de forma ampla |
| **AMSTAR-2** | Qualidade metodológica especificamente de revisões sistemáticas |
| **RoB 2** | Risco de viés especificamente dentro de ensaios clínicos randomizados |

### GRADE (Grading of Recommendations, Assessment, Development and Evaluation)

É o sistema mais usado por organizações como OMS, Cochrane e UpToDate para padronizar a classificação da qualidade da evidência. Seu diferencial é a **transparência**: qualquer leitor consegue reconstruir como os avaliadores chegaram àquela recomendação. O GRADE avalia cinco domínios:

| Domínio | O que avalia | Exemplo |
| --- | --- | --- |
| Risco de viés | Se o estudo foi desenhado para minimizar erros sistemáticos | ECR sem randomização descrita aumenta o risco |
| Consistência dos resultados | Se os resultados se repetem entre estudos ou subgrupos | Metanálise com I² < 25% indica consistência |
| Precisão | Tamanho da amostra e largura do intervalo de confiança (IC) | IC 95% estreito indica mais precisão |
| Evidência direta | Se população, intervenção e desfecho são diretamente aplicáveis | Estudo em adolescentes extrapolado para adultos é evidência indireta |
| Viés de publicação | Se houve busca ampla de estudos e omissão de resultados negativos | Só incluir estudos patrocinados com resultado positivo é sinal de alto risco |

A partir desses cinco domínios, a evidência recebe uma classificação final:

- **Alta** — resultados muito confiáveis.
- **Moderada** — podem mudar com novos estudos.
- **Baixa** — grande incerteza.
- **Muito baixa** — resultados altamente incertos.

Um ensaio clínico randomizado **começa** na classificação alta; um estudo observacional **começa** mais abaixo. Mas essa posição de partida pode subir (por exemplo, com efeito muito grande e consistente) ou descer (por exemplo, com financiamento da indústria somado a desenho aberto).

## A pirâmide de evidências e o viés de pesquisa

A pirâmide de evidências organiza os delineamentos conforme sua capacidade de fornecer conclusões livres de viés e com maior força de recomendação. Quanto mais alto na pirâmide, menor o risco de viés e maior a confiança para aplicar o resultado diretamente ao paciente — mas essa posição só se traduz em recomendação forte de fato quando confirmada por ferramentas como o GRADE.

![Pirâmide de evidências científicas: da opinião de especialistas, na base, até revisões sistemáticas e metanálises, no topo](img:pg17)

Da base para o topo, a ordem típica é: opinião de especialistas sem avaliação crítica → séries de casos e relatos de caso → estudos de caso-controle → estudos de coorte → ensaios clínicos randomizados → revisões sistemáticas e metanálises.

**Viés de pesquisa** é o nome geral para os erros sistemáticos que distorcem os resultados de um estudo, comprometendo sua validade interna. Toda pesquisa carrega algum grau de viés — o que muda é o quanto ele foi minimizado e quão transparente foi essa avaliação. Por isso, avaliar risco de viés é etapa obrigatória em qualquer revisão sistemática séria.

## Caso aplicado: semaglutida × tirzepatida na obesidade e na esteatose hepática

Um paciente com obesidade grau 1 (IMC 31, 92 kg, 170 cm) e esteatose hepática leve, sem fibrose, diabetes ou hipertensão, quer saber se semaglutida ou tirzepatida podem fazê-lo perder 30 kg, qual das duas é melhor, se a perda se mantém e se o medicamento trata também a esteatose. Ambas são terapias baseadas em incretinas: a **semaglutida** é agonista do receptor GLP-1 de ação prolongada, reduzindo apetite e retardando o esvaziamento gástrico; a **tirzepatida** é agonista duplo, atuando também no receptor GIP — inclusive em receptores de GIP presentes nos adipócitos —, o que é a hipótese para sua maior eficácia na redução de peso.

Analisar criticamente cada estudo citado exige sempre o mesmo roteiro: delineamento (classificação de Oxford), PICO, pontos fortes e fracos da metodologia, ferramentas de avaliação de viés usadas, e classificação GRADE resultante.

| Estudo | Delineamento | Resultado principal | Viés relevante | GRADE |
| --- | --- | --- | --- | --- |
| SURMOUNT-5 | ECR fase 3b, head-to-head, aberto (open-label) | Tirzepatida: 19,7% ≥30% de perda de peso; semaglutida: 6,9% | Patrocínio (Eli Lilly) + ausência de cegamento | Alta → Moderada |
| Coorte EHR (Truveta) | Coorte observacional, pareamento por escore de propensão 1:1 | Tirzepatida superior à semaglutida em mundo real, > 18 mil pacientes pareados | Fatores de confusão não mensurados (motivação, estilo de vida) | Moderada → Alta |
| STEP 5 | ECR fase 3, duplo-cego, controlado por placebo, 2 anos | Perda de ~15,2% com semaglutida, estável da semana 60 à 104 | Patrocínio (Novo Nordisk), baixa diversidade racial (7% não brancos) | Alto → Moderado |
| ESSENCE | ECR fase 3, multicêntrico, duplo-cego, placebo, biópsia centralizada | 62,9% de resolução da esteato-hepatite com semaglutida vs. 34,3% placebo | Patrocínio (Novo Nordisk), mitigado por patologistas cegados | Não detalhado — biópsia cegada eleva a confiança |

No SURMOUNT-5, a diferença mais citada nas redes — tirzepatida 2,8 vezes mais provável de atingir 30% de perda de peso do que a semaglutida — é numericamente correta, mas vem de um **desfecho secundário adicional (exploratório)**, não do desfecho primário do estudo. O desenho aberto (pacientes e investigadores sabiam qual droga usavam) e o financiamento pela fabricante da tirzepatida são os motivos do rebaixamento cauteloso de alta para moderada.

> Desfecho primário e desfecho exploratório não têm o mesmo peso estatístico. Um resultado exploratório pode ser real e ainda assim não ter sido "procurado" com o mesmo rigor amostral do desfecho principal — é um sinal de alerta, não um motivo para descartar o dado.

O ESSENCE, por sua vez, só testou semaglutida contra placebo: não existe, ali, nenhuma comparação com tirzepatida, então qualquer afirmação sobre tirzepatida tratar a esteato-hepatite não pode se apoiar nesse estudo.

## O que é extrapolável para este paciente, e o que não é

Um estudo bem desenhado metodologicamente e um resultado extrapolável para um paciente específico são duas perguntas diferentes — a primeira é sobre a qualidade interna do estudo, a segunda é sobre a semelhança entre a amostra estudada e a pessoa à sua frente.

- **Raça**: favorável. Participantes brancos foram maioria tanto no STEP 5 (93,1%) quanto no SURMOUNT-5 (76,1%), compatível com o perfil do paciente.
- **Sexo**: limitado. O STEP 5 teve apenas 22,4% de homens — proporção que os próprios autores consideram insuficiente para conclusões definitivas nesse subgrupo; o SURMOUNT-5 teve 35,3% de homens.
- **Meta de perda de peso**: ambiciosa. Perder 30 kg a partir de 92 kg equivale a cerca de 32,6% do peso corporal — mais exigente que o corte de 30% avaliado no SURMOUNT-5, atingido por apenas 19,7% do grupo tirzepatida e 6,9% do grupo semaglutida.
- **Gravidade da doença hepática**: não compatível. O ESSENCE incluiu apenas pacientes com esteato-hepatite (MASH) e fibrose em estágios 2 ou 3 — um estágio muito mais avançado do que a esteatose grau 1 sem fibrose do paciente.

> Nenhum desses estudos foi conduzido especificamente para responder pela realidade deste paciente. Os dados são parcialmente extrapoláveis: sustentam a plausibilidade de um benefício, mas não garantem a mesma magnitude de resultado — e a decisão final ainda depende do julgamento clínico individual, algo que nenhum artigo isolado substitui.

---

Esse roteiro — delineamento, PICO, pontos fortes e fracos, ferramenta de viés, classificação GRADE e extrapolabilidade — é o que separa uma leitura crítica de um artigo científico de uma simples repetição do que "alguém leu e achou".
