"""Grade curta de C na logística, com CV municipal exclusiva do treino."""
from pathlib import Path
import argparse
import hashlib
import json
import warnings
import numpy as np
import pandas as pd
import sklearn
from src.modeling.training import fit_model
from src.preprocessing.features import NUMERIC
from src.evaluation.metrics import evaluate

ROOT = Path(__file__).resolve().parents[2]
GRID = [.01, .1, 1., 10.]
BLOCKS = {
    'referencia': [],
    'rendimento': ['reprovacao_AI_pct_2022', 'abandono_AI_pct_2022',
                   'reprovacao_2ano_pct_2022', 'abandono_2ano_pct_2022'],
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False),
                    encoding='utf-8')


def run(output):
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError('Escolha uma saída nova; resultados existentes são preservados')
    protected = [ROOT/'models/logistica_referencia.joblib',
                 ROOT/'models/boosting_comparador.joblib',
                 ROOT/'reports/avaliacao-final/protocolo_teste_fixado.json',
                 ROOT/'reports/avaliacao-final/resultados_teste.json']
    before = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    inputs = {key: ROOT/rel for key, rel in {
        'base': 'data/processed/dados_analiticos_municipais.json',
        'contexto': 'data/processed/contexto_municipal_candidato.json',
        'folds': 'data/splits/folds_treino.json',
    }.items()}
    hashes = {k: sha(p) for k, p in inputs.items()}
    manifest = json.loads((ROOT/'data/manifest.json').read_text(encoding='utf-8'))
    if hashes['base'] != manifest['dataset_sha256']:
        raise ValueError('Hash do dataset de origem inválido')
    extra_manifest = json.loads((ROOT/'data/manifest_enriquecimento.json').read_text(encoding='utf-8'))
    if hashes['contexto'] != extra_manifest['files']['contexto_municipal_candidato.json']:
        raise ValueError('Hash do contexto inválido')
    folds = pd.read_json(inputs['folds'], dtype={'id_municipio': str})
    ids = set(folds.id_municipio)
    # Only municipalities belonging to the frozen TRAIN folds are selected.
    records = json.loads(inputs['base'].read_text(encoding='utf-8'))
    train = pd.DataFrame([r for r in records if r['id_municipio'] in ids])
    del records
    if not train.conjunto.eq('treino').all():
        raise ValueError('Mapa de folds contém município fora do treino')
    context = pd.read_json(inputs['contexto'], dtype={'id_municipio': str})
    context = context[['id_municipio'] + BLOCKS['rendimento']]
    train = train.merge(folds, on='id_municipio', how='left', validate='1:1')
    train = train.merge(context, on='id_municipio', how='left', validate='1:1')
    train = train.sort_values('id_municipio').reset_index(drop=True)
    if len(train) != 3267 or train.n.sum() != 968939 or train.fold.isna().any():
        raise ValueError('Cobertura ou volume do treino inesperado')
    if set(train.fold) != {0, 1, 2} or set(train.id_municipio) != ids:
        raise ValueError('Folds inconsistentes')
    output.mkdir(parents=True)
    protocol = {
        'data': '2026-11-01', 'C': GRID, 'blocos': BLOCKS,
        'features_referencia': NUMERIC, 'categoricas': ['sigla_uf'],
        'modelo': {'familia': 'LogisticRegression', 'regularizacao': 'L2 padrão',
                   'solver': 'lbfgs', 'max_iter': 3000, 'tol': 1e-8, 'random_state': 42},
        'metrica_primaria': 'AP média simples nos mesmos 3 folds de municípios do treino',
        'selecao': 'Maior AP média em cada bloco; empate exato favorece menor C',
        'pesos': 'Contagens de alunos por classe; sem normalizar e sem pesos amostrais INEP',
        'preprocessamento': 'Ajustado somente no fold de ajuste; igual peso por município',
        'interpretacao_C': 'Menor C significa regularização mais forte. A escala depende dos pesos de frequência mantidos constantes.',
        'escopo': 'Somente treino. Sem nova previsão na validação externa ou no teste. Sem refit final ou substituição da v1.',
        'limite': 'Desenvolvimento nos mesmos folds já explorados. O melhor score selecionado não é confirmação independente.',
        'hashes_entradas': hashes, 'arquivos_congelados_antes': before,
        'versoes': {'sklearn': sklearn.__version__, 'numpy': np.__version__, 'pandas': pd.__version__},
    }
    write(output/'protocolo.json', protocol)
    results, notes, summaries, by_uf = [], [], [], []
    scores = train[['id_municipio', 'sigla_uf', 'fold', 'n', 'nao_alfabetizados']].copy()
    for block, extra in BLOCKS.items():
        for c in GRID:
            oof = np.full(len(train), np.nan)
            for fold in range(3):
                fit = train.loc[train.fold.ne(fold)]
                hold = train.loc[train.fold.eq(fold)]
                if not set(fit.id_municipio).isdisjoint(hold.id_municipio):
                    raise ValueError('Município compartilhado entre ajuste e holdout')
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter('always')
                    pipe = fit_model(fit, params={'C': c, 'max_iter': 3000, 'tol': 1e-8},
                                     numeric_features=NUMERIC + extra)
                notes.extend({'bloco': block, 'C': c, 'fold': fold,
                              'aviso': str(w.message)} for w in caught)
                p = pipe.predict_proba(hold)[:, 1]
                oof[hold.index] = p
                model = pipe.named_steps['model']
                results.append({'bloco': block, 'C': c, 'fold': fold,
                                'municipios_ajuste': len(fit), 'municipios_holdout': len(hold),
                                'alunos_holdout': int(hold.n.sum()),
                                'iteracoes': int(model.n_iter_.max()),
                                'norma_coeficientes': float(np.linalg.norm(model.coef_)),
                                'ajuste': evaluate(fit, pipe.predict_proba(fit)[:, 1]),
                                'holdout': evaluate(hold, p)})
                print(f'{block} C={c:g} fold={fold}: AP={results[-1]["holdout"]["AP"]:.7f}', flush=True)
            if not np.isfinite(oof).all():
                raise ValueError('Previsões OOF incompletas')
            rr = [r for r in results if r['bloco'] == block and r['C'] == c]
            summaries.append({'bloco': block, 'C': c,
                              'AP_media': float(np.mean([r['holdout']['AP'] for r in rr])),
                              'AP_desvio_folds': float(np.std([r['holdout']['AP'] for r in rr], ddof=1)),
                              'AP_ajuste_media': float(np.mean([r['ajuste']['AP'] for r in rr])),
                              'Brier_media': float(np.mean([r['holdout']['Brier'] for r in rr])),
                              'AP_por_fold': [r['holdout']['AP'] for r in rr],
                              'OOF': evaluate(train, oof)})
            scores[f'p_{block}_C{c:g}'] = oof
            for uf, g in train.groupby('sigla_uf'):
                by_uf.append({'bloco': block, 'C': c, 'uf': uf, 'municipios': len(g),
                              **evaluate(g, oof[g.index])})
    previous = json.loads((ROOT/'reports/validacao-cruzada-enriquecimento/resultados.json').read_text(encoding='utf-8'))
    reproduced = {}
    chosen = {}
    for block in BLOCKS:
        baseline = next(r for r in summaries if r['bloco'] == block and r['C'] == 1.)
        expected = next(r for r in previous['resumo'] if r['bloco'] == block)
        reproduced[block] = abs(baseline['AP_media'] - expected['AP_media_folds']) < 1e-12
        if not reproduced[block]:
            raise ValueError('Controle C=1 não reproduziu a comparação anterior')
        for row in summaries:
            if row['bloco'] == block:
                row['delta_AP_vs_C1'] = row['AP_media'] - baseline['AP_media']
                row['gap_AP_ajuste_holdout'] = row['AP_ajuste_media'] - row['AP_media']
        chosen[block] = max([r for r in summaries if r['bloco'] == block],
                            key=lambda r: (r['AP_media'], -r['C']))['C']
    after = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    if before != after or hashes != {k: sha(p) for k, p in inputs.items()}:
        raise ValueError('Arquivo protegido ou de entrada foi alterado')
    payload = {'resumo': summaries, 'folds': results, 'C_selecionado_exploratorio': chosen,
               'controles_C1_reproduzidos': reproduced, 'avisos': notes,
               'teste_reavaliado': False, 'modelo_final_substituido': False,
               'arquivos_congelados_preservados': before == after}
    write(output/'resultados.json', payload)
    write(output/'metricas_por_uf.json', by_uf)
    scores.to_json(output/'previsoes_oof.json', orient='records', indent=2, double_precision=15)
    lines = ['# Comparação curta de regularização', '',
             'Somente treino: 3.267 municípios, 968.939 alunos e três folds fixos. '
             'Regularização L2; menor C implica penalização mais forte. A AP média dos folds é a métrica principal.', '',
             '| Bloco | C | AP média | Desvio folds | Delta AP vs C=1 | Brier médio | Gap AP ajuste-holdout |',
             '|---|---:|---:|---:|---:|---:|---:|']
    for row in summaries:
        lines.append(f"| {row['bloco']} | {row['C']:g} | {row['AP_media']:.7f} | "
                     f"{row['AP_desvio_folds']:.7f} | {row['delta_AP_vs_C1']:+.7f} | "
                     f"{row['Brier_media']:.7f} | {row['gap_AP_ajuste_holdout']:.7f} |")
    lines += ['', '## Interpretação', '',
              'As contagens de alunos foram mantidas como pesos de frequência; o valor de C não deve ser '
              'comparado diretamente com outro experimento que normalize esses pesos.', '',
              'A diferença entre ajuste e holdout é apenas um diagnóstico de generalização. '
              'Não é uma curva de aprendizagem, e estas três partições não são repetições independentes.', '',
              'O melhor C em cada bloco foi escolhido nesta mesma CV e permanece uma escolha exploratória. '
              'Não se deve tratar pequenas diferenças como evidência de superioridade populacional.', '',
              f'Escolhas exploratórias por AP: {chosen}. Os controles C=1 reproduzem a análise anterior.', '',
              'O teste e a validação externa não receberam novas previsões. Nenhum modelo final foi '
              'reajustado ou substituído. Uma nova amostra ou safra é necessária para confirmação independente.']
    for block in BLOCKS:
        best = next(r for r in summaries if r['bloco'] == block and r['C'] == chosen[block])
        baseline = next(r for r in summaries if r['bloco'] == block and r['C'] == 1.)
        changes = [a-b for a, b in zip(best['AP_por_fold'], baseline['AP_por_fold'])]
        lines += ['', f"Bloco {block}: C={best['C']:g} teve delta de AP média "
                  f"{best['delta_AP_vs_C1']:+.7f} versus C=1; melhorou em "
                  f"{sum(x > 0 for x in changes)} dos três folds. A AP OOF agrupada "
                  f"mudou em {best['OOF']['AP']-baseline['OOF']['AP']:+.7f}. "
                  'A ordenação pela AP média pode diferir da AP OOF agrupada, pois AP não é aditiva.']
    (output/'relatorio.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'work/regularizacao')
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps({'resumo': result['resumo'],
                      'C_selecionado_exploratorio': result['C_selecionado_exploratorio']},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
