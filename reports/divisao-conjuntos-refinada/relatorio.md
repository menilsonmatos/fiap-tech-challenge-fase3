# Divisão refinada — treino, validação e teste

A atribuição foi refinada exclusivamente com UF, contagem de alunos e contagens das duas classes por município. Cada município e, por consequência, seus alunos e escolas, permanece inteiro em um único conjunto. As contagens de municípios por UF/conjunto da primeira divisão foram preservadas. O banco individual e os arquivos da divisão anterior não foram alterados.

## Resultado e decisão

A divisão refinada fica fixada para os próximos experimentos. As frações de alunos são 60,154% no treino, 19,906% na validação e 19,939% no teste. As taxas de alfabetizados são 59,432%, 59,279% e 59,285%, respectivamente; a amplitude global caiu de 2,03 para 0,15 ponto percentual.

A média dos desvios absolutos das taxas UF/conjunto caiu de 2,614 para 0,262 ponto percentual; o pior desvio caiu de 25,151 para 4,631. A média dos desvios absolutos das frações de alunos por UF caiu de 7,128 para 0,311 ponto percentual; o pior, de 38,080 para 5,967. Foram realocados 888 municípios, mantendo a contagem municipal por UF/conjunto.

Não se alcançou igualdade exata, especialmente em UFs com concentração populacional. Os detalhes abaixo tornam essas limitações verificáveis. O objetivo conjunto melhorou em todas as UFs. Uma reconciliação independente por junção dos arquivos confirmou as contagens de municípios, alunos e classes por conjunto. O hash da atribuição está em `manifesto_divisao.json`.

## Método reproduzível

{
  "method": "Estratificação por UF; contagens municipais 60/20/20 preservadas; busca local por trocas de pares, até 150 trocas por início e 12 inícios determinísticos por UF (original + 11 reinícios). Heurística, sem garantia de ótimo global.",
  "objective": "Soma por UF, conjunto e categoria [alunos totais, alfabetizados, não alfabetizados] de (fração da categoria atribuída − proporção alvo)^2 / proporção alvo.",
  "targets": {
    "treino": 0.6,
    "validacao": 0.2,
    "teste": 0.2
  },
  "randomness": "UF-specific seed derived from SHA256(fase3-refinada42|UF), NumPy default_rng; first start is prior assignment",
  "source_sha256": "f69957bd682e6b45c83576f257c878ee0c5d45571c2144c6556f02f13eff53c4",
  "uses_labels": "Somente contagens agregadas para estratificação; nenhum modelo, feature ou resultado de desempenho participa da seleção.",
  "numpy_version": "2.3.5"
}

O uso do alvo aqui se limita à estratificação, autorizada pelo pedido de equilíbrio de classes; não houve treinamento nem escolha com base em performance. A divisão utiliza todos os alunos elegíveis e não somente os municípios da Gold da Fase 2. A comparação completa está em `verificacao.json`; o mapeamento está em `atribuicao_municipios.json`.

## Comparação global

Anterior:

| conjunto | municipios | alunos | fracao_alunos_pct | taxa_alfabetizados_pct | ufs |
| --- | --- | --- | --- | --- | --- |
| teste | 1087 | 364296 | 22.616 | 58.083 | 25 |
| treino | 3267 | 937620 | 58.210 | 60.111 | 25 |
| validacao | 1096 | 308838 | 19.174 | 58.650 | 25 |

Refinada:

| conjunto | municipios | alunos | fracao_alunos_pct | taxa_alfabetizados_pct | ufs |
| --- | --- | --- | --- | --- | --- |
| teste | 1087 | 321176 | 19.939 | 59.285 | 25 |
| treino | 3267 | 968939 | 60.154 | 59.432 | 25 |
| validacao | 1096 | 320639 | 19.906 | 59.279 | 25 |

## Equilíbrio por UF

| uf | conjunto | municipios | alunos | fracao_alunos_pct | desvio_fracao_alunos_pp | taxa_alfabetizados_pct | diferenca_taxa_uf_pp |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC | teste | 4 | 1148 | 19.972 | -0.028 | 49.303 | 0.486 |
| AC | treino | 13 | 3449 | 60.003 | 0.003 | 48.594 | -0.223 |
| AC | validacao | 5 | 1151 | 20.024 | 0.024 | 49.001 | 0.184 |
| AL | teste | 20 | 6043 | 19.999 | -0.001 | 49.330 | -0.005 |
| AL | treino | 61 | 18129 | 59.998 | -0.002 | 49.335 | 0.001 |
| AL | validacao | 21 | 6044 | 20.003 | 0.003 | 49.338 | 0.003 |
| AM | teste | 12 | 6046 | 17.018 | -2.982 | 42.458 | -4.605 |
| AM | treino | 37 | 23436 | 65.967 | 5.967 | 49.445 | 2.383 |
| AM | validacao | 13 | 6045 | 17.015 | -2.985 | 42.432 | -4.631 |
| AP | teste | 3 | 1739 | 20.985 | 0.985 | 51.064 | 1.251 |
| AP | treino | 10 | 5356 | 64.631 | 4.631 | 50.205 | 0.392 |
| AP | validacao | 3 | 1192 | 14.384 | -5.616 | 46.225 | -3.588 |
| BA | teste | 81 | 20760 | 20.000 | -0.000 | 35.963 | -0.001 |
| BA | treino | 244 | 62282 | 60.001 | 0.001 | 35.965 | 0.001 |
| BA | validacao | 82 | 20760 | 20.000 | -0.000 | 35.963 | -0.001 |
| CE | teste | 37 | 17538 | 20.000 | 0.000 | 85.363 | -0.001 |
| CE | treino | 110 | 52613 | 60.000 | -0.000 | 85.365 | 0.001 |
| CE | validacao | 37 | 17538 | 20.000 | 0.000 | 85.363 | -0.001 |
| ES | teste | 15 | 8105 | 20.000 | 0.000 | 71.289 | -0.002 |
| ES | treino | 47 | 24313 | 59.995 | -0.005 | 71.291 | -0.001 |
| ES | validacao | 16 | 8107 | 20.005 | 0.005 | 71.296 | 0.005 |
| GO | teste | 49 | 14150 | 20.000 | 0.000 | 73.011 | -0.002 |
| GO | treino | 147 | 42449 | 59.999 | -0.001 | 73.015 | 0.002 |
| GO | validacao | 49 | 14150 | 20.000 | 0.000 | 73.011 | -0.002 |
| MA | teste | 43 | 12570 | 20.001 | 0.001 | 60.127 | -0.003 |
| MA | treino | 130 | 37708 | 60.000 | -0.000 | 60.130 | 0.000 |
| MA | validacao | 44 | 12569 | 19.999 | -0.001 | 60.132 | 0.002 |
| MG | teste | 166 | 28486 | 20.000 | 0.000 | 71.965 | 0.001 |
| MG | treino | 498 | 85458 | 60.000 | 0.000 | 71.963 | -0.001 |
| MG | validacao | 166 | 28486 | 20.000 | 0.000 | 71.965 | 0.001 |
| MS | teste | 16 | 7303 | 20.001 | 0.001 | 56.675 | 0.018 |
| MS | treino | 47 | 21909 | 60.002 | 0.002 | 56.653 | -0.005 |
| MS | validacao | 16 | 7302 | 19.998 | -0.002 | 56.656 | -0.002 |
| MT | teste | 28 | 8740 | 20.000 | -0.000 | 61.396 | 0.004 |
| MT | treino | 84 | 26221 | 60.001 | 0.001 | 61.390 | -0.002 |
| MT | validacao | 28 | 8740 | 20.000 | -0.000 | 61.396 | 0.004 |
| PA | teste | 29 | 15467 | 20.000 | 0.000 | 48.135 | -0.001 |
| PA | treino | 86 | 46400 | 59.999 | -0.001 | 48.136 | 0.000 |
| PA | validacao | 29 | 15467 | 20.000 | 0.000 | 48.135 | -0.001 |
| PB | teste | 44 | 5965 | 20.001 | 0.001 | 56.664 | -0.002 |
| PB | treino | 133 | 17894 | 59.999 | -0.001 | 56.667 | 0.001 |
| PB | validacao | 44 | 5965 | 20.001 | 0.001 | 56.664 | -0.002 |
| PE | teste | 37 | 15160 | 19.999 | -0.001 | 61.049 | -0.000 |
| PE | treino | 110 | 45482 | 60.000 | 0.000 | 61.048 | -0.001 |
| PE | validacao | 37 | 15161 | 20.001 | 0.001 | 61.051 | 0.002 |
| PI | teste | 45 | 6194 | 19.998 | -0.002 | 60.203 | -0.004 |
| PI | treino | 134 | 18584 | 60.001 | 0.001 | 60.208 | 0.000 |
| PI | validacao | 45 | 6195 | 20.001 | 0.001 | 60.210 | 0.003 |
| PR | teste | 80 | 23926 | 20.000 | 0.000 | 70.810 | 0.001 |
| PR | treino | 239 | 71778 | 60.000 | 0.000 | 70.809 | -0.001 |
| PR | validacao | 80 | 23926 | 20.000 | 0.000 | 70.810 | 0.001 |
| RJ | teste | 18 | 25115 | 20.006 | 0.006 | 55.246 | -0.619 |
| RJ | treino | 55 | 75307 | 59.988 | -0.012 | 56.275 | 0.410 |
| RJ | validacao | 19 | 25114 | 20.005 | 0.005 | 55.256 | -0.609 |
| RN | teste | 33 | 3863 | 20.003 | 0.003 | 38.856 | 0.009 |
| RN | treino | 100 | 11587 | 59.999 | -0.001 | 38.845 | -0.001 |
| RN | validacao | 34 | 3862 | 19.998 | -0.002 | 38.840 | -0.006 |
| RO | teste | 10 | 3720 | 19.981 | -0.019 | 63.038 | 0.066 |
| RO | treino | 31 | 11172 | 60.006 | 0.006 | 62.952 | -0.019 |
| RO | validacao | 11 | 3726 | 20.013 | 0.013 | 62.963 | -0.008 |
| RS | teste | 91 | 12211 | 20.001 | 0.001 | 45.279 | 0.000 |
| RS | treino | 274 | 36631 | 59.999 | -0.001 | 45.279 | -0.000 |
| RS | validacao | 91 | 12211 | 20.001 | 0.001 | 45.279 | 0.000 |
| SC | teste | 58 | 10653 | 20.001 | 0.001 | 64.592 | 0.000 |
| SC | treino | 173 | 31957 | 60.000 | -0.000 | 64.593 | 0.001 |
| SC | validacao | 58 | 10652 | 19.999 | -0.001 | 64.589 | -0.003 |
| SE | teste | 15 | 3133 | 19.992 | -0.008 | 38.206 | -0.011 |
| SE | treino | 45 | 9403 | 60.003 | 0.003 | 38.222 | 0.005 |
| SE | validacao | 15 | 3135 | 20.005 | 0.005 | 38.214 | -0.003 |
| SP | teste | 125 | 59781 | 20.000 | 0.000 | 56.095 | -0.001 |
| SP | treino | 376 | 179342 | 60.000 | -0.000 | 56.096 | 0.000 |
| SP | validacao | 125 | 59781 | 20.000 | 0.000 | 56.095 | -0.001 |
| TO | teste | 28 | 3360 | 20.001 | 0.001 | 50.119 | -0.003 |
| TO | treino | 83 | 10079 | 59.998 | -0.002 | 50.124 | 0.002 |
| TO | validacao | 28 | 3360 | 20.001 | 0.001 | 50.119 | -0.003 |

## Limites

UFs com poucos municípios ou com grande concentração na capital não podem ser perfeitamente proporcionais sem dividir municípios. As proporções de alunos são objetivos, não restrições exatas. A heurística otimiza conjuntamente volumes das classes; pode haver uma métrica isolada que piore enquanto o objetivo conjunto melhora. As taxas por UF devem continuar acompanhando as métricas dos modelos.

Esta é uma divisão interna de dados de 2024. A EDA já observou toda a base; não é validação externa intocada nem validação temporal. Fixar esta atribuição antes dos experimentos e não modificá-la por resultados de modelos. Ajustar preprocessamento, seleção de features, hiperparâmetros e limiares sem consultar o teste. Não houve oversampling ou perda de registros.

## Verificações

- same_municipalities: True
- municipal_counts_by_uf_preserved: True
- all_25_ufs_each_set: True
- all_rows_preserved: True
- all_labels_preserved: True
- both_classes_each_uf_set: True
- each_uf_objective_no_worse: True

### Maiores diferenças residuais de taxa por UF

| UF | Conjunto | Alunos | Taxa (%) | Diferença para UF (pp) |
|---|---|---:|---:|---:|
| AM | validacao | 6045 | 42.432 | -4.631 |
| AM | teste | 6046 | 42.458 | -4.605 |
| AP | validacao | 1192 | 46.225 | -3.588 |
| AM | treino | 23436 | 49.445 | 2.383 |
| AP | teste | 1739 | 51.064 | 1.251 |
