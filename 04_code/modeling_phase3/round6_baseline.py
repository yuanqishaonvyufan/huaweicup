"""CP2: exact bounded baseline plus independent multistart SLSQP."""
from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parent))
from round6_core import *
RUN='EXP-Q3-BASE-R6-20260924-v1';OUT=ROOT/'06_results/raw'/RUN
def main():
    cfg=load();assert not OUT.exists();OUT.mkdir(parents=True)
    p=cfg['parameters'];nb=cfg['N_bounds'];db=cfg['D_bounds'];L=cfg['reference_context'];rows=[];num=[]
    for C in cfg['budget_FLOPs']:
        c=C/1e18;n,d=analytic(c,L,p,nb,db);diag=diagnostics(c,L,n,d,.5,'exponential',0,p,nb,db,baseline=True)
        row=dict(Budget_FLOPs=C,L_ctx=L,N_B=n,D_B=d,Q=.5,loss=loss(n,d,p),quality='OFF',mixture='OFF',**diag);rows.append(row)
        for v in numerical(c,L,'exponential',0,p,nb,db,baseline=True):num.append(dict(Budget_FLOPs=C,analytic_loss=row['loss'],loss_gap=v['loss']-row['loss'],N_relative_gap=v['N_B']/n-1,D_relative_gap=v['D_B']/d-1,**v))
    data=pd.DataFrame(rows);tests=pd.DataFrame(num);data.to_csv(OUT/'budget_path.csv',index=False);tests.to_csv(OUT/'multistart_checks.csv',index=False)
    okay=bool(tests.success.all() and tests.loss_gap.abs().max()<=1e-8 and tests[['N_relative_gap','D_relative_gap']].abs().max().max()<=1e-4 and data.budget_relative_violation.max()<=1e-8 and data.kkt_projected_max.max()<=1e-7 and np.max(np.diff(data.loss))<=1e-10)
    A=p['A'];B=p['B'];a=p['alpha'];b=p['beta'];k=6+.0002*L;ratio=(a*A/(b*B))**(1/(a+b))
    transitions={'unconstrained_N_upper_C':k*(nb[1]/ratio)**((a+b)/b)*1e18,'unconstrained_D_upper_C':k*(db[1]*ratio)**((a+b)/a)*1e18,'both_upper_saturation_C':k*nb[1]*db[1]*1e18,'N_budget_elasticity_interior':b/(a+b),'D_budget_elasticity_interior':a/(a+b)}
    dump(OUT/'summary.json',dict(run_id=RUN,status='PASS' if okay else 'FAIL',rows=len(data),numeric_starts=len(tests),all_starts_success=bool(tests.success.all()),max_loss_gap=float(tests.loss_gap.abs().max()),max_kkt=float(data.kkt_projected_max.max()),transitions=transitions,config_sha256=sha(CONFIG),code_sha256=sha(__file__),core_sha256=sha(Path(__file__).parent/'round6_core.py'),evidence='ATTACHMENT-INTERNAL ESTIMATED + PROBLEM-PROVIDED COST PROXIES',Q4_started=False))
    dump(OUT/'output_manifest.json',{f.name:sha(f) for f in OUT.iterdir() if f.is_file()})
    print((OUT/'summary.json').read_text());print(data.iloc[[0,30,50]][['Budget_FLOPs','N_B','D_B','loss','active_constraints']].to_string(index=False))
    assert okay
if __name__=='__main__':main()
