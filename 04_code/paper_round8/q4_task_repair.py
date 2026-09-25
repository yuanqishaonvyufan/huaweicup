"""Read-only Q4 scale coverage audit and exogenous benchmark-space scenarios."""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'06_results/raw/Q4_TASK_REPAIR_20260925_v1';OUT.mkdir(parents=True,exist_ok=True)
P=ROOT/'01_data/processed/modeling_phase4/round7/Q4_PRIMARY_v1.csv'
F=ROOT/'06_results/raw/EXP-Q4-R7-20260925-v1/frontier_family.csv'
DEC=ROOT/'06_results/raw/EXP-Q4-R7-20260925-v1/decomposition_changes.csv'
FORE=ROOT/'06_results/raw/EXP-Q4-R7-20260925-v1/forecast_summary.json'
ROL=ROOT/'06_results/raw/EXP-Q4-R7-20260925-v1/rolling_metrics.csv'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reg(y,x):
 b,*_=np.linalg.lstsq(x,y,rcond=None)
 fit=x@b
 return dict(coefficients=[float(t) for t in b],n=int(len(y)),rank=int(np.linalg.matrix_rank(x)),condition=float(np.linalg.cond(x)),rmse=float(np.sqrt(np.mean((fit-y)**2))))
p=pd.read_csv(P)
assert len(p)==853 and p.canonical.nunique()==853
strict=p[(p.D_primary_usable==True)&(p.model_type=='base')&(p.N_B>0)&(p.D_B>0)&(p.C4_compute_FLOP>0)].copy()
assert len(strict)==6
strict['compute_ratio_to_6ND']=strict.C4_compute_FLOP/(6e18*strict.N_B*strict.D_B)
strict['consistent_6ND_proxy']=strict.compute_ratio_to_6ND.between(.8,1.2)
strict[['Model','evaluation_date','model_type','family','N_B','D_B','C4_compute_FLOP','compute_ratio_to_6ND','consistent_6ND_proxy','training_tokens_source','score_raw6']].to_csv(OUT/'FULL_SCALE_SUBSET_ENTITIES_v1.csv',index=False)
def fit_nd(frame):
 x=np.column_stack([np.ones(len(frame)),np.log(frame.N_B),np.log(frame.D_B)])
 return reg(frame.score_raw6.to_numpy(float),x)
allfit=fit_nd(strict)
consistent=strict[strict.consistent_6ND_proxy]
consfit=fit_nd(consistent)
loo=[]
for _,row in strict.iterrows():
 f=fit_nd(strict[strict.Model!=row.Model]);loo.append(dict(left_out=row.Model,n=f['n'],rank=f['rank'],logN=f['coefficients'][1],logD=f['coefficients'][2],rmse=f['rmse']))
pd.DataFrame(loo).to_csv(OUT/'FULL_SCALE_SUBSET_LOO_v1.csv',index=False)
compute=p[(p.model_type=='base')&(p.C4_compute_FLOP>0)].copy();assert len(compute)==16
compfit=reg(compute.score_raw6.to_numpy(float),np.column_stack([np.ones(len(compute)),np.log(compute.C4_compute_FLOP)]))
comp=pd.DataFrame(compute[['Model','N_B','C4_compute_FLOP','score_raw6','evaluation_date','family','C4_match']]);comp.to_csv(OUT/'C4_COMPUTE_DIAGNOSTIC_ENTITIES_v1.csv',index=False)
front=pd.read_csv(F);dec=pd.read_csv(DEC);forecast=json.loads(FORE.read_text(encoding='utf-8'))
beta=float(dec.loc[dec.model=='family','beta_logN'].iloc[0]);first,last=front.iloc[0],front.iloc[-1]
delta_ln=float(last.frontier_logN-first.frontier_logN);weeks=float(last.t_week-first.t_week)
g=delta_ln/weeks
assert g>0 and abs(beta-4.595943203340986)<1e-8
rows=[];origin=pd.Timestamp(forecast['origin'])
for f in forecast['forecast']:
 target=pd.Timestamp(f['target']);h=(target-origin).days/7
 for rho,label in [(1.0,'NO_SLOWDOWN_REFERENCE'),(.5,'MODERATE_EXOGENOUS_SLOWDOWN'),(0.0,'STRONG_EXOGENOUS_SLOWDOWN')]:
  delta=(rho-1)*beta*g*h;center=float(np.clip(f['central']+delta,0,100))
  rows.append(dict(target=f['target'],scenario=label,rho=rho,baseline_dynamic_center=f['central'],reference_log_compute_growth_per_week=g,assumed_D_growth='FIXED_ZERO',reference_parameter_associated_increment=beta*g*h,score_shift=delta,conditional_frontier_center=center,source_kind='EXOGENOUS_CONDITIONAL_NOT_IDENTIFIED_EFFECT',conditional_PI95_only_for_reference=json.dumps(f['conditional_PI95']) if rho==1 else '',model_center_range_only_for_reference=json.dumps(f['model_range']) if rho==1 else ''))
pd.DataFrame(rows).to_csv(OUT/'EXOGENOUS_COMPUTE_SLOWDOWN_SCENARIOS_v1.csv',index=False)
rolling=pd.read_csv(ROL);available=rolling.groupby('horizon_weeks').n.max().to_dict()
assert available=={4:20,13:11}
summary=dict(run_id='Q4_TASK_REPAIR_20260925_v1',input_hashes={x.name:sha(x) for x in [P,F,DEC,FORE,ROL]},full_scale_subset=dict(n_D_observed=int(p.D_B.notna().sum()),n_D_primary_usable=int(p.D_primary_usable.sum()),n_strict=len(strict),n_compute_consistent=len(consistent),n_compute_only=len(compute),N_plus_D_6=allfit,N_plus_D_5=consfit,LOO_logN_range=[float(min(r['logN'] for r in loo)),float(max(r['logN'] for r in loo))],LOO_logD_range=[float(min(r['logD'] for r in loo)),float(max(r['logD'] for r in loo))],compute_only_16=compfit,full_853_ND_share='NOT_IDENTIFIED'),scenario_reference=dict(first_date=str(first.date),last_date=str(last.date),first_frontier_logN=float(first.frontier_logN),last_frontier_logN=float(last.frontier_logN),weeks=weeks,delta_logN=delta_ln,reference_log_growth_per_week=g,theta_N=beta,compute_assumption='C≈6ND and D fixed; exogenous benchmark-space scenario'),scenarios=rows,rolling_available=available,unavailable_horizons_weeks=[26,52],thirty_to_forty_two_month_validation='UNAVAILABLE',outputs={})
for f in OUT.iterdir():
 if f.name!='summary.json':summary['outputs'][f.name]=sha(f)
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'subset':summary['full_scale_subset'],'reference':summary['scenario_reference'],'scenarios':rows,'rolling_available':available},ensure_ascii=False,indent=2))
