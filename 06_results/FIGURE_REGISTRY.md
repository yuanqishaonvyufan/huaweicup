# FIGURE_REGISTRY

> 二稿图4—7仅按既有机器表重新导出打印版式，未修改数值：`FIG4_Q2_TOTAL_LOSS_ELASTICITY_REEXPORT`、`FIG5_Q3_BUDGET_REEXPORT`、`FIG6_Q3_QUALITY_REEXPORT`、`FIG7_Q3_UNCERTAINTY_REEXPORT`，图源和SHA256见 `08_paper/revised_v2/figures/REEXPORT_MANIFEST_v1.json`。原图及原结果保留。图4图注现在仅描述N/D总Loss弹性热图，有限替代由公式和正文示例承担。

> CURRENT ROUND7: Q4 package completed; qualified results only, final QA linked below. Earlier Gate/Round status paragraphs are historical. No unrestricted FINAL-model promotion.

**当前 Gate3：G3-SINGLE-001 / Verdict A — PASS。Q2 PROVISIONALLY CLOSED；Q3 AUTHORIZED TO START / NOT EXECUTED。既有 Run/数值/图与证据等级不变，无新模型运行；下方 Gate3 待审文字保留形成时状态。FINAL 仍为0。**

当前：Q1四图 + Q2四图为CHECKED候选；Round5单图QA通过，最终正文嵌入待审。

Round 4 有四张已生成并核来源哈希的 Q1 候选图；Gate 2 已接受其受限 Q1 证据用途，仍保留论文候选状态。PDF 向量文件与 PNG 预览、脚本哈希见 `03_models/modeling_phase1/q1/round4/figures/figure_manifest.json`。正式嵌入仍须按论文版面检查中文字形和实际尺寸。

| Figure ID | Question | Purpose / claim | Source Run | Source data | Result ID | Generation script | Filename | Axes / unit | Limitation | Paper location | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FIG-Q1-R4-001 | Q1 | 比较五核心描述坐标的域差与扩展对照 | AUDIT-Q1-QUALITY-CLOSURE-R4-20260924-v1 | `Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv` | CAND-Q1-R4-QUAL-001 | `04_code/modeling_phase1/round4_q1_figures.py` | `figures/FIG-Q1-R4-001_core_domain_profile.pdf`；同名 PNG | 横轴五核心语义；纵轴来源域和 n；颜色为 A1 参考平均分位，0–1 | 同标注体系对照，不是独立质量干预；DQ0 非真 Q | 正文候选 | CHECKED PAPER CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE |
| FIG-Q1-R4-002 | Q1 | 显示 A7/1M M1 对 M0 的 13 域 RMSE 比，检查是否有域恶化 | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | `P_RESPONSE_DOMAIN_VALIDATION_v2.csv` | CAND-Q1-R4-VAL-001；CAND-Q1-R4-VAL-002 | `04_code/modeling_phase1/round4_q1_figures.py` | `figures/FIG-Q1-R4-002_domain_validation_gain.pdf`；同名 PNG | 横轴 M1/M0 RMSE 无量纲比；纵轴 13 域；1 为无改善 | 仅 1M 同尺度，主要 near-support；非因果效应 | 正文候选 | CHECKED PAPER CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE |
| FIG-Q1-R4-003 | Q1 | 对照 1M/60M/1B 的中心化误差比，突出 1B 迁移失败 | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | `P_RESPONSE_VALIDATION_METRICS_v2.csv` | CAND-Q1-R4-TRANSFER-001 | `04_code/modeling_phase1/round4_q1_figures.py` | `figures/FIG-Q1-R4-003_scale_transfer_failure.pdf`；同名 PNG | 横轴规模与 n；纵轴 M1/M0 中心化 RMSE 比，无量纲 | 跨规模只检相对配比形状，不代表绝对 Loss 预测 | 正文候选 | CHECKED PAPER CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE |
| FIG-Q1-R4-004 | Q1 | 显示经验凸包和训练近邻的验证配比分层 | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | `P_SUPPORT_VALIDATION_ROWS_v2.csv` | CAND-Q1-R4-SUPPORT-001 | `04_code/modeling_phase1/round4_q1_figures.py` | `figures/FIG-Q1-R4-004_support_strata.pdf`；同名 PNG | 横轴配比组数；纵轴规模；堆叠 IN/NEAR/OUT | A6/A8 同一 p；经验支持不等于现实供给或最终 Q3 域 | 附录候选 | CHECKED PAPER CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE |

图形宣称、来源、SHA-256 与 PNG 分辨率由 Round 4 QA 检查；四张 PNG 亦已人工查看无明显裁切。论文最终位图参考至少 300 dpi；当前优先采用 PDF 向量文件。

## Round5 Q2 figures

| ID | Purpose | Result IDs | Source/paths | Script | Status |
|---|---|---|---|---|---|
| FIG-Q2-R5-001 | 八条附件轨迹与幂律吻合；微小残差不证明外部真实性。 | CAND-Q2-R5-ND-001, CAND-Q2-R5-UNC-001 | 06_results/figures/round5/figure_manifest.json | 04_code/visualization/round5_figures.py | CHECKED CANDIDATE; Gate3 pending |
| FIG-Q2-R5-002 | 三类无随机拆行验证中，加性幂律优于两个透明对照。 | CAND-Q2-R5-VAL-001 | 06_results/figures/round5/figure_manifest.json | 04_code/visualization/round5_figures.py | CHECKED CANDIDATE; Gate3 pending |
| FIG-Q2-R5-003 | 幂指数为常数，总Loss弹性随N-D状态变化。 | CAND-Q2-R5-MARG-001 | 06_results/figures/round5/figure_manifest.json | 04_code/visualization/round5_figures.py | CHECKED CANDIDATE; Gate3 pending |
| FIG-Q2-R5-004 | 上图为半合成表内斜率；下图为假定Q从0.5增至0.6的替代情景，不能解释为真实收益。 | CAND-Q2-R5-QUAL-001, SCEN-Q2-R5-SUB-001 | 06_results/figures/round5/figure_manifest.json | 04_code/visualization/round5_figures.py | CHECKED CANDIDATE; Gate3 pending |

接管完整性复核：4 张 Q2 PNG 与 4 张 PDF 均命中既有 manifest SHA-256；脚本及有效 Run 的源数据齐全。未重画、未新增目视审查；沿用原 R5_VISUAL_QA。合并图表计划见 `03_models/modeling_phase2/round5/Q2_DELIVERY_FIGURE_TABLE_PLAN_v1.md`。候选身份及最终模板嵌入复核要求不变。

## Round6 Q3 figures — CHECKED CANDIDATES

| ID | Purpose | Result IDs | Manifest | Status |
|---|---|---|---|---|
| FIG-Q3-R6-001 | 基线预算路径：虚线为统计支持边界触发，后段平台不代表现实扩展失效。 | CAND-Q3-R6-BASE-001, CAND-Q3-R6-SHIFT-001 | 06_results/figures/round6/figure_manifest.json | CHECKED，Gate4待审 |
| FIG-Q3-R6-002 | 同一REFERENCE质量收益假设下，三类题面成本导致不同质量投入路径。 | SCEN-Q3-R6-QUAL-001 | 06_results/figures/round6/figure_manifest.json | CHECKED，Gate4待审 |
| FIG-Q3-R6-003 | 对数成本的局部与全局质量激活门槛分离，不能只用一阶条件判断投入。 | SCEN-Q3-R6-BREAK-001 | 06_results/figures/round6/figure_manifest.json | CHECKED，Gate4待审 |
| FIG-Q3-R6-004 | C7最大上下文档位仅用作外生情景；30000是成本代理等值点。 | SCEN-Q3-R6-CTX-001 | 06_results/figures/round6/figure_manifest.json | CHECKED，Gate4待审 |
| FIG-Q3-R6-005 | 给定附件的参数带极窄，机制情景范围更宽；两者均不保证外部覆盖。 | SENS-Q3-R6-UNC-001 | 06_results/figures/round6/figure_manifest.json | CHECKED，Gate4待审 |
| FIG-Q3-R6-006 | 预算影子价在统计支持饱和后为零；质量上限价值仍只属收益假设。 | SENS-Q3-R6-SHADOW-001 | 06_results/figures/round6/figure_manifest.json | CHECKED，Gate4待审 |


Gate4 G4-SINGLE-001已接受六张Q3图的限定内容用途；行内Gate4待审为形成时状态。未重画/新增视觉审查，沿用Round6图哈希及视觉QA；最终模板嵌入仍待全文阶段，不晋升FINAL。


## Round7 completed figures

| ID | result | claim | sources | code | files |
| --- | --- | --- | --- | --- | --- |
| FIG-Q4-R7-001 | Q4-R7-001 | Observed evaluation-cohort q90 improves; not an all-time record | Q4_PRIMARY_v1.csv,frontier_family.csv | 04_code/modeling_phase4/round7_figures.py | 06_results/figures/round7/FIG-Q4-R7-001.png;06_results/figures/round7/FIG-Q4-R7-001.svg |
| FIG-Q4-R7-002 | Q4-R7-002 | Parameter/residual decomposition is descriptive and incomplete | decomposition_changes.csv,frontier_family.csv | 04_code/modeling_phase4/round7_figures.py | 06_results/figures/round7/FIG-Q4-R7-002.png;06_results/figures/round7/FIG-Q4-R7-002.svg |
| FIG-Q4-R7-003 | Q4-R7-003 | Pythia bridge fails preregistered generalization tests | bridge_residuals.csv,bridge_validation.csv | 04_code/modeling_phase4/round7_figures.py | 06_results/figures/round7/FIG-Q4-R7-003.png;06_results/figures/round7/FIG-Q4-R7-003.svg |
| FIG-Q4-R7-004 | Q4-R7-004 | Logit selected at 4 and 13 weeks; long-horizon validation absent | rolling_metrics.csv | 04_code/modeling_phase4/round7_figures.py | 06_results/figures/round7/FIG-Q4-R7-004.png;06_results/figures/round7/FIG-Q4-R7-004.svg |
| FIG-Q4-R7-005 | Q4-R7-005 | Conditional statistical fan does not include model/source uncertainty | frontier_family.csv,forecast_fan.csv | 04_code/modeling_phase4/round7_figures.py | 06_results/figures/round7/FIG-Q4-R7-005.png;06_results/figures/round7/FIG-Q4-R7-005.svg |
| FIG-Q4-R7-006 | Q4-R7-006 | Family and population selection affect decomposition and forecast | same_family_trajectories.csv,robustness_variants.csv | 04_code/modeling_phase4/round7_figures.py | 06_results/figures/round7/FIG-Q4-R7-006.png;06_results/figures/round7/FIG-Q4-R7-006.svg |
| FIG-Q4-R7-007 | Q4-R7-007 | Long-horizon model spread is separate from statistical intervals | forecast_all_models_scenarios.csv | 04_code/modeling_phase4/round7_figures.py | 06_results/figures/round7/FIG-Q4-R7-007.png;06_results/figures/round7/FIG-Q4-R7-007.svg |
| FIG-Q4-R7-008 | Q4-R7-008 | Collapsed scenarios do not establish robustness to real compute slowdown | scenario_decomposition.csv | 04_code/modeling_phase4/round7_figures.py | 06_results/figures/round7/FIG-Q4-R7-008.png;06_results/figures/round7/FIG-Q4-R7-008.svg |

## v5 supplementary visualizations

The following figures are visual derivations from already frozen outputs. Their Run manifests record input, code, and output SHA-256 hashes. They add no new fitted model or Result ID.

| ID | Run | Reader task and boundary | Figure and machine source |
| --- | --- | --- | --- |
| FIG-Q1-V5-001 | SUPP-Q1-VIS-20260925-v1 | Compare A1 W0/W1/DQ0 ranks; constructed scores are not observed training returns | `06_results/figures/paper_v5/FIG-Q1-V5-001_rank_rules.png`; `Q_FULL_A1_RANKS_v1.csv` and `Q_FULL_DOMAIN_RESULTS_v1.csv` |
| FIG-Q1-V5-002 | SUPP-Q1-VIS-20260925-v1 | Show six preregistered signed Spearman pairs; correlation is not semantic conflict or causality | `06_results/figures/paper_v5/FIG-Q1-V5-002_fixed_pair_correlations.png`; `QUALITY_CORRELATION_PAIRS_v1.csv` |
| FIG-Q2-V5-001 | SUPP-Q2-VIS-20260925-v1 | Display five parameter conditional quantiles and the joint α–β draws; eight-trajectory numerical stability is not external generalization | `06_results/figures/paper_v5/FIG-Q2-V5-001_bootstrap_joint.png`; `cluster_bootstrap.csv` and `summary.json` |
| FIG-Q3-V5-001 | SUPP-Q3-VIS-20260925-v1 | Trace 51-budget training, attention, and unused shares against support transitions; slack is a statistical support outcome, not observed industry saturation | `06_results/figures/paper_v5/FIG-Q3-V5-001_budget_composition.png`; `budget_path.csv` and frozen Q3 summary |
| FIG-Q4-V5-001 | SUPP-Q4-VIS-20260925-v1 | Show two target dates under three exogenous positive-growth retention assumptions; interval bars apply only to the reference model | `06_results/figures/paper_v5/FIG-Q4-V5-001_exogenous_slowdown.png`; `EXOGENOUS_COMPUTE_SLOWDOWN_SCENARIOS_v1.csv` |
| FIG-Q4-V5-002 | SUPP-Q4-VIS-20260925-v1 | Show six task-specific endpoint changes and the separate descriptive parameter-associated component | `06_results/figures/paper_v5/FIG-Q4-V5-002_six_task_deltas.png`; `TABLE-Q4-R7-007.csv` |
