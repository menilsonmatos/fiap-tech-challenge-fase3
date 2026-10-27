# Roteiro do vídeo executivo — até 5 minutos

Duração planejada: aproximadamente 4min40s, ajustável ao ritmo da apresentação. Confirmar integrantes antes da gravação. O material visual está em `apoio_visual.html`. Não exibir microdados, identificadores individuais ou arquivos privados.

## 0:00–0:40 | Problema e objetivo

A alfabetização é central para o desenvolvimento educacional. Nosso projeto investigou se dados territoriais, econômicos e educacionais anteriores à avaliação permitem antecipar o rótulo de alfabetização de um aluno. O objetivo é apoiar a compreensão do problema e o planejamento educacional, sem substituir a avaliação pedagógica. Definimos como classe de interesse o aluno não alfabetizado, para medir diretamente quantos casos o modelo consegue identificar.

## 0:40–1:25 | Dados e cuidados

Partimos dos dados preservados na Fase 2 e mantivemos 1,61 milhão de avaliações válidas de 2024. Excluímos registros sem avaliação válida e variáveis que revelam a própria resposta, como a proficiência do exame. Integramos dados de referência 2021 e 2022 do IBGE e indicadores do INEP. O vínculo por escola não foi possível; usamos indicadores agregados por município e documentamos essa limitação. A Gold anterior foi utilizada na auditoria e análise de cobertura; os rótulos individuais vieram da Bronze.

## 1:25–2:10 | Método

Separamos municípios inteiros entre treino, validação e teste, evitando que o mesmo contexto aparecesse dos dois lados. Ajustamos o pré-processamento somente no treino. Comparamos referências simples, regressão logística, árvore, Random Forest e boosting. Os modelos mais complexos foram avaliados em três folds de municípios dentro do treino. Também exploramos perfis municipais com K-Means e PCA. Como só temos um ano observado e não há ações ou recompensas, não aplicamos séries temporais nem aprendizado por reforço.

## 2:10–3:00 | Resultados

Os modelos mais complexos e os novos indicadores não demonstraram melhora clara sobre a logística simples. Por isso, mantivemos a logística como referência e só então abrimos o teste reservado. Em 321 mil alunos de municípios separados do treino, ela alcançou average precision de 0,536. No limiar de comparação de 0,50, a precisão foi 58,96% e o recall foi 27,12%. Isso significa que identificou pouco mais de um quarto dos não alfabetizados: um resultado insuficiente para diagnóstico individual. Não reajustamos o modelo depois de observar o teste.

## 3:00–3:50 | Interpretação e valor estratégico

O SHAP mostrou que o contexto estadual tem grande influência nas previsões. Essa é uma associação do modelo, não uma explicação causal da alfabetização. As análises também mostraram diferenças importantes de cobertura e municípios com poucas avaliações. Aumentar o número de alertas pode ampliar o recall, mas gera mais falsos positivos. Apresentamos esses cenários apenas como hipóteses acadêmicas, sem escolher uma capacidade real de atendimento. O principal valor desta versão é tornar esses limites e compromissos visíveis para uma decisão responsável sobre os dados necessários.

## 3:50–4:40 | Limites e próximos passos

Hoje, todos os alunos de um município recebem a mesma previsão, porque faltam atributos que os diferenciem. Para evoluir, precisamos de uma chave escolar legítima ou de atributos individuais autorizados e anteriores à avaliação, além de outros anos observados. Entregamos uma pipeline reproduzível, comparações, interpretação, auditoria e avaliação final preservada. A conclusão não é que o problema foi resolvido, mas que identificamos de forma verificável o que os dados atuais conseguem e não conseguem sustentar. Essa base técnica orienta a próxima versão do projeto.
