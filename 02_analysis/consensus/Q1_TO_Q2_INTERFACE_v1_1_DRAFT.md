# Q1→Q2 Interface v1.1 DRAFT — after Round 3 candidate comparisons

**状态：DRAFT / NOT ACTIVE；待后续 Gate 与必要 Evidence Review。**继承 [ACTIVE v1](Q1_TO_Q2_INTERFACE_v1.md) 的分源、`NO_MATCHED_Q` 与识别边界，仅把 Round 3 的非最终比较结果按用途分层；不改变 Gate 1 共识，不确认 Q1 最终模型或 B1 baseline 资格。

| 类型 | 当前可传对象 | 当前证据地位 | 未来进入参数模型的条件 |
|---|---|---|---|
| **TYPE A — Descriptive representation** | A1/A2/A3 的 22 项使用资格、五核心 DQ0 透明相对分位摘要、DQ1/2/3 的结构与域敏感性、非核心信号面板 | `CHECKED/CANDIDATE`；更倾向多维剖面，DQ0 不是“真实质量”独立标量；A1 与 A2/A3 重叠 ID 不作独立验证 | 只可用于描述与机制假设；没有同运行训练 Q 的新识别证据时不转 TYPE E |
| **TYPE B — Domain/composition evidence** | A5 R0 为非最终主报告基线候选，R1 尺度敏感性、R2 结构探针、R3 13 域强制并行；A16 direct/near_direct/inferred 映射等级 | A5 训练内响应结构，**不是** p→Loss 拟合/留出验证；13 域显著异质 | 必须冻结 p 模型和响应选择、完成 A6–A11 预留检验、报告逐域误差与支持范围后才可运输受限 p 效果 |
| **TYPE C — Scenario information** | DSIR/QuRating/文本形态的分层描述；若外部设定 Q 变化，须标 `CONDITIONAL`；B6/B7 仅 E3 半合成支撑 | 场景与语义限制，不提供真实 Q 弹性；B8 继续 QUARANTINED | 明确假设、边界、校准和敏感性；不可伪称同运行干预 |
| **TYPE D — Model constraints** | p 非负且和为 1 的理论单纯形、A4 训练支持与零值、映射等级及当前不确定性 | 理论/经验/现实可行性分层；最终 p 可行域 DEFERRED | Q1 p 响应和 A6–A11 验证、真实供给证据后另审可实施域 |
| **TYPE E — Potential downstream variables** | **当前无获准变量** | 22 项下游资格为 17 `DESCRIPTIVE_ONLY`、5 `UNKNOWN`；`NO_MATCHED_Q` 持续 | 新的可核同运行 Q–Loss 配对与独立变化，完成泄漏、秩、精度、支持和留组审计；另立版本及 Gate 审查 |

**本轮界面变化：**v1 的 `quality_description` 与 `mixture_response` 现在有具体但非最终的候选表现和不确定性；没有将任何描述评分或域统计升级为 Q2 经验系数。B1 Alert 仍 `PARTIALLY RESOLVED / NOT YET ELIGIBLE`，所以 Q2 的来源内正式 N–D baseline 依旧暂停；A/B 绝对 Loss 不池化。若将来取得 B1 `val_loss` 来源或考虑仅附件内受限基线，须先独立更新 Q2 资格，不由本接口自动放行。
