# DATA AUDIT — PHASE 1 本地执行／复核 Prompt

在 `D:\work document\codex\_work\mathmodel\F题\HuaweiCup_F_2026` 继续 2026 研究生数模 F 题。Discovery 六轮已经完成，`02_analysis/consensus/CONSENSUS_F_PROBLEM_ANALYSIS_v1.md` 是唯一 ACTIVE 研究设计共识；不要从零重做 Discovery，也不要选定 Q1–Q4 最终数学模型。

先完整读取：

1. `02_analysis/consensus/CONSENSUS_F_PROBLEM_ANALYSIS_v1.md`
2. `09_handoff/PROJECT_STATE.md`
3. `09_handoff/JOINT_CONTEXT.md`
4. `09_handoff/NEXT_ACTION.md`
5. `01_data/IDENTIFIABILITY_AUDIT_SPEC.md`
6. `10_review/ISSUE_TRACKER.md`
7. `01_data/audits/phase1/ROUTE_DECISION_AUDIT_PHASE1.md` 及 `route_audit_metrics.json`

按 `PROJECT_RULES.md` 与 `skills/data-audit/SKILL.md` 工作。原始附件 `01_data/raw/real_attachments/` 只读，哈希基线在 `01_data/raw/RAW_SHA256.csv`。对实际使用的表说明来源性质、路径/哈希、观测粒度、字段、缺失、重复、量纲和拟合/留出/外推角色。不要向外部服务上传原件。

本轮七项路线审计已首次执行，状态仅为 **CHECKED AUDIT RESULT**。如果要复跑，在项目根目录执行：

```powershell
python 04_code/data_audit/route_decision_phase1.py
```

脚本会重建 `01_data/audits/phase1/route_audit_metrics.json`、C8 文件清单及 AUDIT-01 分支输入/输出，并同步指标哈希。复跑后先核与现有报告的数字是否一致；任何差异记录输入哈希、脚本哈希和原因，不静默改结论。

按依赖顺序复核或增补：**AUDIT-01 → 04 → 07 → 02 → 03 → 05 → 06**。每项输出 `QUESTION → DATA USED → METHOD → EVIDENCE → DECISION → MODEL ROUTE IMPACT → FALLBACK → STILL OPEN`，说明保留/淘汰什么路线；不要只给相关系数或图。当前必须保持以下已测事实与证据边界，除非发现可核反证：

- AUDIT-01：A4/A5 512 条 p/Loss 按 index 配对；A1/A2/A3 三份必用 SlimPajama 质量信号分别为 51,230 / 17,523 / 203,752 条，均无同运行键，且 A1 与 A2/A3 分别重叠 1,419/10,000 个样本 ID。机器分支 `NO_MATCHED_Q`。A18 的 138,034 条 RegMix 原文只是可选辅助，不能误当 A2/A3。合法 p 基线满秩不等于独立 Q 可识别。
- AUDIT-04：13 域 Loss 尺度和相关异质；主响应权重仍未冻结。A6–A11 的 Loss 继续作为预留检验，不能据其调权。
- AUDIT-07：17 比例原表有约千分级舍入；检验配比多落在 A4 训练凸包之外。经验支持与现实供给分开，不能把整个 simplex 当可实施域。
- AUDIT-02：A/B 验证语料与 tokenizer 尚无共同标尺证据，不直接合并绝对 Loss。B1 的 1,176 行只是 8 个模型规模各 147 个相关检查点。
- AUDIT-03：B6 360 行完全嵌于 B7 且 Loss 相同；B8 在所有固定 N,D 组的 Q–Loss 斜率与 B6/B7 反向。B8 先隔离并追查生成机制；B6–B8 始终标 `SEMI-SYNTHETIC`，B8 的 `extrapolated` 行另标外推。
- AUDIT-05：C7 中 12/45 个架构上限达到 30,000 token，表里没有实际训练长度；约 30,000 只是题面成本代理的条件阈值。
- AUDIT-06：C5 是 C6 的模型子集，高可比层只有 7 个同族 Pythia；Strong Bridge 不能由覆盖统计直接放行。C4/C1 名称精确交集为零，C8 有 4 个坏 JSON；需实体/版本/时间对齐和按族/时间留出。

优先补查 B8 的生成代码或说明、Q_score 含义及其与 B6/B7 相反的原因；若仍找不到，保留来源冲突并交 Sol/Opus 联合审议，不用拟合消除冲突。随后继续所有题面必用文件的完整九维数据审计，拟定 Q1 主响应使用前预注册、A/B 标尺证据、p 现实供给和 C1/C4/C8 对齐。保持 `GATE 1 = CONDITIONAL / NOT FULLY CLEARED` 直至对应证据补齐。任何 Q3/桥接强数值结论、最终 Scaling Law、正式预测或论文结果都不得在此阶段生成。

写回 `01_data/DATA_AUDIT.md`、`DATA_DICTIONARY.md`、`09_handoff/PROJECT_STATE.md`、`JOINT_CONTEXT.md`、`NEXT_ACTION.md` 和相关 Issue；需要改变 ACTIVE 数学规格时先登记 `DECISION_LOG.md` 并交 Sol/Opus 收敛。所有本阶段产物只标 `AUDIT EVIDENCE` 或 `CHECKED AUDIT RESULT`，不要标 `VALIDATED FINAL RESULT`。
