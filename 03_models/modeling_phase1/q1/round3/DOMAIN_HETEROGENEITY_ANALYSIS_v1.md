# DOMAIN_HETEROGENEITY_ANALYSIS v1

**状态：A5 训练内 13 域结构诊断；R3 始终保留。**逐域数值见[机器 CSV](DOMAIN_HETEROGENEITY_RESULTS_v1.csv)，Spearman 矩阵见[相关表](Q1_13_DOMAIN_CORRELATION_v1.csv)，代码/原件哈希与 B=500 稳定性见[响应机器记录](Q1_13_DOMAIN_RESPONSE_METRICS_v1.json)。没有 A6–A11 留出结果、没有 p→Loss 拟合。

## 共同成分与相关结构

13 域共 78 对。[双口径复核](Q1_DOMAIN_SUPPORT_DIAGNOSTICS_v1.json)得到 **Pearson 负相关 24/78**，与 Phase 1 预注册依据一致；**Spearman 负相关 29/78**。两数不同是相关系数口径所致，不是文件矛盾。标准化后的 PC1 只解释 **22.78%**，前三维累计约 **55.51%**。PC1 对各域的载荷有近零及负值，说明“一项共同 Loss 因子”不足以覆盖全部领域。

以 `1−Spearman ρ` 的 average-linkage 给出的三组仅是探索性结构：组 1 为 arxiv、pubmed_central、pubmed_abstracts、uspto_backgrounds；组 2 为 freelaw、wikipedia_en、gutenberg_pg_19、pile_cc、hackernews；组 3 为 dm_mathematics、github、stackexchange、ubuntu_irc。组数不代表自然学科类别，也未通过独立留出验证，不能据此固定后续配比效应符号。

## 聚合遮蔽的具体方式

- 相对 R0 的两运行排序，单个域的逆序比例约 **29%–41%**，最高的 arxiv、freelaw、pubmed_abstracts、uspto_backgrounds 等接近或超过 40%。这是运行对的秩结构，不是已支持 p 干预的结果。
- 去掉 `dm_mathematics` 后的等权聚合与完整 R0 排序 Spearman 约 **0.912**，比去掉 pile_cc（约 **0.997**）变化明显；两域对 R0 方差贡献约 **21.3%/3.0%**。等权系数不意味着信息贡献相等。
- R2 对 github、pubmed_central、arxiv 等域的标准化重建残差均接近 1；pile_cc/gutenberg_pg_19 的残差低得多。R2 的低维轴集中解释了一部分域，不能以 PC1 改善代替 13 域同时改善。
- 同表平均 Loss 从 dm_mathematics 的约 **3.894** 到 ubuntu_irc 的约 **6.553**；可称“低/高平均原表 Loss”，但没有相同域内任务难度/语料熵校准，不直接称两域“容易/困难”。

后续 p 响应分析必须给出 13 域误差、效果方向和最差受损域；若综合响应改善而关键域可信恶化，不得用 R0/R1 掩盖。当前无 p 模型或留出验证，故只提供 R3 的训练内结构基线。
