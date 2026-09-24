# QUALITY_CONFLICT_CANDIDATES v1

**状态：PROVISIONAL DEFINITIONS AND TARGETED DIAGNOSTICS；无最终冲突判定或质量评分。**对应运行 `AUDIT-Q1-SEMANTICS-CONFLICT-20260924-v1`。逐条分类与 Round 1 编号保存在 [42 项候选 CSV](QUALITY_CONFLICT_CANDIDATES_v1.csv)，数值/分层/敏感性见 [稳定性 CSV](Q1_CONFLICT_STABILITY_v1.csv)。

## 操作定义

仅在两指标均有来源支持的共同“较高较好”诊断方向时，用同一分析层 `d` 的非缺失、不同 `id` 记录计算中秩百分位 `u_j(i,d)=(midrank_j(i,d)−0.5)/n_d`。主阈值 `q=0.80`，敏感性 `q=0.75,0.90`。**极端统计分歧率**为

`C_jk,d(q)=n_d^(-1) Σ_i 1{[u_j≥q 且 u_k≤1−q] 或 [u_k≥q 且 u_j≤1−q]}`。

第二指标是两信号对文档对的**排序逆序比例** `D/(C+D)`，只在两信号均不并列的可比较文档对中计算；程序用 Kendall tau-b 与精确并列计数恢复逆序数。两个指标都描述**统计分歧**，不自动证明两个质量目标存在语义冲突。极端率的 95% Wilson 区间以不同 `id` 为单位、条件于已计算的分位界；它不覆盖分位界再估计、数据采样偏差或模型误差。

分别报告 A1 七域、A2/A3 全表，以及扣除 A1 重叠 ID 后的 A2/A3 新记录；`UNIQUE_ALL` 只包含 261,086 个不同 ID。A1 的 arxiv/github 重叠记录不作独立复现。A1 book 仅 171 行，区间宽，不能以其单独判方向。

## 六类标签与本轮结果

| 标签 | 判据与当前用法 | 42 项中的数量 |
|---|---|---:|
| `SEMANTIC CONFLICT` | 已证明两个指标对应的质量目标/用途存在真实取舍，且统计表现支持；**本轮无一项达到** | 0 |
| `STATISTICAL DISAGREEMENT` | 方向候选的分位或排序不一致，但无已证实的目标取舍 | 7 |
| `REDUNDANCY` | 同源算法或文本派生量高度重合的候选 | 5 |
| `SCALE ARTIFACT` | 长度、分母或原始尺度可能造成的关联；当前均为待确认机制候选 | 12 |
| `DOMAIN-SPECIFIC REVERSAL` | 至少两个独立/分层样本量 ≥1,000 的分析层，Spearman 分别 ≥0.1 和 ≤−0.1；仍只描述符号反转 | 3 |
| `UNRESOLVED` | 方向、尺度或 PC1 残差含义不足以分类为真实质量冲突 | 15 |

其中 `QCI-025`（readability 对无广告 margin）、`QCI-026`（cleanliness 对无广告 margin）、`QCI-027`（FineWeb 教育价值对无广告 margin）出现统计关联的域别符号反转；该类别不是因变量效果、更不是语义冲突。`|ρ|≥0.1` 是查看定向结果后确定的**探索性分类界**，未预注册，也不能用作后续模型选择门槛。A1 `QCI-025` 的 `q=.80` 极端分歧率为 8.811%，A2 新 ID 为 13.332%，A3 新 ID 为 8.676%。A1 `QCI-027` 约 6.016%，A2/A3 新 ID 约 9.911%/9.469%。`QCI-034`（cleanliness 对 readability）在 A1 为 0.486%，但 A2 新 ID 为 6.557%，说明即使同一模型评级族也不能直接假设跨域稳定。

DSIR 三列在原尺度近完全同序且长度关系强，归入冗余候选；DSIR 与词数等负相关归入**可能的尺度伪象**而非质量负向冲突。PRRC/二分类列表的 margin、softmax 期望等级与 `argmax` 变换不同，当前分歧率基于 Round 1 连续诊断表示；正式描述 Q 候选比较前还应做列表表示敏感性，不能拿本表直接赋权。

## 使用限制

本表没有选最终 Q，没有借 A4/A5 或 A6–A11 Loss 定方向，也没有建立同运行 Q。后续若主张 `SEMANTIC CONFLICT`，须补目标语义、适用域、方向和稳健性证据；若只是数值负相关，应保留 `STATISTICAL DISAGREEMENT` 或 `UNRESOLVED`。阈值是预先定义的诊断尺度，不能被解释为自然质量界或题面规定。
