# A1–A3 nine-dimension quality-signal audit v1

**AUDIT RUN:** `AUDIT-Q1-QUALITY-20260924-v1`。**STATUS: CHECKED AUDIT RESULT / STRUCTURE DIAGNOSTIC — NO FINAL Q。**可复跑脚本：[modeling_phase1_q1_audit.py](../../../../04_code/data_audit/modeling_phase1_q1_audit.py)，SHA-256 `7d5e67631f103f0e61f733102e73c5fe4f68ac723b8a0738076ad088211d0ae5`；输入路径/哈希、UTC 运行时刻、关键计数在[机器记录](QUALITY_AUDIT_METRICS_v1.json)。原始文件只读，随机算法未用。质量字段含义参考[官方映射确认](A1_A3_OFFICIAL_MAPPING_v1.md)和数据源[Dataset Card](https://huggingface.co/datasets/opendatalab/SlimPajama-Meta-rater/blob/main/README.md)；后者不替代 F 题官方文件。

## 1 Completeness / 结构完整性

| 来源 | 解析行 | 每行字段 | 22 指标键 | JSON 解码失败 | `id` 缺失 |
|---|---:|---:|---|---:|---:|
| A1 样本 | 51,230 | 27 | 全部存在 | 0 | 0 |
| A2 arxiv 扩展 | 17,523 | 24 | 全部存在 | 0 | 0 |
| A3 github 扩展 | 203,752 | 24 | 全部存在 | 0 | 0 |

文件哈希、大小、实际路径与可见官方说明及 RAW_SHA256 一致；A2/A3 没有 content/source 列是设计上的结构性缺列。Python 解码器可读取全部行；源 JSONL 中有下述字面 `NaN`，Python 默认解码接受它，但严格 JSON/有限数值读者可能拒绝，不能把“可解码”当跨解析器或数值完整。

## 2 Missingness / 缺失模式

22 指标的键都在每行出现，数值诊断发现 **19 个含字面 `NaN` 的不可用六级列表**：A1 `modernbert_reasoning` 13/51,230（0.0254%）、A1 `modernbert_professionalism` 5/51,230（0.00976%）、A3 professionalism 1/203,752（0.00049%）；A2 无此问题。列表长度仍为 6，问题是非有限值，具体错误类别/比例见 [诊断 CSV](QUALITY_SIGNAL_DIAGNOSTICS_v1.csv)。A1 reasoning 缺失集中在 wikipedia 域的 13/10,000；A1 professionalism 至少 4 个在 commoncrawl。按原始 `fineweb_edu` 四分位的分层缺失率均很低，不能以此证明缺失随机；分域和原始质量层次的明细在[分层表](QUALITY_MISSINGNESS_STRATA_v1.csv)。本轮不插补、不删除源行。

## 3 Duplicate structure / 连接粒度

三表各自 `id` 唯一、逐字节相同行为 0。A1 有 content，内容哈希重复 0；A2/A3 无 content，无法据此判内容重复。A1∩A2=`1,419`、A1∩A3=`10,000`，重叠行的 22 信号**全部逐值相同**；A2∩A3 无共同 ID。三表合计 272,505 条物理行，扣除已知跨表 ID 重叠后为 261,086 个不同 ID。抽样与扩展对照可做，但不把重叠行当独立验证。三表没有可连到 A4/A5 的 `index/run_id/mixture_id`，`NO_MATCHED_Q` 的粒度边界保持。

## 4 Outliers / 数值异常

极端尾部是真实审计信号，不自动删除。A1 `rps_doc_word_count` 中位数 253、99 分位约 10,202、最大 552,671，偏度约 +33.9；A1 三个 DSIR 量的中位数约 −2,100，但最小值达 −1.24M 至 −1.67M，偏度约 −22 至 −41。`rps_doc_frac_chars_top_2gram` 和 `top_3gram` 虽名为 fraction，A1 最大分别为 135.13、201.68；源卡没有给足可确认的本地量纲/上界，因此标 **UNIT_SCALE_UNRESOLVED**，不能机械裁成 0–100。极端文本长度、编码与算法输出需要后续逐指标语义核对；按 1/5/25/50/75/95/99/99.9 分位及 min/max 的全量表见诊断 CSV。

## 5 Unit / scale / direction

14 个标量和 8 个列表字段的原始量纲不同：文长/句数、百分比样式比率、熵、DSIR 大负值、二分类 logits、四维 QuRating 和四套六级 PRRC logits。仅为**结构诊断**，脚本把 FineWeb 单元素列表取值、二分类 logits 取正类−负类 margin、PRRC logits 转 softmax 期望等级、QuRating 四分量取均值；原始列表保留不变，分量均值/范围另存[列表分量诊断](QUALITY_LIST_COMPONENT_DIAGNOSTICS_v1.csv)。这不是最终指标压缩政策。

根据数据源字段定义，只有 5 个诊断标量暂可标 `POSITIVE_CANDIDATE`（FineWeb 教育价值、流畅正类 margin、无广告正类 margin、cleanliness、readability）；其余 **17/22 的质量方向未定**。例如 DSIR 是目标域相似度，词数/专业难度/推理复杂度未必单调等于“越高越好”。`ad_en` 的原始概念“广告”偏负向，本轮的诊断 margin 特意取“无广告”类，不能把原始列表整体直接翻转。任何方向统一必须在下一轮依据官方/源定义和用途冻结，**不得以与 Loss 的相关符号反推方向**。[22 信号字典](QUALITY_SIGNAL_DICTIONARY_v1.csv)逐项写了含义、单位状态、方向、压缩候选、来源性质和下游限制。

## 6 Distribution / 分布与域差

A1 覆盖七域：arxiv 1,419、book 171、c4 10,000、commoncrawl 9,640、github 10,000、stackexchange 10,000、wikipedia 10,000；book 的样本极少，域级不确定性不能只按行数相同处理。A2/A3 是各自单域扩展，抽样与扩展分布比较必须处理 ID 重叠。没有某指标在三表中接近常数到只有 ≤10 个不同诊断值；多项连续分数强偏态或长尾，原尺度均值对极端值敏感，后续需比较稳健/对数变换，但不在本轮改数据含义。分域/原始 FineWeb 四分位缺失表和逐来源分位数 CSV 可复核。

## 7 Correlation / redundancy / preliminary dimensionality

[A1 Spearman 22×22 矩阵](QUALITY_CORRELATION_MATRIX_v1.csv)与[三来源 Pearson/Spearman 配对表](QUALITY_CORRELATION_PAIRS_v1.csv)基于**诊断性列表压缩**，不代表最终 Q 权重。A1 231 对原始信号中 114 对 Spearman 为负；多数信号方向未定，负相关本身不等于质量冲突。最强重复是 DSIR 三列：books–wiki `ρ=0.9990`、books–math `ρ=0.9969`、wiki–math `ρ=0.9968`；A2/A3 的 books–wiki 也分别为 `0.9998/0.9999`。A1 词数–单词熵 `ρ=0.9506`，DSIR-math–词数 `ρ=−0.9125`，提示 DSIR 与长度/域可能共变，不能把三列当独立质量证据。

A1 的 rank-space 相关矩阵数值秩 22，首成分解释 **35.1%**、前两成分 53.3%；谱参与率约 **5.57**，`|ρ|` 诊断阈值 0.6 下有 15 个探索性簇。这些是多维结构提示，不是“恰有 5.57 个独立质量维度”或已证实的潜在评分模型。A2/A3 的相关矩阵首特征值份额约 29.7%/37.7%，提示域别结构不同；后续需核分组和稳健变换。[簇/载荷表](QUALITY_STRUCTURE_CLUSTERS_v1.csv)和 [FIG-Q1-AUDIT-002/003](figures/FIGURES_MANIFEST.md)记录具体证据。

## 8 Leakage / derived-variable risk

三表没有 Loss、Benchmark 或 A4/A5 同运行结果字段，未见**直接字段级目标泄漏**。但 11 个 `rps_*` 是由文本规则派生、3 个 `dsir_*` 是目标域相似/重要性算法输出、8 个为模型标注；各组可能共享输入、生成器或训练语料，**不是 22 项互相独立的原始质量真值**。Meta-rater 数据卡提供字段族和列表语义，却没有为这批比赛摘录文件提供完整训练/校准谱系；特别是 DSIR 原始负值与“importance weight”文字之间的尺度关系仍需追索。不得把 A1/A2/A3 的内容变化伪接到配方级 Q 或用下游 Loss 监督赋权后再声称独立质量效应。

## 9 Evidence / experimental role and route impact

A1 是样本级抽样信号，A2/A3 是同源扩展；E1 指这些**真实提供的标注记录**，并不意味着每个指标都是独立训练干预。A4/A5 的配方 Loss 属另一运行粒度。当前只允许推进质量结构、方向核验、可解释冲突定义和**描述性 Q 候选**；`Q_descriptive` 不自动变为 Q2 的独立 `Q_identified`。九维审计总体完成，**没有新的官方 ID/字段重大不一致或明确目标泄漏 Evidence Alert**；B1 支线的来源警报另案处理，不污染 Q1 文件角色。需要进一步厘清 17 个方向未定信号、DSIR/“fraction”量纲与域不均衡，才能选择质量评分候选。

## Conflict candidates and figures

[QUALITY_CONFLICT_INPUT_v1.csv](QUALITY_CONFLICT_INPUT_v1.csv)列出高同向/反向原始相关、正向候选信号的相反五分位排名样本比例，以及第一秩主成分残差较大的信号。例：readability 与“无广告”诊断 margin 的相反五分位比例约 **8.81%**；这只是下一轮冲突定义输入，不是最终冲突判定。诊断图仅有缺失、相关和特征值谱三张，均有 [Figure ID/版本/n 说明](figures/FIGURES_MANIFEST.md)，没有论文图或最终评分图。
