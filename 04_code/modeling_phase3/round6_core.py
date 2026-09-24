"""Q3 proxy costs, analytic N-D optima, bounded quality and KKT diagnostics."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.optimize import brentq,minimize,minimize_scalar
ROOT=Path(__file__).resolve().parents[2]
CONFIG=ROOT/'05_experiments/configs/Q3_R6_FROZEN_v1.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def native(v):
    if isinstance(v,np.generic):return v.item()
    raise TypeError(str(type(v)))
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2,default=native,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def load():
    c=json.loads(CONFIG.read_text())
    for p,h in {**c['inputs'],**c['spec_hashes']}.items():assert sha(ROOT/p)==h,p
    return c
def loss(n,d,p):return p['E']+p['A']*n**(-p['alpha'])+p['B']*d**(-p['beta'])
def g(q,fam):
    if fam=='exponential':return 1e7*np.exp(6*q)
    if fam=='power':return 5e9*q**4
    if fam=='logarithmic':return 2e9*np.log1p(10*q)
    raise ValueError(fam)
def gp(q,fam):
    if fam=='exponential':return 6e7*np.exp(6*q)
    if fam=='power':return 2e10*q**3
    if fam=='logarithmic':return 2e10/(1+10*q)
    raise ValueError(fam)
def costs(n,d,q,L,fam='exponential',q0=.5):
    return {'train_FLOPs':6e18*n*d,'attention_FLOPs':.0002*L*1e18*n*d,
            'quality_FLOPs':1e9*d*max(0.,g(q,fam)-g(q0,fam))}
def analytic(c,L,p,nb,db):
    k=6+.0002*L;K=c/k;n0,n1=nb;d0,d1=db
    if K<n0*d0*(1-1e-12):return None
    if K>=n1*d1:return n1,d1
    lo=max(n0,K/d1);hi=min(n1,K/d0)
    n=np.clip((p['alpha']*p['A']/(p['beta']*p['B']))**(1/(p['alpha']+p['beta']))*K**(p['beta']/(p['alpha']+p['beta'])),lo,hi)
    return float(n),float(K/n)
def fixed_quality(c,L,q,fam,p,nb,db):
    k=6+.0002*L;r=(g(q,fam)-g(.5,fam))/1e9;n0,n1=nb;d0,d1=db
    if (k*n0+r)*d0>c*(1+1e-12):return None
    if (k*n1+r)*d1<=c:return n1,d1
    hi=min(n1,(c/d0-r)/k);lo=max(n0,min(hi,(c/d1-r)/k))
    def grad(x):
        n=np.exp(x);d=c/(k*n+r)
        return -p['alpha']*p['A']*n**(-p['alpha'])+p['beta']*p['B']*d**(-p['beta'])*k*n/(k*n+r)
    if hi<=lo*(1+1e-12) or grad(np.log(lo))>=0:n=lo
    elif grad(np.log(hi))<=0:n=hi
    else:n=float(np.exp(brentq(grad,np.log(lo),np.log(hi),xtol=1e-13)))
    return float(n),float(min(d1,c/(k*n+r)))
def quality_opt(c,L,fam,h,p,nb,db,qcap=1.,grid=101):
    if h==0:
        n,d=analytic(c,L,p,nb,db);return n,d,.5,loss(n,d,p)
    qhi=qcap;k=6+.0002*L
    if fixed_quality(c,L,qhi,fam,p,nb,db) is None:
        qhi=brentq(lambda q:(k*nb[0]+(g(q,fam)-g(.5,fam))/1e9)*db[0]-c,.5,qcap)
    def obj(q):
        nd=fixed_quality(c,L,q,fam,p,nb,db)
        return loss(*nd,p)-h*(q-.5) if nd else 1e10
    xx=np.linspace(.5,qhi,grid);yy=np.array([obj(q) for q in xx]);candidates=[(.5,yy[0]),(qhi,yy[-1])]
    for i in range(1,len(xx)-1):
        if yy[i]<=yy[i-1] and yy[i]<=yy[i+1]:
            out=minimize_scalar(obj,bounds=(xx[i-1],xx[i+1]),method='bounded',options={'xatol':1e-10})
            candidates.append((float(out.x),float(out.fun)))
    minimum=min(v for _,v in candidates);qbest=min(q for q,v in candidates if v<=minimum+1e-10)
    n,d=fixed_quality(c,L,qbest,fam,p,nb,db)
    return n,d,float(qbest),float(obj(qbest))
def numerical(c,L,fam,h,p,nb,db,qcap=1.,baseline=False):
    k=6+.0002*L;bounds=[tuple(np.log(nb)),tuple(np.log(db))]+([] if baseline else [(.5,qcap)])
    def unpack(x):return np.exp(x[0]),np.exp(x[1]),.5 if baseline else x[2]
    def obj(x):
        n,d,q=unpack(x);return loss(n,d,p)-h*(q-.5)
    def jac(x):
        n,d,q=unpack(x);v=[-p['alpha']*p['A']*n**(-p['alpha']),-p['beta']*p['B']*d**(-p['beta'])]
        return np.array(v if baseline else v+[-h])
    if baseline:
        cons={'type':'ineq','fun':lambda x:np.log(c/k)-x.sum(),'jac':lambda x:-np.ones(2)}
        K=min(c/k,nb[1]*db[1]);lo=max(nb[0],K/db[1]);hi=min(nb[1],K/db[0]);starts=[np.log([n,K/n]) for n in np.exp(np.linspace(np.log(lo),np.log(hi),4))]
    else:
        def cf(x):
            n,d,q=unpack(x);return 1-(k*n+(g(q,fam)-g(.5,fam))/1e9)*d/c
        def cj(x):
            n,d,q=unpack(x);r=(g(q,fam)-g(.5,fam))/1e9
            return -np.array([k*n*d,(k*n+r)*d,gp(q,fam)*d/1e9])/c
        cons={'type':'ineq','fun':cf,'jac':cj};starts=[]
        for q in [.5,(.5+qcap)/2,qcap]:
            nd=fixed_quality(c,L,q,fam,p,nb,db)
            if nd is None:q=.5;nd=fixed_quality(c,L,q,fam,p,nb,db)
            starts.append(np.r_[np.log(nd),q])
    out=[]
    for i,x in enumerate(starts):
        f=minimize(obj,x,jac=jac,method='SLSQP',bounds=bounds,constraints=[cons],options={'ftol':1e-12,'maxiter':1000})
        n,d,q=unpack(f.x);out.append(dict(start=i,success=bool(f.success),message=str(f.message),N_B=float(n),D_B=float(d),Q=float(q),loss=float(obj(f.x)),constraint=float(cons['fun'](f.x))))
    return out
def diagnostics(c,L,n,d,q,fam,h,p,nb,db,qcap=1.,baseline=False):
    k=6+.0002*L;r=(g(q,fam)-g(.5,fam))/1e9;used=(k*n+r)*d
    vals=np.array([np.log(n),np.log(d)]+([] if baseline else [q]));lo=np.array([np.log(nb[0]),np.log(db[0])]+([] if baseline else [.5]));hi=np.array([np.log(nb[1]),np.log(db[1])]+([] if baseline else [qcap]))
    grad=np.array([-p['alpha']*p['A']*n**(-p['alpha']),-p['beta']*p['B']*d**(-p['beta'])]+([] if baseline else [-h]))
    cg=np.array([k*n*d,used]+([] if baseline else [d*gp(q,fam)/1e9]))
    low=np.abs(vals-lo)<2e-7;high=np.abs(vals-hi)<2e-7;free=~(low|high)
    if used<c*(1-1e-8):mu=0.
    elif free.any():mu=float(max(0,-np.dot(grad[free],cg[free])/np.dot(cg[free],cg[free])))
    else:
        lower=max([0.]+[-grad[i]/cg[i] for i in range(len(vals)) if low[i]])
        upper=min([np.inf]+[-grad[i]/cg[i] for i in range(len(vals)) if high[i]])
        mu=float(lower if lower<=upper else (lower+upper)/2)
    residual=grad+mu*cg;projected=np.where(low,np.minimum(residual,0),np.where(high,np.maximum(residual,0),residual))
    labels=['N','D']+([] if baseline else ['Q']);active=[labels[i]+('_LOW' if low[i] else '_HIGH') for i in range(len(vals)) if low[i] or high[i]]
    active+=['BUDGET_ACTIVE' if abs(used/c-1)<1e-8 else 'BUDGET_SLACK']
    return dict(total_FLOPs=used*1e18,budget_slack_FLOPs=(c-used)*1e18,budget_relative_violation=max(0,used/c-1),
        mu_per_1e18=mu,dLoss_dBudget_FLOPs=-mu/1e18,kkt_projected_max=float(np.max(np.abs(projected))),
        complementarity=float(abs(mu*(used-c))),active_constraints=';'.join(active),
        quality_cap_value=0. if baseline else max(0.,h-mu*d*gp(q,fam)/1e9),support_status='B1_RECTANGLE_CONDITIONAL',
        **costs(n,d,q,L,fam))
