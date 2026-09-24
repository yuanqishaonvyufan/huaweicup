"""Independent arithmetic, provenance and no-leakage audit of saved Q2 outputs."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
B=ROOT/'06_results/raw/EXP-Q2-ND-R5-20260924-v1';S=ROOT/'06_results/raw/SCEN-Q2-R5-20260924-v3'
OUT=ROOT/'10_review';checks=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(name,passed,detail=''):
    checks.append(dict(check=name,passed=bool(passed),detail=detail))
def main():
    for dr in [B,S]:
        m=json.loads((dr/'output_manifest.json').read_text())
        check(dr.name+'_output_hashes',all(sha(dr/p)==h for p,h in m.items()))
    conf=json.loads((ROOT/'05_experiments/configs/Q2_R5_v1.json').read_text());summary=json.loads((B/'summary.json').read_text())
    check('spec_frozen',sha(ROOT/conf['spec'])==conf['spec_sha256'])
    check('fit_code_frozen',sha(ROOT/'04_code/modeling_phase2/round5_fit.py')==conf['fit_code_sha256']==summary['code_sha256'])
    sc=json.loads((ROOT/'05_experiments/configs/Q2_R5_SCEN_v3.json').read_text())
    check('scenario_code_and_inputs_frozen',sha(ROOT/'04_code/modeling_phase2/round5_scenarios.py')==sc['code_sha256'] and all(sha(ROOT/p)==h for p,h in sc['inputs'].items()))
    inp=json.loads((ROOT/'01_data/processed/modeling_phase2/round5/INPUT_MANIFEST_v1.json').read_text())
    check('raw_and_processed_hashes',all(sha(ROOT/r['source'])==r['raw_sha256'] and sha(ROOT/r['processed'])==r['processed_sha256'] for r in inp['inputs']))
    data=pd.read_csv(B/'training_predictions.csv').set_index('row_id');params=summary['parameters'];E,A,C,a,b=[params[k] for k in ['E','A','B','alpha','beta']]
    def f(n,d):return E+A/np.power(n,a)+C/np.power(d,b)
    check('full_predictions_recomputed',np.allclose(f(data.N_params_B,data.D_tokens_B),data.prediction,rtol=0,atol=1e-12))
    check('positive_bounds',0<=E<=data.val_loss.min() and 0<A<=20 and 0<C<=20 and .001<=a<=2 and .001<=b<=2)
    splits=json.loads((B/'splits.json').read_text());folds=pd.read_csv(B/'fold_parameters.csv');pv=pd.read_csv(B/'validation_predictions.csv');mv=pd.read_csv(B/'validation_metrics.csv')
    check('fold_counts',len(splits)==18 and len(folds)==18 and mv.groupby(['kind','model']).size().to_dict()=={(k,m):v for k,v in [('LONO',8),('FORWARD',16),('BLOCK2D',8)] for m in ['S0','S1','Slog']})
    for fold in splits:
        tr=data.loc[fold['train']];te=data.loc[fold['test']];kind=fold['kind'];fid=fold['fold']
        okay=not set(tr.index)&set(te.index)
        if kind in ['LONO','BLOCK2D']:okay &= not set(tr.N_params_B)&set(te.N_params_B)
        if kind in ['FORWARD','BLOCK2D']:okay &= tr.D_rank.max()<te.D_rank.min()
        check('split_'+kind+'_'+fid,okay)
        fp=folds[(folds.kind==kind)&(folds.fold==fid)].iloc[0]
        q=pv[(pv.kind==kind)&(pv.fold==fid)&(pv.model=='S1')]
        pp=fp.E+fp.A/np.power(q.N_params_B,fp.alpha)+fp.B/np.power(q.D_tokens_B,fp.beta)
        check('prediction_'+kind+'_'+fid,set(q.row_id)==set(te.index) and np.allclose(pp,q.prediction,atol=1e-12,rtol=0))
    maxerr=0
    for _,r in mv.iterrows():
        z=pv[(pv.kind==r.kind)&(pv.fold==r.fold)&(pv.model==r.model)&(pv.N_params_B==r.N_params_B)]
        maxerr=max(maxerr,abs(float(np.sqrt(np.mean((z.prediction-z.val_loss)**2)))-r.rmse))
    check('all_validation_metrics_recomputed',maxerr<1e-12,str(maxerr))
    for kind,v in summary['validation'].items():
        z=mv[(mv.kind==kind)&(mv.model=='S1')]
        check('macro_'+kind,abs(z.rmse.mean()-v['S1']['macro_rmse'])<1e-12)
    ef=pd.read_csv(B/'marginal_effects.csv');x=ef.N_params_B.to_numpy();y=ef.D_tokens_B.to_numpy();h=1e-5
    dn=(f(x*(1+h),y)-f(x*(1-h),y))/(2*h*x);dd=(f(x,y*(1+h))-f(x,y*(1-h)))/(2*h*y)
    check('derivatives_finite_difference',np.allclose(dn,ef.dL_dN,rtol=1e-6,atol=1e-10) and np.allclose(dd,ef.dL_dD,rtol=1e-6,atol=1e-10))
    check('elasticity_definitions',np.allclose(ef.elasticity_N,ef.dL_dN*ef.N_params_B/ef.loss) and np.allclose(ef.elasticity_D,ef.dL_dD*ef.D_tokens_B/ef.loss))
    check('monotonicity_and_substitution_signs',((ef.dL_dN<0)&(ef.dL_dD<0)&(ef.dD_dN<0)).all())
    nd=json.loads((S/'ND_finite_substitution.json').read_text());check('finite_ND_equal_loss',all(abs(f(r['N_new'],r['D_new'])-f(r['N0'],r['D0']))<1e-10 for r in nd if r['finite_solution']))
    qs=pd.read_csv(S/'quality_substitution_scenarios.csv');errs=[]
    for _,r in qs.iterrows():
        if r.mechanism=='additive':
            vals=[f(r.N_keep_L,r.D0)-r.g*(r.Q1-r.Q0),f(r.N0,r.D_keep_L)-r.g*(r.Q1-r.Q0)]
        else:vals=[f(r.N_keep_L,r.D0*(r.Q1/r.Q0)**r.rho),f(r.N0,r.D_keep_L*(r.Q1/r.Q0)**r.rho)]
        errs.extend(abs(v-r.loss_initial) for v in vals)
    check('quality_substitution_inverse_equations',max(errs)<1e-10,str(max(errs)))
    q=pd.read_csv(ROOT/'01_data/processed/modeling_phase2/round5/B7_v1.csv');xc=q.Q_score-q.groupby(['N_params_B','D_tokens_B']).Q_score.transform('mean');yc=q.val_loss-q.groupby(['N_params_B','D_tokens_B']).val_loss.transform('mean')
    ss=json.loads((S/'summary.json').read_text());g=float(-(xc@yc)/(xc@xc))
    check('quality_common_slope_independent',abs(g-ss['quality_common_g'])<1e-12)
    boot=pd.read_csv(B/'cluster_bootstrap.csv');check('bootstrap_whole_groups',len(boot)==200 and boot['draw'].map(lambda s:len(s.split(';'))==8).all() and not boot.boundary.any(),f'min unique groups={boot.unique_groups.min()}')
    check('no_quality_identification_no_Q3',ss['TYPE_E']==0 and ss['empirical_quality_coefficient'] is None and ss['empirical_AB_transport_coefficient'] is None and not ss['Q3_started'])
    check('no_B8_input',all('large.csv' not in r['source'] or 'supplementary_large' in r['source'] for r in inp['inputs']) and ss['B8']=='QUARANTINED_UNREAD')
    check('failed_runs_isolated',all((ROOT/f'06_results/raw/SCEN-Q2-R5-20260924-v{v}/FAILED.md').exists() for v in [1,2]))
    status='PASS' if all(c['passed'] for c in checks) else 'FAIL'
    result=dict(status=status,scope='Round 5 numerical and lineage QA; not Gate 3',created_utc=datetime.now(timezone.utc).isoformat(),checks=checks,script_sha256=sha(__file__))
    (OUT/'MODELING_PHASE2_R5_NUMERICAL_QA_20260924.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if status!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
