"""Independent saved-result arithmetic and provenance audit, no optimization."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
RUNS=['EXP-Q3-BASE-R6-20260924-v1','SCEN-Q3-R6-20260924-v1','UNC-Q3-R6-20260924-v1']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    cfg=json.loads((ROOT/'05_experiments/configs/Q3_R6_FROZEN_v1.json').read_text());checks={};p=cfg['parameters'];nb=cfg['N_bounds'];db=cfg['D_bounds']
    checks['frozen_sources_specs']=all(sha(ROOT/f)==h for f,h in {**cfg['inputs'],**cfg['spec_hashes']}.items())
    summaries={}
    for name in RUNS:
        dr=ROOT/'06_results/raw'/name;m=json.loads((dr/'output_manifest.json').read_text());checks[name+'_hashes']=all(sha(dr/f)==h for f,h in m.items());summaries[name]=json.loads((dr/'summary.json').read_text())
    checks['valid_run_status']=all(s['status']=='PASS' for s in summaries.values())
    b=ROOT/'06_results/raw'/RUNS[0];s=ROOT/'06_results/raw'/RUNS[1];u=ROOT/'06_results/raw'/RUNS[2]
    baseline=pd.read_csv(b/'budget_path.csv');quality=pd.read_csv(s/'quality_context_path.csv');context=pd.read_csv(s/'context_baseline.csv')
    for label,d in [('baseline',baseline),('quality',quality),('context',context)]:
        n=d.N_B.to_numpy();dt=d.D_B.to_numpy();q=d.Q.to_numpy();L=d.L_ctx.to_numpy();C=d.Budget_FLOPs.to_numpy()
        benefit=np.zeros(len(d)) if label!='quality' else d.factor.to_numpy()*cfg['quality_g']*(q-.5)
        f=p['E']+p['A']/n**p['alpha']+p['B']/dt**p['beta']-benefit
        checks[label+'_objective']=np.allclose(f,d.loss,rtol=0,atol=1e-12)
        cq=np.zeros(len(d))
        if label=='quality':
            for i,(_,row) in enumerate(d.iterrows()):
                qq=row.Q
                if row.cost_family=='exponential':delta=1e7*(np.exp(6*qq)-np.exp(3))
                elif row.cost_family=='power':delta=5e9*(qq**4-.5**4)
                else:delta=2e9*(np.log(1+10*qq)-np.log(6))
                cq[i]=1e9*row.D_B*max(0,delta)
        used=6e18*n*dt+.0002*L*1e18*n*dt+cq
        checks[label+'_cost_units']=np.allclose(used,d.total_FLOPs,rtol=1e-12) and np.allclose(cq,d.quality_FLOPs,rtol=1e-10,atol=1)
        checks[label+'_budget']=bool(np.max((used-C)/C)<1e-8)
        checks[label+'_support']=bool(((n>=nb[0]-1e-10)&(n<=nb[1]+1e-10)&(dt>=db[0]-1e-10)&(dt<=db[1]+1e-10)).all())
        checks[label+'_kkt']=bool(d.kkt_projected_max.max()<1e-6 and d.complementarity.max()<1e-6)
        group=['scenario'] if label=='quality' else ['L_ctx']
        checks[label+'_budget_monotonicity']=all(g.sort_values('Budget_FLOPs').loss.diff().max()<1e-9 for _,g in d.groupby(group))
    checks['quality_bounds']=bool((quality.Q>=.5-1e-9).all() and (quality.Q<=quality.qcap+1e-9).all())
    off=quality[(quality.factor==0)&(quality.qcap==1)]
    checks['quality_OFF_exact_baseline']=all(np.allclose(g.sort_values('Budget_FLOPs').loss,baseline.sort_values('Budget_FLOPs').loss,atol=1e-12) and np.allclose(g.Q,.5) for _,g in off.groupby('cost_family'))
    start=pd.read_csv(s/'quality_multistart.csv');best=start[start.success & start.constraint.ge(-1e-8)].groupby(['scenario','Budget_FLOPs']).loss_gap.min()
    checks['every_scenario_numeric_agrees']=len(best)==len(quality) and best.abs().max()<1e-6
    checks['failed_and_local_starts_preserved']=(~start.success).sum()==4 and (start.loss_gap>1e-6).sum()==17
    mix=pd.read_csv(s/'mixture_local_candidates.csv');qb=json.loads((ROOT/'03_models/modeling_phase1/q1/round4/P_RESPONSE_FROZEN_MODEL_BUNDLE_v1.json').read_text());P=np.array(qb['training_p_matrix']);p0=P.mean(0);expected=np.vstack([p0,(P+p0)/2]);observed=mix[qb['p_columns']].to_numpy()
    checks['mixture_hull_witness']=np.allclose(observed,expected,atol=1e-14) and observed.min()>=0 and np.max(abs(observed.sum(1)-1))<1e-10
    coef=np.array(qb['basis'])@np.array(qb['models']['M1']['coef']);checks['mixture_all13_recomputed']=np.allclose((observed-p0)@coef,mix[['delta_'+s for s in qb['loss_columns']]],atol=1e-12)
    checks['main_mixture_prohibited']=cfg['mixture_main_transport']==0 and pd.read_csv(s/'mixture_scenarios.csv').B1_joint_use.eq('FORBIDDEN_NO_SCALE_OVERLAP').all()
    checks['context_observation_boundary']=cfg['contexts']==[2048,4096,8192,32768,131072] and not json.loads((ROOT/'01_data/audits/modeling_phase3/round6/Q3_COST_AUDIT_METRICS_v1.json').read_text())['train_context_observed']
    draws=pd.read_csv(u/'conditional_draw_paths.csv.gz');bp=pd.read_csv(ROOT/'06_results/raw/EXP-Q2-ND-R5-20260924-v1/cluster_bootstrap.csv').set_index('replicate');pp=bp.loc[draws.replicate]
    vv=pp.E.to_numpy()+pp.A.to_numpy()/draws.N_B.to_numpy()**pp.alpha.to_numpy()+pp.B.to_numpy()/draws.D_B.to_numpy()**pp.beta.to_numpy()
    checks['joint_draws_loss_recomputed']=len(draws)==51000 and draws.replicate.nunique()==200 and np.allclose(vv,draws.loss,atol=1e-12)
    checks['all_draw_budget_paths_monotone']=all(g.sort_values('Budget_FLOPs').loss.diff().max()<1e-10 for _,g in draws.groupby(['replicate','L_ctx']))
    sh=pd.read_csv(u/'shadow_prices.csv');checks['shadow_finite_difference']=sh.abs_error.max()<1e-6
    checks['scenario_envelope_not_CI']=summaries[RUNS[2]]['scenario_envelope_is_CI']==False
    checks['Q4_not_started']=all(not ss['Q4_started'] for ss in summaries.values())
    result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':{k:bool(v) for k,v in checks.items()},'scope':'Q3 conditional numeric validation; not Gate4 or external validation','code_sha256':sha(__file__)}
    (ROOT/'10_review/MODELING_PHASE3_R6_NUMERICAL_QA_20260924.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2));assert all(checks.values())
if __name__=='__main__':main()
