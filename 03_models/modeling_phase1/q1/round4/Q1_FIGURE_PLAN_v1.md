# Q1 Round 4 figure plan v1

**状态：PAPER-READY FIGURE PLAN；图的数值仅从冻结 Round 4 CSV/JSON 生成。**图形不添加新统计结果，图注承担标题，图内不用重复标题。出版候选须在实际论文嵌入宽度下复核字体不低于 9pt、无遮挡；当前仍待整篇编译验收。

| Figure ID | 论点 / 读者任务 | 来源 | 预定角色 |
|---|---|---|---|
| FIG-Q1-R4-001 | 比较 A1 七域与 A2/A3 非重叠扩展的五 CORE 相对分位，说明多维与域差 | `Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv` | 正文候选 |
| FIG-Q1-R4-002 | 逐域检验 A7/1M M1 对 M0 的 RMSE 比，确认改善是否覆盖 13 域 | `P_RESPONSE_DOMAIN_VALIDATION_v2.csv` | 正文候选 |
| FIG-Q1-R4-003 | 对比 1M/60M/1B 的中心化配比效应，明确 1B 迁移失败 | `P_RESPONSE_VALIDATION_METRICS_v2.csv` | 正文候选 |
| FIG-Q1-R4-004 | 展示经验凸包与局部近邻支持分类人数，不把其误作现实供给 | `P_SUPPORT_VALIDATION_ROWS_v2.csv` | 附录/诊断候选 |

每图登记 Figure ID、`claim/source/reader_task/publish/placement` 于 `figures/figure_manifest.json`，保留 PDF 向量成品与 PNG 预览，并做视觉/哈希 QA。Round 3 结构图仍为诊断图，若进入论文需重新审视最终文字尺寸和主张。
