# Q3 → Q4 interface v1

STATUS: ACTIVE / FROZEN — GATE4 ACCEPTED FOR RESTRICTED Q4 USE。授权G4-SINGLE-001，Verdict A — PASS。Q3 PROVISIONALLY CLOSED；Q4 AUTHORIZED TO START / NOT EXECUTED。

机器接口03_models/modeling_phase3/round6/Q3_TO_Q4_INTERFACE_v1.json；哈希见Q3_TO_Q4_INTERFACE_FREEZE_v1.json。仅冻结准入用途，原数值/Run/证据等级不变。

## A–J 准入分类

| 类别 | 输出 | 分类 | 强制边界 |
|---|---|---|---|
| A | budget-conditioned optimal N path | ENTER Q4 | B1附件曲面+题面FLOPs代理的条件配置；非历史实际N，十亿单位，支持[.070542,11.965825]。 |
| B | budget-conditioned D path | ENTER Q4 | 同一D用于训练/质量处理/注意力，十亿token，支持[.134,299.893]。不是已经识别的quality-adjusted effective D；若Q4新增有效D，须新定义与证据或另标情景。 |
| C | predicted Loss path | ENTER Q4 | 仅B1附件量尺，quality OFF/mix OFF基线；非跨来源统一absolute Loss或Benchmark。桥接须Q4另证；非零quality路径按E为情景。 |
| D | 200联合参数及51000配置/条件分位 | SENSITIVITY ONLY | 保留参数相关性；附件内条件数值稳定性，非外部覆盖或历史波动分布。 |
| E | quality paths / investment break-even | ENTER Q4 AS SCENARIO | B7内部SEMI-SYNTHETIC CALIBRATED，运输SCENARIO-CONDITIONAL；OFF为baseline，q0非DQ0，门槛非企业实证阈值。 |
| F | local / attenuated / zero-transfer mixture paths | ENTER Q4 AS SCENARIO | A源1M局部关联，60M仅部分形状；衰减系数未校准，1B失败禁运。513凸包候选、R3并行、真实供给未知，B1主运输0。 |
| G | active constraints / support-cap transitions | ENTER Q4 | 基线适用范围及条件机制元数据；quality/cap/供应等情景的活跃集携带对应情景标签。统计支持非实测供应，平台非现实前沿饱和。 |
| H | budget/support/quality/context shadow values | SENSITIVITY ONLY | model/data-support constrained marginal return；mu为Loss/1e18 FLOPs，dF*/dC=-mu/1e18，非经济价格或算力最终收益。 |
| I | context scenarios | ENTER Q4 AS SCENARIO | C7五档仅architecture maximum，2048为外生参考选择；非实训长度，30000仅成本交点，当前目标无已识别context能力收益。 |
| J | evidence grade / units / source / Run / caveats | ENTER Q4 | 强制元数据，不因下游使用晋升；TYPE E=0、B8隔离、A/B分源、FINAL=NONE。 |

## Scale expansion / non-scale progress

Scale expansion主要由N、D、compute/budget路径描述；Q3路径是条件反事实，不是发布历史。真实规模变化需Q4从C数据识别。Quality improvement、mixture improvement、efficiency improvement、architecture/technical shift只为non-scale候选解释，必须新核模型版本、时点、评价口径及规模控制；不能把情景收益或回归剩余项自动命名为真实技术进步。

## DO NOT ENTER Q4

B8；真实因果quality elasticity；跨来源统一absolute Loss；universal mixture effect；1B当前M1运输；C7 max=actual training context；30k empirical threshold；support-bound plateau=real-world frontier saturation；FLOPs proxy=真实经济成本；Q3场景=历史技术进步；未识别的quality-adjusted effective D；未经Q4验证的Loss→Benchmark或12/24月预测。

有效Run：EXP-Q3-BASE-R6-20260924-v1、SCEN-Q3-R6-20260924-v1、UNC-Q3-R6-20260924-v1。影子价、参数、图表、原始结果和QA保持不变；用途放行不晋升FINAL模型/结果。旧Round6报告的Gate4待审为形成时状态，当前以GATE4_CONSENSUS为准。

后续Q4需自行核C1–C10实体/时间/族、规模与非规模证据、C8任务聚合及桥接有效域；预测不可把Q3反事实作为历史训练样本。本Gate完成后停止，Q4未执行；无具体P0不重开Q3或运行package覆盖冻结接口。
