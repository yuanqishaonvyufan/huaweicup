# 2026 年中国研究生数学建模竞赛 F 题研究工程

当前进度：Round5 Q2受限研究包完成，Gate3预审就绪；请先读09_handoff/PROJECT_STATE.md。Q3/Q4未启动，FINAL模型/结果仍无。

题目：算力约束下提升大语言模型能力的资源配置建模。

## 当前状态

- 状态：DISCOVERY COMPLETE；CONSENSUS_F_PROBLEM_ANALYSIS_v1.md 为 ACTIVE 研究设计共识，[GATE1_CONSENSUS_v1.md](02_analysis/consensus/GATE1_CONSENSUS_v1.md) 为 ACTIVE 路线共识，Gate 1 CONDITIONAL PASS (ROUTE LEVEL)。Modeling Phase 1 Round 4 COMPLETE — 本地 QA PASS；Gate 2 PASS WITH DOCUMENT-ONLY CORRECTIONS（B）；Q1 PROVISIONALLY CLOSED；Round 5 READY TO START / NOT EXECUTED。
- 赛题、数据说明及 2026 年论文规范、模板、上传手册见 00_problem/original/。
- 原始数据已完整复制到 01_data/raw/real_attachments/，不得在原位清洗或覆盖。
- Q1 已有 1 次正式训练、1 次有效 A6–A11 留出及 1 次失败隔离验证；M1 为 PROVISIONAL PREFERRED 候选。没有 ACTIVE FINAL MODEL 或 VALIDATED FINAL RESULT，正式 B1 N–D 拟合为 0。
- Q1 的 Full-22/五维质量表示、13 域 R0+R3、1M 改善、60M 部分形状转移和 1B 失败已收入 [Gate 2 预审包 v1.1](10_review/GATE2_PRE_REVIEW_PACKAGE_v1_1.md)；B1 外部来源仍未解，附件内 B 级受限入口已由 [Gate 2 共识](02_analysis/consensus/GATE2_CONSENSUS_v1.md)允许进入 Round 5；B8 继续隔离。下一步见 [NEXT_ACTION.md](09_handoff/NEXT_ACTION.md) 与 [MODELING_PHASE1_STATE.md](03_models/modeling_phase1/MODELING_PHASE1_STATE.md)。
- meta-model-agent 已通过 META_MODEL_AGENT_ADAPTER.md 对接本项目六步流程；原生状态机没有直接运行。

## 工作区

00_problem 存题面、官方要求和任务依赖；01_data 存原始与处理后数据及审计；02_analysis 存 Sol/Opus 联合草稿、延伸、整合、复核、争议与共识，independent 仅供特定触发时使用；03_models 存逐问模型规格；04_code 存实现；05_experiments 存实验配置与注册；06_results 存结果及图表登记；07_validation 存检验；08_paper 存论文骨架与各格式；09_handoff 存共同上下文、状态和交接；10_review 存检测与整改；11_delivery 存最终交付；skills 存项目本地 Skill。

## 使用顺序

1. 先读 PROJECT_RULES.md、META_MODEL_AGENT_ADAPTER.md、00_problem/OFFICIAL_REQUIREMENTS.md、09_handoff/PROJECT_STATE.md 与 JOINT_CONTEXT.md。
2. 默认 MODE A 联合协作：Sol 建立第一版，Opus 读取并延伸，Sol 整合，Opus 复核，形成阶段共识；逐轮文件和记录见 02_analysis/consensus/JOINT_COLLABORATION_PROTOCOL.md。
3. 实质争议进入 debate；仅在争议、共同盲点、核心选择久议不决、需要独立第二意见或用户明确要求时使用 MODE B 独立分析。只有 CONFIRMED 数学规格可进入正式代码实现。
4. 数据审计、实验运行、结果验证和论文写作按证据链递进。论文数字只能来自 06_results/RESULTS_REGISTRY.md 中的 VALIDATED 记录。
5. 检测与整改使用 MODE C；核心数学定义、数据口径或结论变更须先登记决策。

Sol 和 Opus 是内部双核心研究接口。项目文件并不代表已调用或接通任何外部模型。

## 来源与可信度

原件与 SHA256 见 00_problem/original/SOURCE_MANIFEST.md。赛题 DOCX 与数据说明 PDF 由用户提供；当届格式、模板和上传手册来自竞赛平台公开附件。数据说明 PDF 的页边存在极浅色附加文字，已在 01_data/DATA_AUDIT.md 中隔离；不得把这些文字当作官方题意或真实结果。

## Current: Round5 Q2 complete, Gate3 review ready

Read [PROJECT_STATE](09_handoff/PROJECT_STATE.md), [Q2 results](03_models/modeling_phase2/round5/Q2_RESULTS_REPORT_v1.md), [Gate3 package](10_review/GATE3_PRE_REVIEW_PACKAGE_v1.md). B1 restricted candidate fitted/validated; quality and mixture remain evidence-tiered scenarios. Q3/Q4 not started. No final model/result promotion. User-authorized Round5 sync to GitHub. Prior Round4 summaries below/above retain historical context.
