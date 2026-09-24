# DATA_DICTIONARY

状态：PHASE 1 ROUTE FIELDS CHECKED；A1–A3 的 22 指标 Round 1 字典在 [QUALITY_SIGNAL_DICTIONARY_v1.csv](audits/modeling_phase1/q1/QUALITY_SIGNAL_DICTIONARY_v1.csv)，Round 2 方向/单位/派生关系/下游资格在 [QUALITY_SIGNAL_SEMANTICS_v1.csv](audits/modeling_phase1/q1/QUALITY_SIGNAL_SEMANTICS_v1.csv)。Round 4 的 [Full-22 + 五维描述候选](../03_models/modeling_phase1/q1/Q1_QUALITY_REPRESENTATION_FINAL_CANDIDATE_v1.md)保留所有信号角色，非 Q2 可识别 Q。A4/A5 与 A6–A11 的正式 p 响应/验证口径见[模型规格](../03_models/modeling_phase1/q1/round4/Q1_MODEL_SPEC_v1.md)。B1 外部 Alert 与附件内部受限资格分层见 [R4 裁决](audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md)。其他组仍为 INITIAL SKELETON；Phase 1 原指标见[路线审计](audits/phase1/route_audit_metrics.json)。

| 组 | 字段或模式 | 已知含义/单位 | 待核对 |
|---|---|---|---|
| A 质量 | _source_domain、22 个质量指标、content/text | 来源域、质量信号、原始文本 | 指标方向、多维列表压缩、缺失 |
| A 配比 | index、train_the_pile_*（17 列） | 配方索引与 17 域配比 | 单纯形容差、跨文件配对 |
| A Loss | index、metric/the_pile_*_val_loss（13 列） | 验证域交叉熵损失 | 域匹配、缺失、量纲 |
| A 映射 | mixture_domain、quality_domain、mapping_type | 17 域到质量域的参考映射 | 一对多关系与覆盖率 |
| B 标度律 | N_params_B、D_tokens_B、val_loss | N 与 D 的单位均为十亿，Loss 为交叉熵 | 训练轨迹依赖性、数据性质 |
| B 质量补充 | Q_score | 质量评分 | 与 Q1 评分尺度可比性 |
| C 算力 | C_FLOPs_1e21 | 单位为 10^21 FLOPs | 缺失、估算来源 |
| C 评测 | Model、#Params (B)、Submission Date、六维 Benchmark | 模型、参数规模、日期、能力指标 | 模型去重、日期定义、评分范围 |
| C 桥接 | Val_Loss、LB_*、Loss_Comparability | 损失、基准分与可比性等级 | 层级口径及映射误差 |
| C 架构 | model_name、n_layers、n_heads、max_position_embeddings | 模型名、层数、头数、上下文候选 | 模型匹配与可行值 |

统一单位换算需在预处理合同中明确：N_params_B 与 D_tokens_B 的“B”表示十亿；C_FLOPs_1e21 表示 10^21 FLOPs。以原始文件与题面公式再核对。

后续逐字段登记：文件编号、列名、类型、单位、正负方向、缺失码、有效范围、来源性质、拟合/验证/外推角色及处理版本。

## Phase 1 实测字段补充（2026-09-23）

| 来源 | 实测键/响应及行数 | 使用限制 |
|---|---|---|
| A1 / A2 / A3 SlimPajama 质量信号 xz | 51,230 / 17,523 / 203,752 条；共同有 `id` 和 22 指标，A2/A3 的来源域来自文件路径；均无 `index/run_id/mixture_id/experiment_id` | 样本粒度，无 A4/A5 同运行 Q；A1 与 A2/A3 分别重叠 1,419/10,000 个 ID，不能当独立重复实验 |
| A18 RegMix 文本 xz | 138,034 条、17 域；`text` 与 `_source_domain` | 可选原文辅助，不是 A2/A3 扩展质量信号；v1 曾误归类，已修正 |
| A4 `train_mixture_1m.csv` + A5 `train_pile_loss_1m.csv` | 各 512 个唯一 `index` 完全配对；17 个 `train_the_pile_*` 比例与 13 个 `*_val_loss` | p 行和 0.996–1.003 是显示舍入；秩/几何诊断单独归一化，不改原件 |
| A6/A8/A10 配比检验 | 256 / 256 / 64 行；A6/A8 的 17 维 p 完全相同 | 检验配比不是新增训练样本，Loss 留出不用于权重选择 |
| A16 映射 | 17 行；direct 3、near_direct 3、inferred 11 | inferred 不等于观测质量域 |
| B1 Pythia 轨迹 | 1,176 行；8 个 N 水平 × 147 检查点，`run_id` 逐行唯一 | 检查点相关；无语料/tokenizer 字段，不和 A Loss 直接池化 |
| B6 / B7 / B8 | 360 / 450 / 1,704 行；`N_params_B,D_tokens_B,Q_score,val_loss`，B8 另有 `data_type` | 全部半合成；B6 嵌于 B7，B8 的 Q–Loss 方向相反，先隔离 |
| C7 架构 | 45 个唯一 `model_name`；`max_position_embeddings` 为 2k/4k/8k/32k/131k 档 | 架构上限不是实际训练长度 |
| C1/C2/C3/C4 | 4,576 / 4,576 / 4,599 / 3,523 行 | C1/C3 大量重复来源，C1/C4 名称精确交集为零；日期和规模需对齐 |
| C5/C6 桥接 | 43 / 75 个唯一模型；`Val_Loss,LB_*,Loss_Source,Loss_Comparability` | C5 模型为 C6 子集；High 7 个均为 Pythia，不能据此宣称 Strong Bridge |
| C8 逐任务 JSON | 1,958 个文件中 1,954 可解析，4 个损坏 | 按模型版本去重后聚合；坏文件原件只读保留 |

## Modeling Phase 1 Round 2 定向证据补充（2026-09-24）

| 字段/来源 | 新核实内容 | 下游资格 |
|---|---|---|
| A1–A3 全部 22 个质量信号 | 五个正向候选、17 个仍无通用质量方向；逐项证据、压缩方式及 `DOWNSTREAM_ELIGIBILITY` 见语义表 | 当前无一项可作为 Q2 独立 Q 效应；17 项 `DESCRIPTIVE_ONLY`、5 项 `UNKNOWN`（DSIR 与两个 top n-gram） |
| `dsir_books/wiki/math` | 与词数强负相关；控制词数秩后三列仍近重复。上游对数重要性公式提供机制候选，但比赛字段的目标分布/开关/尺度未核 | UNKNOWN；不直接标准化/合并为 Q |
| `rps_doc_frac_chars_top_2gram/top_3gram` | A1 两个超 100 的 ID 在四次比较中与 RedPajama 上游重叠 n-gram 公式×100 精确匹配；A3 亦有超 100 行但无原文可重算 | UNKNOWN 全来源生成链；不裁剪、不过度按“百分比必须≤100”判错 |
| B1 `steps`/候选 checkpoint | 147 个标签等于公开 154 个去掉最早七个；本地索引三处 commit 与公开模型 API 一致 | 仅标签候选映射部分通过；不能代替 Loss 来源 |
| B1 `precision/wd/lr` | 轨迹内或相对固定公开配置有差异，字段究竟是训练、评估或后加仍 UNKNOWN | 排除正式基线规格，不凭它们估参数 |
| B1 `val_loss` | 仍无原始 run/revision、验证语料/tokenizer、逐行评估抽取锚；`ppl≈exp(val_loss)` 只证算术 | **NOT YET ELIGIBLE**；Alert `PARTIALLY RESOLVED`、基线暂停 |

用户提供《数据说明》PDF 的页边 96 段近白色小字已被[来源干扰核查](audits/modeling_phase1/DOCUMENT_INTERFERENCE_AUDIT_v1.md)排除出官方定义；编号和字段继续以可见正文与原件路径/哈希交叉核对。

## Modeling Phase 1 Round 3 候选比较补充（2026-09-24）

| 输入或表示 | 当前含义与来源 | 资格边界 |
|---|---|---|
| `q1_quality_features_v1.csv.gz` | 272,505 条 A1/A2/A3 物理记录的 22 项诊断标量、部分列表替代编码、ID/来源域；原始文本不复制，去重为 261,086 ID | 冻结哈希见输入 manifest；仅供描述候选，A1/A2/A3 不和 A4/A5 伪接 |
| DQ0–DQ3 | 五个有依据的方向候选构造透明标量、PCA、分组向量、域内归一化；其余 17 项在上下文/敏感性层明确保留 | 当前倾向多维描述，DQ0 仅透明对照；全体均非 Q2 独立质量变量 |
| `a5_13_domain_loss_v1.csv.gz` | A5 512 个训练运行 × 13 域原始验证 Loss，按冻结列顺序；A4 仅核 index 对齐 | R0–R3 比较只用 A5，R0 为非最终报告候选且 R3 必保留；A6–A11 未读/未验证 |
| B1 `val_loss` | 官方与附件对照仍无法取得该列行级 run/验证语料/tokenizer/转换锚；两个 README 链接 W&B run 的末步 Loss 与 B1 不同但目标未证相同 | Alert `PARTIALLY RESOLVED`；正式 N–D baseline 暂停；`SOURCE NOT RECOVERABLE FROM AVAILABLE PRIMARY MATERIALS` 不等于伪造证明 |

## Modeling Phase 1 Round 4 模型与验证口径补充（2026-09-24）

| 字段/文件 | 已核处理与数值角色 | 限制 |
|---|---|---|
| A1/A2/A3 22 信号 | Full-22 按 5 CORE、2 SECONDARY、12 SENSITIVITY、1 UNKNOWN、2 REDUNDANT 保留；五 CORE 按 A1 训练 ECDF 形成多维描述，DQ0 为等权摘要；A1 原文 14 案例做有限面效度检查 | 无同运行 Q；DQ0 不是 Q2 独立弹性变量；代码/非英文反例说明用途限制 |
| A4/A5 p 与 13 域 Loss | `index` 一对一；17 域 p 原始零值保留、行和仅按舍入归一；固定 17×16 Helmert 对比坐标；13 域 M1 线性输出后等权成 R0，R3 强制 | M1 是观察性预测关系，个别对比系数非独立因果效应 |
| A6/A7、A8/A9、A10/A11 | 官方验证对 256/256/64 行、哈希见 P_RESPONSE_VALIDATION_METRICS_v2.json；A6/A8 配比字节相同 | A7/1M 同尺度绝对预测检验；A9/60M、A11/1B 只做中心化相对形状/排序，1B 转移 FAIL |
| p 经验支持 | A4 留一近邻 q95/q99、观测凸包 LP、低维 PCA、单域边界分层；1M 为 2 IN/252 NEAR/2 OUT | 非现实供给约束，Q3 最终可行域仍 DEFER |
| B1 `N,D,val_loss` | 外部来源未解；内部 8×147 算术与轨迹/跨 N 顺序自洽，单列 Loss 可作附件内部条件响应 | Round 4 B 级受限入口待 Gate 2；外部 Pythia 声明不可用、N–D 参数尚未拟合 |
