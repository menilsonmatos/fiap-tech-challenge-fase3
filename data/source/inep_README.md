# Enriquecimento educacional de referência 2022

Os downloads oficiais INEP ATU e DSU foram concluídos. O ATU XLSX tem divergência do MD5 do pacote, por isso foi lido o ODS cujo MD5 confere. O DSU XLSX confere. Hashes, URLs e arquivo efetivamente utilizado estão em `manifesto_fontes.json`.

## Vínculo por escola: sem correspondência

Nenhuma das 36.920 chaves de escola da avaliação encontrou correspondência por município e código escolar nos dois arquivos. Não foi encontrada tabela de equivalência. Os códigos da avaliação não foram presumidos como códigos INEP. Isso pode indicar anonimização ou outro domínio de identificadores, mas a causa não foi comprovada. O resultado está em `cobertura.json`; não se afirma enriquecimento por escola.

## Alternativa aplicada: contexto municipal educacional

Foram usadas as escolas identificadas como municipais no arquivo ATU de 2022, com médias simples dos indicadores disponíveis por município. São proxies calculadas neste projeto, não os indicadores municipais oficiais ponderados por turmas ou funções docentes:

- Média entre escolas da média de alunos por turma nos anos iniciais.
- Média entre escolas da média de alunos por turma do 2º ano.
- Média entre escolas do percentual de funções docentes com curso superior nos anos iniciais, para escolas do recorte ATU com correspondência DSU.
- Percentual de escolas rurais entre as escolas municipais do recorte ATU.

As contagens de escolas com indicador disponível acompanham a tabela contextual. Não houve ponderação por matrículas, turmas ou funções docentes, pois esses denominadores não estão nesses arquivos. Valores `--` foram tratados como ausentes, nunca como zero. A imputação será feita apenas nos folds de treino.

## Banco e integração

`contexto_escolar.sqlite` contém `contexto_educacional_municipal_2022` e `municipios_analiticos`, além da tentativa escolar documentada. `municipios_analiticos` contém contagens das duas classes por município e atribuição aos conjuntos. Para enriquecer a tabela individual existente, fazer LEFT JOIN pelo `id_municipio` com `contexto_educacional_municipal_2022`. A chave é única, preservando a cardinalidade dos alunos. A base individual e a divisão original não foram alteradas. O treinamento consulta somente as linhas de treino/validação.

Não foi criado atributo individual: a previsão permanece igual para alunos de um mesmo município. Referência 2022 anterior ao exame de 2024; downloads atuais, sem garantia de versão histórica exata. As páginas de atividades do INEP em 2023 registram a divulgação dos indicadores de 2022.

Fontes: [ATU](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/media-de-alunos-por-turma/2022), [DSU](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/percentual-de-docentes-com-curso-superior/2022), [atividades INEP em 2023](https://www.gov.br/inep/pt-br/relatorio-anual-de-atividades-e-gestao-do-inep-2023/pesquisas-estatisticas-e-indicadores-educacionais/indicadores-educacionais).


O leitor `ler_base_enriquecida.py` disponibiliza a tabela individual acrescida das quatro features municipais educacionais, em blocos e com escolha explícita de conjunto. O bloco inicial da validação foi lido e verificado sem alterar os bancos; nenhum registro do teste foi lido nessa verificação. A função não treina nem avalia modelos.
