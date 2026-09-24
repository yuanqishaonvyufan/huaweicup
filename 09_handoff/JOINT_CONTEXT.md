# JOINT_CONTEXT

## 当前共同决定

[Gate 2 共识 v1](../02_analysis/consensus/GATE2_CONSENSUS_v1.md)为 ACTIVE，Decision ID `G2-SINGLE-001`，Verdict **B — PASS WITH DOCUMENT-ONLY CORRECTIONS — ROUND 5 MAY START**。文档修正已完成，P0=0。Round 4 COMPLETE / QA PASS；Q1 PROVISIONALLY CLOSED；M1 PROVISIONAL PREFERRED Q1 p-RESPONSE MODEL。Round 5 READY TO START / NOT EXECUTED；Q2 BASELINE MODELING AUTHORIZED；Q3/Q4 NOT STARTED。Q1–Q4 ACTIVE FINAL MODEL 与 VALIDATED FINAL RESULT 均为 0。

Discovery 共识与 [Gate 1 共识](../02_analysis/consensus/GATE1_CONSENSUS_v1.md)的路线边界继续有效。本轮按用户要求一次性裁决，未请求另一账号审查、未重训或重跑验证。Round 4 QA 与 Gate 2 预审包 v1.1 是历史证据；当前授权由 Gate 2 共识和[Round 5 交接](GATE2_TO_ROUND5_HANDOFF_v1.md)控制。

## 来源与粒度

官方任务取用户提供 DOCX 和《数据说明》可见正文：Q1 A1–A3 全量、A4/A5 配比、A6–A11 检验；Q2 B1 主表及分级数据；Q3 外生 context；Q4 C8 与桥接。原始 `01_data/raw/real_attachments/` 的 2,012 文件只读，OFFICIAL_MAPPING_FIRST 有效，A18 不代替 A2/A3。PDF 96 段近白色页边干扰继续[隔离](../01_data/audits/modeling_phase1/DOCUMENT_INTERFERENCE_AUDIT_v1.md)。

A1–A3 共 272,505 物理行、261,086 不同 ID；文档质量与 A4/A5 配方运行没有同运行质量键，`NO_MATCHED_Q`，TYPE E=0。Full-22 保留全部画像角色，五 CORE 用于多维描述，DQ0 仅透明摘要；确认语义冲突 0，统计分歧、域反转、冗余和长度/尺度影响仍存在。代码/非英文面效度反例和编码敏感性不能隐藏。

## Q1 限定结论

冻结的 A4/A5 训练有 17 份配比、16 自由坐标，M1 为暂定首选。A7/1M R0 RMSE 0.2278 vs M0 0.2846，13/13 域改善；M2 无稳定额外收益，M3 未触发。模型结构/超参数只用训练确定；A7 参与冻结候选的预定验收与偏好判定，不称完全未参与选模的最终测试。R0 统一报告 + R3 十三域并行强制保留。

60M 只见部分中心化形状转移，1B 明显失败，规模不变性不成立是现有模型的经验含义，尚无已识别的配比×规模机制。A6/A8 同一 p，1M 凸包覆盖 2/256、2 IN/252 NEAR/2 OUT；经验支持与实际供应分开，禁止 full-simplex deployable optimization 宣称。[接口 v1.1](../02_analysis/consensus/Q1_TO_Q2_INTERFACE_v1_1.md)仅传 TYPE A 描述、B 领域/配比证据、C 条件情景、D 支持约束，TYPE E **0**。

## B1/B8 与 Round 5

B1 附件内部 **B 级受限 baseline 已获 Round 5 入口**；外部经验 provenance 未恢复，权威[Alert v4](../01_data/audits/modeling_phase1/q2/EVIDENCE_ALERT_B1_SOURCE_METADATA_v4.md)仍 PARTIALLY RESOLVED。8×147 的内部数值一致性只支持附件 Loss 标尺建模。只用 N、D、val_loss，隔离异常元数据；八条 N 轨迹是留出分组单位，不把 1,176 检查点当独立样本；须固定 D 段外推和失败 fallback。A/B 绝对 Loss 不池化，不拟独立 Q 系数。

B8 保持 GENERATOR UNKNOWN / QUARANTINED / SEARCH PAUSED。正式 N–D 拟合 0；下一轮按[交接](GATE2_TO_ROUND5_HANDOFF_v1.md)先冻结合同再建受限基线，当前未执行。

## 证据登记

[Experiment Registry](../05_experiments/EXPERIMENT_REGISTRY.md)仍为 1 次正式 Q1 训练、1 次有效验证 v2、1 次失败隔离验证 v1，另有既有 2 非最终比较/4 诊断；[Results Registry](../06_results/RESULTS_REGISTRY.md)14 项候选/诊断与选择状态，[Figure Registry](../06_results/FIGURE_REGISTRY.md)4 张候选图。[Round 4 QA](../10_review/MODELING_PHASE1_R4_QA_20260924.md)原 PASS 保留；Gate 2 通过没有晋升最终模型或最终论文结果。
