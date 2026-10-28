# Aderência e adaptações

| Requisito | Evidência / limite |
|---|---|
| Classificar aluno alfabetizado/não alfabetizado | Rótulo individual representado por contagens e perda binária ponderada; preditores municipais não diferenciam indivíduos do mesmo município. |
| Usar Gold da Fase 2 | Reutilizada em auditoria, cobertura e descrição. Rótulos individuais recuperados da Bronze, pois não existem na Gold agregada. Adaptação explícita que o grupo deve revisar frente à interpretação do professor. |
| EDA, preparação e prevenção de leakage | Auditoria, EDA, features autorizadas e pipelines. |
| Otimização e validação | Comparação de seis configurações em três folds de municípios no treino; validação e teste separados. |
| Interpretabilidade | SHAP dos modelos logístico e boosting, coeficientes, aditividade verificada. |
| Perfis e análise estratégica | K-Means/PCA exploratórios; silhouette moderada/baixa; sem inferência causal. |
| Todas as abordagens ensinadas consideradas | Supervisionado e não supervisionado aplicados; séries temporais e reforço não aplicados por falta de histórico e de ações/recompensas. |
| Pipeline reproduzível e organização | CLI, dados agregados, requirements e testes de contrato/reprodução. |
| Git e colaboração | Histórico local iniciado nesta organização; remoto/PR e colaboração do grupo não simulados. |
| Vídeo executivo até 5 minutos | Roteiro e apoio visual prontos; gravação pendente. |

Não foi prometida alta precisão nem generalização temporal. O relatório explica o resultado modesto e o caminho de evolução. O PDF original contém identificação do aluno e não foi incluído no pacote de distribuição.

## Esclarecimento posterior do professor — 28/10/2026

Na resposta compartilhada pelo aluno, o professor confirmou a adequação da classificação individual com atributos municipais, a separação por município e o pré-processamento dentro dos folds. Não há desempenho mínimo informado. A interpretação é risco contextual. Foram acrescentadas comparações com prevalência e baseline por UF, sem alterar a origem documentada do alvo ou afirmar que a Gold individual já foi publicada em cloud.
