# P-response A6–A11 validation run v1 — FAILED

**Run ID:** `VAL-Q1-PRESP-A6A11-R4-20260924-v1`。**Status: FAILED / NO VALIDATION DECISION。**冻结训练包未改变，脚本原始 SHA-256 为 `7e0b29dd6280518e3193ea3cd91f4a7a8c3927ab41252bd90a686b2520d6cba9`。

脚本在计算、生成 5 个 CSV 之后，向 `P_RESPONSE_VALIDATION_METRICS_v1.json` 序列化机器摘要时因 NumPy `int64` 不可直接 JSON 编码而退出（`TypeError: Object of type int64 is not JSON serializable`）。完整机器结果和 QA 未形成，因此该次运行的数值**不得**用于候选选择、Gate 2 或论文。五个 CSV 已移至 `failed_validation_v1/` 单独保留，未覆盖冻结的训练模型或原始附件。

修复仅限将机器摘要的计数转换为 Python `int`，并以新 Run ID、独立 v2 输出文件重跑。比较合同、训练 bundle、M0/M1/M2 参数、M3 未触发状态和 A6–A11 数据均不因该异常修改。
