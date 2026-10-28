# Combinação de rendimento e distorção

27/10/2026. A combinação melhora a referência, mas não supera o rendimento isolado na métrica principal. Recomenda-se manter rendimento como primeiro candidato à evolução. Não houve substituição do modelo entregue.

Somente treino: 3.267 municípios, 968.939 alunos, 25 UFs. Mesmos três folds estratificados por UF e mesmos parâmetros de regressão logística. Cada município permanece inteiro em um fold. Mediana, indicadores de ausência, escala e one-hot são ajustados dentro de cada fold.

| Modelo | AP média folds | Δ AP média vs referência | AP OOF | Brier OOF | Log loss OOF |
| --- | --- | --- | --- | --- | --- |
| Referência atual | 0.51990 | +0.00000 | 0.51552 | 0.22922 | 0.64967 |
| + Distorção | 0.52590 | +0.00600 | 0.52514 | 0.22731 | 0.64544 |
| + Rendimento | 0.52735 | +0.00744 | 0.52570 | 0.22756 | 0.64614 |
| + Ambos | 0.52640 | +0.00650 | 0.52509 | 0.22741 | 0.64572 |

AP maior é melhor; Brier e log loss menores são melhores. A métrica principal pré-definida é a média simples da AP dos três folds. A AP OOF agrupada tem outro cálculo e pode ordenar configurações de maneira diferente. Não comparar estes valores diretamente com a AP do teste final.

## Ganho incremental da combinação

| Comparação | Δ AP média | Δ fold 0 | Δ fold 1 | Δ fold 2 | Δ AP OOF | IC 95% Δ AP OOF |
| --- | --- | --- | --- | --- | --- | --- |
| combinado menos rendimento | -0.00094 | +0.00032 | -0.00192 | -0.00122 | -0.00061 | [-0.0021, 0.00074] |
| combinado menos distorcao | +0.00051 | -0.00278 | +0.00300 | +0.00129 | -0.00005 | [-0.00265, 0.0021] |

A combinação ficou abaixo de rendimento em dois dos três folds e abaixo de distorção em um deles. Os intervalos incrementais incluem zero. Não há evidência de ganho ao juntar os dois. Isso é compatível com informação parcialmente sobreposta; não demonstra que um bloco seja inútil em outras famílias de modelos ou populações.

Os intervalos são bootstrap pareado de 500 reamostragens municipais estratificadas por UF, semente 42, com previsões OOF fixas. Referem-se ao delta de AP OOF, não ao delta de média dos folds. Não incluem refazer os ajustes nem a incerteza das escolhas anteriores. São condicionais e sem correção de comparações múltiplas.

## Preditores e cobertura

Referência: população e densidade de 2022, PIB por habitante e composição econômica de 2021, mais UF. Distorção: taxas dos anos iniciais e do 2º ano de 2022. Rendimento: reprovação e abandono nos anos iniciais e no 2º ano de 2022. Aprovação foi omitida por depender das outras duas taxas. Todos os dados de enriquecimento são anteriores ao alvo de alfabetização de 2024.

| Modelo | Municípios com bloco completo | Alunos com bloco completo | Cobertura alunos |
| --- | --- | --- | --- |
| Referência atual | 3267 | 968939 | 100.000% |
| + Distorção | 3261 | 968813 | 99.987% |
| + Rendimento | 3261 | 968813 | 99.987% |
| + Ambos | 3261 | 968813 | 99.987% |

A avaliação preserva todos os alunos do treino, incluindo municípios com dados ausentes, tratados no pré-processamento. As perdas e métricas usam contagens de alunos, não os pesos amostrais do INEP. Todos os alunos de um município continuam recebendo o mesmo score de contexto.

## Resultados por UF

| Combinação versus | UFs com melhora AP | UFs com piora AP | Empates |
| --- | --- | --- | --- |
| Referência atual | 21 | 4 | 0 |
| + Rendimento | 14 | 11 | 0 |
| + Distorção | 13 | 12 | 0 |

As métricas completas por estado e a calibração por faixas de 0,10 acompanham o relatório em JSON. Os pequenos ganhos agregados não garantem melhora em cada UF. A distorção isolada teve o menor Brier e log loss; rendimento isolado teve a maior AP média. O objetivo pré-definido de AP favorece rendimento.

## Verificações e decisão

Os três controles reproduziram os scores do experimento anterior. Todos os ajustes convergiram sem avisos; contagens e métricas OOF foram reconciliadas. Os arquivos de entrada e o protocolo de teste mantiveram seus hashes. Nenhuma nova previsão na validação externa ou no teste foi produzida. Não houve escolha de limiar ou capacidade operacional, nem treino de um novo modelo final.

Priorizar rendimento isolado como candidato e conservar distorção como alternativa. A combinação não justifica acrescentar preditores neste experimento. Para afirmar ganho final sobre a versão v1, será necessária uma nova safra temporal ou amostra independente; o teste v1 já foi observado. Estes resultados são de desenvolvimento por validação cruzada.

## Reprodução

protocolo.json registra entradas, hashes, variáveis e parâmetros antes dos ajustes. resultados.json contém métricas por fold. comparacoes_pareadas.json contém os contrastes incrementais. previsoes_oof_municipais.json permite auditoria. Scripts em reproducao devem ser copiados para work do workspace original.
