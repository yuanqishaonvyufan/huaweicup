# P0_CLOSURE_REPORT_v1

| Field | Record |
|---|---|
| P0 ID | P0-1 — Q/p 秩检验结果缺少输出决策树 |
| Original issue | JOINT_F_PROBLEM_REVIEW_v1.md §2 指出 v1 整合稿虽有代数秩条件，却未把秩亏、弱识别、支持不足、样本外区分及半合成来源映射到 Q2/Q3 行动。 |
| Why blocker | 当时数据审计即使得到条件数、残差化 Q 或满秩结果，也无法给出可追踪的模型输入和允许措辞；复核稿又同时写 P0 BLOCKER 与 READY FOR DATA AUDIT，违反项目门槛。 |
| Correction | 01_data/IDENTIFIABILITY_AUDIT_SPEC.md 定义运行粒度、字段、合法 p 参数化、泄漏/配对/确定性构造/秩/精度/支持/留出/来源分级与分支输出；04_code/utils/identifiability_decision.py 消费审计摘要并产生机器可读 Q2/Q3_ACTION；JOINT_F_PROBLEM_SYNTHESIS_v1_1.md §5 纳入完整决策树和 P1 使用前合同。 |
| Decision tree | Step 0 来源/目标泄漏 → A 同运行配对与独立变化 → B Q=f(p,q_fixed) 的结构别名 → C 合法 simplex 设计秩 → D 噪声校准的弱识别/共同支持 → E 同切分样本外增益 → F 半合成证据叠加；每步都有主分支、允许/禁止主张和 fallback。 |
| Fallback | 联合 p/q 响应（不称独立 Q 效应）；固定 p 或 Q 的条件情景；B6–B8 半合成敏感性另列；真实数据若无法识别，放弃独立质量弹性点估计。 |
| Remaining uncertainty | 实际 A4/A5 配方级 Q_r 是否存在、矩阵秩与精度、真实独立运行簇和留出增益均未知；所有 P1-1 至 P1-6 仅完成使用前设计，不代表实测通过。 |
| Needs data? | YES。后续正式 Data Audit 才能决定实际 identifiability branch；本轮未读取配方级质量数据做秩、拟合或验证。 |
| Status | CLOSED — DESIGN LEVEL；AWAITING EMPIRICAL AUDIT；AWAITING OPUS FINAL CHECK。只关闭“缺决策树”的设计缺陷，不宣称 Q/p 在真实数据中可独立识别；Opus 快速复核前不得进入正式 Data Audit 或最终 CONSENSUS。 |

## 设计级核验

已用非真实逻辑摘要覆盖分支器的 14 个路径：来源未知、目标泄漏、无配方级 Q、固定 q 结构别名、未测秩、其他秩亏、混合来源未分层、未校准精度、弱识别、支持不足、未做留出、无增量预测、半合成唯一支持、真实配对的稳定预测关联。每一输出含 Q2_ACTION、Q3_ACTION、fallback 与禁止过度结论；额外确认“声称真实稳定增益但缺少留出指标证据 ID”会被拒绝。未访问 A/B/C 原始数据，也未运行正式实验。

后续 Opus Final Check 只需核逻辑覆盖、fallback、P1 合同与状态标签。若发现分支有遗漏，重开 P0-1 并保持 CONDITIONAL HOLD。
