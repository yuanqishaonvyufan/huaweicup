# Q1 descriptive signal set v1

**状态：FROZEN BEFORE ROUND 3 COMPARISON。**完整 22 行字段合同见 [CSV](Q1_DESCRIPTIVE_SIGNAL_SET_v1.csv)，源表及脚本哈希见[机器记录](Q1_DESCRIPTIVE_SIGNAL_SET_v1.json)。依据 Round 1/2 已核语义和单位设置使用角色；角色不是新增的 Q2 变量资格。

| 描述使用角色 | 数量 | 处理原则 |
|---|---:|---|
| `CORE_DESCRIPTIVE_SIGNAL` | 5 | FineWeb 教育价值、流畅正类 margin、无广告正类 margin、cleanliness/readability 的连续诊断等级；只生成相对描述排序，argmax 另作编码敏感性 |
| `SENSITIVITY_ONLY_SIGNAL` | 12 | 推理/专业等级、QuRating 四面向及文本规则特征；保留上下文和域差，不强行赋统一质量方向或并入核心平均 |
| `EXCLUDED_FOR_NOW` | 2 | 词数和句数仅作长度/派生关系协变量，非单调质量分 |
| `UNKNOWN` | 3 | DSIR 三列单列比较冗余与长度关系；生成/尺度未明，不纳入主 Q |

Round 2 的 `DOWNSTREAM_ELIGIBILITY` 原样继承：17 `DESCRIPTIVE_ONLY`、5 `UNKNOWN`（DSIR 三列和两个 top n-gram 字段），**零项可直接作为 Q2 独立质量效应自变量**。因此两个 top n-gram 虽列为描述敏感性，仍有下游资格 UNKNOWN；这两套标签回答不同问题。原始 22 项和列表分量都保留在冻结处理输入，不因为主表示仅使用五项就把其余指标从题目分析中删除。
