# B1 Baseline Eligibility Audit v2 — Round 2 source trace

**Verdict: NOT YET ELIGIBLE.** **Alert stage: PARTIALLY RESOLVED.** 本文件只重审 Round 1 的 B1 来源资格，继承 [v1](B1_BASELINE_ELIGIBILITY_AUDIT_v1.md) 的 8×147 几何和算术诊断，不重跑或改写原始数据，也不拟正式 N–D Scaling Law。

| 必要条件 | Round 2 证据 | 结论 |
|---|---|---|
| 官方 B1 编号/路径/字段/哈希 | 可见《数据说明》、原件、`RAW_SHA256.csv` 与 Round 1 映射一致 | CHECKED |
| N/D 独立覆盖及轨迹依赖 | v1 已核完整 8×147 网格；只有八条推断规模轨迹 | GEOMETRY PASS；不是 1,176 独立运行 |
| 发布检查点标签 | 147 个 step 等于官方 154 个删去最早七个；本地索引三处 commit 与公开 API 一致 | PARTIAL：候选标签可核，B1 行来源尚未连接 |
| 模型变体、run、seed | B1 无相应字段或逐行原始日志 URI | UNKNOWN |
| `val_loss` 原始来源与统一验证语料/tokenizer | 表内无版本/语料/tokenizer/抽取配方；`ppl` 算术一致不替代来源 | **FAIL — 阻断正式基线** |
| `precision`、`wd`、`lr` 语义 | 与对应公开训练说明/配置有具体差异；尚不知训练字段还是附加元数据 | UNKNOWN_OR_AUGMENTED；不进基线 |

释放条件以 [B1 来源追踪](B1_PROVENANCE_TRACE_v1.md)的三档规则为准。若取得能核实关键 Loss、tokenizer、八条轨迹及 checkpoint 对齐的证据，可把无法追溯但不参与基线的 `precision/wd/lr` 标为附加或未知并排除，再重审至 `RESOLVED FOR BASELINE USE`。在当前证据下 B1 正式基线继续暂停；N/D 几何只保留为审计结果。不得把该结论表述为已经证明 `val_loss` 伪造。
