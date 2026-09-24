# Q1_DESCRIPTIVE_QUALITY_CANDIDATES v1

**状态：四种非最终 DQ 候选；无经验证的真实质量标量。**计算定义冻结于 [Round 3 合同](../Q1_ROUND3_COMPARISON_CONTRACT_v1.md)；22 项使用角色见[信号集](../Q1_DESCRIPTIVE_SIGNAL_SET_v1.csv)。原始 A1/A2/A3 共 272,505 行均有处理输出，去重分析为 261,086 ID；冻结输入哈希见 `01_data/processed/modeling_phase1/round3/INPUT_MANIFEST_v1.json`。

| 候选 | 输出 | 语义与限制 |
|---|---|---|
| DQ0 | 五项方向候选按 A1 训练参考逐项 ECDF 后等权平均 | 透明的相对描述排序，0–1 仅相对训练参考；不是 22 项“真实质量”或 Q2 弹性 |
| DQ1 | 同五项训练标准化秩的 PCA 各维；PC1 与 DQ0 正向对齐 | 显示共变结构；PC1 不能默认覆盖全部质量面向，其他 PC 不统一赋优劣方向 |
| DQ2 | A1 训练参考五信号 Spearman 平均链接聚类的 k=2 与 k=3 等权组内均值向量 | 多维结构候选；组数/分组仅统计探索，必须核域别/扩展集稳定性，不事先命名“语言质量”等维度 |
| DQ3 | 按 A1 各域参考分别 ECDF 后五项等权平均 | 只比较域内排序；域间位置差被构造性消除，不宜直接作跨域质量比较 |

每个候选均保留五项原始/编码后分量及 17 项非核心指标的上下文角色。`DSIR_REPRESENTATION_COMPARISON_v1` 不把 DSIR 加入主分数；`LIST_SIGNAL_REPRESENTATION_COMPARISON_v1` 比较 logits 压缩。逐物理记录的候选值见 [结果 CSV.gz](Q1_DESCRIPTIVE_QUALITY_RESULTS_v1.csv.gz)，结论须连同[比较报告](Q1_DESCRIPTIVE_QUALITY_COMPARISON_v1.md)阅读。
