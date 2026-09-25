# Q4 C1–C10 role matrix v1

ACTIVE / CHECKED. OFFICIAL_MAPPING_FIRST; visible PDF pp.4,5,12,13 and official Q4 appendix. Full file hashes, fields and all requested role attributes are in the adjacent JSON; C8 individual hashes are included. Raw files unchanged.

| ID | Official description | Actual path under C_efficiency_evolution | Files / rows | Time | Q4 role |
|---|---|---|---|---|---|
| C1 | 排行榜主表 | leaderboard_cleaned.csv | 1 / 4576 | Submission Date | primary snapshot, submission cohorts |
| C2 | 排行榜增强 | leaderboard_enhanced.csv | 1 / 4576 | Submission Date; Epoch_AI_Publication_Date | same snapshot + release-date sensitivity |
| C3 | 排行榜时序 | leaderboard_extended_timeseries.csv | 1 / 4599 | Year (mixed) | mixed-time comparability audit; historical rows excluded from primary |
| C4 | 全模型元数据 | epoch_all_ai_models.csv | 1 / 3523 | Publication date; Last modified | macro compute/data/open-weight audit; conservative exact metadata matching |
| C5 | Loss–Benchmark 桥接 | loss_benchmark_bridge.csv | 1 / 43 | absent | bridge subset cross-check |
| C6 | 桥接扩展 | loss_benchmark_bridge_expanded.csv | 1 / 75 | absent | primary stratified bridge |
| C7 | 架构元数据含最大上下文 | model_architecture_metadata.csv | 1 / 45 | absent | architecture context only; TB is not training tokens |
| C8 | 逐任务评测 JSON | detailed_results/0-hero_Matter-0.2-7B-DPO/results_2024-08-07T13-21-02.903091.json | 1958 / 1958 | evaluation filename timestamp | mandatory task aggregation and evaluation-date sensitivity |
| C9 | 原始 Leaderboard Parquet | data/train-00000-of-00001.parquet | 1 / 4576 | absent | equivalent snapshot audit, no double counting |
| C10 | 评测说明目录 | pythia_1.4b_eval_details/README.md | 7 / 7 | absent | documentation only |
