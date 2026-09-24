# Q1 to Q2 Interface v1 — Gate 1 convergence draft

状态：**CONFIRMED ROUTE INTERFACE UNDER [ACTIVE GATE 1](GATE1_CONSENSUS_v1.md)**。本文件只规定 Q1 当前允许向 Q2 提供的对象与证据边界，不是最终 Q1 模型输出，也不宣称 Gate 2 已通过。依据：ACTIVE 共识 C11–C16、[Phase 1 v2](../../01_data/audits/phase1/ROUTE_DECISION_AUDIT_PHASE1.md) 的 `NO_MATCHED_Q`、[P1-1 v1.1](../../01_data/audits/phase1/P1_1_13_DOMAIN_RESPONSE_PREREG_v1_1.md)。

| 接口对象 | 当前允许的内容 | 状态及进入 Q2 的门槛 |
|---|---|---|
| `quality_description` | A1/A2/A3 全量 22 信号经方向统一、列表压缩、冲突检查后的样本/域级描述分数、分布与不确定性；A1 与扩展集重叠 ID 单列 | 目前仅 **DESCRIPTIVE**；评分定义、尺度和稳定性须通过 Q1 审计/验证。不能自动命名为同运行独立 Q_r |
| `domain_mapping` | A16 的 3 direct、3 near_direct、11 inferred 映射等级及误差；质量侧 c4 无同名训练域 | 映射是一组假设与约束，inferred 不可冒充真实配对 |
| `mixture_response` | A4/A5 同 `index` 的 17 域配比与 13 域 Loss；零值安全 simplex 对比、训练支持、R0/R1/R2 候选及强制 R3 逐域 | Gate 2 对 A6–A11 预留检验后才可传已验证的受限 p 响应/误差；当前只能传规格与证据角色 |
| `quality_scenario` | 外部明确假设或 B6/B7 E3 半合成下的 Q 变化范围和符号敏感性 | 只标 **CONDITIONAL / SEMI-SYNTHETIC**；Q1 描述分数与 B 的 `Q_score` 未校准，B8 保持 QUARANTINED |
| `identification_status` | `NO_MATCHED_Q`、合法 p 基线秩、未测试的 Q_full/精度/留出及允许/禁止主张 | Q2 不得由 A4/A5 估独立 γ_Q，不得把固定 q 的 `pᵀq`/`p⊙q` 当独立干预 |

**接口形式**：Q1 输出质量描述、领域结构、配比响应、误差/支持域、条件情景与证据等级的分轨包；**不强迫一个未经识别的 Q 标量**。若未来发现真实同运行质量与独立变化，须按 `IDENTIFIABILITY_AUDIT_SPEC.md` 重新执行配对、泄漏、秩、精度、支持与留组分支，另立接口版本。当前 Q2 的 B1 N–D 候选与 A p 响应分源，任何数值合成须先通过可比性与运输检验。
