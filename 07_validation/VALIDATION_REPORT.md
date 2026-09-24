# VALIDATION_REPORT

状态：Q1 Round 4 已完成一次正式 A4/A5 训练和一次有效 A6–A11 留出验证；本地[Round 4 QA](../10_review/MODELING_PHASE1_R4_QA_20260924.md) PASS。Q1 PROVISIONALLY CLOSED，M1 仍为暂定首选；Gate 2 已按 G2-SINGLE-001 / Verdict B 通过限定用途，VALIDATED FINAL RESULT 0。Q2–Q4 正式模型验证尚未启动。

| Question | Model version | Baseline comparison | Error/residual | Sensitivity | Robustness | Uncertainty | Extrapolation | Ablation | Feasibility | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | M1 16D simplex contrast，训练 `EXP-Q1-PRESP-TRAIN-R4-20260924-v1`，有效留出 `VAL-Q1-PRESP-A6A11-R4-20260924-v2` | A7/1M M1 R0 RMSE 0.2278 vs M0 0.2846；13/13 域改善；M2 无稳定额外增益，M3 未触发 | [逐行/逐域结果](../03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_A6_A11_v1.md)与机器 JSON；R0 排序相关约 0.624 | R1/R2 训练定义仅敏感性；R3 逐域强制 | A6/A8 同 p；1M 2 IN/252 NEAR/2 OUT | M1−M0 两层成对 bootstrap 上界 <0；OUT 仅两点，不给远域误差保证 | A9/60M 中心化形状部分转移；A11/1B 失败，禁止通用 p 效应 | M0/M1/M2 冻结比较；M3 未激活 | [经验支持](../03_models/modeling_phase1/q1/round4/P_FEASIBLE_REGION_EVIDENCE_v1.md)不等于现实供给/最终 Q3 域 | CHECKED OUT-OF-SAMPLE CANDIDATE — GATE 2 ACCEPTED FOR PROVISIONAL USE；非 VALIDATED FINAL |

Q1 质量表示另见[规格](../03_models/modeling_phase1/q1/round4/Q1_MODEL_SPEC_v1.md)与[限制](../03_models/modeling_phase1/q1/round4/Q1_LIMITATIONS_v1.md)：Full-22 画像与五维描述并行、语义冲突确认 0、TYPE E=0；该描述不是同运行质量弹性验证。失败验证 v1 的 JSON 序列化异常已隔离，不用于结论。Q2 重视来源内整轨迹留出及外部来源边界；Q3/Q4 仍待后续正式验证，不在 Round 4 范围。

留出角色：A7 未用于结构/超参数搜索或参数回填，但用于冻结候选的预定验收与偏好判定；其成对区间不视为完整选择过程校正的最终泛化区间。
