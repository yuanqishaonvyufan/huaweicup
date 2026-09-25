"""Assemble Q3 checked tables, paper candidate and scoped Q4 handoff."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];MODEL=ROOT/'03_models/modeling_phase3/round6';TABLE=ROOT/'06_results/tables/round6'
B=ROOT/'06_results/raw/EXP-Q3-BASE-R6-20260924-v1';S=ROOT/'06_results/raw/SCEN-Q3-R6-20260924-v1';U=ROOT/'06_results/raw/UNC-Q3-R6-20260924-v1'
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n',encoding='utf-8',newline='\n')
def md(d):
    fmt=lambda v:f'{v:.7g}' if isinstance(v,(float,np.floating)) else str(v)
    return '| '+' | '.join(d.columns)+' |\n| '+' | '.join(['---']*len(d.columns))+' |\n'+'\n'.join('| '+' | '.join(fmt(v) for v in row)+' |' for row in d.itertuples(index=False,name=None))
def main():
    cfg=json.loads((ROOT/'05_experiments/configs/Q3_R6_FROZEN_v1.json').read_text());qa=json.loads((ROOT/'10_review/MODELING_PHASE3_R6_NUMERICAL_QA_20260924.json').read_text());assert qa['status']=='PASS'
    bs=json.loads((B/'summary.json').read_text());ss=json.loads((S/'summary.json').read_text());us=json.loads((U/'summary.json').read_text())
    b=pd.read_csv(B/'budget_path.csv');q=pd.read_csv(S/'quality_context_path.csv');ctx=pd.read_csv(S/'context_baseline.csv');be=pd.read_csv(S/'quality_break_even.csv');mix=pd.read_csv(S/'mixture_scenarios.csv');cq=pd.read_csv(U/'conditional_quantiles.csv');sh=pd.read_csv(U/'shadow_prices.csv');sp=pd.read_csv(S/'supply_stress.csv')
    sel=lambda df:df[df.Budget_FLOPs.isin([1e19,1e22,1e24])]
    tables={
      'TABLE-Q3-R6-001':sel(b)[['Budget_FLOPs','N_B','D_B','loss','mu_per_1e18','total_FLOPs','active_constraints']],
      'TABLE-Q3-R6-002':sel(q[(q.L_ctx==2048)&(q.factor==1)&(q.qcap==1)])[['cost_family','Budget_FLOPs','N_B','D_B','Q','loss','quality_FLOPs']],
      'TABLE-Q3-R6-003':ctx[ctx.Budget_FLOPs.eq(1e19)][['L_ctx','N_B','D_B','loss','mu_per_1e18']],
      'TABLE-Q3-R6-004':sel(be)[['Budget_FLOPs','cost_family','local_threshold_h','global_threshold_h','global_witness_Q']],
      'TABLE-Q3-R6-005':sel(cq[cq.L_ctx==2048]),
      'TABLE-Q3-R6-006':sel(sh[(sh['mode']=='BASELINE')&(sh.L_ctx==2048)])[['Budget_FLOPs','mu','N_upper_marginal_value_per_B','D_upper_marginal_value_per_B','context_cost_derivative']],
      'TABLE-Q3-R6-007':mix,
      'TABLE-Q3-R6-008':sel(sp)[['D_cap_factor','Budget_FLOPs','N_B','D_B','loss','active_constraints']],
      'TABLE-Q3-R6-009':sel(q[(q.L_ctx==2048)&(q.factor==1)&(q.qcap==.75)])[['cost_family','Budget_FLOPs','N_B','D_B','Q','loss','quality_cap_value']]}
    for id,df in tables.items():df.to_csv(TABLE/f'{id}.csv',index=False,lineterminator='\n');write(TABLE/f'{id}.md',md(df))
    report=rf'''# Q3：支持域约束下的算力资源配置

状态：CHECKED / PAPER-READY CANDIDATE；Round6 CP5。Q3 PROVISIONALLY CLOSED，Gate4 READY FOR PRE-REVIEW而非已通过；Q4 NOT STARTED。本报告引用的配置仅在附件量尺、题面算力代理和显式情景内成立。原始Q1/Q2参数没有重估。

## 1. 数据证据、决策边界与成本模型

本问用Q2的附件内部幂律评价Loss，用题面提供的FLOPs代理约束资源，不引入美元、GPU账单或数据市场价格。以n、d表示十亿参数和十亿token，c=C/10^18，外生上下文L取C7记录的架构档位。训练、注意力和质量处理都使用同一数据量d，避免把过滤前后token混用。

$$
c_{{used}}=[k(L)n+r(q)]d,\quad k(L)=6+0.0002L,\quad
r(q)=\frac{{[g(q)-g(0.5)]_+}}{{10^9}}.
$$

三条题面成本依次为g_exp(q)=10^7 exp(6q)、g_power(q)=5×10^9 q^4、g_log(q)=2×10^9 ln(1+10q)。g的单位是代理FLOPs/token；原参数不为获得期望配置而重标。q0=.5是明示情景，不能代指DQ0或真实可识别质量。主baseline关闭质量收益，q=q0，因此质量增量成本为零；p固定为Q1训练配比均值，跨源配比运输为零。

题面未给独立领域价格/供应量，故不虚构C_mix或现实供应上限。固定p时不增加一个未定义的成本项，不代表现实配比调整免费。n∈[.070542,11.965825]、d∈[.134,299.893]来自Gate3的统计支持范围，不是官方硬件界限。预算包含题面1e19/1e22/1e24及事前冻结的51点对数网格；所有预算都是上界，允许因支持饱和而不花完。

来源审计见Q3_DATA_COST_AUDIT_v1；成本、目标及支持在CP1远端确认后才求解。C7共45条架构记录，档位为2048/4096/8192/32768/131072；参考2048来自Pythia架构档位选择，不是实测训练长度。

## 2. 基线解析最优与数值核验

目标为L=E+A n^(-a)+B d^(-b)，五参数完全继承Q2。设K=c/k，未触及上界时预算紧、d=K/n，从而

$$
n_*=\left(\frac{{aA}}{{bB}}\right)^{{1/(a+b)}}K^{{b/(a+b)}},\qquad d_*=K/n_*.
$$

n的实际可行区间为[max(n_min,K/d_max),min(n_max,K/d_min)]，把上式截取到区间即得到盒约束全局解；若K≥n_max d_max则两变量取上限。理由是在x=log n坐标，目标的两项指数函数之和严格凸。内点KKT条件aU=bV，其中U=A n^(-a)、V=B d^(-b)，预算弹性为b/(a+b)={bs['transitions']['N_budget_elasticity_interior']:.6f}和a/(a+b)={bs['transitions']['D_budget_elasticity_interior']:.6f}。这给出机制解释，数值优化只作验证。

{md(tables['TABLE-Q3-R6-001'])}

51个预算点、每点4个SLSQP初值全部成功，最坏目标差{bs['max_loss_gap']:.3g}，最大投影KKT残差{bs['max_kkt']:.3g}。解析和数值解一致并不赋予目标外部实证资格；配置仍是ATTACHMENT-INTERNAL ESTIMATED关系在PROBLEM-PROVIDED COST PROXIES下的条件解（CAND-Q3-R6-BASE-001）。图FIG-Q3-R6-001展示完整路径。

## 3. 结构转移与支持限制

将“结构转移”明确为最优解的活跃约束集合变化，另记录离散情景候选切换；平滑的n/d比例变化不自动算质变。参考L=2048下，先于9.325359×10^21 FLOPs触及d上限，随后n随预算线性增加，到2.300064×10^22 FLOPs两上限同时饱和，之后Loss平台为2.093379。无界公式的n上限交点6.886597×10^22已经不在实际内点路径上，不能误报为实际第二转移。

在1e24预算处，baseline只使用约2.3001%的预算，其余闲置源自统计支持限制。这个平台不能解释为现实扩展训练必然失效。把d上限缩为原来的.25/.5只作为未知供应的压力情景，高预算平台Loss分别为2.212525/2.147192；没有把这些上限伪装成实际供应。完整路径及活跃集合转变区间见active_set_transitions.csv和TABLE-Q3-R6-008（CAND-Q3-R6-SHIFT-001）。

## 4. 质量收益、成本选择与激活门槛

广义目标采用F=L_B(n,d)-h(q-.5)，h∈{{0,.5,1,1.5}}×0.3619952862，对应OFF/LOW/REFERENCE/HIGH。0.361995来自B7表内半合成校准；运输到此成本模型后全部为SCENARIO-CONDITIONAL，而非真实因果质量弹性。质量取[.5,1]，另以.75上限做压力比较。三种成本均按题面原值使用。

固定q时，d=min(d_max,c/(kn+r))；预算紧段的n一阶条件为

$$
-aA n^{{-a}}+bB\left(\frac{{kn+r}}{{c}}\right)^b\frac{{kn}}{{kn+r}}=0.
$$

此条件的负项随n变得不那么负，正项严格递增，故固定q有唯一内点或边界解。外层q枚举端点及101点网格的所有局部谷，逐谷有界精化，再以201点加密验证；另作每情景3初值SLSQP对照，不把非凸质量目标交给单一起点。

{md(tables['TABLE-Q3-R6-002'])}

结果包含1377个质量/context/质量cap配置，三类成本在低预算给出不同q。在1e19、REFERENCE收益下，指数成本q≈.674774，幂成本q≈.506789，对数成本q=1。三者Loss依次2.980638、2.998908、2.935776。高预算三者均到q上限且n/d支持饱和，REFERENCE情景Loss=1.912382；这是收益假设下的平台，不是实测性能（SCEN-Q3-R6-QUAL-001；图FIG-Q3-R6-002）。

令mu为归一预算c的正乘子，局部质量激活要求h>mu d r'(q0)。这个条件只回答“小幅投入是否划算”。全局质量启动门槛应比较有限变化：

$$
h_{{crit}}(c)=\inf_{{q>q_0}}\frac{{L_{{ND}}^*(c,q)-L_{{ND}}^*(c,q_0)}}{{q-q_0}},
$$

并将q趋于q0的局部极限作为候选。数值实现按事前冻结的网格/局部精化计算该一维比值，不宣称一般解析全局证明。

{md(tables['TABLE-Q3-R6-004'])}

关键反例是低预算对数成本：局部门槛.472240高于REFERENCE h=.361995，但全局门槛.235678更低，故小幅投资不优而直接投向q=1可更优。4131次SLSQP中17个起点进入较差局部解，最坏Loss差.082847；4次线搜索返回失败，全部保存、不用作成功证据。每个情景仍至少有一个成功数值解与预冻结嵌套解吻合，最坏差1.29e-12；101/201网格目标差4.44e-16。由此保留局部与全局门槛的差别，而不声称“所有初值一致”（SCEN-Q3-R6-BREAK-001；图FIG-Q3-R6-003）。

## 5. 领域配比与可实施性

当前Q1配比证据主要在1M，60M仅部分形状转移，1B已失败；B1主域最低70.542M，与前两个规模不重合。因此主资源优化不能合法地加入一个已识别的固定配比系数，k_mix保持0；p用训练均值固定，D_i=p_i D保持数量一致。

为了回答局部领域替代，另在A源构造513个有限候选：训练均值p0以及(p0+p_i)/2。每点都有显式非负凸组合权重，处于观测凸包内，simplex最大误差3.33e-16；同时记录最近训练距离，而不只核非负和为1。固定M1的解析预测用于比较，不重训、不重新使用A6–A11选模。

最小R0关联候选136的中心化变化约-.353773，但13域中10域改善、3域恶化；60M的.25/.5衰减只能作为未校准情景。真实供给仍UNKNOWN，有限候选最小值不是可部署最优，更不加入B1绝对Loss。zero-transfer分支按约定保留参考p0；没有计算1B运输。配比边界是统计候选集合，现实域价格和供给影子价未识别（SCEN-Q3-R6-MIX-001，TABLE-Q3-R6-007）。

## 6. 上下文敏感性与30k交点

所有五个C7架构档位作为外生场景比较，不把L作为内点优化变量。

{md(tables['TABLE-Q3-R6-003'])}

固定预算1e19，L从2048升到131072时，代理开销提高，baseline配置由n=.221309/d=7.049698变为n=.106754/d=2.907819，Loss由2.998935升至3.367161。此比较只计成本，当前Loss目标没有独立的长上下文能力收益项，因此不能由此推荐实际系统缩短上下文。

$$
C_{{attn}}/C_{{train}}=\eta L/6,\qquad L_{{crit}}=6/\eta=30000.
$$

该比例在固定L时与预算无关。32768和131072档位分别给出比例1.092267和4.369067，2048档位约.068267。30000不是实测临界点、训练窗口或官方推荐值，只是两代理项相等的解析位置（SCEN-Q3-R6-CTX-001；图FIG-Q3-R6-004）。

## 7. 影子价格与约束的边际价值

mu以Loss/10^18 FLOPs计，价值函数满足dF*/dC=-mu/10^18。内点mu=aU/c=bV/c；d封顶而n自由时mu=aU/c，n封顶而d自由时mu=bV/c，全部收益相关变量封顶且预算松弛时mu=0。支持上界放松的价值需要扣去预算机会成本，例如n上界为max(0,aA n^(-a-1)-mu k d)，d上界为max(0,bB d^(-b-1)-mu(kn+r))；只有相应上界活跃才报告。qcap的条件价值为max(0,h-mu d r'(qcap))。

{md(tables['TABLE-Q3-R6-006'])}

预算影子价为零并不意味着扩充统计证据没有价值：高预算两支持上限活跃，模型内放松n/d界仍有正边际值，但它们是曲面的局部导数，尚无域外验证保证，不是现实资源的市场价格。context成本边际为mu eta n d。对baseline与质量配置共1632个预算乘子进行有限差分核对，最坏绝对差8.97e-10（SENS-Q3-R6-SHADOW-001；图FIG-Q3-R6-006）。

## 8. 参数和情景不确定性

保留Q2整轨迹bootstrap的200个联合五参数向量，不把边际区间重新独立组合。在5档context×51预算传播，得到51000条条件配置，检查每个向量的预算Loss单调性。分位数据包含n、d、Loss和mu，只有数值敏感性含义。

例如1e19/2048的条件2.5–97.5%区间约为n=[.221249,.221387]、d=[7.047196,7.051612]、Loss=[2.998852,2.998986]。窄带来自附件曲面的高度规则，不覆盖来源、真实独立训练或结构错误。与之分开的LOW/REFERENCE/HIGH/成本类型范围是情景包络，明确不是CI；图FIG-Q3-R6-005分别显示参数带宽和情景范围（SENS-Q3-R6-UNC-001）。

## 9. 验证、适用范围与后续接口

独立只读QA共{len(qa['checks'])}项全部通过：核成本十亿单位、每个目标回代、预算/支持/质量界、KKT与互补、OFF退化为baseline、多起点失败保留、候选凸包见证/13域、全部51000配置Loss重算及单调性、影子价差分和来源哈希。数值PASS表示预定条件问题求解可靠，不代替真实世界模型验证。

Q3给Q4传递带证据标签的预算配置、Loss路径、结构转移、影子价、参数敏感性和单独情景范围；不把Loss直接改写为Benchmark能力，不启动桥接或趋势预测。Q1/Q2的外部来源、TYPE E=0、1B失败和B8隔离全部保持。Gate4需要审查这些用途界限后再决定下游使用；本轮Q3仅暂定关闭，Q4仍未启动。

有效Run：EXP-Q3-BASE-R6-20260924-v1；SCEN-Q3-R6-20260924-v1；UNC-Q3-R6-20260924-v1。逐行原始输出及哈希在06_results/raw/对应目录，九表和六候选图在round6目录。最终论文模板/全文排版尚未执行，单图检查不等同最终嵌入质量验收。
'''
    write(MODEL/'Q3_RESULTS_REPORT_v1.md',report);write(ROOT/'08_paper/sections/Q3_ROUND6_PAPER_CANDIDATE_v1.md',report)
    limits='''# Q3 limitations v1

- 五参数仅B1附件内部估计，外部来源Alert未解除；优化不把条件目标升格为真实能力。
- 所有成本是题面FLOPs代理，不是美元/GPU账单。领域价格、真实供应与DQ0→Q_score映射均UNKNOWN。
- N/D范围是统计支持；高预算闲置、Loss平台、支持界影子价来自该限制，不是产业算力收益上限。
- 质量收益来自半合成校准后的显式运输假设，OFF为基线；质量成本由题面给定也不能识别真实收益。
- 对数成本外层非凸，17次局部劣解和4次失败保留。嵌套搜索/201点加密/成功数值对照不等于任意非凸函数的形式全局证明。
- p只有513个显式凸包内候选；当前A-source规模与B1支持不重叠，故无联合p最优。13域存在3域恶化，R0不能替代R3；真实供给未核。1B运输未执行。
- C7架构最大上下文不等于训练窗口；L场景的比较只计代理成本，未识别长上下文能力收益，不能推导实际缩短窗口的建议。
- 30000只为两成本代理相等点，固定L下预算不改变两项比例；结构转移只按活跃集合/情景候选切换。
- 200联合参数分位带仅给定附件的数值敏感性；质量/成本/配比情景包络非CI，均不保证外部覆盖。
- B8不读取；Q4桥接/Benchmark/预测未执行；无独立Opus或人工复审宣称。六图单图已核，最终模板嵌入尚待全文阶段。
''';write(MODEL/'Q3_LIMITATIONS_v1.md',limits)
    delivery='''# Q3 delivery map / figure and table plan v1

不建立平行重复文档，以下按等价章节归档：

| Requested artifact | Authoritative file / section |
|---|---|
| Q3_DATA_COST_AUDIT_v1 | 01_data/audits/modeling_phase3/round6/Q3_DATA_COST_AUDIT_v1.md |
| Q3_COST_MODEL_v1 | 本目录同名 |
| baseline/generalized spec | Q3_MODEL_SPEC_v1.md，前两节分别冻结 |
| Q3_BASELINE_OPTIMIZATION_v1 | 本目录同名、EXP-Q3-BASE输出 |
| Q3_GENERALIZED_OPTIMIZATION_v1 | 本目录同名、SCEN-Q3输出 |
| budget/quality/mixture/context/structure results | Q3_RESULTS_REPORT_v1.md §2–6，九张表、active_set_transitions.csv |
| uncertainty/shadow analysis | Q3_RESULTS_REPORT_v1.md §7–8，UNC-Q3输出 |
| validation/limitations | 07_validation/round6/Q3_VALIDATION_REPORT_v1.md；本目录Q3_LIMITATIONS_v1.md |
| Q3_FIGURE_PLAN / TABLE_PLAN | 本文件；六图manifest与九表逐项下列 |
| Q3_TO_Q4_INTERFACE | 02_analysis/consensus/Q3_TO_Q4_INTERFACE_v1.md及本目录JSON |
| Gate4 package / final QA | 10_review/GATE4_PRE_REVIEW_PACKAGE_v1.md；MODELING_PHASE3_R6_QA_20260924.md |

六图：001基线配置/支持边界；002三成本质量路径；003局部/全局激活；004外生上下文/成本交点；005参数带与情景范围分离；006影子价与quality cap。每图对应来源/Result ID/脚本/300dpi PNG及PDF/15cm字号见figure_manifest。都是正文候选，Gate4与最终模板检查后才正式采用。

九表：001三档baseline；002REFERENCE质量；003五context低预算；004break-even；005条件分位；006影子价；007有限配比；008供应压力；009quality cap压力。来源分别为有效Run的原始CSV，生成入口round6_package.py。原全路径结果保留，候选精简表不替代机器结果。
''';write(MODEL/'Q3_DELIVERY_FIGURE_TABLE_PLAN_v1.md',delivery)
    iface={'status':'Q3 PROVISIONALLY CLOSED / GATE4 PRE-REVIEW READY','source_runs':[bs['run_id'],ss['run_id'],us['run_id']],
        'cost_type':'PROBLEM-PROVIDED FLOPs PROXIES','baseline_loss_scope':'ATTACHMENT-INTERNAL B1','units':{'N':'billion parameters','D':'billion tokens','C':'FLOPs','mu':'Loss per 1e18 FLOPs'},
        'support':{'N':cfg['N_bounds'],'D':cfg['D_bounds'],'real_supply':'UNKNOWN'},'baseline_quality':'OFF','main_mixture_transport':0,
        'allowed_to_Q4':['conditional N/D/Loss budget paths','source-labeled scenarios','active-support transitions','budget shadow values','joint-parameter numerical sensitivity'],
        'not_established':['Loss-to-Benchmark bridge','causal quality effect','external prediction coverage','deployable mixture configuration','actual training context'],
        'quality_scenarios':'SEMI-SYNTHETIC CALIBRATED source; SCENARIO-CONDITIONAL transport','mixture':'A-source local only; no B1 scale overlap; no1B transport','B8':'QUARANTINED',
        'uncertainty':'parameter quantiles are conditional sensitivity; scenario envelope NOT CI','next_gate':'Gate4 review required','Q4_started':False,'active_final_model':None}
    write(MODEL/'Q3_TO_Q4_INTERFACE_v1.json',json.dumps(iface,ensure_ascii=False,indent=2))
    write(ROOT/'02_analysis/consensus/Q3_TO_Q4_INTERFACE_v1.md','''# Q3 → Q4 interface v1

CHECKED CANDIDATE，Q3 PROVISIONALLY CLOSED，Gate4待审；本文件不是Gate4共识。机器接口03_models/modeling_phase3/round6/Q3_TO_Q4_INTERFACE_v1.json。

可传受限预算N/D/Loss、proxy成本分解、支持边界、质量条件情景、局部配比限制、影子价、条件参数集合/独立情景范围。预算乘子单位Loss/1e18 FLOPs；模型N/D均十亿。所有来源和证据等级必须随下游使用保留。

不传未经验证的能力分数、Loss–Benchmark桥接、真实质量弹性、1B配比运输、外部置信区间、实际训练context或可部署最优。C7最大context与30000代理交点不变。Q4若推进需独立完成C8、桥接、时间/族/评测口径验证；本轮未执行任何Q4分析。
''')
    write(ROOT/'07_validation/round6/Q3_VALIDATION_REPORT_v1.md',f'''# Q3 validation v1

PASS FOR CONDITIONAL Q3 PACKAGE。独立数值检查{len(qa['checks'])}项全PASS，机器记录10_review/MODELING_PHASE3_R6_NUMERICAL_QA_20260924.json。baseline51×4全部成功/解析一致；1377情景均有成功数值对照，4失败和17劣局部起点保留；网格加密/KKT/预算/单调性均通过。51000联合参数结果逐行重算；1632影子价有限差分max8.97e-10。513配比显式凸包见证、和为1、全13域回代通过。

查模型失配与算法失效分别处理：局部非凸求解的差异已由预定算法交叉核验，不删除差异、不改规格。成本十亿单位/原参数/同D、上下文解释、source hashes、OFF退化、TYPE E=0、B8与Q4边界均核对。没有把程序QA当作模型外部验证。

六图单图检查通过；最终模板编译未执行。所有结果维持CHECKED候选或情景，Gate4未通过。限制见Q3_LIMITATIONS_v1，问题覆盖及等价文档索引见Q3_DELIVERY_FIGURE_TABLE_PLAN_v1。
''')
    print('Built Q3 report/paper candidate,9 tables,delivery map,limitations,validation and interface')
if __name__=='__main__':main()
