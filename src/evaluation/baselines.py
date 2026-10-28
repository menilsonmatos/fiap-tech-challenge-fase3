"""Recalcula baselines sem treinar candidatos ou acessar validação/teste.
Executar com Python, numpy, pandas e scikit-learn do projeto.
"""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd
from sklearn.metrics import average_precision_score,brier_score_loss,roc_auc_score,log_loss
ROOT=Path(__file__).resolve().parents[2]
import argparse
parser=argparse.ArgumentParser(description='Baselines globais e por UF nos folds congelados do treino')
parser.add_argument('--output',type=Path,default=ROOT/'work/baselines_reproduzidos')
args=parser.parse_args()
OUT=args.output.resolve()
if OUT.exists(): raise FileExistsError('Escolha uma saída nova')
OUT.mkdir(parents=True)
path=ROOT/'data/processed/dados_treino_oof.json'
d=pd.read_json(path,dtype={'id_municipio':str})
assert len(d)==3267 and d.n.sum()==968939 and d.id_municipio.is_unique
assert set(d.fold)=={0,1,2}
d['p_global']=np.nan;d['p_uf']=np.nan
records=[]
def metric(g,p):
 y=np.r_[np.ones(len(g)),np.zeros(len(g))];w=np.r_[g.nao_alfabetizados,g.alfabetizados];p=np.r_[p,p]
 return {'AP':float(average_precision_score(y,p,sample_weight=w)),'Brier':float(brier_score_loss(y,p,sample_weight=w)),'ROC_AUC':float(roc_auc_score(y,p,sample_weight=w)),'log_loss':float(log_loss(y,p,sample_weight=w))}
names=['global','uf','referencia','distorcao','rendimento','combinado']
for fold in range(3):
 fit=d.loc[d.fold.ne(fold)];hold=d.loc[d.fold.eq(fold)]
 assert set(fit.id_municipio).isdisjoint(hold.id_municipio)
 prior=fit.nao_alfabetizados.sum()/fit.n.sum()
 rates=fit.groupby('sigla_uf')[['n','nao_alfabetizados']].sum();rates=rates.nao_alfabetizados/rates.n
 assert set(hold.sigla_uf)<=set(rates.index)
 d.loc[hold.index,'p_global']=prior;d.loc[hold.index,'p_uf']=hold.sigla_uf.map(rates)
 prevalence=hold.nao_alfabetizados.sum()/hold.n.sum()
 for name in names:
  p=d.loc[hold.index,'p_'+name].to_numpy();m=metric(hold,p)
  if name=='global':assert abs(m['AP']-prevalence)<1e-12
  records.append({'modelo':name,'fold':fold,'municipios':len(hold),'alunos':int(hold.n.sum()),'prevalencia_holdout':float(prevalence),'prevalencia_ajuste':float(prior),**m})
summary=[]
uf_ap=np.mean([x['AP'] for x in records if x['modelo']=='uf'])
global_ap=np.mean([x['AP'] for x in records if x['modelo']=='global'])
for name in names:
 rr=[x for x in records if x['modelo']==name];ap=float(np.mean([x['AP'] for x in rr]))
 summary.append({'modelo':name,'AP_media_folds':ap,'AP_desvio_folds':float(np.std([x['AP'] for x in rr],ddof=1)),'delta_AP_vs_global':ap-global_ap,'delta_AP_vs_UF':ap-uf_ap,'razao_AP_vs_global':ap/global_ap,'OOF':metric(d,d['p_'+name].to_numpy())})
byuf=[]
for name in names:
 for uf,g in d.groupby('sigla_uf'):byuf.append({'modelo':name,'uf':uf,'alunos':int(g.n.sum()),'municipios':len(g),**metric(g,g['p_'+name].to_numpy())})
result={'data':'2026-10-28','classe_positiva':'não alfabetizado','alunos':int(d.n.sum()),'municipios':len(d),'prevalencia_treino':float(d.nao_alfabetizados.sum()/d.n.sum()),'prevalencia_media_folds':global_ap,'resumo':summary,'folds':records,'fonte_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'regras':['Baselines estimados somente nos folds de ajuste.','Scores dos modelos reutilizados da CV anterior, sem novos ajustes.','AP média e AP OOF agrupada são medidas distintas.','Bootstrap e resultados de desenvolvimento anteriores não constituem confirmação independente.'],'verificacoes':{'AP_constante_igual_prevalencia_em_cada_fold':True,'municipios_separados':True,'todas_UFs_holdout_presentes_no_ajuste':True,'scores_completos':bool(d[['p_'+n for n in names]].notna().all().all()),'sem_acesso_a_validacao_ou_teste':True}}
(OUT/'comparacao_baselines.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
(OUT/'metricas_baselines_por_uf.json').write_text(json.dumps(byuf,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'prevalencia':result['prevalencia_treino'],'resumo':summary},ensure_ascii=False,indent=2))
