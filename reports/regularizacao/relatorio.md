# Comparação curta de regularização

Somente treino: 3.267 municípios, 968.939 alunos e três folds fixos. Regularização L2; menor C implica penalização mais forte. A AP média dos folds é a métrica principal.

| Bloco | C | AP média | Desvio folds | Delta AP vs C=1 | Brier médio | Gap AP ajuste-holdout |
|---|---:|---:|---:|---:|---:|---:|
| referencia | 0.01 | 0.5200306 | 0.0145684 | +0.0001273 | 0.2284354 | 0.0146352 |
| referencia | 0.1 | 0.5197889 | 0.0143973 | -0.0001144 | 0.2286078 | 0.0149013 |
| referencia | 1 | 0.5199033 | 0.0142040 | +0.0000000 | 0.2286284 | 0.0147765 |
| referencia | 10 | 0.5198896 | 0.0141785 | -0.0000137 | 0.2286305 | 0.0147957 |
| rendimento | 0.01 | 0.5276477 | 0.0151872 | +0.0003013 | 0.2268998 | 0.0136326 |
| rendimento | 0.1 | 0.5273749 | 0.0145900 | +0.0000286 | 0.2270458 | 0.0139778 |
| rendimento | 1 | 0.5273463 | 0.0144934 | +0.0000000 | 0.2270647 | 0.0140237 |
| rendimento | 10 | 0.5273829 | 0.0145387 | +0.0000365 | 0.2270666 | 0.0139849 |

## Interpretação

As contagens de alunos foram mantidas como pesos de frequência; o valor de C não deve ser comparado diretamente com outro experimento que normalize esses pesos.

A diferença entre ajuste e holdout é apenas um diagnóstico de generalização. Não é uma curva de aprendizagem, e estas três partições não são repetições independentes.

O melhor C em cada bloco foi escolhido nesta mesma CV e permanece uma escolha exploratória. Não se deve tratar pequenas diferenças como evidência de superioridade populacional.

Escolhas exploratórias por AP: {'referencia': 0.01, 'rendimento': 0.01}. Os controles C=1 reproduzem a análise anterior.

O teste e a validação externa não receberam novas previsões. Nenhum modelo final foi reajustado ou substituído. Uma nova amostra ou safra é necessária para confirmação independente.

## Resultado observado

referencia: o melhor C por AP média foi 0.01, com ganho de +0.0001273. Melhorou em 2/3 folds. A diferença de AP OOF agrupada foi -0.0001083.
rendimento: o melhor C por AP média foi 0.01, com ganho de +0.0003013. Melhorou em 2/3 folds. A diferença de AP OOF agrupada foi -0.0000067.

Os ganhos de AP média são pequenos frente à variação entre folds. A AP OOF agrupada do candidato com rendimento não melhorou com C=0,01, apesar da média dos folds maior. A comparação não sustenta uma alegação de superioridade populacional. A configuração e o artefato final C=1 da v1 foram preservados.
