# B8 生成器定向追踪 v1

**状态：GENERATOR UNKNOWN / B8 QUARANTINED。**本轮是对 [Round 1 机制调查](B8_MECHANISM_INVESTIGATION_v1.md) 的小范围来源追踪，没有重跑 B6/B7/B8 数值审计、没有拟合质量参数。

在项目 `04_code/` 与 B 组原始附件的文件清单中，未找到 B8 生成脚本、校准配置、随机种子或说明 0.5 边界的公式。`source_manifest.json` 只为 B6 记载“Pythia training log + RegMix quality signals”的半合成来源；B7/B8 未附生成过程。对 `supplementary_NQ_experiment_large.csv`、`supplementary_NQ_experiment_expanded.csv` 和 `Q_score/data_type/calibrated/extrapolated` 的公开精准搜索没有命中可核的原始生成器。公开 [RegMix](https://github.com/sail-sg/regmix)与 [Pythia](https://github.com/EleutherAI/pythia) 仓库介绍各自原始研究，不能据此认定比赛 B8 的构造方法。

因此 Round 1 的 **LIKELY SYNTHETIC RULE EFFECT** 仍仅是统计模式推断；`Q_score` 与 `val_loss` 的共同定义、校准参数、`calibrated/extrapolated` 机制和精确 0.5 边界均 `UNKNOWN`。B8 不翻转 Q、不删除、不估主参数，也不阻塞 Q1 或 B1。若后续取得生成器，须先锁版本/输入/seed，逐格复现原始哈希对应的 CSV，再单独讨论 alternative-regime stress test。
