from common import *
import platform
def append_once(path,marker,body):
    s=path.read_text('utf-8') if path.exists() else ''
    if marker not in s:write(path,s+'\n\n'+marker+'\n\n'+body)
def main():
    summary=json.loads((OUT/'forecast_summary.json').read_text('utf-8'));a=json.loads((AUD/'Q4_DATA_AUDIT_METRICS_v1.json').read_text('utf-8'));b=json.loads((OUT/'bridge_summary.json').read_text('utf-8'));f=pd.read_csv(OUT/'frontier_family.csv');pred=pd.read_csv(OUT/'forecast_12m_24m.csv');base=pred[pred.scenario=='BASELINE'];dc=pd.read_csv(OUT/'decomposition_changes.csv');rv=pd.read_csv(OUT/'robustness_variants.csv');va=pd.read_csv(OUT/'rolling_metrics.csv');figs=json.loads((ROOT/'06_results/figures/round7/figure_manifest.json').read_text('utf-8'))
    report=f'''# Q4 结果报告 / 论文候选 v1

状态：ACTIVE，受限解释的 Q4 模型包；最终 QA 见 07_validation/round7/Q4_VALIDATION_REPORT_v1.md。所有数字来自 EXP-Q4-R7-20260925-v1，原始机器输出目录 06_results/raw/EXP-Q4-R7-20260925-v1。以下为可进入正文的候选内容，尚未做完整论文排版。

## 1 研究对象与证据范围

问题四要求区分规模扩张与非规模性能提升，并预测算力增长放缓背景下的开源模型能力前沿。现有附件支持“参数规模关联—剩余性能分量”的描述性分解，但不足以识别完整 N–D 规模贡献或因果技术进步比例，也不足以验证真实算力放缓的远期效应。我们把这些不可识别部分作为结论保留，不以情景补成观测。

C1 共4576行；规范化完整模型ID后有81个重复ID、162行身份不唯一，整组排除。C2只提供辅助发布日期，核心分数与C1的差异为浮点末位，不能重复计样本。C3共4599行，其中26条更早历史记录为异口径混合，23条均分与六维均值相差超过1分；不与同口径榜单拼接拟合。C4的算力、训练数据、开放权重字段进入元数据匹配及年度宏观审计；96条名称和参数一致的辅助匹配不等于运行身份完全一致。训练阶段和单位继续单独标记。

C8全部1958个JSON逐文件核SHA并解析；4个截断文件保留而跳过。按目录取最新可解析记录，共1860个目录、1854个六维完整目录；另保存BBH逐任务聚合，满足必用逐任务分析。C9与C1核心字段等价，用于可下载状态和flagged筛选，不作为额外样本。C10为说明，C7为架构上限元数据，均不替代逐任务评测或实际训练token。

主样本采用已报告许可证且Hub可用、未标记异常、六维完整、C1/C8完整ID相同且参数量差异≤2%的模型，共853条，评测日期2024-06-16至2025-03-14。含92个base、539个chat/finetuned、221个merge及1个其他类型，回归显式控制类型。许可证口径为“开放权重研究可用代理”，含有限制许可证，并非完整开源认证；严格许可证另做敏感性。家族仅依模型名称保守识别，246条未知，不推断合并模型血缘。

主时间轴为C8评测文件日期；提交日期和C2发布日期不相互填补。数据是保留最新版本的回溯样本，不是完整历史排行榜快照，因此滚动验证仅称pseudo-out-of-sample；历史许可证可用性与幸存者偏差仍在。

## 2 综合能力与前沿

令六维原始任务组得分为b_ik，定义 y_i=(1/6)Σ_k b_ik，范围0–100。IFEval使用prompt-strict与instruction-strict的平均；BBH、GPQA、MUSR用组acc_norm，MATH用exact_match，MMLU-PRO用acc。此指标与C1归一化Average不同，桥接图另标量尺。

在周末t，取评测日期位于(t−28天,t]的模型，数量至少15时定义 F_t=Q_0.90(y_i)。采用线性插值分位数，末次评测日另保留终点。该前沿是高表现评测群体的稳健代表，允许因样本组成改变而下降；并非历史最高分。由{f.F.iloc[0]:.4f}升至{f.F.iloc[-1]:.4f}，端点增量{f.F.iloc[-1]-f.F.iloc[0]:.4f}分（Q4-R7-001）。首窗仅16条，起点选择是重要敏感项。六个任务的前沿端点均提高，但幅度不一致，MATH提升最显著。

## 3 Loss–Benchmark桥接检验

C6为主、C5为嵌套对照，75条不与43条重复相加。只有7条Pythia被附件标为High；其Loss与B1末检查点逐项一致，但仍缺外部验证语料、tokenizer及配对时点锚。与C1比，5条小规模模型的参数记载差异超过2%，不把同名当成同量尺同版本。

在High单族中，Spearman(−Loss,LB_Average)={b['high_rank_rho']:.4f}；留一尺度RMSE分别为线性0.5528、单调插值0.4366、均值基准0.4244，端部规模留出也未全面过关（Q4-R7-003）。单一高可比家族不支持leave-one-family-out；没有成对日期，不支持桥接的时间留出。中可比的Gemma/Qwen等仅展示族内诊断，来源损失并未统一，不能用较高相关提升为Strong。

最终 **NO RELIABLE BRIDGE**，采用B0禁止数量运输。全部7个高可比ID能找到C8，但同时满足冻结C1规模一致性的只有2条，不能建立主分析raw6量尺的合格桥接。故Q2/Q3预测Loss保留原附件单位，不能换算为本节benchmark预测；这是桥接误差对结论的直接影响。

## 4 参数规模与剩余性能分解

建立 y_i=a+β lnN_i+γt_i+类型固定效应+家族固定效应+ε_i，并比较仅N与不控制家族的回归。主样本仅9条记录含D且含后训练/估计量，无法可靠估计全样本f(N,D)。不插补D，不使用C7的TB代替tokens。因此β仅为参数规模关联，残差仍可能包含数据规模扩张。

对F_t所用的两个排序邻点采用同一分位数插值权重，令S_t=β·插值(lnN)，R_t=F_t−S_t，可得严格恒等式 ΔF=ΔS+ΔR。主β={dc.loc[dc.model=='family','beta_logN'].iloc[0]:.6f}分/lnN；端点ΔS=2.70325分、ΔR=13.17640分，对应17.0233%与82.9767%（Q4-R7-002）。这些是**指定样本、时间窗和模型下的描述性比例**，不是完整规模与真实技术的份额。

三种控制规格的参数端点份额为17.78%、16.71%、17.02%；但只保留已知家族、严格许可证、较晚起点或56天窗口时份额可变负。家族bootstrap只对系数抽样、固定端点的95%条件份额区间为[{summary['cluster_bootstrap_parameter_share95'][0]*100:.2f}%,{summary['cluster_bootstrap_parameter_share95'][1]*100:.2f}%]，不覆盖改变前沿或缺失D的不确定性。不能用这条较窄区间反驳敏感性失败。

pooled时间关联为5.14488分/年，控制家族后为4.57404；同家族中Gemma/Yi为负，Llama/Qwen等为正（Q4-R7-006）。因此“统一稳定的技术进步率”也不成立。R_t只是technical-progress proxy，包含未观测D、对齐与微调、家族组成、评测噪声和选择。

## 5 动态模型、验证与结构变化

比较持续性、线性截断、有界logit线性和最近13周局部logit。最少16个周端点后滚动预测4/13/26/52周；实际仅支持4周20折、13周11折。按期限等权MAE选中logit：4周MAE=1.7566、13周MAE=1.5293；持续性为1.9957、3.6833（Q4-R7-004）。26/52周无可用验证，不能写已验证6/12个月，更不能据此宣称24个月覆盖。

模型为 logit(F_t/100)=a+bt+e_t，反变换保证0–100边界。固定历史中点分段斜率AIC=47.50，一条趋势AIC=45.61，未获得升级分段模型的证据；短序列检验力有限。2025年2月一周有204条评测，剔除该月后的预测变动另报。重叠窗口和折次不独立，模型选择使用了这些验证，未另有未使用最终测试集。

## 6 日期明确的条件预测与三类不确定性

运行日/forecast origin=2026-09-25（北京时间）；最后数据=2025-03-14，中间相隔560天。因此下表实际从最后评测外推约30/42个月，均标 **EXTRAPOLATION-DOMINATED**，不是以最新产业状态为条件的预测。

{mdtable(base[['target','central','lower95_conditional','upper95_conditional']])}

上述95%区间来自1000次固定种子的4周循环残差块重抽样并重新拟合，再按SD·sqrt(1+h/4)假设加入未来扰动。这是给定平稳误差/扩散规则的条件模型预测区间；扩散律并没有长时段数据校准，不能标作经验覆盖保证（Q4-R7-005）。模型不确定性独立报告：2027年中心预测范围52.17–83.77，2028年52.33–97.11（Q4-R7-007）。统计区间与模型范围互不替代。

情景只对参数规模部分使用历史正增长的保留比例0、0.5、1，分别为CONSERVATIVE、BASELINE、ACCELERATED。全时段S_t拟合斜率为−0.029739分/周，因此A(h)=max(0,b_S h)=0，三条情景重合（Q4-R7-008）。端点ΔS为正并不意味着全时段趋势为正。这种重合只说明本样本无法给出有效的正规模趋势放缓对照，绝不是“算力放缓不影响能力”的证据。

R_t历史趋势为0.284911分/周；未来分解使用选中模型总预测减去假设的参数分量，不将R趋势重复相加。未来剩余分量依旧含遗漏规模，不能宣称由因果技术贡献。完整compute-slowdown效应及其情景区间 **NOT IDENTIFIED**。未量化的结构不确定性还包括新家族、评测污染/改版、训练D及任务相关性；没有概率保证排除逻辑范围0–100内的其他未来。

## 7 Q1–Q3递进接口与论文使用规则

Q1质量画像、局部配比证据和Q2来源内标度律通过Gate4冻结接口保留。Q3的51个预算条件N/D/Loss路径提供资源配置机制示例，三代表点来自既有模型而非C历史。主情景quality/mix OFF，高预算支持cap造成的平台不代表实际产业前沿饱和。没有可靠桥接时，Q3只能解释“何种资源改变可能降低来源内Loss”，不能代替C评测或校准benchmark趋势。

论文应把“同口径历史前沿上升、桥接未通过、分解比例不稳定、远期仅条件外推”作为联合结论。17%/83%必须与N-only和敏感性限制同段出现，不宜进入摘要作为普适贡献比例。未来两点必须连同原点日期、560天空档、统计假设和模型范围一起引用。不得把本模型结果改称现实技术因果效果、官方未来榜单或已验证的产业算力放缓预测。
'''
    write(SPEC/'Q4_RESULTS_REPORT_v1.md',report)
    paper=ROOT/'08_paper/sections/Q4_ROUND7_PAPER_CANDIDATE_v1.md';write(paper,report)
    write(SPEC/'Q4_LIMITATIONS_v1.md','''# Q4 limitations v1

1. Full N–D scale/non-scale shares and actual compute-slowdown effect are NOT IDENTIFIED. Nine D entries include estimates/post-training; no imputation or stage mixing. The 17/83 split is parameter association/residual under one definition and reverses under several sensitivities.
2. No reliable Loss–Benchmark bridge. One high family, failed rank/scale tests, five C1 parameter discrepancies, missing paired loss/evaluation timestamps, inherited B1 provenance alert. All seven C8 name overlaps are not seven fully eligible bridge pairs.
3. Only June2024–March2025 comparable evaluation history; 560-day gap before run date. Requested targets extrapolate about30/42 months beyond data. No 26/52-week backtest and no empirical long-horizon coverage. Both targets extrapolation-dominated.
4. Frontier is 28-day q90 of a selected C8 raw6 evaluation cohort, not ecosystem all-time record, release-date frontier or normalized C1 Average. Four corrupted C8 files, 81 duplicate C1 IDs and incomplete/unlicensed/mismatched cases excluded. Latest snapshot/revision survival and metadata availability not reconstructible historically.
5. Name-derived family labels miss ancestry of merges and unknown models. Type/family composition changes; base-only and post-trained targets differ. Family control is association, not causal adjustment.
6. High quantile from16 initial records is unstable; timing/window/filter changes alter shares. Quantile-of-score representatives need not be quantile-of-N. Endpoints and fitted trends differ.
7. Four-week overlapping windows/folds are dependent. Bootstrap assumes stationary residuals and a researcher-specified diffusion law; model selection and missing D/source uncertainty excluded. No universal CI, and bounded link saturation is imposed.
8. Scenario 0/.5/1 retained positive parameter expansion collapses under negative S trend. This cannot demonstrate robustness to real compute slowdown; scenarios have no assigned probabilities. Future residual includes omitted scale.
9. C3 historical metrics are not homogeneous with the six-task composite. C4 compute/data are sometimes estimated, and auxiliary name matching does not identify a pretraining run. C7 maximum context/TB cannot substitute for actual context/tokens.
10. Q3 paths remain conditional mechanism inputs with source-internal Loss; no universal quality/mix transfer, B8, 1B failed transport, economic-cost interpretation or support-cap saturation claim.
11. Single-agent researcher execution and programmatic/visual audit; no external Opus/independent reviewer claim. Paper package is qualified and provisional, not final contest submission.
''')
    table_dir=ROOT/'06_results/tables/round7';table_dir.mkdir(parents=True,exist_ok=True)
    tables={'TABLE-Q4-R7-001':pd.DataFrame([{k:v for k,v in a.items() if isinstance(v,(int,float,str,bool))}]).T.reset_index().rename(columns={'index':'metric',0:'value'}),'TABLE-Q4-R7-002':pd.read_csv(OUT/'bridge_validation.csv'),'TABLE-Q4-R7-003':dc,'TABLE-Q4-R7-004':va,'TABLE-Q4-R7-005':base,'TABLE-Q4-R7-006':rv,'TABLE-Q4-R7-007':pd.read_csv(OUT/'benchmark_robustness.csv')}
    for name,t in tables.items():t.to_csv(table_dir/(name+'.csv'),index=False);write(table_dir/(name+'.md'),mdtable(t))
    write(SPEC/'Q4_FIGURE_PLAN_v1.md','# Q4 figure plan and completed manifest\n\nEight PNG/SVG figures generated by round7_figures.py; sources/hashes/results in 06_results/figures/round7/figure_manifest.json.\n\n'+mdtable(pd.DataFrame([{'figure':x['id'],'claim':x['claim'],'result':x['result_id']} for x in figs])) )
    write(SPEC/'Q4_TABLE_PLAN_v1.md','# Q4 completed tables\n\n'+mdtable(pd.DataFrame([{'table':k,'rows':len(v),'source':'EXP-Q4-R7-20260925-v1 or Q4 data audit','location':'06_results/tables/round7/'+k+'.csv'} for k,v in tables.items()])))
    write(SPEC/'Q4_TO_PAPER_INTERFACE_v1.md','''# Q4 to paper interface v1

ACTIVE / Round8 integration only after final QA. Candidate section: 08_paper/sections/Q4_ROUND7_PAPER_CANDIDATE_v1.md. All results Q4-R7-001…008 are VALIDATED FOR RESTRICTED REPORTING only when QA passes; no upgrade to causal truth or long-horizon coverage.

Use Q4-R7-001 for observed raw6 q90 history;002 parameter/residual descriptive identity;003 rejected bridge;004 short rolling validation;005 conditional run-date forecasts/statistical PI;006 family/time/screening instability;007 model spread;008 collapsed parameter-scale scenarios. Figure/table manifests identify machine outputs and code. Labels: observed=C8 group scores; estimated=regression/frontiers; scenario=long-horizon forecasts and Q3 resource paths. Raw6 versus normalized C1/C6 score must always remain separate.

Required language: NO RELIABLE BRIDGE; full N–D/non-scale and actual compute-slowdown effects NOT IDENTIFIED; endpoint split not robust; EXTRAPOLATION-DOMINATED at both run-date targets; conditional diffusion PI with no long-horizon coverage validation. Do not place 83% in abstract as technical contribution; do not omit 560-day gap or model range. Use eight figures selectively; no full-paper layout in Round7. Q1–Q3 remain frozen and their source-specific limitations remain active.
''')
    claims=[('001','Observed raw6 q90 36.453073 →52.332722','frontier_family.csv','CHECKED/VALIDATED restricted observation'),('002','Parameter share17.0233%; residual82.9767%; full ND NOT IDENTIFIED','decomposition_changes.csv','VALIDATED arithmetic, unstable descriptive scope'),('003','NO RELIABLE BRIDGE; rho0.60714; failed held-out criteria','bridge_summary.json','VALIDATED rejection'),('004','Logit short rolling MAE1.756586/1.529283 at4/13weeks','rolling_metrics.csv','VALIDATED retrospective selection'),('005','2027/2028 conditional79.75536/87.12751 with separate PI','forecast_summary.json','VALIDATED computation; extrapolation-dominated'),('006','Family/time/filter contribution instability; six tasks improve','robustness_variants.csv','VALIDATED diagnostics'),('007','Model ranges52.16860–83.77111 /52.33272–97.11295','forecast_all_models_scenarios.csv','VALIDATED model envelope; not CI'),('008','Scale scenarios collapse A(h)=0; full compute effect unknown','scenario_decomposition.csv','VALIDATED conditional scenario')]
    append_once(ROOT/'06_results/RESULTS_REGISTRY.md','## Round7 restricted result register',mdtable(pd.DataFrame([{'ID':'Q4-R7-'+i,'result':claim,'source_run':'EXP-Q4-R7-20260925-v1','source_file':'06_results/raw/EXP-Q4-R7-20260925-v1/'+src,'evidence':status,'validation':'07_validation/round7/Q4_VALIDATION_REPORT_v1.md','paper':'Q4 section '+str(int(i))} for i,claim,src,status in claims])))
    append_once(ROOT/'06_results/FIGURE_REGISTRY.md','## Round7 completed figures',mdtable(pd.DataFrame([{'ID':r['id'],'result':r['result_id'],'claim':r['claim'],'sources':','.join(r['sources']),'code':r['generator'],'files':';'.join(r['files'])} for r in figs])))
    append_once(ROOT/'05_experiments/EXPERIMENT_REGISTRY.md','## Round7 completed execution','EXP-Q4-R7-20260925-v1 COMPLETED: bridge/decomposition/rolling/forecast/robustness; Python '+platform.python_version()+'; seed20260925;400 family-cluster coefficient replicates,1000 forecast blocks,200 rolling blocks. Frozen Q4_R7_FROZEN_v1.json; INPUT_MANIFEST; code/output hashes in ROUND7_REPRODUCIBILITY_MANIFEST_v1.json. Numerical outputs unchanged by document fixes. Audit/read-only recomputation QA-Q4-R7-20260925-v1 separate from model run. See QA verdict for reporting scope.')
    append_once(ROOT/'10_review/ISSUE_TRACKER.md','## Round7 QA defects and retained limitations','''New defects P0=0 / P1=0 / P2=3, all CLOSED after final QA:

| ID | Severity | Finding | Resolution |
|---|---|---|---|
| R7-PKG-01 | P2 | Optional markdown formatter unavailable and report apostrophe syntax | Deterministic local formatter and corrected literal; numerical outputs unaffected |
| R7-DOC-01 | P2 | Seven raw6 name overlaps incorrectly described as insufficient without eligibility distinction | Seven name overlaps but two pass frozen triple-source scale criterion; no model/bridge verdict changed |
| R7-VIS-01 | P2 | Dense date ticks; absolute S/R bars risk interpretation as identified absolute contributions | Sparse dates and scenario increments from last frontier; visual review repeated |

Retained scientific scope limitations, NOT declared resolved: R7-LIM-01 missing same-stage D prevents full N–D/non-scale and compute-slowdown identification;R7-LIM-02 560-day data gap and no long-horizon coverage;R7-LIM-03 decomposition/filter/family instability;R7-LIM-04 no reliable bridge. These are explicit negative/inconclusive research results, not hidden successful tests. Existing DA-02/05/07/10 and Q1–Q3 provenance/transfer limits remain. DA-04 C8 four damaged files handled/excluded, source damage itself unresolved. No new P0 reopening Q1–Q3.
''')
    # Registry tops are active status, old detailed history retained.
    for rel in ['05_experiments/EXPERIMENT_REGISTRY.md','06_results/RESULTS_REGISTRY.md','06_results/FIGURE_REGISTRY.md']:
        p=ROOT/rel;s=p.read_text('utf-8');marker='> CURRENT ROUND7:'
        if marker not in s:s=s.replace('\n','\n\n> CURRENT ROUND7: Q4 package completed; qualified results only, final QA linked below. Earlier Gate/Round status paragraphs are historical. No unrestricted FINAL-model promotion.\n',1);write(p,s)
    append_once(ROOT/'04_code/ENTRYPOINT.md','## Round7 reproducibility','Read frozen specs/config first. Source attachments restored by RAW_SHA256 manifest. Python dependencies numpy,pandas,scipy,matplotlib,pymupdf,pyarrow. Run round7_mapping.py, round7_audit.py to reproduce audit; do not rerun round7_freeze.py on an existing frozen experiment. Numeric entries round7_models.py then round7_forecast.py; they reproduce the fixed run in an isolated checkout. Reports/figures/package then round7_qa.py. No network or Q1–Q3 re-fitting required. Use new experiment ID for changed assumptions/data; never overwrite established evidence as a new run.')
    print('Paper candidate, reports, 7 tables and registries written')
if __name__=='__main__':main()
