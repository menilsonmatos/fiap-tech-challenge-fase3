import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from src.preprocessing.features import make_preprocessor

def compress_as_binary(frame):
    """Duas linhas por contexto, pesos de contagem; 1 significa não alfabetizado."""
    x = pd.concat([frame, frame], ignore_index=True)
    y = np.r_[np.ones(len(frame), dtype=int), np.zeros(len(frame), dtype=int)]
    w = np.r_[frame.nao_alfabetizados.to_numpy(), frame.alfabetizados.to_numpy()].astype(float)
    return x, y, w

def fit_model(frame, family='logistica', enriched=False, params=None):
    if not frame.conjunto.eq('treino').all():
        raise ValueError('O ajuste aceita somente municípios do treino')
    params = params or {}
    pre = make_preprocessor(enriched)
    pre.fit(frame)
    x, y, w = compress_as_binary(frame)
    if family == 'logistica':
        model = LogisticRegression(C=1.0, solver='lbfgs', max_iter=2000,
                                   tol=1e-7, random_state=42, **params)
    elif family == 'random_forest':
        model = RandomForestClassifier(n_estimators=150, max_features='sqrt',
            bootstrap=False, n_jobs=4, random_state=42, **params)
    elif family == 'boosting':
        model = GradientBoostingClassifier(learning_rate=.05, min_weight_fraction_leaf=.001,
            subsample=1.0, random_state=42, **params)
    else:
        raise ValueError('Família desconhecida')
    model.fit(pre.transform(x), y, sample_weight=w)
    if hasattr(model, 'max_iter') and np.max(model.n_iter_) >= model.max_iter:
        raise RuntimeError('O modelo não convergiu')
    return Pipeline([('preprocessing', pre), ('model', model)])
