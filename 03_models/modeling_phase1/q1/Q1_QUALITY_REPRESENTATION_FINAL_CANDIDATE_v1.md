# Q1 质量表示：PROVISIONAL FINAL CANDIDATE v1

**状态：PROVISIONAL Q1 QUALITY REPRESENTATION；待 Gate 2。**本候选收束 Round 1–3 的真实证据，不宣称“真实质量”、通用潜因子或 Q2 可识别质量效应。原始 A1/A2/A3 仍全量使用，22 项不因低维表示只用五项而消失。现有 `NO_MATCHED_Q`、下游资格 17 `DESCRIPTIVE_ONLY` + 5 `UNKNOWN`、TYPE E=0 均不改变。

## 两层输出

**Layer 1 — Full-22 quality profile（主表示）。**对全部 22 项逐字段保留定义、原尺度/诊断编码、有效数、来源域、分位数、异常、冗余、统计分歧与长度关系。每项指定一个展示角色：

| 角色 | 信号 | 处理 |
|---|---|---|
| `CORE`（5） | `fineweb_edu`, `fluency_en`, `ad_en`, `modernbert_cleanliness`, `modernbert_readability` | 方向有来源依据，形成五维相对 A1 训练参考的经验分位向量；原始/列表编码仍可查 |
| `SECONDARY`（2） | `rps_doc_word_count`, `rps_doc_num_sentences` | 长度/派生关系协变量，不作单调质量分 |
| `SENSITIVITY`（12） | `modernbert_reasoning`, `modernbert_professionalism`, `qurater`, `rps_doc_unigram_entropy`, `rps_doc_frac_unique_words`, `rps_doc_frac_no_alph_words`, `rps_doc_frac_chars_top_2gram`, `rps_doc_frac_chars_top_3gram`, `rps_lines_uppercase_letter_fraction`, `rps_lines_ending_with_terminal_punctution_mark`, `rps_lines_numerical_chars_fraction`, `rps_doc_mean_word_length` | 保留原义、域别及列表分量/压缩敏感性；未确认通用“越高越好”时不并入主质量向量 |
| `UNKNOWN`（1） | `dsir_books` | 三列 DSIR 中统计 medoid，仅作目标相似性待定面板；源公式/长度修正未核 |
| `REDUNDANT`（2） | `dsir_wiki`, `dsir_math` | 与 DSIR 代表列近完全同序，原值仍列于 Full-22 表，不作为独立质量证据重复加权 |

`UNKNOWN/REDUNDANT` 是 Full-22 的展示角色，不覆盖既有 `DOWNSTREAM_ELIGIBILITY`；两项 top n-gram 的下游资格仍是 `UNKNOWN`，虽然在完整画像中作敏感性特征。

**Layer 2 — Stable descriptive representation（五维）。**对五 CORE 项使用 [Round 3 冻结合同](Q1_ROUND3_COMPARISON_CONTRACT_v1.md)中的连续诊断编码和 A1 固定训练参考 ECDF，形成文档级向量 `u_i=(u_{i1},…,u_{i5})∈[0,1]^5`。域级主要汇报每维分位分布、均值/中位数和不确定性，并列 A1 与扩展集非重叠 ID 对照。该向量是**多维相对描述坐标**，不假定五项具有共同测量标尺或普遍用途权。

**Secondary descriptive summary：DQ0** 为 `5^-1 Σ_j u_ij`，只作相同固定编码下的透明标量参考；必须与五维分量并列，不可独立替代 Full-22 或作为 Q2 `γ_Q` 自变量。DQ1 PCA 是共变结构诊断（首维仅 48.11%、无广告载荷小）；DQ2 pooled 分组只有 3/9 域/扩展层复现，不固定维度名称；DQ3 域内归一化会构造性擦除域间位置，仅作敏感性。

## 质量冲突的正式措辞

在现有[六类候选审计](../../../01_data/audits/modeling_phase1/q1/QUALITY_CONFLICT_CANDIDATES_v1.md)下，**没有足够证据确认 SEMANTIC CONFLICT（0 项）**。保留并分别量化统计分歧、域别符号反转、冗余、长度/尺度伪象候选及未决关系；普通负相关不得称作语义质量冲突。消解方式是分开标示来源语义、避免重复计权、把未定方向留在 Full-22 面板，而不是构造未经证实的“冲突指数”。

本候选使“22 项完整画像”与“五维可定向描述表示”各有明确责任；Q1 论文结果仍须引用真实域级聚合和后续 p→Loss 验证，不能将这份规格单独称为 Gate 2 通过或完全满足题面最终评分要求。
