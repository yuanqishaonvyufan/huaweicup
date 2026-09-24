# PROJECT_STATE

## 当前阶段与 Gate

ROUND 4：**COMPLETE — QA PASS**。Q1：**PROVISIONALLY CLOSED**。GATE 2：**PASS WITH DOCUMENT-ONLY CORRECTIONS（Verdict B）— ACTIVE**，依据 [GATE2_CONSENSUS_v1](../02_analysis/consensus/GATE2_CONSENSUS_v1.md)，Decision ID `G2-SINGLE-001`。文档修正已完成，P0=0。ROUND 5：**READY TO START / NOT EXECUTED**。Q2：**BASELINE MODELING AUTHORIZED**。Q3/Q4：**NOT STARTED**。

DISCOVERY COMPLETE；[Gate 1 共识](../02_analysis/consensus/GATE1_CONSENSUS_v1.md)继续 ACTIVE / CONDITIONAL PASS (ROUTE LEVEL)。本次 Gate 2 为用户授权的单次裁决，未开启 Modeling Round、未调用另一账号复审。Round 4 [QA](../10_review/MODELING_PHASE1_R4_QA_20260924.md)和[预审包 v1.1](../10_review/GATE2_PRE_REVIEW_PACKAGE_v1_1.md)保留原形成时状态；本页与 Gate 2 共识记录当前状态。

## Q1 与接口

M1：**PROVISIONAL PREFERRED Q1 p-RESPONSE MODEL**；无 ACTIVE FINAL MODEL 晋升。质量主线是 Full-22 画像与五核心多维描述，DQ0 仅 scalar descriptive summary，确认语义冲突 0。A7/1M M1 R0 RMSE **0.2278** vs M0 **0.2846**、13/13 域改善；M2 无稳定额外收益，M3 未触发。R0 报告 + R3 逐域强制并行；60M 仅部分 centered-shape transfer，1B transfer failure。

结构、超参数及验收门槛在 A6–A11 前冻结；A7 用于冻结候选的预定比较与偏好判定，不能写成完全未参与选模的最终测试集。1M 仅 2/256 位于观测凸包，2 IN/252 NEAR/2 OUT；禁止 full-simplex deployable optimum，最终 Q3 可实施域仍 DEFERRED。

[Q1→Q2 v1.1](../02_analysis/consensus/Q1_TO_Q2_INTERFACE_v1_1.md)已获限定用途接受：TYPE A descriptive quality evidence；TYPE B domain/composition response evidence；TYPE C quality scenarios；TYPE D support constraints；**TYPE E=0 independently estimable quality variables**。无 matched Q，独立质量系数不估。

## B1 与后续范围

B1：**ATTACHMENT-INTERNAL RESTRICTED BASELINE ALLOWED FOR ROUND 5**。外部经验来源仍未通过，权威[Alert v4](../01_data/audits/modeling_phase1/q2/EVIDENCE_ALERT_B1_SOURCE_METADATA_v4.md)继续 PARTIALLY RESOLVED；[双层资格](../01_data/audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md)的内部 8×147 一致性支持附件标尺下条件 N–D 建模。核心只用 N、D、val_loss，异常元数据隔离，A/B 绝对 Loss 不池化，八条轨迹分组与 D 段检验须预先固定。正式 N–D 拟合仍为 **0**。

B8 GENERATOR UNKNOWN / QUARANTINED / SEARCH PAUSED，不入主参数。Q3 现实供给约束、Q4 桥接/能力模型均未启动；Weak Bridge 仅限 Pythia 且待验证，Strong 未放行。

## 运行与结果

[Experiment Registry](../05_experiments/EXPERIMENT_REGISTRY.md)仍为 2 非最终比较、4 诊断、1 正式 Q1 训练、1 有效留出验证、1 失败隔离验证；本次无新模型 Run。Q1 训练 `EXP-Q1-PRESP-TRAIN-R4-20260924-v1`，有效验证 `VAL-Q1-PRESP-A6A11-R4-20260924-v2`，失败 v1 不用于选择。[Results Registry](../06_results/RESULTS_REGISTRY.md)14 项、[Figure Registry](../06_results/FIGURE_REGISTRY.md)4 图保持 CHECKED/CANDIDATE；Q1–Q4 **ACTIVE FINAL MODEL=NONE，VALIDATED FINAL RESULTS=NONE**。

## 下一行动

执行[Gate 2→Round 5 交接](GATE2_TO_ROUND5_HANDOFF_v1.md)：下一轮先冻结 B1 受限基线规格与训练/验证合同并登记 Run，再启动已获准的 Q2 baseline。当前停在 READY，尚未实际拟合。原始 2,012 附件只读，OFFICIAL_MAPPING_FIRST 和 PDF 页边干扰隔离持续有效。

更新时间：2026-09-24（Asia/Shanghai）。
