# DATA_AUDIT

状态：DATA AUDIT IN PROGRESS。2026-09-23 已完成七项 **PHASE 1 / ROUTE-DECISION AUDIT** 的程序计算、来源核对和安全分支；详见 [路线审计报告](audits/phase1/ROUTE_DECISION_AUDIT_PHASE1.md)、[逐项指标与哈希](audits/phase1/route_audit_metrics.json)。这不是完整 STEP 2 九维审计或任何最终模型验证。

## Modeling Phase 1 Execution Round 1（2026-09-24）

- Q1 A1–A3 [完整九维质量信号审计](audits/modeling_phase1/q1/A1_A3_QUALITY_AUDIT_v1.md)已 CHECKED：官方 ID/路径/哈希及 22 指标键匹配；三表共 272,505 物理行、19 个数值不可用列表值、11,419 个跨表重叠 ID 的信号逐值一致。结构初判多维，DSIR 三列近重复，17 个质量方向未定；未生成最终 Q。机器细节与图在该目录。
- Q2 B1 [eligibility 审计](audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_AUDIT_v1.md)判 **NOT YET ELIGIBLE**。8×147 N–D 网格具独立几何变化，但 [Evidence Alert](audits/modeling_phase1/q2/EVIDENCE_ALERT_B1_SOURCE_METADATA_v1.md)记录 `precision` 元数据与 Pythia 官方训练精度矛盾及 Loss 源口径缺失；受影响的正式基线拟合暂停。
- B8 [机制调查](audits/modeling_phase1/parallel/B8_MECHANISM_INVESTIGATION_v1.md)完成第一层统计核验，分类 LIKELY SYNTHETIC RULE EFFECT 只是模式推断，生成器未找到，B8 继续 QUARANTINED；无新官方定义 Alert。三项均为 [AUDIT RUN](audits/modeling_phase1/AUDIT_RUN_REGISTRY.md)，无正式模型实验或 VALIDATED 结果。

## Phase 1 已核事实及门槛

- 修订 v2 已正确流式读完 A1/A2/A3 的 51,230 / 17,523 / 203,752 条 SlimPajama 质量信号；三表均无可配 A4/A5 的运行键。A1 的 arxiv 1,419 个 ID 与 A2 重叠，github 10,000 个 ID 与 A3 重叠，不能当独立重复实验。可选 RegMix 原文样本 A18 不再误列为扩展质量信号。A4/A5 512 条按 index 配对，合法 p 基线秩 17/17，但真实 Q 列缺失；机器分支仍为 `NO_MATCHED_Q`，Q_full 秩与独立效应未检验。
- A5 的 13 域 Loss 有异质尺度与弱公共因子；主响应权重尚未冻结。A4 配比和 0.996–1.003、零值比例 45.1%；舍入包络下 A6/A8 仅 21/256、A10 仅 41/64 落在训练凸包内或其显示精度邻域。
- A/B 无已验证的共同验证语料、tokenizer 或同运行锚点，不能直接池化绝对 Loss。B1 的 1,176 行是 8 个模型规模各 147 检查点，不是 1,176 个独立训练簇。
- B6 全部包含于 B7，重叠 Loss 一致；B8 与 B6/B7 在固定 N,D 下的 Q–Loss 方向全部相反，先隔离 B8 并追查生成机制。B6–B8 均保留 SEMI-SYNTHETIC 标签，B8 另有 720 行源表标 extrapolated。
- C7 的 45 个架构中 12 个上限达 30,000 token，但无实际训练长度；C5/C6 的 High 桥接仅 7 个同族 Pythia，Strong Bridge 未放行。C4 与 C1 模型名精确交集为 0，需实体对齐。C8 的 1,958 份 JSON 中 1,954 可解析、4 损坏。
- Gate 1：CONDITIONAL / NOT FULLY CLEARED。继续详细数据审计与有条件的 Q1 规格准备，不允许最终模型、正式结果和强桥接声明。

## 原件与异常

- 数据说明 PDF 为 13 页、未加密、有文字层；原件保留于 00_problem/original/。题面 DOCX 可打开。
- 数据说明 PDF 的多个页边位置嵌有 5pt、颜色约 #FCFCFC 的极浅色文本。渲染页面中几乎不可辨，但普通文本提取会把它与正文混合。内容含具体模型建议和未经程序运行的数字，且有与题面要求相冲突的说法。按不可信附加文本隔离：不从中提取官方要求、数据事实、参数或建模方案；后续阅读该 PDF 应按可见页面正文与题面原件核对。
- 附件数据分真实、半合成、插值、外推/估算、混合及参考文件，性质标签需贯穿模型与论文。

## 九维检查框架（Phase 1 仅完成路线所需切片）

| 维度 | 当前状态 | STEP 2 需核验 |
|---|---|---|
| 完整性 | 路线文件已核；全量未完成 | 编号 A1–A18、B1–B12、C1–C10 与实际路径映射，必用文件可读；C8 四文件损坏 |
| 缺失 | 路线关键列已核；全量未完成 | 字段缺失率与缺失机制 |
| 重复 | 已查 A index、B6/B7、C1/C3/C5/C6、C8；全量未完成 | 行、样本、模型与时序重复 |
| 异常值 | 已查 p 闭合与 B8 方向；全量未完成 | 非法范围、重尾、录入错误 |
| 单位量纲 | 已核 N/D 标头与 C7 上限；全量未完成 | 十亿参数/Token、10^21 FLOPs、百分制及 Loss |
| 分布 | 已查 13 Loss、Q 网格、C7；全量未完成 | 逐关键变量分布和分层 |
| 相关/共线性 | 已查合法 p 基线秩及 13 Loss 相关；Q_full 无法检验 | 指标、配比、规模与时间依赖 |
| 数据泄漏 | 已保持 A6–A11 Loss 的预留角色；全量未完成 | A 训练/检验/外推表、C 版本与榜单、派生表 |
| 训练/验证/外推角色 | B6–B8、C5/C6 与 A 检验角色已分层；全量未完成 | 每个文件的允许用途和可信度边界 |

不能用“文件存在”代替字段、样本和质量审计；也不能把说明中的近似条数写成实测统计。
