# Auditoria dos dados da Fase 2

Data: 27/10/2026. Prazo do projeto informado pelo aluno: 03/11/2026.

## Parecer

Há microdados individuais preservados na Bronze. Portanto, a previsão por aluno é tecnicamente investigável, embora a Gold existente seja municipal/estadual. A base ainda precisa de preparação e enriquecimento para oferecer uma previsão útil anterior à avaliação. Não foi treinado modelo nesta auditoria.

Corrige-se a avaliação preliminar de que só existiam dados municipais: o backup privado `C:\Users\menil\Downloads\fiap-backup-bruto-B9DePx.zip` contém `alunos.csv` com 12 colunas. A restrição estava nas saídas Gold, não na origem preservada.

## Escopo e evidências

Auditoria local do backup e do código da pipeline em `C:\Users\menil\Documents\Codex\2026-08-25\n\outputs\fiap-tech-challenge-fase2-local`. Não houve consulta externa, atualização dos dados ou alteração das fontes. Foram lidos todos os registros de alunos em blocos, conferidos os hashes dos sete extratos contra o manifesto e reconciliadas as saídas municipais e estaduais. A verificação de duplicidades de alunos usou hashes de linhas/chaves de 64 bits; não é uma comparação criptográfica de cada par de chaves.

SHA-256 do ZIP: `170114395cdcd07153fe844d337cc3c45ff8a54f0ea9a3210d64c44ebfe00077`.

Os sete hashes conferem. Os dois snapshots têm manifestos idênticos: são cópias da mesma extração, não dois períodos históricos. O manifesto identifica Base dos Dados/INEP, extração em 30/08/2026 e referência 2024. A autenticidade externa e possíveis revisões posteriores não foram verificadas.

## Volumes e qualidade

| Camada/recorte | Registros | Unidade |
|---|---:|---|
| Bronze alunos | 1.840.277 | registro de aluno/escola/município/ano |
| Avaliações válidas | 1.610.754 | aluno com presença e caderno preenchido |
| Sem avaliação válida | 229.523 | 228.686 ausentes e 837 presentes sem caderno preenchido |
| Classe não alfabetizado, avaliações válidas | 654.411 | 40,63% das avaliações válidas |
| Classe alfabetizado, avaliações válidas | 956.343 | 59,37% das avaliações válidas |
| Fonte municipal | 5.448 | município em 2024 |
| Silver / Gold ranking | 5.232 | município em 2024 |
| Gold por UF | 24 | UF em 2024 |
| Alunos válidos cobertos pela Gold | 1.568.597 | alunos dos municípios aprovados |

Não foram detectadas chaves de aluno duplicadas, linhas integralmente duplicadas ou rótulos conflitantes por chave. Nenhuma avaliação válida tem identificadores vazios. Proficiência e peso têm 229.523 valores vazios, correspondentes às avaliações inválidas; não há falhas de conversão numérica nessas duas colunas.

Na Silver e nas duas Gold não foram encontrados campos vazios ou chaves duplicadas. O ranking é consecutivo, ordenado pela prioridade e cobre os mesmos municípios da Silver. Prioridade = meta − resultado; gap = resultado − meta. As contagens de alunos conferem por município, e os totais, contagens municipais e médias de alfabetização ponderadas conferem nas 24 UFs, com tolerância de 0,011 ponto percentual para arredondamento.

## Achados que alteram a modelagem

### 1. Rótulo inválido fora do recorte elegível

Todos os 229.523 registros sem avaliação válida trazem `alfabetizado=0`. Não devem ser tratados automaticamente como não alfabetizados. O filtro inicial deve exigir `presenca=1`, `preenchimento_caderno=1` e rótulo em {0,1}. Presença e preenchimento servem ao filtro, não como preditores da classe neste recorte.

### 2. Proficiência revela o alvo

Nas avaliações válidas, os não alfabetizados têm proficiência de 594,2 a 742,9996427; os alfabetizados, de 743 a 900,89. Portanto, `proficiencia >= 743` reproduz perfeitamente o rótulo observado neste arquivo. Isso é evidência empírica do backup, não confirmação externa da regra oficial. Excluir proficiência dos preditores para uma previsão anterior ao exame.

### 3. Agregados do mesmo exame também exigem restrição

Taxas de alfabetização municipais/estaduais de 2024 usam resultados contemporâneos ao alvo. Não são entradas adequadas para prever o resultado antes de sua divulgação. `atingiu_meta`, `gap_meta_pp`, `prioridade` e `ranking_vulnerabilidade` derivam desses resultados e devem permanecer nas análises descritivas. Um alvo municipal definido por atingir a meta seria trivialmente reconstruído se resultado e meta do mesmo período entrassem como features.

### 4. Poucos atributos individuais anteriores ao exame

As 12 colunas são: ano, município, escola, aluno, caderno, série, rede, presença, preenchimento, alfabetizado, proficiência e peso. Ano=2024, série=2 e rede=3 são constantes. Não existem idade, sexo, raça/cor, renda familiar ou histórico escolar nesses extratos. IDs são chaves de integração e agrupamento, não medidas numéricas de capacidade do aluno. Caderno e peso precisam de dicionário e análise de disponibilidade; não incluí-los automaticamente como preditores. O peso amostral deve ser avaliado para métricas/estimativas, sem assumir que a contagem simples reproduz o indicador oficial.

### 5. Perda de cobertura na integração

216 dos 5.448 municípios de entrada foram excluídos (3,96%): 96 sem linha de meta e 120 com meta de 2024 vazia. Não imputar essas metas automaticamente. Há 5.450 municípios com ao menos uma avaliação válida nos microdados, dos quais dois não constam na fonte municipal. Uma junção com a Gold conserva 1.568.597 avaliações válidas e deixa 42.157 fora; registrar essa perda e comparar os perfis antes de decidir o recorte final.

A Gold cobre 24 UFs, sem AC, DF e RR. Isso descreve o recorte disponível; não prova ausência de alunos nessas unidades nem cobertura nacional. As médias por UF são ponderadas por número de avaliados dos municípios aprovados, não pelos pesos amostrais individuais, e não devem ser apresentadas como reprodução do ICA oficial.

### 6. Só existe um ano observado

Os registros são de 2024. Colunas de metas para 2025–2030 são metas, não resultados observados. Os snapshots e eventos simulados de streaming não criam histórico temporal. Esta base isolada não sustenta ARIMA/SARIMA, backtest entre anos nem comprovação de previsão futura. Também não contém ações, recompensas ou transições suficientes para avaliar uma política de aprendizado por reforço.

## Encaminhamento para a Fase 3

1. Construir uma tabela analítica individual privada com o filtro de elegibilidade, aproveitando os microdados Bronze e documentando como ela se relaciona à Gold da Fase 2. A Gold atual sozinha não contém o alvo individual exigido.
2. Integrar atributos educacionais, territoriais e socioeconômicos com referência anterior ao exame e data de disponibilidade documentada. Evitar taxa do mesmo exame e derivados do alvo.
3. Definir o cenário de uso: generalização para novas escolas/municípios em 2024 ou previsão de anos futuros. Para o primeiro, separar grupos escolares ou municipais entre treino/validação/teste; para o segundo, obter novos anos observados e validar cronologicamente.
4. Comparar uma referência simples e classificadores ensinados, com pré-processamento e seleção ajustados somente no treino. Reportar recall, precisão, F1, matriz de confusão e curvas adequadas ao desbalanceamento, além do recorte e da incerteza por grupos.
5. Usar agrupamento municipal como análise complementar, com indicadores contextuais e avaliação da estabilidade dos grupos. Interpretar SHAP como associação do modelo, sem alegar causalidade.
6. Justificar a ausência de séries temporais e reforço se não forem obtidos os dados necessários. Não produzir histórico artificial para aplicar essas técnicas.

O próximo passo concreto é preparar a tabela analítica individual e selecionar fontes contextuais anteriores a 2024. Os dados atuais permitem investigar classificação individual, mas ainda não demonstram capacidade preditiva útil ou generalização temporal.

## Artefatos de auditoria

`auditoria-fase2-resultados.json` guarda métricas agregadas, esquemas, verificações de integridade e reconciliação. O script de reprodução está em `work/audit_fase2.py`. Nenhum microdado individual foi incluído nos entregáveis da auditoria.
