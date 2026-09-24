# Gate 1 Round A QA — 2026-09-23

审查范围：Round A 路线综合、Sol→Opus 交接、P1-1 预注册提案、B8 计划及 Phase 1 v2 证据修订。状态：**ROUTE DRAFT CHECKED / OPUS REVIEW REQUIRED**；不是数学模型或论文结果的 VALIDATED 状态。

## 证据与一致性

- 重新读取 ACTIVE 共识、Phase 1 报告、识别规范、状态/上下文、Issue、字典、清单、审计脚本和 `NO_MATCHED_Q` 分支；用用户提供的题面 DOCX 与数据说明 PDF 可见正文核对 A/B/C 编号和 Q3/4 约束。
- PDF 为 13 页、未加密、有文字层；发现页面 2–13 存在 5pt、近白色边缘文字，内容读取时按颜色/字号隔离。另渲染并目视核对第 2、9 页的可见 A 表和指标说明。DOCX 为 60 段、1 表、72 个 OMML 公式；本轮未作公式编辑，具体数学符号沿用已核的 ACTIVE 共识及原件可见上下文。
- Phase 1 初版把 A18 RegMix 文本误当 A2/A3。当前 v2 脚本对三份正确质量信号逐行解析、核哈希：51,230/17,523/203,752，运行键 0，A1 与 A2/A3 的 ID 重叠 1,419/10,000；分支输入与指标 SHA-256 一致，机器输出仍为 `NO_MATCHED_Q`。旧版报告/脚本/指标和分支另存 `superseded_v1/`，没有覆盖原始附件。
- QA 断言通过：修订证据哈希、19 条路线矩阵的 Decision 枚举、主稿 18 章节、产物本地链接、Sol→Opus 交接与 JOINT_WORK_LOG 一致。没有任何 ACTIVE FINAL MODEL、正式参数估计、Q3 求解、Q4 预测或论文数字。
- Gate 1 路线层级的 CONDITIONAL PASS 只是 Round A 提案；项目完整 DATA_AUDIT 仍 `CONDITIONAL / NOT FULLY CLEARED`，结构预检仍因没有 frozen processed 输入而未通过。P1-1 预注册也须在查看 A6–A11 留出 Loss 选模型前经 Opus 审核并冻结。

## 能力与工具取舍

- 使用项目本地 `joint-collaboration`、`data-audit` 与 meta-model-agent 阶段适配规则；用 Python 流式审计、哈希和分支器核实数据；只读使用 documents/pdf 技能检查原始 DOCX/PDF。长文档提取物与 PDF 页面预览放 `D:\work document\codex_work\F_gate1_roundA`，项目交付只写目标目录。
- 已有 RegMix、Pythia 和 Hugging Face 原始公开资料足够作本阶段来源先例；未调用 Firecrawl、未安装/连接外部插件，也未上传用户原件。未启用 `computational-realization` 求解、`validation-audit` 结果验证或论文/图表生成，因为还无 CONFIRMED 数学规格、processed 输入或正式结果。若以后进入这些阶段需重新复查技能和门槛。
- 本地 Codex 按用户指定 Sol Round A 任务撰稿，并在主稿/交接中明示未实际调用外部 Sol 或 Opus。下一轮只交 Opus 审查，不由 Codex 假扮已完成联合共识。
