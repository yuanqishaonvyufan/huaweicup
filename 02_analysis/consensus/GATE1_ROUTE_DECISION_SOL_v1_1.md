# Gate 1 Route Decision — Sol convergence v1.1

状态：**SOL REVISED POSITION / AWAITING OPUS FINAL CONFIRMATION**。本文件承接[Sol v1](GATE1_ROUTE_DECISION_SOL_v1.md)、[Opus Round B Review](../opus/GATE1_OPUS_EVIDENCE_REVIEW_v1.md)、[Opus→Sol handoff](../../09_handoff/OPUS_GATE1_TO_SOL_v1.md)与[Phase 1 v2](../../01_data/audits/phase1/ROUTE_DECISION_AUDIT_PHASE1.md)。只收敛 Gate 1 允许的建模路线；不重做 Discovery、不设置 ACTIVE FINAL MODEL、也不把本稿当 ACTIVE Gate 1 共识。

## CHANGELOG FROM v1

| 来源 | 吸收/修订 | 证据边界 |
|---|---|---|
| MODIFY-1 Bridge | 当前候选状态改为 **WEAK BRIDGE — PYTHIA-CONFINED, PENDING VALIDATION**；Strong 不放行，`NO RELIABLE BRIDGE` 留作验证失败 fallback | [7 点定向核查](../../01_data/audits/phase1/bridge_pythia_focus_check.json)确认 C6 High 与 B1 末检查点 Loss 7/7 一致，但 D 固定、综合得分关联不稳、逐任务方向混合；当前不允许数值能力预测 |
| MODIFY-2 B6/B7 | E3 半合成之外，明确**生成/校准机制不透明，可能预置 Q–Loss 关联**；质量参数仅为给定生成机制的条件关联 | B6 360 全嵌 B7 450，B7 生成器未见；B6 来源说明不足以验证生成函数 |
| DEFER-1 p 域 | 撤回“有限观测配比已是 Q3 最终 baseline 可行域”的预定；五类可行域均保留 CANDIDATE，最终选择待 Q1 配比模型 + A6–A11 检验和供给证据 | 当前只确认完整 simplex 解不能自动称现实可实施 |
| Opus 六问 | Review §20 的 Q1–Q6 逐题回应如下；handoff §5 的七个 Sol 旧问答已逐项核对，其中第七项 Gate 状态见后文 | 不把 Opus 回答当新的实测数据 |
| 四条补充建议 | 分别 `ADOPT WITH MODIFICATION`、`ADOPT WITH MODIFICATION`、`DEFER`、`ADOPT`，见后文 | 只改路线/次序，不添加最终模型 |
| 证据引用更正 | 更正 Opus 文稿中 B1 154,000→1,176、B7 1,620→450、AUDIT-08/09 等不存在编号及 `NO_MATCHED_Q` 的代数措辞 | [更正记录](../../10_review/GATE1_ROUND_B_EVIDENCE_ERRATA.md)；未重跑完整 Phase 1，路线方向不因这些引用错误自动反转 |

## 1 当前证据与收敛原则

ACTIVE Discovery 共识 C01–C22 不变。Phase 1 v2 的 `NO_MATCHED_Q`、A/B 无共同标尺、13 域异质、B8 反向、C7 架构/训练长度区别和 p 支持缺口仍是主边界。Opus 的 16 KEEP、2 MODIFY、1 DEFER 按内容映射为[19 条 v1.1 矩阵](ROUTE_DECISION_MATRIX_v1_1.md)；其中真正的行级状态变化是 RD-15 改 DEFER，RD-11 与 RD-17/18 主要收紧证据和桥接措辞。KEEP 的路线未重新打开，除了发现 Opus 引用数字与原表冲突所需的局部更正。

## 2 Opus 六个反向问题逐题回应

以下 Q1–Q6 来自 Opus Review §20；handoff §5 另列七个对 Sol 旧问题的答复，Q7 的 Gate 条件已纳入 §12。每问均按用户要求记录七项字段。

### Q1 Bridge 状态

**QUESTION**：是否同意从 `No Reliable Bridge yet` 改为限 Pythia Weak？  
**OPUS CONCERN**：七个同族、高可比且有规模梯度的点不是零证据。  
**SOL RESPONSE**：同意把**路线候选状态**定为 `WEAK BRIDGE — PYTHIA-CONFINED, PENDING VALIDATION`。7/7 Loss 与 B1 末点完全相同，提供可追溯锚；但七点 D 固定为 299.893B、综合分与 Loss Pearson 约 −0.397，各任务方向混合，尚不能称稳定预测映射。  
**EVIDENCE**：[定向 JSON](../../01_data/audits/phase1/bridge_pythia_focus_check.json)及 C6/B1 原始 SHA-256；无留出/残差/区间校准。  
**DECISION**：吸收 MODIFY-1；Strong 禁止、跨族禁止，No Reliable Bridge 保留为 Gate 4 检验失败 fallback。  
**STATUS**：CONDITIONAL / DATA_REQUIRED for predictive use。  
**NEXT ACTION**：P1-2 预注册高可比子群、分任务映射、整族/时间留出、残差和区间；先限 Pythia 探索，不向 Q3 全域运输。

### Q2 M0–M3 标签

**QUESTION**：正式换 M1/M2 标签，还是保持原标签并灵活排序？  
**OPUS CONCERN**：Round A 把 M1=p、M2=Q 与 ACTIVE 共识 C17 的候选名称不同。  
**SOL RESPONSE**：采纳保持 **C17 设计标签**：M0 N–D、M1 Q 候选、M2 p/领域候选、M3 少量交互；但实际**工作顺序**可先检验有 E1 配对的 p 分源关系，再进入仅 E3 支持的 Q 情景。M1 目前不是已估独立 Q 项；M2 也不意味着能无锚地数值叠加到 B1。  
**EVIDENCE**：`NO_MATCHED_Q`；A4/A5 有 p/Loss，B1 有 N/D/Loss，B6/B7 仅 E3。  
**DECISION**：保留原标签、调整证据执行顺序，不更改 ACTIVE C17。  
**STATUS**：RESOLVED AT ROUTE LEVEL。  
**NEXT ACTION**：正式模型规格时分开列数据来源、共享参数假设和同口径留出，不能把标签当已嵌套拟合模型。

### Q3 B8 的未来角色

**QUESTION**：若 B8 是反向情景，是否保留 stress test？  
**OPUS CONCERN**：方向反转不自动等于文件错误，不能简单删掉。  
**SOL RESPONSE**：保留 future stress test / alternative regime **候选**，不现时使用。先依[DA-01 调查计划](../../10_review/B8_CONFLICT_INVESTIGATION_PLAN.md)分 `calibrated` 984 与 `extrapolated` 720 核生成器、Q/Loss 定义和共同网格。  
**EVIDENCE**：B8 150 个固定 N,D 组均与 B6/B7 方向相反，224 共同点存在尺度冲突；生成机制未明。  
**DECISION**：当前 QUARANTINE 不变；解释充分后可单列反向情景。  
**STATUS**：DEFER / DATA_REQUIRED。  
**NEXT ACTION**：追溯生成器与版本，不能把 B8 合估或作 B7 的独立验证。

### Q4 安全跨源利用

**QUESTION**：是否增加 A 的领域结构指导 B 参数化？  
**OPUS CONCERN**：完全分源可能浪费可迁移的结构信息。  
**SOL RESPONSE**：允许 A 的域簇/冲突作为**待检的参数化假设**，不能运输 p 系数、弹性数值或未经 B 内验证的符号约束。B1 本身无可变 p，故“指导 B 的 p 项”不能在 B1 上直接检验。相对变化/normalized effect 仅是可比性探针；two-stage、calibration、hierarchical 均待锚/运输证据。  
**EVIDENCE**：AUDIT-02 的源别语料/tokenizer 缺口与 A/B 不同观测粒度。  
**DECISION**：ADOPT WITH MODIFICATION。  
**STATUS**：CONDITIONAL。  
**NEXT ACTION**：先定结构假设和可拒绝的验证设计，再找共同锚；无锚保持 SOURCE-SEPARATED FIRST。

### Q5 p 可行域时机

**QUESTION**：是否同意待 Q1 配比拟合后再选择最终域？  
**OPUS CONCERN**：凸包内外误差未知，过早指定有限集/局部扩展会锁死 Q3。  
**SOL RESPONSE**：同意。有限集合、观测凸包、局部外扩、经验边界、低维流形均为候选，不指定扩展百分比或最终域。唯一当前硬边界是完整 simplex 最优不自动等于现实可实施。  
**EVIDENCE**：A6/A8 同 p；舍入包络下 1M 仅 21/256、1B 41/64 在 A4 凸包内或精度邻域，真实供给未知。  
**DECISION**：吸收 DEFER-1，RD-15→DEFER。  
**STATUS**：DEFER / DATA_REQUIRED。  
**NEXT ACTION**：Gate 2 报凸包内外与边界误差，再审供给/许可证、优化稳定性。

### Q6 Gate 1 之后优先级

**QUESTION**：是否把 P1-1 与 A1–A3 九维审计排在 B8 调查前？  
**OPUS CONCERN**：P1-1 和质量原始数据直接阻塞 Q1；B8 不阻塞 E1 主线。  
**SOL RESPONSE**：同意：① [P1-1 v1.1](../../01_data/audits/phase1/P1_1_13_DOMAIN_RESPONSE_PREREG_v1_1.md) 比较规则冻结并等待模型比较；② A1–A3 全量九维审计；③ B8 机制调查可并行；④ A/B 锚、C 实体、p 供给与实训长度。  
**EVIDENCE**：Q1 必用 A1–A3、P1-1 使用前门槛；B8 仅 E3 且已隔离。  
**DECISION**：ADOPT 调整后优先级。  
**STATUS**：RESOLVED AT ROUTE LEVEL。  
**NEXT ACTION**：Opus 最终短审后按此顺序启动受限 Q1/Q2 工作，不做本轮正式估计。

## 3 四条非强制建议逐项处理

| Opus 建议 | 处理 | 理由及落点 |
|---|---|---|
| 1. A 领域结构安全用于 B 参数化 | **ADOPT WITH MODIFICATION** | 只作可拒绝的结构/分组假设，不运输数值/符号；B1 无 p 变异，需未来 B 证据。写入[接口](Q1_TO_Q2_INTERFACE_v1.md)与来源分层路线。 |
| 2. 保留 C17 M1/M2 标签、允许证据顺序灵活 | **ADOPT WITH MODIFICATION** | 标签不动，执行顺序先 p 来源内证据再 Q E3 情景；不把 M1 当已识别 γ。 |
| 3. B8 若为反向情景保留 stress test | **DEFER** | 调查机制前任何使用均可能混淆 Q/Loss 定义；计划中保存此出口。 |
| 4. P1-1→A1–A3 审计→B8 并行→其余 | **ADOPT** | 优先处理真正阻塞 Q1 的输入和使用前规则。 |

## 4 Q1、Q1→Q2 与 Q2 当前允许路线

Q1 冻结的是两轨**研究结构**：Track A 使用 A1/A2/A3 全量质量信号做方向、缺失、列表压缩、冗余、冲突和描述评分，处理 A1/扩展样本重叠；Track B 在 A4/A5 同 `index` 的 p/13 Loss 上用合法 simplex 对比研究配比响应，并在 A6–A11 留出检验。描述性 Q 不自动成为可独立识别的 Q_r。Q1 向 Q2 当前准许传的对象、证据等级与禁止主张见 [Q1_TO_Q2_INTERFACE_v1](Q1_TO_Q2_INTERFACE_v1.md)；它不强迫单一 Q 标量。

Q2 第一阶段是 **B1 SOURCE-INTERNAL N–D SCALING LAW BASELINE CANDIDATE**，非最终 Scaling Law。针对 Opus 的错误计数已查：B1 是 8 个 N 水平×147 检查点=1,176 行，N=0.070542–11.965825B、D=0.134–299.893B，`val_loss` 2.0933–4.7388；简约 `[1,log N,log D]` 设计秩 3、全表 logN/logD 相关近零，但每条轨迹相关，精度/泛化尚未证明。正式拟合前核验证语料、单位、轨迹/模型族簇、非线性与整轨迹留出；B2 或 B3、B4/B5 按题面分级检验。A 的 p 响应与 B 的 N/D 基线先分源，质量只能以有来源的 conditional scenario、B6/B7 E3 支持或未来同运行可识别证据进入；不得把未识别 γ_Q 写成主模型固定参数。

## 5 A/B、B6–B8、13 域及 Context Length

**A/B SOURCE-SEPARATED FIRST**：当前禁止绝对 Loss 直接池化。相对效应和 normalized effect 可作来源内探针，标准化不产生共同标尺；two-stage、calibration、hierarchical 需额外共同比较目标/锚、运输和留出证据后开启。

**B6/B7**：同一 E3 半合成网格，B6 360 全嵌 B7 450，不双计。source_manifest 只概述 B6 的 Pythia+RegMix 校准，生成函数与 B7 扩展机制未完整可核，观察到的 Q–Loss 关系可能由生成规则预置。任何 γ_Q 只能称“在给定半合成生成机制下的条件关联”；未来敏感性至少按生成假设、校准参数、样本组成检查稳定性。**B8**：QUARANTINED — GENERATION MECHANISM UNDER REVIEW；不估主参数，`calibrated`/`extrapolated` 分层追查，解释后才考虑 alternative regime/stress test。

**P1-1**：[v1.1 预注册](../../01_data/audits/phase1/P1_1_13_DOMAIN_RESPONSE_PREREG_v1_1.md)沿用 R0–R3：R0 是透明主响应 baseline 候选，R1 标准化敏感性，R2 PCA 低维候选，R3 强制 13 域异质性。冻结比较规则和“综合+逐域”双层结构，不宣称 R0 已是最终赢家；A6–A11 不用于事后选权。

**L_ctx**：题面外生敏感性变量。η=2×10⁻⁴ 的 30k 条件阈值仅为 architecture-support reference；C7 12/45 架构上限达阈值，实训长度未知，不能叫已验证结构转移点。

## 6 Bridge 与 p 可行域

桥接当前路线状态为 **WEAK BRIDGE — PYTHIA-CONFINED, PENDING VALIDATION**，这里的 Weak 是**限族待验证候选**，不是已经通过预测误差审查的数值映射。C6 七个 High 与 B1 末点 Loss 完全对齐，但都在同一 Pythia 族、同一 D，综合 Benchmark 相关较弱且任务方向混合；不用于全模型能力预测、Q3 全决策域运输或 Strong 声明。Gate 4 前须按高可比层预注册 held-out、残差、区间、时间和跨族覆盖；失败则启用 `NO RELIABLE BRIDGE` fallback，Q4 独立分析能力并披露映射失败。

p 的最终可行域 **DEFERRED UNTIL Q1 MIXTURE MODEL + A6–A11 VALIDATION**。观测凸包、局部外扩、单域经验界、低维流形、有限候选集仍为 CANDIDATE；不指定任意外扩百分比或现实供给数。当前可确认：完整 simplex 最优不能自动解释为现实可实施配置。最终须分报理论、数据支持和可实施域，并通过 P1-3 供给/许可审计。

## 7 19 条路线与 Gate 1 状态

[ROUTE_DECISION_MATRIX v1.1](ROUTE_DECISION_MATRIX_v1_1.md)保留 RD-01–RD-19，逐行给 Sol v1、Opus、收敛决定、证据、理由和下一 Gate。建议 **GATE 1 = CONDITIONAL PASS（路线层级）**：七项审计足以允许受约束 Q1/Q2 工作；完整九维审计、processed 冻结和后续 Gate 仍未完成。此建议写入[Gate 1 Consensus Draft](GATE1_CONSENSUS_DRAFT_v1.md)，**不是 ACTIVE**，须 Opus 最终短审。没有新增重大模型路线/假设，也没有改原始真实证据；本轮只吸收 MODIFY-1/2、DEFER-1、答复意见并纠正 Opus 引用，所以建议 `OPUS FINAL CONFIRMATION`，不重做全套 Evidence Review。

**ALLOWED TO MODEL NOW（经最终短审后）**：Q1 质量结构/冲突、A4/A5 p 与 13 域响应的受限 baseline 和预注册比较、B1 来源内 N–D baseline 候选、B8 机制调查与必要九维审计。**NOT ALLOWED YET**：真实独立 Q 弹性、A/B 绝对 Loss 池化、B8 主参数、Strong/跨族桥接、完整 simplex 可实施最优或最终 p 域、正式 Q3 优化、Q4 强定量桥接预测、ACTIVE FINAL Q1/Q2/Q3/Q4 模型与正式论文结果。
