# Gate 2 pre-review package v1.1 — Round 4 closeout

**状态：READY FOR GATE 2 PRE-REVIEW；GATE 2 NOT PASSED。**本版在历史 [v1](GATE2_PRE_REVIEW_PACKAGE_v1.md) 的基础上确认 Round 4 QA、已存在的四图五表、Results/Figure Registry 与 B1 Alert v4。用途是审查 Q1 暂定关闭范围和 B1 附件内部受限入口；不批准 Q2 正式 N–D 拟合、Q3/Q4、ACTIVE FINAL MODEL 或 VALIDATED FINAL RESULT。

## 1. 题目要求与已交证据

| Q1 要求 | Round 4 交付 | 当前证据边界 |
|---|---|---|
| A1–A3 全量质量指标与综合评价 | [Q1 质量两层规格](../03_models/modeling_phase1/q1/Q1_QUALITY_REPRESENTATION_FINAL_CANDIDATE_v1.md)、[Q1 模型规格](../03_models/modeling_phase1/q1/round4/Q1_MODEL_SPEC_v1.md)、Full-22/五核心域画像及[结果报告](../03_models/modeling_phase1/q1/round4/Q1_RESULTS_REPORT_v1.md) | 22 项全部入画像；五维有方向的描述坐标为主；DQ0 只作透明摘要，非可识别真 Q |
| 质量差异、冲突与稳健性 | 原文 14 案例面效度、Round 2/3 冲突/冗余/长度审计、Round 4 质量机器记录 | 确认语义冲突 0；统计分歧、域反转、冗余、尺度/长度伪象分别报告；代码/非英文反例限制普适质量解释 |
| A4/A5 领域配比与 13 域 Loss | [预拟合合同](../03_models/modeling_phase1/q1/round4/P_RESPONSE_PREFIT_CONTRACT_v1.md)、[模型比较](../03_models/modeling_phase1/q1/round4/P_RESPONSE_MODEL_COMPARISON_v1.md)、冻结训练包 | 17 份配比经归一与 Helmert 变换为 16 自由坐标；M0/M1/M2 已拟，M3 未触发；R0 透明统一报告 + R3 十三域强制并行 |
| A6–A11 外部检验 | [正式验证报告](../03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_A6_A11_v1.md)、逐行/逐域 CSV 与机器 JSON | A7/1M 同尺度通过；60M 仅中心化形状部分转移；1B 失败；A6/A8 同一 p 不视为两套独立支持 |
| 可行性与跨问传递 | [支持域证据](../03_models/modeling_phase1/q1/round4/P_FEASIBLE_REGION_EVIDENCE_v1.md)、[Q1→Q2 v1.1](../02_analysis/consensus/Q1_TO_Q2_INTERFACE_v1_1.md) | 经验支持与现实供给分开；TYPE E=0；最终 Q3 p 可实施域仍 DEFERRED |

## 2. 质量表示与 13 域响应

- A1/A2/A3 共 **272,505 物理行、261,086 不同 ID**。Full-22 角色：5 CORE、2 SECONDARY、12 SENSITIVITY、1 UNKNOWN、2 REDUNDANT；主描述为五 CORE 相对 A1 固定参考的五维分位向量。DQ0 为五维等权描述摘要；22 项没有同运行 A4/A5 质量干预键，不能估 Q2 独立 `γ_Q`。
- 五 CORE 的 PC1 方差份额 **48.11%**，DSIR 三列近重复且有长度效应，DQ2 pooled 分组仅在 3/9 域/扩展层复现。42 个冲突候选无已确认的语义冲突；域别反转、统计分歧、冗余、尺度/长度问题仍须写入结果与限制。
- P1-1 响应合同未改：R0 为原表 13 域 Loss 的透明等权报告基线，R3 强制逐域并行，R1 训练标准化敏感性，R2 结构诊断。R2 PC1 仅 **22.78%**、R0/R2 运行排序相关 **0.545**，不得以单一综合 Loss 代替领域异质性。

## 3. p 模型、训练冻结与失败运行

- 正式训练 `EXP-Q1-PRESP-TRAIN-R4-20260924-v1` 只用 A4/A5 **512** 配方，设计矩阵满秩 16、条件数 **45.4356**。17 部分原始零值保留，只校正原表总和舍入；使用零值安全的 Euclidean simplex contrast，不称 Aitchison ILR。
- M0 为十三域训练均值；M1 为各域 16D 线性响应；M2 在条件数触发后以训练五折选 ridge `α=0.01`。五折综合分数 M0/M1/M2 为 **1.001578/0.750417/0.749715**。M3 预注册残差触发为 false，未进入模型包。参数、合同和脚本在 A6–A11 Loss 读取前冻结，SHA-256 见训练/验证机器记录。
- `VAL-Q1-PRESP-A6A11-R4-20260924-v1` 在输出 JSON 时发生 NumPy int64 序列化错误，五个 CSV 隔离于 `failed_validation_v1/`，状态 `FAILED — NO VALIDATION DECISION`。有效留出仅为新 ID `VAL-Q1-PRESP-A6A11-R4-20260924-v2`，未回填参数或改合同。

## 4. 正式验证与可用范围

| 检验 | 冻结 M1 相对 M0 | 结论 |
|---|---|---|
| A7/1M，n=256 | R0 RMSE **0.227765 vs 0.284615**；13/13 域 RMSE 下降；R0 MSE 成对 bootstrap 差 **−0.02913**，2.5–97.5% **[−0.03949,−0.01893]** | 1M 同尺度、已观测/局部近邻配比范围的暂定预测改善 |
| M2 对 M1，A7/1M | R0 MSE 差约 −0.0000504，两层成对 bootstrap 区间均跨零 | 不增加复杂度，首选 M1 |
| A9/60M，n=256 | 中心化 R0/13 域平均 RMSE 比 **0.888/0.677** | 仅相对配比形状部分转移，无绝对 Loss 预测资格 |
| A11/1B，n=64 | 中心化 R0/13 域平均 RMSE 比 **3.108/1.967** | **TRANSFER FAIL**，不能运输 M1 的 1M 数值 p 效应 |

这些结果支持“配比响应在现有检验中不具规模不变性”的研究含义，尚未建立配比 × 规模交互模型。R3 十三域误差与 1B 失败须与 1M 正向结果同时呈现。

## 5. 支持与可行域

A4 训练 p 的观测凸包对 A6/A8 各仅覆盖 **2/256**；按训练留一近邻 q95/q99 和凸包预设分类为 **2 IN / 252 NEAR / 2 OUT**。A10 为 **15/46/3**；其凸包内点更多而 1B 仍失败，说明规模迁移问题不能只归因于 p 域外。NEAR 是局部经验外推，不是严格插值；OUT 样本过少，不能断言远外推安全。Q3 只能以理论 simplex、经验凸包、近邻扩展与现实供应证据分层构造候选约束，最终可实施域未定。

## 6. Q1→Q2、B1 与 B8

[接口 v1.1](../02_analysis/consensus/Q1_TO_Q2_INTERFACE_v1_1.md)传 TYPE A 多维描述、TYPE B 限 1M/部分 60M 的领域/配比证据、TYPE C 条件情景、TYPE D 经验支持约束候选，**TYPE E=0**。A/B 绝对 Loss 不池化；DQ0 不成为 Q2 真质量弹性。

B1 的权威[外部来源 Alert v4](../01_data/audits/modeling_phase1/q2/EVIDENCE_ALERT_B1_SOURCE_METADATA_v4.md)仍 `PARTIALLY RESOLVED`：缺 `val_loss` 行级原始 run、验证语料、tokenizer、抽取/变换锚，**外部经验资格 NO**。独立的[Round 4 双层裁决](../01_data/audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md)仅给 **B — ATTACHMENT-INTERNAL RESTRICTED BASELINE / PROVISIONAL PENDING GATE 2**：8×147 内部 N–D–Loss 表、算术和轨迹顺序自洽；未来只许可用 `N_params_B,D_tokens_B,val_loss` 研究附件内部标尺，需八条整轨迹留出和 D 段检验。Round 4 正式 N–D 拟合 **0**，本包不启动 Round 5。

B8 仍 `GENERATOR UNKNOWN / QUARANTINED / SEARCH PAUSED`；不入主参数，不阻断 Q1 收口。

## 7. QA、表图与审查问题

[Round 4 QA](MODELING_PHASE1_R4_QA_20260924.md) **PASS**，机器记录 `failures=[]`；原始 A4–A11 与冻结包/合同/脚本及所有既有输出哈希相符，从保存逐行预测复算 13 域和 R0 关键误差。QA 新增问题 P0=0、P1=1、P2=5，均已作收口修复；QA 不是 Gate 2 裁决。四张已有候选图和五张表经来源/文件哈希及视觉检查，见 [Figure Registry](../06_results/FIGURE_REGISTRY.md)、[Results Registry](../06_results/RESULTS_REGISTRY.md)。候选图未取得最终论文发布资格。

审查重点：① Full-22/五维/DQ0 与题面“质量评分”的措辞是否足够；② M1 的 1M 限定是否充分携带 1B 失败和支持风险；③ R0+R3、失败 v1 隔离和训练/留出冻结是否完整；④ B1 外部 NO 与附件内部 B 级提案可否并存，以及 Round 5 的最小验证门槛。请给出 `PASS CONDITIONAL / MODIFY / BLOCK` 的 **pre-review** 意见及 P0/P1 最短整改清单；不自动修改正式 Gate 2 状态。

## 8. 已知限制与停止线

[Q1 限制](../03_models/modeling_phase1/q1/round4/Q1_LIMITATIONS_v1.md)持续生效：五维 Q 非同运行质量效应、M1 非因果配比效应、13 域异质、A6/A8 重复 p、1B 失败、支持狭窄、B1 外部来源未解。此时 Q1 为 **PROVISIONAL CLOSURE / PAPER-READY DRAFT**；Gate 2 **READY FOR PRE-REVIEW, NOT PASSED**；Q2 正式模型、Q3/Q4、VALIDATED FINAL RESULT 均未启动或未获最终资格。
