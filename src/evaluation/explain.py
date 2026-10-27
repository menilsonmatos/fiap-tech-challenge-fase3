import json
from pathlib import Path
import numpy as np
import joblib

def run(frame, root, output):
    import shap
    train=frame[frame.conjunto.eq('treino')]
    val=frame[frame.conjunto.eq('validacao')].sample(500,random_state=42)
    result={}
    for name,path in [('logistica','logistica_referencia.joblib'),('boosting','boosting_comparador.joblib')]:
        pipe=joblib.load(root/'models'/path)
        pre=pipe.named_steps['preprocessing'];model=pipe.named_steps['model']
        bg=pre.transform(train.sample(200,random_state=42));x=pre.transform(val)
        if name=='logistica':explainer=shap.LinearExplainer(model,shap.maskers.Independent(bg,max_samples=200))
        else:explainer=shap.TreeExplainer(model,data=bg,feature_perturbation='interventional',model_output='raw')
        exp=explainer(x);assert np.allclose(exp.base_values+exp.values.sum(axis=1),model.decision_function(x),atol=1e-5)
        groups={}
        for j,col in enumerate(pre.get_feature_names_out()):
            key='UF (conjunto das categorias)' if col.startswith('cat__sigla_uf_') else col.replace('num__','')
            groups[key]=groups.get(key,np.zeros(len(x)))+exp.values[:,j]
        result[name]=dict(method='Interventional SHAP em log-odds, peso municipal igual; não causal',
                          summary=sorted([dict(feature=k,mean_abs_shap=float(np.abs(v).mean())) for k,v in groups.items()],key=lambda x:x['mean_abs_shap'],reverse=True),
                          additivity_verified=True,background_effective=200 if name=='logistica' else 100)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return str(output)
