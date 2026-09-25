"""Supplementary Q1 rubric and estimated extrapolation; frozen M1 is never fit."""
from pathlib import Path
import hashlib, json, sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, rankdata
from scipy.spatial import cKDTree
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'06_results/raw/Q1_TASK_REPAIR_20260925_v1';OUT.mkdir(parents=True,exist_ok=True)
F=ROOT/'01_data/processed/modeling_phase1/round3/q1_quality_features_v1.csv.gz'
MAN=ROOT/'01_data/processed/modeling_phase1/round3/INPUT_MANIFEST_v1.json'
BUNDLE=ROOT/'03_models/modeling_phase1/q1/round4/P_RESPONSE_FROZEN_MODEL_BUNDLE_v1.json'
RAW=ROOT/'01_data/raw/real_attachments/A_data_value/regmix_tables'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,x):(OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def check(c,msg):
 if not c:raise ValueError(msg)
manifest=json.loads(MAN.read_text(encoding='utf-8'));check(sha(F)==manifest['processed']['quality']['sha256'],'frozen features changed')
bundle=json.loads(BUNDLE.read_text(encoding='utf-8'))
df=pd.read_csv(F,compression='gzip',dtype={'id':str,'source':str,'domain':str})
check(len(df)==272505 and df.id.nunique()==261086,'sample mismatch')
source=df.source.to_numpy();domain=df.domain.to_numpy();n=len(df)
is_check=np.fromiter((int.from_bytes(hashlib.sha256(str(x).encode()).digest()[:8],'big')%5==0 for x in df.id),dtype=bool,count=n)
train=(source=='A1') & ~is_check
check(train.sum()==40926,'A1 reference mismatch')
core=['fineweb_edu','fluency_en','ad_en','modernbert_cleanliness','modernbert_readability']
cols=bundle['p_columns']
fields=[x['signal_id'] for x in pd.read_csv(ROOT/'03_models/modeling_phase1/q1/round4/Q1_FULL22_ROLE_MAP_v1.csv').to_dict('records')]
check(len(fields)==22,'22-field map mismatch')
def ecdf(ref,vals):
 ref=np.sort(np.asarray(ref,dtype=float));ref=ref[np.isfinite(ref)]
 vals=np.asarray(vals,dtype=float);left=np.searchsorted(ref,vals,'left');right=np.searchsorted(ref,vals,'right')
 out=(left+right)/(2*len(ref));out[~np.isfinite(vals)]=np.nan
 return out
core_u=np.column_stack([ecdf(df.loc[train,c],df[c]) for c in core]);dq0=np.nanmean(core_u,axis=1)
high=train & (dq0>=np.quantile(dq0[train],.8))
utils=np.empty((n,22),dtype=np.float32);targets=[];rules=[]
for j,f in enumerate(fields):
 if f=='qurater':
  us=[];ts=[]
  for facet in [f'qurater_facet_{k}' for k in range(4)]:
   raw=df[facet].to_numpy(float);ref=raw[train];v=ecdf(ref,raw)
   t=float(np.nanmedian(v[high]));us.append(1-np.abs(v-t));ts.append(t)
  u=np.nanmean(np.array(us),axis=0);targets.append(ts);rule='four-facet median-target proximity, then mean'
 else:
  raw=df[f].to_numpy(float)
  if f in ['rps_doc_word_count','rps_doc_num_sentences']:raw=np.log1p(np.maximum(raw,0))
  v=ecdf(raw[train],raw)
  if f in core:u=v;targets.append(None);rule='source-supported increasing description'
  else:
   t=float(np.nanmedian(v[high]));u=1-np.abs(v-t);targets.append(t);rule='high-core-reference proximity; no universal raw direction'
 utils[:,j]=u;rules.append(rule)
missing=np.isnan(utils);coverage=22-missing.sum(axis=1)
u=np.where(missing,0.5,utils).astype(np.float32)
w0=np.repeat(1/22,22)
rho=spearmanr(u[train],axis=0).statistic
pen=np.maximum(0,np.abs(rho)-.5);np.fill_diagonal(pen,0)
w1=1/(1+pen.sum(axis=1));w1/=w1.sum()
qfull=u@w0;qfull1=u@w1
out=pd.DataFrame({'id':df.id,'source':source,'domain':domain,'Q_full_W0':qfull,'Q_full_W1':qfull1,'DQ0':dq0,'n_observed_signals':coverage})
out.to_csv(OUT/'Q_FULL_SAMPLE_SCORES_v1.csv.gz',index=False,compression={'method':'gzip','compresslevel':6})
ids_a1=set(df.loc[source=='A1','id']);ext=np.array([s=='A1' or id not in ids_a1 for s,id in zip(source,df.id)])
labels=np.where(source=='A1','A1_'+domain,np.where(ext,source+'_new_ids',source+'_overlap'))
rng=np.random.default_rng(20260925);groups=[]
for lab in sorted(set(labels)):
 mask=labels==lab;idx=np.flatnonzero(mask);n0=len(idx)
 if n0==0:continue
 a=qfull[idx];b=qfull1[idx];d=dq0[idx]
 if n0>1:
  boots=np.array([np.mean(a[rng.integers(0,n0,n0)]) for _ in range(200)])
  lo,hi=np.quantile(boots,[.025,.975])
 else:lo=hi=float(a[0])
 groups.append(dict(group=lab,n=n0,Q_full_mean=float(a.mean()),Q_full_median=float(np.median(a)),Q_full_p25=float(np.quantile(a,.25)),Q_full_p75=float(np.quantile(a,.75)),mean_boot_p025=float(lo),mean_boot_p975=float(hi),W1_mean=float(b.mean()),DQ0_mean=float(d.mean()),mean_coverage=float(coverage[idx].mean())))
pd.DataFrame(groups).to_csv(OUT/'Q_FULL_DOMAIN_RESULTS_v1.csv',index=False)
a1=[g for g in groups if g['group'].startswith('A1_')]
rank_w0={g['group']:rank+1 for rank,g in enumerate(sorted(a1,key=lambda z:z['Q_full_mean'],reverse=True))}
rank_w1={g['group']:rank+1 for rank,g in enumerate(sorted(a1,key=lambda z:z['W1_mean'],reverse=True))}
pd.DataFrame([dict(group=g['group'],W0_rank=rank_w0[g['group']],W1_rank=rank_w1[g['group']],**{k:g[k] for k in ['Q_full_mean','W1_mean','DQ0_mean']}) for g in a1]).to_csv(OUT/'Q_FULL_A1_RANKS_v1.csv',index=False)
contract=pd.DataFrame(dict(field=fields,rule=rules,target_percentile=targets,weight_W0=w0,weight_W1=w1,missing_n=missing.sum(axis=0),source_role=pd.read_csv(ROOT/'03_models/modeling_phase1/q1/round4/Q1_FULL22_ROLE_MAP_v1.csv')['full22_role']))
contract.to_csv(OUT/'Q_FULL_FIELD_CONTRACT_v1.csv',index=False)
qsummary=dict(run_id='Q1_TASK_REPAIR_20260925_v1',input_hash=sha(F),bundle_hash=sha(BUNDLE),rows=n,unique_ids=int(df.id.nunique()),A1_reference=int(train.sum()),high_core_reference=int(high.sum()),min_observed=int(coverage.min()),complete_case_rows=int((coverage==22).sum()),A1_domain_rank_spearman_W0_W1=float(spearmanr([rank_w0[x] for x in sorted(rank_w0)],[rank_w1[x] for x in sorted(rank_w0)]).statistic),weights=dict(zip(fields,map(float,w1))),outputs={})

# A12-A15: frozen M1 response-shape check only, no scale intercept calibration.
H=np.asarray(bundle['basis'],float)
def pred(kind,p):
 m=bundle['models'][kind];ym=np.asarray(m['ymean'],float)
 if kind=='M0':return np.tile(ym,(len(p),1))
 return ym+(p-np.asarray(m['pmean'],float))@H@np.asarray(m['coef'],float)
trainp=np.asarray(bundle['training_p_matrix'],float);ztrain=(trainp-trainp.mean(axis=0))@H;tree=cKDTree(ztrain)
refq=json.loads((ROOT/'03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_METRICS_v2.json').read_text(encoding='utf-8'))
q95=refq['support_thresholds']['train_loo_NN_q95'];q99=refq['support_thresholds']['train_loo_NN_q99']
exrows=[];prediction_rows=[]
for scale,sfx in [('10B','10b'),('70B','70b')]:
 pf=RAW/f'est_mixture_{sfx}.csv';yf=RAW/f'est_pile_loss_{sfx}.csv'
 pdat=pd.read_csv(pf);ydat=pd.read_csv(yf)
 check(list(pdat.columns)==['index',*bundle['p_columns']] and list(ydat.columns)==['index',*bundle['loss_columns']],scale+' columns')
 merged=pdat.merge(ydat,on='index',validate='one_to_one').sort_values('index')
 check(len(merged)==len(pdat)==len(ydat) and merged['index'].is_unique,scale+' pairing')
 p=merged[cols].to_numpy(float);y=merged[bundle['loss_columns']].to_numpy(float)
 check(np.isfinite(p).all() and np.isfinite(y).all() and p.min()>=0,scale+' invalid data')
 sums=p.sum(axis=1);check((sums>.99).all() and (sums<1.01).all(),scale+' simplex sum');p=p/sums[:,None]
 m0=pred('M0',p);m1=pred('M1',p);r=y.mean(axis=1);r0=m0.mean(axis=1);r1=m1.mean(axis=1)
 cy=r-r.mean();cp=r1-r1.mean();rm0=float(np.sqrt(np.mean(cy**2)));rm1=float(np.sqrt(np.mean((cy-cp)**2)))
 d,_=tree.query((p-trainp.mean(axis=0))@H,k=1)
 hull=[]
 for row in p:
  sol=linprog(np.zeros(len(trainp)),A_eq=trainp.T,b_eq=row,bounds=(0,None),method='highs')
  hull.append(bool(sol.success and np.max(np.abs(trainp.T@sol.x-row))<1e-7 and abs(sol.x.sum()-1)<1e-7))
 in_n=int(np.sum(hull));near=int(np.sum((d<=q99)|hull));out_n=len(p)-near
 row=dict(scale=scale,n=len(p),source_kind='ESTIMATED_EXTRAPOLATION_CHECK',p_sha256=sha(pf),loss_sha256=sha(yf),r0_centered_rmse_M0=rm0,r0_centered_rmse_M1=rm1,centered_ratio_M1_to_M0=rm1/rm0,r0_spearman=float(spearmanr(r,r1).statistic),direction_concordance=float(np.mean(np.sign(r-r.mean())==np.sign(r1-r1.mean()))),mean_domain_centered_ratio=float(np.mean(np.sqrt(np.mean(((y-y.mean(axis=0))-(m1-m1.mean(axis=0)))**2,axis=0))/np.sqrt(np.mean((y-y.mean(axis=0))**2,axis=0)))),strict_hull_in=in_n,near_by_existing_q99=near,strict_or_near=near,outside=out_n,nearest_median=float(np.median(d)),q95_distance=q95,q99_distance=q99)
 exrows.append(row)
 for i,idx in enumerate(merged['index']):prediction_rows.append(dict(scale=scale,index=int(idx),observed_R0=float(r[i]),predicted_R0_M1=float(r1[i]),centered_observed=float(cy[i]),centered_predicted=float(cp[i]),nearest_training_distance=float(d[i]),inside_train_hull=bool(hull[i])))
pd.DataFrame(exrows).to_csv(OUT/'A12_A15_EXTRAPOLATION_CHECK_v1.csv',index=False)
pd.DataFrame(prediction_rows).to_csv(OUT/'A12_A15_PREDICTIONS_v1.csv',index=False)
qsummary['extrapolation']=exrows
for file in OUT.iterdir():
 if file.name!='summary.json':qsummary['outputs'][file.name]=sha(file)
dump('summary.json',qsummary)
print(json.dumps({'Q_full_A1':a1,'ranking_rho':qsummary['A1_domain_rank_spearman_W0_W1'],'extrapolation':exrows,'complete_case_rows':qsummary['complete_case_rows']},ensure_ascii=False,indent=2))
