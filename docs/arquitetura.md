# Arquitetura da versão acadêmica

```mermaid
flowchart LR
  A[Bronze Fase 2: avaliações válidas] --> C[Tabela individual privada]
  B[Gold Fase 2] --> D[Auditoria e análises de cobertura]
  E[IBGE 2021/2022 e INEP 2022] --> C
  C --> F[Contagens por município e contexto]
  F --> G[Divisão municipal fixa]
  G --> H[Pré-processamento + modelos no treino]
  H --> I[CV e validação]
  I --> J[Decisão fixada]
  J --> K[Teste único]
  K --> L[Relatório e vídeo]
```

SQLite foi suporte local de preparação e auditoria; não é uma exigência da entrega nem define uma arquitetura cloud. Esta distribuição usa dados agregados em JSON e artefatos Scikit-learn para reproduzir os experimentos. A compressão é válida apenas enquanto as features forem constantes por município; atributos individuais futuros exigirão alterar a unidade de processamento e o contrato de dados.
