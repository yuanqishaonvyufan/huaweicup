# Final paper evidence map v1

起点 HEAD: 029b51e0709972a238c7a34882844c36397836a7

只读取有效冻结产物；不重训、不修改机器结果。摘要核心结论必须携带所列限制。

## E01 1M R0留出误差
- **question**: 1
- **formula**: 见公式登记
- **source_file**: 03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_METRICS_v2.json
- **result_id**: CAND-Q1-R4-VAL-001
- **run**: VAL-Q1-PRESP-A6A11-R4-20260924-v2
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 限附件内部及规定用途
- **forbidden_wording**: 普适因果结论
- **paper_section**: 5.3
- **figure_table_support**: 图2 表3
- **selector**: metrics/1M/*/R0_RMSE_raw
- **source_sha256**: b9362e2f82dd04c7f8086a0d644e55b3c67c708b94f51988f6c42341ceb9fda2
- **Numerical value**: {"M0": 0.2846149798599803, "M1": 0.2277652126109652}

## E02 1M逐域误差及全部改善
- **question**: 1
- **formula**: 见公式登记
- **source_file**: 03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_METRICS_v2.json
- **result_id**: CAND-Q1-R4-VAL-002
- **run**: VAL-Q1-PRESP-A6A11-R4-20260924-v2
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 限附件内部及规定用途
- **forbidden_wording**: 普适因果结论
- **paper_section**: 5.3
- **figure_table_support**: 图2 附录B
- **selector**: metrics/1M/*/domain_RMSE_raw
- **source_sha256**: b9362e2f82dd04c7f8086a0d644e55b3c67c708b94f51988f6c42341ceb9fda2
- **Numerical value**: {"M0": [0.7968727338169288, 0.7377561889376494, 0.8407758795158649, 0.5463924616676069, 1.5392828252360693, 0.9439876197741494, 0.6759335543748374, 0.44895630889823496, 0.3205502612818174, 0.9994356224413378, 0.336555349056319, 0.5708445416742268, 0.5103829885899203], "M1": [0.5888305920438673, 0.48056171811205795, 0.5311874229072513, 0.29571839942925016, 1.1604521500142577, 0.6128758042644806, 0.4487203666789868, 0.2564272615803121, 0.15316725435413237, 0.6486588861444348, 0.19004076265604103, 0.2626328449514563, 0.2725447189986594], "improved": 13}

## E03 中心化规模迁移误差比
- **question**: 1
- **formula**: 见公式登记
- **source_file**: 03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_METRICS_v2.json
- **result_id**: CAND-Q1-R4-TRANSFER-001
- **run**: VAL-Q1-PRESP-A6A11-R4-20260924-v2
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 60M部分中心化迁移；1B失败
- **forbidden_wording**: 1B绝对预测通过
- **paper_section**: 5.4
- **figure_table_support**: 表3
- **selector**: metrics/*/M1/R0_centered_RMSE_ratio_to_M0
- **source_sha256**: b9362e2f82dd04c7f8086a0d644e55b3c67c708b94f51988f6c42341ceb9fda2
- **Numerical value**: {"60M": 0.8875744816416311, "1B": 3.108487461713722}

## E04 经验支持分类
- **question**: 1
- **formula**: 见公式登记
- **source_file**: 03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_METRICS_v2.json
- **result_id**: CAND-Q1-R4-SUPPORT-001
- **run**: VAL-Q1-PRESP-A6A11-R4-20260924-v2
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 凸包和近邻支持
- **forbidden_wording**: 真实供给可实施保证
- **paper_section**: 5.4
- **figure_table_support**: 表3
- **selector**: support_counts
- **source_sha256**: b9362e2f82dd04c7f8086a0d644e55b3c67c708b94f51988f6c42341ceb9fda2
- **Numerical value**: {"1M": {"NEAR_SUPPORT": 252, "IN_SUPPORT": 2, "OUT_OF_SUPPORT": 2}, "60M": {"NEAR_SUPPORT": 252, "IN_SUPPORT": 2, "OUT_OF_SUPPORT": 2}, "1B": {"NEAR_SUPPORT": 46, "IN_SUPPORT": 15, "OUT_OF_SUPPORT": 3}}

## E05 全22项角色与记录规模
- **question**: 1
- **formula**: 见公式登记
- **source_file**: 03_models/modeling_phase1/q1/round4/Q1_QUALITY_CLOSURE_METRICS_v1.json
- **result_id**: CAND-Q1-R4-QUAL-001
- **run**: VAL-Q1-PRESP-A6A11-R4-20260924-v2
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 限附件内部及规定用途
- **forbidden_wording**: 普适因果结论
- **paper_section**: 5.1
- **figure_table_support**: 图1 附录A
- **selector**: role_counts
- **source_sha256**: b6ad755f153017b09b23473c401bce8da66d3402b6f3689e76092c90831c9aac
- **Numerical value**: {"SENSITIVITY": 12, "CORE": 5, "REDUNDANT": 2, "SECONDARY": 2, "UNKNOWN": 1}

## E06 确认语义冲突为0
- **question**: 1
- **formula**: 见公式登记
- **source_file**: 01_data/audits/modeling_phase1/q1/QUALITY_CONFLICT_CANDIDATES_v1.md
- **result_id**: AUDIT-Q1-SEMANTICS-CONFLICT-20260924-v1
- **run**: VAL-Q1-PRESP-A6A11-R4-20260924-v2
- **evidence_grade**: PAPER SUPPORTING
- **allowed_wording**: 已核候选未确认语义冲突
- **forbidden_wording**: 负相关即语义冲突
- **paper_section**: 5.2
- **figure_table_support**: 图1
- **selector**: 正式审计报告
- **source_sha256**: bb18de26aee7aa387bb1d2395869c5ee34e47d29ff6efb4dffaa332d0d82ecfe
- **Numerical value**: "0；统计分歧与域反转另列"

## E07 五参数加性幂律
- **question**: 2
- **formula**: L∞+A N^(-α)+B D^(-β)；N,D均十亿
- **source_file**: 06_results/raw/EXP-Q2-ND-R5-20260924-v1/summary.json
- **result_id**: CAND-Q2-R5-ND-001
- **run**: EXP-Q2-ND-R5-20260924-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 限附件内部及规定用途
- **forbidden_wording**: 普适因果结论
- **paper_section**: 6.1
- **figure_table_support**: 表4
- **selector**: parameters
- **source_sha256**: e92a1e7c9c280f665ebf50e870d2dc332101b8cde8f8255b954a841e58821a35
- **Numerical value**: {"E": 1.6897975629393145, "A": 0.3539803206519287, "B": 1.2403055835398427, "alpha": 0.3399765819061934, "beta": 0.27987812854708494}

## E08 三类分组验证
- **question**: 2
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q2-ND-R5-20260924-v1/summary.json
- **result_id**: CAND-Q2-R5-VAL-001
- **run**: EXP-Q2-ND-R5-20260924-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 附件内部误差很低
- **forbidden_wording**: 真实世界预测精度极高
- **paper_section**: 6.2
- **figure_table_support**: 图3 表5
- **selector**: validation
- **source_sha256**: e92a1e7c9c280f665ebf50e870d2dc332101b8cde8f8255b954a841e58821a35
- **Numerical value**: {"LONO": {"S1": {"macro_rmse": 0.00014688818680258544, "worst_rmse": 0.0002202303704479108, "macro_mae": 0.0001078781705102824}, "S0": {"macro_rmse": 0.3513060875921693, "worst_rmse": 0.5870402590132381, "macro_mae": 0.27704581341768975}, "Slog": {"macro_rmse": 0.11798721364351741, "worst_rmse": 0.19734817854553582, "macro_mae": 0.09073943254723343}, "pass": true}, "FORWARD": {"S1": {"macro_rmse": 0.00011164198178839331, "worst_rmse": 0.00017650889732141414, "macro_mae": 9.009869567404256e-05}, "S0": {"macro_rmse": 0.2712738766118454, "worst_rmse": 0.4662329409381822, "macro_mae": 0.2708190837989295}, "Slog": {"macro_rmse": 0.12038632428086248, "worst_rmse": 0.23759445245265123, "macro_mae": 0.11837514268223667}, "pass": true}, "BLOCK2D": {"S1": {"macro_rmse": 0.00011413398023678218, "worst_rmse": 0.00018962980941470892, "macro_mae": 9.080098143561844e-05}, "S0": {"macro_rmse": 0.2900686162949237, "worst_rmse": 0.46326310634989826, "macro_mae": 0.28987922740524774}, "Slog": {"macro_rmse": 0.12291922923259953, "worst_rmse": 0.2864105808587308, "macro_mae": 0.12144096755123493}, "pass": true}}

## E09 参数稳定性
- **question**: 2
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q2-ND-R5-20260924-v1/summary.json
- **result_id**: CAND-Q2-R5-UNC-001
- **run**: EXP-Q2-ND-R5-20260924-v1
- **evidence_grade**: SENSITIVITY ONLY
- **allowed_wording**: 限附件内部及规定用途
- **forbidden_wording**: 普适因果结论
- **paper_section**: 6.2
- **figure_table_support**: 表4
- **selector**: full_fit
- **source_sha256**: e92a1e7c9c280f665ebf50e870d2dc332101b8cde8f8255b954a841e58821a35
- **Numerical value**: {"sse": 2.5238258731563895e-05, "successful_starts": 12, "total_starts": 12, "max_start_parameter_spread": 1.477109545788835e-10, "min_start_sse": 2.5238258731563895e-05, "max_start_sse": 2.5238258731570532e-05, "jacobian_rank": 5, "jacobian_condition": 33.83473182319467, "boundary": false}

## E10 示例点导数弹性与替代
- **question**: 2
- **formula**: εN=-αU/L；εD=-βV/L；dlnD/dlnN=-αU/(βV)
- **source_file**: 06_results/raw/EXP-Q2-ND-R5-20260924-v1/marginal_effects.csv
- **result_id**: CAND-Q2-R5-MARG-001
- **run**: EXP-Q2-ND-R5-20260924-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 限附件内部及规定用途
- **forbidden_wording**: 普适因果结论
- **paper_section**: 6.3
- **figure_table_support**: 图4
- **selector**: N=1,D=100
- **source_sha256**: bc2852ad56302a2dbc333a1754f310884d26dd6615953f735084c5fd67875249
- **Numerical value**: 完整值与逐行记录见同名 JSON；源文件及选择器如上。

## E11 B7半合成质量校准
- **question**: 2
- **formula**: 见公式登记
- **source_file**: 06_results/raw/SCEN-Q2-R5-20260924-v3/summary.json
- **result_id**: CAND-Q2-R5-QUAL-001
- **run**: SCEN-Q2-R5-20260924-v3
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 题目半合成质量表内校准
- **forbidden_wording**: 真实因果质量弹性
- **paper_section**: 6.4
- **figure_table_support**: 表6
- **selector**: quality_*
- **source_sha256**: ee7c02886d66bbec56e583613aa46f1ba627de38780245079762ac0b1622ebb2
- **Numerical value**: {"quality_common_g": 0.36199528619528604, "quality_negative_cells": 45, "quality_cells": 45, "quality_centered_LOO_macro_RMSE": {"Qcommon": 0.05296418456178245, "Qscale": 0.0436788725990616}}

## E12 跨来源中心化形状诊断
- **question**: 2
- **formula**: 见公式登记
- **source_file**: 06_results/raw/SCEN-Q2-R5-20260924-v3/summary.json
- **result_id**: CAND-Q2-R5-EXT-001
- **run**: SCEN-Q2-R5-20260924-v3
- **evidence_grade**: PAPER SUPPORTING
- **allowed_wording**: 目标均值中心化的事后形状检查
- **forbidden_wording**: 外部绝对Loss验证成功
- **paper_section**: 6.2
- **figure_table_support**: 表6
- **selector**: external_summary
- **source_sha256**: ee7c02886d66bbec56e583613aa46f1ba627de38780245079762ac0b1622ebb2
- **Numerical value**: {"B2": {"groups": 7, "median_centered_ratio": 0.8550844812499261}, "B4": {"groups": 11, "median_centered_ratio": 0.4366006942971866}, "B5": {"groups": 8, "median_centered_ratio": 0.5551350436939388}, "B10": {"groups": 0, "median_centered_ratio": null}}

## E13 有限质量替代条件
- **question**: 2
- **formula**: 见公式登记
- **source_file**: 06_results/raw/SCEN-Q2-R5-20260924-v3/quality_substitution_scenarios.csv
- **result_id**: SCEN-Q2-R5-SUB-001
- **run**: SCEN-Q2-R5-20260924-v3
- **evidence_grade**: SCENARIO ONLY
- **allowed_wording**: 假设量尺可运输时的条件替代
- **forbidden_wording**: 真实资源节省
- **paper_section**: 6.4
- **figure_table_support**: 表6
- **selector**: N=1,D=100,lambda=1
- **source_sha256**: 9fd168f7ffdea042ce45c1e2de351c6ecb5cfc5c4c9966d0240e84aa8e2a2db0
- **Numerical value**: 完整值与逐行记录见同名 JSON；源文件及选择器如上。

## E14 三个预算配置
- **question**: 3
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv
- **result_id**: CAND-Q3-R6-BASE-001
- **run**: EXP-Q3-BASE-R6-20260924-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 题设成本与统计支持范围内最优
- **forbidden_wording**: 现实产业最优
- **paper_section**: 7.2
- **figure_table_support**: 图5 表7
- **selector**: Budget_FLOPs=1e19,1e22,1e24
- **source_sha256**: a114bc9a6dd66519c8e57c76644b515169eae5524ef9778235563015a5382a94
- **Numerical value**: [{"Budget_FLOPs": "1e+19", "L_ctx": "2048", "N_B": "0.22130872721718978", "D_B": "7.049698310488851", "Q": "0.5", "loss": "2.998934933219959", "quality": "OFF", "mixture": "OFF", "total_FLOPs": "1e+19", "budget_slack_FLOPs": "0.0", "budget_relative_violation": "0.0", "mu_per_1e18": "0.020096169212695393", "dLoss_dBudget_FLOPs": "-2.0096169212695393e-20", "kkt_projected_max": "2.7755575615628914e-17", "complementarity": "0.0", "active_constraints": "BUDGET_ACTIVE", "quality_cap_value": "0.0", "support_status": "B1_RECTANGLE_CONDITIONAL", "train_FLOPs": "9.360958562156763e+18", "attention_FLOPs": "6.390414378432351e+17", "quality_FLOPs": "0.0"}, {"Budget_FLOPs": "1e+22", "L_ctx": "2048", "N_B": "5.202388052937084", "D_B": "299.893", "Q": "0.5", "loss": "2.143211279482246", "quality": "OFF", "mixture": "OFF", "total_FLOPs": "1e+22", "budget_slack_FLOPs": "0.0", "budget_relative_violation": "0.0", "mu_per_1e18": "6.869671353280326e-06", "dLoss_dBudget_FLOPs": "-6.869671353280325e-24", "kkt_projected_max": "0.0", "complementarity": "0.0", "active_constraints": "D_HIGH;BUDGET_ACTIVE", "quality_cap_value": "0.0", "support_status": "B1_RECTANGLE_CONDITIONAL", "train_FLOPs": "9.360958562156765e+21", "attention_FLOPs": "6.390414378432351e+20", "quality_FLOPs": "0.0"}, {"Budget_FLOPs": "1e+24", "L_ctx": "2048", "N_B": "11.965825", "D_B": "299.893", "Q": "0.5", "loss": "2.093379471494165", "quality": "OFF", "mixture": "OFF", "total_FLOPs": "2.300063908774456e+22", "budget_slack_FLOPs": "9.769993609122555e+23", "budget_relative_violation": "0.0", "mu_per_1e18": "0.0", "dLoss_dBudget_FLOPs": "-0.0", "kkt_projected_max": "0.0", "complementarity": "0.0", "active_constraints": "N_HIGH;D_HIGH;BUDGET_SLACK", "quality_cap_value": "0.0", "support_status": "B1_RECTANGLE_CONDITIONAL", "train_FLOPs": "2.1530802940349996e+22", "attention_FLOPs": "1.46983614739456e+21", "quality_FLOPs": "0.0"}]

## E15 支持约束结构转移
- **question**: 3
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q3-BASE-R6-20260924-v1/summary.json
- **result_id**: CAND-Q3-R6-SHIFT-001
- **run**: EXP-Q3-BASE-R6-20260924-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: D上界先激活，两上界随后同时活跃
- **forbidden_wording**: 数据300B后不再有价值
- **paper_section**: 7.2
- **figure_table_support**: 图5
- **selector**: transitions
- **source_sha256**: adb54610b6e2dcb5d0735653d4fe8bea4f398a09584c7728fdcdab76f92c710b
- **Numerical value**: {"unconstrained_N_upper_C": 6.886597184056822e+22, "unconstrained_D_upper_C": 9.325359035607933e+21, "both_upper_saturation_C": 2.300063908774456e+22, "N_budget_elasticity_interior": 0.4515221451530468, "D_budget_elasticity_interior": 0.5484778548469532}

## E16 解析与数值求解一致
- **question**: 3
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q3-BASE-R6-20260924-v1/summary.json
- **result_id**: CAND-Q3-R6-BASE-001
- **run**: EXP-Q3-BASE-R6-20260924-v1
- **evidence_grade**: PAPER SUPPORTING
- **allowed_wording**: 限附件内部及规定用途
- **forbidden_wording**: 普适因果结论
- **paper_section**: 7.2
- **figure_table_support**: 表7
- **selector**: rows/numeric_starts/max_loss_gap/max_kkt
- **source_sha256**: adb54610b6e2dcb5d0735653d4fe8bea4f398a09584c7728fdcdab76f92c710b
- **Numerical value**: {"rows": 51, "numeric_starts": 204, "max_loss_gap": 4.858335955759685e-13, "max_kkt": 2.7755575615628914e-17}

## E18 局部与全局启动门槛
- **question**: 3
- **formula**: 见公式登记
- **source_file**: 06_results/raw/SCEN-Q3-R6-20260924-v1/quality_break_even.csv
- **result_id**: SCEN-Q3-R6-BREAK-001
- **run**: SCEN-Q3-R6-20260924-v1
- **evidence_grade**: SCENARIO ONLY
- **allowed_wording**: 条件情景
- **forbidden_wording**: 实测成本收益或窗口推荐
- **paper_section**: 7.3—7.5
- **figure_table_support**: 图6 表8
- **selector**: quality_break_even.csv
- **source_sha256**: a22a5bedceff335f4c6bb48e99505c0069dc7eeb8c2b952935a5c936ad53b224
- **Numerical value**: 完整值与逐行记录见同名 JSON；源文件及选择器如上。

## E19 外生上下文比较
- **question**: 3
- **formula**: 见公式登记
- **source_file**: 06_results/raw/SCEN-Q3-R6-20260924-v1/context_baseline.csv
- **result_id**: SCEN-Q3-R6-CTX-001
- **run**: SCEN-Q3-R6-20260924-v1
- **evidence_grade**: SCENARIO ONLY
- **allowed_wording**: 条件情景
- **forbidden_wording**: 实测成本收益或窗口推荐
- **paper_section**: 7.3—7.5
- **figure_table_support**: 图6 表8
- **selector**: context_baseline.csv
- **source_sha256**: 71be6ad560e222058e4a52048fdaf4a728d06898c6bfc5341a07ca195218d622
- **Numerical value**: 完整值与逐行记录见同名 JSON；源文件及选择器如上。

## E20 联合参数传播
- **question**: 3
- **formula**: 见公式登记
- **source_file**: 06_results/RESULTS_REGISTRY.md
- **result_id**: SENS-Q3-R6-UNC-001
- **run**: EXP-Q3-BASE-R6-20260924-v1
- **evidence_grade**: SENSITIVITY ONLY
- **allowed_wording**: 条件参数敏感性；情景包络另报
- **forbidden_wording**: 情景包络是置信区间
- **paper_section**: 7.6
- **figure_table_support**: 图7
- **selector**: Round6 CP4
- **source_sha256**: 09110cb4ca8cbefb391b554cebd13756c6c79a1e725245c4c1fdc0333e27d6ad
- **Numerical value**: "200联合向量；51000配置"

## E21 参数关联与调整残差分解
- **question**: 4
- **formula**: ΔF=ΔS+ΔR
- **source_file**: 06_results/raw/EXP-Q4-R7-20260925-v1/decomposition_changes.csv
- **result_id**: Q4-R7-002
- **run**: EXP-Q4-R7-20260925-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 指定样本窗口下描述性分解
- **forbidden_wording**: 82.98%由技术创新因果造成
- **paper_section**: 8.3
- **figure_table_support**: 图8 表10
- **selector**: model=family
- **source_sha256**: ba603ab9a44fa5588b265d24955686a303f0d0ceb6ee1f0e28b05d29e1bd2699
- **Numerical value**: [{"model": "N_only", "start": "2024-06-16", "end": "2025-03-14", "delta_F": "15.879649195667376", "delta_S": "2.8229293999150844", "delta_R": "13.056719795752292", "parameter_share": "0.17777026212174107", "residual_share": "0.8222297378782589", "beta_logN": "4.799425309000221", "time_score_per_year": ""}, {"model": "pooled", "start": "2024-06-16", "end": "2025-03-14", "delta_F": "15.879649195667376", "delta_S": "2.6540696316991923", "delta_R": "13.225579563968184", "parameter_share": "0.16713654054922902", "residual_share": "0.832863459450771", "beta_logN": "4.512337064685062", "time_score_per_year": "5.144881632444912"}, {"model": "family", "start": "2024-06-16", "end": "2025-03-14", "delta_F": "15.879649195667376", "delta_S": "2.703245149939386", "delta_R": "13.17640404572799", "parameter_share": "0.17023330406297282", "residual_share": "0.8297666959370272", "beta_logN": "4.595943203340986", "time_score_per_year": "4.5740374294677855"}]

## E22 桥接未通过
- **question**: 4
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q4-R7-20260925-v1/bridge_validation.csv
- **result_id**: Q4-R7-003
- **run**: EXP-Q4-R7-20260925-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 无可靠桥接，能力直接预测
- **forbidden_wording**: 弱定量桥接仍成立
- **paper_section**: 8.2
- **figure_table_support**: 表9
- **selector**: HIGH_pythia/LOSO
- **source_sha256**: 9cd86832ac7fa8b9be2b910e8122db71603c7ef5bef01d89c57bfa77b7f9a921
- **Numerical value**: [{"family": "HIGH_pythia", "split": "HIGH_SCALE", "method": "linear", "rmse": "0.4971448708734639", "mae": "0.494951559776061", "n": "2"}, {"family": "HIGH_pythia", "split": "HIGH_SCALE", "method": "mean", "rmse": "0.4971448708734639", "mae": "0.494951559776061", "n": "2"}, {"family": "HIGH_pythia", "split": "HIGH_SCALE", "method": "monotone", "rmse": "0.23610912656198574", "mae": "0.2314552732923283", "n": "2"}, {"family": "HIGH_pythia", "split": "LOSO", "method": "linear", "rmse": "0.5528338936058493", "mae": "0.47810768059179104", "n": "7"}, {"family": "HIGH_pythia", "split": "LOSO", "method": "mean", "rmse": "0.42444846214318305", "mae": "0.3755617007914142", "n": "7"}, {"family": "HIGH_pythia", "split": "LOSO", "method": "monotone", "rmse": "0.436634672876873", "mae": "0.3605642376494115", "n": "7"}, {"family": "HIGH_pythia", "split": "LOW_SCALE", "method": "linear", "rmse": "0.9987344406582617", "mae": "0.8315397630627808", "n": "2"}, {"family": "HIGH_pythia", "split": "LOW_SCALE", "method": "mean", "rmse": "0.35705863801977156", "mae": "0.25329337772292115", "n": "2"}, {"family": "HIGH_pythia", "split": "LOW_SCALE", "method": "monotone", "rmse": "0.4797678509726912", "mae": "0.40846524336925727", "n": "2"}]

## E23 短期限滚动回测
- **question**: 4
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q4-R7-20260925-v1/rolling_metrics.csv
- **result_id**: Q4-R7-004
- **run**: EXP-Q4-R7-20260925-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 4/13周回溯滚动验证
- **forbidden_wording**: 12/24月预测已验证
- **paper_section**: 8.4
- **figure_table_support**: 表11
- **selector**: model=logit
- **source_sha256**: 044e1585338c5cd39d69da02af20ad69acd93a9f3aeb8c7363238947be425c38
- **Numerical value**: [{"model": "linear", "horizon_weeks": "4", "MAE": "1.7634724874598422", "RMSE": "2.072824284635672", "coverage95": "1.0", "n": "20"}, {"model": "linear", "horizon_weeks": "13", "MAE": "1.5644368549580696", "RMSE": "1.6642572005841558", "coverage95": "1.0", "n": "11"}, {"model": "local_logit", "horizon_weeks": "4", "MAE": "1.9146212907565645", "RMSE": "2.6511506496916915", "coverage95": "0.8", "n": "20"}, {"model": "local_logit", "horizon_weeks": "13", "MAE": "2.8674115761426915", "RMSE": "3.4465835472157313", "coverage95": "1.0", "n": "11"}, {"model": "logit", "horizon_weeks": "4", "MAE": "1.7565863122322334", "RMSE": "2.0743612511497895", "coverage95": "1.0", "n": "20"}, {"model": "logit", "horizon_weeks": "13", "MAE": "1.529282882571689", "RMSE": "1.6148020227880557", "coverage95": "1.0", "n": "11"}, {"model": "persistence", "horizon_weeks": "4", "MAE": "1.995688831218732", "RMSE": "2.506803151589236", "coverage95": "1.0", "n": "20"}, {"model": "persistence", "horizon_weeks": "13", "MAE": "3.683315719802216", "RMSE": "4.11041298348994", "coverage95": "1.0", "n": "11"}]

## E24 两期限条件预测与区间
- **question**: 4
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q4-R7-20260925-v1/forecast_summary.json
- **result_id**: Q4-R7-005;Q4-R7-007
- **run**: EXP-Q4-R7-20260925-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 远外推条件中心及模型区间；中心范围另报
- **forbidden_wording**: 高可信确定预测
- **paper_section**: 8.5
- **figure_table_support**: 图9 表12
- **selector**: forecast
- **source_sha256**: 4f9cb379ea8d808884c18123a00a355713370e26f12c0032eccf3f7ab4d0944d
- **Numerical value**: [{"target": "2027-09-25", "central": 79.75536356779305, "conditional_PI95": [61.24204722669209, 90.40150198993967], "model_range": [52.16859687691628, 83.77111309771917], "scenario_range": [79.75536356779305, 79.75536356779305], "no_slowdown_reference": 79.75536356779305, "removed_scale_component": 0.0}, {"target": "2028-09-25", "central": 87.12751211384048, "conditional_PI95": [69.58018633055818, 95.56880507036963], "model_range": [52.33272228155908, 97.11295319946106], "scenario_range": [87.12751211384048, 87.12751211384048], "no_slowdown_reference": 87.12751211384048, "removed_scale_component": 0.0}]

## E25 数据截止与预测原点
- **question**: 4
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q4-R7-20260925-v1/forecast_summary.json
- **result_id**: Q4-R7-005
- **run**: EXP-Q4-R7-20260925-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 560天空档；长期外推
- **forbidden_wording**: 以最新产业观测为条件
- **paper_section**: 8.5
- **figure_table_support**: 图9 表12
- **selector**: origin,last_data,gap_days
- **source_sha256**: 4f9cb379ea8d808884c18123a00a355713370e26f12c0032eccf3f7ab4d0944d
- **Numerical value**: {"origin": "2026-09-25", "last_data": "2025-03-14", "gap_days": 560}

## E26 规模情景重合
- **question**: 4
- **formula**: A(h)=max(0,bS h)=0
- **source_file**: 06_results/raw/EXP-Q4-R7-20260925-v1/forecast_summary.json
- **result_id**: Q4-R7-008
- **run**: EXP-Q4-R7-20260925-v1
- **evidence_grade**: SCENARIO ONLY
- **allowed_wording**: 正增长情景不能区分
- **forbidden_wording**: 真实算力放缓不影响能力
- **paper_section**: 8.5
- **figure_table_support**: 表12
- **selector**: scale_slope_week
- **source_sha256**: 4f9cb379ea8d808884c18123a00a355713370e26f12c0032eccf3f7ab4d0944d
- **Numerical value**: -0.02973937522845124

## E27 筛选和时间窗口下分解反号
- **question**: 4
- **formula**: 见公式登记
- **source_file**: 06_results/raw/EXP-Q4-R7-20260925-v1/robustness_variants.csv
- **result_id**: Q4-R7-006
- **run**: EXP-Q4-R7-20260925-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 分解比例不稳健
- **forbidden_wording**: 稳健因果技术归因
- **paper_section**: 8.3
- **figure_table_support**: 表10
- **selector**: known_families/strict_license/start_2024_09/window_56d
- **source_sha256**: d68414b8483ef7a2bcc3d7854190e4a186e60c61351aa2b05829c44275e6318d
- **Numerical value**: 完整值与逐行记录见同名 JSON；源文件及选择器如上。

## E28 历史同口径前沿端点
- **question**: 4
- **formula**: C8六维原始均值；28天q90；0—100分
- **source_file**: 06_results/raw/EXP-Q4-R7-20260925-v1/frontier_family.csv
- **result_id**: Q4-R7-001
- **run**: EXP-Q4-R7-20260925-v1
- **evidence_grade**: PAPER CORE
- **allowed_wording**: 评测群体高分位前沿
- **forbidden_wording**: 全生态历史最高分
- **paper_section**: 8.1
- **figure_table_support**: 图8
- **selector**: first,last
- **source_sha256**: 4c0362347e68a0da1481d112c676693ff612b68dc4970dd2b39edbe230ce8a85
- **Numerical value**: [{"date": "2024-06-16", "t_week": "0.0", "n": "16", "F": "36.4530730858917", "S": "9.670537932835904", "R": "26.782535153055797", "frontier_logN": "2.1041465277042546", "lower_ID": "01-ai/yi-1.5-9b-chat-16k", "upper_ID": "qwen/qwen2-7b", "upper_weight": "0.5", "max_input_date": "2024-06-16", "min_input_date": "2024-06-16", "is_sunday": "True", "known_family_share": "0.8125", "largest_family_share": "0.4375"}, {"date": "2025-03-14", "t_week": "38.714285714285715", "n": "99", "F": "52.33272228155908", "S": "12.37378308277529", "R": "39.95893919878379", "frontier_logN": "2.6923272406369736", "lower_ID": "prithivmlmods/primal-opus-14b-optimus-v2", "upper_ID": "lunzima/nqlsg-qwen2.5-14b-megafusion-v5", "upper_weight": "0.20000000000000284", "max_input_date": "2025-03-14", "min_input_date": "2025-02-18", "is_sunday": "False", "known_family_share": "0.7878787878787878", "largest_family_share": "0.36363636363636365"}]
