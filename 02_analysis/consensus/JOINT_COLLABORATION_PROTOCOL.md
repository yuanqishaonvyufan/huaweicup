# Sol × Opus 联合研究协议

状态：ACTIVE。默认使用 JOINT COLLABORATION MODE；Sol 与 Opus 是平级核心研究模型。后接模型阅读前一模型的最新产物并继续推进，不从零重复回答，也不把两份方案交给 Codex 二选一。两者均可提出、修正或撤回模型、公式、假设、实验、验证和论文结构，具体职责随问题变化。

## 默认五轮循环

1. **SOL BUILD**：Sol 读取 JOINT_CONTEXT.md、当前问题、官方题面与要求、数据状态和上一阶段结果，形成 SOL_DRAFT_vX.md。首次 F 题分析用 02_analysis/sol/SOL_F_PROBLEM_ANALYSIS_v1.md。
2. **OPUS EXTEND**：Opus 必须读取对应 Sol 草稿，逐项标记 KEEP、MODIFY、ADD、QUESTION、REJECT，补充证据、推导、遗漏和风险，形成 OPUS_EXTENSION_vX.md。首次文件为 02_analysis/opus/OPUS_F_EXTENSION_v1.md。
3. **SOL SYNTHESIZE**：Sol 同时读取自己的草稿与 Opus 扩展，写明吸收、修改、暂不采用的内容及理由，形成 JOINT_SYNTHESIS_vX.md。首次文件为 02_analysis/consensus/JOINT_F_PROBLEM_SYNTHESIS_v1.md。
4. **OPUS VERIFY**：Opus 复核整合稿的逻辑、数学、数据支撑、假设、遗漏、可实现性、可写性和验证方案，形成 JOINT_REVIEW_vX.md。首次文件为 02_analysis/cross_review/JOINT_F_PROBLEM_REVIEW_v1.md。
5. **CONSENSUS**：若无 Critical 问题，将逐项状态与证据写入 CONSENSUS_vX.md；仅 CONFIRMED 数学规格交给 Codex/Skills 实现。首次文件为 02_analysis/consensus/CONSENSUS_F_PROBLEM_ANALYSIS_v1.md。若仍有 Critical 问题，继续 Sol 修正 → Opus 复核，直到收敛或登记为 OPEN。

每轮只在 JOINT_WORK_LOG.md 记录真正改变方案的增删改、未决问题、实验需求、收敛状态和下一负责人，不粘贴聊天全文。阶段共识可只确认问题结构和数据接口，不强行确认最终模型。

## 例外：独立分析

独立分析仅在明显争议、共同盲点嫌疑、核心选择久议不决、需要独立第二意见、或用户明确要求时启动。先在 OPEN_QUESTIONS.md 或 DEBATE_XXX.md 记录触发原因、范围和预期证据；需要消除锚定时，隔离该局部问题的输入与输出并冻结版本。独立结论回到联合循环核验，不自动替代共同方案。

## 分歧与本地执行

日常质疑写在扩展、整合和复核文件；只有实质分歧进入 debates。用推导、真实实验或可核验文献解决，不按表达自信程度裁决。Codex 保存产物、维护共享上下文、实现 CONFIRMED 规格、运行实验并登记真实结果；遇到互相冲突的数学方案，只记录 OPEN 和证据需求并交回双方，不擅自融合或裁决。

正式实验产生后，更新 JOINT_CONTEXT.md，将模型定义、配置、结果、误差和验证证据交给双方继续共同分析。模型、数据或结论变化必须更新决策和下游证据状态。
