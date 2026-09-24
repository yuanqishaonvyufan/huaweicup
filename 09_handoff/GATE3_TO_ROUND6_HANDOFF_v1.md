# Gate 3 → Round 6 handoff v1

**ACTIVE。授权：G3-SINGLE-001，Gate3 Verdict A — PASS。Q2 PROVISIONALLY CLOSED；Q3 AUTHORIZED TO START / NOT EXECUTED；Round6 READY；Q4 NOT STARTED。** 本交接不表示已执行优化。基准 Git main：`808565ddd10bde7bf8c30f89d8c0a7dadd098a80`。

## 1 baseline / units

采用附件 B1 的 `L=E+A*N^(-alpha)+B*D^(-beta)`，N/D 单位分别十亿参数/十亿 token；Loss 仅附件内部标尺。

| 参数 | 点估计 | 条件 2.5–97.5% 区间（仅敏感性） |
|---|---|---|
| E | 1.6897975629393145 | [1.6896305427433702,1.6899674533448488] |
| A | 0.3539803206519287 | [0.35375822727794193,0.3541190890645844] |
| B | 1.2403055835398427 | [1.2401726066429883,1.2404303828429686] |
| alpha | 0.3399765819061934 | [0.33980790884596923,0.340136856419515] |
| beta | 0.27987812854708494 | [0.2798238331994284,0.27993444220400676] |

主 Run：`EXP-Q2-ND-R5-20260924-v1`；情景只用 `SCEN-Q2-R5-20260924-v3`。主参数 ATTACHMENT-INTERNAL ESTIMATED；三类 macro RMSE .000146888187/.000111641982/.000114133980。12/12 初值、200/200 bootstrap 无边界；不重新拟合。区间不是外部世界不确定性，优先保留原整轨迹联合参数向量，不能混成独立边际区间的概率保证。

## 2 marginals / N–D substitution

U=A*N^(-alpha)，V=B*D^(-beta)：`L_N=-alpha*U/N`，`L_D=-beta*V/D`；总 Loss 弹性为 `-alpha*U/L`、`-beta*V/L`。等 Loss 局部 `dlogD/dlogN=-alpha*U/(beta*V)`。有限替代 `R=L_target-E-A*N_new^(-alpha)>0` 后才有 `D_new=(B/R)^(1/beta)`；结果另核支持，R≤0 无有限正解。

既有示例 N=1,D=100：L_N=-.12034501948，L_D=-.000956624288，弹性 -.05044689804/-.04010031168，对数替代率 -1.25801760446；N_new=.8 对应 D_new=135.55858089。它是模型示例而非资源最优。

## 3 quality / mixture / scale

质量共同 slope=-.36199528619528604 是 B7 的 SEMI-SYNTHETIC CALIBRATED 关系，45/45 单元为负；规模调节 centered 留组 RMSE .052964→.043679，不是新单元绝对预测或真实因果弹性。转入 B1/Q3 使用 `g=lambda*.36199528619528604`，lambda∈{0,.5,1,1.5}，SCENARIO-CONDITIONAL、默认 g=0。有效 D 机制 rho∈{0,.5,1}，默认0；局部匹配 rho≈1.892045 仅机制敏感性。不得把 Q_score 变为 DQ0；TYPE E=0。g 若随 N/D 变化必须加相应偏导；不能套用常数 g 的替代公式。

配比沿用 A 源 M1 的限定关联：1M 有效，60M 部分 centered-shape transfer，1B 失败。Q3 中 mixture/scale 只作场景/敏感性；k(N) 未识别、默认0，禁止 1B 当前 M1 运输与通用固定 mixture coefficient。A 源局部变化仍须在同尺度、支持核验后才可解释，R0 与 R3 并行；不自动加到 B1 绝对 Loss。

## 4 mandatory feasibility / evidence constraints

N∈[.070542,11.965825]B、D∈[.134,299.893]B 为主分析支持范围，矩形不等于所有点被独立验证。p 的 simplex 非负与和为1只是代数约束，还必须定义经验支持域、域外风险和实际供给上限；训练凸包/邻近证据不能直接宣布现实可实施。各域 token、去重/过滤后的有效 D 与配比须数量一致；正式优化前冻结约束和单位。

每个结果必须携带来源、Run、证据等级和情景开关；参数 bootstrap 仅 SENSITIVITY ONLY。不同假设下分别报告条件配置，不把半合成和运输系数混为“确定性最优”。域外分析单列且不称可部署。B8 QUARANTINED / SEARCH PAUSED；A/B absolute pooling 禁止；B1 外部 Alert v4 仍 PARTIALLY RESOLVED。

## 5 missing costs / next work

尚缺实际预算与币种/时间单位、硬件吞吐与利用率、训练计算系数/精度假设、数据采购/清洗/筛选成本、各域供应及去重有效量、质量投入响应或显式情景区间。不得用未经取得的数值冒充实测。它们是 Round6 需要建立并在**正式优化前冻结**的输入，不是阻止启动 Q3 规格/数据准备的 Gate3 条件。

下一回合先读 GATE3_CONSENSUS、冻结 Q2→Q3 Markdown/JSON 及 manifest，再准备 Q3 成本/供应、支持域、目标与验证合同。未取得现实输入时只能明确设条件情景；未冻结合同前不执行正式优化。除非发现具体 P0，不重开 Q2，不重新搜索 B1/B8 provenance。

本回合没有预算优化、KKT、资源分配、optimal N/D/Q/p 或 Q4 工作。状态保持 Q3 AUTHORIZED TO START / NOT EXECUTED。
