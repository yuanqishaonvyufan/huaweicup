"""CP3: prespecified quality, architecture-context and local mixture scenarios."""
from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.spatial.distance import cdist
sys.path.insert(0,str(Path(__file__).resolve().parent))
from round6_core import *
RUN='SCEN-Q3-R6-20260924-v1';OUT=ROOT/'06_results/raw'/RUN
def main():
    cfg=load();assert not OUT.exists();OUT.mkdir(parents=True);p=cfg['parameters'];nb=cfg['N_bounds'];db=cfg['D_bounds'];ref=cfg['reference_context']
    rows=[];num=[];dense=[];context=[];breakeven=[];supply=[]
    for L in cfg['contexts']:
        for C in cfg['budget_FLOPs']:
            n,d=analytic(C/1e18,L,p,nb,db);context.append(dict(Budget_FLOPs=C,L_ctx=L,N_B=n,D_B=d,Q=.5,loss=loss(n,d,p),**diagnostics(C/1e18,L,n,d,.5,'exponential',0,p,nb,db,baseline=True)))
    plans=[(ref,factor,fam,1.) for factor in cfg['quality_factors'] for fam in cfg['cost_families']]
    plans += [(L,1.,fam,1.) for L in cfg['contexts'] if L!=ref for fam in cfg['cost_families']]
    plans += [(ref,1.,fam,.75) for fam in cfg['cost_families']]
    for L,factor,fam,cap in plans:
        h=factor*cfg['quality_g'];name=f'L{L}_{fam}_h{factor}_cap{cap}'
        for C in cfg['budget_FLOPs']:
            c=C/1e18;n,d,q,val=quality_opt(c,L,fam,h,p,nb,db,cap,101)
            ndq2=quality_opt(c,L,fam,h,p,nb,db,cap,201)
            row=dict(scenario=name,Budget_FLOPs=C,L_ctx=L,factor=factor,cost_family=fam,qcap=cap,N_B=n,D_B=d,Q=q,loss=val,evidence='SCENARIO-CONDITIONAL',**diagnostics(c,L,n,d,q,fam,h,p,nb,db,cap));rows.append(row)
            dense.append(dict(scenario=name,Budget_FLOPs=C,loss_difference=ndq2[3]-val,Q_difference=ndq2[2]-q))
            for v in numerical(c,L,fam,h,p,nb,db,cap):num.append(dict(scenario=name,Budget_FLOPs=C,reference_loss=val,loss_gap=v['loss']-val,**v))
        print('Finished',name,flush=True)
    # Local and global quality activation threshold, independent of chosen h.
    for fam in cfg['cost_families']:
        for C in cfg['budget_FLOPs']:
            c=C/1e18;n,d=analytic(c,ref,p,nb,db);f0=loss(n,d,p)
            dg=diagnostics(c,ref,n,d,.5,fam,0,p,nb,db,baseline=True)
            local=dg['mu_per_1e18']*d*gp(.5,fam)/1e9
            def ratio(q):
                nd=fixed_quality(c,ref,q,fam,p,nb,db)
                return (loss(*nd,p)-f0)/(q-.5) if nd else 1e10
            xx=np.linspace(.5000001,1,101);yy=np.array([ratio(q) for q in xx]);cand=[(local,.5),(float(yy[-1]),1.)]
            for i in range(1,100):
                if yy[i]<=yy[i-1] and yy[i]<=yy[i+1]:
                    out=minimize_scalar(ratio,bounds=(xx[i-1],xx[i+1]),method='bounded',options={'xatol':1e-10});cand.append((float(out.fun),float(out.x)))
            best=min(cand);breakeven.append(dict(Budget_FLOPs=C,cost_family=fam,local_threshold_h=local,global_threshold_h=best[0],global_witness_Q=best[1],reference_h=cfg['quality_g'],reference_local_active=cfg['quality_g']>local,reference_global_active=cfg['quality_g']>best[0]))
    for factor in [.25,.5]:
        bounds=[db[0],db[1]*factor]
        for C in cfg['budget_FLOPs']:
            n,d=analytic(C/1e18,ref,p,nb,bounds);supply.append(dict(Budget_FLOPs=C,D_cap_factor=factor,N_B=n,D_B=d,loss=loss(n,d,p),evidence='SCENARIO_NOT_MEASURED_SUPPLY',**diagnostics(C/1e18,ref,n,d,.5,'exponential',0,p,nb,bounds,baseline=True)))
    # Frozen Q1 local evidence: finite convex combinations, not a cross-source p optimizer.
    qb=json.loads((ROOT/'03_models/modeling_phase1/q1/round4/P_RESPONSE_FROZEN_MODEL_BUNDLE_v1.json').read_text())
    P=np.array(qb['training_p_matrix']);p0=P.mean(axis=0);candidates=np.vstack([p0,(P+p0)/2]);coef=np.array(qb['basis'])@np.array(qb['models']['M1']['coef'])
    delta=(candidates-p0)@coef;near=cdist(candidates,P).min(axis=1);mix=pd.DataFrame(candidates,columns=qb['p_columns']);mix.insert(0,'candidate',range(len(mix)));mix['nearest_train_distance']=near;mix['R0_centered_delta']=delta.mean(axis=1)
    for i,col in enumerate(qb['loss_columns']):mix['delta_'+col]=delta[:,i]
    mix['convex_witness']='0.5*uniform_training_weights + 0.5*one_training_row; candidate0 uniform'
    mix.to_csv(OUT/'mixture_local_candidates.csv',index=False,lineterminator='\n')
    mixsummary=[]
    for scale,k in [('ZERO_TRANSFER',0.),('1M_LOCAL',1.),('60M_ATTENUATED_SCENARIO',.25),('60M_ATTENUATED_SCENARIO',.5)]:
        ix=0 if k==0 else int(np.argmin(delta.mean(axis=1)))
        mixsummary.append(dict(scale=scale,k=k,candidate=ix,R0_change=float(k*delta[ix].mean()),improved_domains=int(np.sum(k*delta[ix]<0)),worsened_domains=int(np.sum(k*delta[ix]>0)),nearest_distance=float(near[ix]),empirical_hull=True,real_supply='UNKNOWN',B1_joint_use='FORBIDDEN_NO_SCALE_OVERLAP',evidence='A_SOURCE_LOCAL_ASSOCIATION' if k==1 else 'SCENARIO-CONDITIONAL'))
    frames={'quality_context_path':pd.DataFrame(rows),'quality_multistart':pd.DataFrame(num),'quality_grid_refinement':pd.DataFrame(dense),'context_baseline':pd.DataFrame(context),'quality_break_even':pd.DataFrame(breakeven),'supply_stress':pd.DataFrame(supply),'mixture_scenarios':pd.DataFrame(mixsummary)}
    for name,df in frames.items():df.to_csv(OUT/f'{name}.csv',index=False,lineterminator='\n')
    q=frames['quality_context_path'];numeric=frames['quality_multistart'];check=frames['quality_grid_refinement'];successful=numeric[numeric.success & numeric.constraint.ge(-1e-8)];best=successful.groupby(['scenario','Budget_FLOPs']).loss_gap.min()
    monotone=max(float(gp0.sort_values('Budget_FLOPs').loss.diff().max()) for _,gp0 in q.groupby('scenario'))
    result=dict(run_id=RUN,quality_rows=len(q),numeric_starts=len(numeric),failed_starts=int((~numeric.success).sum()),max_all_start_loss_gap=float(numeric.loss_gap.abs().max()),max_best_start_gap=float(best.abs().max()),best_case_count=len(best),max_dense_grid_difference=float(check.loss_difference.abs().max()),max_kkt=float(q.kkt_projected_max.max()),max_budget_violation=float(q.budget_relative_violation.max()),max_loss_increase=monotone,
        mixture_candidates=len(candidates),simplex_max_error=float(np.max(np.abs(candidates.sum(axis=1)-1))),min_p=float(candidates.min()),main_mix_transport=0,local_mix_not_joint_B1=True,context_levels=cfg['contexts'],context_is_architecture_scenario=True,quality_causal=False,Q4_started=False,code_sha256=sha(__file__),core_sha256=sha(Path(__file__).parent/'round6_core.py'),config_sha256=sha(CONFIG))
    result['status']='PASS' if len(best)==len(q) and result['max_best_start_gap']<1e-6 and result['max_dense_grid_difference']<1e-7 and result['max_kkt']<1e-6 and result['max_budget_violation']<1e-8 and monotone<1e-8 else 'NEEDS_DIAGNOSTIC'
    dump(OUT/'summary.json',result);dump(OUT/'output_manifest.json',{f.name:sha(f) for f in OUT.iterdir() if f.is_file()});print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
