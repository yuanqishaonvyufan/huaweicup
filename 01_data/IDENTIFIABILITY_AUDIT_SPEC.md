# IDENTIFIABILITY_AUDIT_SPEC

版本：v1，ROUND 5 研究设计修复。状态：DESIGN SPECIFICATION；尚未对 A/B/C 真实文件执行秩、拟合、重抽样或预测检验。目标是让 data-audit Skill 在实际审计时产出可被 Q2/Q3 消费的分支结果，关闭“有诊断却无建模行动”的设计缺口。原始数学依据见 02_analysis/consensus/JOINT_F_PROBLEM_SYNTHESIS_v1_1.md §5。

## Question

Q1 生成的质量 Q 与 17 域配比 p，在能够观测同一运行的 Loss 时，是否支持分离的统计质量项？若能，它是稳定的样本外**预测贡献**、仅限半合成设计的贡献，还是仍不足以作独立效应解释？本规范不把预测贡献自动等同因果干预效应。

## Required variables and observational grain

审计单位必须是一条真实配方/训练运行 r，或另有清楚的一对一运行键。不能把 A1–A3 的文本样本行与 A4/A5 的配方行机械拼接，也不能把 B1 的轨迹行与 A4/A5 的配方行填缺失后当完整观测。

| 字段 | 类型与要求 | 来源候选 | 缺失时动作 |
|---|---|---|---|
| run_id / index | 唯一配方运行键、版本/来源键 | A4/A5 的 index，若有批次/模型元数据另存 | 无法配对则 NO_MATCHED_RUN；停止“真实独立 Q 效应”检验 |
| p_r | 17 维非负且和为 1 的训练域配比 | A4（A6/A8/A10 只能按预留用途进入验证） | 不满足单纯形则先修数据合同，不能用伪行补足 |
| L_r,m | 与同一运行配对的 13 维验证域交叉熵 | A5；A7/A9/A11 保留检验 | 缺同运行 Loss 则不可估统计响应 |
| Q_r / q_r | 与该运行所用语料直接关联的质量标量或域向量，附映射版本与误差 | A1–A3、A16 只提供候选原料；是否有逐配方连接待查 | 只有固定 q 或无连接时标记 NO_MATCHED_Q / DETERMINISTIC_FROM_P |
| N_r,D_r | 参数个数和 Token 原始单位；仅在实际同运行可得时进入完整设计 | A 配方固定模型规模线索，B1 轨迹另源 | 不能跨源拼造同运行 N,D,Q,p；分源审计 |
| source_nature | REAL_DIRECT / SEMI_SYNTHETIC / INTERPOLATED / ESTIMATED / MIXED | 数据说明及文件谱系 | 无性质标签则 HOLD_PROVENANCE |
| score_provenance | Q 的指标、权重、训练数据、是否用 L 监督、是否 cross-fit | Q1 预处理版本 | 不可证明未泄漏则 HOLD_SCORE_PROVENANCE |
| group_id | 独立模型族/运行/配方批次，用于留组与重抽样 | 原始元数据 | 无法确认独立单元则不报精确标准误 |

## Required transformations

1. 先冻结文件角色、原始哈希、配对键和 Q1 评分版本；指标方向、列表压缩、标定尺度仅由允许的训练/校准数据确定。若 Q 直接用同一目标 L 的全量标签训练后又在这些行上声称“Q 独立预测 L”，标记 LEAKED_SCORE。交叉拟合可消除部分预测泄漏，但仍不自动给因果含义。
2. 对 A4 的 17 域比例先核非负、行和与缺失。审计秩时使用一个固定的 16 维满秩 simplex 对比基 C（C 的列和为零）得到 P_c=P C，另加截距；等价的 drop-one 可作为复核。不能直接把截距和 17 个原始比例放在一起再把必然秩亏判成额外数据问题。对数比/ILR 只在零值处理、参考和逆变换合同明确后作替代诊断，不能用零替换本身制造独立 Q 变异。
3. 在 A 配方与 Loss 真正配对的行上定义 X₀=[1,P_c,经审计可同运行观测的规模/源别控制] 和 X_q。若规模/源别列在这些行并不存在，X₀ 先仅含合法 p 基和截距；B1/B6–B8 分别建其本源设计，不能堆成一张填充后的“全变量”矩阵。X_full=[X₀,X_q] 的每一列必须写来源和样本粒度。
4. 对非截距列做中心化和可逆尺度标准化后报告数值条件诊断；保留原始单位设计用于解释。任何训练集决定的尺度参数在验证集冻结。Q_eff=pᵀq_fixed 或 p⊙q_fixed 的生成关系应直接登记为 deterministic_from_p，不能靠 z 标准化、正则化、PCA 或换坐标称为新独立实验。

## Variation test — STEP A/B

- **A0 provenance/leakage**：Q 是否由本次要解释的 L 监督得到？是否有严格独立训练、交叉拟合和对应的留组验证？若未避免信息泄漏，先输出 LEAKED_SCORE/HOLD，不进入独立贡献判断；这属于构造/验证问题，不必然是设计矩阵秩亏。
- **A1 matched variation**：能否对同一运行得到 p_r、Q_r、L_r,m？在相同/近似 p 与规模/源别条件下是否存在 Q 变化；反向在相近 Q 条件下 p 是否变化？“近似”邻域的距离定义和支撑规模由审计预注册；它是直观支持诊断，最终代数条件由残差化设计决定。只有 A1–A3 样本内 Q 变化但无 A4/A5 配对时，输出 NO_MATCHED_Q，不能直接跑联合秩检验。
- **B deterministic construction**：若 Q_r=f(p_r,q_fixed)，且无独立域质量或运行批次变化，输出 STRUCTURAL_NON_IDENTIFIABILITY_OF_INDEPENDENT_Q。对于 Q_eff=pᵀq_fixed 且 X₀ 包含完整线性 p 对比，X_q 必在 col(X₀)。即使某非线性 f 让受限线性设计数值满秩，也只说明在该函数形状假设下的统计区分；固定 p 改变 q 的真实反事实未被 A 数据观测。

## Rank test — STEP C

对已配对的训练行分别检验 rank(X₀) 与 rank(X_full)。数值秩须说明 SVD 容差的机器精度、矩阵尺寸和最大奇异值依据，并用合理尺度扰动复核；不设任意固定“小于 10⁻⁸ 即失败”的科学阈值。若 X₀ 自身秩亏，先修 p 参数化、重复列或规模控制；若 X₀ 满秩而 rank(X_full)=rank(X₀)，质量列在既有解释空间中，输出 EXACT_ALIASING / MODEL_SPEC_NON_IDENTIFIABLE。对多列 X_q 逐列及整体检查新增秩，明确只有哪些质量方向可辨。

在单列线性加性规格 L=X₀β+γQ+ε 且 X₀ 满秩的有限样本中，γ 代数上唯一的必要且充分条件是 Q 不在 col(X₀) 中；这不是 γ 的因果识别充分条件。所有“∂L/∂Q”主张须同时标明候选函数、固定的 p/N/D、来源性质和可用支持域。

## Collinearity and stability diagnostics — STEP D

即使 X_full 满秩，也输出标准化设计的奇异值序列、条件数、Q 对 X₀ 残差化后的范数与占原 Q 变异的比例、参数相关矩阵；在线性模型可报告 VIF，但不能单凭 VIF 放行。以独立 run/模型族为重抽样单元，检查 γ 的符号、区间、可接受效应范围与 profile likelihood 或等价诊断在合理模型扰动下是否稳定。比较这些诊断相对于实际 Loss 噪声、Q 测量误差和预先声明的最小有意义效应，而非套固定 δ_weak=0.05、n_min=20 或通用条件数阈值。

审计先登记每个诊断的单位、尺度和可用独立簇，再在查看 A6–A11 等保留结果前冻结 precision_rule 与 support_rule。若无法校准精度或独立样本量，输出 PENDING_CALIBRATION，不得把满秩写成“已识别”。全秩但 Q 残差变异很小、γ 在重抽样/规格替代中失稳时标 WEAK_IDENTIFICATION；全秩且精度尚可、但 p/Q/N/D 的共同支持很窄或独立运行不足以覆盖将要报告的效果范围时标 INSUFFICIENT_SUPPORT。EMPIRICAL_COLLINEARITY 是诊断标志，不与结构性别名混写。

## Model comparisons and out-of-sample distinguishability — STEP E

在相同配对训练行、同一预注册主 Loss 响应与相同按 run/规模分组的保留切分上比较 Model P（X₀）、Model Q（仅可比较的 Q/规模基线）、Model P+Q（X_full），必要时再比 Model Joint（p 与 q 联合编码）。记录每个模型的训练/保留误差、残差模式、参数区间、留族行为、对 Q 测量和域映射替代的稳定性。若 Q 只在训练内改善或增益对划分/来源不稳，输出 NO_INCREMENTAL_PREDICTION；若稳定改善，最多输出 PREDICTIVE_Q_ASSOCIATION，仍须外生变化或更强设计才能写“提高质量导致 Loss 改善”。

若设计无法在同一真实配对单位上比较 P 与 P+Q，不能借 B6–B8 的良好拟合填补 A 的保留结果；可分别报告不同源内的检验并给联结假设。

## Semi-synthetic overlay — STEP F

只要用于 γ 或 Q 敏感性的独立 Q 变化主要来自 B6–B8，就额外标 SEMI_SYNTHETIC_IDENTIFICATION_SUPPORT，即使其设计满秩、内部留出良好也不升为真实训练运行的独立效应。B2 是半合成、B3 是插值、A13/A15/B10 是估算/外推，各自保持原标签。比较真实数据是否至少支持方向/有效域；不一致时同时报告，不平均成单一“证据强度”。

## Decision branches and Q2/Q3 actions

以下顺序是审计后分支器的确定性优先级。每步都有状态、允许措辞和 fallback；多种风险并存时保留全部 flags，主状态取先遇到的阻断分支。

| Branch | 触发条件 | 输出与 Q2_ACTION | 允许/禁止的主张 |
|---|---|---|---|
| 0 HOLD_PROVENANCE / LEAKED_SCORE | 来源/配对/Q 构造未知，或同一目标 Loss 未隔离监督构造 Q | 修复来源；改无监督测量或严格 nested cross-fit，重新冻结数据后从 Step A 重来 | 不报告独立质量作用；泄漏不等同秩亏 |
| 1 NO_MATCHED_Q | 真实运行只有 p 与 Loss，没有同粒度 Q_r | Path A 无法检验；Q2 用可检验配比响应，Q 独立项留 OPEN | 不把 A1 文本间 Q 变化称配方级质量实验 |
| 2 STRUCTURAL_ALIAS | Q=f(p,q_fixed)，且无独立 q 变化；在线性 Q_eff=pᵀq 情况 Q∈col(X₀) | Path A 失败；Q2 可用 Path B 联合响应或 Path D 情景，禁止真实独立 ∂L/∂Q | p⊙q 仅联合编码，不称识别修复 |
| 3 SPEC_RANK_DEFICIENT | 合法 p 参数化后 X₀ 或 X_full 仍秩亏 | 删除重复列、降低自由参数或改变可识别规格，重跑全树 | 不用正则化把不可识别系数包装成可解释参数 |
| 4 PENDING_CALIBRATION / WEAK_IDENTIFICATION | 满秩但精度/支持规则未冻结，或 γ/残差 Q 不稳定 | 先冻结比较规则；弱识别时改简单模型/区间，Q3 只做情景敏感性 | 不报单一质量弹性或确定性最优投入 |
| 5 INSUFFICIENT_SUPPORT | 满秩但真实独立运行/共同支持不足以覆盖声明域 | 限定可报告范围，保留宽区间或寻求额外真实证据 | 不从局部设计外推到高预算/新配比 |
| 6 NO_INCREMENTAL_PREDICTION | 同切分留组检验中 P+Q 未稳定优于 P，或误差改善不超过不确定性 | Q2 不保留单独 Q 预测项；Path B 联合效应或 Path D 情景 | 可报告相关/联合响应，不报独立实用贡献 |
| 7 PREDICTIVE_Q_ASSOCIATION | 实际真实配对数据满秩、精度和支持足够、Q 样本外稳定增益 | Q2 可把受限 Q 项列为待建模候选并给不确定区间；Q3 待 Gate 3 再消费 | 仅称样本外独立预测信息；因果质量效应仍需外生性 |
| overlay SEMI_SYNTHETIC_ONLY | 上述积极证据只来自 B6–B8 | γ/方向只作半合成校准情景，Q3 质量投入输出条件区间 | 禁止“真实训练实验证实质量弹性” |

**Fallback 1 — 联合质量/配比表示**：若 Path A 失败，可报告 q 的测量、p 的真实响应及 p⊙q 等联合特征；不得单列真实 γ。**Fallback 2 — 条件情景**：固定 p 改变 Q 或固定 Q 假设考察 p，只在明确外部/半合成假设下计算。**Fallback 3 — 半合成补充**：B6–B8 给参数范围和敏感性，单独标来源。**Fallback 4 — 放弃独立质量弹性**：真实数据若不支持，就从正式经验估计中删去该系数；仍须按题面讨论其条件性数学关系与可识别边界。Fallback 顺序不是必须逐级采用的最终模型选择。

## Output fields

每次审计产生一个结构化记录，最少字段：audit_id、run_utc、input_paths_and_sha256、dataset_version、score_version、source_nature、pairing_key、matched_run_count、independent_group_count、response_definition、p_basis_and_zero_policy、q_construction、score_uses_target_loss、crossfit_evidence、has_paired_real_Q、deterministic_from_p_fixed_q、X0_columns、Xq_columns、n_rows、rank_X0、rank_Xfull、svd_tolerance_method、singular_values、condition_number_scaled、residualized_Q_norm_and_ratio、variation_summary、precision_rule_id、precision_state、support_rule_id、support_state、oos_split_id、oos_model_metrics、oos_gain_state、semi_synthetic_overlay、primary_branch、risk_flags、allowed_claim、forbidden_claim、Q2_ACTION、Q3_ACTION、fallback_branch、remaining_open_items、reviewer_and_decision_id。

输出值不得用 null 冒充“已通过”；无法测量时填 NOT_TESTED 并写原因。每个输入和输出可追至哈希、预处理版本及留出切分。04_code/utils/identifiability_decision.py 只消费这些审计摘要并路由分支；它不读取原始 A/B/C，也不替代实际秩/SVD/留出计算。

**分支器最小 JSON 输入字段**：audit_id（非空字符串）；score_provenance_valid、score_uses_target_loss、nested_crossfit_valid、paired_quality_available、deterministic_from_p_fixed_q（布尔）；rank_state∈{NOT_TESTED,X0_DEFICIENT,FULL_DEFICIENT,FULL_RANK}；precision_state∈{NOT_CALIBRATED,WEAK,STABLE}；support_state∈{NOT_CALIBRATED,INSUFFICIENT,ADEQUATE}；oos_gain_state∈{NOT_TESTED,NO_STABLE_GAIN,STABLE_GAIN}；quality_evidence_source∈{REAL_DIRECT,SEMI_SYNTHETIC,MIXED}。当相应阶段宣称已有证据时，还必须提供非空 score_provenance_id、pairing_evidence_id、rank_evidence_id、precision_rule_id、support_rule_id、oos_split_id 和 oos_metrics_id；分支器拒绝没有这些引用的“通过”。实际审计摘要仍须附上上段的数值诊断与来源，分类标签不能替代证据。MIXED 必须先分源重跑，不允许池化后直接放行。运行方式：python 04_code/utils/identifiability_decision.py --input <审计摘要.json> --output <分支决定.json>；输出含输入摘要 SHA256、证据 ID、允许/禁止措辞和 Q2/Q3 行动。

## Design-level dry-run coverage

本表是逻辑样例，不是本赛题数据结果：同一目标监督造 Q → Branch 0；无配方级 Q 键 → Branch 1；固定 q 的 Q_eff=pᵀq → Branch 2；另有重复列致秩亏 → Branch 3；满秩但未冻结精度规则 → Branch 4 PENDING；精度弱 → Branch 4 WEAK；共同支持不足 → Branch 5；同切分无增益 → Branch 6；真实配对且稳定增益 → Branch 7；只在 B6–B8 中满足 → SEMI_SYNTHETIC_ONLY overlay。每种分支都必须写 Q2_ACTION、Q3_ACTION、允许/禁止措辞和下一证据。

**P0 关闭条件**：本规范、可执行分支器、fallback 与输出字段齐备并用上述非真实样例覆盖全部分支时，可标 CLOSED — DESIGN LEVEL / AWAITING EMPIRICAL AUDIT；这不表示已在真实数据中通过可识别性检验，也不授权直接采用独立质量模型。
