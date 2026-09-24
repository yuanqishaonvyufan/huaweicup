# LIST_SIGNAL_REPRESENTATION_COMPARISON v1

**状态：训练内编码敏感性；不冻结最终列表压缩。**依据 [Meta-rater 字段说明](https://huggingface.co/datasets/opendatalab/SlimPajama-Meta-rater/blob/main/README.md)比较 `argmax`、连续 logit margin、sigmoid 概率、PRRC softmax 期望等级及 QuRating 四分量。逐来源结果见[机器 CSV](LIST_SIGNAL_REPRESENTATION_RESULTS_v1.csv)，A1/A2/A3 原件不变。19 个含非有限值的 PRRC 六级列表在相应比较中列为缺失，不插补。

- `fineweb_edu` 只有一个列表元素，提取该值不涉及分量权重。二分类 `fluency_en` 和 `ad_en` 的 sigmoid 概率与正类−负类 margin 严格单调，秩信息相同；`argmax` 则只留两档。A2 的流畅/无广告 `argmax` 多数类占比分别约 **99.20%/99.91%**，几乎不保留该域内连续排序。A3 的无广告多数类占比约 **99.69%**。
- PRRC 六级的 `argmax` 是数据卡示例推荐的类别表示，softmax 期望等级是 Round 1 的连续诊断候选；二者不等价。A2 cleanliness 的 `argmax` 多数类约 **99.13%**，期望等级对 `argmax` 的 Spearman 约 **0.160**，主要反映严重并列，不能据此说标签错误。A1 同一比较约 **0.939**，说明编码敏感性有域差。
- QuRating 的 style、required expertise、facts/trivia、education 四分量分别保留。四分量对“简单均值”的秩相关在 A1 为约 **0.674–0.854**，A2 为 **0.513–0.887**，并非同一量；没有共同权重或单调质量方向证据，不把均值作为核心指标。
- 五核心信号的 DQ0 连续编码与 `argmax` 敏感性分数，Spearman 在 A1/A2 新 ID/A3 新 ID 约为 **0.923/0.497/0.873**；固定 ID 破并列后的最佳十分位重合约 **62.9%/30.9%/72.4%**。该重合使用 ID 哈希处理类别并列，是诊断约定，不是唯一自然的类别前十分位。

本轮保留连续编码作为 DQ0 的**候选操作定义**，因为其可用于比较排序；`argmax` 是不可省略的来源语义敏感性。A2 的大幅编码差异阻止将 DQ0 升级为稳定的最终标量 Q，后续若调整编码必须新立版本并重新比较，不能用 Loss 选表示。
