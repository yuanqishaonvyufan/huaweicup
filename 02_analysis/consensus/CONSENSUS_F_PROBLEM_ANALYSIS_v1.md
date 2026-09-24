# CONSENSUS_F_PROBLEM_ANALYSIS_v1

版本：DISCOVERY-CONSENSUS-v1；状态：ACTIVE RESEARCH-DESIGN CONSENSUS。来源为 [v1.1 修正版](JOINT_F_PROBLEM_SYNTHESIS_v1_1.md)、[Opus Final Check](../opus/OPUS_FINAL_CHECK_v1.md)、[P0 设计级关闭报告](../../10_review/P0_CLOSURE_REPORT_v1.md)及官方题面/数据说明的可见正文。本文件确认研究设计和证据边界，**不确认任何 Q1–Q4 最终模型、系数、实验值或论文结论**。

本文件的唯一计数源：§4 的 C01–C22 为 CONFIRMED，§18 的 D01–D14 为 DATA_AUDIT_REQUIRED，§19 的 R01–R12 为 REJECTED。其他 CANDIDATE、OPEN、FALLBACK 条目在各节单独编号；正文重复解释不重复计数。CONFIRMED 须注明 OFFICIAL、MATHEMATICAL-CONDITIONAL 或 DESIGN-CONSENSUS，不把内部方法原则冒充赛题原文。

# 1 Consensus Status

| 状态 | 含义 | 当前约束 |
|---|---|---|
| CONFIRMED | 题面/数据说明直接事实，或双方通过条件代数和设计级复核同意的研究合同 | 可作为下一阶段约束；不表示经验模型通过 |
| DATA_AUDIT_REQUIRED | 需要读取、配对和检查实际 A/B/C 数据才能选择 | 不得先填结论；七项路线审计优先执行 |
| CANDIDATE | 保留的评分、响应、模型或可行域路线 | 不等于 ACTIVE 模型 |
| OPEN | 即使审计后也可能需要进一步拟合、留出验证或文献支持 | 继续追踪，不强行收敛 |
| REJECTED | 与题面、已核字段或条件数学推导冲突的具体做法 | 不作为默认路线；新证据须走决策日志 |
| FALLBACK | 主路径不成立时预定的保守退化路径 | 仍须完成题面必用任务与验证 |

P0-1 的“缺秩检验输出决策树”已 **CLOSED — DESIGN LEVEL / AWAITING EMPIRICAL AUDIT**；Opus Final Check 判定 PASS。14 个非真实样例只验证分支器逻辑覆盖和程序路由，**不构成任何关于 F 题真实数据可识别性、统计性质或模型有效性的证据**。真实 Q/p 是否独立可识别仍 OPEN。

# 2 Executive Consensus

F 题要在有限算力下理解数据质量 Q、17 域配比 p、参数规模 N、训练 Token D 与验证交叉熵 Loss 的关系，并把资源配置与现实 Benchmark 能力演进谨慎相接。Q1 先测量质量、冲突和配比响应；Q2 在不同来源数据的证据边界内建立条件广义损失关系；Q3 用经验证的响应和题面成本代理讨论可行配置及是否存在制度转移；Q4 以 C 数据分析开放模型的规模相关与条件非规模能力变化、Loss–Benchmark 映射和 12/24 月前沿。

当前机制主链最强的是 Q1→Q2→Q3。A 的质量信号/配方 Loss、B 的规模轨迹、C 的榜单和桥接不是同一次实验；完整四维 L(N,D,Q,p) 与 Q3→Q4 强定量桥接都须通过真实数据审计和后续验证。最大的结构风险是固定域质量下 Q_eff 可能只是 p 的确定函数：此时不存在从 A 配方实验中分离质量和配比两个自由效应的证据。半合成 B6–B8 不能替真实质量干预。

可以进入 DATA AUDIT — PHASE 1，是因为输入角色、可识别性决策树、失败分支、六项 P1 使用前合同及四道 Gate 已具备，且 Opus Final Check 放行设计阶段。现在仍不能选最终模型，是因为逐运行 Q 是否存在、A/B Loss 可比性、13 域响应、p 支持、C7 可行长度、C5/C6 桥接、Q4 时间和类型口径都没有实测审计。若 Strong Bridge 不成立，§14 的 Conservative Story 是正式 FALLBACK；它要求完整回答各问并如实披露弱连接，不能用“保守”跳过题面任务。

# 3 Unified Problem Architecture

    A1–A3 质量信号 ─→ Q1：Q/q、冲突、尺度与误差 ──────────┐
    A4–A15 配比与 13 域 Loss ─→ Q1：p 响应与留出边界 ──┼→ Q2：受限/条件 L(N,D,Q,p)
    A16 参考映射 ─→ 质量域到配方域的可追踪关系 ───────────┘       ↑ B1 主拟合；B2/B3、B4/B5 分级检验；B6–B8 半合成
                                                                     ↓ 已识别参数、导数、支持域与误差
    附录 B 成本 + C7 外生 L_ctx ───────────────────────────→ Q3：预算约束资源配置和转移检验
                                                                     ⇢ Q4：条件能力情景，桥接强度待证
    C1/C2、C3、C4、C8 ───────────────────────────────────→ Q4：独立历史能力分解与前沿
    C5/C6 或可核验文献 ─────────────────────────────────→ Q4：分层 Loss–Benchmark 桥接

“⇢”是待验桥接，不是已观察到 Q3 最优配置的真实能力。Q1 的质量测量与配比实验也需运行级接口才能独立估计 Q 效应。任一上游数据口径或 ACTIVE 版本变化，须使其下游模型、实验、图表和论文结论进入重检。

# 4 Confirmed Facts and Principles

以下 22 条是本共识的 CONFIRMED 唯一计数表。OFFICIAL 来源于题面/可见数据说明；MATHEMATICAL-CONDITIONAL 为明确前提下的代数；DESIGN-CONSENSUS 为双方确认的研究程序和陈述边界。

| ID | Status | 来源级别 | 已确认内容 |
|---|---|---|---|
| C01 | CONFIRMED | OFFICIAL | 四问按质量/配比→广义 Loss→预算配置→现实能力演进递进；具体模型、指标和求解方法需说明依据。 |
| C02 | CONFIRMED | OFFICIAL | Q1 对 22 质量指标必要预处理且方向统一为越高越好；A1 与 A2/A3 全量使用，抽样与扩展域级 Q 要对照并处理冲突。 |
| C03 | CONFIRMED | OFFICIAL | Q1 用 A4–A15 建 17 域 p 与交叉熵 Loss 的关系；p_i≥0、Σp_i=1。 |
| C04 | CONFIRMED | OFFICIAL | A6–A11 为 Q1 检验，A12–A15 为估算外推讨论；估算 Loss 不等于真实独立观测。 |
| C05 | CONFIRMED | OFFICIAL | 17 个训练域比例对应 13 个验证域 Loss；题面没有指定 13 域综合 Loss 的最终权重。 |
| C06 | CONFIRMED | OFFICIAL | Q2 以 B1 为经典部分主要拟合，B2 或 B3 做指定辅检，B4/B5 跨族/文献检验；B6–B8 质量补充为半合成，B9/B10 用于大尺度讨论。 |
| C07 | CONFIRMED | OFFICIAL | A 与 B 实验独立；共享“交叉熵损失”名称不足以确认绝对标尺、验证集和 tokenizer 相同。 |
| C08 | CONFIRMED | OFFICIAL | Q3 的 L_ctx 是外生给定情景，取值依据 C7；题面成本含 C_train=6ND、C_Q 和 C_attn=ηNDL_ctx，至少比较三个不同量级预算。 |
| C09 | CONFIRMED | MATHEMATICAL-CONDITIONAL | 在题面代理式、N,D>0 且固定 L_ctx 下，C_attn/C_train=ηL_ctx/6 不随预算 C 单独变化；6/η≈30,000 token 是 PROVISIONAL ANALYTIC THRESHOLD，是否落在 C7 可行域尚未知。 |
| C10 | CONFIRMED | OFFICIAL | Q4 须用 C1 或 C2 与 C3、C4 关键元数据、C8 至少一项逐任务聚合；Loss–Benchmark 映射须按可比性分层并给误差与预测不确定性。 |
| C11 | CONFIRMED | DESIGN-CONSENSUS | Q1→Q2 必须传质量定义、尺度/误差、域映射等级、p 与配比响应的证据性质；不能预先声称 Q 是独立标量效应。 |
| C12 | CONFIRMED | DESIGN-CONSENSUS | Q2→Q3 只传通过相应识别、留出和有效域门槛的 Loss 关系、参数/区间与边际信息；未识别质量项只能作情景。 |
| C13 | CONFIRMED | DESIGN-CONSENSUS | Q3→Q4 仅有待验桥接；Strong、Weak、No Reliable Bridge 是结论强度的三个合法分支，现不确认 Strong。 |
| C14 | CONFIRMED | MATHEMATICAL-CONDITIONAL | 在线性自由 p 效应且固定 q 的 Q_eff=pᵀq 情况，Q 列落入 p 设计空间；p⊙q 不创造真实独立质量变化。 |
| C15 | CONFIRMED | DESIGN-CONSENSUS | 秩检验须合法处理 simplex 的闭合约束；full rank 不等于强识别，预测增益也不自动等于因果质量干预。 |
| C16 | CONFIRMED | DESIGN-CONSENSUS | 真实直接观测、经审计可比的跨源、半合成、模型内部推断、外推/情景需分层陈述；B6–B8 不可写成真实训练实测。 |
| C17 | CONFIRMED | DESIGN-CONSENSUS | Q2 按 M0 经典基线→M1 质量→M2 配比→M3 有依据少量交互逐级提出候选；升级靠同口径留出、残差、稳定与族外证据，不靠训练拟合改善。 |
| C18 | CONFIRMED | DESIGN-CONSENSUS | Q1 的 13 域响应须保留 PRIMARY RESPONSE 候选与 DOMAIN HETEROGENEITY 分析两层，权重在审计后、保留集使用前冻结。 |
| C19 | CONFIRMED | DESIGN-CONSENSUS | Q4 不把所有规模控制后的残差直接称纯技术进步；association、decomposition、contribution、causality 必须区分。 |
| C20 | CONFIRMED | DESIGN-CONSENSUS | GATE 1–4 设 PASS、CONDITIONAL、FAIL 与 fallback；未经对应 Gate 的高传播风险输出不得作为下游正式输入。 |
| C21 | CONFIRMED | DESIGN-CONSENSUS | P0-1 仅设计级关闭；审计规范与分支器已备。14 个非真实样例只证明逻辑覆盖，不证明 F 题真实数据通过识别。 |
| C22 | CONFIRMED | DESIGN-CONSENSUS | P1-6 的 Conservative Story 被确认为 FALLBACK 研究合同；它仍须覆盖题面必用数据、每问验证和桥接误差，证据不足时如实写出部分未达成。 |

# 5 Q1 Consensus

**任务冻结（C02–C05）**：Q1 测量样本/域级质量并消解指标冲突；在 simplex 上研究 17 域配比对验证 Loss 的响应，用 A6–A11 验证并把 A12–A15 仅作估算外推讨论。A1 的文本可作语义核验；A2/A3 缺 content 时只能在可追溯条件下恢复原文或明确只复核信号层。四个训练域没有同名验证 Loss 列，不等于其比例变化对其余响应没有作用。

**CANDIDATE K01**：质量评分从方向一致、透明等权/分组等权 baseline 起，相关结构可解释时比较 PCA/潜变量；用下游 Loss 监督赋权须独立训练与嵌套验证，不能循环定义独立质量效应。未经有界标定的 z 分数不直接作为 Q3 所需 Q∈(0,1]。冲突候选可用方向统一后的指标离散、预定义对立组排序反转或潜变量残差；阈值和处置规则待审计。

**CANDIDATE K02**：13 域 Loss 的透明综合主响应与完整 13 维异质性并行；若综合尺度或任务含义不可比，则以多响应/多目标为主。主权重、零配比处理、p 对比坐标及交互强度保持 DATA_AUDIT_REQUIRED（D01–D05）。A4/A5 的配方/运行 index 是分析单位；p 是该运行的 17 维配比，不混用术语。

# 6 Q1→Q2 Interface

Q1 正式交付应包含：Q/q 定义、方向与尺度、评分和域聚合版本、冲突量/规则、样本与域不确定性；p 的 17 域列与 simplex 参数化、A16 映射等级；各验证 Loss 响应和 A6–A11 留出误差；真实/估算/辅助标签；以及是否有与同一配方运行配对的 Q_r。缺少最后一项时，Q1 仍能向 Q2 传“质量测量”和“配比响应”，但不得传“真实独立质量系数”。

**CANDIDATE K03 — 四条接口**：A 独立标量 Q（须真实运行级独立变异和识别）；B 带映射误差的领域质量向量 q；C p⊙q 等联合编码（无独立 Q 效应）；D B6–B8 半合成/外部假设下的质量情景。最终选哪条及能否并用，由 AUDIT-01、AUDIT-02 与 GATE 2/3 决定。

# 7 Q2 Consensus

**任务冻结（C06–C07、C17）**：Q2 需建立涉及 N、D、Q、p 的可解释条件广义损失关系，分析边际效用、弹性、领域替代/互补及质量与规模局部替代，并估参、检验、验证。A/B 不能按行拼接或默认同一生成机制；B1 真实训练轨迹、B2 半合成或 B3 插值辅检、B4/B5 跨族/文献核验、B6–B8 半合成质量补充和 B9/B10 大尺度讨论，各承担不同证据等级。

**CANDIDATE K04 — 逐级模型族**：M0 题面经典加性 N–D 基线；M1 有识别依据时加入质量效应，否则只作情景；M2 接经验证的领域/配比修正；M3 仅在新增交互有设计覆盖与留出增益时开放。M0→M3 是研究问题的递进，非不同 A/B 表天然共享的一套似然；AIC/BIC 只用于相同响应与样本的可比规格。最终函数、源别锚定、Q=1 等退化约束和质量参数证据等级都未确认（D06–D08）。

若真实数据只能支持 N–D 部分和固定尺度的 p 响应，Q 的半合成变化只能给条件质量修正及其局部替代边界；不得把变量齐全的形式等同于真实数据已独立估出每个系数。题面广义关系要求仍需以清楚的条件函数、参数来源、适用域和失败的识别分支如实回答。

# 8 Q2→Q3 Interface

仅 GATE 3 准许的模型版本、参数区间、源别 Loss 口径、N/D/Q/p 支持域、验证误差和可计算边际量可进入 Q3。质量提升等效于参数增加的数值必须说明固定 D/p、比较基点、两项偏导的符号与不确定区间；若质量系数仅半合成，则等效量和 Q3 质量投资也是情景结果。失败时传经验证 N–D/配比分块与 Q 的条件范围，不传伪精确一体化曲线。

# 9 Q3 Consensus

**任务冻结（C08–C09）**：在预算 C 下研究 N、D、Q、p 的可行配置，比较指数/幂/对数渐进质量成本，至少三个不同量级预算，给结构性转移可计算定义和 C7 可行 L_ctx 敏感性。L_ctx 只作外生情景；不预设 N/D/Q/p 全是无限制连续自由变量。

**CANDIDATE K05 — p 可行域层级**：完整 simplex 仅用于理论参考；A4 观测支持/凸包、经审计的局部扩展、带真实供给上下界的可实施域，须分开比较。p 亦可由 Q1 固定或限定候选/低维参数化，题面允许说明理由后采用；高维自由优化只有在预测支持足够时才考虑。不能把经验凸包或任意距离阈值冒充官方硬约束。

**CANDIDATE K06 — 转移判据**：Primary 候选为有证据支持的固定外生约束/投入制度在预算扫掠中稳定改变；份额弹性和边际投资排序仅作佐证。预算约束若始终活跃不算转移，固定真实上界在制度切换中也可能重要；人为随 C 移动的边界或数值容差伪开关不算。若无稳定变化，可正式报告“在所定义判据下未检出结构性转移”。

题面代理式给 C_attn/C_train=ηL_ctx/6，因此 6/η≈30,000 token 是 **PROVISIONAL ANALYTIC THRESHOLD**；它是给定成本式的条件算术结果，C7 是否覆盖、架构上限是否为真实训练长度均未审计。固定 L_ctx 下只增预算不会让这两项成本比自动翻转。正式预算网格和 g(Q) 主用方式仍属 D09–D10。

# 10 Q3→Q4 Scenarios

**CANDIDATE K07**：Strong Bridge 须在高可比层有足够覆盖、稳定的样本外映射和可传播的预测区间，才允许把 Q3 Loss 情景解释为限定模型类型/规模的 Benchmark 区间。Weak Bridge 只允许有限子群或宽区间趋势。No Reliable Bridge 时，Q3 报 Loss/成本，Q4 以 C 数据独立完成历史能力与前沿分析，明确两链不能强定量闭合；不得叫 Q4 为 Q3 最优策略的外部验证。三场景是事前**分支规则**，不是当前三种实验结论（D11）。

# 11 Q4 Consensus

**任务冻结（C10、C19）**：Q4 定义六维或逐任务能力、开源筛选、pretrained/chat 类型和统一时间轴；用 C1 或 C2、C3、C4、C8 分析规模相关与条件非规模变化，给算力放缓情景的 12/24 月开放模型前沿和不确定性；C5/C6 或可核验文献用于 Loss–Benchmark 映射及误差。

**CANDIDATE K08**：透明描述性/条件回归作基准；Oaxaca 型、家族/时间固定效应、frontier/time 效应或在足够可比时序下的状态空间为备选。Scale 可考虑 (log N,log D)、log C，或避免重复的联合尺度/形状参数化；若 C≈6ND，不同时把 log N、log D、log C 无约束当三个可分贡献。非规模部分是控制已测规模后的条件时间/边界变化，可能混入遗漏、对齐、数据工程和评测变化；无识别设计不能说成纯技术因果效应。主规模变量、时钟、类型/许可证口径、模型族、桥接强度和前沿预测法均待真实数据（D11–D14）。

# 12 Identifiability Consensus

**C14–C15 的条件数学已确认，经验结果未确认。** 若 q 在配方运行间固定且 Q_eff=pᵀq，自由线性 p 设计已张成 Q_eff 列，独立质量系数不能由这些运行辨识；p⊙q 是联合表示而非独立干预。即使另一非线性 Q=f(p,q) 在受限回归中数值满秩，跨质量水平的独立反事实仍非 A 实验提供。17 比例加截距的必然依赖先用合法 16 维 simplex 对比消除；之后再区分结构别名、其他规格秩亏、经验共线、弱识别与共同支持不足。

审计按 [IDENTIFIABILITY_AUDIT_SPEC](../../01_data/IDENTIFIABILITY_AUDIT_SPEC.md) 的 Step 0→A→B→C→D→E→F 执行，保存配对/秩/精度/支持/样本外来源证据及分支器 Q2_ACTION/Q3_ACTION。预测增益最多支持统计增量信息，因果质量效果仍需外生性。P0-1 的设计关闭不替代 AUDIT-01 的实测分支。

# 13 Evidence Hierarchy

以下 E1–E5 是项目内部证据标签，且“来源真实性”与“跨源可比性”应分别登记；一份表可按行或模型族分层。

| 等级 | 当前合同 | 例子与可用范围 |
|---|---|---|
| E1 真实直接实验/公开观测 | 只在其原测量环境支持陈述 | A 真实质量/配方 Loss、B1 真实轨迹、C 排行榜/元数据；不自动跨源可比 |
| E2 跨源且已验证可比 | 须有共同目标、来源和留出证据 | 审计后 B4/B5 或 C5/C6 的合格子集；不能给全表一律 E2 |
| E3 真实规律校准的半合成 | 可作条件估计/压力测试，单独标生成机制 | B2、B6–B8；B3 插值须另附 INTERPOLATED 标签 |
| E4 模型内部推断 | 依赖已估参数/规格，不能作为新观测真值 | 拟合函数、导数、局部弹性和模型内区间 |
| E5 外推、情景、优化或未来预测 | 需说明范围、上游误差与条件 | A13/A15、B10、Q3 最优配置、Q4 未来前沿 |

禁止把 E3 写作 E1，或把 E4/E5 写成真实实验结果；B6–B8 的质量参数若是主要来源，后续只能写“半合成校准情景下……”并列真实证据缺口。

# 14 Conservative Story

**CONFIRMED FALLBACK STORY（C22，设计级）**：即使真实配方中没有可独立识别的 Q、Strong Bridge 失败且 17 维 p 自由优化不可靠，仍按题面逐问完成：Q1 对 A1–A3 全量建立可解释质量与冲突规则、对 A4–A11 建有留出检验的配比响应；Q2 以 B1 真实 N–D、A 的可验证配比关系及明确 E3 的质量情景构成条件广义损失关系，报告可识别与不可识别的弹性/替代条件；Q3 在可验证的低维或固定配比域内比较三类质量成本、至少三个不同量级预算与 C7 外生长度，并可报告“未检出稳健结构转移”；Q4 使用 C1 或 C2、C3、C4、C8 建独立能力演化与 12/24 月不确定前沿，按 C5/C6 或可核文献尝试并评价 Loss–Benchmark 映射。

若桥接不能运输，No Reliable Bridge 是有效的科学发现：报告失败的可比性/样本外证据，把 Q4 作为现实能力研究而非 Q3 优化的实测验证；不得把这说成已经完成强定量闭环。若连题面要求的映射本身都无法建立，应明确部分任务未完全满足、寻求可靠文献或重审数据，不用“Fallback”掩盖。所有必用附件和对应验证仍须执行。

| ID | Status | 触发与安全行动 |
|---|---|---|
| F01 | FALLBACK | Q 与 p 真实独立效应不可识别 → 只报告可验证的联合配比—质量响应，不单列真实 γ。 |
| F02 | FALLBACK | 缺真实 Q 变化 → 固定 p 或 Q 假设作条件情景，显式说明不可观测反事实。 |
| F03 | FALLBACK | B6–B8 是唯一质量变化来源 → 单列半合成校准区间/灵敏度，不称 E1。 |
| F04 | FALLBACK | 实际审计/留出不支持独立质量弹性 → 从经验主模型删该点参数，保留可解释的条件数学关系与局限。 |
| F05 | FALLBACK | Q3→Q4 无可靠桥接或 p 高维失稳 → 按本节保守四问主线完成，桥接失败作为受限结论报告。 |

# 15 Stage Gates

Gate 状态为 PASS、CONDITIONAL、FAIL；这是下一阶段执行规则，不是当前 Gate 的实测判定。具体指标、误差容限和支持域需在看到保留集结果前依噪声、有效簇数和研究用途预注册；不得套外部建议中的固定常数。

| Gate | PASS | CONDITIONAL | FAIL 与 fallback |
|---|---|---|---|
| GATE 1 — DATA AUDIT | 七项路线审计有可追溯文件/字段、配对/秩分支、单位/来源标签；当前要用的必用数据可读且角色冻结 | 无真实配方级独立 Q、A/B 部分不可比或桥接范围有限，但原因和安全分支明确；准许带条件的后续规格 | 来源/键/泄漏不明或必用数据无法核查：先修复/声明缺口，禁止把 Q/p、Loss 或桥接当正式输入；走 F01–F04 或退回审计 |
| GATE 2 — Q1 VALIDATION | 质量规则在 A1–A3 的规定范围复现，A4/A5 模型在 A6–A11 的预注册目标/域别误差和跨规模留出有足够支持 | 仅部分域、配比或规模有稳定响应：向 Q2 传限制范围、q/p 分开及误差 | 评分或配比关系无可用留出证据：返工预处理、响应或规格；不向 Q2 传普适质量/配比系数 |
| GATE 3 — Q2 IDENTIFICATION | 拟进入 Q3 的每一参数有来源/秩/精度、B1 分组留出及 B2 或 B3、B4/B5 的分级核验；Q/p 新项的适用域和误差明确 | 只验证 N–D 或局部 p；半合成 Q 可作情景：Q3 接受区间/情景和支持域限制 | M0 或目标口径系统失配：不得据此做确定性 Q3 最优；重审 Loss 可比性/源别规格 |
| GATE 4 — Q3/Q4 BRIDGE | 高可比桥接在相关模型类型、Loss 和 Q3 预测域有稳定留出映射及校准区间 → 允许 Strong 声明 | 有有限子群关联或误差较大 → Weak，仅报告限定范围情景 | 无可靠运输 → No Reliable Bridge；Q3 报 Loss/成本，Q4 独立报能力，禁称 Q4 为 Q3 实测验证 |

GATE 4 的 FAIL 是“强桥接不成立”，不必等同全题失败；仍须按题面尝试映射、分析误差并记录不能运输的证据。高传播风险数据若某 Gate 仅 CONDITIONAL，其下游状态也必须明确 CONDITIONAL，不得被摘抄成无条件结论。

# 16 High-Propagation-Risk Variables

| 对象 | 最早需通过的 Gate | 若失败的下游传播 |
|---|---|---|
| Q 定义、方向、域映射与误差 | GATE 1，再 GATE 2 | Q2 质量项、Q3 质量成本收益、Q4 情景解释失真 |
| Q/p 独立接口与分支状态 | GATE 1 的真实秩/精度/留出，再 GATE 2/3 | 独立弹性、质量—规模等效与 Q3 质量最优伪精确 |
| 13 域 Loss 主响应/权重 | GATE 1 预注册，GATE 2 验证 | Q2 标尺、Q3 目标及桥接目标不一致 |
| Scaling Law 参数及适用域 | GATE 3 | Q3 最优配置和预算转移不可信 |
| p 可行域和现实供给 | GATE 1，Q3 可行性验证 | 理论角点被误报为可实施配置 |
| Loss–Benchmark 映射与误差 | GATE 4 | Q3 优化结果被误写成现实 Benchmark 能力 |

未过门槛的版本可用于标明假设的探索或情景，但不能进入下游 ACTIVE 正式输入；上游修订时下游结果/图表/论文引用须回退重检。

# 17 P1 Tracking

P1-1 至 P1-5 的**规则设计已获双方确认**，其具体数据校准和实证结论仍未完成；P1-6 已确认的只是 Conservative Story 的设计级最低内容，不是今后所有实际数据都会使论文完整达标。

| P1 | 当前 Status | 使用前必须完成 | 失败/不足时 |
|---|---|---|---|
| P1-1 13 域 Loss 权重 | DATA_AUDIT_REQUIRED | 审计尺度与用途，比较原始等权、训练部分标准化综合和可解释低维候选；冻结权重并保留 13 域异质性 | 多响应/多目标升为主口径，不能用 A6–A11 调权重 |
| P1-2 Strong Bridge | DATA_AUDIT_REQUIRED | 高可比层、有效家族/规模/类型覆盖、留族/留时误差、区间校准，在 GATE 4 前注册判断规则 | 降 Weak/No，不硬给能力点预测 |
| P1-3 p 现实供给 | DATA_AUDIT_REQUIRED | 核对经验支持、许可证、可得性/总量与外部供给界，在 Q3 前区分理论/数据内/可实施解 | 只称理论或数据支持情景 |
| P1-4 Q4 规模变量 | DATA_AUDIT_REQUIRED | 审计 N/D/C 的覆盖、时间完整性、秩与共线，在能力拟合前选不重复的主集合 | 报联合规模项，不分摊不可分系数 |
| P1-5 非平凡转移 | CANDIDATE / 后续验证 | 在 Q3 求解前固定约束来源与活跃制度判据，核极端集中、零投入、近多解和扰动 | 报无稳健转移或仅条件性边界切换 |
| P1-6 保守主线最低内容 | CONFIRMED FALLBACK STORY（设计级） | 仍须实际完成 Q1–Q4 必用数据、条件关系、成本配置、能力预测及映射误差分析 | 任一必用任务无法完成则如实标部分未达成并返工，不称完整闭环 |

# 18 NOT_YET_CONFIRMED

以下 D01–D14 是 DATA_AUDIT_REQUIRED 的唯一计数表。不能因 Opus Final Check 通过设计而填任何一项的经验结果。

| ID | Status | 需要实际审计后才可决定 |
|---|---|---|
| D01 | DATA_AUDIT_REQUIRED | A1–A3 的指标方向、列表压缩、缺失、评分尺度与扩展域稳定性；Q 的最终定义和 (0,1] 标定。 |
| D02 | DATA_AUDIT_REQUIRED | A4/A5 是否存在同运行可追溯 Q_r、Q 相对 p 的独立变化、合法设计秩/精度/样本外增益及真实分支结果。 |
| D03 | DATA_AUDIT_REQUIRED | A16 的 7 质量域到 17 配方域映射覆盖、direct/near/inferred 不确定性及 q 向配方运行的传递。 |
| D04 | DATA_AUDIT_REQUIRED | 13 域 Loss 尺度/相关性、主响应权重、原始综合/标准化/低维候选与逐域异质性的选择。 |
| D05 | DATA_AUDIT_REQUIRED | A4/A5 index、零配比/闭合，A6–A11 留出支持与 A12–A15 估算来源；p 的正式可预测区域。 |
| D06 | DATA_AUDIT_REQUIRED | A/B Loss 的验证集、tokenizer、模型族和绝对标尺可比性；B1/B4/B5 重叠与外部验证有效性。 |
| D07 | DATA_AUDIT_REQUIRED | B6–B8 的 Q_score 生成、N/D/Q 设计变化、与 Q1 尺度对齐及质量项仅半合成还是有额外真实支持。 |
| D08 | DATA_AUDIT_REQUIRED | p 的观测凸包、真实域供给/许可/数量与可实施上下界；Q3 固定、候选、低维或联立形式。 |
| D09 | DATA_AUDIT_REQUIRED | C7 实际上下文范围、架构上限与训练使用长度、30,000 token 代理阈值是否位于可行情景。 |
| D10 | DATA_AUDIT_REQUIRED | C5/C6 的 Loss 来源、高/中可比层、独立模型族与 Q3 域覆盖、留出误差；Strong/Weak/No 的实际归类。 |
| D11 | DATA_AUDIT_REQUIRED | C1/C2/C3/C4/C9 的模型匹配、重复、Type、开放权重/许可证、日期与 N/D/C 规模字段缺失和共线。 |
| D12 | DATA_AUDIT_REQUIRED | C8 逐任务 JSON 的可解析/版本选择、六维聚合与榜单一致性；Q4 综合能力度量。 |
| D13 | DATA_AUDIT_REQUIRED | Q3 的 N/D/Q 原始单位、Q0、成本数量级、可行预算与至少三档正式网格及成本函数比较。 |
| D14 | DATA_AUDIT_REQUIRED | Q4 预测统一时钟和 t=0、规模变量主集合、开放模型筛选与前沿预测支持范围。 |

以下更深的研究问题仍 OPEN，即使 D 项审计完成也可能需要模型检验或新的证据：O01 真实质量干预的因果效应；O02 唯一可运输的完整 L(N,D,Q,p) 是否存在；O03 预算路径有无稳健结构性转移；O04 非规模“技术进步”的因果份额；O05 Strong Bridge 是否成立；O06 No Bridge 情况下题面映射要求能否得到充分的有界回答。OPEN 不得被“数据文件存在”自动关闭。

# 19 REJECTED

以下 R01–R12 是已由代数、题面、数据性质或证据伦理排除的**具体做法**；不是排除整个研究问题。

| ID | Status | 正式排除的做法与依据 |
|---|---|---|
| R01 | REJECTED | 固定 q 时把 p⊙q 或 pᵀq 当作独立于 p 的真实质量实验；它们由 p 决定。 |
| R02 | REJECTED | 用标准化、PCA、正则化或仅改变坐标声称修复结构性不可识别；这些不创造独立运行级 Q 变化。 |
| R03 | REJECTED | 带截距直接使用 17 个闭合比例，再把必然秩亏解释为额外数据质量问题。 |
| R04 | REJECTED | 未核验证集/词表/来源便把 A 与 B 的 Loss 绝对值直接合并拟合。 |
| R05 | REJECTED | 将 B2、B6–B8 的半合成或 B3 插值称为真实直接训练实验。 |
| R06 | REJECTED | 用 A13/A15、B10 或同模型生成预测值反向验证该模型的真实外推准确率。 |
| R07 | REJECTED | 没有真实设计覆盖和稳定留出就加入全部 Q×N、Q×p、N×p 等高维交互。 |
| R08 | REJECTED | 把 Q4 所有未解释残差无条件称为纯因果技术进步。 |
| R09 | REJECTED | 为让论文闭环而强制建立未经可比性和样本外检验的 Loss–Benchmark 映射；No Bridge 时称 Q4 为 Q3 外部验证。 |
| R10 | REJECTED | 在固定 L_ctx 的题面代理成本下声称仅预算 C 增加会改变 C_attn/C_train 的比值。 |
| R11 | REJECTED | 用未校准的固定样本数、相关系数、R²、ε 距离等作官方或项目自动放行阈值。 |
| R12 | REJECTED | 在 A4 不存在的训练域列上选择参考域，或在未核 A16 关联时把“近似域”代理当真实对应验证 Loss。 |

# 20 Route-Decision Audit Questions

DATA AUDIT — PHASE 1 先回答下列七问，不等于跳过其他必用数据的后续完整九维审计。每问要写来源路径/哈希、字段、实际诊断、证据等级、分支和不能作出的主张。

| ID / 优先问题 | WHY IT MATTERS | REQUIRED DATA | OUTPUT | DECISION AFFECTED | FALLBACK IF FAILED |
|---|---|---|---|---|---|
| AUDIT-01：Q 与 p 有无独立变化和可识别性？ | 决定独立质量弹性、Q2 质量项与 Q3 投入是否可经验估计 | A1–A5、A16 的同运行连接；17 p、候选 Q_r、13 Loss、评分谱系；按 IDENTIFIABILITY_AUDIT_SPEC 的合法设计 | 配对证据、秩/精度/支持/留出、机器分支结果、允许措辞 | Q1→Q2 Path A/B/C/D 与 GATE 1 | F01 联合响应、F02 情景、F03 半合成、F04 删除独立弹性 |
| AUDIT-02：A/B Loss 能否比较？ | 无共同标尺便不能把 Q1 配比修正接 B1 规模基线 | A4/A5 与 B1/B4/B5 的验证语料、tokenizer、模型族、单位、重叠来源 | 可比层/不可比层、源别偏差/锚定候选、外部验证样本清单 | Q2 joint/two-stage/分源规格与 GATE 3 | 分块条件关系，禁直接池化绝对 Loss |
| AUDIT-03：B6–B8 提供怎样的 Q 变化？ | 决定质量参数能否在半合成设计中估，及其能否运输 | B6–B8 生成说明、N/D/Q_score/val_loss、与 Q1 Q 的尺度和来源 | 生成机制、设计秩、变异/交互范围、SEMI-SYNTHETIC 标签 | M1 质量情景与 Q3 参数区间 | 若只预置质量律，保留压力测试并拒真实质量弹性 |
| AUDIT-04：13 域 Loss 的结构是什么？ | 主响应选错会改变 p 效应和 Q2 目标 | A4/A5、A6–A11 成对列、13 域尺度/相关/缺失、训练域与验证域对应 | 原始综合/训练标准化/低维候选条件、固定权重方案、13 域异质性 | Q1 主响应与 GATE 2 | 多响应/多目标；无权重依据不强造单一指标 |
| AUDIT-05：C7 L_ctx 的真实范围和阈值位置？ | 决定代理式 30,000 token 是否有现实意义及 Q3 情景 | C7 max_position_embeddings、架构/模型名、实际训练长度可得证据 | 可行长度集合、架构上限与训练长度区别、30,000 的覆盖状态 | Q3 L_ctx 敏感性与成本分项 | 仅在可行长度内报告成本比，阈值外部情景另标 |
| AUDIT-06：C 桥接覆盖、族别和时间结构？ | 决定 Q3→Q4 Strong/Weak/No 与 Q4 预测时钟 | C1/C2、C3、C4、C5/C6、C8（C9 可核）；Loss_Source/Comparability、Type、日期、开放性、逐任务 | 高/中可比子群、模型/日期匹配、独立簇、任务与 Loss 覆盖、预测可用截止 | GATE 4、Q4 规模/非规模解释和 t=0 | Weak/No Bridge；Q4 独立能力演化，误差/缺口显式报告 |
| AUDIT-07：p 的观测支持、凸包与现实上下界？ | 自由 simplex 优化易跑到数据/工程不可达角点 | A4、A6–A11、A16/A17 及可核域供给、许可、总量资料 | 训练/检验支持域、零值与凸包/局部邻域、可信供给约束和不确定性 | Q3 p 固定/低维/联立及可实施性 | 数据内或固定候选配比；理论解与可实施解分报 |

# 21 Discovery Closure Statement

DISCOVERY / PRE-MODELING RESEARCH DESIGN  
STATUS: **COMPLETE**  
CONSENSUS: **v1 ACTIVE（研究设计共识）**  
NEXT PHASE: **DATA AUDIT — PHASE 1 / ROUTE-DECISION AUDIT**

本次关闭基于题面、双方 Round 1–6 文档、P0-1 设计级关闭和 Opus Final Check PASS；仅放行真实数据审计的**开始**，不放行任何具体数学模型或数值结论。当前无 ACTIVE FINAL MODEL、无真实实验结果、无真实 Q/p 可识别性结论、无最终 Scaling Law、无最终 Q3 优化模型、无最终 Q4 分解模型。14 个非真实分支样例只证明程序逻辑覆盖，不证明 F 题数据或模型有效。
