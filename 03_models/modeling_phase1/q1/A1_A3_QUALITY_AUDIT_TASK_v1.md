# Workstream A — Q1 Phase 1A audit task v1

**STATUS: INITIALIZED / NOT RUN.** 任务入口为 A0 [P1-1 FINAL v1](P1_1_13_DOMAIN_RESPONSE_PREREG_FINAL_v1.md)和 [A1–A3 官方映射](A1_A3_OFFICIAL_MAPPING_v1.csv)。正式审计必须先核官方 ID/角色/实际路径/字段粒度/原始哈希；A18 可选原文不能代替 A2/A3。

## 输入与执行合同

输入为 A1 51,230 条抽样信号、A2 arxiv 17,523 条、A3 github 203,752 条；这些计数来自已核 Phase 1 v2，是本次完整审计的核对基线。三表共有 22 指标；A1 有 content/domain 等辅助列，A2/A3 的域取自文件路径。A1 与 A2/A3 分别重叠 1,419/10,000 个 ID，必须核值一致性和去重粒度，不能当独立重复实验。流式处理，保留原件；指标语义/方向/列表维度不明时明确 OPEN，不用平均值或评分结果掩盖。

| 审计维度 | 本轮后续必须计算/记录 |
|---|---|
| 1 Completeness | 官方映射、文件哈希、解析成功/失败、记录数、22 键与每行 schema |
| 2 Missingness | null/NaN/空列表/无效码，按指标、来源和域分层；区分缺键与缺值 |
| 3 Duplicate structure | 表内 ID/内容或信号重复、A1 与扩展集重叠及同 ID 值一致性 |
| 4 Outliers | 极端量级、非法范围、重尾；先查定义，不任意删除 |
| 5 Units/scale | 14 标量和 8 列表的量纲、正/负/非单调方向、列表长度/分量含义、压缩候选 |
| 6 Distribution | 分位数、稀疏/零值、近常数、偏态、域内外分布；不输出最终 Q |
| 7 Correlation/redundancy | 原尺度与稳健/rank 相关、冗余和共线诊断；必须注明有效样本与处理版本 |
| 8 Leakage/derived risk | 指标是否共享生成器/衍生关系、A1/扩展重叠、任何 Loss 监督或数据切分风险 |
| 9 Experimental/evidence role | E1 质量描述粒度、与 A4/A5 无同运行 Q、必用/检验角色和允许主张 |

## 预期产物（尚未生成）

在 `01_data/audits/modeling_phase1/q1/` 生成 `A1_A3_QUALITY_AUDIT_v1.md`、`QUALITY_SIGNAL_DICTIONARY_v1.md`、`QUALITY_SIGNAL_DIAGNOSTICS_v1.csv` 与 `QUALITY_SIGNAL_AUDIT_FIGURES/`。字典逐指标列实际字段、类型、单位、方向依据、列表压缩候选、缺失与风险；图只服务于相关/维度/域差异判断。执行脚本、环境、输入/输出哈希与失败日志必须保存。

## 后续 A2–A7 的顺序

完整审计完成后才进入 22 信号质量结构 → 可解释冲突定义候选 → 描述 Q 候选（透明 baseline 必有）→ 按 P1-1 的 R0–R3 比较 → 合法 compositional p baseline → A6–A11 的支持内外、排序/参数/域效应/残差验证。PCA 等工具可用于诊断，不预定最终评分。所有真实候选模型比较先登记 Experiment ID；每步保留审计/模型版本与下一步资格，不跨步产生最终 Q 或最终 p 可行域。
