# Gate 3 consensus v1 — single-pass decision

**STATUS: ACTIVE。DECISION ID: G3-SINGLE-001。日期：2026-09-24。**

**VERDICT A — PASS — Q2 PROVISIONALLY CLOSED, Q3 MAY START。** Q3 **AUTHORIZED TO START / NOT EXECUTED**；Round 6 READY，Q4 NOT STARTED。这是用户明确授权的一次短 Gate 裁决，未调用另一账号或冒称独立 Opus 审查；不进行预算优化、KKT、资源配置或最优 N/D/Q/p 求解。

同步起点与远端 main 均为 `808565ddd10bde7bf8c30f89d8c0a7dadd098a80`，工作区干净。审查依据是既有冻结规格、有效主 Run / 情景 v3、原数值 QA、接管 QA、registry、Q2→Q3 接口与权威 B1 Alert v4。只读核验记录见 [GATE3_DECISION_CHECK_v1.json](../../10_review/GATE3_DECISION_CHECK_v1.json)：89 项通过，包括原哈希、18 splits 成员隔离、机器指标和一个已有示例的公式核对；没有重拟合、重跑情景、重新寻找 provenance 或构造质量弹性。

## 六项裁决

| 问题 | 裁决 | 证据与放行范围 |
|---|---|---|
| 1 B1 baseline 资格 | PASS，限定附件内部 | 五参数加性幂律 S1 已满足冻结容差与稳定性要求，可作为 Q3 条件目标。仅 ATTACHMENT-INTERNAL ESTIMATED，不是 universal external Pythia law。权威 [B1 Alert v4](../../01_data/audits/modeling_phase1/q2/EVIDENCE_ALERT_B1_SOURCE_METADATA_v4.md)仍 PARTIALLY RESOLVED；其中“拟合未执行”是其形成时状态，不替代当前结果。 |
| 2 validation 与参数稳定性 | PASS，限定内部数值证据 | LONO/forward/blocked 分别 8/2/8 折，行不交叉；LONO/blocked 的 N 隔离、forward/blocked 的 D_rank 隔离成立。宏 RMSE 0.00014688818680258544 / 0.00011164198178839331 / 0.00011413398023678218。12/12 初值收敛、200/200 bootstrap 有效、无边界，未触发模型升级。误差极低表示附件曲面高度规则；小组数条件区间不包含外部来源或真实运行不确定性。 |
| 3 marginals / elasticity / substitution | PASS，允许进入受限 trade-off | U=A N^(-alpha)、V=B D^(-beta)；L_N=-alpha U/N、L_D=-beta V/D；总 Loss 弹性分别 -alpha U/L、-beta V/L；dlogD/dlogN=-alpha U/(beta V)。N=1,D=100 时数值与报告一致，N_new=.8 的 D_new=135.55858088564557。有限反函数须正余项，替代终点须在支持范围；不能将幂指数当总 Loss 弹性。 |
| 4 quality scenario | PASS，严格保留情景身份 | B7 45/45 单元负斜率，共同 slope=-0.36199528619528604；规模调节 centered 留组 RMSE .05296418456→.04367887260。测试单元均值用于中心化，只检生成表内形状。表内 SEMI-SYNTHETIC CALIBRATED；跨到 B1/Q3 只能 SCENARIO-CONDITIONAL；不是因果质量弹性，TYPE E=0。 |
| 5 mixture / scale | PASS，仅场景/局部有限用途 | A 源 M1 为 EMPIRICALLY ESTIMATED 关联，1M 有限支持，60M 部分 centered-shape transfer，1B 失败。Q3 内跨来源使用仅 SCENARIO-CONDITIONAL / 敏感性，k 默认 0。源内局部使用仍须核参考点、切向方向、R3 和经验支持；不能自动运输到 B1。无跨规模确定 coefficient，无已识别 scale interaction。 |
| 6 Q2→Q3 接口与可行域 | PASS，正式冻结 | [接口 v1](Q2_TO_Q3_INTERFACE_v1.md)的 A–J 四类准入全部接受；support-aware 约束、证据标签、外部 provenance 限制是强制输入。N/D 矩形不代表处处已验证，p full simplex 不是现实可部署域；实际成本与供应须在 Round6 正式优化前取得或显式设情景并冻结，不能混成确定性最优。 |

## 冻结参数与区间解释

N、D 均以十亿计，主 Run 为 `EXP-Q2-ND-R5-20260924-v1`：

`L=1.6897975629393145 + 0.3539803206519287*N^(-0.3399765819061934) + 1.2403055835398427*D^(-0.27987812854708494)`。

alpha 的条件 2.5–97.5% 区间为 [0.33980790884596923, 0.340136856419515]，beta 为 [0.2798238331994284, 0.27993444220400676]。完整五参数区间及 200 组联合参数保留在原 summary/cluster_bootstrap，不把五个独立区间任意拼接成有概率保证的参数集合。Q3 中作为 **SENSITIVITY ONLY**，不构造外部覆盖保证。

## 准入决定与禁止项

- **ENTER Q3**：B1 五参数及单位、N/D 导数/弹性、等 Loss 替代、支持约束、来源和证据标签。
- **ENTER Q3 AS SCENARIO**：质量 g/rho 机制、配比运输 k(N)，均包含默认零分支；情景得到的解只能称该假设下的条件配置。
- **SENSITIVITY ONLY**：整轨迹参数集合、LONO 范围、未校准域外/scale-interaction 假设；不得替代实际数据。B7 Qscale 系数只留生成表内诊断，跨源使用须另显式假设，不能成为确定交互系数。
- **DO NOT ENTER Q3**：B8、真实独立质量系数、通用 mixture/scale coefficient、跨源绝对 Loss pooling、当前 M1 的 1B 运输、外部通用指数/概率保证、未取得却冒充实测的成本/供给输入。

N∈[0.070542,11.965825]B，D∈[0.134,299.893]B 是受限主分析支持；域外只能明确敏感性讨论。p 经验支持与实际供给分开，保留 1M 凸包 2/256、2 IN/252 NEAR/2 OUT；不把训练 q95/q99 自动变成现实边界。Q3 须先冻结可行域与成本单位，不能跨证据等级给出唯一“确定性最优配置”。

## 问题计数、冻结与后续

本 Gate 新发现 **P0=0、P1=0、P2=0；阻断项=0**。本次状态生效与接口冻结属于正常 Gate 交付，不虚构文档缺陷。此前 R5 的修复计数仅属于历史审计；B1 外部来源、TYPE E=0、1B 失败、B8 和成本/供给缺口仍保留，均不被本 Gate 宣称已解决。

[接口冻结 manifest](Q2_TO_Q3_INTERFACE_FREEZE_v1.json)锁定 Markdown 与机器 JSON 的 SHA-256；数值仍指向原有效 Run，失败情景 v1/v2 隔离。Q1/Q2 PROVISIONALLY CLOSED，Gate2 原结论不变；本 Gate 不晋升 ACTIVE FINAL MODEL 或 VALIDATED FINAL RESULTS。除非 Q3 发现具体 P0，不重新打开 Q2。

下一步仅按 [Gate3→Round6 handoff](../../09_handoff/GATE3_TO_ROUND6_HANDOFF_v1.md)在后续回合启动 Q3；本回合到裁决、共识、接口冻结与交接为止。
