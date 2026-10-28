# Exploratório de fontes para enriquecimento

Data: 27/10/2026. Base analisada: **3.267 municípios, 968.939 alunos e 25 UFs, exclusivamente do treino**. Alvo: proporção municipal de alunos válidos não alfabetizados em 2024. A versão entregue e o teste v1 foram preservados. Não houve treinamento ou seleção de novos modelos nesta etapa.

## Recomendação

Priorizar **distorção idade-série e taxas de rendimento de 2022, além do INSE municipal de 2021**, em blocos separados. O VAAT anterior à complementação de 2023 fica como experimento secundário. São dimensões socioeconômicas, de trajetória escolar e financiamento ausentes ou representadas apenas indiretamente no modelo atual. Aprovação, reprovação e abandono de 2022 devem ser comparados em um bloco próprio. Não usar simultaneamente as três taxas da mesma etapa: elas somam aproximadamente 100%.

Esses dados acrescentam contexto municipal. Não descrevem a família, o docente ou a trajetória do aluno individual. Todos os alunos do mesmo município continuarão com o mesmo contexto; o enriquecimento não resolve sozinho a ausência de variáveis individuais.

## Cobertura e associação observadas

Cobertura de alunos significa o número de alunos do treino cujo município tem indicador, sem pesos amostrais. As correlações usam municípios com o dado disponível, com o mesmo peso por município. O sinal positivo significa associação com maior proporção de não alfabetizados.

| Indicador | Municípios com dado | Alunos cobertos | Spearman com alvo | Correlação dos ranks dentro da UF |
|---|---:|---:|---:|---:|
| INSE médio municipal (2021) | 3,180 | 99,5% | -0.243 | -0.179 |
| INSE: níveis 1 e 2 (%) | 3,180 | 99,5% | +0.246 | +0.146 |
| Distorção idade-série: anos iniciais | 3,263 | 100,0% | +0.394 | +0.217 |
| Distorção idade-série: 2º ano | 3,261 | 100,0% | +0.196 | +0.135 |
| Aprovação: anos iniciais (2022) | 3,263 | 100,0% | -0.426 | -0.202 |
| Aprovação: 2º ano (2022) | 3,261 | 100,0% | -0.132 | -0.142 |
| Reprovação: anos iniciais (2022) | 3,263 | 100,0% | +0.401 | +0.184 |
| Reprovação: 2º ano (2022) | 3,261 | 100,0% | +0.041 | +0.115 |
| Abandono: anos iniciais (2022) | 3,263 | 100,0% | +0.432 | +0.237 |
| Abandono: 2º ano (2022) | 3,261 | 100,0% | +0.326 | +0.175 |
| VAAT anterior à complementação (2023) | 3,229 | 98,9% | -0.170 | -0.053 |
| VAAT após complementação (2023) | 3,229 | 98,9% | -0.183 | -0.069 |
| Complementação VAAT total (2023) | 3,229 | 98,9% | +0.209 | +0.026 |
| Recebe complementação VAAT (2023) | 3,229 | 98,9% | +0.209 | +0.004 |
| PNAD: renda domiciliar por pessoa, UF | 3,267 | 100,0% | -0.171 | sem variação dentro da UF |

O último coeficiente remove a média de cada UF dos ranks globais de indicador e alvo e calcula a correlação dos resíduos. É um diagnóstico descritivo de associação dentro dos estados, sem controle por todas as demais variáveis. Não demonstra causalidade, estabilidade ou ganho preditivo. Amostras diferem quando há ausência de dados. Correlações agregadas não são desempenho de classificação individual.

O bloco combinado de INSE, distorção e abandono nos anos iniciais tem dados completos para **3.180 municípios e 963.719 alunos (99,46% do treino), nas 25 UFs**. A tabela candidata reúne 5.568 municípios das fontes públicas, mas as estatísticas de associação e cobertura deste relatório se restringem ao treino.

Os sinais mais fortes dentro das UFs foram abandono nos anos iniciais (+0,237), distorção nos anos iniciais (+0,217) e aprovação nos anos iniciais (−0,202). INSE médio teve −0,179. O VAAT anterior teve apenas −0,053, e o recebimento de complementação ficou próximo de zero (+0,004). O INSE também se relaciona com PIB por habitante (Spearman +0,737), portanto parte de sua informação pode já estar representada.

Os detalhes incluem mínimo, percentis 1 e 99, mediana, máximo, redundância com as seis variáveis atuais e cobertura por UF nos arquivos JSON. Extremos legítimos foram mantidos. Eventual transformação logarítmica, imputação ou corte deve ser ajustado somente nos folds de treino.

## O que foi extraído e como cruzar

**INSE 2021 — prioridade alta.** Seleção de rede municipal (`TP_TIPO_REDE=3`) e localização total (`TP_LOCALIZACAO=0`), com participantes INSE > 0. Média ponderada oficial dos participantes e soma das porcentagens dos níveis 1 e 2. INSE igual a zero com zero participantes foi tratado como ausência, não como vulnerabilidade extrema. A quantidade de participantes acompanha a tabela como metadado de suporte, não como indicador direto do nível socioeconômico. Não representa especificamente os alunos do 2º ano de 2024.

**Distorção idade-série 2022 — prioridade alta.** Arquivo municipal oficial, dependência Municipal, localização Total. Anos iniciais e 2º ano. São percentuais anteriores à avaliação, não a idade ou o histórico dos próprios alunos de 2024. As duas medidas devem ser comparadas como alternativas se houver redundância.

**FUNDEB/VAAT 2023 — prioridade intermediária.** Anexo III da Portaria de 28/08/2023. Extraídos código IBGE, VAAT anterior e posterior à complementação, valor total da complementação e indicador de recebimento. VAAT anterior mede disponibilidade de recursos por aluno na definição legal do financiamento; não é gasto executado e não se restringe ao 2º ano. Complementação é compensatória: eventual associação com vulnerabilidade não mede o efeito do financiamento. O VAAT posterior tem piso comum entre beneficiários e pode perder discriminação. Preferir o valor anterior no primeiro experimento.

Traços explicitamente presentes nas colunas financeiras do anexo foram convertidos em zero para complementação. Municípios ausentes do anexo ficaram ausentes; não foram classificados como não beneficiários. Extração textual verifica unicidade de códigos e VAAT posterior >= anterior. Como a fonte é PDF, uma revisão adicional contra totais oficiais será necessária antes de incorporar valores financeiros em produção.

**Aprovação, reprovação e abandono 2022 — prioridade alta para experimento.** Arquivo municipal oficial, rede Municipal e localização Total, para anos iniciais e 2º ano. Códigos 1, 2 e 3 do arquivo correspondem a aprovação, reprovação e abandono, conforme cabeçalho. Podem capturar trajetórias anteriores, mas também políticas de progressão e o contexto de recuperação da pandemia. Taxa de aprovação alta não implica alfabetização alta.

**PNAD Contínua 2022 — prioridade baixa no modelo atual.** Rendimento domiciliar per capita nominal mensal por UF, publicação de 24/02/2023. Cruzamento por sigla da UF. O valor de Roraima usado é a estimativa estatística de R$ 1.242 da tabela, não o valor judicial de R$ 1.166 mencionado na nota para finalidade específica. Não estimar renda municipal ou familiar com esses dados. Escolaridade adulta, pobreza e desocupação por UF são candidatos conceituais adicionais, ainda não extraídos. Com uma única referência temporal, variáveis constantes por UF são representáveis pelas dummies de UF já usadas na regressão logística; não adicionam informação territorial independente. Podem ser úteis em outra formulação temporal ou como alternativa explicativa à UF.

Todos os cruzamentos municipais usam código IBGE de sete dígitos e validação 1:1 após os filtros. Não se usou nome para vínculo. Os indicadores oficiais municipais evitam o problema do cruzamento escolar sem correspondência encontrado anteriormente.

## Disponibilidade temporal e versões

Adotado corte conservador de publicação até 31/12/2023, anterior à avaliação de 2024. Ano de referência e ano de divulgação são campos diferentes.

| Fonte | Referência | Evidência de publicação utilizada |
|---|---|---|
| INSE | 2021 | Página publicada em 27/03/2023; arquivo municipal atualizado em 10/05/2023 |
| Distorção idade-série | 2022 | Página oficial publicada em 08/02/2023 às 12h16 |
| Rendimento escolar | 2022 | Página publicada e atualizada em 19/05/2023 |
| FUNDEB VAAT | 2023 | Publicação da Portaria de 28/08/2023 |
| PNAD renda | 2022 | Documento datado de 24/02/2023 |

Os arquivos foram baixados em 2026 e têm hashes registrados. Datas de páginas e documentos sustentam a disponibilidade das séries, mas não provam que os bytes atuais sejam idênticos a uma cópia arquivada de 2023. Para reprodução histórica estrita, preservar a edição oficial e conferir revisões. Não utilizar retificações do FUNDEB 2023 publicadas em 2026 como se fossem conhecidas em 2023.

## Fontes adicionais identificadas, sem cobertura medida

- **Adequação da formação docente, 2022:** arquivo municipal oficial, publicado em 08/02/2023. Priorizar percentual de docências dos anos iniciais com formação adequada (grupo 1), após confirmar o dicionário. O servidor encerrou as tentativas de download; nenhuma cobertura ou correlação foi atribuída. Formação adequada é diferente de apenas ter ensino superior, já representado no enriquecimento anterior.
- **Censo Escolar 2022:** infraestrutura, internet pedagógica, bibliotecas, saneamento escolar, tempo integral, oferta de educação infantil e transporte. Agregar escolas municipais por código de município, com denominador explícito (escolas ou matrículas). Requer extração própria; não houve medição nesta etapa. O identificador escolar da nossa base não tem vínculo oficial validado.
- **IBGE/Censo Demográfico:** saneamento, composição etária e escolaridade adulta municipal podem melhorar o contexto. Escolher edição efetivamente disponível antes do corte. Resultados temáticos do Censo 2022 divulgados em 2024/2025 não entram automaticamente só por terem referência 2022. Censo 2010 é alternativa histórica com defasagem relevante. Não houve extração dessas novas dimensões.
- **SIOPE/FUNDEB:** despesa educacional executada, proporção destinada a remuneração e receitas por matrícula da rede são candidatos futuros. Exigem conciliação de período, despesas e matrículas. Não dividir receita total pelo número de alunos avaliados do 2º ano, nem confundir previsão com execução.

## Próximo experimento proposto

1. Consolidar os indicadores candidatos numa nova tabela Gold municipal com fonte, unidade, referência, data de publicação, versão e situação do vínculo. Preservar a origem do alvo individual e a delimitação de cobertura da Gold da Fase 2. Os JSON desta exploração são tabelas candidatas, ainda não uma nova Gold oficial.
2. Fixar previamente os blocos: referência atual; referência + INSE; referência + distorção; referência + VAAT anterior; referência + combinação; rendimento como alternativa. Evitar crescimento irrestrito de combinações orientado por resultados.
3. Comparar por validação cruzada agrupada por município no treino, incluindo imputação, normalização e seleção dentro dos folds. Examinar AP, calibração, cobertura e comportamento por UF. O conjunto de validação já consultado pode acompanhar o desenvolvimento, mas não fornece uma nova confirmação independente.
4. O teste v1 já foi visto. Não reutilizá-lo para declarar ganho final de uma versão ajustada após a entrega. Para confirmação independente da evolução, obter nova safra temporal ou nova amostra externa não explorada. Na ausência dela, reportar o resultado como exploratório de validação cruzada.

## Fontes oficiais

- [INSE 2021](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico/2021)
- [Distorção idade-série 2022](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/taxas-de-distorcao-idade-serie/2022)
- [Rendimento escolar 2022](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/taxas-de-rendimento-escolar/2022)
- [FUNDEB 2023: publicações e revisões](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2023)
- [Anexo VAAT de 28/08/2023](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2023-1/AnexoIIIPortariaInterm.n3de28.08.2023.pdf/@@display-file/file)
- [PNAD: rendimento domiciliar per capita 2022](https://www.ibge.gov.br/biblioteca/visualizacao/periodicos/3100/rdpc_2022.pdf)
- [Adequação docente 2022](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/adequacao-da-formacao-docente/2022)
- [Censo Escolar 2022](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-escolar/resultados/2022)

## Arquivos

`contexto_municipal_candidato.json`: indicadores públicos extraídos, sem alvo ou identificação individual. `contexto_pnad_uf.json`: tabela por UF. `resultados_exploratorios.json`: cobertura, correlações, extremos e verificações. `cobertura_por_uf.json`: denominadores por estado e indicador, apenas no treino. `manifesto_fontes.json`: arquivos e hashes. As verificações confirmaram chaves únicas, taxas de rendimento somando 100%, consistência entre VAAT anterior e posterior e seis municípios conferidos contra o texto do PDF. São controles de extração, ainda sem conciliação integral de totais financeiros. A extração e a geração do relatório estão em `reproducao/`; devem ser copiados para a pasta work do workspace original e exigem os arquivos originais listados no manifesto e a base municipal v1. A versão entregue não foi alterada.
