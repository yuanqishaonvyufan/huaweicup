"""Q3 checked-result figures at a declared 15cm insertion width."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'06_results/figures/round6'
B=ROOT/'06_results/raw/EXP-Q3-BASE-R6-20260924-v1';S=ROOT/'06_results/raw/SCEN-Q3-R6-20260924-v1';U=ROOT/'06_results/raw/UNC-Q3-R6-20260924-v1'
plt.rcParams.update({'font.family':'Microsoft YaHei','font.size':11,'axes.labelsize':11,'xtick.labelsize':10,'ytick.labelsize':10,'legend.fontsize':10,'axes.unicode_minus':False,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':300})
FAMS=['exponential','power','logarithmic'];LABELS=['指数成本','幂函数成本','对数成本'];COLORS=['#28658b','#c47b38','#43835e'];M=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(fig,id,claim,sources,ids):
    fig.canvas.draw();renderer=fig.canvas.get_renderer();texts=[]
    for ax in fig.axes:
        # Only ticks within axis data limits will actually render.
        for tick in ax.xaxis.get_major_ticks()+ax.xaxis.get_minor_ticks():
            if tick.get_loc()<min(ax.get_xlim()) or tick.get_loc()>max(ax.get_xlim()):tick.label1.set_visible(False);tick.label2.set_visible(False)
        for tick in ax.yaxis.get_major_ticks()+ax.yaxis.get_minor_ticks():
            if tick.get_loc()<min(ax.get_ylim()) or tick.get_loc()>max(ax.get_ylim()):tick.label1.set_visible(False);tick.label2.set_visible(False)
    fig.canvas.draw()
    for t in fig.findobj(matplotlib.text.Text):
        if t.get_visible() and t.get_text():
            bb=t.get_window_extent(renderer);texts.append({'text':t.get_text(),'font_pt':t.get_fontsize(),'inside':bool(bb.x0>=-1 and bb.y0>=-1 and bb.x1<=fig.bbox.x1+1 and bb.y1<=fig.bbox.y1+1)})
    files=[]
    for ext in ['png','pdf']:
        path=OUT/f'{id}.{ext}';fig.savefig(path);files.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path)})
    M.append({'id':id,'claim':claim,'reader_task':claim,'source':sources,'result_ids':ids,'paths':files,'publish':True,'placement':'Q3 paper candidate, Gate4 pending','insert_width_cm':15,'minimum_effective_font_pt':9.525,'text_checks':texts});plt.close(fig)
def main():
    assert json.loads((ROOT/'10_review/MODELING_PHASE3_R6_NUMERICAL_QA_20260924.json').read_text())['status']=='PASS';OUT.mkdir(parents=True,exist_ok=True)
    base=pd.read_csv(B/'budget_path.csv');q=pd.read_csv(S/'quality_context_path.csv');ctx=pd.read_csv(S/'context_baseline.csv');be=pd.read_csv(S/'quality_break_even.csv');qq=pd.read_csv(U/'conditional_quantiles.csv');env=pd.read_csv(U/'scenario_envelope_NOT_CI.csv')
    fig,ax=plt.subplots(2,1,figsize=(6.2,5.5),sharex=True,layout='constrained')
    ax[0].plot(base.Budget_FLOPs,base.N_B,'-',label='N（十亿参数）',color=COLORS[0]);ax[0].plot(base.Budget_FLOPs,base.D_B,'--',label='D（十亿 token）',color=COLORS[1]);ax[0].set_yscale('log');ax[0].set_ylabel('条件配置（对数刻度）');ax[0].legend(frameon=False,ncol=2,loc='lower center',bbox_to_anchor=(.5,1))
    ax[1].plot(base.Budget_FLOPs,base.loss,color=COLORS[0]);ax[1].set_ylabel('附件内预测 Loss');ax[1].set_xlabel('算力代理预算 C（FLOPs，对数刻度）')
    for aa in ax:aa.set_xscale('log');aa.axvline(9.325359e21,ls=':',lw=1,color='.4');aa.axvline(2.300064e22,ls='--',lw=1,color='.4')
    save(fig,'FIG-Q3-R6-001','基线预算路径：虚线为统计支持边界触发，后段平台不代表现实扩展失效。',[str((B/'budget_path.csv').relative_to(ROOT))],['CAND-Q3-R6-BASE-001','CAND-Q3-R6-SHIFT-001'])
    fig,ax=plt.subplots(2,1,figsize=(6.2,5.5),sharex=True,layout='constrained')
    for fam,label,col in zip(FAMS,LABELS,COLORS):
        g=q[(q.L_ctx==2048)&(q.qcap==1)&(q.cost_family==fam)&(q.factor==1)].sort_values('Budget_FLOPs')
        ax[0].plot(g.Budget_FLOPs,g.Q,label=label,color=col);ax[1].plot(g.Budget_FLOPs,base.loss.to_numpy()-g.loss.to_numpy(),color=col)
    ax[0].axhline(.5,color='.4',ls=':');ax[0].set_ylabel('最优质量 Q（情景刻度）');ax[0].legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,1))
    ax[1].set_ylabel('相对 OFF 的 Loss 改善');ax[1].set_xlabel('预算 C（FLOPs，对数刻度）')
    for aa in ax:aa.set_xscale('log')
    save(fig,'FIG-Q3-R6-002','同一REFERENCE质量收益假设下，三类题面成本导致不同质量投入路径。',[str((S/'quality_context_path.csv').relative_to(ROOT))],['SCEN-Q3-R6-QUAL-001'])
    fig,ax=plt.subplots(figsize=(6.2,4.4),layout='constrained')
    for fam,label,col in zip(FAMS,LABELS,COLORS):
        g=be[be.cost_family==fam].sort_values('Budget_FLOPs');ax.plot(g.Budget_FLOPs,g.local_threshold_h,color=col,label=label+'：局部');ax.plot(g.Budget_FLOPs,g.global_threshold_h,color=col,ls='--',label=label+'：全局')
    ax.axhline(.3619952862,color='.2',ls=':',label='REFERENCE 收益系数');ax.set_xscale('log');ax.set_yscale('symlog',linthresh=.003);ax.set_ylim(0,.6);ax.set_xlabel('预算 C（FLOPs，对数刻度）');ax.set_ylabel('质量投入门槛 h（对称对数刻度）');ax.legend(frameon=False,ncol=2,loc='lower center',bbox_to_anchor=(.5,1))
    save(fig,'FIG-Q3-R6-003','对数成本的局部与全局质量激活门槛分离，不能只用一阶条件判断投入。',[str((S/'quality_break_even.csv').relative_to(ROOT))],['SCEN-Q3-R6-BREAK-001'])
    fig,ax=plt.subplots(2,1,figsize=(6.2,5.7),layout='constrained')
    for (L,g),sty in zip(ctx.groupby('L_ctx'),['-','--','-.',':','-']):ax[0].plot(g.Budget_FLOPs,g.loss,label=f'{L:g}',ls=sty)
    ax[0].set_xscale('log');ax[0].set_xlabel('预算 C（FLOPs，对数刻度）');ax[0].set_ylabel('基线预测 Loss');ax[0].legend(title='架构上下文档位情景（token）',frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,1))
    levels=np.array(sorted(ctx.L_ctx.unique()));ax[1].plot(levels,.0002*levels/6,'o-',color=COLORS[0]);ax[1].set_xscale('log');ax[1].set_yscale('log');ax[1].axhline(1,color='.4',ls=':');ax[1].axvline(30000,color='.4',ls=':');ax[1].set_xlabel('外生 L（token，对数刻度）');ax[1].set_ylabel('注意力 / 基础训练成本比')
    save(fig,'FIG-Q3-R6-004','C7最大上下文档位仅用作外生情景；30000是成本代理等值点。',[str((S/'context_baseline.csv').relative_to(ROOT))],['SCEN-Q3-R6-CTX-001'])
    fig,ax=plt.subplots(2,1,figsize=(6.2,5.5),sharex=True,layout='constrained');x=qq[qq.L_ctx==2048];lo=x[x.conditional_quantile==.025].sort_values('Budget_FLOPs');hi=x[x.conditional_quantile==.975].sort_values('Budget_FLOPs')
    ax[0].plot(lo.Budget_FLOPs,(hi.loss.to_numpy()-lo.loss.to_numpy())*1e5,color=COLORS[0]);ax[0].set_ylabel(r'条件参数分位带宽（Loss × $10^5$）')
    ax[1].fill_between(env.Budget_FLOPs,env.loss_min,env.loss_max,color='#b8ccd7',label='情景范围（非置信区间）');ax[1].plot(base.Budget_FLOPs,base.loss,color=COLORS[0],label='quality OFF');ax[1].set_ylabel('预测 Loss');ax[1].legend(frameon=False,loc='upper right');ax[1].set_xlabel('预算 C（FLOPs，对数刻度）')
    for aa in ax:aa.set_xscale('log')
    save(fig,'FIG-Q3-R6-005','给定附件的参数带极窄，机制情景范围更宽；两者均不保证外部覆盖。',[str((U/'conditional_quantiles.csv').relative_to(ROOT)),str((U/'scenario_envelope_NOT_CI.csv').relative_to(ROOT))],['SENS-Q3-R6-UNC-001'])
    fig,ax=plt.subplots(2,1,figsize=(6.2,5.5),sharex=True,layout='constrained');ax[0].plot(base.Budget_FLOPs,base.mu_per_1e18,color=COLORS[0]);ax[0].set_yscale('symlog',linthresh=1e-5);ax[0].set_ylabel(r'$\mu$（Loss / $10^{18}$ FLOPs）')
    for fam,label,col in zip(FAMS,LABELS,COLORS):
        g=q[(q.L_ctx==2048)&(q.qcap==1)&(q.factor==1)&(q.cost_family==fam)].sort_values('Budget_FLOPs');val=np.where(np.isclose(g.Q,1),g.quality_cap_value,0);ax[1].plot(g.Budget_FLOPs,val,color=col,label=label)
    ax[1].set_ylabel('质量上限放松价值（Loss / Q）');ax[1].legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,1.01));ax[1].set_xlabel('预算 C（FLOPs，对数刻度）')
    for aa in ax:aa.set_xscale('log')
    save(fig,'FIG-Q3-R6-006','预算影子价在统计支持饱和后为零；质量上限价值仍只属收益假设。',[str((U/'shadow_prices.csv').relative_to(ROOT))],['SENS-Q3-R6-SHADOW-001'])
    (OUT/'figure_manifest.json').write_text(json.dumps({'script_sha256':sha(Path(__file__)),'figures':M},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (OUT/'figure_references.tex').write_text('\n'.join('\\begin{figure}[!htbp]\n\\centering\n\\includegraphics[width=15cm]{'+f['paths'][1]['path']+'}\n\\caption{'+f['claim']+'}\n\\end{figure}' for f in M)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({f['id']:[t['text'] for t in f['text_checks'] if not t['inside']] for f in M},ensure_ascii=False))
if __name__=='__main__':main()
