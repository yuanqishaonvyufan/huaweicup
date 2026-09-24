"""Source-separated Q2 diagnostics and explicitly conditional substitutions."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
sys.path.insert(0,str(Path(__file__).resolve().parent))
from round5_fit import pred,metrics,PARS
ROOT=Path(__file__).resolve().parents[2]
INP=ROOT/'01_data/processed/modeling_phase2/round5'
BASE=ROOT/'06_results/raw/EXP-Q2-ND-R5-20260924-v1'
RUN='SCEN-Q2-R5-20260924-v1'; OUT=ROOT/'06_results/raw'/RUN
CONF=ROOT/'05_experiments/configs/Q2_R5_SCEN_v1.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def quality_x(d,interaction):
    q=d.Q_score-d.groupby(['N_params_B','D_tokens_B']).Q_score.transform('mean')
    x=np.array(q)[:,None]
    if interaction:x=np.column_stack([q,q*np.log(d.N_params_B),q*np.log(d.D_tokens_B/100)])
    y=d.val_loss-d.groupby(['N_params_B','D_tokens_B']).val_loss.transform('mean')
    return x,np.array(y)
def main():
    c=json.loads(CONF.read_text());assert sha(__file__)==c['code_sha256']
    for p,h in c['inputs'].items():assert sha(ROOT/p)==h,p
    if OUT.exists():raise RuntimeError('Immutable scenario run exists')
    OUT.mkdir(parents=True)
    summ=json.loads((BASE/'summary.json').read_text());p=np.array([summ['parameters'][k] for k in PARS]);E,A,B,a,b=p
    source_rows=[]
    for lab in ['B2','B4','B5','B10']:
        d=pd.read_csv(INP/f'{lab}_v1.csv');d['B1_scenario_prediction']=pred(p,d.N_params_B,d.D_tokens_B)
        group='N_params_B' if lab=='B2' else 'family'
        d['observed_centered']=d.val_loss-d.groupby(group).val_loss.transform('mean')
        d['predicted_centered']=d.B1_scenario_prediction-d.groupby(group).B1_scenario_prediction.transform('mean')
        d['outside_B1_N']=~d.N_params_B.between(.070542,11.965825);d['outside_B1_D']=~d.D_tokens_B.between(.134,299.893)
        d.to_csv(OUT/f'{lab}_source_diagnostic.csv',index=False)
        for name,g in d.groupby(group):
            if len(g)<2 or g.val_loss.std()==0:continue
            baseline=float(np.sqrt(np.mean(g.observed_centered**2)))
            err=metrics(g.observed_centered,g.predicted_centered)
            pairs=0;agree=0
            for i,ri in g.iterrows():
                for j,rj in g.iterrows():
                    if i==j:continue
                    if ri.N_params_B>=rj.N_params_B and ri.D_tokens_B>=rj.D_tokens_B and (ri.N_params_B>rj.N_params_B or ri.D_tokens_B>rj.D_tokens_B):
                        pairs+=1;agree+=int(ri.val_loss<=rj.val_loss)
            source_rows.append(dict(source=lab,group=str(name),n=len(g),centered_rmse=err['rmse'],
                centered_ratio_to_zero=err['rmse']/baseline,rho=float(spearmanr(g.val_loss,g.B1_scenario_prediction).statistic),
                ordered_pairs=pairs,monotone_agree=agree,outside_N=int(g.outside_B1_N.sum()),outside_D=int(g.outside_B1_D.sum()),
                use='ESTIMATE_COMPARISON_NOT_VALIDATION' if lab=='B10' else 'SOURCE_CENTERED_DIAGNOSTIC'))
    pd.DataFrame(source_rows).to_csv(OUT/'external_shape_diagnostics.csv',index=False)
    b9=pd.read_csv(INP/'B9_v1.csv'); b9['N_multiple_of_B1_max']=b9.N_params_B/11.965825
    b9.to_csv(OUT/'B9_extrapolation_scope.csv',index=False)
    q=pd.read_csv(INP/'B7_v1.csv'); slopes=[]
    for (n,d),g in q.groupby(['N_params_B','D_tokens_B']):
        xc=g.Q_score-g.Q_score.mean();yc=g.val_loss-g.val_loss.mean();slope=float(xc@yc/(xc@xc))
        slopes.append(dict(N_params_B=float(n),D_tokens_B=float(d),slope=slope,n=len(g),q_min=float(g.Q_score.min()),q_max=float(g.Q_score.max())))
    pd.DataFrame(slopes).to_csv(OUT/'quality_cell_slopes.csv',index=False)
    qfits={};qval=[];qfold=[]
    for interaction in [False,True]:
        label='Qcommon' if not interaction else 'Qscale'
        x,y=quality_x(q,interaction);coef=np.linalg.lstsq(x,y,rcond=None)[0]
        qfits[label]=dict(coefficients=list(map(float,coef)),rank=int(np.linalg.matrix_rank(x)),**metrics(y,x@coef))
        for n in sorted(q.N_params_B.unique()):
            tr=q[q.N_params_B.ne(n)];te=q[q.N_params_B.eq(n)]
            tx,ty=quality_x(tr,interaction);vx,vy=quality_x(te,interaction)
            cc=np.linalg.lstsq(tx,ty,rcond=None)[0]
            qval.append(dict(model=label,N_params_B=float(n),n=len(te),**metrics(vy,vx@cc)))
            qfold.append(dict(model=label,N_params_B=float(n),coef_q=float(cc[0]),coef_q_logN=float(cc[1]) if interaction else 0.,coef_q_logD=float(cc[2]) if interaction else 0.))
    pd.DataFrame(qval).to_csv(OUT/'quality_centered_LONO.csv',index=False)
    pd.DataFrame(qfold).to_csv(OUT/'quality_fold_coefficients.csv',index=False)
    g=-qfits['Qcommon']['coefficients'][0]
    assert g>0
    # No identification claim: only the assumed B7-change-to-B1-loss scenario.
    U=A;V=B*100**(-b);L=E+U+V;rho_cal=g*.5/(b*V)
    scenarios=[]
    for scale in [0,.5,1,1.5]:
        gs=scale*g;dq=.1;nnew=(A/(U+gs*dq))**(1/a);dnew=(B/(V+gs*dq))**(1/b)
        scenarios.append(dict(mechanism='additive',factor=scale,g=gs,rho=0.,N0=1.,D0=100.,Q0=.5,Q1=.6,
            loss_initial=L,loss_new_fixed_ND=L-gs*dq,quality_elasticity=-gs*.5/L,
            N_keep_L=nnew,D_keep_L=dnew,N_saving_fraction=1-nnew,D_saving_fraction=1-dnew/100,
            dlogN_dQ=-gs/(a*U),dlogD_dQ=-gs/(b*V),evidence='SCENARIO-CONDITIONAL'))
    for rho in [0,.5,1,rho_cal]:
        ratio=(.6/.5)**rho;Vp=V*ratio**(-b);nnew=(A/(U+V-Vp))**(1/a);dnew=100/ratio
        scenarios.append(dict(mechanism='effective_D',factor=1.,g=rho*b*V/.5,rho=rho,N0=1.,D0=100.,Q0=.5,Q1=.6,
            loss_initial=L,loss_new_fixed_ND=E+U+Vp,quality_elasticity=-rho*b*V/L,
            N_keep_L=nnew,D_keep_L=dnew,N_saving_fraction=1-nnew,D_saving_fraction=1-dnew/100,
            dlogN_dQ=-rho*b*V/(.5*a*U),dlogD_dQ=-rho/.5,evidence='SCENARIO-CONDITIONAL'))
    pd.DataFrame(scenarios).to_csv(OUT/'quality_substitution_scenarios.csv',index=False)
    # Finite N-D substitution, with full inverse equation and explicit feasibility flags.
    nd=[]
    for factor in [.5,.8,1.,1.25,2.]:
        nn=factor;remaining=L-E-A*nn**(-a);dn=(B/remaining)**(1/b) if remaining>0 else None
        nd.append(dict(N0=1.,D0=100.,N_new=nn,D_new=dn,finite_solution=remaining>0,
            within_B1_rectangle=bool(dn is not None and .134<=dn<=299.893 and .070542<=nn<=11.965825)))
    dump(OUT/'ND_finite_substitution.json',nd)
    # Reuse frozen Q1 coefficients and validation artifacts; no training/validation rerun.
    q1=ROOT/'03_models/modeling_phase1/q1/round4';bundle=json.loads((q1/'P_RESPONSE_FROZEN_MODEL_BUNDLE_v1.json').read_text())
    coef=np.array(bundle['basis'])@np.array(bundle['models']['M1']['coef'])
    ref=np.array(bundle['models']['M1']['pmean']);mi=[]
    for i in range(17):
        for j in range(i+1,17):
            delta=.01*(coef[i]-coef[j])
            row=dict(add_domain=bundle['p_columns'][i],remove_domain=bundle['p_columns'][j],delta_p=.01,
                R0_change=float(delta.mean()),reference_nonnegative=bool(ref[j]>=.01),support_status='UNVERIFIED_DO_NOT_OPTIMIZE',scale='1M_ONLY')
            row.update({f'delta_{domain}':float(v) for domain,v in zip(bundle['loss_columns'],delta)});mi.append(row)
    pd.DataFrame(mi).to_csv(OUT/'mixture_tangent_scenarios.csv',index=False)
    old=pd.read_csv(q1/'P_RESPONSE_VALIDATION_METRICS_v2.csv');old[old.model.eq('M1')].to_csv(OUT/'inherited_mixture_scale_evidence.csv',index=False)
    domains=pd.read_csv(q1/'P_RESPONSE_DOMAIN_VALIDATION_v2.csv');domains[domains.model.eq('M1')].to_csv(OUT/'inherited_mixture_domain_evidence.csv',index=False)
    # Post-fit rounding diagnostic: not another model or source recovery.
    train=pd.read_csv(BASE/'training_predictions.csv');rounded=[1.69,.354,1.24,.34,.28]
    rounddiag=metrics(train.val_loss,pred(rounded,train.N_params_B,train.D_tokens_B))
    r=dict(run_id=RUN,created_utc=datetime.now(timezone.utc).isoformat(),code_sha256=sha(__file__),config_sha256=sha(CONF),
        quality_fits=qfits,quality_centered_LOO_macro_RMSE={model:float(np.mean([x['rmse'] for x in qval if x['model']==model])) for model in qfits},
        quality_common_g=g,quality_cell_slope_range=[min(x['slope'] for x in slopes),max(x['slope'] for x in slopes)],quality_negative_cells=sum(x['slope']<0 for x in slopes),quality_cells=len(slopes),
        effective_data_rho_local_calibration=float(rho_cal),B9_zero_D=int((b9.D_tokens_B<=0).sum()),
        external_summary={lab:dict(groups=len([r for r in source_rows if r['source']==lab]),
            median_centered_ratio=float(np.median([r['centered_ratio_to_zero'] for r in source_rows if r['source']==lab]))) for lab in ['B2','B4','B5','B10']},
        rounded_parameter_diagnostic=rounddiag,source_generator_recovered=False,TYPE_E=0,B8='QUARANTINED_UNREAD',
        empirical_quality_coefficient=None,empirical_AB_transport_coefficient=None,Q3_started=False)
    dump(OUT/'summary.json',r);dump(OUT/'output_manifest.json',{str(f.relative_to(OUT)):sha(f) for f in OUT.iterdir() if f.is_file()})
    print(json.dumps(r,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
