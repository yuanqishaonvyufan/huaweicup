# Modeling Phase 1 state

**STATUS: ROUND 4 COMPLETE — LOCAL QA PASS；GATE 2 PASS WITH DOCUMENT-ONLY CORRECTIONS（B）；Q1 PROVISIONALLY CLOSED；ROUND 5 READY TO START / NOT EXECUTED（2026-09-24，Asia/Shanghai）。** Gate 1 [ACTIVE / CONDITIONAL PASS (ROUTE LEVEL)](../../02_analysis/consensus/GATE1_CONSENSUS_v1.md)。本状态取代本文件先前停在 Round 1 的总览描述；历史审计与运行产物不改。

| Workstream | 当前状态 | 证据与边界 | 下一阶段 |
|---|---|---|---|
| A — Q1 质量表示 | Full-22 画像 + 五核心多维分位向量，DQ0 仅描述摘要；Q1 PROVISIONAL FINAL CANDIDATE | A1–A3 共 272,505 物理行；确认语义冲突 0，仍有统计分歧/冗余/域反转/长度效应；无同运行 Q，TYPE E=0。见[模型规格](q1/round4/Q1_MODEL_SPEC_v1.md)与[结果](q1/round4/Q1_RESULTS_REPORT_v1.md) | Gate 2 已接受描述边界；不拟独立 Q 弹性 |
| A — Q1 p→13 域 Loss | M1 PROVISIONAL PREFERRED；正式训练 1、有效留出 1、失败隔离验证 1；M3 未触发 | A7/1M M1 R0 RMSE 0.2278 vs M0 0.2846，13/13 域改善；M2 无稳定额外增益；60M 部分中心化形状转移，1B FAIL；A6/A8 同 p，1M 仅 2/256 在训练凸包。见[正式验证](q1/round4/P_RESPONSE_VALIDATION_A6_A11_v1.md) | Gate 2 已接受限定用途；最终 Q3 可实施 p 域仍 DEFERRED |
| B — Q2 B1 baseline | 外部来源资格 NO；附件内部 B 级受限入口 ALLOWED FOR ROUND 5 | [双层裁决](../../01_data/audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md)；权威[Alert v4](../../01_data/audits/modeling_phase1/q2/EVIDENCE_ALERT_B1_SOURCE_METADATA_v4.md)仍 PARTIALLY RESOLVED；正式 N–D 拟合 0 | Q2 BASELINE MODELING AUTHORIZED；Round 5 先冻结合同再做附件内 N–D 与轨迹分组验证 |
| C — B8 | GENERATOR UNKNOWN / QUARANTINED / SEARCH PAUSED | 统计规则迹象不是生成机制证明，不进主参数 | 无新机制不重启 |

[Experiment Registry](../../05_experiments/EXPERIMENT_REGISTRY.md)记录 2 个非最终比较、4 个诊断、1 个正式训练、1 个有效验证和 1 个失败验证；[Results Registry](../../06_results/RESULTS_REGISTRY.md)有 14 项候选/诊断与选择状态；[Figure Registry](../../06_results/FIGURE_REGISTRY.md)有 4 张候选图。[Round 4 QA](../../10_review/MODELING_PHASE1_R4_QA_20260924.md) PASS，未重训或重跑验证；Q1–Q4 ACTIVE FINAL MODEL 与 VALIDATED FINAL RESULT 仍均为 0。

[Gate 2 共识 v1](../../02_analysis/consensus/GATE2_CONSENSUS_v1.md)已 ACTIVE，受限启动已放行；[Round 5 交接](../../09_handoff/GATE2_TO_ROUND5_HANDOFF_v1.md)已准备，当前未执行拟合。下一步见 [NEXT_ACTION.md](../../09_handoff/NEXT_ACTION.md)。
