# Gate 2 pre-review package v1 — Q1 closure + B1 restricted baseline decision

**给 Claude Opus 的独立 Evidence Review。请只审本包所列模型规格、关键结果、验证、限制、接口和 B1 资格；不要重做 Discovery、Gate 1、原始数据审计、拟合或网页搜索，不要改项目文件。**请明确哪些结论达到 Q1 paper-ready 的“暂定可写”标准，哪些仍不能进入 Q2。输出 `KEEP / MODIFY / QUESTION / REJECT` 及 P0/P1 问题、Gate 2 pre-review 意见与最短整改清单；不得补造数值。

## 冻结状态

Discovery COMPLETE；Gate 1 ACTIVE / CONDITIONAL PASS（路线层级）；Gate 2–4 NOT STARTED。Round 4 首次正式 Q1 p 模型训练 1 次、有效 A6–A11 留出验证 1 次、首次验证因 JSON 序列化失败隔离 1 次。Q2 正式 N–D 拟合 0，Q3/Q4 未启动。全部结果仍 PROVISIONAL/CANDIDATE；ACTIVE FINAL MODEL 和 VALIDATED FINAL RESULT 均 0。用户提供《数据说明》PDF 的 96 段近白色页边诱导文字已按物理位置/样式隔离，不作为官方事实。

## Q1 质量表示与冲突（[规格](../03_models/modeling_phase1/q1/round4/Q1_MODEL_SPEC_v1.md)、[结果](../03_models/modeling_phase1/q1/round4/Q1_RESULTS_REPORT_v1.md)、[限制](../03_models/modeling_phase1/q1/round4/Q1_LIMITATIONS_v1.md)）

- A1/A2/A3 全量 272,505 物理行、261,086 不同 ID；Full-22 画像保留所有指标角色：5 CORE、2 SECONDARY 长度、12 SENSITIVITY、1 UNKNOWN DSIR 代表、2 REDUNDANT DSIR。22 项 `DOWNSTREAM_ELIGIBILITY` 仍为 17 `DESCRIPTIVE_ONLY` + 5 `UNKNOWN`，TYPE E=0。
- 主描述是五 CORE 相对 A1 固定训练参考的**五维分位向量**；DQ0 只作等权标量摘要。五 CORE 的 PC1 仅解释 48.11%；DQ2 pooled 分组仅在 3/9 域/扩展分析层复现，A2 对 argmax 压缩敏感。A1 arxiv/github 与 A2/A3 非重叠扩展的各 CORE 均值相近，但同属一标注体系，不是独立干预。
- A1 原文按七域固定 5/95 分位抽 14 案例面效度检查：广告/新闻、目录/连续文本等部分符合预期，代码和非英文条目提供明显用途/语言反例；不是人工真值。确认的 SEMANTIC CONFLICT = 0；统计分歧、域别反转、冗余、长度/尺度候选分开写，未制造冲突指数。
- A1–A3 无配方运行键，描述 Q 与 A4/A5 不能真实同运行匹配；不得推出 Q2 独立 Q 弹性。

## Q1 p→13 域 Loss（[模型比较](../03_models/modeling_phase1/q1/round4/P_RESPONSE_MODEL_COMPARISON_v1.md)、[正式验证](../03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_A6_A11_v1.md)、[响应选择](../03_models/modeling_phase1/q1/round4/Q1_RESPONSE_SELECTION_REPORT_v1.md)）

- A4/A5 512 训练配方；17 部分 p 只按原表千分位舍入归一、零值保留，使用 16D Helmert 对比，无非法 17p+截距。M0 各域均值，M1 13 个域的同输入线性模型，M2 ridge 在条件数45.44触发、A5 五折 α=0.01；M3 训练内残差门槛未触发。M1/M2 A5 五折综合分数约 0.7504/0.7497，M0 1.0016；参数在读取 A6–A11 Loss 前冻结。
- 有效正式验证 Run `VAL-Q1-PRESP-A6A11-R4-20260924-v2`：A7/1M 256 行，M1 R0 RMSE **0.2278** 对 M0 **0.2846**；平均逐域 RMSE **0.4540** 对 **0.7129**，**13/13** 域改善。M1−M0 R0 MSE 的成对 B=500 bootstrap 差 **−0.02913**，2.5–97.5% **[−0.03949,−0.01893]**；逐域平均标准化 MSE 差 **−0.5804**，区间 **[−0.6276,−0.5359]**。M2−M1 两层收益区间均跨 0，故按停止规则暂选 M1，不升级。首次验证 v1 只因 JSON int64 序列化失败，CSV 已隔离，无模型或数据变动。
- P1-1 定义未改：R0 原始等权 Loss 作为 **PROVISIONAL PRIMARY REPORTING RESPONSE**，R3 十三维强制并行，R1 尺度敏感性、R2 结构诊断。R2 PC1 仅解释 22.78%，R0/R2 排序相关 0.545；A7 的 13 域误差并报，不能只给 R0。
- A6/A8 是哈希相同的同一 256 配比，不是两份独立 p 支持。A9/60M 的 M1/M0 中心化 R0/平均逐域 RMSE 比 **0.888/0.677**（只表示相对形状部分转移）；A11/1B 为 **3.108/1.967**，**FAIL**。不存在已验证的跨规模通用 p 效应或 1B 绝对 Loss 预测。
- A4 训练留一近邻阈值 q95=`0.2600`、q99=`0.2805`；A6/A8 各 **2 IN/252 NEAR/2 OUT**，A10 **15/46/3**。观测凸包对 1M 仅含 2/256，但局部近邻覆盖多；OUT 样本太少。1B 在更多凸包内点仍失败，不能只怪 p 支持。最终 Q3 p 可实施域仍 DEFERRED。[经验支持报告](../03_models/modeling_phase1/q1/round4/P_FEASIBLE_REGION_EVIDENCE_v1.md)

## Q1→Q2 与 B1（[接口 v1.1](../02_analysis/consensus/Q1_TO_Q2_INTERFACE_v1_1.md)、[B1 双层裁决](../01_data/audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md)）

- TYPE A 质量多维描述；TYPE B 是经 A7 1M 验证但规模受限的 p/13 域证据；TYPE C 条件情景；TYPE D 经验支持约束候选；**TYPE E=0**。不可把 DQ0 数值搬进 Q2 当真实 Q 系数，也不池化 A/B 绝对 Loss。
- B1 外部经验资格 **NOT ELIGIBLE**：行级原始 run/验证语料/tokenizer/处理链无锚；Alert 继续 `PARTIALLY RESOLVED`，不声称 B1 是经核实的公开 Pythia 原始验证曲线。
- 独立的附件内部受限资格暂定 **B — ELIGIBLE FOR ATTACHMENT-INTERNAL RESTRICTED BASELINE**：官方可见正文定义 B1 内部 Loss 列，原件 1,176 行形成 8×147 全网格，同规模随 D 和固定 D 随 N 均无 Loss 反增，D/计算量/PPL 算术自洽；异常 `precision/wd/lr` 整体隔离，拟模只用 N,D,val_loss。B 只许可写“比赛附件内部 Loss 标尺的条件/相对 N–D 曲面”，须整轨迹留出，不能推广外部 Pythia、不能拟 Q 效应。**Round 4 未拟 N–D**；[Round 5 待审规格](../03_models/modeling_phase1/q2/Q2_BASELINE_MODEL_SPEC_v1.md)。
- B8 `GENERATOR UNKNOWN / QUARANTINED / SEARCH PAUSED`；无主参数用途。

## 请重点回答的 Gate 2 问题

1. Full-22 画像 + 五维定向表示、DQ0 限制和 A1 原文反例，是否足以形成**暂定可写**的 Q1 质量章节？哪里仍有题面完整性风险？
2. M1 的 A7 同尺度双层改善与 13/13 域结果，是否足以支持**限 1M/经验近邻**的 p 响应候选？1B 失败应如何限制模型名、摘要和 Q1→Q2 运输？
3. R0+R3 选择、训练/留出隔离、A6/A8 重复支持及凸包/近邻分类是否有关键方法漏洞？
4. TYPE E=0 与来源内 B1 **B 级受限入口**可否并存？Round 5 可否在明确附件内措辞和整轨迹留出条件下启动 N–D，还是必须降为 C？
5. 给出 `PASS CONDITIONAL / MODIFY / BLOCK` 的 Gate 2 **pre-review** 意见、P0/P1 问题和最短整改清单；不要把本预审写成正式 Gate 2 已通过。

## 复核包边界

上述结论已由 Round 4 本地 QA 核查原件/代码/结果哈希、13 域预测关系、支持分类、表图和登记一致性；QA 报告为 `MODELING_PHASE1_R4_QA_20260924.md`。Opus 请只审逻辑、证据等级、是否越界和应补门槛，不重做数值工作或新建模型。
