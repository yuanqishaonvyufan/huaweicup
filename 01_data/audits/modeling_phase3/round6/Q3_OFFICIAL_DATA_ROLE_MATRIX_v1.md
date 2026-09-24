# Q3 official data role matrix v1

OFFICIAL_MAPPING_FIRST：以已排除页边干扰的说明第4/12/13页与题面附录A为准。所有完整路径、逐文件SHA、字段、单位、资格及未决事项见同名JSON。C8/C9/C10只引用既有原件manifest，不开展Q4解析。

| ID | 官方说明 | 实际路径（C_efficiency_evolution/下） | 文件/行 | Q3目标 | Q3约束/敏感性 | 等级/未决 |
|---|---|---|---|---|---|---|
| C1 | 排行榜主表 | leaderboard_cleaned.csv | 1 / 4576 | NO | NO；Q4保留 | OBSERVED / mixed metadata；Cross-source alignment/comparability not reopened in Q3 |
| C2 | 排行榜增强 | leaderboard_enhanced.csv | 1 / 4576 | NO | NO；Q4保留 | OBSERVED / merged metadata；Cross-source alignment/comparability not reopened in Q3 |
| C3 | 排行榜时序 | leaderboard_extended_timeseries.csv | 1 / 4599 | NO | NO；Q4保留 | MIXED；Cross-source alignment/comparability not reopened in Q3 |
| C4 | 全模型元数据 | epoch_all_ai_models.csv | 1 / 3523 | NO | NO；Q4保留 | PROVIDED metadata, some compute ESTIMATED；Cross-source alignment/comparability not reopened in Q3 |
| C5 | Loss–Benchmark 桥接 | loss_benchmark_bridge.csv | 1 / 43 | NO | NO；Q4保留 | MIXED；Cross-source alignment/comparability not reopened in Q3 |
| C6 | 桥接扩展 | loss_benchmark_bridge_expanded.csv | 1 / 75 | NO | NO；Q4保留 | MIXED；Cross-source alignment/comparability not reopened in Q3 |
| C7 | 架构元数据含最大上下文 | model_architecture_metadata.csv | 1 / 45 | NO | 外生长度情景；非实训约束 | PROVIDED architecture metadata；maximum context is not observed training context; no hardware utilization or supply-price curve |
| C8 | 逐任务评测 JSON | detailed_results/ | 1958 / None | NO | NO；Q4保留 | OBSERVED evaluations; out of Q3 scope；Cross-source alignment/comparability not reopened in Q3 |
| C9 | 原始 Leaderboard Parquet | data/ | 1 / None | NO | NO；Q4保留 | OBSERVED; out of Q3 scope；Cross-source alignment/comparability not reopened in Q3 |
| C10 | 评测说明目录 | pythia_*_eval_details/ | 7 / None | NO | NO；Q4保留 | PROVIDED documentation；Cross-source alignment/comparability not reopened in Q3 |
