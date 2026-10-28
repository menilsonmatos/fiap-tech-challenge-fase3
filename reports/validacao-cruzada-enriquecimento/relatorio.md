# Validação cruzada dos blocos de enriquecimento

27/10/2026. Rendimento escolar e distorção idade-série produziram ganhos modestos e consistentes nos três folds da regressão logística. INSE não melhorou a média; VAAT e PNAD ficaram próximos da referência. Estes resultados orientam o próximo experimento e não confirmam desempenho em uma nova população.

## Comparação principal

3.267 municípios, 968.939 alunos e 25 UFs, somente do treino. Cada linha adiciona um único bloco à referência atual. AP maior é melhor; Brier e log loss menores são melhores. A decisão pré-definida usa a média simples da AP dos três folds.

| Modelo | AP média folds | Δ AP média | AP OOF agrupada | Brier OOF | Log loss OOF |
| --- | --- | --- | --- | --- | --- |
| Referência atual | 0.51990 | +0.00000 | 0.51552 | 0.22922 | 0.64967 |
| + INSE 2021 | 0.51850 | -0.00140 | 0.50505 | 0.22989 | 0.65097 |
| + Distorção idade-série 2022 | 0.52590 | +0.00600 | 0.52514 | 0.22731 | 0.64544 |
| + Rendimento escolar 2022 | 0.52735 | +0.00744 | 0.52570 | 0.22756 | 0.64614 |
| + FUNDEB / VAAT 2023 | 0.51908 | -0.00082 | 0.51550 | 0.22923 | 0.64966 |
| + PNAD / renda UF 2022 | 0.51991 | +0.00001 | 0.51552 | 0.22922 | 0.64967 |

A média das APs dos folds difere da AP calculada ao reunir as previsões OOF. AP não é uma métrica aditiva e scores gerados por ajustes distintos podem ter escalas diferentes. Não comparar estes números diretamente com a AP do teste v1.

## Consistência entre folds

| Modelo | AP fold 0 | AP fold 1 | AP fold 2 |
| --- | --- | --- | --- |
| Referência atual | 0.51044 | 0.51303 | 0.53624 |
| + INSE 2021 | 0.49215 | 0.51885 | 0.54451 |
| + Distorção idade-série 2022 | 0.51731 | 0.52000 | 0.54038 |
| + Rendimento escolar 2022 | 0.51421 | 0.52493 | 0.54290 |
| + FUNDEB / VAAT 2023 | 0.51061 | 0.51347 | 0.53316 |
| + PNAD / renda UF 2022 | 0.51044 | 0.51304 | 0.53625 |

O rendimento aumentou a AP em +0,00377, +0,01190 e +0,00666. A distorção aumentou em +0,00687, +0,00697 e +0,00415. O INSE perdeu 0,01829 no primeiro fold, apesar de melhorar nos outros dois. A associação descritiva encontrada na exploratória, portanto, não garantiu ganho preditivo.

## O que foi testado

Referência: seis variáveis municipais de população, densidade, PIB por habitante e composição econômica, mais one-hot de UF. Mesma regressão logística L2, C=1, solver lbfgs, max_iter=3000, tol=1e-8, semente 42. Não houve busca de hiperparâmetros ou combinação de blocos.

| Bloco | Variáveis adicionais |
| --- | --- |
| INSE | Média municipal e percentual nos níveis 1 e 2, 2021 |
| Distorção | Percentuais nos anos iniciais e no 2º ano, 2022 |
| Rendimento | Reprovação e abandono nos anos iniciais e no 2º ano, 2022 |
| FUNDEB | VAAT anterior à complementação, publicação de 28/08/2023 |
| PNAD | Renda domiciliar per capita nominal por UF, 2022 |

Aprovação foi omitida porque é determinada por reprovação e abandono, cujas taxas somam 100% com ela. O bloco FUNDEB testou uma medida de recursos por aluno; o resultado não descarta outras variáveis de financiamento. A PNAD fornece uma variável constante por UF, já representável pelas dummies do estado. Sua diferença residual é desprezível e pode decorrer da regularização e do ajuste numérico.

## Cobertura

| Bloco | Municípios com bloco completo | Alunos com bloco completo | Cobertura de alunos |
| --- | --- | --- | --- |
| Referência atual | 3267 | 968939 | 100.00% |
| + INSE 2021 | 3180 | 963719 | 99.46% |
| + Distorção idade-série 2022 | 3261 | 968813 | 99.99% |
| + Rendimento escolar 2022 | 3261 | 968813 | 99.99% |
| + FUNDEB / VAAT 2023 | 3229 | 958169 | 98.89% |
| + PNAD / renda UF 2022 | 3267 | 968939 | 100.00% |

Todos os blocos foram avaliados nos mesmos alunos, sem excluir municípios com indicadores ausentes. A mediana e os indicadores de ausência foram ajustados apenas nos folds de ajuste. O bloco completo de INSE cobre 99,46% dos alunos; FUNDEB cobre 98,89%. Esses percentuais não são taxas de cobertura da população nacional.

## Incerteza condicional

| Bloco | Δ AP OOF agrupada | Intervalo percentil 95% |
| --- | --- | --- |
| + INSE 2021 | -0.01047 | [-0.02297; +0.00680] |
| + Distorção idade-série 2022 | +0.00963 | [+0.00118; +0.01847] |
| + Rendimento escolar 2022 | +0.01018 | [+0.00273; +0.01781] |
| + FUNDEB / VAAT 2023 | -0.00001 | [-0.00164; +0.00126] |
| + PNAD / renda UF 2022 | +0.00000 | [-0.00000; +0.00001] |

Bootstrap pareado de 500 reamostragens de municípios dentro das UFs, semente 42, mantendo as previsões OOF fixas. Estes intervalos se referem à diferença de AP OOF agrupada, não à diferença de médias de AP dos folds. Não incluem refazer os ajustes, escolher variáveis ou selecionar blocos. Não foram corrigidos por comparações múltiplas e não devem ser tratados como confirmação estatística independente.

## Variação por UF

| Bloco | UFs com Δ AP > 0 | UFs com Δ AP < 0 | Menor Δ AP | Maior Δ AP |
| --- | --- | --- | --- | --- |
| + INSE 2021 | 17 | 8 | -0.0431 | +0.0484 |
| + Distorção idade-série 2022 | 21 | 4 | -0.0070 | +0.0391 |
| + Rendimento escolar 2022 | 21 | 4 | -0.0163 | +0.0547 |
| + FUNDEB / VAAT 2023 | 13 | 11 | -0.0151 | +0.0081 |
| + PNAD / renda UF 2022 | 3 | 2 | -0.0000 | +0.0000 |

Melhora agregada não significa melhora em todas as UFs. AP depende da prevalência do alvo, e estados pequenos têm estimativas instáveis. As métricas completas estão em metricas_por_uf.json. A calibração por faixas fixas de 0,10 está em calibracao.json; o Brier resume erro probabilístico, sem comprovar calibração perfeita.

## Protocolo e verificações

Foram reutilizados os três folds anteriores, construídos sobre municípios únicos e estratificados por UF. Alunos do mesmo município permaneceram juntos. Mediana, escala e codificação de UF foram ajustadas somente nos municípios de ajuste de cada fold. A função de perda e as métricas usam contagens de alunos por classe, sem pesos amostrais do INEP. Duas linhas ponderadas por município preservam o objetivo de classificação porque seus preditores são constantes dentro do município.

Todos os ajustes convergiram. Conferidos: uma previsão OOF por município/bloco, reconciliação das contagens por fold e UF, calibração e equivalência das métricas ponderadas com expansão individual em uma amostra determinística de 20 municípios. Os hashes das entradas e do protocolo de teste foram conferidos antes e depois. Não houve novas previsões na validação externa ou no teste; a entrega v1 não foi alterada.

## Recomendação

Priorizar rendimento escolar como primeiro candidato, com distorção idade-série como alternativa de resultado próximo. Ambos também reduziram Brier e log loss em relação à referência. Não há evidência para afirmar que rendimento é superior à distorção. O próximo experimento pode avaliar a combinação pré-definida dos dois, ainda no treino. Manter INSE, VAAT e PNAD fora da primeira evolução, na configuração testada.

O teste v1 já foi consultado anteriormente. Uma versão escolhida após estes experimentos precisará de uma nova safra ou amostra externa para confirmação independente. Sem ela, os ganhos devem ser apresentados como exploratórios. Os indicadores continuam municipais e não diferenciam alunos do mesmo município.

## Reprodução

protocolo.json fixa colunas, parâmetros, folds e hashes. resultados.json contém métricas por fold e resumo. previsoes_oof_municipais.json contém scores agregados para auditoria. Os scripts em reproducao devem ser copiados para work do workspace original, mantendo as entradas nos caminhos registrados. Dependências são as do ambiente já usado no projeto. Não foram gerados modelos finais nesta etapa.
