# Alfabetização no Brasil — relatório consolidado

Atualização de 28/10/2026 após orientação do professor. Este documento consolida a interpretação metodológica e os experimentos posteriores à entrega acadêmica v1. A v1 permanece congelada. O candidato enriquecido não substituiu o modelo final da v1.

## Resultado e decisão

O modelo estima o risco de não alfabetização associado ao contexto municipal de cada aluno. A granularidade do alvo é individual; os atributos disponíveis são municipais. Assim, alunos de um mesmo município recebem a mesma probabilidade. Essa abordagem foi considerada adequada pelo professor na resposta compartilhada pelo aluno, desde que suas motivações e limitações sejam documentadas. O professor também informou que não há desempenho mínimo e recomendou comparar AP com prevalência e baselines.

O candidato prioritário para evolução é a regressão logística com o bloco de rendimento escolar de 2022: reprovação e abandono nos anos iniciais e no 2º ano. Sua AP média foi 0,52735, frente a 0,51990 da referência e 0,51088 do baseline por UF. A combinação com distorção não acrescentou ganho na métrica principal. Não há confirmação independente de superioridade em uma nova safra.

## Comparação solicitada pelo professor

A classe positiva é **não alfabetizado**. No treino, são 393.076 alunos nessa classe, em 968.939 avaliações válidas, resultando em prevalência de **40,57%**. As contagens abaixo devem ser lidas no recorte de alunos elegíveis, sem pesos amostrais do INEP.

Todos os candidatos e baselines foram comparados nos mesmos três folds de municípios, estratificados por UF. Para cada fold, o baseline global recebe a prevalência dos municípios de ajuste. O baseline por UF recebe a prevalência estadual calculada apenas nos municípios de ajuste. Nenhum alvo do fold de avaliação é usado para criar suas previsões.

| Configuração | AP média dos folds | Δ AP versus global | Δ AP versus UF | Brier OOF |
|---|---:|---:|---:|---:|
| Probabilidade global | 0.40509 | +0.00000 | -0.10578 | 0.24114 |
| Probabilidade por UF | 0.51088 | +0.10578 | +0.00000 | 0.22938 |
| Logística de referência | 0.51990 | +0.11481 | +0.00903 | 0.22922 |
| Referência + distorção | 0.52590 | +0.12081 | +0.01502 | 0.22731 |
| Referência + rendimento | 0.52735 | +0.12226 | +0.01647 | 0.22756 |
| Referência + ambos | 0.52640 | +0.12131 | +0.01553 | 0.22741 |

A AP do score constante em cada fold é exatamente a prevalência observada naquele fold. A média dessas prevalências foi **0,40509**. Ela difere da prevalência geral do treino, **0,40568**, porque a média dos três folds dá o mesmo peso a cada fold, enquanto a taxa geral pondera a quantidade de alunos.

O candidato com rendimento supera o baseline global em **0,12226 ponto de AP** e o baseline por UF em **0,01647 ponto de AP**, na média dos folds. A razão entre sua AP e a do baseline global é 1,302. Essa razão não significa acurácia de 130%, precisão de 52,7% em um limiar ou melhoria garantida de resultados educacionais.

O baseline por UF já alcança boa parte da discriminação observada. Por isso, a comparação com ele é mais exigente e informativa que apenas comparar com a prevalência global. O acréscimo do rendimento à logística de referência é de 0,00744 na AP média, consistente nos três folds, mas modesto.

AP maior é melhor. Brier menor é melhor e mede o erro quadrático das probabilidades. AP é average precision, não a área trapezoidal da curva precisão–recall. As métricas OOF agrupadas são calculadas reunindo scores de ajustes distintos e não são iguais à média das métricas por fold. O baseline global varia ligeiramente entre folds; sua AP OOF agrupada pode, portanto, diferir da prevalência, embora dentro de cada fold ela seja exatamente igual. A comparação principal usa a média pareada nos mesmos folds.

## Estrutura, origem e alvo

O backup da Fase 2 contém 1.840.277 registros de alunos de 2024, da rede municipal e do 2º ano. A auditoria manteve 1.610.754 avaliações válidas em 5.450 municípios e 36.920 grupos escolares. Registros sem avaliação válida foram excluídos, em vez de tratados como não alfabetizados. O alvo foi recodificado como 1 − alfabetizado.

A Gold original contém agregados municipais e estaduais. Os resultados individuais foram recuperados da Bronze e passaram pelos filtros e validações da preparação analítica. Não se afirma que esses rótulos já existissem na Gold agregada. A rastreabilidade preserva essa adaptação. O enunciado da Fase 2 não fixa uma única granularidade para a Gold; a Fase 3 estabelece classificação por aluno e permite enriquecimento externo.

A tabela lógica individual possui chave pseudonimizada do aluno, grupo escolar pseudonimizado, código IBGE do município, ano, resultado e peso amostral de origem. O código municipal conecta os indicadores de contexto. O peso amostral é preservado como metadado, mas não foi empregado na função de perda ou nas métricas aqui reportadas.

Como o X é constante por município, os ajustes usam duas linhas por município, uma para cada classe, com pesos iguais às contagens correspondentes. Esse é um recurso computacional equivalente à classificação das observações individuais sob essas features. Não é regressão de taxa municipal e não cria informação individual nova. As contagens e proporções de alfabetização não entram como preditores.

## Contrato proposto para uma Gold individual

É possível manter os agregados da Fase 2 e acrescentar um dataset individual para modelagem, sem alterar o alvo ou reconstruir toda a arquitetura. A implementação atual já dispõe da tabela individual e do contexto em banco analítico local. Isso não representa publicação de uma nova Gold em cloud nem reexecução do pipeline da Fase 2.

| Grupo | Campos e regras |
|---|---|
| Chave | aluno_chave pseudonimizada; unicidade definida com a referência temporal |
| Referência | ano_avaliacao, id_municipio IBGE de sete dígitos e escola_grupo pseudonimizada |
| Alvo | alfabetizado em {0,1}; nao_alfabetizado derivado como 1 − alfabetizado |
| Elegibilidade | Somente avaliações que passam nos filtros de presença, preenchimento e resultado válido |
| Contexto atual | População/densidade 2022; PIB por habitante e composição econômica 2021; UF |
| Contexto candidato | Reprovação e abandono, anos iniciais e 2º ano, 2022 |
| Proveniência | Fonte, ano de referência, data de publicação, extração, edição e hash em manifesto |
| Divisão | Uma atribuição de conjunto e fold por município, controlada à parte dos preditores |

Os nomes finais das colunas, as unidades e a edição das fontes devem constar no dicionário. Fontes externas entram tratadas e validadas, com chave municipal única por recorte de ano, rede e localização. Ausência não vira zero automaticamente. Não incluir presença, proficiência, ranking ou resultado contemporâneo como atributos de entrada.

## Prevenção de vazamento e validação

A divisão fixa preserva todos os alunos de um município no mesmo conjunto: 968.939 alunos no treino, 320.639 na validação e 321.176 no teste. Nos experimentos posteriores usamos somente o treino. Os mesmos três folds municipais foram mantidos para todas as comparações.

Mediana, indicador de ausência, padronização e one-hot são ajustados apenas nos municípios de ajuste de cada fold. A escala considera municípios com peso igual; a função de perda considera contagens de alunos. O baseline por UF também é estimado só no fold de ajuste. Nenhum identificador ou contagem do alvo entra no vetor de preditores.

A referência e os enriquecimentos empregaram regressão logística L2, C=1, solver lbfgs, max_iter=3000, tol=1e-8 e semente 42. Não houve busca adicional de hiperparâmetros nesta etapa. Os três controles do experimento combinado reproduziram o experimento anterior. Todos os ajustes convergiram sem avisos.

Os indicadores externos são anteriores à avaliação de 2024 por referência e publicação documentada. Downloads atuais não garantem identidade com os bytes publicados em 2023; não se apresenta esta análise como backtest com snapshot histórico certificado.

## Experimentos e limites da evidência

INSE, distorção, rendimento, VAAT e renda estadual da PNAD foram testados separadamente. INSE oscilou e não melhorou a média. VAAT e PNAD não demonstraram ganho relevante na configuração testada. Rendimento e distorção melhoraram a referência nos três folds. A combinação atingiu AP média de 0,52640 e ficou abaixo do rendimento isolado em dois folds.

O candidato com rendimento melhorou a AP frente à referência em 21 das 25 UFs e piorou em quatro. Não há melhora uniforme. Distorção apresentou Brier e log loss ligeiramente melhores que rendimento, embora rendimento tenha maior AP média. A prioridade segue a métrica principal declarada, sem afirmar superioridade universal.

Os intervalos anteriores usam bootstrap municipal estratificado por UF com previsões OOF fixas. Não incluem refazer ajustes e escolhas de atributos; não corrigem comparações múltiplas. Não se deve tratar as rodadas sucessivas de desenvolvimento nos mesmos folds como confirmações independentes.

## Resultado histórico da v1

A v1, com a logística contextual anterior aos novos indicadores, foi avaliada uma vez no teste: **AP 0,53556**, ROC AUC 0,64336, precisão 0,58963 e recall 0,27115 no limiar comparativo 0,50. Esses números são históricos e pertencem a outro conjunto e configuração. Não representam o desempenho final do candidato com rendimento e não devem ser comparados diretamente com sua AP de CV para alegar melhora ou piora.

O teste v1 já foi observado. Uma versão escolhida após essas explorações requer nova safra temporal ou nova amostra externa para confirmação independente. Nenhuma nova previsão no teste foi calculada nesta consolidação. A entrega v1 permanece preservada.

## Insights e ações possíveis

| Evidência | Aplicação possível | Limite |
|---|---|---|
| Há diferenças territoriais capturadas pelo baseline por UF | Estruturar diagnósticos estaduais e comparar municípios dentro de cada UF | UF não identifica mecanismo causal |
| Rendimento anterior acrescentou discriminação | Usar reprovação e abandono como dimensões para investigação das redes | Não prova que reduzir esses indicadores cause a melhora prevista |
| Todos os alunos do município compartilham o score | Apoiar triagem de contextos municipais para análise humana | Não indicar uma criança específica para intervenção com base apenas nesse score |
| Taxas pequenas são instáveis em municípios com poucos alunos | Mostrar denominadores e considerar incerteza no acompanhamento | Evitar ordenações rígidas baseadas em diferenças pequenas |
| Combinar blocos não trouxe ganho adicional | Priorizar o bloco de rendimento no próximo candidato e conservar uma solução simples | Resultado restrito à configuração e à base observada |

Nenhum limiar operacional ou capacidade real de atendimento foi escolhido. Recomendações educacionais dependem de avaliação pedagógica local. Os scores são associações de contexto, sem causalidade e sem previsão temporal comprovada.

## Reprodução e arquivos

Na raiz do repositório, execute python -m src.evaluation.baselines --output work/baselines_novos, em ambiente com as dependências de requirements.txt. O módulo lê data/processed/dados_treino_oof.json, contendo agregados municipais, contagens e previsões OOF, e recalcula os dois baselines. Não carrega modelos, não acessa microdados individuais e não consulta validação ou teste. comparacao_baselines.json registra métricas por fold, resumo, prevalência e hash da entrada. metricas_baselines_por_uf.json registra os resultados por estado. O dataset distribuído não contém identificadores individuais ou escolares.

Os experimentos originais, a interpretação SHAP, os perfis exploratórios e a avaliação histórica permanecem documentados na entrega v1 e nos relatórios de validação cruzada e combinação. Esta atualização complementa essas evidências e não transforma os experimentos em um novo resultado final de teste.

## Conclusão para a entrega

A modelagem é aderente à orientação do professor: explicita a granularidade, separa municípios, ajusta transformações dentro dos folds, compara com baselines e documenta limitações. O desempenho mostra ganho frente à prevalência e um ganho menor frente à referência por UF. Não há requisito de desempenho mínimo, conforme orientação recebida.

A publicação inicial no repositório remoto foi realizada pelo autor e um PR de consolidação foi aberto. Antes da submissão continuam necessários a revisão do grupo, a gravação do vídeo executivo, a conclusão da revisão e integração do PR e a submissão no portal. A recomendação é apresentar a v1 como avaliação histórica congelada e os novos indicadores como evolução exploratória, distinguindo claramente as duas etapas.
