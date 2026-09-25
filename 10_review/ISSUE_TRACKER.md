# ISSUE_TRACKER

Round 4 Opus Verify 提出 1 个 P0、实际列明 6 个 P1、5 个 P2；报告若写“5 个 P1”属计数笔误。以下状态区分**设计修复**与**真实数据/模型检验**。

| Issue ID | Stage | Severity | Symptom | Evidence | Affected files | Repair class | Owner | Fix / Decision ID | Recheck | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| P0-1 | DISCOVERY | P0 | Q/p 秩诊断无结果→Q2 决策树 | JOINT_F_PROBLEM_REVIEW_v1 §2 | v1.1、IDENTIFIABILITY_AUDIT_SPEC、identifiability_decision.py | 数学合同/路由 | Sol + Opus Final Check | P0_CLOSURE_REPORT_v1；DISCOVERY-CONSENSUS-v1 | 14 非真实分支与 Opus Final Check PASS；真实 Q/p 仍待审计 | CLOSED — DESIGN LEVEL；AWAITING EMPIRICAL AUDIT |
| P1-1 | Q1 前 | P1 | 13 域 Loss 主响应比较规则 | Phase 1 AUDIT-04；Round 3 A5 训练比较；Round 4 A7 逐域留出检验 | P1_1_13_DOMAIN_RESPONSE_PREREG_FINAL_v1.md；Q1_RESPONSE_SELECTION_REPORT_v1.md | 使用前预注册、训练与留出复核 | Q1 建模者 | G1-PROMOTE-001 / MC-Q1-RSP-R3-20260924-v1 / VAL-Q1-PRESP-A6A11-R4-20260924-v2 | R0–R3 定义未改；R0 暂定主报告基线，R3 强制；A7/1M M1 13/13 域误差降低，1B 迁移失败 | GATE 2 ACCEPTED FOR Q1 PROVISIONAL CLOSURE；R0 + MANDATORY R3 |
| P1-2 | GATE 4 前 | P1 | Strong Bridge 判据不够可操作 | Verify §3 P1-2；7 点定向核查 | C5/C6 审计、bridge_pythia_focus_check.json | 使用前预注册 | Q4/桥接建模者 | ROUND5-P1-2；G1-RC-BRIDGE | Weak 仅限 Pythia 且待验证；Strong 需高可比留族/时间误差、残差/区间及运输域 | ROUTE CANDIDATE；GATE 4 VALIDATION REQUIRED |
| P1-3 | Q3 前 | P1 | p 经验支持和现实供给未区分 | Verify §3 P1-3；Opus DEFER-1 | A4/A6–A11、ROUTE_DECISION_MATRIX_v1_1.md | 现实可行域审计 | Q3 建模者 | ROUND5-P1-3；G1-RC-PDOMAIN | 理论/数据内/可实施解分报；Q1 拟合/留出已完成；最终域仍待现实供给和用途验证 | GATE 2 SUPPORT LOGIC ACCEPTED；FINAL Q3 REGION / SUPPLY DEFERRED |
| P1-4 | Q4 前 | P1 | N/D/C 规模变量高度共线 | Verify §3 P1-4 | v1.1 §15、C4 字段 | 变量选择预注册 | Q4 建模者 | ROUND5-P1-4 | 来源覆盖和设计秩后、能力拟合前定 | DESIGN DRAFTED；DATA_AUDIT_REQUIRED |
| P1-5 | Q3 前 | P1 | 结构转移“非平凡”与退化解未操作化 | Verify §3 P1-5 | v1.1 §15、Q3_VALIDATION_PLAN 待建 | 验证合同 | Q3 建模者 | ROUND5-P1-5 | 固定外生约束、扫预算及扰动 | DESIGN DRAFTED；待计算 |
| P1-6 | DISCOVERY | P1 | 保守主线最低完整性未定义 | Verify §3 P1-6 | v1.1 §15/§21；CONSENSUS §14 | 交付边界 | Sol/Opus | ROUND5-P1-6；DISCOVERY-CONSENSUS-v1 | Opus Final Check PASS，必用任务仍须实做 | CONFIRMED FALLBACK STORY — DESIGN LEVEL |
| P2-1 | 流程 | P2 | 原 Opus→Sol 交接缺失 | Verify §4 P2-1 | 回溯交接文件 | 可追溯性 | Codex | RETROSPECTIVE-v1 | 明确非原始产物 | RETROSPECTIVE CREATED |
| P2-2 | 表达 | P2 | 配比与配方偶有混用 | Verify §4 P2-2 | v1.1、NOTATION.md | 术语 | Codex | ROUND5-TERMS | 后续稿件核对 | DESIGN FIXED |
| P2-3 | 表达 | P2 | 缺集中符号表 | Verify §4 P2-3 | 03_models/shared/NOTATION.md | 符号 | Codex | ROUND5-NOTATION | 模型版本时扩充单位/范围 | INITIAL TABLE CREATED |
| P2-4 | 方法 | P2 | A16 inferred 固定百分比阈值无依据 | Verify §4 P2-4 | v1.1、数据审计合同 | 删除无依据阈值 | Sol | ROUND5-MAP | 审计报告实际覆盖与不确定性 | THRESHOLD REJECTED |
| P2-5 | Q4 | P2 | 多源日期与预测起点尚未核对 | Verify §4 P2-5 | v1.1 §15、C1–C4 审计 | 时间口径 | Q4 建模者 | ROUND5-TIME | 实际字段和数据截止后定 | DESIGN DRAFTED；DATA_AUDIT_REQUIRED |

检测 → 分类 → 整改 → 必要时重算 → 复检。核心模型、关键数据逻辑与结果修改仍须经双方确认。Round 4 已有正式 Q1 候选拟合与 A6–A11 留出验证，Gate 2 已按 G2-SINGLE-001 通过限定用途，但仍没有 ACTIVE FINAL MODEL 或 VALIDATED FINAL RESULT，故上述 P1/P2 不得写成“最终经验通过”。

## DATA AUDIT — PHASE 1 新发现（2026-09-23）

以下 DA 编号独立于上表 Round 4 的 P0/P1/P2 计数；证据见 `01_data/audits/phase1/ROUTE_DECISION_AUDIT_PHASE1.md`。

| ID | Severity | Evidence / symptom | Immediate route | Closure condition | Status |
|---|---|---|---|---|---|
| DA-01 | P1 | Round 1 的 B7/B8 共同 N–D 组方向冲突及 B8 0.5 边界仍无生成器证据；Round 4 未新增机制 | B8 QUARANTINED / SEARCH PAUSED；LIKELY SYNTHETIC RULE EFFECT 仅统计推断，不入主参数 | 真正需要 Q2 情景或取得生成器/校准规则后再开 | OPEN — GENERATOR UNKNOWN / SEARCH PAUSED |
| DA-02 | P1 | A4/A5 512 配方有 p/Loss；修订后 A1/A2/A3 三份质量信号仍均无同运行键，分支 `NO_MATCHED_Q` | 不拟真实独立 Q 弹性 | 找到可验证的同运行质量干预/键，或确认长期采用联合/条件接口 | OPEN — NO MATCHED Q |
| DA-06 | P1 | 初版 Phase 1 脚本误把可选 RegMix 原文 A18 当扩展质量信号，漏扫 A2/A3 | 保留 v1 为 SUPERSEDED；v2 流式补扫 A1/A2/A3；项目 data-audit Skill 已加入 OFFICIAL_MAPPING_FIRST | Gate 1 ACTIVE、A1_A3_OFFICIAL_MAPPING_v1.csv 已记录正确编号/路径/哈希；后续 Q1 保持全量使用并处理 ID 重叠 | CLOSED — MAPPING REPAIRED / GUARD ACTIVE |
| DA-03 | P1 | C4/C1 模型名精确交集 0；C2 仅 447 日期和 443 开放权重匹配 | 禁止按行合并 C4 规模和 C1 能力 | 冻结可核的实体/版本/日期对齐表及错配率 | OPEN — ENTITY MATCH |
| DA-04 | P2 | C8 的 1,958 个逐任务 JSON 中 4 个解析失败 | 原件保留，聚合时单列排除/修复状态 | 核源是否截断、必要时重新获取同版本，记录哈希与聚合影响 | OPEN — FOUR FILES |
| DA-05 | P1 | A/B Loss 缺共同验证语料/tokenizer 锚；C5/C6 High 仅单族 7 个 | A/B 分源；桥接仅作 Pythia-confined Weak 待验证候选，Strong 不放行 | 来源口径、共同锚、分任务/分族/时间留出和区间按 P1-2/P1-4 核验 | OPEN — COMPARABILITY / GATE 4 |
| DA-07 | CRITICAL for Q2 B1 external provenance | 147/154 检查点候选标签与内部 8×147 数值一致，但 `val_loss` 仍无行级 run/验证语料/tokenizer 锚；官方公开候选日志两处末值不同且未证同目标 | 外部 Alert v4 仍 `PARTIALLY RESOLVED`；Gate 2 G2-SINGLE-001 已允许附件内部 **B 级受限入口**；正式 N–D 拟合仍 0 | Round 5 已获受限入口，须先冻结合同并做轨迹分组/D 段检验；若得到原始来源再审外部资格 | OPEN EXTERNAL ALERT / RESTRICTED INTERNAL B ALLOWED FOR ROUND 5 |
| DA-08 | P1 for Q1 quality scoring | Round 4 22 项角色全覆盖、五核心域级分位与扩展对照，A1 原文 14 案例有代码/非英文反例；DQ0 编码敏感，语义冲突确认 0 | Q1 主表示为 Full-22 画像+五维分位向量，DQ0 仅描述摘要；`NO_MATCHED_Q`，TYPE E=0 | Gate 2 已接受描述性质量表示及面效度边界，不能用 Loss 反向赋权或估独立 Q | Q1 PROVISIONALLY CLOSED BY G2-SINGLE-001；DESCRIPTIVE LIMITS RETAINED |
| DA-09 | P1 source-integrity guard | 用户提示原始《数据说明》有 AI 扫描干扰；Round 2 在固定哈希 13 页 PDF 的第 2–13 页各检出 8 段 #fcfcfc、约 5pt 的页边额外文字，共 96 段，含无证据方法/数值指令 | `DOCUMENT_INTERFERENCE_AUDIT_v1.md` 按位置/颜色/字号隔离；官方编号仅取可见正文并与原件路径/哈希核对；未重开 Gate 1 | 当前 PDF 的异常层持续排除；若平台新版本或可见正文冲突则重新审核来源 | CLOSED FOR CURRENT PDF — INTERFERENCE EXCLUDED |
| DA-10 | P1 for Q1 scale transfer | 正式 M1 p→13 域模型在 A7/1M 留出改善全部域，A9/60M 仅中心化形状部分改善，A11/1B 中心化 R0 RMSE 比 M0 达 3.108 | M1 仅 1M 同尺度主预测候选；不得作为通用 1B p 效应或 Q3 全域目标；1B 失败进入论文限制 | 后续若需跨规模统一，另立规模机制和独立留出，不回填 A11 当前失败 | OPEN — 1B TRANSFER FAILED / Q1 SCOPE LIMITED |

## MODELING PHASE 1 ROUND 4 TAKEOVER QA（2026-09-24）

以下是本次接管新发现的**文件/门槛收口问题**，与上方历史设计问题和 DA 编号分开计数。新发现 P0=0、P1=1、P2=5；均已修复或由新版本取代。机器核查见 `MODELING_PHASE1_R4_QA_20260924.json`，正式裁决见同名 `.md`；不代表 Gate 2 已通过。

| ID | Severity | 接管时问题 | 整改 | 状态 |
|---|---|---|---|---|
| R4-QA-01 | P1 | 状态和 Gate 2 v1 均引用实际不存在的 Round 4 QA | 建立标准库只读 QA 脚本、机器 JSON 与 QA 报告；复核冻结/泄漏/逐行数值/图表/登记，最终 PASS | CLOSED — QA PASS |
| R4-QA-02 | P2 | Results Registry 未逐项登记 M1/M2 五折、M3 未触发和 M2 留出未获稳定收益 | 新增四项 CAND 结果 ID，保持 VALIDATED FINAL=0 | CLOSED |
| R4-QA-03 | P2 | Figure Registry 为空，四张已生成图仅有 manifest | 登记四图的来源 Run、CSV、脚本、文件、主张和限制；核原有 PDF/PNG 哈希 | CLOSED |
| R4-QA-04 | P2 | B1 活跃双层裁决末尾引用历史 Alert v3 | 改指权威 v4，同时明示 v3 继承链；旧 v1–v3 文件保留 | CLOSED |
| R4-QA-05 | P2 | Gate 2 v1 声称 QA 已完成而当时文件不存在；README、Modeling Phase 1 State、Stage Gates、Validation Report 仍留旧阶段描述 | 保留历史 v1，建立含真实 QA 的 Gate 2 v1.1；同步四份活跃总览文件 | CLOSED — v1 SUPERSEDED / ACTIVE STATUS SYNCHRONIZED |
| R4-QA-06 | P2 | B1 双层裁决的预冻结合同相对路径少一级目录，链接不可用 | 修正至 `../../../../03_models/...`，QA 本地链接检查通过 | CLOSED |

## GATE 2 SINGLE-PASS DECISION（2026-09-24）

[GATE2_CONSENSUS_v1](../02_analysis/consensus/GATE2_CONSENSUS_v1.md)，G2-SINGLE-001，ACTIVE，Verdict B。六项裁决 P0=0、技术阻断=0；两项 P2 文档修正已完成，不阻断 Round 5。历史 QA/DA 数量保持其原审查范围。

| ID | Severity | 问题 / 边界 | 修正 | 状态 |
|---|---|---|---|---|
| G2-DOC-01 | P2 | “holdout 未参与选模”过宽；原冻结合同明确 A7 用于候选比较与偏好判定 | Q1 验证/限制及共识统一为未用留出搜索结构、调参或回填；不宣称未使用最终测试或选择过程校正的区间 | CLOSED — DOCUMENT ONLY；NO RERUN |
| G2-DOC-02 | P2 | 活跃入口状态需从待审同步为已授权；B1 Alert v4 到 Q2 规格链接少一级目录 | 修正链接并同步共识、接口、B1、登记与交接状态；外部 Alert 仍未解除 | CLOSED — DOCUMENT ONLY |

DA-02/DA-05/DA-07 的识别或外部来源缺口、DA-10 规模转移失败和 Q3 实际供给限制继续携带；Gate 2 限定用途通过不把它们改写成已解决。

## Round5 current audit

新增P0=0。R5-INPUT-01：B9四个D=0已标无效且不插补（CLOSED）。R5-CODE-01/02：情景v1/v2序列化及空分组处理失败已修复，有效v3，旧运行隔离（CLOSED）。R5-VIS-01：图中文字缺字与外界刻度已修复（CLOSED）。DA-07外部来源仍OPEN，附件内部主拟合现为1且受限验证通过；DA-02 TYPE E=0、DA-05跨来源量尺、DA-10 1B失败不变。不得用窄bootstrap区间声称外部保证。Gate3待审。

## Round 5 takeover closeout — 2026-09-24

本次发现 P0=0、P1=1、P2=3；下列均 CLOSED，本次未解决项为 0。历史 DA-02/05/07/10、B8 与现实成本/供给边界未因此消失。

| ID | Severity | 问题 | 修正及状态 |
|---|---|---|---|
| R5-TAKE-01 | P1 | Git checkout 换行导致冻结代码/spec/Q1输入及四个含换行字段 CSV 的严格哈希不匹配 | 只接受精确命中既有 SHA 的字节恢复；逐路径 gitattributes 防止再变，原始附件不写；CLOSED — NO NUMERIC CHANGE |
| R5-TAKE-02 | P2 | 缺接管 A–Q 状态清单与显式合并图表/交付导航 | 新增 recovery check 与 delivery figure/table plan，引用已有等价报告；CLOSED |
| R5-TAKE-03 | P2 | Q2→Q3 尚未逐项给出 A–J 四类准入标签和成本缺口 | Markdown/JSON 同步准入规则，仍以 Gate3 批准为前提；CLOSED |
| R5-TAKE-04 | P2 | QA verdict 用语不在本次要求枚举内；需明确暂定关闭的候选范围 | 改为 PASS WITH DOCUMENT CORRECTIONS，补15项证据表、当前状态及交接；CLOSED |

已有 registry 顶部已经区分当前 Round5 与历史 Round4，接管未发现漏登数值/图形；本次仅附加完整性复核记录。

## Gate3 decision — 2026-09-24

G3-SINGLE-001 本次新发现 P0=0、P1=0、P2=0，阻断0。Gate3 Verdict A — PASS，Q2 PROVISIONALLY CLOSED。DA-02/05/07/10、B8 与实际成本/供给缺口继续保留；不是模型通过即已解决。历史 Round5 问题计数不混入本 Gate。


## Round6 CP3 numerical diagnostic

R6-NUM-01：17个对数质量成本初值停较差局部解；4次线搜索失败。已保存所有起点，通过预冻结嵌套搜索、加密网格和逐情景最佳成功对照消解；不声称全部初值一致，无新P0。该限制进入论文，不调改数学规格。


Round6 closeout：新增P0=0/P1=0/P2=3（R6-VIS-01，006图例遮线与ylabel越界已修；关闭）。R6-NUM-01为已解释的局部求解限制，非未解决P0。继承来源/质量/供应/1B风险不冒称关闭。Q3 PROVISIONALLY CLOSED，Gate4 READY，Q4 NOT STARTED。

R6-DOC-01（P2 CLOSED）：论文候选LaTeX写入转义异常被包QA拦截；仅修复生成脚本与派生文字，数值/冻结规格未变，初始失败QA保留，复检后上传。新缺陷总计P0=0/P1=0/P2=3，均已关闭。

R6-GIT-01（P2 CLOSED）：Round6目录属性会影响继承CP0的CRLF冻结哈希；增加两条精确eol=crlf覆盖并保留论文候选LF。科学内容/原始字节未改，Git模拟checkout哈希检查PASS。最终新缺陷P0=0/P1=0/P2=3，全部关闭。


## Gate4 decision — 2026-09-25

G4-SINGLE-001 新发现P0=0/P1=0/P2=0、阻断0。Gate4 Verdict A；Round6三项P2保持历史关闭。B1外部来源/真实质量/供给/1B等限制继续携带，不因Gate通过宣布解决。D语义与A–J为正常接口冻结，非新的模型错误。


## Round7 QA defects and retained limitations

New defects P0=0 / P1=0 / P2=3, all CLOSED after final QA:

| ID | Severity | Finding | Resolution |
|---|---|---|---|
| R7-PKG-01 | P2 | Optional markdown formatter unavailable, report literal syntax, and Q3 copy round-trip last-bit drift | Deterministic formatter/literal fix; Q3 copy preserves original decimal strings; fitted/forecast numbers unaffected |
| R7-DOC-01 | P2 | Seven raw6 name overlaps incorrectly described as insufficient without eligibility distinction | Seven name overlaps but two pass frozen triple-source scale criterion; no model/bridge verdict changed |
| R7-VIS-01 | P2 | Dense date ticks; absolute S/R bars risk interpretation as identified absolute contributions | Sparse dates and scenario increments from last frontier; visual review repeated |

Retained scientific scope limitations, NOT declared resolved: R7-LIM-01 missing same-stage D prevents full N–D/non-scale and compute-slowdown identification;R7-LIM-02 560-day data gap and no long-horizon coverage;R7-LIM-03 decomposition/filter/family instability;R7-LIM-04 no reliable bridge. These are explicit negative/inconclusive research results, not hidden successful tests. Existing DA-02/05/07/10 and Q1–Q3 provenance/transfer limits remain. DA-04 C8 four damaged files handled/excluded, source damage itself unresolved. No new P0 reopening Q1–Q3.

