# Q2 → Q3 interface v1

状态：CHECKED CANDIDATE / GATE3 PENDING，非新Gate共识。依据R5-SPEC-001和Round5真实结果。

主接口：`03_models/modeling_phase2/round5/Q2_TO_Q3_INTERFACE_v1.json`。

可携带：B1附件内部S1参数、源内N-D矩形支持、三类轨迹验证、全部导数、整轨迹参数集合。只有Gate3裁决后才能在Q3作为受限条件目标使用。区间不是外部预测误差保证。

需场景开关：质量增量g、有效D指数rho与A/B配比运输k均未真实识别，默认0；备选值只做条件机制压力测试。不得把B7刻度直接替代DQ0，也不得把1B失败的M1当作可迁移效应。R3领域异质性、p经验支持、实际供给成本必须分开。

不传：B8主参数、真实独立质量弹性、跨族统一绝对Loss、现实可部署最优、预算配置、KKT解或Q4能力桥接。本轮Q3/Q4未启动。

## A–J 准入分类（接管收口补充）

以下是**待 Gate 3 批准的接口用途**，不是已经启动 Q3 的授权。ENTER Q3 表示可供后续受限模型使用；所有情景必须包含默认零分支。与机器 JSON 的 `admission` 对应。

| 类别 | 传入内容 | 分类 | 证据与前置条件 |
|---|---|---|---|
| A N/D baseline | E、A、B、alpha、beta 及十亿单位 | ENTER Q3 | ATTACHMENT-INTERNAL ESTIMATED；仅 B1 曲面；Gate 3 待批 |
| B uncertainty | 200 个整轨迹参数向量、LONO 范围 | SENSITIVITY ONLY | DIAGNOSTIC ONLY；条件数值稳定性，不是外部概率覆盖或校准风险约束 |
| C marginals | dL/dN、dL/dD、总 Loss/超额 Loss 弹性 | ENTER Q3 | B1 附件内解析量，随 N/D 状态变化；幂指数不是总 Loss 弹性 |
| D substitution | 局部等 Loss 斜率及有限反函数 | ENTER Q3 | 必须检查反函数余项为正及替代后的 N/D 支持；不等于预算或真实节省 |
| E quality | g=lambda×0.3619952862；有效 D 的 rho 机制 | ENTER Q3 AS SCENARIO | B7 校准 SEMI-SYNTHETIC CALIBRATED；跨到 B1 为 SCENARIO-CONDITIONAL；g/rho 默认 0，不能映射 DQ0 |
| F mixture | A 源 centered/tangent response，外生 k(N) | ENTER Q3 AS SCENARIO | A 源关联为 EMPIRICALLY ESTIMATED，A→B 运输为 SCENARIO-CONDITIONAL；k 默认 0，当前 M1 的 1B 运输禁用，不强拟 scale coefficient |
| G support | N∈[0.070542,11.965825]B，D∈[0.134,299.893]B；p 支持证据 | ENTER Q3 | 矩形仅为插值候选域；Q1 凸包 2/256 与 NEAR/OUT 标签保留；现实供给另建，禁止 full-simplex 可部署解 |
| H evidence labels | 来源、Run ID、证据级别、候选状态 | ENTER Q3 | 强制携带，不随求解而晋升；TYPE E=0、FINAL=0 |
| I forbidden extrapolation | 外部通用系数、B8、绝对 Loss pooling、真实独立 Q 系数、1B M1 运输、域外保证 | DO NOT ENTER Q3 | 原限制均保留；B9/B10 只可做明确域外敏感性讨论，不作验证真值或正式支持域 |
| J missing cost inputs | 实际预算、硬件吞吐/利用率、训练计算系数与单位、数据采购/清洗/筛选成本、各域供给及去重有效量、质量投入映射 | DO NOT ENTER Q3 | 这些数值尚未取得/冻结；不得填默认“实测值”。下一阶段单独建立来源、单位和情景区间后再定可用性 |

N/D 有限替代：给定目标 L* 和新 N，`R=L*-E-A*N^(-alpha)` 必须严格为正，才有 `D=(B/R)^(1/beta)`。即使 R>0，超出支持的解仍仅为域外敏感性结果。质量和配比的替代率不具有同等级实证资格。

当前 Q2 **PROVISIONALLY CLOSED — ATTACHMENT-INTERNAL RESTRICTED CANDIDATE**；Gate 3 **READY FOR PRE-REVIEW / NOT PASSED**；Q3 **NOT STARTED**。
