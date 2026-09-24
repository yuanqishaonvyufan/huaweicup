# Gate 1 route consensus v1

**STATUS: ACTIVE. GATE: GATE 1 — CONDITIONAL PASS (ROUTE LEVEL).**  
**PROMOTED FROM:** [GATE1_CONSENSUS_DRAFT_v1.md](GATE1_CONSENSUS_DRAFT_v1.md)  
**PROMOTION BASIS:** [GATE1_OPUS_FINAL_CONFIRMATION_v1.md](../opus/GATE1_OPUS_FINAL_CONFIRMATION_v1.md) — A. PASS  
**PROMOTION DATE:** 2026-09-23（Asia/Shanghai）。本文件冻结“哪些路线准许进入下一阶段”，不确认最终 Q1 评分、Scaling Law、Q3 优化器、Q4 分解/预测、任何系数或论文结果。[DISCOVERY-CONSENSUS-v1](CONSENSUS_F_PROBLEM_ANALYSIS_v1.md) 仍为 ACTIVE 研究设计共识；本文件为 ACTIVE Gate 1 路线共识。来源为 [Phase 1 v2](../../01_data/audits/phase1/ROUTE_DECISION_AUDIT_PHASE1.md)、[Sol v1.1](GATE1_ROUTE_DECISION_SOL_v1_1.md)和 [Opus Round B](../opus/GATE1_OPUS_EVIDENCE_REVIEW_v1.md)；Opus 引用中的计数/编号更正见[记录](../../10_review/GATE1_ROUND_B_EVIDENCE_ERRATA.md)。

## 1 Gate-1 Status

**CONDITIONAL PASS — ACTIVE ROUTE LEVEL ONLY。**已能安全选择 Q1/Q2 的受限基线路线，完整九维 Data Audit、processed 输入与 Gate 2–4 未完成。项目尚不能把 Gate 1 写为无条件 PASS；本路线状态已由 Opus Final Confirmation 短审放行。

## 2 Evidence Base

原始附件只读，2,012 文件 SHA-256 清单可查；Phase 1 v2 指标和 `NO_MATCHED_Q` 分支为 CHECKED AUDIT RESULT，不是最终模型实验。Round C 只因 Opus 文稿与原表冲突，对 B1 与 C6 High 七点作[小范围来源核查](../../01_data/audits/phase1/bridge_pythia_focus_check.json)，未重跑完整 Phase 1 或拟合桥接。

## 3 Confirmed Audit Findings

- A1/A2/A3 为 51,230/17,523/203,752 条必用质量信号；A18 是可选 RegMix 原文，旧 v1 误映射已标 SUPERSEDED。A4/A5 512 条按 index 有 p/Loss、无同运行 Q；分支 `NO_MATCHED_Q`，不扩大为“全题永远无质量效应”。
- A5 13 域相关弱且异质，逐域分析不能被一个综合 Loss 取代。A4 配比有大量零值与训练/检验支持差异；现实供给未核。
- A/B 缺绝对 Loss 共同标尺。B1 为 8 个 Pythia 模型规模各 147 检查点，共 1,176 行；B6 360 全嵌 B7 450，B8 1,704 行质量方向冲突。B6–B8 均非真实质量干预。
- C7 有 12/45 个**架构上限**达到 30k token，实际训练长度未知。C6 High 仅 7 个同族 Pythia，Loss 与 B1 末检查点吻合，但 D 固定、Benchmark 方向异质，未做留出/区间校准。

## 4 Q1 Route

准许 **Track A QUALITY DESCRIPTION**：A1–A3 全量指标结构、方向/列表压缩、冗余、冲突、描述性评分与抽样/扩展重叠处理；准许 **Track B MIXTURE/DOMAIN RESPONSE**：A4/A5 合法 simplex 表示、p→13 域 Loss 候选和 A6–A11 预留检验。`Q_descriptive` 不自动等于 Q2 所需同运行 `Q_identified`；没有真实配对时不能拟独立 γ_Q。最终评分算法与 p 函数仍 OPEN。

## 5 Q1→Q2 Interface

[Q1_TO_Q2_INTERFACE_v1](Q1_TO_Q2_INTERFACE_v1.md)冻结质量描述、领域结构与 A16 映射等级、p 响应及其支持/误差、条件质量情景、证据等级和识别分支；不强迫单一 Q 标量。Gate 2 未验证前，向 Q2 只传规格与范围，不传“已验证真实质量系数”。

## 6 Q2 Route

第一候选是 **B1 SOURCE-INTERNAL N–D BASELINE**，不是最终 Scaling Law。保留 ACTIVE C17 的 M0–M3 候选标签及逐级证据原则，实际先检验有 E1 配对的 p 分源响应，再处理仅 E3 支持的 Q 条件情景；M1 不等于已识别独立 Q 项。正式估计须先核 B1 轨迹独立簇、N/D 覆盖、Loss 定义、相对精度、整轨迹留出、B2/B3 与 B4/B5 的分级验证。

## 7 A/B Strategy

**SOURCE-SEPARATED FIRST**。A 主要提供领域/配比与 13 域 Loss，B1 提供来源内 N–D；禁止直接池化绝对 Loss。来源内 relative/normalized effect 可作探针；two-stage、calibration bridge、hierarchical model 要等共同目标/锚、运输与独立留出证据。A 的域结构可供 B 未来参数化假设，数值系数和未经 B 验证的符号不得运输。

## 8 B6/B7/B8 Evidence Rules

B6/B7 是同一 **SEMI-SYNTHETIC SUPPORT**，生成/校准机制尚不透明且可能预置 Q–Loss 关系；任何质量敏感性只解释为给定半合成规则下的条件关联。未来至少按生成假设、校准参数、样本组成做敏感性。B8 为 **QUARANTINED — GENERATION MECHANISM UNDER REVIEW**，不进入主参数；`calibrated` 与 `extrapolated` 分层调查后才考虑 alternative regime/stress test。

## 9 13-Domain Response Preregistration

[P1-1 v1.1](../../01_data/audits/phase1/P1_1_13_DOMAIN_RESPONSE_PREREG_v1_1.md)状态为 **PREREGISTERED — AWAITING MODEL COMPARISON**。沿用 R0 原始等权透明 baseline、R1 训练标准化敏感性、R2 PCA 低维候选、R3 强制逐域异质性。冻结的是比较规则和“主响应候选 + DOMAIN HETEROGENEITY ANALYSIS”双层结构，**没有冻结最终赢家**；A6–A11 不得事后选权。

## 10 Context-Length Status

`L_ctx` 是 **EXOGENOUS SENSITIVITY VARIABLE**。题面 η=2×10⁻⁴ 产生约 30k 的代理成本临界值，仅作 C7 架构支持参照，不等于已观测训练长度或 Q3 已验证的结构转移阈值。

## 11 Bridge Status

当前候选状态：**WEAK BRIDGE — PYTHIA-CONFINED, PENDING VALIDATION**。范围限 7 个 High Pythia 点，不向全模型族、Q/p 变化或全 Q3 预测域运输，也不作全模型能力点预测；宽不确定性和逐任务差异必须显式。Strong **NOT ALLOWED**；跨族映射 **NOT ESTABLISHED**。Gate 4 留出、残差、时间/族覆盖与区间校准失败时，`NO RELIABLE BRIDGE` 为合法 fallback，Q4 独立分析能力并披露映射限制。

## 12 p Feasible-Region Status

最终形式 **DEFERRED UNTIL Q1 MIXTURE MODEL + A6–A11 VALIDATION**。观测凸包、局部扩展、单域经验界、低维流形、有限候选集均为 CANDIDATE；不预定扩展百分比、最终优化域或现实供给界。当前只确认完整 simplex 解不能自动解释为可实施最优。

## 13 Route Decision Matrix

[ROUTE_DECISION_MATRIX_v1_1.md](ROUTE_DECISION_MATRIX_v1_1.md)保存 RD-01–RD-19 的 Sol v1、Opus、Gate 1 已确认路线状态和下一 Gate；仅 RD-15 的路线状态由 KEEP AS BASELINE 改为 DEFER，RD-11 与 RD-17/18 吸收证据/桥接措辞。矩阵不确认任何模型参数。

## 14 Allowed to Model Now

Opus 最终短审确认后，准许继续：Q1 全量质量结构/冲突与必要九维审计；Q1 A4/A5 p 与 13 域响应基线及冻结规则下的候选比较；B1 来源内 N–D baseline 候选与整轨迹验证计划；B8 机制调查；A/B 锚、C 实体、C7 长度等针对性审计。受限代码/估计可在对应预处理合同与规格确认后进行，结果不因 Gate 1 条件通过自动升为 VALIDATED。

## 15 Not Allowed Yet

不得拟真实独立 Q 弹性、直接合并 A/B 绝对 Loss、用 B8 估主参数、把 E3 γ 写为真实实验、宣布 Strong 或通用跨族桥接、定最终 p 可行域、做 full-simplex 可实施优化、正式 Q3 资源最优、Q4 强定量桥接预测、确定任何 ACTIVE FINAL MODEL 或写正式论文结果。

## 16 Active Fallbacks

继续遵守 ACTIVE 共识 F01–F05：无 matched Q 时联合/条件情景并放弃独立经验 γ；半合成只给条件敏感性；若桥接验证失败则 `NO RELIABLE BRIDGE`，Q3 报 Loss/成本、Q4 独立报能力并尝试/披露映射误差。Fallback 不免除题面必用数据与验证。

## 17 Open Issues

P1-1 只完成响应比较预注册、未完成模型比较；P1-2 Strong 判据与桥接验证未过；P1-3 p 现实供给未核；P1-4/Q4 规模变量、P1-5 转移判据仍待后阶段。DA-01 B8、DA-02 matched Q 缺口、DA-03 C4/C1 实体、DA-04 C8 四坏文件、DA-05 A/B 可比性、DA-06 来源映射修复继续按 Issue Tracker 管理。无新增重大数学分歧需要重开全部 Gate 1；Opus 文稿的事实引文错误见更正记录，最终短审已确认未污染结论。

## 18 Next Stage

Opus 已通过 [Final Confirmation](../opus/GATE1_OPUS_FINAL_CONFIRMATION_v1.md) 的五项短审。本轮进入受约束的 Q1/Q2 Modeling Phase 1 初始化，优先冻结 P1-1 并执行 A1–A3 九维质量审计，同时准备 B1 eligibility，B8 机制调查并行；Q1–Q4 ACTIVE FINAL MODEL 仍 NONE。
