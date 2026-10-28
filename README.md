# Tech Challenge — Fase 3: Alfabetização no Brasil

Consolidação para publicação, 28/10/2026. O relatório principal está em **[reports/relatorio_final.pdf](reports/relatorio_final.pdf)**. A versão acadêmica v1 e sua avaliação de teste permanecem congeladas na tag **v1.0.0** e em `ABRIR_RELATORIO.html`.

## Resultado atualizado e limites

Nos mesmos três folds por município do treino, a AP média foi 0,40509 para a probabilidade global, 0,51088 para a probabilidade por UF, 0,51990 para a logística de referência e 0,52735 com rendimento escolar de 2022. O ganho além da informação estadual é modesto. A combinação de rendimento e distorção não superou rendimento isolado na métrica principal.

Estes resultados são de desenvolvimento por validação cruzada, não um novo teste final. O candidato enriquecido não substituiu o modelo entregue na v1. Todos os alunos de um município recebem o mesmo score, interpretado como risco do contexto. O professor confirmou a adequação dessa escolha e informou que não existe desempenho mínimo, enfatizando metodologia, validação, interpretação e documentação.

## Reprodução dos novos experimentos

Após instalar `requirements.txt`, na raiz do repositório:

```text
python -m src.cli verify
python -m unittest discover -s tests -v
python -m src.modeling.enrichment --output work/enriquecimento_novo
python -m src.evaluation.baselines --output work/baselines_novos
```

Os diretórios de saída devem ser novos. O comando de enriquecimento refaz os blocos separados e a combinação somente no treino; o comando de baselines compara previsões OOF congeladas com baselines estimados dentro dos mesmos folds. Ambos usam os dados incluídos e caminhos relativos ao projeto, sem acesso aos Downloads ou à pasta de preparação original. Não consultam validação ou teste para gerar novos scores. Os módulos novos usam os mesmos parâmetros das análises relatadas.

Os contextos municipais públicos e scores agregados de treino estão em `data/processed/`. O manifesto adicional é `data/manifest_enriquecimento.json`. Não distribuímos registros individuais, chaves HMAC, bancos SQLite ou credenciais. Resultados e decisões estão em `reports/consolidacao-fase3/`, além dos relatórios de fontes, CV e combinação. Os relatórios originais registram os caminhos de preparação da época; os comandos acima são o caminho de reprodução portátil.

O roteiro atualizado está em `video/roteiro_atualizado.md`. A publicação em etapas está descrita em `docs/publicacao-em-etapas.md`. Ainda faltam revisão do grupo, gravação do vídeo e submissão. A Gold individual é um contrato proposto e a tabela analítica local existe; não se afirma publicação de uma nova Gold em cloud.

## Documentação da v1 preservada


Versão acadêmica 1.0, preparada em 27/10/2026. Comece por **ABRIR_RELATORIO.html**. A documentação técnica completa está em `reports/relatorio_final.md`.

## Problema e resultado

Prever o rótulo individual de não alfabetização com contexto anterior ao exame de 2024 e produzir análises territoriais. A referência final é uma regressão logística, mantida por simplicidade após a comparação com árvore, Random Forest e Gradient Boosting. No teste reservado: AP=0.5356, precisão=58.96%, recall=27.12% em limiar comparativo 0,50. O desempenho é limitado e não justifica diagnóstico individual.

## Base e pipeline

1. Recuperar avaliações válidas da Bronze da Fase 2 e reconciliar com sua Gold.
2. Integrar indicadores IBGE de 2021/2022 e proxies municipais dos indicadores INEP 2022.
3. Separar municípios inteiros em treino/validação/teste, com equilíbrio de UF, volume e classes.
4. Ajustar imputação, escala, one-hot e modelos só no treino; comparar por CV municipal.
5. Explicar associações com SHAP e explorar perfis por K-Means/PCA.
6. Fixar o modelo de referência e avaliar uma vez no teste; conservar os resultados sem retuning.

Os dados distribuídos são **agregados por município**, com contagens das duas classes que representam os 1.610.754 alunos válidos. Como todos os preditores são municipais, pesos de frequência preservam a perda individual e as métricas para um score constante por município. Não se trata de regressão de taxa municipal. Não há IDs de alunos/escolas, microdados, chaves HMAC, credenciais ou infraestrutura nesta distribuição.

## Execução

Python 3.12. Em um ambiente virtual novo:

```text
python -m pip install -r requirements.txt
python -m src.cli verify
python -m unittest discover -s tests -v
python -m src.cli evaluate
python -m src.cli train --model logistica --output work/logistica_reproduzida.joblib
python -m src.cli evaluate --artifact work/logistica_reproduzida.joblib
python -m src.cli cross-validate
python -m src.cli explain
python -m src.cli show-final
```

`evaluate` avalia somente a validação. `show-final` lê a avaliação de teste já congelada, sem recalcular. `train` recusa sobrescrever modelos. O comando de CV reproduz as seis configurações com os folds entregues. O treinamento não usa o teste. Abra arquivos joblib somente quando confiar na sua origem.

## Organização

```text
data/processed/    Dados municipais e contagens das classes
data/splits/       Divisão fixa e folds de treino
data/gold_fase2/   Gold de origem para auditoria e descrição
data/source/       Manifestos e cobertura das fontes
src/preprocessing Contratos, features e transformações
src/modeling      Treinamento e validação cruzada
src/evaluation    Métricas
src/visualization Gráficos
reports/          Relatório, métricas, decisões e verificações
images/           Figuras
models/           Modelos congelados de confiança local
notebooks/        Guia dos scripts, sem duplicação de pipeline
video/            Roteiro de até 5 minutos e apoio visual
docs/             Dados, arquitetura e aderência ao enunciado
```

## Interpretação e insights

UF tem maior influência nos modelos. O enriquecimento e o aumento de complexidade não demonstraram ganho claro. As análises evidenciaram seleção de cobertura da Gold, poucos alunos em muitos municípios, colinearidade e contexto territorial forte. SHAP não estabelece causalidade; perfis K-Means não são diagnósticos de risco. Detalhes, coeficientes, erros por UF e limitações estão nos relatórios.

## Limites e aplicação

Faltam características que diferenciem alunos do mesmo município; o vínculo escolar direto teve cobertura zero. Dados de um único ano não permitem alegar previsão de anos futuros. Nenhuma capacidade real ou limiar operacional foi escolhido. A aplicação desta versão é análise acadêmica e planejamento territorial exploratório. Evoluir requer dados anteriores mais granulares e novos anos de avaliação.

## Entrega e versionamento

Há repositório Git local com commits e branches reais desta organização. Não representa um histórico de desenvolvimento desde a Fase 2. Nenhum repositório remoto ou PR foi publicado nesta etapa. Vídeo, revisão do grupo e submissão no FIAP ON permanecem pendentes. Consulte `docs/checklist-entrega.md`.

## Exportar o relatório em PDF

O PDF consolidado está em `reports/relatorio_final.pdf`. A fonte editável está em `reports/consolidacao-fase3/relatorio_atualizado.md`. Para regenerar o PDF, instale a dependência opcional e execute na raiz:

```text
python -m pip install -r requirements-pdf.txt
python -m src.visualization.report_pdf
```

O gerador apenas formata o relatório e incorpora figuras históricas existentes; não treina modelos nem recalcula o teste.
