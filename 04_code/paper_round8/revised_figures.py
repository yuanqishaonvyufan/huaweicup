"""Re-export final-size Q2/Q3 figures from frozen machine outputs only."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'08_paper/revised_v2/figures';OUT.mkdir(exist_ok=True,parents=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.labelsize':12,'xtick.labelsize':11,'ytick.labelsize':11,'legend.fontsize':10.5,'savefig.dpi':300,'pdf.fonttype':42})
specs=[]
def finish(fig,name,sources):
 fig.savefig(OUT/(name+'.png'),dpi=300,bbox_inches='tight',pad_inches=.08)
 fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight',pad_inches=.08)
 plt.close(fig)
 specs.append(dict(name=name,source_files=sources,source_sha256={x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in sources},png_sha256=hashlib.sha256((OUT/(name+'.png')).read_bytes()).hexdigest(),pdf_sha256=hashlib.sha256((OUT/(name+'.pdf')).read_bytes()).hexdigest(),intended_print_width_cm=12,base_font_pt=12))

p='06_results/raw/EXP-Q2-ND-R5-20260924-v1/marginal_effects.csv';m=pd.read_csv(ROOT/p);m=m[m.support=='OBSERVED_GRID']
ns=sorted(m.N_params_B.unique());ds=sorted(m.D_tokens_B.unique())
fig,axes=plt.subplots(1,2,figsize=(5.8,4.5),sharey=True,layout='constrained')
for ax,col,title in [(axes[0],'elasticity_N','N elasticity'),(axes[1],'elasticity_D','D elasticity')]:
 grid=m.pivot(index='N_params_B',columns='D_tokens_B',values=col).loc[ns,ds].to_numpy()
 im=ax.imshow(grid,origin='lower',aspect='auto',cmap='cividis',norm=Normalize(-.13,0))
 ax.set_title(title,fontsize=12);ax.set_xlabel('Training tokens D (billion)')
 ax.set_xticks([0,len(ds)//2,len(ds)-1],[f'{ds[0]:.2g}',f'{ds[len(ds)//2]:.2g}',f'{ds[-1]:.0f}'])
 ax.set_yticks([0,len(ns)//2,len(ns)-1],[f'{ns[0]:.2g}',f'{ns[len(ns)//2]:.2g}',f'{ns[-1]:.0f}'])
axes[0].set_ylabel('Parameters N (billion)')
fig.colorbar(im,ax=axes,location='bottom',shrink=.85,pad=.11,label='Elasticity of total Loss')
finish(fig,'FIG4_Q2_TOTAL_LOSS_ELASTICITY_REEXPORT',[p])

p='06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv';b=pd.read_csv(ROOT/p);x=b.Budget_FLOPs
fig,(a,c)=plt.subplots(2,1,figsize=(5.8,4.5),sharex=True,layout='constrained')
a.plot(x,b.N_B,label='N, billion',color='#184d72',lw=2.1)
a.plot(x,b.D_B,label='D, billion',color='#b66231',lw=2.1,ls='--')
a.set_xscale('log');a.set_yscale('log');a.set_ylabel('Conditional allocation');a.legend(loc='upper left',frameon=False)
c.plot(x,b.loss,color='#184d72',lw=2.1);c.set_xlabel('Budget C (FLOPs)');c.set_ylabel('Source-internal Loss')
for ax in [a,c]:
 for mark in [9.325359035607933e21,2.300063908774456e22]:ax.axvline(mark,color='.5',ls=':',lw=1)
finish(fig,'FIG5_Q3_BUDGET_REEXPORT',[p])

p='06_results/raw/SCEN-Q3-R6-20260924-v1/quality_context_path.csv';q=pd.read_csv(ROOT/p)
q=q[(q.L_ctx==2048)&(q.factor==1)&(q.qcap==1)].sort_values('Budget_FLOPs')
fig,(a,c)=plt.subplots(2,1,figsize=(5.8,4.5),sharex=True,layout='constrained')
for family,color,ls in [('exponential','#184d72','-'),('power','#a95527','--'),('logarithmic','#357461','-.')]:
 d=q[q.cost_family==family]
 a.plot(d.Budget_FLOPs,d.Q,label=family,color=color,ls=ls,lw=2)
 c.plot(d.Budget_FLOPs,d.loss,color=color,ls=ls,lw=2)
a.set_ylabel('Assumed quality Q');a.legend(loc='lower right',frameon=False)
c.set_xscale('log');c.set_ylabel('Conditional Loss');c.set_xlabel('Budget C (FLOPs)')
finish(fig,'FIG6_Q3_QUALITY_REEXPORT',[p])

p='06_results/raw/UNC-Q3-R6-20260924-v1/conditional_quantiles.csv';r='06_results/raw/UNC-Q3-R6-20260924-v1/scenario_envelope_NOT_CI.csv'
t=pd.read_csv(ROOT/p);t=t[t.L_ctx==2048];band=t.pivot(index='Budget_FLOPs',columns='conditional_quantile',values='loss').sort_index();env=pd.read_csv(ROOT/r).sort_values('Budget_FLOPs')
fig,(a,c)=plt.subplots(2,1,figsize=(5.8,4.5),sharex=True,layout='constrained')
x=band.index.to_numpy();a.fill_between(x,band[.025].to_numpy(),band[.975].to_numpy(),color='#a9bac6');a.plot(x,band[.5].to_numpy(),color='#184d72',lw=2)
a.set_ylabel('Parameter band\n(Loss)')
c.fill_between(env.Budget_FLOPs,env.loss_min,env.loss_max,color='#d3b494');c.plot(env.Budget_FLOPs,env.loss_max,color='#a95527',lw=1.6)
c.set_ylabel('Scenario envelope\n(Loss)');c.set_xscale('log');c.set_xlabel('Budget C (FLOPs)')
finish(fig,'FIG7_Q3_UNCERTAINTY_REEXPORT',[p,r])
(OUT/'REEXPORT_MANIFEST_v1.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2),encoding='utf-8')
print([(s['name'],(OUT/(s['name']+'.png')).stat().st_size) for s in specs])
