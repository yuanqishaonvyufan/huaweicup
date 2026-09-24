# Gate 1 Round B evidence citation errata

状态：**CHECKED SOURCE CORRECTION FOR ROUND C**。本记录只核 Opus Round B 与 Phase 1 v2 原始证据的直接冲突；不改写 `GATE1_OPUS_EVIDENCE_REVIEW_v1.md` 原件，不重新运行完整 Phase 1，也不拟合 Loss–Benchmark 最终映射。来源：[Phase 1 v2 报告](../01_data/audits/phase1/ROUTE_DECISION_AUDIT_PHASE1.md)、[指标与原始哈希](../01_data/audits/phase1/route_audit_metrics.json)、[7 点定向核查](../01_data/audits/phase1/bridge_pythia_focus_check.json)。

| Opus Round B 表述 | 可核事实 | 对路线的影响 |
|---|---|---|
| §3 E03 把 B1 写为约 154,000 条轨迹、引用 AUDIT-03 | B1 原表 **1,176** 行，8 个 N 水平各 147 检查点；相关证据在 AUDIT-02。`[1,log N,log D]` 简约设计秩 3，不能把检查点当 1,176 个独立训练簇 | 保留来源内 N–D **baseline candidate**，删去“样本量充分/稳健已证”的强措辞；后续按整轨迹/规模块留出 |
| §3 E04 把 B7 写为 1,620 行、引用 AUDIT-04 | B7 **450** 行，B6 **360** 行全嵌于 B7；B8 为 1,704 行。相关证据在 AUDIT-03 | B6/B7 仍为同一 E3 半合成来源，校准机制不透明的警示应更强 |
| §3 E11/E12 引用 AUDIT-08/AUDIT-09 | 本项目仅 AUDIT-01 至 AUDIT-07；C7 长度是 **AUDIT-05**，桥接是 **AUDIT-06** | 仅修正可追溯引用；不改 C7 外生或 Strong 不放行 |
| §4 把 `NO_MATCHED_Q` 解释为“Q 列落入 p 设计空间” | 当前真实 A4/A5 **没有同运行 Q 列**，故 `X_full` 未构造；只有将来按固定域 q 定义 `Q_eff=pᵀq` 时，条件性结构别名才成立 | 明确区分“缺配对 Q”和“若构造固定 q 则别名”，不得用未计算的秩作经验结论 |

**Bridge 定向复核**：C6 的 7 个 High Pythia 点均与 B1 在相同 N,D 的末检查点 `val_loss` 完全一致；七点 D 均为 299.893B tokens，N 为 0.162405–11.965825B。仅对这 7 点做描述性检查，`Val_Loss` 与 `LB_Average` 的 Pearson 相关约 −0.397、Spearman 约 −0.607，六项任务的方向并不一致。这些数值不是预注册拟合或样本外验证，不足以宣称已建立可预测的桥接；可把 **WEAK BRIDGE — PYTHIA-CONFINED, PENDING VALIDATION** 作为受限候选状态，Strong 与跨族运输均未放行。若后续留出/误差校准失败，回落 `NO RELIABLE BRIDGE`。

本次纠错不推翻 Opus 的两项 MODIFY、一项 DEFER 的研究方向；Round C 应在 v1.1 中改证据引用、收紧 B1 与桥接强度，并将更正交给 Opus 最终短审确认。
