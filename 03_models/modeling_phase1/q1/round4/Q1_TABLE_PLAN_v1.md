# Q1 Round 4 table plan v1

**状态：PAPER-READY TABLE PLAN。**表中数值必须来自 Round 4 冻结 CSV/JSON，保留原单位、样本量、证据等级、失败情况与清晰脚注；正式论文中的表号待整体排版确定。

| Table ID | 内容 / 来源 | 用途 |
|---|---|---|
| TABLE-Q1-R4-001 | 22 项 Full-22 使用角色及下游资格；`Q1_FULL22_ROLE_MAP_v1.csv` | 交代“22 项完整画像”和“五维表示”的区别 |
| TABLE-Q1-R4-002 | A1 arxiv/github 与 A2/A3 非重叠扩展的五核心相对分位；`Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv` | 样本/扩展域级质量对照 |
| TABLE-Q1-R4-003 | M0/M1/M2 A5 五折及 A7 1M 主/逐域验证；训练/验证机器结果 | 选择 M1 的定量证据，M3 未激活 |
| TABLE-Q1-R4-004 | 13 域 A7 RMSE 与 M0 比、逐域排序；`P_RESPONSE_DOMAIN_VALIDATION_v2.csv` | 防止聚合 R0 遮蔽域别损失 |
| TABLE-Q1-R4-005 | 1M/60M/1B 相对形状、支持类别与误差；验证/支持机器结果 | 明确 1B 失败、A6/A8 共享 p、可行域仅为候选 |

脚本生成 Markdown/CSV 可检查表，不把表内 CANDIDATE 数字提前晋升 VALIDATED FINAL；Gate 2 后再决定正文/附录位置。
