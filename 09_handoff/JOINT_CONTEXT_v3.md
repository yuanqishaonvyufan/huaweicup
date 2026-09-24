# 当前阶段

STEP 1 联合赛题分析进行中：SOL BUILD、OPUS EXTEND、SOL SYNTHESIZE 已完成，等待 OPUS VERIFY。共享上下文 ACTIVE 版本：v3，快照见 JOINT_CONTEXT_v3.md；阶段尚未形成共识。

# 当前研究问题

共同厘清 F 题 Q1–Q4 的数学本质、数据与数学接口、理论和数据驱动部分、拟合/验证/外推角色、可信度边界与主要风险；第一轮暂不确定最终具体模型。

# 官方任务要求

读取 00_problem/original/F_2026_problem_user_supplied.docx、00_problem/OFFICIAL_REQUIREMENTS.md、PROBLEM_MAP.md 和 CONSTRAINTS.md。题面内嵌公式以 DOCX 原件核对；官方、外部建议和内部目标保持分离。

# 已确认的数据事实

原始附件在 01_data/raw/real_attachments/，2,012 个文件的复制哈希一致。初始文件角色见 01_data/DATA_INVENTORY.md；截至整合稿仅做先前少数 CSV 表头核对，没有启动完整数据审计。A/B/C 中真实、半合成、插值、估算和混合数据须区分。

# 当前模型方案

无 ACTIVE 或 FINAL 模型；四问 MODEL_INTERFACE 的 FINAL MODEL 均为 OPEN。

# Sol 最新贡献

02_analysis/consensus/JOINT_F_PROBLEM_SYNTHESIS_v1.md（DRAFT_FOR_OPUS_VERIFY）。基于 Sol 首稿与 Opus 延伸建立 14 项融合矩阵、Q/P 秩检验、Q1 主/次响应候选、分级标度律、Q3 结构转移候选和 Q3→Q4 三种桥接情景；纠正固定 q 的 p⊙q 识别、预算影响注意力/训练成本比及任意放行阈值。原 SOL_F_PROBLEM_ANALYSIS_v1.md 保留为第一轮来源。

# Opus 最新贡献

02_analysis/opus/OPUS_F_EXTENSION_v1.md（已保存，非最终共识）。提出 Q_eff 三路径、13 域 Loss 方案、分块 Q2、Q3 p 支持、Q4 分解/桥接与阶段门槛；其具体建议在整合稿中分别采纳、修正、暂缓或驳回。

# 当前共同认可内容

只有题面/数据说明支持的事实与项目工作流可作为共同已知。双方对不可识别、半合成证据和桥接风险有方向性共识，但尚未有经 OPUS VERIFY 后确认的数学规格或实验结论；整合稿不是 CONSENSUS。

# 当前未解决问题

见 OPEN_QUESTIONS.md 与整合稿 §18–19。最高优先为是否有逐配方独立质量变异、13 域主响应、A/B Loss 可比性、C7 长度范围、C5/C6 桥接覆盖及 Q4 贡献识别；完整数据审计未开始。

# 最近实验结果

无正式实验；RESULTS_REGISTRY 中无 VALIDATED 结果。

# 当前需要继续完成的任务

OPUS VERIFY：完整审阅 JOINT_F_PROBLEM_SYNTHESIS_v1.md，尤其 §2 的逐项取舍、§5 的秩条件、§8 的 C7 阈值、§15 Gates 和 §21 强/保守主线；逐项标记 KEEP、MODIFY、ADD、QUESTION、REJECT。若有 Critical 分歧回 Sol 修订/DEBATE；此时不生成 CONSENSUS。

# 禁止重新讨论的已确认事项

未经新原始证据或正式决策，不反复改写题面明确要求、原始文件哈希、结果必须来自真实运行及只有 CONFIRMED 数学规格可正式实现等既定项目合同。此项不意味着模型选择已被确认。

# 下一步

Opus 读取本文件、09_handoff/OPUS_CONTEXT.md、SOL_TO_OPUS_VERIFY_HANDOFF_v1.md 和 02_analysis/consensus/JOINT_F_PROBLEM_SYNTHESIS_v1.md 全文，写出 02_analysis/cross_review/JOINT_F_PROBLEM_REVIEW_v1.md。当前 Codex 回合在此停止。
