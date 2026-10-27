# Versionamento local

O repositório foi iniciado durante a organização desta versão, com autoria técnica de commits identificada como Codex; isso não substitui a identificação dos integrantes do grupo no portal.

Foram criados commits separados de pipeline/dados e de resultados, uma branch `analise/entrega-v1` e uma integração real com merge na branch `main`. Não há PR remoto ou revisão humana simulada.

O arquivo `HISTORICO.bundle` dentro do ZIP preserva todas as branches e a tag de versão. Para recuperar o repositório com histórico em outra pasta:

```text
git clone HISTORICO.bundle projeto-com-historico
git -C projeto-com-historico log --oneline --all
```

A pasta extraída já contém a árvore de arquivos utilizável sem Git. O bundle não contém dados individuais ou credenciais; as fontes de entrada distribuídas são agregadas. Publicar remotamente e criar PR seguem pendentes.
