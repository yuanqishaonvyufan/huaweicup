# 阶段门槛与当前状态

当前：Round5 Q2研究包及候选QA完成，Gate3待审，Q3/Q4未启动；下表Round4阶段记录由末尾Round5更新补充。

本表吸收 meta-model-agent 的阶段证据逻辑，并以本项目路径表达。门槛分两层：stage_gate.py 的结构预检，以及对数学、数据、运行、图表和文字的实质审查。DISCOVERY 已 COMPLETE；CONSENSUS_F_PROBLEM_ANALYSIS_v1.md 为 ACTIVE 研究设计共识。GATE1_CONSENSUS_v1.md 已经 Opus Final Confirmation 晋升为 ACTIVE / CONDITIONAL PASS (ROUTE LEVEL)；Phase 1 七项路线审计为 CHECKED AUDIT RESULT，完整 Data Audit 尚未完成。Modeling Phase 1 Round 4 已本地 QA PASS，Gate 2 PASS WITH DOCUMENT-ONLY CORRECTIONS（G2-SINGLE-001）；Q1 PROVISIONALLY CLOSED；Round 5 READY / NOT EXECUTED。

| 阶段 | 结构证据 | 实质门槛 | 当前 |
|---|---|---|---|
| INITIALIZATION | 原件、目录、核心规则、联合协议与共同上下文、Skills、RAW 哈希清单 | 官方/外部/内部来源分离；无虚构模型与结果 | COMPLETE |
| DISCOVERY | JOINT_CONTEXT_v1.md、Sol/Opus 前六轮产物、v1.1、P0_CLOSURE_REPORT_v1.md、CONSENSUS_F_PROBLEM_ANALYSIS_v1.md、JOINT_WORK_LOG.md | 四问问题契约、来源与证据分级、P0-1 设计级关闭、Opus Final Check PASS、六项 P1 使用前门槛、研究设计共识；最终模型保持 OPEN | COMPLETE — CONSENSUS v1 ACTIVE |
| DATA_AUDIT | 字段字典、九维审计、预处理日志、数据版本、AUDIT-01 至 AUDIT-07 来源证据与分支记录 | PHASE 1 路线审计已做；Q1 A1–A3 九维审计 CHECKED；B1 外部来源 Alert v4 未解、附件内 B 级入口已获 Round 5 许可；其余必用数据继续按角色审计 | GATE 1 CONDITIONAL PASS — ACTIVE (ROUTE LEVEL)；完整 Data Audit IN PROGRESS |
| FORMULATION | 每问版本化数学规格、共识/决策 ID、验证方案 | 模型与算法分开；变量、目标、约束、识别、替代假设和预处理合同可核验；FINAL 规格 CONFIRMED | Q1 PROVISIONALLY CLOSED；M1 PROVISIONAL PREFERRED，Gate 2 已接受限定用途；Q2–Q4 无 FINAL 规格 |
| COMPUTATION | 04_code/ENTRYPOINT.md、code_manifest.json、逐问源码、配置、日志、实验 ID、原始结构化结果与代码哈希 | 真实执行、逐问覆盖、输入冻结、结果可复算、代码与数学规格一致 | Q1 正式训练 1、有效留出 1、失败隔离验证 1；Q2 N–D 拟合 0；其他未启动 |
| VALIDATION | 逐问验证报告与结果状态 | 合理基准、误差、敏感性、鲁棒性、外推、现实可行性；只让通过者进入 VALIDATED | Q1 A6–A11 留出及 Round 4 本地 QA PASS；Gate 2 通过限定用途，VALIDATED FINAL 仍 0 |
| EVIDENCE / SCHEMATICS | 图表登记、生成脚本、必要的可编辑示意源和视觉报告 | 图有论点、来源、单位、可读性；图表与结果 ID 一致 | Q1 四图五表为 CHECKED PAPER CANDIDATES；整体论文排版验收待做 |
| MANUSCRIPT | 官方模板源稿、章节、引用、附录、结果索引 | 数学、数值、图表、参考文献一致；每问有机制、求解、结果、验证和解释 | NOT_STARTED |
| ASSURANCE | 最终 PDF、交付清单、编译/渲染报告及哈希 | 当届格式与匿名、文件可打开、版面、支撑附件、最终结果/代码一致 | NOT_STARTED |

原 Skill 的字节阈值和固定中文文件名属于原生工作区的机器契约；本项目不伪称原生 gate_contracts.py 已通过。这里用可复核证据与项目本地检查器执行适配门槛。阶段完成或返工需同步 PROJECT_STATE.md、DECISION_LOG.md 和相关登记表。

## Round5 superseding status update

Q2 FORMULATION/COMPUTATION/VALIDATION/EVIDENCE候选研究已完成，数值与单图QA PASS；Gate3预审就绪，未裁决。先前表中Q2 N-D=0为Round4/Gate2历史状态，当前=1主运行。Q3/Q4未开始，完整四问COMPUTATION与最终MANUSCRIPT/ASSURANCE未完成。

## Gate3 decision — 2026-09-24

Gate3 ACTIVE / G3-SINGLE-001 / Verdict A — PASS；Q2 PROVISIONALLY CLOSED，Q3 AUTHORIZED TO START / NOT EXECUTED，Round6 READY。原表与 Round5 待审状态是历史。完整四问 COMPUTATION、MANUSCRIPT、ASSURANCE 尚未完成。


CURRENT 2026-09-25：Round6 Q3 FORMULATION/COMPUTATION/VALIDATION/EVIDENCE候选链完成、QA PASS，Q3 PROVISIONALLY CLOSED。Gate4 READY/NOT PASSED，Q4/完整全文MANUSCRIPT与ASSURANCE尚未启动；历史表不得覆盖PROJECT_STATE。


CURRENT Gate4 G4-SINGLE-001 ACTIVE / PASS，Q3 PROVISIONALLY CLOSED，Round7 READY，Q4 AUTHORIZED / NOT EXECUTED。只放行限定用途，无FINAL模型/结果晋升；旧阶段记录为历史状态。


## Round7 superseding status

Q4 formulation/computation/qualified evidence package COMPLETE; QA42/42. MODELING COMPLETE WITH RESTRICTED EVIDENCE SCOPE; Q1–Q4 PROVISIONALLY CLOSED. Round8 manuscript integration READY, not executed. Negative/unidentified findings remain mandatory; earlier current-status paragraphs are historical.
