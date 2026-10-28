# Roteiro executivo atualizado — até 5 minutos

## 0:00–0:40 — Problema
Queremos apoiar o entendimento do risco de não alfabetização ao final do segundo ano. O alvo é individual, mas os dados disponíveis descrevem principalmente o município. Por isso interpretamos a saída como risco do contexto, sem diagnosticar crianças individualmente.

## 0:40–1:30 — Dados e estrutura
A Fase 2 forneceu o pipeline e as fontes. Auditamos os registros de 2024 e mantivemos aproximadamente 1,61 milhão de avaliações válidas. Integramos informações anteriores de população, economia e educação. Documentamos que a Gold original era agregada e que o resultado individual precisou ser recuperado das fontes preservadas e validado. Para calcular o modelo com eficiência, representamos as classes por suas contagens em cada município.

## 1:30–2:20 — Metodologia
Mantivemos todos os alunos de cada município no mesmo conjunto. Na validação cruzada, imputação, escala e codificação foram ajustadas dentro de cada fold. Excluímos proficiência e resultados contemporâneos, pois poderiam revelar a própria resposta. Comparamos a regressão logística com outras configurações e preservamos as limitações observadas.

## 2:20–3:20 — Quanto o modelo agrega
Nos três folds do treino, o baseline global teve AP média de 0,405. O baseline estadual, calculado só com municípios de ajuste, alcançou 0,511. A logística contextual chegou a 0,520, e a inclusão de reprovação e abandono anteriores levou a 0,527. O ganho existe, mas é modesto além da informação estadual. Somar distorção idade-série não trouxe ganho adicional. Esses são resultados de desenvolvimento, não uma nova confirmação de teste.

## 3:20–4:10 — Limitações
Alunos do mesmo município recebem a mesma probabilidade. O modelo não explica causalmente o aprendizado, não foi validado em uma nova safra e não melhorou em todos os estados. A avaliação de teste da primeira versão está congelada e não pode confirmar uma configuração escolhida depois. Não selecionamos capacidade de atendimento ou limiar operacional.

## 4:10–4:50 — Aplicação e evolução
O uso possível é apoiar diagnósticos territoriais e investigação de redes, junto com análise pedagógica. A evolução exige atributos anteriores mais granulares e novos anos para validação independente. O principal resultado do projeto é uma pipeline reproduzível e documentada, com evidências do ganho incremental e dos seus limites.
