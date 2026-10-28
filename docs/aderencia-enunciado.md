# Aderência e adaptações

| Requisito | Evidência / limite |
|---|---|
| Classificar aluno alfabetizado/não alfabetizado | Rótulo individual representado por contagens e perda binária ponderada; preditores municipais não diferenciam indivíduos do mesmo município. |
| Usar Gold da Fase 2 | Reutilizada em auditoria, cobertura e descrição. Rótulos individuais recuperados da Bronze, pois não existem na Gold agregada. Adaptação explícita, documentada na descrição da base e na rastreabilidade. |
| EDA, preparação e prevenção de leakage | Auditoria, EDA, features autorizadas e pipelines. |
| Otimização e validação | Comparação de seis configurações em três folds de municípios no treino; validação e teste separados. |
| Interpretabilidade | SHAP dos modelos logístico e boosting, coeficientes, aditividade verificada. |
| Perfis e análise estratégica | K-Means/PCA exploratórios; silhouette moderada/baixa; sem inferência causal. |
| Todas as abordagens ensinadas consideradas | Supervisionado e não supervisionado aplicados; séries temporais e reforço não aplicados por falta de histórico e de ações/recompensas. |
| Pipeline reproduzível e organização | CLI, dados agregados, requirements e testes de contrato/reprodução. |
| Git e colaboração | Histórico local iniciado nesta organização; remoto/PR e colaboração do grupo não simulados. |

Não foi prometida alta precisão nem generalização temporal. O relatório explica o resultado modesto e o caminho de evolução. O PDF original contém identificação do aluno e não foi incluído no pacote de distribuição.
