# DATA AUDIT — PHASE 1 / ROUTE-DECISION AUDIT

状态：**CHECKED AUDIT RESULT，修订 v2**（2026-09-23）；只裁定当前数据允许的后续建模路线，不是 Q1–Q4 的 `VALIDATED FINAL RESULT`，不确认最终模型。v2 按可见《数据说明》修正 A1/A2/A3 编号：原 v1 误把可选 RegMix 文本 A18 当作扩展质量信号，并漏扫 A2/A3。原版证据与脚本保存在 `superseded_v1/`，不得作为当前质量样本计数引用；其余路线诊断由 v2 脚本重算复核。

## 事实源、执行与边界

- ACTIVE 设计依据：[共识 v1](../../../02_analysis/consensus/CONSENSUS_F_PROBLEM_ANALYSIS_v1.md)、[项目状态](../../../09_handoff/PROJECT_STATE.md)、[可识别性规范](../../IDENTIFIABILITY_AUDIT_SPEC.md)。未重开 Discovery。
- 只读输入：`01_data/raw/real_attachments/`；[RAW_SHA256.csv](../../raw/RAW_SHA256.csv) 为 2,012 个原件的哈希清单，本次使用的逐文件路径与 SHA-256 在 [route_audit_metrics.json](route_audit_metrics.json) 的 `input_paths_and_sha256` 中。清单自身 SHA-256 为 `62f97ac6cb8f84d95bda7e3c87914d5d3fa695cb1b865a4c0fa880988ac75413`。小表和 A1/A2/A3 三份 xz 经本次实际哈希核对；C8 JSON 使用初始化时已校验的原件清单并逐文件解析，明细见 [C8_file_manifest.json](C8_file_manifest.json)。
- 可复跑代码：[route_decision_phase1.py](../../../04_code/data_audit/route_decision_phase1.py)，命令 `python 04_code/data_audit/route_decision_phase1.py`。它记录脚本哈希与 UTC 运行时刻，计算不覆盖原件。AUDIT-01 的机器分支由 [identifiability_summary.json](identifiability_summary.json) 输入已有分支器，输出 [identifiability_branch.json](identifiability_branch.json)。
- E1 表示原附件中的真实样本或公开观测，仅在原粒度成立；E3 为半合成；`calibrated`、`High` 等源内标签没有经本次审计自动升级为跨源 E2。几何、相关和秩是审计计算，不是因果估计。
- 执行顺序：**01 → 04 → 07**（先确定 A 的配对、响应、配比支持），**02 → 03**（再判断 A/B 标尺和质量补充），**05 → 06**（最后核 C7 情景与 C 桥接）。A6–A11 的 Loss 值没有用于挑选主响应权重或拟合模型；只核了表形、配比支持和预留角色。

## AUDIT-01 — 同运行 Q/p 独立变化

**QUESTION**：A 是否允许估计固定 p 后的真实独立质量项？

**DATA USED / METHOD**：完整流式解析 A1 `A_data_value/slimpajama_quality_signal_sample.jsonl.xz`、A2 `slimpajama_quality_extended/arxiv_part-6777d8857c6e-000486.jsonl.xz`、A3 `slimpajama_quality_extended/github_part-6777d8857c6e-000275.jsonl.xz` 的字段、样本 ID 与来源域；以 A4 `regmix_tables/train_mixture_1m.csv` 的 `index`、17 个 `train_the_pile_*` 与 A5 `train_pile_loss_1m.csv` 的 `index`、13 个 `*_val_loss` 配对；核 A16 `domain_mapping_guide.csv`。可选 A18 `regmix_domain_sample.jsonl.xz` 是原文样本，不是 A2/A3 质量信号。对 17 比例先仅在秩诊断中归一化，再用截距加 16 个比例坐标检查 p 基线秩。输入哈希见指标 JSON 的 A 项及原件清单。

**EVIDENCE**：A1/A2/A3 分别为 **51,230 / 17,523 / 203,752** 条质量信号记录，均完整可解析且各表 `id` 唯一；三表共有相同的 22 个质量指标键且每行均含这些键，指标值的缺失/有效性仍待完整九维审计。A1 与 A2 有 **1,419** 个相同样本 ID、与 A3 有 **10,000** 个相同 ID，扩展集不是与抽样集独立的重复实验。三表均无 `index`、`run_id`、`mixture_id` 或 `experiment_id` 键；A2/A3 的域由文件路径给出。A4/A5 有 **512** 个唯一且完全一致的配方 `index`，但无同运行 Q 列。A16 的 17 域映射为 3 个 direct、3 个 near_direct、11 个 inferred。合法 p 基线设计秩为 **17/17**；由于 Q_r 不存在，`X_full` 秩、Q 残差变化、精度和留组增益均 **NOT_TESTED**。分支器在修正输入后仍输出 `NO_MATCHED_Q`，不是把 p 基线满秩误写为 Q 已识别。

**DECISION / MODEL ROUTE IMPACT**：保留 p→13 域 Loss 的真实配对响应研究，以及独立的质量信号测量；Q1→Q2 的真实独立标量质量弹性 Path A 暂不可检验。淘汰“直接从现有 A 配方估出独立 γ”的路线。Q2 只能把 p 响应作为候选真实输入；Q 在 Q3 中只能先作显式条件情景。固定域质量下的 `pᵀq` 或 `p⊙q` 若将来构造，须按共识标为 p 的确定函数/联合编码。

**FALLBACK / STILL OPEN**：启用 F01/F02；若后续真实同运行 q 仍缺失，F04 删去独立经验弹性点估计。Q 评分、噪声、泄漏控制和最终质量尺度尚未建立；A1/A2/A3 的重叠样本须在比较和不确定性估计中识别，不能当独立样本。不能宣称“质量没有作用”，也不能用 B6–B8 补成 A 的真实同运行证据。

## AUDIT-04 — 13 域 Loss 的主响应条件

**QUESTION**：单一公共 Loss 因子或既定等权响应是否受到 A4/A5 的支持？

**DATA USED / METHOD**：只在 512 条 A5 训练配方的 13 域 Loss 上核缺失、均值/标准差、78 对相关与标准化奇异值；A6–A11 仅核字段、行数及配比支持，保持检验角色。

**EVIDENCE**：训练表无缺失。域均值 **3.894–6.553**，标准差 **0.321–1.535**；78 对相关的中位数 **0.081**、范围 **−0.173 至 0.816**，其中 **24 对为负**。标准化第一主成分解释约 **22.8%**，前三个合计约 **55.5%**。这些是训练内描述，不证明某种权重在保留集上的优越性。

**DECISION / MODEL ROUTE IMPACT**：保留透明等权原始 Loss、仅由训练部分确定的标准化综合、低维综合和多响应四类候选；强单因子假设不获当前审计支持，不能直接用 PCA 第一主成分替代 13 域异质性。`PRIMARY RESPONSE + DOMAIN HETEROGENEITY` 双层结构继续有效。淘汰“按 A6–A11 检验成绩反调主响应权重”的路线。

**FALLBACK / STILL OPEN**：若用途、尺度和权重依据不能冻结，以多响应/多目标为主，不强造单指标。P1-1 仍需在正式 Q1 拟合和查看保留 Loss 结果前预注册权重及评价规则；最终响应 **OPEN**。

## AUDIT-07 — p 的经验支持与现实供给

**QUESTION**：17 维 simplex 自由优化是否有足够观测与实施支持？

**DATA USED / METHOD**：A4 512 配方、A6/A8 的 256 个相同配比和 A10 的 64 配比；检查和、负值、零值、合法 p 设计秩。针对检验配比，用线性规划判断是否落在 512 个训练配比的凸包；另按原表 0.001 的显示精度，允许源/目标每坐标合计 **0.001** 的舍入包络复核。A16 映射和现有供给元数据仅用于判断能否建立现实界，不把经验包络称工程硬约束。

**EVIDENCE**：A4 比例和为 **0.996–1.003**，为显示精度导致的闭合偏差；无负值，**45.1%** 的格子为零，每条配方激活域中位数为 **9/17**。归一化后的合法 16 维 p 基线秩为 **17/17**。严格凸包包含 A6/A8 的 **2/256**、A10 的 **17/64**；纳入 0.001 舍入包络后分别为 **21/256**、**41/64**。A6 与 A8 的配比完全相同，不能重复计作独立 p 支持。未找到可逐域核实的许可、可得 Token 总量和供给上下界。

**DECISION / MODEL ROUTE IMPACT**：保留“观测配比候选集／经验凸包／审计后局部扩展／低维参数化”作为不同层级的 Q3 候选。当前数据不支持把完整 17 维 simplex 上的角点解称为可预测或可实施最优解。舍入敏感性已单列，避免把严格凸包数字当成无误差真值。

**FALLBACK / STILL OPEN**：若 Q1 配比响应在检验集失稳，固定/枚举观测配比；理论 simplex 解与数据内解、可实施解分报。真实供给约束和局部扩展距离 **OPEN**，P1-3 未通过使用前门槛。

## AUDIT-02 — A/B Loss 可比性

**QUESTION**：A 的 13 域交叉熵能否与 B 的单列 `val_loss` 直接合并？

**DATA USED / METHOD**：对 A4/A5 与 B1 `pythia_training_log_existing.csv`、B4 `scaling_baseline.csv`、B5 `published_scaling_data.csv` 检查观测粒度、响应列、验证语料/tokenizer 元数据、模型族和运行键；核公开 [RegMix 原仓库](https://github.com/sail-sg/regmix) 与 [Pythia 原仓库](https://github.com/EleutherAI/pythia) 的数据设计。

**EVIDENCE**：A 是 RegMix 512 条小模型配方运行 × 13 个 Pile 验证域；B1 是 Pythia **1,176** 行检查点，但只有 **8** 个模型规模、各 **147** 个检查点，`run_id` 在表中是逐行唯一键，不能当 1,176 个独立训练簇。B4 有 **57** 行 12 个族，B5 有 **44** 行 9 个族。这三份 B 表均无验证语料/tokenizer 字段；A/B 无同运行锚点，B 的单列 `val_loss` 也不能自动等同 A 某一域或其综合。

**DECISION / MODEL ROUTE IMPACT**：淘汰未校准绝对 Loss 的直接 joint fitting。保留分源建模、两阶段修正和在确有共同锚点后才尝试的校准/分层模型；B1 的训练轨迹应按模型规模与时间块处理依赖，不随机逐行分割。

**FALLBACK / STILL OPEN**：先分别建立来源内可验证关系；跨源绝对标尺、源别偏差和能否形成 E2 可比层 **OPEN**。不能从相似数值范围推断语料/词表相同。

## AUDIT-03 — B6–B8 的质量变化及冲突

**QUESTION**：半合成 Q 变化可支持什么，三张表是否相互独立且同向？

**DATA USED / METHOD**：逐行核 `supplementary_NQ_experiment.csv`、`_expanded.csv`、`_large.csv` 的 `N_params_B,D_tokens_B,Q_score,val_loss,data_type`；计算同 N,D 下的 Q 梯度符号、简约设计秩和重叠网格的 Loss 差异。原件哈希分别为 `c7450ce0…`, `880fd265…`, `bda0d449…`（全长见指标 JSON）。

**EVIDENCE**：B6 为 **360** 行，9×5×8 网格；B7 为 **450** 行，9×5×10 网格。B6 的 **360** 行全部出现在 B7，重叠 `val_loss` 最大差 **0**，不能当独立重复实验。B8 为 **1,704** 行，15 个 N、10 个 D、12 个 Q 水平，其中源表标 `calibrated` **984** 行、`extrapolated` **720** 行；后三者均是半合成或更远外推。三表的 `[1, log N, log D, Q]` 设计各为 4/4 满秩，但这种秩只属于生成表。固定 N,D 的 Q–Loss 线性斜率：B6/B7 的全部 45 组为负，B8 的全部 150 组为正。B7/B8 的 224 个共同 N,D,Q 点，Loss 中位绝对差 **1.1393**，相关约 **−0.026**。目前未见可审计的 B8 生成代码或 Q 含义反转说明。

**DECISION / MODEL ROUTE IMPACT**：B6/B7 可作为**同一半合成规律**的条件压力测试；不得把重叠行翻倍增加样本量。B8 与其方向冲突，先**隔离为来源/定义待查的半合成外推表**，不能与 B6/B7 合估单一质量参数，也不能用于验证 B6/B7 所拟合的规律。淘汰“B6–B8 一致支持真实独立质量弹性”的路线。

**FALLBACK / STILL OPEN**：启用 F03；Q2 若需要质量情景，暂分报 B6/B7 与 B8 相反假设，B8 在来源解释和 Sol/Opus 复核前不进入主校准。Q_score 与 Q1 的尺度对齐、生成机制、B8 符号原因和外推可信度 **OPEN**；不能由半合成满秩推断真实质量干预。

## AUDIT-05 — C7 长度与 30,000 token 代理阈值

**QUESTION**：解析阈值是否落在给定架构上限中？

**DATA USED / METHOD**：核 `C_efficiency_evolution/model_architecture_metadata.csv` 的 45 个唯一 `model_name` 与 `max_position_embeddings`，并查是否另有真实训练上下文长度列。

**EVIDENCE**：架构上限计数：2,048 有 **18**，4,096 有 **8**，8,192 有 **7**，32,768 有 **11**，131,072 有 **1**。**12/45** 个架构上限达到或超过 30,000；表中没有实际训练时使用的上下文长度字段。代理阈值位于 8,192 与 32,768 两档之间。

**DECISION / MODEL ROUTE IMPACT**：保留跨阈值的 C7 架构情景，但只称架构能力上限；不能把 32k/131k 直接写为训练长度或现实成本事实。固定 L_ctx 的成本比仍按共识为 `η L_ctx / 6`，预算单独增加不改变这一比值。

**FALLBACK / STILL OPEN**：若训练长度证据仍缺，Q3 只在明示的 C7 架构上限情景中作成本敏感性，阈值外推另标。题面已给代理系数 η=2×10⁻⁴；其现实适用性、实际训练长度、实现效率和可行预算还需后续证据/成本合同；最终 Q3 网格 **OPEN**。

## AUDIT-06 — C 桥接、时间、模型族及 C8

**QUESTION**：C5/C6 是否已有足够可比和独立覆盖支持 Strong Bridge；C 的能力时钟和规模变量能否直接拼接？

**DATA USED / METHOD**：核 C1 `leaderboard_cleaned.csv`、C2 `leaderboard_enhanced.csv`、C3 `leaderboard_extended_timeseries.csv`、C4 `epoch_all_ai_models.csv`、C5/C6 两份桥接、C8 的 1,958 个逐任务 JSON；按模型名做保守精确匹配，不以模糊匹配制造连接。C8 逐个解析并记录可读性、模型名和任务数；这里只测覆盖，不拟合最终 Loss→Benchmark 映射。

**EVIDENCE**：C1 有 **4,576** 行、**4,497** 个模型名，79 条重复名；六个基准列齐全，参数列 4,573 行非空，许可证仅 2,823 行非空。提交日期可解析 **4,564** 行，范围 **2024-06-08 至 2025-03-13**。C3 的 4,599 行中 **4,573** 来自同一榜单、仅 **26** 为历史报告，不应把 C1/C3 当独立重复观察。C2 只有 **447** 个 Epoch 发布日期和 **443** 个开放权重匹配值。C4 有 3,523 行，训练算力 1,390 行、数据量 1,424 行非空，但与 C1 的**精确名称交集为 0**；需审计实体对齐，不能按行拼接。C5 为 43、C6 为 75 个不同模型，C5 模型集合包含于 C6；C6 的 High 仅 **7** 个，全部为 EleutherAI/Pythia 同族，Medium 为 **68** 个且标记不同验证集。高层只沿 Pythia 规模变化，不覆盖 Q/p 变化。C8 找到 **1,958** 文件，**1,954** 可解析、**4** 个 JSON 损坏（文件大小接近截断块），有 1,861 个唯一模型名，其中 1,859 与 C1 精确匹配；可用文件每份有 25–45 个任务结果。

**DECISION / MODEL ROUTE IMPACT**：**Strong Bridge 目前不能放行**；高可比层仅单族小样本且没有覆盖 Q3 的 Q/p 决策空间，Medium 不可自动并入。保留限族 Weak/No 两个待检分支，待 P1-2 判据预注册及留族/留时误差后选择。Q4 先从 C1 的能力和参数覆盖做可核描述，C4 的 N/D/C 规模分解必须先实体匹配和单位审计；C8 可支持逐任务聚合，但需排除 4 个坏文件并冻结同模型版本。以 C1 截止 **2025-03-13** 的可观测信息定义任何对应回测时钟；C4 含后续日期，不能回填到更早预测时点。

**FALLBACK / STILL OPEN**：若桥接留出失败，走 No Reliable Bridge，Q4 独立能力演进并报告映射误差/失败。最终 Strong/Weak/No、可用开源定义、pretrained/chat 分层、C4 匹配规则、六维聚合、规模变量和 t=0 均 **OPEN**；本审计不作预测或因果“技术进步”分解。

## Gate 1 与下一步

七项路线问题已有来源、字段、程序诊断和安全分支，**可继续受限的详细数据审计与 Q1 规格准备**。Gate 1 暂记 **CONDITIONAL / NOT FULLY CLEARED**：A 的真实同运行 Q 不存在，A/B 标尺未校准，B8 冲突未解释，p 现实供给未核，C4/C1 实体对齐与 C5/C6 留出未做，且尚未完成全部必用文件的九维审计和预处理冻结。这个状态不放行 Q1–Q4 的最终模型、正式实验或论文数字。

项目结构预检 `python 04_code/utils/stage_gate.py --stage DATA_AUDIT` 的[报告](../../../10_review/detection_reports/DATA_AUDIT_PHASE1_20260923.json)为 `MISSING_STRUCTURE`，唯一未过项是 `01_data/processed/**/*`：当前没有冻结模型输入。该检查器针对完整 Data Audit 阶段；Phase 1 只完成路线审计，因此不以占位 processed 文件换取通过。

优先处理顺序：① 追查 B8 生成与 Q 定义并由 Sol/Opus 审议质量情景；② 预注册 Q1 主响应权重/保留检验和 p 可预测域；③ 补 A/B 验证语料与 tokenizer 的可比证据；④ C4/C1 名称/版本/时间对齐、C8 坏文件与逐任务口径；⑤ 现实域供给、实际训练上下文与 Q3 成本参数。上述均属后续工作，不在本审计中偷定数学模型。
