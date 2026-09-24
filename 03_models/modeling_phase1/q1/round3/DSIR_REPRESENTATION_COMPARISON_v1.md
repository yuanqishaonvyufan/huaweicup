# DSIR_REPRESENTATION_COMPARISON v1

**状态：DIAGNOSTIC / DESCRIPTIVE ONLY；无 DSIR 质量方向或下游模型资格。**输入为已冻结 A1/A2/A3 处理记录；训练参考只取 A1 固定 ID 训练子集（40,926 行），域内 ID 重抽样 200 次，种子 `20260924`。数值与代码/输入哈希见 [机器结果](Q1_DESCRIPTIVE_QUALITY_METRICS_v1.json)；Round 2 [长度诊断](../../../../01_data/audits/modeling_phase1/q1/Q1_DSIR_LENGTH_DIAGNOSTICS_v1.csv)提供三来源/域别对照。

| 处理 | 实测比较 | 允许解释 |
|---|---|---|
| A 三列原值 | A1 训练参考的三对秩相关约 `0.9968–0.9990`；原值高度负偏且与词数的 Spearman 约 `−0.889/−0.892/−0.912` | 保留各目标域标签，但三列不能算三个独立维度，也不能原尺度直接平均进质量 Q |
| B 一个代表列 | 按预冻结“平均绝对秩相关最高”规则得到 `dsir_books`；三列信息近重复 | 可作目标相似性**描述代表**，不声称 books 是普遍更好的质量目标 |
| C 三列秩空间 PC1 | 首维解释 `99.839%`，载荷约 `0.5775/0.5775/0.5771`；200 次域内 bootstrap 首维份额 95% 范围约 `99.834–99.842%`，载荷余弦接近 1 | 强共同统计成分；其意义仍是未知口径的 DSIR 共同变化，不是经验证质量分 |
| D 长度/域调整残差 | 控制域和 `log1p(word_count)` 秩后，与词数的残差秩相关约 `−0.009/−0.009/−0.017` | 仅说明所用线性秩调整能去掉观测长度关联，不能证明残差具有质量语义；**不进入 DQ0 或 Q2** |

Round 2 的三来源比较还表明：DSIR 与词数在 A1/A2/A3 都强负相关；控制词数秩后三列之间仍高度同序。A/B/C 的统计冗余结论稳定，但上游 [RedPajama DSIR 类代码](https://github.com/togethercomputer/RedPajama-Data/blob/6d2cee9df2b0204dd2bcb00bf06b5a7b1d7432d7/app/src/core/quality_signals/importance_weights.py)并未被证实就是比赛数据的生成版本，目标分布与长度修正开关也未核。因此 D 不具备进入“真实质量”表示的语义条件。Round 3 对 DQ 候选的 DSIR 敏感性结论是：主表示完全不依赖 DSIR；若要增加目标相似度，只能分开给出 B/C 描述维度，不能借高解释率给它质量权重。
