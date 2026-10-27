# Logística mantida como referência — cenários hipotéticos de limiar

A logística contextual foi mantida como referência de simplicidade. O manifesto `modelo_referencia.json` aponta para o artefato existente e registra seu hash. Não houve retreinamento sobre treino+validação, alteração da divisão ou avaliação no teste.

Os limiares abaixo foram calculados exclusivamente das previsões fora do fold (OOF) nos três folds de municípios do treino já fixados. Em cada fold, imputação, escala, codificação e regressão foram ajustadas apenas nos municípios de treino. O limiar é o menor score que permite manter todos os empates sem exceder a capacidade nominal no treino. A verificação na validação usa o modelo já ajustado no treino completo.

| Capacidade-alvo no treino | Limiar | Alertas na validação | % dos alunos alertados | Precisão | Recall | Falsos positivos | Falsos negativos |
|---|---:|---:|---:|---:|---:|---:|---:|
| 20% | 0.548842 | 36036 | 11.24% | 61.76% | 17.04% | 13781 | 108312 |
| 30% | 0.497229 | 55670 | 17.36% | 58.87% | 25.10% | 22895 | 97792 |
| 50% | 0.407191 | 148548 | 46.33% | 51.74% | 58.86% | 71695 | 53714 |

Por definição do usuário, não será escolhida uma capacidade real de atendimento. Os percentuais são apenas cenários acadêmicos hipotéticos, não compromissos de atendimento nem requisito pendente. Nenhum limiar operacional foi selecionado. O limiar 0,50 permanece apenas como referência convencional para comparar métricas entre modelos. O limiar aprendido no treino não garante a mesma fração de alertas em dados novos: as populações e distribuições de score variam. Uma quota rígida exigiria uma regra de priorização adicional; como os scores são iguais por município, empates não devem ser quebrados arbitrariamente para escolher alunos.

O alvo é não alfabetizado. Falsos positivos são alunos alfabetizados que receberiam alerta; falsos negativos são não alfabetizados não identificados. Aumentar a capacidade tende a ampliar recall e falsos alertas; não melhora a informação individual do modelo. Dados de custo dos erros e capacidade de atendimento não foram inventados. Os resultados por UF estão no JSON associado. Não houve decisão ou contato sobre alunos.
