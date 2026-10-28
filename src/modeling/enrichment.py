from pathlib import Path
import sys,json,hashlib,warnings,time
ROOT=Path(__file__).resolve().parents[2]

import numpy as np,pandas as pd,sklearn
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score,roc_auc_score,brier_score_loss,log_loss
import argparse
parser=argparse.ArgumentParser(description='CV municipal dos blocos de enriquecimento; somente treino')
parser.add_argument('--output',type=Path,default=ROOT/'work/enriquecimento_reproduzido')
args=parser.parse_args()
OUT=args.output.resolve()
if OUT.exists(): raise FileExistsError('Escolha uma saída nova para preservar os resultados anteriores')
OUT.mkdir(parents=True)
paths={'base':ROOT/'data/processed/dados_analiticos_municipais.json','contexto':ROOT/'data/processed/contexto_municipal_candidato.json','pnad':ROOT/'data/processed/contexto_pnad_uf.json','folds':ROOT/'data/splits/folds_treino.json','teste_fechado':ROOT/'reports/avaliacao-final/protocolo_teste_fixado.json'}
hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()}
base=pd.DataFrame(json.loads(paths['base'].read_text(encoding='utf8')))
d=base.loc[base.conjunto.eq('treino')].copy();del base
ctx=pd.read_json(paths['contexto'],dtype={'id_municipio':str});pnad=pd.read_json(paths['pnad']);folds=pd.read_json(paths['folds'],dtype={'id_municipio':str})
d=d.merge(ctx,on='id_municipio',how='left',validate='1:1').merge(pnad,on='sigla_uf',how='left',validate='m:1').merge(folds,on='id_municipio',how='left',validate='1:1').sort_values('id_municipio').reset_index(drop=True)
assert len(d)==3267 and d.n.sum()==968939 and d.id_municipio.is_unique and d.fold.notna().all()
assert set(folds.id_municipio)==set(d.id_municipio) and set(d.fold)=={0,1,2}
from src.preprocessing.features import NUMERIC
nums=list(NUMERIC)
blocks={'referencia':[], 'INSE':['inse_municipal_2021','inse_niveis_1_2_pct_2021'], 'distorcao':['tdi_AI_pct_2022','tdi_2ano_pct_2022'], 'rendimento':['reprovacao_AI_pct_2022','abandono_AI_pct_2022','reprovacao_2ano_pct_2022','abandono_2ano_pct_2022'], 'FUNDEB':['vaat_antes_reais_2023'], 'PNAD':['renda_domiciliar_pc_UF_2022']}
blocks['combinado']=blocks['distorcao']+blocks['rendimento']
protocol={'data':'2026-10-27','escopo':'Treino exclusivamente. Sem ajuste na validação externa ou teste; sem substituição do modelo v1.','alvo':'não alfabetizado = 1 - alfabetizado','blocos':blocks,'referencia_numerica':nums,'categoricas':['sigla_uf'],'modelo':{'classe':'LogisticRegression','C':1.,'solver':'lbfgs','max_iter':3000,'tol':1e-8,'random_state':42},'folds':'Os mesmos 3 folds municipais anteriores, estratificados por UF, semente 42. Não são repetições independentes.','metrica_primaria':'Média simples da AP nos 3 folds; comparação pareada com referência','metricas_secundarias':['AP OOF agrupada','ROC AUC','Brier','log loss','calibração por faixas fixas','AP por UF'],'preprocessamento':'Mediana, indicadores de ausência para colunas com ausência observada no fold, StandardScaler e one-hot ajustados só em municípios de ajuste de cada fold, com peso igual por município.','pesos':'Contagens de alunos em duas linhas por município/classe; não pesos amostrais INEP.','rendimento':'Aprovação omitida para evitar dependência linear com reprovação e abandono.','fundeb':'Somente VAAT anterior à complementação. Não testar receita total sem denominador compatível.','pnad':'Experimento de redundância: renda da UF é função das dummies já existentes. A regularização pode mudar previsões sem nova informação.','incerteza':'Bootstrap pareado estratificado por UF de municípios com previsões OOF fixas, 500 réplicas, semente 42; intervalo condicional, sem refazer ajuste e seleção, não confirmação independente.','hashes_entrada':hashes,'versoes':{'sklearn':sklearn.__version__,'numpy':np.__version__,'pandas':pd.__version__}}
(OUT/'protocolo.json').write_text(json.dumps(protocol,ensure_ascii=False,indent=2),encoding='utf8')
def expanded(g,p=None):
 y=np.r_[np.ones(len(g)),np.zeros(len(g))];w=np.r_[g.nao_alfabetizados,g.alfabetizados].astype(float)
 return y,w,np.r_[p,p] if p is not None else None
def metrics(g,p):
 y,w,p=expanded(g,p)
 return {'AP':float(average_precision_score(y,p,sample_weight=w)),'ROC_AUC':float(roc_auc_score(y,p,sample_weight=w)),'Brier':float(brier_score_loss(y,p,sample_weight=w)),'log_loss':float(log_loss(y,p,sample_weight=w))}
records=[];oofs={};notes=[];coverage=[]
for name,extra in blocks.items():
 oof=np.full(len(d),np.nan)
 covered=d[extra].notna().all(axis=1) if extra else pd.Series(True,index=d.index)
 coverage.append({'bloco':name,'municipios_completos':int(covered.sum()),'alunos_completos':int(d.loc[covered,'n'].sum()),'alunos_pct':float(d.loc[covered,'n'].sum()/d.n.sum()*100)})
 for fold in range(3):
  started=time.monotonic();fit=d.loc[d.fold.ne(fold)];hold=d.loc[d.fold.eq(fold)]
  assert set(fit.id_municipio).isdisjoint(hold.id_municipio)
  pre=ColumnTransformer([('numerico',Pipeline([('imputacao',SimpleImputer(strategy='median',add_indicator=True)),('escala',StandardScaler())]),nums+extra),('uf',OneHotEncoder(handle_unknown='ignore',sparse_output=False),['sigla_uf'])],sparse_threshold=0)
  x=pre.fit_transform(fit);hx=pre.transform(hold);y,w,_=expanded(fit)
  model=LogisticRegression(**{k:v for k,v in protocol['modelo'].items() if k!='classe'})
  with warnings.catch_warnings(record=True) as caught:
   warnings.simplefilter('always');model.fit(np.r_[x,x],y,sample_weight=w)
  notes.extend({'bloco':name,'fold':fold,'aviso':str(z.message)} for z in caught)
  assert model.n_iter_.max()<model.max_iter
  p=model.predict_proba(hx)[:,1];oof[hold.index]=p
  records.append({'bloco':name,'fold':fold,'municipios':len(hold),'alunos':int(hold.n.sum()),'iteracoes':int(model.n_iter_.max()),'segundos':time.monotonic()-started,**metrics(hold,p)})
  print(name,fold,records[-1]['AP'],flush=True)
 assert np.isfinite(oof).all();oofs[name]=oof
ref=[x for x in records if x['bloco']=='referencia'];summary=[];byuf=[];calibration=[]
for name in blocks:
 rr=[x for x in records if x['bloco']==name];deltas=[x['AP']-ref[i]['AP'] for i,x in enumerate(rr)]
 summary.append({'bloco':name,'AP_media_folds':float(np.mean([x['AP'] for x in rr])),'AP_desvio_folds':float(np.std([x['AP'] for x in rr],ddof=1)),'delta_AP_media':float(np.mean(deltas)),'delta_AP_por_fold':deltas,'OOF':metrics(d,oofs[name])})
 for uf,g in d.groupby('sigla_uf'):
  p=oofs[name][g.index];byuf.append({'bloco':name,'uf':uf,'municipios':len(g),'alunos':int(g.n.sum()),**metrics(g,p)})
 bins=np.minimum((oofs[name]*10).astype(int),9)
 for b in range(10):
  mask=bins==b;g=d.loc[mask]
  if not len(g):continue
  calibration.append({'bloco':name,'faixa_inferior':b/10,'faixa_superior':(b+1)/10,'municipios':len(g),'alunos':int(g.n.sum()),'probabilidade_media':float(np.average(oofs[name][mask],weights=g.n)),'frequencia_observada':float(g.nao_alfabetizados.sum()/g.n.sum())})
rng=np.random.default_rng(42);ufidx=[g.index.to_numpy() for _,g in d.groupby('sigla_uf')];y,w,_=expanded(d);boot={k:[] for k in blocks if k!='referencia'}
for _ in range(500):
 count=np.zeros(len(d))
 for ids in ufidx:
  drawn=rng.choice(ids,size=len(ids),replace=True);count+=np.bincount(drawn,minlength=len(d))
 ww=w*np.r_[count,count];r=average_precision_score(y,np.r_[oofs['referencia'],oofs['referencia']],sample_weight=ww)
 for name in boot:boot[name].append(float(average_precision_score(y,np.r_[oofs[name],oofs[name]],sample_weight=ww)-r))
for row in summary:
 if row['bloco']=='referencia':continue
 row['IC95_delta_AP_OOF_condicional']=[float(x) for x in np.quantile(boot[row['bloco']],[.025,.975])]
 row['delta_AP_OOF']=row['OOF']['AP']-summary[0]['OOF']['AP']
assert hashes=={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()}
result={'resumo':summary,'folds':records,'cobertura':coverage,'avisos':notes,'integridade_entradas_preservada':True,'teste_reavaliado':False}
for filename,obj in [('resultados.json',result),('metricas_por_uf.json',byuf),('calibracao.json',calibration)]:
 (OUT/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
pd.DataFrame({'id_municipio':d.id_municipio,'fold':d.fold,'n':d.n,'nao_alfabetizados':d.nao_alfabetizados,**{f'p_{k}':v for k,v in oofs.items()}}).to_json(OUT/'previsoes_oof_municipais.json',orient='records',indent=2)
print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
