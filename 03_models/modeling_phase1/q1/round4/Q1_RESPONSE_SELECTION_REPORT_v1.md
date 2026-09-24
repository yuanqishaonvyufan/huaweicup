# P1-1 13 域响应选择报告 v1

**判定：R0 为 PROVISIONAL PRIMARY REPORTING RESPONSE，R3 为 MANDATORY DOMAIN HETEROGENEITY；R1/R2 保留敏感性/结构角色。GATE 2 ACCEPTED FOR Q1 PROVISIONAL CLOSURE。**严格继承[使用前预注册](../P1_1_13_DOMAIN_RESPONSE_PREREG_FINAL_v1.md)，未改 R0–R3 数学定义或编号。Round 3 比较 Run `MC-Q1-RSP-R3-20260924-v1` 只用 A5 512 训练运行，Round 4 正式训练 `EXP-Q1-PRESP-TRAIN-R4-20260924-v1` 与有效留出 `VAL-Q1-PRESP-A6A11-R4-20260924-v2`；首次验证 v1 失败隔离，不用其数值。A4/A5/A6–A11 原始哈希、处理/模型/响应版本和代码哈希见各机器 JSON。

**选择理由：**R0 原表 13 域等权，单位与解释最透明；R1 标准化改变尺度且不得直接当 B1 绝对 Loss；R2 的训练 PC1 只解释 22.78%，R0/R2 排序相关 0.545，若主用会遮蔽多数域。Round 4 模型先逐域预测再聚合 R0，A7/1M 的 M1 在 R0 和全部 13 域均比 M0 降低误差，避免仅聚合通过；R3 因此持续并行。A7 的 R1/R2 投影仅作预注册敏感性，不据此调 R0 权重。A9 仅部分转移、A11 失败，故不宣称跨规模最终主响应已验证。

**候选范围：**R0 是 Q1 附件 A 的 1M 同尺度报告基线，不是现实用途权或 Q2/B1 通用标尺；所有模型/论文图表须同时给 R3 逐域错误、最差受损域和规模/支持限制。A12–A15 为估算外推，不是独立真值。Gate 2 本次只接受受限暂定报告结构，仍不能写 `RESOLVED FINAL RESPONSE` 或 `ACTIVE FINAL MODEL`。
