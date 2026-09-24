"""CP4: joint-draw propagation, scenario envelopes and shadow sensitivity."""
from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parent))
from round6_core import *
RUN='UNC-Q3-R6-20260924-v1';OUT=ROOT/'06_results/raw'/RUN
SCEN=ROOT/'06_results/raw/SCEN-Q3-R6-20260924-v1'
def main():
    cfg=load();assert not OUT.exists();OUT.mkdir(parents=True);nb=cfg['N_bounds'];db=cfg['D_bounds'];p=cfg['parameters']
    bp=pd.read_csv(ROOT/'06_results/raw/EXP-Q2-ND-R5-20260924-v1/cluster_bootstrap.csv');records=[]
    for _,draw in bp.iterrows():
        pp={k:float(draw[k]) for k in p}
        for L in cfg['contexts']:
            for C in cfg['budget_FLOPs']:
                n,d=analytic(C/1e18,L,pp,nb,db);dg=diagnostics(C/1e18,L,n,d,.5,'exponential',0,pp,nb,db,baseline=True)
                records.append(dict(replicate=int(draw.replicate),Budget_FLOPs=C,L_ctx=L,N_B=n,D_B=d,loss=loss(n,d,pp),mu_per_1e18=dg['mu_per_1e18'],active_constraints=dg['active_constraints']))
    draws=pd.DataFrame(records);draws.to_csv(OUT/'conditional_draw_paths.csv.gz',index=False,lineterminator='\n',compression={'method':'gzip','mtime':0})
    quant=draws.groupby(['Budget_FLOPs','L_ctx'])[['N_B','D_B','loss','mu_per_1e18']].quantile([.025,.5,.975]);quant.index.names=['Budget_FLOPs','L_ctx','conditional_quantile'];quant.reset_index().to_csv(OUT/'conditional_quantiles.csv',index=False,lineterminator='\n')
    q=pd.read_csv(SCEN/'quality_context_path.csv');ref=q[(q.L_ctx==2048)&(q.qcap==1)]
    env=ref.groupby('Budget_FLOPs')[['N_B','D_B','Q','loss','mu_per_1e18']].agg(['min','max']);env.columns=['_'.join(c) for c in env.columns];env.reset_index().to_csv(OUT/'scenario_envelope_NOT_CI.csv',index=False,lineterminator='\n')
    baseline=pd.read_csv(SCEN/'context_baseline.csv');shadows=[]
    for mode,data in [('BASELINE',baseline),('QUALITY',q)]:
        for _,row in data.iterrows():
            c=row.Budget_FLOPs/1e18;L=row.L_ctx;n=row.N_B;d=row.D_B;mu=row.mu_per_1e18;eps=1e-5
            if mode=='BASELINE':
                values=[loss(*analytic(c*(1+t*eps),L,p,nb,db),p) for t in [-1,1]]
                cap=1.;fam='exponential';h=0
            else:
                cap=row.qcap;fam=row.cost_family;h=row.factor*cfg['quality_g']
                values=[quality_opt(c*(1+t*eps),L,fam,h,p,nb,db,cap,101)[3] for t in [-1,1]]
            fd=-(values[1]-values[0])/(2*eps*c);r=(g(row.Q,fam)-g(.5,fam))/1e9;k=6+.0002*L
            vn=max(0.,p['alpha']*p['A']*n**(-p['alpha']-1)-mu*k*d) if abs(n/nb[1]-1)<1e-7 else 0.
            vd=max(0.,p['beta']*p['B']*d**(-p['beta']-1)-mu*(k*n+r)) if abs(d/db[1]-1)<1e-7 else 0.
            vq=max(0.,h-mu*d*gp(row.Q,fam)/1e9) if mode=='QUALITY' and abs(row.Q-cap)<1e-7 else 0.
            shadows.append(dict(mode=mode,scenario=row.get('scenario','BASELINE'),Budget_FLOPs=row.Budget_FLOPs,L_ctx=L,
                mu=mu,finite_difference_mu=fd,abs_error=abs(fd-mu),N_upper_marginal_value_per_B=vn,D_upper_marginal_value_per_B=vd,
                Q_cap_marginal_value=vq,context_cost_derivative=mu*.0002*n*d,evidence='CONDITIONAL_DERIVATIVES_NOT_MARKET_PRICES'))
    sh=pd.DataFrame(shadows);sh.to_csv(OUT/'shadow_prices.csv',index=False,lineterminator='\n')
    monotone=max(float(g0.sort_values('Budget_FLOPs').loss.diff().max()) for _,g0 in draws.groupby(['replicate','L_ctx']))
    summary=dict(run_id=RUN,status='PASS' if sh.abs_error.max()<1e-6 and monotone<=1e-10 else 'NEEDS_DIAGNOSTIC',joint_draws=len(bp),conditional_configurations=len(draws),quantile_rows=len(quant),shadow_rows=len(sh),shadow_max_absolute_error=float(sh.abs_error.max()),max_draw_loss_increase=monotone,scenario_envelope_is_CI=False,external_uncertainty_covered=False,Q4_started=False,code_sha256=sha(__file__),core_sha256=sha(Path(__file__).parent/'round6_core.py'),config_sha256=sha(CONFIG))
    dump(OUT/'summary.json',summary);dump(OUT/'output_manifest.json',{f.name:sha(f) for f in OUT.iterdir() if f.is_file()});print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
