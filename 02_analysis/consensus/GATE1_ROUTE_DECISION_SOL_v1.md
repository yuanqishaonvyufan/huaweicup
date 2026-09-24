# GATE 1 Route Decision — Sol Round A Evidence-Based Synthesis v1

状态：**DRAFT FOR OPUS REVIEW / ROUTE-LEVEL CONDITIONAL PASS PROPOSED**。本稿由当前本地 Codex 按用户指定的 Sol Round A 任务撰写；没有调用独立的 GPT-5.6 Sol 或 Claude Opus，不冒充其已完成复核。它消费 [ACTIVE Discovery 共识](CONSENSUS_F_PROBLEM_ANALYSIS_v1.md)和[Phase 1 路线审计 v2](../../01_data/audits/phase1/ROUTE_DECISION_AUDIT_PHASE1.md)，只提出数据驱动路线，不设置 ACTIVE FINAL MODEL、不做正式参数估计或论文结果。七项审计数字、原始路径和 SHA-256 在[指标记录](../../01_data/audits/phase1/route_audit_metrics.json)；AUDIT-01 分支在[机器输出](../../01_data/audits/phase1/identifiability_branch.json)。

## 1 Evidence Summary

最关键的新事实是：A1/A2/A3 三份**必用**质量信号分别为 51,230 / 17,523 / 203,752 条，均无 A4/A5 配方运行键；A1 与扩展集有 1,419/10,000 个重复样本 ID。A4/A5 的 512 条 p/Loss 虽按 `index` 配对，却没有同运行 Q，分支为 `NO_MATCHED_Q`。可选的 138,034 条 RegMix 原文是 **A18**，不是 A2/A3；首轮审计的错误映射已在 Phase 1 v2 中修正，旧版留存 `superseded_v1/`。这使质量**描述指标**与能进入 Q2 的**独立可识别质量变量**必须分开。

其余路线证据：A5 的 13 域 Loss 相关中位数 0.081、24/78 对为负、标准化第一主成分仅解释 22.8%；A4 p 有 45.1% 零格，舍入包络下仅 21/256 个 1M 检验配比、41/64 个 1B 配比落在训练凸包内或其精度邻域。B1 1,176 行来自 8 个模型规模各 147 检查点；A/B 未找到共同验证语料/tokenizer 锚。B6 嵌在 B7，B8 在固定 N,D 下 Q–Loss 方向全反。C7 有 12/45 个架构上限覆盖 30k，但没有实际训练长度。C5/C6 High 桥接只有 7 个同族 Pythia；C4/C1 精确名称交集为零，C8 1,958 JSON 中 4 个损坏。上述数字均是 AUDIT EVIDENCE，不是模型效果或因果证据。

## 2 Audit-by-Audit Decisions

下表的 PASS 指“足以给出安全路线判断”，不表示目标效应存在或后续 Gate 已通过。单项失效路线另写明。

| Audit | Round A 状态 | 保留与降级 | 排除/隔离 | Fallback 与尚缺证据 |
|---|---|---|---|---|
| 01 Q/p | **PASS**（负分支可判） | 保留质量描述、p→Loss；独立 Q 弹性从主路线降级为有真实同运行新数据才可重开的研究支线 | REJECT 由现有 A4/A5 直接估 γ_Q；固定 q 的 `pᵀq`/`p⊙q` 不是独立干预 | F01/F02/F04；仍可定向寻找运行→质量真实键，但不等它开工 |
| 02 A/B | **CONDITIONAL** | 分源建模为 baseline；相对效应、两阶段作为条件桥梁 | REJECT 未校准绝对 Loss 直接池化 | 无共同验证集/tokenizer/锚点时只报分源关系 |
| 03 B6–B8 | **CONDITIONAL**（B8 主用途失败） | B6/B7 作为同一 E3 半合成敏感性来源 | B8 QUARANTINE；B6/B7 不双计，B8 不估主参数 | F03；查生成器、Q 与 Loss 定义后再定 stress test 或独立情景 |
| 04 13 Loss | **CONDITIONAL** | 原始等权主响应 baseline + 必报 13 域异质性 | DOWNGRADE PCA 第一因子为探索；REJECT 按 A6–A11 调权 | 多响应 fallback；P1-1 提案须 Opus 审核并在留出使用前冻结 |
| 05 C7 | **CONDITIONAL** | L_ctx 仅为外生敏感性参数；30k 仅架构支持参照 | REJECT 把 `max_position_embeddings` 当已观测训练长度 | 待实际训练长度/效率证据；Q3 仅可准备情景规格 |
| 06 Bridge | **CONDITIONAL**（Strong 不放行） | 当前主张状态为 **No Reliable Bridge yet**；限族 Weak 仅为待检候选 | DOWNGRADE Strong；不得从相关性或 7 个同族点运输 Q3 全决策空间 | F05；高可比留族/留时误差、区间校准、类型/规模覆盖后再分级 |
| 07 p 域 | **CONDITIONAL** | 有限观测配比集合为最保守 Q3 baseline；经验凸包是下一层 | REJECT 完整 simplex 角点作现实最优 | P1-3 供给/许可未核；局部扩展和低维域待 Q1/Q2 验证 |

## 3 Q1 Route Decision

**Q1-A 质量预处理。**必须流式使用 A1/A2/A3 全量 22 个质量信号；先核各指标方向、8 个列表型指标的含义/压缩、缺失和异常尺度，再用同一训练确定的方向与变换处理扩展集。A1 的 `content` 可做文本语义抽查；A2/A3 无原文时只作信号层复核，除非找到可追踪原文。A1 与 A2/A3 的重叠 ID 用来作“抽样对照”，不能当独立验证或重复加权。质量评分先建立透明、无 Loss 监督的样本/域描述 baseline，补域内分布与不确定性；抽样设计不明时不把简单合并均值称人口域质量。

**Q1-B 结构与冲突。**方向统一后再分析分布、指标冗余、相关簇及同文本指标排序反转；区分真正价值目标冲突与量纲、缺失、多维压缩造成的假冲突。以 A1 七域分析并在 A2/A3 的 arxiv/github 全量扩展上检查主要规则的稳定性。冲突规则与评分权重仅能用质量信号/预定任务定义，不能用 A7/A9/A11 的 Loss 倒灌选择。

**Q1-C Q 的角色。**当前可以得到 `Q_descriptive` 的样本/域分数候选；**不存在**与 A4/A5 同运行且独立于 p 的 `Q_identified`。A16 只有 3 direct、3 near_direct、11 inferred，质量侧 c4 在 17 个配方域中无同名列。即使以固定域 q 构造 `Q_eff(p)`，它仍是 p 的确定函数，最多作联合描述/条件情景，不估“固定 p 提高质量”的真实弹性。仍值得做一次有范围的原始配置/运行键搜索，但它是并行证据补充，不阻挡 Q1 主线。

**Q1-D 配比响应。**A4/A5 的 512 配方按 `index` 成对；p 的闭合、舍入和零值必须先处理。第一候选用对零值安全的 16 维 simplex 线性对比与截距，不把 17 原始比例加截距一起解释；若采用对数比/ILR，必须先预注册零值政策、逆变换与参考意义。对 p 的可解释效果按域替代方向与实际支持报告，训练/检验凸包内外分层；四个无同名验证 Loss 的训练域仍可影响其他 13 域响应。

**Q1-E 输出给 Q2。**分别交付：质量信号的定义/方向/压缩/域聚合/误差及 A16 映射等级；A4/A5 p→主响应和 13 域响应的候选关系、零值/支持域、A6–A11 留出检验计划；来源与 E1/E3/E5 标签；`NO_MATCHED_Q` 标志。Gate 2 未完成前只传接口规格，不能传已验证 p 系数；更不能传真实独立 γ_Q。

## 4 Q1→Q2 Interface Decision

优先采用**分阶段双轨接口**：质量轨描述“可测的 22 维/域级质量和冲突”；配比轨在 RegMix 同运行 p/Loss 上估可验证关系。二者在 A16 的 direct/near/inferred 级别下可形成带映射误差的联合图景，但不硬拼为同运行 Q。`p⊙q` 仅保留为明确“固定 q 条件下”的联合编码候选，不能当识别修复。Q 的数值进入 Q2/Q3 时目前只能是公开声明来源、尺度与不确定性的条件情景，B6/B7 仅提供 E3 敏感性；其 `Q_score` 与 Q1 的 `Q_descriptive` 没有自动相等关系。

暂禁的论断包括“质量提高 0.1 导致真实 Loss 降低某值”“A 数据同时识别 p 与 Q 的独立弹性”“B6/B7 验证了真实质量干预”“PCA/正则化解除固定 q 别名”。是否能恢复独立 Q 研究取决于真实配方运行键、不同 q 的同 p 附近设计、无目标泄漏的评分谱系及后续秩/精度/留组检验，而不是再造一个评分。

## 5 Q2 Route Decision

拟议模型升级树是**证据顺序提案**，尚非 ACTIVE 数学规格。它保留 C17“从简单基线逐级升级、每步靠同口径留出”的原则；因 `NO_MATCHED_Q`，建议 Opus 审议是否把旧标签“先独立 Q、再 p”调整为：

| 层级 | 当前候选路线 | 证据来源与升级门槛 |
|---|---|---|
| M0 | B1 内部的经典 N–D Scaling Law baseline | 8 个规模的相关轨迹，按模型规模/时间块留出；B2（E3）或 B3（插值）履行题面辅助验证，B4/B5 真实跨族/文献分级核验，绝不把 B1 1,176 行当独立运行数 |
| M1 | 与 M0 **分源并列**的 A 领域/配比结构修正，先表现为来源内相对 Loss 响应 | Q1 Gate 2 的 p→13 域及预注册主响应通过；共同目标、尺度或可运输关系未建立时不把 M1 直接加成 B 的绝对 Loss 项 |
| M2 | 有明确来源的质量**条件情景**或质量调整项 | B6/B7 作为同一 E3 网格，只给半合成灵敏度/参数条件区间；与 Q1 Q 尺度、真实方向和运输假设未核前不估真实 γ_Q。质量调整有效数据量等形式仅为形状候选 |
| M3 | 少量必要交互 | 同粒度设计覆盖、噪声相对精度、同切分留出增益、跨族/来源稳定均支持时才提出；当前不启动高维交互 |

最现实的 baseline 是 **B1 的 N–D 关系 + A 的独立 p 响应分析**，而不是一张伪完整的 `(N,D,Q,p,L)` 拼接表。题面要求的广义关系可以作为有标注的条件函数族与分源参数/区间来回答：对可识别 N、D、p 分别给经验支持；对未识别 Q 给条件假设、符号推导和 E3 情景区间，清楚指出质量—规模等效量是条件结果。是否最终足以满足题面“统一模型”的力度，须经 Gate 2/3 与 Opus 复核；不能以变量都出现在公式中代替验证。

## 6 A/B Separation Strategy

**当前首选 A：分源建模。**A 的 13 域 Loss 与 B1 单列 `val_loss` 没有核实同一验证语料/tokenizer/模型族锚，故分开估计和报告。**C：来源内相对变化/normalized effect** 是可比性探针，用共同定义的基准点/方向与区间比较 p 对 Loss 和 N/D 对 Loss 的局部变化；标准化本身不消除验证集差异，不能自动升级为共同绝对标尺。**B：two-stage estimation** 只有在 Q1 p 关系经 Gate 2 验证且相对效应可以运输或有锚点时才作为条件机制。**D：calibration** 需后续同模型、同 tokenizer/语料或可核 overlap 锚及独立留出证据，当前不执行。跨源 E2 标签不得预支。

## 7 B6/B7/B8 Evidence Strategy

B6/B7 是同一半合成设计的嵌套版本，优先以 B7 为覆盖更完整的 E3 条件敏感性表，B6 作为复制一致性检查，不叠加独立样本量。B8 状态定为 **QUARANTINED / NEEDS GENERATION-MECHANISM REVIEW**。在查清生成规则前，它不得估质量项的符号、大小、弹性、质量—规模替代率，也不能验证 B7。调查合同见 [B8_CONFLICT_INVESTIGATION_PLAN](../../10_review/B8_CONFLICT_INVESTIGATION_PLAN.md)。若证明是不同质量定义/生成机制而可解释，可单列 alternative scenario 或 stress test；若无法解释，保留隔离；若有错误，保留原件并另立可复现修订版本。

## 8 13-Domain Response Preregistration

P1-1 的[单独预注册提案](../../01_data/audits/phase1/P1_1_13_DOMAIN_RESPONSE_PREREG_SOL_v1.md)指定：**R0 = A5 十三域原始交叉熵等权均值**为最简单 PRIMARY RESPONSE baseline，同时**强制保留全部十三域异质性 R3**；A5 训练标准化等权 R1 为尺度敏感性，PCA 第一因子 R2 仅作降级的结构候选。选择 R0 因其保留 Loss 单位、权重透明；并不声称不同域的真实用途相等。现有第一因子解释率和负相关不支持“PCA 一维足以代表全部领域”。权重、标准化参数和 PCA 载荷只由 A5 定义，不用 A6–A11 结果调权。未来每个配比结论要同时报主响应、逐域方向和最差受损域；若平均改善隐藏明确领域恶化，转多响应 fallback。Opus 可在留出结果使用前要求修改并另立版本。

## 9 Context-Length Decision

题面将 L_ctx 明确设为**外生情景变量**。η=2×10⁻⁴ 与 `C_attn/C_train=ηL_ctx/6` 给出条件解析阈值 30,000 token；C7 的 12/45 个架构上限高于该值，仅说明**architecture-support reference**。无实际训练上下文时，不称阈值已在真实训练成本中实现，也不把 L_ctx 当优化内点变量。后续 Q3 可在 C7 代表性档位作外生敏感性，并明确“架构上限情景”与已观测训练长度的差别；固定 L_ctx 时单独增加预算不改变代理成本比。

## 10 Loss–Benchmark Bridge Status

当前可作的陈述是 **No Reliable Bridge yet**：C6 高可比层 7 个 Pythia 同族模型，缺跨族、Q/p 和 Q3 预测域覆盖；68 个 Medium 点来自不同验证集，不能合并后声称高可比。此状态表示**尚无足够证据放行桥接**，不是证明真实世界不存在任何关系。`Weak Bridge` 仅保留为限族、限目标、宽区间的待检候选。要升级 Strong，需预先定义高可比层、模型类型/规模/时间/Q3 预测域覆盖，建立验证集与 tokenizer 的可比链，做独立模型族或时间留出、误差和区间校准，并证明预测不依赖单一族或来源；单一强相关不够。若最终无可靠桥接，按 F05 让 Q3 报 Loss/成本，Q4 独立完成能力分析及题面要求的映射尝试与误差披露。

## 11 p Support-Domain Decision

预注册 Q3 的可行域层级如下，均只在 Q2/Gate 3 放行输入后才实际优化：**E 有限候选配比集**（A4 原观测且经 Q1 验证）是最保守 baseline；**A 经验凸包**允许有来源的插值，但预测误差须按凸包内外核验；**B 受控局部外扩**须在 Q1 留出证实外推精度并预先定义距离、扰动与不确定性；**C 单域经验上下界**只能作边界辅助，不能代替联合支持域；**D 低维配比流形**须有可解释参数化与逆映射、留出稳定性。完整 simplex 只作理论参照，不把角点叫现实最优。现实供给、许可证、可得 Token 仍未核，所以“数据支持解”也不等于“可实施解”。

## 12 Route Decision Matrix

`Decision` 列只使用本轮约定的七类状态；“下一证据”是打开路线的门槛，不表示现已通过。

| Route ID | Question | Candidate route | Audit evidence | Decision | Reason | Risk | Required next evidence | Fallback |
|---|---|---|---|---|---|---|---|---|
| RD-01 | Q1 | A1–A3 质量描述/冲突 | 51,230/17,523/203,752 信号，ID 重叠 | KEEP AS BASELINE | 题面必用且来源可追 | 抽样/重叠偏差 | 指标方向、列表压缩、域聚合 | 透明分组评分 |
| RD-02 | Q1→Q2 | A 的独立 Q 弹性主线 | `NO_MATCHED_Q`，p/Loss 512 | DOWNGRADE | 无同运行 Q | 伪因果/别名 | 真实运行键与独立 q 变化 | F01/F02/F04 |
| RD-03 | Q1 | 现有 A4/A5 直接估 γ_Q | 无 Q 列，X_full 未测 | REJECT | 无数据列可估 | 虚构参数 | 新真实配对数据另立路线 | p 响应 |
| RD-04 | Q1 | p 的零值安全 simplex 对比 | 17 比例、45.1% 零格、合法秩 17 | KEEP AS BASELINE | 可表达训练设计 | 参考/坐标误读 | 留出与替代坐标核验 | 固定候选配比 |
| RD-05 | Q1 | R0 等权 Loss + 13 域 | PC1 22.8%、24/78 负相关 | KEEP AS BASELINE | 透明且保存异质性 | 平均遮蔽冲突 | P1-1 复核、逐域留出 | 多响应 |
| RD-06 | Q1 | PCA 单因子作唯一主响应 | PC1 22.8% | DOWNGRADE | 公共因子不强 | 域冲突消失 | 训练载荷稳定与独立用途证据 | R0+R3 |
| RD-07 | Q1 | 多响应/多目标 | 13 域异质 | CONDITIONAL | 有科学必要性 | 复杂度与解释成本 | 同 p 方向逐域效果与误差 | R0+逐域分析 |
| RD-08 | Q2 | B1 N–D baseline | 8 规模×147 相关检查点 | KEEP AS BASELINE | 真实来源内最稳健 | 伪独立样本 | 分组留出、B2/B3、B4/B5 | 源内低复杂度基线 |
| RD-09 | Q2 | A/B 绝对 Loss 直接 joint fit | 无共同标尺/运行锚 | REJECT | 来源与响应不等价 | 源偏差误当效应 | 新可核共同锚 | 分源模型 |
| RD-10 | Q2 | 相对变化/两阶段桥梁 | A p 响应与 B N–D 分源 | CONDITIONAL | 可研究运输假设 | 标准化伪可比 | Gate 2、共同方向/锚、留出 | 分源并列 |
| RD-11 | Q2 | B7 质量条件情景 | B6 嵌于 B7，E3 | CONDITIONAL | 可做半合成灵敏度 | 预置生成规律 | 生成机制与真实方向核对 | 仅符号情景 |
| RD-12 | Q2 | B8 主质量参数 | 150 组斜率全反 | QUARANTINE | 机制/定义冲突 | 反向参数污染 Q3 | B8 调查计划 | 不用 B8 |
| RD-13 | Q2 | 高维 Q×p×N 交互 | 无同粒度联合设计 | REJECT | 设计不支持 | 伪精度 | 新同运行设计+留出 | M0–M2 分块 |
| RD-14 | Q3 | 外生 L_ctx 敏感性 | C7 12/45 上限达 30k | CONDITIONAL | 题面允许情景 | 上限误当训练值 | 实训长度/代理适用性 | 架构情景注明 |
| RD-15 | Q3 | 有限观测配比候选 | A4 512 训练，检验凸包外多 | KEEP AS BASELINE | 最少插值假设 | 未必可实施 | Q1/Gate 2 与供给核对 | 固定配比 |
| RD-16 | Q3 | 完整 simplex 现实最优 | 经验覆盖有限、供给缺 | REJECT | 不能运输到角点 | 虚假可实施性 | 新响应/供给证据另立路线 | RD-15 |
| RD-17 | Q4 | Strong Loss–Benchmark Bridge | High 仅 7 同族 | DOWNGRADE | 跨族/决策域缺口 | 过强闭环 | 高可比多族留出与校准 | No Reliable Bridge |
| RD-18 | Q4 | 限族 Weak Bridge | 7 个 Pythia，68 Medium 异源 | CONDITIONAL | 有可检验小范围候选 | 小簇与标尺差 | P1-2 留族/留时及误差 | No Reliable Bridge |
| RD-19 | Q4 | 无可靠桥接时独立能力分析 | C1/C3/C4/C8 可审计但未对齐 | FALLBACK | 保留题面 Q4 主任务 | 连接较弱 | C4/C1 实体、C8、时钟 | 明示部分未达成 |

## 13 Allowed to Model Now

“现在”指 **Opus 审议并确认路线后可进入的受限规格/基线工作**；本 Round A 本身不做参数估计。允许：A1–A3 全量质量信号预处理、描述评分和冲突结构；A4/A5 的零值安全 p 设计与 R0+13 域响应基线规格；B1 的来源内 N–D baseline 规格与分组留出计划；A/B 分源、B6/B7 E3 情景、C7 外生长度和 C 数据实体对齐的预注册与审计。允许在原件只读、使用前合同冻结后继续必要代码与数据处理。所有输出必须标来源/用途，不提前升为 VALIDATED。

## 14 Not Allowed Yet

本轮及未过后续门槛前禁止：拟合真实独立质量弹性；把 A/B 绝对 Loss 直接合并；用 B8 估主参数；由 B6/B7 生成关系宣称真实 Q 效应；使用 A6–A11 Loss 调整 R0 权重；把 PCA 一因子当全部 13 域；Q3 完整 simplex 或 Q/N/D/p 无限制联合最优；把 C7 架构上限叫真实训练长度；Strong Bridge；把 Q4 残差叫纯因果技术进步；正式预测、论文数字或 ACTIVE FINAL MODEL。

## 15 Candidate Innovation Update

优先保留三个**可由后续证据支持的候选**：① Q 描述与可识别 Q 效应分离，明确 `NO_MATCHED_Q` 后的安全 Q1→Q2 接口；② 把 17 域 compositional p 的零值、支持域与 13 域冲突一并纳入可检验响应；③ 用 E1/E3/E5 分层的 N–D/配比/质量情景与误差传播回答广义标度律。它们目前只是路线优势，不宣称最终创新或性能增益。Support-aware Q3 优化和 No/Weak Bridge 下的 Q4 前沿叙事有潜力，但须先通过 Gate 2–4 和实体/成本证据；复杂参数数量本身不算创新。

## 16 Remaining Evidence Needs

按依赖优先：A1–A3 22 指标方向、8 列表压缩、抽样与扩展重叠处理/域聚合；P1-1 主响应与检验冻结；A4/A5 p→Loss 的留出支持及现实域供给；A/B tokenizer、验证语料和可能的同模型锚；B8 生成器/Q 定义冲突；B1 独立簇与 B2/B3、B4/B5 验证口径；C7 实训长度；C1/C3/C4/C8 名称、版本、时间与开源权重对齐；C5/C6 的来源分层、留族/留时误差与区间校准。`01_data/processed/` 尚无冻结输入，完整 DATA_AUDIT 结构门槛未过。

## 17 Proposed Gate-1 Status

**建议 OVERALL GATE 1 = CONDITIONAL PASS（路线层级）**：七项审计都给出了可追溯的安全分叉，因而 Q1 质量/领域结构和 Q2 分源基线可继续规格化；其中 AUDIT-01 的 PASS 是“确认没有同运行 Q”，不是独立 Q 通过。Q1 主响应 P1-1、B8、A/B 标尺、p 供给、C 实体匹配和完整九维审计仍限制下游。项目当前的 `CONDITIONAL / NOT FULLY CLEARED` 保持不变，直到 Opus 复核、使用前合同冻结和后续数据门槛满足；`stage_gate.py` 对完整 DATA_AUDIT 的结构预检因无 processed 输入仍报 `MISSING_STRUCTURE`。不得把本建议改成整项目或 Gate 2/3/4 PASS。

## 18 Questions for Opus

1. `NO_MATCHED_Q` 下，Q1→Q2 的**分阶段双轨**是否足够回答题面“同时包含 N,D,Q,p”的要求？如认为不足，请给可审计的强于条件情景的桥梁证据，而非要求伪拼表。
2. 是否认可将 C17 的 M0–M3 **证据升级原则保留**、具体候选顺序改为“B1 N–D → A p 分源修正 → E3 Q 条件情景 → 少量交互”？若不认可，指出哪个真实同粒度数据支持先上独立 Q。
3. P1-1 的 R0 原始等权 + R3 强制逐域是否足够透明？A5 域方差相差较大、PC1 仅 22.8%；在看 A6–A11 留出结果前，有无更可辩护的主响应权重或多响应优先理由？
4. B8 应保持 QUARANTINE 还是现在就判为独立机制 stress test？请给生成器/定义层证据要求，并审查 [调查计划](../../10_review/B8_CONFLICT_INVESTIGATION_PLAN.md)的出口。
5. `No Reliable Bridge yet` 是否是比 `Weak Bridge` 更准确的当前主张等级？7 个同族 High 点在什么预注册留出/区间条件下可支持严格限定的 Weak？
6. Q3 有限 A4 配比集合能否作最保守 baseline；经验凸包内插、舍入包络和现实供给应如何分层？
7. 是否同意 Gate 1 **路线层级 CONDITIONAL PASS**，同时完整 Data Audit 仍未完成、无 processed、无正式模型估计？若不同意，请具体指出会阻断 Q1/Q2 受限规格工作的证据缺口。
