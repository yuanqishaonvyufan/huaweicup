# Q1_13_DOMAIN_RESPONSE_COMPARISON v1

**P1-1 状态：PROVISIONAL PREFERRED CANDIDATE = R0（透明原始 Loss 基线）+ 强制 R3 逐域分析。非 FINAL RESPONSE。**实验 `MC-Q1-RSP-R3-20260924-v1` 严格沿用 [已冻结 P1-1](../P1_1_13_DOMAIN_RESPONSE_PREREG_FINAL_v1.md) 的 R0–R3 定义，A5 512 个训练运行的全部 13 域 Loss 均可计算；未读 A6–A11 留出 Loss，未拟 p 响应。每运行 [R0/R1/R2 与 R3 原值](Q1_13_DOMAIN_RESPONSE_RESULTS_v1.csv)、[候选摘要](Q1_13_DOMAIN_RESPONSE_CANDIDATE_SUMMARY_v1.csv)和[机器指标/代码哈希](Q1_13_DOMAIN_RESPONSE_METRICS_v1.json)可复核。

| 候选 | 训练内证据 | 当前判定 |
|---|---|---|
| **R0** 原表 13 域等权 | 原 Loss 单位，定义最清楚；R0 对 R1 的秩相关 `0.924`、最佳十分位交集 `71.2%`。但等权不等于等方差贡献，`dm_mathematics` 对 R0 方差贡献约 `21.3%`、`ubuntu_irc` 约 `13.9%` | **PREFERRED CANDIDATE for reporting baseline**；必须附 R3，不能单独得出逐域改善结论 |
| **R1** A5 训练均值/标准差后等权 | B=500 运行重抽样的固定 512 行得分秩相关下 2.5% 分位约 `0.99948`；减少原尺度波动主导 | 可保留为尺度敏感性；小方差域和噪声可能被放大，不可直接当 B1 绝对 Loss |
| **R2** A5 z 的 PC1 | PC1 解释 `22.78%`、前三维累计约 `55.51%`；B=500 PC1 份额约 `21.64–24.78%`，载荷余弦约 `0.917–0.998` | 共同成分**存在但不足以代表 13 域**；R0–R2 秩相关仅 `0.545`、最佳十分位交集仅 `36.5%`，不升主响应 |
| **R3** 原始 13 维向量 | 逐域方向、偏差、受损域与不确定性可查；原单位保留 | **MANDATORY**，无论报告 R0/R1/R2 的哪一项均不删除 |

R2 对 pile_cc、gutenberg_pg_19、hackernews、wikipedia_en 有较大正载荷，对 arxiv/pubmed_central 的载荷接近零或为负；其“共同”方向并不能代替所有领域。R0/R1/R2 原始 RMSE 因单位不同不直接排名。R0 的保留主要源于可解释性与 P1-1 预先规定的透明基线地位，**不是**因为训练拟合优于其他响应。A5 仅作训练内响应结构比较；没有 p 扰动因果结论或留出验证。

[逐域异质性报告](DOMAIN_HETEROGENEITY_ANALYSIS_v1.md)为本结论的必需伴随文件。后续若选最终主响应，须依 P1-1 建立 `Q1_RESPONSE_SELECTION_REPORT_v1.md`，并在冻结选择后经过 A6–A11 检验及 Gate 2；本报告不代替该步骤。
