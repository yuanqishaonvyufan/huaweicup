# Gate 2 consensus v1 — single-pass decision

**STATUS: ACTIVE。DECISION ID: G2-SINGLE-001。日期：2026-09-24。**

**VERDICT B — PASS WITH DOCUMENT-ONLY CORRECTIONS — ROUND 5 MAY START。**两项文档修正已随本裁决完成，不设待修阻断。Q1 **PROVISIONALLY CLOSED**；M1 **PROVISIONAL PREFERRED Q1 p-RESPONSE MODEL**，无 ACTIVE FINAL MODEL 晋升。B1 **ATTACHMENT-INTERNAL RESTRICTED BASELINE ALLOWED FOR ROUND 5**。Round 5 **READY TO START / NOT EXECUTED**；Q2 **BASELINE MODELING AUTHORIZED**；Q3/Q4 **NOT STARTED**。

本次依据用户授权作一次 Gate 2 决策，未调用另一账号或冒称 Opus 复审；未进行新模型搜索、训练、留出验证或 Round 5 拟合。证据为 [Gate 2 预审包 v1.1](../../10_review/GATE2_PRE_REVIEW_PACKAGE_v1_1.md)、[Round 4 QA PASS](../../10_review/MODELING_PHASE1_R4_QA_20260924.md)以及下列已冻结产物。预审包和 Round 4 QA 保留形成时状态；本文件是后续门槛状态的权威来源。

## 六项裁决

| 问题 | 裁决 | 依据与放行边界 |
|---|---|---|
| Q1 质量表示是否严谨 | PASS，限描述用途 | [Q1 模型规格](../../03_models/modeling_phase1/q1/round4/Q1_MODEL_SPEC_v1.md)保留全 22 项画像；五核心仅作固定参考下多维描述坐标，DQ0 为 scalar descriptive summary。五维表示可保留，不宣称跨语言/用途普适稳定或已识别真质量；PCA/列表编码/长度与面效度限制保留。确认语义冲突 0，不制造冲突指数。 |
| Q2 M1 是否可暂定 | PASS WITH DOCUMENT-ONLY CORRECTION | [预拟合合同](../../03_models/modeling_phase1/q1/round4/P_RESPONSE_PREFIT_CONTRACT_v1.md)和冻结包确认 A4/A5 训练、16 自由坐标满秩、参数及升级门槛冻结。A7/1M M1 R0 RMSE 0.2278 vs M0 0.2846、13/13 域改善；M2 留出增益区间跨零；M3 训练残差触发未满足。A7 参与预先规定的候选验收与偏好判定，故不能称其完全未参与选模；未据此新增结构、调整超参数或回填参数。 |
| Q3 验证边界是否正确 | PASS | [验证报告](../../03_models/modeling_phase1/q1/round4/Q1_VALIDATION_REPORT_v1.md)：1M 为附件内同尺度验证；60M 仅部分 centered-shape transfer；1B 为 transfer failure。中心化 R0 误差比 60M=0.888、1B=3.108。R0 统一报告与 R3 逐域并行继续强制，不能作 cross-scale universal claim。 |
| Q4 支持/外推是否充分 | PASS，作为后续约束逻辑 | [支持证据](../../03_models/modeling_phase1/q1/round4/P_FEASIBLE_REGION_EVIDENCE_v1.md)：1M 为 2 IN/252 NEAR/2 OUT，训练观测凸包覆盖 2/256；主体证据来自局部近邻外推。禁止将 full-simplex 解宣布为 deployable optimum；Q3 必须采用 support-aware feasible-region logic 并另核现实供给。此处不确定最终约束集合或域外误差保证。 |
| Q5 Q1→Q2 接口是否正确 | PASS | [接口 v1.1](Q1_TO_Q2_INTERFACE_v1_1.md)传描述、领域/配比证据、条件情景和支持约束；TYPE E=0 independently estimable quality variables。没有新识别证据不得构造独立质量系数。 |
| Q6 B1 是否可进入 Round 5 | PASS，B 级附件内受限入口 | [B1 双层资格](../../01_data/audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md)与既有内部机器记录支持 8×147 N–D–Loss 网格、算术/轨迹一致性；现有材料未显示阻断级的附件内部不可比问题。仅授权研究附件内部给定 Loss 标尺；内部数值一致性不证明原运行真实共同语料/tokenizer。权威 [Alert v4](../../01_data/audits/modeling_phase1/q2/EVIDENCE_ALERT_B1_SOURCE_METADATA_v4.md)外部 provenance 仍 PARTIALLY RESOLVED，外部经验资格未恢复。 |

## 两项文档修正与 P0 判定

**G2-DOC-01（P2，已完成）：**统一描述为“结构、超参数及验收规则由训练阶段冻结；A7 留出用于预先规定的冻结候选比较和偏好判定，未回填模型”。因此 A7 不是在最终候选确定后仍完全未使用的独立最终测试集；报告的成对 bootstrap 区间是既定比较下的区间，不能宣称覆盖完整选择过程的不确定性。该事实符合原冻结合同，不构成新发现的泄漏或合同违反；M1 保留暂定资格，不要求补跑。

**G2-DOC-02（P2，已完成）：**修正 B1 Alert v4 到 Q2 规格的相对链接；在活跃状态/接口/资格文档同步 Gate 2 已放行的入口。外部来源事实与 Alert v4 版本不变，Round 4 历史预审包和 QA 不追改。

本次六项裁决 **P0=0；C/D 技术阻断=0**。未发现数据泄漏、留出污染、错误公式/映射/指标、冻结合同违反或 B1 附件内部不可比的实证依据。现有来源、规模和支持限制通过缩小用途保留，不借门槛通过消除限制。

## 正式跨问接口与 B1 授权

| TYPE | 放行内容 |
|---|---|
| A | descriptive quality evidence：Full-22、五核心分位向量、DQ0 描述摘要及限制 |
| B | domain/composition response evidence：M1 的 1M 关联、R0+R3、60M 部分形状转移、1B 失败；不直接运输到 B1 系数 |
| C | quality scenarios：显式条件假设；B6/B7 半合成证据分级；不得解释为真实独立质量弹性 |
| D | support constraints：经验支持/外推与供给约束分开；最终 Q3 可实施域仍待定 |
| E | **0 independently estimable quality variables** |

B1 仅用 `N_params_B,D_tokens_B,val_loss` 建立附件内部条件 N–D baseline，隔离未经溯源的 `precision/wd/lr/gpu_days/step_time/grad_norm` 等元数据。Round 5 须先冻结规格/训练验证合同并登记 Run，再做按八条 N 轨迹分组的留出与 D 段外推检查；八组是验证分组单位，不据此证明统计独立，1,176 个相关检查点不能随机按行拆分后冒称独立验证。拟合失败允许降为局部描述或 NO RELIABLE ATTACHMENT-INTERNAL BASELINE。A/B 绝对 Loss 不池化，B8 继续 QUARANTINED / SEARCH PAUSED。

正式训练仍为 `EXP-Q1-PRESP-TRAIN-R4-20260924-v1`；有效验证仍为 `VAL-Q1-PRESP-A6A11-R4-20260924-v2`，失败 v1 继续隔离。14 项结果和四图保持 CHECKED/CANDIDATE，不升级 VALIDATED FINAL。下一步依据 [Gate 2→Round 5 交接](../../09_handoff/GATE2_TO_ROUND5_HANDOFF_v1.md)启动受限 Q2；本轮未实际启动拟合。
