# 2稿图表与代码溯源

未列入压缩包的旧机器文件保留于完整仓库；原始附件由参赛队本地另行提供。

|表|正文任务|结果文件|程序|
|---:|---|---|---|
|1|表1 主要符号与单位|旧公式/来源定义|build_paper.py|
|2|表2 数据用途与限制|旧公式/来源定义|build_paper.py|
|3|表3 22项综合评分的领域结果及五维摘要对照|Q1_TASK_REPAIR_20260925_v1/Q_FULL_DOMAIN_RESULTS_v1.csv|q1_task_repair.py|
|4|表4 配比模型的留出验证及适用边界|P_RESPONSE_VALIDATION_METRICS_v2.json|round4_validate_p_response.py|
|5|表5 A12—A15估算外推压力检验|Q1_TASK_REPAIR_20260925_v1/A12_A15_EXTRAPOLATION_CHECK_v1.csv|q1_task_repair.py|
|6|表6 幂律参数与200次整轨迹重抽样区间|EXP-Q2-ND-R5-20260924-v1/summary.json|round5_fit.py|
|7|表7 三类轨迹验证的宏平均 RMSE|EXP-Q2-ND-R5-20260924-v1/summary.json|round5_fit.py|
|8|表8 质量与跨来源证据的可解释范围|SCEN-Q2-R5-20260924-v3/summary.json|round5_scenarios.py|
|9|表9 题设预算下的基线资源配置|EXP-Q3-BASE-R6-20260924-v1/budget_path.csv|round6_baseline.py|
|10|表10 相同收益假设下的三类质量成本比较|SCEN-Q3-R6-20260924-v1/quality_context_path.csv|round6_scenarios.py|
|11|表11 高可比桥接组的留一规模预测误差|EXP-Q4-R7-20260925-v1/bridge_validation.csv|round7_models.py|
|12|表12 分解的控制规格与敏感性|EXP-Q4-R7-20260925-v1/decomposition_changes.csv + robustness_variants.csv|round7_models.py|
|13|表13 C4训练数据与算力字段的识别范围|Q4_TASK_REPAIR_20260925_v1/summary.json|q4_task_repair.py|
|14|表14 前沿模型的回溯滚动验证|EXP-Q4-R7-20260925-v1/rolling_metrics.csv|round7_forecast.py|
|15|表15 未来能力的条件预测及独立的模型范围|EXP-Q4-R7-20260925-v1/forecast_summary.json|round7_forecast.py|
|16|表16 外生算力增长保留情景下的条件中心|Q4_TASK_REPAIR_20260925_v1/EXOGENOUS_COMPUTE_SLOWDOWN_SCENARIOS_v1.csv|q4_task_repair.py|

|图|结果来源|图文件|
|---:|---|---|
|1|5.1 二十二项综合评分与五维解释性画像|03_models/modeling_phase1/q1/round4/figures/FIG-Q1-R4-001_core_domain_profile.png|
|2|5.3 单纯形约束下的配比响应|03_models/modeling_phase1/q1/round4/figures/FIG-Q1-R4-002_domain_validation_gain.png|
|3|6.2 轨迹验证与跨来源诊断|06_results/figures/round5/FIG-Q2-R5-002.png|
|4|6.3 边际效用 弹性与规模替代|08_paper/revised_v2/figures/FIG4_Q2_TOTAL_LOSS_ELASTICITY_REEXPORT.png|
|5|7.2 解析最优配置与结构转移|08_paper/revised_v2/figures/FIG5_Q3_BUDGET_REEXPORT.png|
|6|7.3 质量成本选择与投入门槛|08_paper/revised_v2/figures/FIG6_Q3_QUALITY_REEXPORT.png|
|7|7.6 影子价格与不确定性|08_paper/revised_v2/figures/FIG7_Q3_UNCERTAINTY_REEXPORT.png|
|8|8.3 参数规模关联与剩余性能分量|06_results/figures/round7/FIG-Q4-R7-002.png|
|9|8.5 日期明确的预测与三类不确定性|06_results/figures/round7/FIG-Q4-R7-005.png|

公式1—24的逐式来源、符号、假设及正文位置见 `FINAL_EQUATION_REGISTRY_v2.json`。
