"""Q2 scientific figures from QA-checked immutable outputs; no model fitting."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties,findfont
ROOT=Path(__file__).resolve().parents[2]
B=ROOT/'06_results/raw/EXP-Q2-ND-R5-20260924-v1';S=ROOT/'06_results/raw/SCEN-Q2-R5-20260924-v3'
OUT=ROOT/'06_results/figures/round5';OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'Microsoft YaHei','font.size':11,'axes.labelsize':11,'xtick.labelsize':10,
    'ytick.labelsize':10,'legend.fontsize':10,'axes.unicode_minus':False,'pdf.fonttype':42,'ps.fonttype':42,
    'axes.spines.top':False,'axes.spines.right':False,'axes.grid':False,'savefig.dpi':300})
manifest=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(fig,name,claim,source,rids):
    fig.canvas.draw();renderer=fig.canvas.get_renderer();bounds=fig.bbox
    textchecks=[]
    for artist in fig.findobj(matplotlib.text.Text):
        if artist.get_visible() and artist.get_text():
            box=artist.get_window_extent(renderer)
            # Axis ticks outside the displayed limits are renderer objects, not drawn labels.
            if artist in [x for ax in fig.axes for x in ax.get_xticklabels()+ax.get_yticklabels()]:
                if box.x1<0 or box.y1<0 or box.x0>bounds.x1 or box.y0>bounds.y1:continue
            textchecks.append(dict(text=artist.get_text(),font_pt=artist.get_fontsize(),
                inside=bool(box.x0>=-1 and box.y0>=-1 and box.x1<=bounds.x1+1 and box.y1<=bounds.y1+1)))
    paths=[]
    for ext in ['png','pdf']:
        p=OUT/f'{name}.{ext}';fig.savefig(p);paths.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)))
    manifest.append(dict(id=name,paths=paths,claim=claim,source=source,result_ids=rids,
        reader_task=claim,publish=True,placement='Q2 candidate section; gate3 pending',width_cm=15.748,
        recommended_insert_cm=15.0,min_effective_font_pt=10*15/15.748,text_checks=textchecks))
    plt.close(fig)
def main():
    qa=json.loads((ROOT/'10_review/MODELING_PHASE2_R5_NUMERICAL_QA_20260924.json').read_text());assert qa['status']=='PASS'
    d=pd.read_csv(B/'training_predictions.csv');colors=plt.cm.viridis(np.linspace(.05,.9,8))
    fig,axes=plt.subplots(2,1,figsize=(6.2,5.8),sharex=True,layout='constrained')
    for (n,g),col in zip(d.groupby('N_params_B'),colors):
        axes[0].plot(g.D_tokens_B,g.val_loss,color=col,lw=1.2,label=f'{n:.3g}B')
        axes[0].scatter(g.D_tokens_B.iloc[::10],g.prediction.iloc[::10],s=12,marker='x',color=col)
        axes[1].plot(g.D_tokens_B,g.residual*1e4,color=col,lw=.8)
    axes[0].set_ylabel('附件 B1 Loss');axes[1].set_ylabel(r'预测 - 观测（$\times 10^{-4}$）');axes[1].set_xlabel('数据规模 D（十亿 token，对数刻度）')
    axes[0].set_xscale('log');axes[1].axhline(0,color='.45',lw=.7,ls='--')
    axes[0].legend(ncol=4,loc='lower center',bbox_to_anchor=(.5,1.02),frameon=False,columnspacing=.8,handlelength=1.4)
    save(fig,'FIG-Q2-R5-001','八条附件轨迹与幂律吻合；微小残差不证明外部真实性。',[str((B/'training_predictions.csv').relative_to(ROOT))],['CAND-Q2-R5-ND-001','CAND-Q2-R5-UNC-001'])
    m=pd.read_csv(B/'validation_metrics.csv');kinds=['LONO','FORWARD','BLOCK2D'];labels=['整规模留出','向前预测','双维分块'];fig,ax=plt.subplots(figsize=(6.2,4.1),layout='constrained');xx=np.arange(3)
    for i,(model,label,col) in enumerate([('S0','训练均值','#aaaaaa'),('Slog','对数线性','#c47b38'),('S1','加性幂律','#28658b')]):
        vals=[m[(m.kind==k)&(m.model==model)].rmse.mean() for k in kinds]
        ax.bar(xx+(i-1)*.24,vals,width=.23,label=label,color=col)
    ax.set_xticks(xx,labels);ax.set_yscale('log');ax.set_ylabel('轨迹宏平均 RMSE（Loss，对数刻度）');ax.legend(loc='upper center',bbox_to_anchor=(.5,1.18),ncol=3,frameon=False)
    save(fig,'FIG-Q2-R5-002','三类无随机拆行验证中，加性幂律优于两个透明对照。',[str((B/'validation_metrics.csv').relative_to(ROOT))],['CAND-Q2-R5-VAL-001'])
    ef=pd.read_csv(B/'marginal_effects.csv');ef=ef[ef.support=='OBSERVED_GRID'];fig,axes=plt.subplots(2,1,figsize=(6.2,5.8),sharex=True,layout='constrained')
    for ax,col,label in zip(axes,['elasticity_N','elasticity_D'],['|总 Loss 规模弹性|','|总 Loss 数据弹性|']):
        tab=ef.pivot(index='N_params_B',columns='D_tokens_B',values=col)
        mesh=ax.pcolormesh(tab.columns,tab.index,-tab.to_numpy(),shading='nearest',cmap='cividis');ax.set_xscale('log');ax.set_yscale('log');ax.set_ylabel('N（十亿参数）');fig.colorbar(mesh,ax=ax,label=label)
    axes[1].set_xlabel('D（十亿 token，对数刻度）')
    save(fig,'FIG-Q2-R5-003','幂指数为常数，总Loss弹性随N-D状态变化。',[str((B/'marginal_effects.csv').relative_to(ROOT))],['CAND-Q2-R5-MARG-001'])
    qc=pd.read_csv(S/'quality_cell_slopes.csv');qs=pd.read_csv(S/'quality_substitution_scenarios.csv');qs=qs[qs.mechanism=='additive']
    fig,axes=plt.subplots(2,1,figsize=(6.2,5.8),layout='constrained')
    for (dv,z),marker in zip(qc.groupby('D_tokens_B'),['o','s','^','D','v']):
        axes[0].plot(z.N_params_B,-z.slope,marker=marker,ms=3,label=f'D={dv:g}B',lw=1)
    axes[0].set_xscale('log');axes[0].set_ylabel('B7 条件质量改善斜率 g');axes[0].set_xlabel('N（十亿参数，对数刻度）');axes[0].legend(ncol=3,frameon=False,loc='lower center',bbox_to_anchor=(.5,1.01))
    axes[1].plot(qs.factor,100*qs.N_saving_fraction,'o-',color='#28658b',label='参数规模 N')
    axes[1].plot(qs.factor,100*qs.D_saving_fraction,'s--',color='#c47b38',label='数据规模 D')
    axes[1].set_xlabel('假定跨来源质量斜率倍数（情景参数）');axes[1].set_ylabel('等 Loss 减少比例（%）');axes[1].legend(frameon=False,loc='upper left');axes[1].set_ylim(-2,50);axes[1].set_xticks([0,.5,1,1.5])
    save(fig,'FIG-Q2-R5-004','上图为半合成表内斜率；下图为假定Q从0.5增至0.6的替代情景，不能解释为真实收益。',[str((S/'quality_cell_slopes.csv').relative_to(ROOT)),str((S/'quality_substitution_scenarios.csv').relative_to(ROOT))],['CAND-Q2-R5-QUAL-001','SCEN-Q2-R5-SUB-001'])
    (OUT/'figure_manifest.json').write_text(json.dumps(dict(script_sha256=sha(__file__),font=findfont(FontProperties(family='Microsoft YaHei')),figures=manifest),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    tex='\n'.join('\\begin{figure}[!htbp]\n\\centering\n\\includegraphics[width=15cm]{'+x['paths'][1]['path']+'}\n\\caption{'+x['claim']+'}\n\\end{figure}' for x in manifest)
    (OUT/'figure_references.tex').write_text(tex+'\n',encoding='utf-8')
    print(json.dumps({x['id']:{'all_text_inside':all(t['inside'] for t in x['text_checks']),'minimum_effective_pt':x['min_effective_font_pt']} for x in manifest},ensure_ascii=False))
if __name__=='__main__':main()
