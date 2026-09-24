# JOINT_CONTEXT

## Current authoritative state — 2026-09-24

DISCOVERY COMPLETE；Gate1 ACTIVE / CONDITIONAL PASS。Gate2 ACTIVE / PASS WITH DOCUMENT-ONLY CORRECTIONS（G2-SINGLE-001）。Q1 PROVISIONALLY CLOSED，M1暂定首选；Q1不重训不重验。MODELING PHASE 2 ROUND 5：COMPUTATION AND Q2 CANDIDATE PACKAGE COMPLETE，NUMERICAL QA PASS，单图视觉检查通过。Gate3：PRE-REVIEW READY / NOT PASSED。Q2：ATTACHMENT-INTERNAL RESTRICTED CANDIDATE，待Gate3用途裁决；Q3/Q4 NOT STARTED。

## Q2 actual results

EXP-Q2-ND-R5-20260924-v1：B1五参数 E=1.68979756、A=0.35398032、B=1.24030558、alpha=0.33997658、beta=0.27987813。N/D单位均十亿；外部来源未恢复。LONO/forward/2D blocked宏平均RMSE=0.000146888/0.000111642/0.000114134；18个切分、200次整轨迹bootstrap，升级未触发。非常窄的区间只反映附件内部数值稳定性，不是外部预测保证。

SCEN-Q2-R5-20260924-v3：有效情景与分源诊断。B7共同Q斜率=-0.361995，45/45单元负；规模调节只支持生成表内形状。TYPE E=0，真实Q系数仍未识别。A/B绝对Loss不池化，M1不移植B1；1B配比转移失败保持。B8 QUARANTINED / SEARCH PAUSED / UNREAD。

情景v1因NumPy布尔序列化失败、v2因B10无多行族的空中位数失败，均隔离；只有v3有效。B9四个D=0元数据被标无效不插补。B1主运行一次成功，无模型规格/验证阈值事后改写。

## Deliverables and evidence

- 03_models/modeling_phase2/round5/Q2_ROUND5_SPEC_v1.md：拟合前冻结；R5-SPEC-001。
- 03_models/modeling_phase2/round5/Q2_RESULTS_REPORT_v1.md：完整结果/推导；Q2_LIMITATIONS_v1.md、Q2_COVERAGE_MATRIX_v1.md、Q2_TO_Q3_INTERFACE_v1.json。
- 08_paper/sections/Q2_ROUND5_PAPER_CANDIDATE_v1.md：中文论文候选；4张PNG/PDF、5张表。
- 07_validation/round5/Q2_VALIDATION_REPORT_v1.md；10_review/MODELING_PHASE2_R5_NUMERICAL_QA_20260924.json；10_review/GATE3_PRE_REVIEW_PACKAGE_v1.md。
- 全部新增结果CHECKED/CANDIDATE或SCENARIO-CONDITIONAL；Q1–Q4 ACTIVE FINAL MODEL=NONE，VALIDATED FINAL RESULTS=NONE。Gate3不得自动PASS。

## Git and recovery

本轮从GitHub main 052ba706464fa9a1d092ba1f8d01d50a328b61c8恢复；旧本地28个差异文件完整备份于D:/work document/codex_work/F2026_Round5/recovery_052ba706/。用户已明确授权本轮成果上传GitHub。当前新增正式工作应随Round5提交推送；实际提交SHA以git HEAD/origin/main为准，避免在提交内自引用SHA。

下一步：阅读NEXT_ACTION及Gate3预审包，只做Gate3裁决或必要局部整改；不重复Round5、不重开Q1、不重启B1/B8来源搜索。Q3必须等下一阶段明确启动。

用户本轮授权Lead研究者直接推进；没有独立Opus审查，不冒称双方新共识。历史Gate1/2共识保留原范围。
