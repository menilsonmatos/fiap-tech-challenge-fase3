from pathlib import Path
import json
import pandas as pd
from src.modeling.training import fit_model
from src.evaluation.metrics import evaluate

ROOT=Path(__file__).resolve().parents[2]

def run(train):
    folds=pd.DataFrame(json.loads((ROOT/'data/splits/folds_treino.json').read_text(encoding='utf-8')))
    data=train.merge(folds,on='id_municipio',validate='one_to_one')
    if len(data)!=len(train):
        raise ValueError('Mapa de folds incompleto')
    specs=[('logistica_contexto','logistica',False,{}),('logistica_educacional','logistica',True,{}),
           ('rf_prof8','random_forest',True,{'max_depth':8,'min_weight_fraction_leaf':.001}),
           ('rf_prof12','random_forest',True,{'max_depth':12,'min_weight_fraction_leaf':.0005}),
           ('gb_prof2','boosting',True,{'n_estimators':120,'max_depth':2}),
           ('gb_prof3','boosting',True,{'n_estimators':160,'max_depth':3})]
    results=[]
    for name,family,enriched,params in specs:
        scores=[]
        for fold in range(3):
            fit=data[data.fold.ne(fold)]; hold=data[data.fold.eq(fold)]
            assert set(fit.id_municipio).isdisjoint(hold.id_municipio)
            model=fit_model(fit,family,enriched,params)
            scores.append(evaluate(hold,model.predict_proba(hold)[:,1])['AP'])
        results.append({'candidate':name,'fold_AP':scores,'mean_AP':sum(scores)/3})
    return results
