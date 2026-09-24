# Q1 质量信号语义与量纲定向核查 v1

**Audit Run:** `AUDIT-Q1-SEMANTICS-CONFLICT-20260924-v1`。**状态：CHECKED TARGETED AUDIT；无最终 Q、无正式模型拟合。**本轮复用 Round 1 已确认的 A1/A2/A3 官方编号、实际路径、字段粒度和 SHA-256；执行脚本 `04_code/data_audit/modeling_phase1_round2_q1.py` 在读取前再次校验原始哈希和《数据说明》哈希。`Q1_ROUND2_DIAGNOSTICS_v1.json` 记录本次代码/映射哈希、运行时间与输出行数。原件保持只读。

## 1. 22 项信号的使用资格

[逐项证据表](QUALITY_SIGNAL_SEMANTICS_v1.csv)覆盖全部 22 项，新增 `DOWNSTREAM_ELIGIBILITY`。该字段指**当前项目中作为下游 Q2 等模型自变量的资格**，不等于某个数值方向是否有描述价值。当前 17 项为 `DESCRIPTIVE_ONLY`、5 项为 `UNKNOWN`（DSIR 三列及两个 top n-gram 字段）；`POTENTIALLY_MODEL_ELIGIBLE` 与 `NOT_ELIGIBLE` 是保留状态，但本轮没有任何信号取得前者。所有 22 项均受 `NO_MATCHED_Q` 约束，不得变成独立 Q 弹性。

依据 [Meta-rater 数据卡](https://huggingface.co/datasets/opendatalab/SlimPajama-Meta-rater/blob/main/README.md)的语义，`fineweb_edu`、流畅正类 margin、无广告正类 margin、`modernbert_cleanliness`、`modernbert_readability` 仍是 **5 个方向为正的候选**；这不是最终赋权。其余 17 项没有获准的通用“越高越好”方向：专业/推理复杂度依用途而变，DSIR 是目标域相似性，词数/熵/文本形态是派生特征，QuRating 含四个不同面向。公开卡片可说明字段族，但不能证明比赛摘录的每项生成/校准版本。

列表指标需保留原分量。数据卡建议二分类和 PRRC logits 以 `argmax` 取类别；Round 1 的二分类 margin 与 PRRC softmax 期望等级只是连续诊断表示。本轮[压缩敏感性表](Q1_LIST_ENCODING_SENSITIVITY_v1.csv)显示这些表示的秩相关因来源而异，例如 A2 的 `modernbert_cleanliness` 期望等级与 `argmax` 的 Spearman 约 0.160，而 A1 约 0.939；大量类别并列会压低相关，不能单凭此数宣布哪种表示“错误”。QuRating 四分量仍不能以未经论证的简单均值当最终指标。Round 1 记录的 19 个非有限六级列表值保持不可用标记，不插补、不改原件。

## 2. DSIR 的长度效应和重复信息

[定向统计表](Q1_DSIR_LENGTH_DIAGNOSTICS_v1.csv)给出三来源及 A1 各域的结果。三项 DSIR 与 `rps_doc_word_count` 的 Spearman：A1 为 −0.889 至 −0.913，A2 为 −0.778 至 −0.801，A3 为 −0.956 左右。三项 DSIR 彼此的原始 Spearman 在 A1 为 0.9968–0.9990；控制词数秩后的偏秩相关仍为 0.9884–0.9953（A2/A3 也均大于 0.983）。因此**长度强共变与三列近重复同时存在**；“只由长度造成”或“三项独立质量证据”都没有得到支持。

[RedPajama 上游重要性代码](https://github.com/togethercomputer/RedPajama-Data/blob/6d2cee9df2b0204dd2bcb00bf06b5a7b1d7432d7/app/src/core/quality_signals/importance_weights.py)使用词组特征的对数分布比求和，并可选长度修正，这给负值和长度相关提供**机制候选**；但目前没有证据证明比赛的 `dsir_books/wiki/math` 恰由同一代码版本、目标分布和修正开关生成。原始 DSIR 的确切量纲、长度归一化及跨目标解释继续 `UNRESOLVED`。本轮没有对原始列除以词数或翻转符号。

## 3. top n-gram “fraction” 超过 100

[全来源统计](Q1_NGRAM_BOUNDARY_DIAGNOSTICS_v1.csv)：A1 两列各有 2 行超过 100，且同属 2 个 ID；A2 为 0；A3 的 top 2-gram 为 7 行、top 3-gram 为 9 行。A1 两个可读原文案例的四个值，与按[RedPajama 原代码](https://github.com/togethercomputer/RedPajama-Data/blob/6d2cee9df2b0204dd2bcb00bf06b5a7b1d7432d7/app/src/core/quality_signals/repetitions.py)重算后乘 100 **逐值一致**，最大绝对差约 `2.9e-14`，见[样本核对表](Q1_NGRAM_SOURCE_FORMULA_CHECK_v1.csv)。该公式将“最高频 n-gram 的字符数 × 出现次数”除以全文标准化字符数；重叠的 n-gram 可重复计入字符，故结果可超过 1（百分比超过 100）。

这解决了 **A1 两个超界案例的算法解释**，并不证明 A2/A3 的完整生成链；A3 缺 `content`，无法逐条重算其超界记录。原列保留，不能裁至 100，也不能二次除以 100。全来源统一单位及版本仍待上游摘录生成记录核定。

## 4. 进入下一步的边界

22 项不能直接压为单一 Q。先以五个方向候选建立可解释的统计分歧候选，DSIR、量纲不明和用途依赖指标保留描述/敏感性角色；具体见 [QUALITY_CONFLICT_CANDIDATES_v1](QUALITY_CONFLICT_CANDIDATES_v1.md)。A1/A2/A3 是文档级信号；A4/A5 是配方运行级 Loss，仍无同运行 Q。后续描述性 Q 候选与 13 域响应 R0–R3 比较须分别按既有预注册推进，不能用 A6–A11 留出 Loss 回填方向或权重。
