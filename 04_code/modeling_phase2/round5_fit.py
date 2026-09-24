"""Frozen B1 nonlinear regression and trajectory validation. No Q1 refits."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,platform,itertools
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import least_squares
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[2]
INP=ROOT/'01_data/processed/modeling_phase2/round5'
RUN='EXP-Q2-ND-R5-20260924-v1'
OUT=ROOT/'06_results/raw'/RUN
CONF=ROOT/'05_experiments/configs/Q2_R5_v1.json'
PARS=['E','A','B','alpha','beta']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def pred(p,n,d):
    E,A,B,alpha,beta=p
    return E+A*np.asarray(n)**(-alpha)+B*np.asarray(d)**(-beta)
def fit(d,weights=None,starts=None):
    n=d.N_params_B.to_numpy();dt=d.D_tokens_B.to_numpy();y=d.val_loss.to_numpy()
    weights=np.ones(len(d)) if weights is None else np.asarray(weights)
    w=np.sqrt(weights/weights.mean())
    lo=np.array([0,1e-8,1e-8,.001,.001]);hi=np.array([y.min(),20,20,2,2])
    starts=starts if starts is not None else [[e,1,1,a,b] for e,a,b in itertools.product([.5,1.5],[.1,.3,.7],[.1,.3])]
    solutions=[]
    for start in starts:
        f=least_squares(lambda p:(pred(p,n,dt)-y)*w,np.clip(start,lo+1e-9,hi-1e-9),
            bounds=(lo,hi),method='trf',x_scale='jac',max_nfev=5000,ftol=1e-11,xtol=1e-11,gtol=1e-11)
        if f.success and np.isfinite(f.fun).all():solutions.append(f)
    if not solutions:raise RuntimeError('No converged start')
    solutions.sort(key=lambda f:float(np.dot(f.fun,f.fun)));f=solutions[0]
    return f.x,dict(sse=float(np.dot(f.fun,f.fun)),successful_starts=len(solutions),
        total_starts=len(starts),max_start_parameter_spread=float(np.max(np.ptp(np.array([s.x for s in solutions]),axis=0))),
        min_start_sse=float(np.dot(f.fun,f.fun)),max_start_sse=float(max(np.dot(s.fun,s.fun) for s in solutions)),
        jacobian_rank=int(np.linalg.matrix_rank(f.jac)),jacobian_condition=float(np.linalg.cond(f.jac)),
        boundary=bool(np.any(f.x-lo<1e-6)|np.any(hi-f.x<1e-6)))
def metrics(y,p):
    e=np.asarray(p)-np.asarray(y)
    return dict(rmse=float(np.sqrt(np.mean(e**2))),mae=float(np.mean(np.abs(e))),bias=float(e.mean()))
def compare(train,test):
    p,info=fit(train)
    x=lambda z:np.column_stack([np.ones(len(z)),np.log(z.N_params_B),np.log(z.D_tokens_B)])
    sl=np.linalg.lstsq(x(train),train.val_loss,rcond=None)[0]
    return {'S1':pred(p,test.N_params_B,test.D_tokens_B),'S0':np.full(len(test),train.val_loss.mean()),'Slog':x(test)@sl},p,info
def main():
    config=json.loads(CONF.read_text(encoding='utf-8'))
    assert sha(__file__)==config['fit_code_sha256']
    assert sha(ROOT/config['spec'])==config['spec_sha256']
    manifest=json.loads((INP/'INPUT_MANIFEST_v1.json').read_text())
    for item in manifest['inputs']:assert sha(ROOT/item['processed'])==item['processed_sha256']
    if OUT.exists():raise RuntimeError('Immutable run already exists')
    OUT.mkdir(parents=True)
    d=pd.read_csv(INP/'B1_v1.csv'); nvals=sorted(d.N_params_B.unique())
    full,full_info=fit(d);d['prediction']=pred(full,d.N_params_B,d.D_tokens_B);d['residual']=d.prediction-d.val_loss
    d.to_csv(OUT/'training_predictions.csv',index=False)
    print('Full fit:',dict(zip(PARS,full)),flush=True)
    foldplans=[]
    for n in nvals:foldplans.append(('LONO',f'N{n}',d.N_params_B.ne(n),d.N_params_B.eq(n)))
    for cut in [73,110]:foldplans.append(('FORWARD',f'Drank{cut}',d.D_rank.lt(cut),d.D_rank.ge(cut)))
    for n in nvals:foldplans.append(('BLOCK2D',f'N{n}_D98',d.N_params_B.ne(n)&d.D_rank.lt(98),d.N_params_B.eq(n)&d.D_rank.ge(98)))
    rows=[];predrows=[];pars=[];splits=[]
    for kind,fid,tr,te in foldplans:
        train=d.loc[tr];test=d.loc[te]; assert not set(train.row_id)&set(test.row_id)
        pp,p,info=compare(train,test)
        pars.append(dict(kind=kind,fold=fid,**dict(zip(PARS,map(float,p))),**info))
        splits.append(dict(kind=kind,fold=fid,train=train.row_id.tolist(),test=test.row_id.tolist()))
        for model,pv in pp.items():
            z=test[['row_id','N_params_B','D_tokens_B','val_loss']].copy();z['prediction']=pv;z['kind']=kind;z['fold']=fid;z['model']=model
            predrows.append(z)
            for n,g in z.groupby('N_params_B'):
                rows.append(dict(kind=kind,fold=fid,model=model,N_params_B=float(n),count=len(g),**metrics(g.val_loss,g.prediction)))
        print(kind,fid,'S1 RMSE',metrics(test.val_loss,pp['S1'])['rmse'],flush=True)
    m=pd.DataFrame(rows);m.to_csv(OUT/'validation_metrics.csv',index=False)
    pd.concat(predrows,ignore_index=True).to_csv(OUT/'validation_predictions.csv',index=False)
    pd.DataFrame(pars).to_csv(OUT/'fold_parameters.csv',index=False);dump(OUT/'splits.json',splits)
    validation={}
    for kind in ['LONO','FORWARD','BLOCK2D']:
        sub=m[m.kind.eq(kind)];v={}
        for model in ['S1','S0','Slog']:
            a=sub[sub.model.eq(model)];v[model]=dict(macro_rmse=float(a.rmse.mean()),worst_rmse=float(a.rmse.max()),macro_mae=float(a.mae.mean()))
        v['pass']=bool(v['S1']['macro_rmse']<=.05 and v['S1']['worst_rmse']<=.10 and v['S1']['macro_rmse']<=.8*v['S0']['macro_rmse'])
        validation[kind]=v
    residual=[]
    for n,g in d.groupby('N_params_B'):
        residual.append(dict(N_params_B=float(n),**metrics(g.val_loss,g.prediction),
            rho_logD=float(spearmanr(g.residual,np.log(g.D_tokens_B)).statistic),
            residual_range=float(g.residual.max()-g.residual.min()),lag1=float(g.residual.autocorr())))
    pd.DataFrame(residual).to_csv(OUT/'residual_diagnostics.csv',index=False)
    upgrade_trigger=any(sum(r['rho_logD']*sign>.3 and r['residual_range']>.005 for r in residual)>=6 for sign in [1,-1])
    rng=np.random.default_rng(20260924);boot=[];bootfail=[]
    starts=[full,[.5,1,1,.1,.1],[1.5,1,1,.7,.3]]
    for b in range(200):
        draw=rng.choice(nvals,size=8,replace=True);counts={n:int(np.sum(draw==n)) for n in nvals};z=d[d.N_params_B.isin(draw)]
        try:
            p,inf=fit(z,z.N_params_B.map(counts).to_numpy(),starts=starts)
            boot.append(dict(replicate=b,unique_groups=len(set(draw)),draw=';'.join(map(str,draw)),**dict(zip(PARS,map(float,p))),boundary=inf['boundary']))
        except Exception as exc:bootfail.append(dict(replicate=b,error=str(exc)))
        if (b+1)%50==0:print('Cluster bootstrap',b+1,flush=True)
    bp=pd.DataFrame(boot);bp.to_csv(OUT/'cluster_bootstrap.csv',index=False)
    ci={k:list(map(float,np.quantile(bp[k],[.025,.5,.975]))) for k in PARS}
    sensitivities=[]
    for cut in [1,10]:
        z=d[d.D_tokens_B.ge(cut)];p,inf=fit(z);sensitivities.append(dict(name=f'D_ge_{cut}',**dict(zip(PARS,map(float,p))),**inf,**metrics(z.val_loss,pred(p,z.N_params_B,z.D_tokens_B))))
    # Trapezoidal measure in log D; equal total mass per trajectory.
    ld=np.log(np.sort(d.D_tokens_B.unique()));edge=np.r_[ld[0],(ld[:-1]+ld[1:])/2,ld[-1]];dw=np.diff(edge)
    p,inf=fit(d,d.D_rank.map(dict(enumerate(dw))).to_numpy());sensitivities.append(dict(name='logD_weighted',**dict(zip(PARS,map(float,p))),**inf,**metrics(d.val_loss,pred(p,d.N_params_B,d.D_tokens_B))))
    pd.DataFrame(sensitivities).to_csv(OUT/'parameter_sensitivity.csv',index=False)
    # Derivatives on observed support and a clearly labelled illustrative N=1,D=100 point.
    E,A,B,a,b=full;effects=[]
    points=[(float(n),float(dt),'OBSERVED_GRID') for n in nvals for dt in sorted(d.D_tokens_B.unique())]+[(1.,100.,'INTERPOLATION_SCENARIO')]
    for n,dt,status in points:
        U=A*n**(-a);V=B*dt**(-b);L=E+U+V
        effects.append(dict(N_params_B=n,D_tokens_B=dt,support=status,loss=L,dL_dN=-a*U/n,dL_dD=-b*V/dt,
            elasticity_N=-a*U/L,elasticity_D=-b*V/L,excess_elasticity_N=-a*U/(U+V),excess_elasticity_D=-b*V/(U+V),
            dD_dN=-a*U*dt/(b*V*n),dlogD_dlogN=-a*U/(b*V)))
    pd.DataFrame(effects).to_csv(OUT/'marginal_effects.csv',index=False)
    derivative_ci=[]
    for _,r in bp.iterrows():
        E0,A0,B0,a0,b0=[r[k] for k in PARS];U=A0;V=B0*100**(-b0);L=E0+U+V
        derivative_ci.append(dict(loss=L,dL_dN=-a0*U,dL_dD=-b0*V/100,elasticity_N=-a0*U/L,elasticity_D=-b0*V/L,dlogD_dlogN=-a0*U/(b0*V)))
    pd.DataFrame(derivative_ci).to_csv(OUT/'illustrative_derivative_bootstrap.csv',index=False)
    summary=dict(run_id=RUN,created_utc=datetime.now(timezone.utc).isoformat(),code_sha256=sha(__file__),config_sha256=sha(CONF),
        input_manifest_sha256=sha(INP/'INPUT_MANIFEST_v1.json'),python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,pandas=pd.__version__,
        evidence_level='ATTACHMENT-INTERNAL ESTIMATED',parameters=dict(zip(PARS,map(float,full))),full_fit=full_info,
        training=metrics(d.val_loss,d.prediction),validation=validation,restricted_predictive_pass=all(x['pass'] for x in validation.values()),
        upgrade_trigger=upgrade_trigger,bootstrap_valid=len(boot),bootstrap_failures=bootfail,bootstrap_boundary=int(bp.boundary.sum()),
        parameter_conditional_interval=ci,final_model=False,gate3='NOT DECIDED')
    dump(OUT/'summary.json',summary)
    dump(OUT/'output_manifest.json',{str(p.relative_to(OUT)):sha(p) for p in OUT.iterdir() if p.is_file()})
    print(json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
