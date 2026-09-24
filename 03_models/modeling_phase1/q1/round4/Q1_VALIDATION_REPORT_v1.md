# Q1 validation report v1

**总体：1M 同尺度正式留出验证支持 M1；60M 相对形状部分支持；1B 迁移失败。Gate 2 已按 G2-SINGLE-001 / Verdict B 接受 Q1 暂定关闭。**A4/A5 的 512 组训练与 M0/M1/M2 参数、条件升级、超参数均在读 A6–A11 Loss 前冻结；M3 未激活。首次验证 v1 因 JSON 序列化异常未过 QA、产物隔离；有效机器运行是 `VAL-Q1-PRESP-A6A11-R4-20260924-v2`，参数包未改。脚本与逐行证据见 [validation JSON](P_RESPONSE_VALIDATION_METRICS_v2.json)及[预测 CSV](P_RESPONSE_VALIDATION_PREDICTIONS_v2.csv)。

| 检验 | 结果 | 判定 |
|---|---|---|
| A7/1M 绝对 Loss | R0 M1 RMSE 0.2278 < M0 0.2846；13/13 域 RMSE 下降，成对 bootstrap R0/逐域 MSE 差的 97.5% 上界均 <0 | **PASS within A4/A6 near-support context** |
| A9/60M 配比形状 | 中心化 R0/逐域 RMSE 比 M0 为 0.888/0.677；R0 秩相关 0.558 | **PARTIAL TRANSFER**；不称绝对 Loss 预测通过 |
| A11/1B 配比形状 | 中心化 R0/逐域 RMSE 比 M0 为 3.108/1.967；R0 秩相关 0.368 | **FAIL**；不得向 1B 运输 M1 p 效果 |
| 领域异质性 | A7 13 域均改善，但相对 M0 RMSE 比为 0.460–0.754；R3 逐域报告保留 | **CHECKED**；不简化为单一聚合结果 |
| 支持域 | A6/A8 同一 p；1M 2 IN/252 NEAR/2 OUT；1B 15 IN/46 NEAR/3 OUT | 经验支持不等于现实可实施域；小 OUT 组不足以证明远外推安全 |

使用 A5 训练均值/标准差投影的 R1 和 R2 仅为预注册敏感性，不能替换 R0+R3；未使用 A12–A15 外推 Loss 作真实验证。详细 domain/support 误差与不确定性见[正式验证](P_RESPONSE_VALIDATION_A6_A11_v1.md)和[支持域](P_FEASIBLE_REGION_EVIDENCE_v1.md)。论文应把 1B 失败作为主要局限，不能只摘要 1M PASS。

**Gate 2 文档澄清（G2-DOC-01）：**A7 是拟合外留出验证，同时用于冻结合同预先规定的候选验收与偏好判定。结构、超参数和参数未由 A7 回填，因此不能将其概括为“holdout 完全未参与选模”，也不能当作偏好判定后仍未使用的独立最终测试。原成对 bootstrap 区间针对既定比较，不是完整模型选择过程校正的泛化区间。数值、模型与验证合同均未修改，无重跑要求。
