"""Build Q2 candidate tables/report/interface from audited results; no estimation."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
B=ROOT/'06_results/raw/EXP-Q2-ND-R5-20260924-v1';S=ROOT/'06_results/raw/SCEN-Q2-R5-20260924-v3'
MODEL=ROOT/'03_models/modeling_phase2/round5';TABLE=ROOT/'06_results/tables/round5'
PAPER=ROOT/'08_paper/sections';VALID=ROOT/'07_validation/round5'
def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def md(d):
    fmt=lambda v:f'{v:.6g}' if isinstance(v,(float,np.floating)) else str(v)
    return '| '+' | '.join(d.columns)+' |\n| '+' | '.join(['---']*len(d.columns))+' |\n'+'\n'.join('| '+' | '.join(fmt(v) for v in row)+' |' for row in d.itertuples(index=False,name=None))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    for p in [MODEL,TABLE,PAPER,VALID]:p.mkdir(parents=True,exist_ok=True)
    q=json.loads((ROOT/'10_review/MODELING_PHASE2_R5_NUMERICAL_QA_20260924.json').read_text());assert q['status']=='PASS'
    s=json.loads((B/'summary.json').read_text());t=json.loads((S/'summary.json').read_text());p=s['parameters'];E,A,Bv,a,b=[p[k] for k in ['E','A','B','alpha','beta']]
    parameters=pd.DataFrame([dict(parameter=k,estimate=p[k],conditional_p025=s['parameter_conditional_interval'][k][0],conditional_p975=s['parameter_conditional_interval'][k][2]) for k in p])
    vv=pd.DataFrame([dict(validation=k,**{m:v[m]['macro_rmse'] for m in ['S0','Slog','S1']},S1_worst=v['S1']['worst_rmse']) for k,v in s['validation'].items()])
    ef=pd.read_csv(B/'marginal_effects.csv');e=ef.iloc[-1]
    qsub=pd.read_csv(S/'quality_substitution_scenarios.csv');ex=pd.read_csv(S/'external_shape_diagnostics.csv')
    source=pd.DataFrame([
        ['B1','8 N × 147 D','ATTACHMENT-INTERNAL ESTIMATED','受限N-D参数/导数','外部原始loss锚未恢复'],
        ['B2','7 N × 147 D','SEMI-SYNTHETIC CALIBRATED','中心化形状压力测试','非独立真实轨迹验证'],
        ['B3','插值轨迹','DIAGNOSTIC ONLY','不额外使用；已选择B2','派生自B1，不增独立证据'],
        ['B4/B5','57/44行，12/9族','DIAGNOSTIC ONLY','族内形状/偏序检查','loss量尺未共标；单行族不算相关'],
        ['B6/B7','360⊂450，同一生成表系','SEMI-SYNTHETIC CALIBRATED','Q表内条件斜率与规模调节','生成器/真实质量干预未知'],
        ['B8','不读取','QUARANTINED','无','GENERATOR UNKNOWN / SEARCH PAUSED'],
        ['B9/B10','132元数据/128估算loss','SCENARIO-CONDITIONAL','大规模外推范围讨论','B9四行D=0禁用；B10非验证真值'],
        ['B11/B12','元数据/检查点索引','DIAGNOSTIC ONLY','沿用既有来源核查','不重新打开来源搜索'],
        ['Q1 M1','1M验证、60M部分、1B失败','EMPIRICALLY ESTIMATED','A来源内配比关联，R0+R3','非因果；不运输A/B绝对Loss'],
        ['跨A/B的g、rho、k','外生情景假设','SCENARIO-CONDITIONAL','机制与替代敏感性','TYPE E=0；运输系数未识别']
    ],columns=['source','coverage','evidence_level','permitted_use','restriction'])
    for name,table in [('TABLE-Q2-R5-001_parameters',parameters),('TABLE-Q2-R5-002_validation',vv),('TABLE-Q2-R5-003_evidence',source),('TABLE-Q2-R5-004_marginal_example',ef.tail(1)),('TABLE-Q2-R5-005_quality_scenarios',qsub)]:
        table.to_csv(TABLE/f'{name}.csv',index=False);write(TABLE/f'{name}.md',md(table))
    report=rf'''# Q2 Round 5：来源分层的广义幂律模型

状态：CHECKED PAPER-READY CANDIDATE；Round 5研究与QA完成，Gate 3待裁决；无ACTIVE FINAL MODEL/VALIDATED FINAL RESULT。完整数值均来自EXP-Q2-ND-R5-20260924-v1和SCEN-Q2-R5-20260924-v3，失败情景v1/v2不引用。

## 1. 问题、来源和建模机制

问题二要求解释参数规模、训练数据、质量及领域配比对Loss的影响，并计算边际、弹性与替代条件。四类因素的识别证据不同：B1给出8条规模轨迹、共1176个检查点；Q1给出A来源内的配比关联；B7为质量变化提供半合成情景。它们缺少经验证的共同验证集、tokenizer及同运行质量锚，不能把所有绝对Loss直接拼接。因而采用“来源内估计＋显式条件情景”的分层关系，保留无法识别的参数为空，而不是强行填入质量系数。

N、D均以十亿为单位。主模型为加性幂律非线性回归：

$$
L_B(N,D)=E+A N^{{-\alpha}}+B D^{{-\beta}}.
$$

这里E是附件量尺下的渐近截距，两个衰减项表达单调改善及边际收益递减；该结构是[Hoffmann等的经典形式](https://arxiv.org/abs/2203.15556)的本题受限应用。文献系数没有直接移入。假设N-D水平上的加性可分离，不预设真实世界不存在交互。模型在8组等权的残差平方损失下，用12初值有界最小二乘估计；E≥0，A/B>0，指数为正，所有边界和求解精度在计算前冻结。只读N、D、val_loss，不使用隔离元数据，不裁去早期点。

## 2. 参数与数值稳定性

{md(parameters)}

参数证据级别为ATTACHMENT-INTERNAL ESTIMATED（CAND-Q2-R5-ND-001）。本次具体关系为

$$
\widehat L_B={E:.8f}+{A:.8f}N^{{-{a:.8f}}}+{Bv:.8f}D^{{-{b:.8f}}}.
$$

12个初值均收敛，最大参数分歧{s['full_fit']['max_start_parameter_spread']:.3g}，Jacobian满秩5、条件数{s['full_fit']['jacobian_condition']:.4f}，没有触及参数界。训练RMSE={s['training']['rmse']:.8f}。图FIG-Q2-R5-001展示拟合和残差。删去D<1、D<10的敏感性以及log D测度加权均保留接近的指数（具体数值见parameter_sensitivity.csv），但不替换预定主拟合。

表中区间由整条轨迹重抽样200次形成，仅衡量给定附件、模型结构和轨迹可交换假设下的数值稳定性；有效组数最少3、最多8，8组本身不等于已证明独立。它不是外部普适指数的置信区间，也没有覆盖来源不确定性、量尺偏差、模型选择或真实运行间波动（CAND-Q2-R5-UNC-001）。拟合结果接近四舍五入后的(E,A,B,alpha,beta)=(1.69,0.354,1.24,0.34,0.28)，该舍入函数RMSE={t['rounded_parameter_diagnostic']['rmse']:.8f}。这是附件高度规则的诊断，不能据此断言找回生成器或原始训练实验。

## 3. 轨迹验证、残差与模型升级判定

不能把同一模型的检查点随机拆分，故采用三类验证。整规模留出为8折；前向验证分别用前73和110个D点，检验后续检查点；双维分块用7个规模的前98个D训练，预测完全未见规模的后49个D。所有切分保持训练和测试行不交叉；双维测试的N与后期D都没有进入训练。均值S0与对数线性Slog作为透明对照。

{md(vv)}

三类S1误差均低于预先设定的宏平均0.05、最坏组0.10并优于均值至少20%的实用容差，支持附件内部预测用途（CAND-Q2-R5-VAL-001；图FIG-Q2-R5-002）。阈值是内部研究标准，不是官方门槛或外部误差保证。最小、最大N的留出属于一侧规模外推；内部N留出属于插值，不能把两者混称同一泛化难度。

各组残差的log D秩相关约-0.168至0.100，最大组残差跨度约0.00153，未达到预注册的稳定结构及幅度触发条件；不增加自由交互项或轨迹偏移以追求训练误差下降。部分残差有弱序列相关，区间按整轨迹重抽样而非逐行独立标准误。模型选择使用这些验证，因此报告不能再称作模型确定后从未使用的最终测试性能。

## 4. 边际效应、弹性与N-D替代

记U=A N^(-alpha)、V=B D^(-beta)，有

$$
\frac{{\partial L}}{{\partial N}}=-\frac{{\alpha U}}{{N}},\quad
\frac{{\partial L}}{{\partial D}}=-\frac{{\beta V}}{{D}},\quad
\varepsilon_N=-\frac{{\alpha U}}{{L}},\quad
\varepsilon_D=-\frac{{\beta V}}{{L}}.
$$

总Loss弹性随状态变化，不能直接以-alpha/-beta代替；以L-E为分母的超额Loss弹性另存marginal_effects.csv（图FIG-Q2-R5-003）。二阶自身偏导为正，故增加N或D的绝对边际改善递减。在单位固定时，N与D的局部等Loss替代条件为

$$
\frac{{dD}}{{dN}}=-\frac{{\alpha U D}}{{\beta V N}},\qquad
\frac{{d\log D}}{{d\log N}}=-\frac{{\alpha U}}{{\beta V}}.
$$

取支持范围内的示例N=1、D=100（不是观测点本身，也不是资源最优），预测Loss={e.loss:.6f}，dL/dN={e.dL_dN:.6f} Loss/十亿参数，dL/dD={e.dL_dD:.8f} Loss/十亿token；总Loss弹性分别为{e.elasticity_N:.6f}、{e.elasticity_D:.6f}，等Loss对数替代率{e.dlogD_dlogN:.6f}。因此在该点附近，N增加1%可局部补偿D约减少1.258%，并非任意大步长都线性成立（CAND-Q2-R5-MARG-001）。

有限变化用反函数计算而不是导数线性外推：N从1降到0.8时，等Loss需要D约135.5586；降到0.5时D约315.8275，已超过B1最大299.893，必须标域外。源内N-D水平交叉偏导为0只是当前加性代理的结构设定；不能由此证明实际训练资源之间不存在互补。

## 5. 分级跨来源检查与大规模外推

{md(source)}

B2的7条半合成轨迹中，族内中心化形状的中位RMSE/零响应比={t['external_summary']['B2']['median_centered_ratio']:.6f}，相关方向很强但幅度误差约0.394–0.398 Loss；大多数D已超过B1支持。不能把约0.855的误差比包装成跨族标尺验证成功。B4/B5分别只有11/8个多行族可计算族内形状，中位误差比为{t['external_summary']['B4']['median_centered_ratio']:.6f}/{t['external_summary']['B5']['median_centered_ratio']:.6f}；原表另有单行族，保留而不伪造相关。B4的Gemma/Qwen2也存在偏序反例。中心化使用了目标组均值，仅是事后形状诊断，不是未校准的新族绝对预测（CAND-Q2-R5-EXT-001）。

B9含132条大模型元数据，N从100到10000B，远超本轮B1最大11.965825B；其中4条D=0只标无效，不填补。B10为128个估算Loss，family实际逐模型命名，不能构造多行“族”来算留族相关；保留逐行曲面值与来源估算的对照供压力讨论，绝不作为验证真值。B1很窄的重抽样带不能成为百亿以上外推保证（CAND-Q2-R5-EXT-002）。

## 6. 质量效应：半合成校准与规模条件

B6是B7的精确子集，只保留450个唯一N-D-Q点作为同一生成体系分析。固定每个N-D单元中心化Q与Loss，45个单元斜率均为负，范围[{t['quality_cell_slope_range'][0]:.6f},{t['quality_cell_slope_range'][1]:.6f}]，共同斜率为-{t['quality_common_g']:.6f}。这是SEMI-SYNTHETIC CALIBRATED系数，生成器和真实Q含义没有恢复，不是EMPIRICALLY ESTIMATED真实质量弹性（CAND-Q2-R5-QUAL-001）。

预注册的规模调节诊断为单元截距加s(N,D)Q，其中

$$
s(N,D)=-0.370147+0.059516\log N+0.015761\log(D/100).
$$

按9个N层留一的中心化RMSE从{t['quality_centered_LOO_macro_RMSE']['Qcommon']:.6f}降为{t['quality_centered_LOO_macro_RMSE']['Qscale']:.6f}，约改善17.53%，但并非每个N层都改善。测试单元自己的均值用于消去截距，因此此检验只支持生成表内质量响应形状的规模依赖，不能作为新单元绝对Loss预测，更不能跨来源自动套入B1。图FIG-Q2-R5-004上部给出单元斜率。

为明确回答“质量如何替代规模”，在独立情景层假设B7的一单位Loss变化量可按外生倍数lambda转入B1：

$$
L_s=L_B-g_s(Q-Q_0)+h_s(N,p),\qquad g_s=\lambda\,0.361995,\quad\lambda\in\{{0,0.5,1,1.5\}}.
$$

默认可识别B1模型取g_s=0，TYPE E仍为0。Q0=.5、ΔQ=.1只是B7刻度上的情景，不是DQ0提升0.1。固定g、p时

$$
\frac{{d\log N}}{{dQ}}=-\frac{{g_s}}{{\alpha U}},\quad
\frac{{d\log D}}{{dQ}}=-\frac{{g_s}}{{\beta V}},\quad
N_{{new}}=\left(\frac{{A}}{{U+g_s\Delta Q}}\right)^{{1/\alpha}}.
$$

在N=1,D=100示例，lambda=1给出等Loss的N减少24.903%、或D减少30.210%；lambda=0时二者均为0，lambda=1.5时约34.280%/40.951%。这些是条件替代量，不是质量投入的已验证节省，更未包含筛选成本和数据供应（SCEN-Q2-R5-SUB-001）。若g依赖N/D，求导必须加入其偏导，本轮示例只用常数g。

另一机制假设有效数据D_eff=D(Q/Q0)^rho，纯情景rho为0/.5/1；若仅在示例点匹配上述共同斜率，可得rho={t['effective_data_rho_local_calibration']:.6f}。局部斜率相同但有限替代不同：匹配rho的模型给N减少22.153%、D减少29.175%。rho=1则约12.890%/16.667%。机制与运输假设的不确定性显著大于附件内窄参数带，因此不应只报告单一质量替代数字。

## 7. 领域配比、规模依赖与替代/互补边界

Q1冻结M1给出的13域预测为均值加Helmert对比系数。令17×16基为H，16×13系数为C，则来源A内沿simplex方向v（sum v=0）的变化为v^T H C；把域j的1个百分点转给域i，对第k个响应的影响是0.01[(HC)_ik-(HC)_jk]。它是总量不变的关联变化，不是同时增加所有域。136个成对方向和全部13域变化保存于mixture_tangent_scenarios.csv，并标支持待核；没有选择“最优配方”、没有执行Q3。

相同方向可令一些域改善、另一些域恶化，所以R0平均变化不能替代R3逐域。M1在线性代理内部二阶配比互补项为0；这不能作为现实领域互补不存在的证据。配比弹性还需要选定参考p与切向方向，零配比处普通对数弹性未定义，因此不输出伪通用的17个独立弹性。

沿用既有有效验证而不重新计算：1M R0 RMSE=0.2278且13/13域改善，60M中心化误差比约0.888，1B约3.108且失败；A6/A8为相同配比。h_s(N,p)=k_s(N)乘A源中心化响应仅可作为假设，k_s包含未估计的量尺转换且默认0。常数k是规模不变的对照假设，不能把1B失败“修复”为已知衰减函数。Q1观测凸包仅覆盖1M验证2/256，p支持与现实供应约束必须另行处理（CAND-Q2-R5-MIX-001）。

## 8. 结论边界与下一问接口

本轮完成了附件内N-D关系、轨迹验证、参数稳定性、分级来源检验、边际与替代推导、半合成质量校准以及配比情景接口。Q2可写的结论是来源分层关系成立于各自限定用途，不能写成已识别的通用L(N,D,Q,p)。Q3在Gate3批准后可用B1受限曲面和参数集合开展支持范围内条件优化；质量与配比机制必须保留情景标签和默认零运输分支。外部普适预测、独立质量弹性、成本收益、最终可行配比和能力分数转换均未被本轮建立。

四张图和五张表均为本轮CHECKED候选，正式论文使用仍需Gate3及最终版式复核。题目要求覆盖见Q2_COVERAGE_MATRIX_v1.md；具体机器接口见Q2_TO_Q3_INTERFACE_v1.json。Q3/Q4未启动。
'''
    # Raw f-string preserves literal LaTeX commands.
    write(MODEL/'Q2_RESULTS_REPORT_v1.md',report)
    write(PAPER/'Q2_ROUND5_PAPER_CANDIDATE_v1.md',report)
    limits='''# Q2 limitations v1

1. B1外部val_loss原始run、语料、tokenizer、抽取锚未恢复；所有N-D系数只限附件内部Loss标尺。精确幂律吻合与圆整参数诊断不证明生成机制。
2. 仅8条N轨迹，不能把1176行当独立样本。200次整轨迹bootstrap只覆盖给定曲面与交换性假设，非真实运行间误差、来源误差、选择后区间或域外预测保证。
3. 留出误差参与了已冻结候选的用途判定；没有额外的完全未使用最终测试集。实用误差阈值由研究者制定，不是官方标准。
4. 参数支持N∈[0.070542,11.965825]B、D∈[0.134,299.893]B。矩形范围表示可考虑插值，不等于矩形内每点都经过独立检验；Q3现实供给、预算和成本未建。
5. B2半合成、B3插值、B10估算均非独立真值。B4/B5共同Loss量尺未证明，组均值中心化诊断使用目标响应均值，不是绝对预测校准成功。
6. B6⊂B7，只有450个唯一生成点，不能合计810。生成器未知，表内斜率、规模调节、rho局部校准均非真实质量效应；TYPE E=0，DQ0与Q_score没有映射。
7. Q变化的B1损失增量、有效D机制及A→B的p运输系数为SCENARIO-CONDITIONAL，默认零。不能把情景资源减少比例写成可实现节省或因果效果。
8. Q1配比只在1M有相应验证；60M部分形状转移、1B失败不变。线性M1不识别真实互补；零配比处对数弹性未定义；simplex切向候选未核经验支持，不能优化。
9. B8仍隔离且未读取；B9四条D=0不做幂律预测。百亿以上外推与窄参数区间不能互相担保。
10. 无独立Opus或外部审稿，本轮是Lead研究者执行及程序化/视觉复核。Gate3待裁决，ACTIVE FINAL MODEL与VALIDATED FINAL RESULT仍无。论文候选未做最终模板编译，图在最终嵌入尺寸仍须复核。
'''
    write(MODEL/'Q2_LIMITATIONS_v1.md',limits)
    iface=dict(status='CHECKED CANDIDATE — GATE3 PENDING',version=1,model_id='Q2-S1-R5-v1',
        evidence_level='ATTACHMENT-INTERNAL ESTIMATED',equation='E+A*N_B**(-alpha)+B*D_B**(-beta)',parameters=p,
        units={'N':'billion parameters','D':'billion tokens','Loss':'B1 attachment scale'},
        support={'N_B':[.070542,11.965825],'D_B':[.134,299.893],'interpolation_not_guarantee':True},
        uncertainty={'ensemble':'06_results/raw/EXP-Q2-ND-R5-20260924-v1/cluster_bootstrap.csv','coverage':'conditional numeric only; no calibrated external prediction interval'},
        derivatives='06_results/raw/EXP-Q2-ND-R5-20260924-v1/marginal_effects.csv',
        quality={'identified_coefficients':0,'default_g':0,'scenario_common_g':t['quality_common_g'],'scenario_factors':[0,.5,1,1.5],'requires_explicit_transport_assumption':True},
        mixture={'default_AB_transport':0,'1B_transport':'FORBIDDEN_WITH_CURRENT_M1','R3_required':True,'feasible_region':'DEFERRED_SUPPORT_AND_REAL_SUPPLY'},
        B8='QUARANTINED',requirements_before_Q3=['Gate3 decision','actual costs/supply constraints','support-aware p domain','scenario labels','dimensionally consistent cost formulas'],
        Q3_started=False,source_runs=[s['run_id'],t['run_id']],active_final=False)
    write(MODEL/'Q2_TO_Q3_INTERFACE_v1.json',json.dumps(iface,ensure_ascii=False,indent=2))
    write(ROOT/'02_analysis/consensus/Q2_TO_Q3_INTERFACE_v1.md','''# Q2 → Q3 interface v1

状态：CHECKED CANDIDATE / GATE3 PENDING，非新Gate共识。依据R5-SPEC-001和Round5真实结果。

主接口：`03_models/modeling_phase2/round5/Q2_TO_Q3_INTERFACE_v1.json`。

可携带：B1附件内部S1参数、源内N-D矩形支持、三类轨迹验证、全部导数、整轨迹参数集合。只有Gate3裁决后才能在Q3作为受限条件目标使用。区间不是外部预测误差保证。

需场景开关：质量增量g、有效D指数rho与A/B配比运输k均未真实识别，默认0；备选值只做条件机制压力测试。不得把B7刻度直接替代DQ0，也不得把1B失败的M1当作可迁移效应。R3领域异质性、p经验支持、实际供给成本必须分开。

不传：B8主参数、真实独立质量弹性、跨族统一绝对Loss、现实可部署最优、预算配置、KKT解或Q4能力桥接。本轮Q3/Q4未启动。
''')
    write(VALID/'Q2_VALIDATION_REPORT_v1.md',f'''# Q2 validation report v1

Numerical QA: {q['status']}，{len(q['checks'])}项。建议CHECKED / ATTACHMENT-INTERNAL RESTRICTED CANDIDATE；Gate3待审，不晋升最终结果。

{md(vv)}

证据：18个切分、96条按模型/轨迹指标、逐行预测、fold参数、splits.json；独立QA重算全部RMSE并核N与D隔离，差值小于1e-12。数学检查涵盖有限差分、弹性定义、N-D和质量替代反函数回代、哈希、原件不变和失败隔离。原始8条规模轨迹未随机拆行。

参数多初值、Jacobian、200次整轨迹重抽样、晚期截断/logD权重均已完成。升级触发False，不新增正式候选。B2/B4/B5为来源中心化形状诊断，B7为生成表内中心化Q检验，均不升级为跨来源外部验证。B10无多行族，分组指标记null，不以NaN或0冒充成功。

失败隔离：SCEN v1 numpy.bool序列化，v2无多行B10族导致空中位数；有效v3保留原公式/输入/规则。输入冻结v1/v2因B9四个D零值被正值门槛拦截，元数据保留并加无效标签，不影响B1。无对Q1重新训练或验证。

完整限制见03_models/modeling_phase2/round5/Q2_LIMITATIONS_v1.md。图表4张候选单图已检，最终论文嵌入/完整模板尚未执行。
''')
    coverage=pd.DataFrame([
        ['N如何影响Loss','负边际、递减收益、状态依赖弹性','CAND-Q2-R5-MARG-001','附件内'],
        ['D如何影响Loss','负边际、递减收益、N-D替代','CAND-Q2-R5-MARG-001','附件内'],
        ['quality如何影响','B7条件负斜率+两种质量情景机制','CAND-Q2-R5-QUAL-001','半合成/情景'],
        ['mixture如何影响','冻结M1切向变化+R3并行','CAND-Q2-R5-MIX-001','A源1M有限支持'],
        ['规模依赖','B7 Qscale诊断+1B p转移失败','CAND-Q2-R5-QUAL-001 / MIX-001','非通用交互律'],
        ['N/D/Q替代','解析导数、有限反函数、机制敏感性','SCEN-Q2-R5-SUB-001','g=0默认，其他显式假设'],
        ['边际及弹性','1176网格+1示例点','CAND-Q2-R5-MARG-001','总Loss/超额Loss分开'],
        ['参数证据级别','五参数附件估计；Q表内半合成；运输未识别','TABLE-Q2-R5-003','TYPE E=0'],
        ['验证及不确定性','LONO/forward/2D+200整轨迹+跨来源诊断','VAL-001 / UNC-001 / EXT-001','无外部概率保证'],
        ['Q3可用内容','机器接口/来源/支持/成本待定','Q2_TO_Q3_INTERFACE_v1','待Gate3，未做Q3']
    ],columns=['task','answer','evidence','boundary'])
    write(MODEL/'Q2_COVERAGE_MATRIX_v1.md','# Q2 coverage\n\n'+md(coverage))
    print('Built report, 5 tables, validation, limitations, coverage and machine interface.')
if __name__=='__main__':main()
