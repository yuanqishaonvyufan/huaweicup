# RESULTS_REGISTRY

**当前 Gate3：G3-SINGLE-001 / Verdict A — PASS。Q2 PROVISIONALLY CLOSED；Q3 AUTHORIZED TO START / NOT EXECUTED。既有 Run/数值/图与证据等级不变，无新模型运行；下方 Gate3 待审文字保留形成时状态。FINAL 仍为0。**

当前：14项Q1 + 9项Q2候选；Round5数值QA通过，Gate3待审，VALIDATED FINAL=NONE。以下Round4统计保留历史范围。

论文唯一允许直接引用的定量结果源。MODELING PHASE 1 ROUND 4 累计 14 项**候选/诊断数值及模型选择状态**（Round 3 的 5 项及 Round 4 的 9 项）；VALIDATED FINAL RESULTS：NONE。Round 4 的 A7 留出证据已通过本地 QA，Gate 2 已接受 Q1 暂定关闭与受限用途，模型仍为 PROVISIONAL；不得提前标为 VALIDATED FINAL RESULT。

| Result ID | Question | Variable / Metric | Value | Unit | Confidence interval | Source experiment | Source dataset | Source model | Source code | Validation status | Paper location | Figure / Table ID | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

| CAND-Q1-DQ-R3-001 | Q1 | 五核心 DQ1 PC1 方差份额 | 0.4811446 | 比例 | A1 域内 bootstrap 2.5–97.5%：0.478684–0.483691；非独立总体推断 | MC-Q1-DQ-R3-20260924-v1 | A1 训练参考 40,926 ID；输入哈希见 INPUT_MANIFEST_v1.json | DQ1 PCA CANDIDATE | 04_code/modeling_phase1/round3_q1_descriptive.py；哈希见机器 JSON | CANDIDATE — TRAINING STRUCTURE ONLY | NONE | FIG-Q1-R3-001 | 五核心而非 22 维全质量；不能称最终 Q |
| CAND-Q1-DQ-R3-002 | Q1 | DQ2 “无广告单独成组”的域/扩展层数 | 3/9 | 分层数 | NOT_APPLICABLE | DIAG-Q1-DOMAIN-R3-20260924-v1 | A1 七域、A2/A3 非重叠扩展 | DQ2 分组探针 | 04_code/modeling_phase1/round3_domain_support_check.py；哈希见机器 JSON | CANDIDATE — EXPLORATORY DOMAIN DIAGNOSTIC | NONE | NONE | pooled bootstrap 稳定但跨域分组不稳，不固定语义组名 |
| CAND-Q1-RSP-R3-001 | Q1 | R2 PC1 方差份额 | 0.2277804 | 比例 | A5 运行 bootstrap 2.5–97.5%：0.216432–0.247802；训练内 | MC-Q1-RSP-R3-20260924-v1 | A5 512 训练运行；输入哈希见 INPUT_MANIFEST_v1.json | P1-1 R2 CANDIDATE | 04_code/modeling_phase1/round3_q1_response.py；哈希见机器 JSON | CANDIDATE — NO HELDOUT VALIDATION | NONE | FIG-Q1-R3-004 | R2 不代表 13 域；R3 必保留 |
| CAND-Q1-RSP-R3-002 | Q1 | R0 与 R2 训练运行 Spearman 排序相关 | 0.5451188 | 相关系数 | NOT_ESTIMATED；训练内描述 | MC-Q1-RSP-R3-20260924-v1 | A5 512 训练运行 | P1-1 R0/R2 CANDIDATES | 04_code/modeling_phase1/round3_q1_response.py；哈希见机器 JSON | CANDIDATE — NO HELDOUT VALIDATION | NONE | NONE | 不以不同单位原始 RMSE 排名 |
| CAND-Q1-RSP-R3-003 | Q1 | 13 域负相关对数 | Pearson 24/78；Spearman 29/78 | 域对 | NOT_APPLICABLE | DIAG-Q1-DOMAIN-R3-20260924-v1 | A5 512 训练运行 × 13 域 | DOMAIN HETEROGENEITY DIAGNOSTIC | 04_code/modeling_phase1/round3_domain_support_check.py；哈希见机器 JSON | CANDIDATE — TRAINING STRUCTURE ONLY | NONE | FIG-Q1-R3-003 | 两相关口径不同，前期 24/78 是 Pearson |
| CAND-Q1-R4-QUAL-001 | Q1 | Full-22 展示角色计数 | CORE 5；SECONDARY 2；SENSITIVITY 12；UNKNOWN 1；REDUNDANT 2 | 指标数 | NOT_APPLICABLE | AUDIT-Q1-QUALITY-CLOSURE-R4-20260924-v1 | A1/A2/A3 272,505 物理记录 | PROVISIONAL MULTIDIMENSIONAL QUALITY PROFILE | round4_quality_closure.py；哈希见机器 JSON | CHECKED CANDIDATE — DESCRIPTIVE ONLY | NONE | FIG-Q1-R4-001 | 不等于下游资格；Q2 TYPE E=0 |
| CAND-Q1-R4-VAL-001 | Q1 | A7/1M M1 与 M0 的 R0 RMSE | M1 0.2278；M0 0.2846 | A5/A7 原表交叉熵 Loss | M1−M0 R0 MSE 成对 bootstrap 2.5–97.5%：−0.03949 至 −0.01893 | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | A4/A5 训练 512；A6/A7 留出 256 | M1 16D SIMPLEX-CONTRAST CANDIDATE | round4_train_p_response.py；round4_validate_p_response.py，哈希见机器 JSON | CHECKED OUT-OF-SAMPLE CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE | NONE | FIG-Q1-R4-002 | 仅 1M 同尺度/经验近邻范围；非因果 p 效应 |
| CAND-Q1-R4-VAL-002 | Q1 | A7/1M 改善域数与 RMSE 比 | 13/13 域改善；比率 0.460–0.754 | 域及比例 | NOT_APPLICABLE | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | A7 256 运行 × 13 域 | M1 R3 MANDATORY | round4_validate_p_response.py；哈希见机器 JSON | CHECKED OUT-OF-SAMPLE CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE | NONE | FIG-Q1-R4-002 | M2 微小收益不稳，逐域误差仍需披露 |
| CAND-Q1-R4-TRANSFER-001 | Q1 | M1/M0 中心化 R0 RMSE 比 | 60M 0.888；1B 3.108 | 无量纲误差比 | NOT_APPLICABLE | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | A8/A9 256；A10/A11 64 | FROZEN M1 SHAPE TRANSFER | round4_validate_p_response.py；哈希见机器 JSON | CHECKED CANDIDATE — 1B TRANSFER FAILED | NONE | FIG-Q1-R4-003 | 跨规模只看中心化形状，不能称绝对 Loss 预测 |
| CAND-Q1-R4-SUPPORT-001 | Q1 | 验证 p 的经验支持分类 | A6/A8 各 2 IN、252 NEAR、2 OUT；A10 15/46/3 | 配比组 | OUT 组样本极少，无可靠误差区间 | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | A4 512 配比、A6/A8 同 p、A10 64 | TRAINING SUPPORT DIAGNOSTIC | round4_validate_p_response.py；哈希见机器 JSON | CHECKED CANDIDATE — NOT FINAL Q3 REGION | NONE | FIG-Q1-R4-004 | 经验近邻和凸包不是现实供给约束 |
| CAND-Q1-R4-CV-001 | Q1 | M1 A5 五折综合分数 | 0.750417 | 训练内归一化综合分数 | 五折均值；非独立置信区间 | EXP-Q1-PRESP-TRAIN-R4-20260924-v1 | A4/A5 512 训练运行 | M1 16D SIMPLEX-CONTRAST CANDIDATE | round4_train_p_response.py；训练指标 JSON 与 CV CSV 哈希锁定 | CHECKED TRAINING CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE | NONE | TABLE-Q1-R4-003 | 与 M0 1.001578 比较；验证结论另见 VAL-001 |
| CAND-Q1-R4-CV-002 | Q1 | M2 A5 五折综合分数 | 0.749715；α=0.01 | 训练内归一化综合分数及 ridge 参数 | 五折均值；非独立置信区间 | EXP-Q1-PRESP-TRAIN-R4-20260924-v1 | A4/A5 512 训练运行 | M2 REGULARIZED CANDIDATE | round4_train_p_response.py；训练指标 JSON 与 CV CSV 哈希锁定 | CHECKED TRAINING CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE | NONE | TABLE-Q1-R4-003 | 微小训练收益不足以升级，须看 A7 |
| CAND-Q1-R4-SELECT-001 | Q1 | M3 训练残差触发与激活 | trigger=false；activated=false | 预注册升级状态 | NOT_APPLICABLE | EXP-Q1-PRESP-TRAIN-R4-20260924-v1；VAL-Q1-PRESP-A6A11-R4-20260924-v2 | A4/A5 训练及冻结包；A7 不参与 M3 触发 | M3 NOT ACTIVATED | round4_train_p_response.py；冻结 bundle 与验证 JSON | CHECKED MODEL-SELECTION CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE | NONE | TABLE-Q1-R4-003 | 未拟合 M3，不能报告其留出收益 |
| CAND-Q1-R4-SELECT-002 | Q1 | M2 对 M1 A7/1M 留出收益 | R0 MSE 差 −0.0000504，bootstrap 2.5–97.5% [−0.000525,0.000401]；逐域标准化 MSE 差 0.000198，区间 [−0.000682,0.001063] | 原表 Loss² 与标准化 Loss² | 500 次成对运行 bootstrap 分位区间 | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | A6/A7 256 留出运行 | FROZEN M2 vs M1 | round4_validate_p_response.py；验证 JSON 与逐行 CSV 哈希锁定 | CHECKED OUT-OF-SAMPLE CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE | NONE | TABLE-Q1-R4-003 | 两层区间均跨零，按冻结停止规则不升级 M2 |

证据审查链为 RAW → CHECKED → VALIDATED，不合格为 REJECTED；当前 Phase 1 候选性可另标 CANDIDATE。只有经过后续相应 Gate 的 VALIDATED 结果可以支撑正式正文核心结论；每个结果 ID 同时追到配置、数据、响应、模型和代码版本。

Gate 2 状态同步：G2-SINGLE-001 / Verdict B 已生效，数值及 Result ID 不变。A7 用于冻结候选的预定验收与偏好判定，未用于结构/超参数搜索或参数回填；表列成对 bootstrap 区间不是完整选择过程校正的区间。VALIDATED FINAL RESULTS 仍为 NONE。

## Round5 Q2 — CHECKED CANDIDATES, Gate3 pending

| Result ID | Metric | Value | Evidence level | Run | Artifact under run | Status |
|---|---|---|---|---|---|---|
| CAND-Q2-R5-ND-001 | 五参数S1 | {"E": 1.6897975629393145, "A": 0.3539803206519287, "B": 1.2403055835398427, "alpha": 0.3399765819061934, "beta": 0.27987812854708494} | ATTACHMENT-INTERNAL ESTIMATED | EXP-Q2-ND-R5-20260924-v1 | summary.json | CHECKED CANDIDATE; NOT FINAL |
| CAND-Q2-R5-VAL-001 | 轨迹验证宏RMSE | LONO .000146888; forward .000111642; blocked .000114134 | ATTACHMENT-INTERNAL ESTIMATED | EXP-Q2-ND-R5-20260924-v1 | validation_metrics.csv | CHECKED CANDIDATE; NOT FINAL |
| CAND-Q2-R5-UNC-001 | 200整轨迹区间/稳定性 | 200成功; boundary 0; rank 5; condition 33.8347 | DIAGNOSTIC ONLY | EXP-Q2-ND-R5-20260924-v1 | cluster_bootstrap.csv | CHECKED CANDIDATE; NOT FINAL |
| CAND-Q2-R5-MARG-001 | N=1,D=100总Loss弹性 | N -0.050447; D -0.040100; substitution -1.258018 | ATTACHMENT-INTERNAL ESTIMATED | EXP-Q2-ND-R5-20260924-v1 | marginal_effects.csv | CHECKED CANDIDATE; NOT FINAL |
| CAND-Q2-R5-QUAL-001 | B7条件质量共同斜率 | -0.361995; negative 45/45; centered LONO .052964→.043679 | SEMI-SYNTHETIC CALIBRATED | SCEN-Q2-R5-20260924-v3 | quality_cell_slopes.csv | CHECKED CANDIDATE; NOT FINAL |
| SCEN-Q2-R5-SUB-001 | Q .5→.6, lambda=1条件替代 | N减少24.903%; D减少30.210%; 非真实节省 | SCENARIO-CONDITIONAL | SCEN-Q2-R5-20260924-v3 | quality_substitution_scenarios.csv | CHECKED CANDIDATE; NOT FINAL |
| CAND-Q2-R5-EXT-001 | B2/B4/B5中位中心化误差比 | .855084 / .436601 / .555135 | DIAGNOSTIC ONLY | SCEN-Q2-R5-20260924-v3 | external_shape_diagnostics.csv | CHECKED CANDIDATE; NOT FINAL |
| CAND-Q2-R5-EXT-002 | B9/B10外推 | 132元数据; 4个D=0; 128估算; 非验证真值 | SCENARIO-CONDITIONAL | SCEN-Q2-R5-20260924-v3 | B9_extrapolation_scope.csv | CHECKED CANDIDATE; NOT FINAL |
| CAND-Q2-R5-MIX-001 | 继承M1与136切向示例 | 1M限定; 60M部分; 1B失败; 支持未核 | EMPIRICALLY ESTIMATED / SCENARIO-CONDITIONAL | SCEN-Q2-R5-20260924-v3 | mixture_tangent_scenarios.csv | CHECKED CANDIDATE; NOT FINAL |

数值来源：06_results/raw/<Run>/<Artifact>，规格/代码/输入哈希见配置与summary。当前全项目14项Q1+9项Q2候选，VALIDATED FINAL仍0。

接管收口：原 9 项 Q2 Result ID、数值、Run 和证据级别不变；Q2 PROVISIONALLY CLOSED 只指受限研究包完成，不升格 VALIDATED FINAL。新增导航见 `03_models/modeling_phase2/round5/Q2_DELIVERY_FIGURE_TABLE_PLAN_v1.md`；Q3 准入见接口 A–J。QA 和字节修复不新增科学结果。Gate3 仍未通过。
