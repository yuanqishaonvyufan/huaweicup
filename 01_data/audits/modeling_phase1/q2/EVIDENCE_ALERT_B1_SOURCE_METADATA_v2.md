# EVIDENCE ALERT — B1 source metadata v2

**Status: PARTIALLY RESOLVED — formal B1 baseline PAUSED.** 继承 [v1 OPEN Alert](EVIDENCE_ALERT_B1_SOURCE_METADATA_v1.md) 的事实、原件哈希和禁止拟合边界；本版增加三档处置状态，**不撤销**原警报。

Round 2 已核 B1 的 147 个 step 对应公开 Pythia 154 个发布检查点去掉最早七个，本地辅助索引的三处 commit 与公开模型 API 一致。但 B1 不含可识别的原始 run/模型变体、验证集、tokenizer 或 `val_loss` 抽取方式。`precision` 仍在每条轨迹内切换，`wd` 与 `lr` 也未获字段口径解释。详情见 [来源追踪](B1_PROVENANCE_TRACE_v1.md)和 [资格重审 v2](B1_BASELINE_ELIGIBILITY_AUDIT_v2.md)。

只在 `RESOLVED FOR BASELINE USE` 时允许启动正式来源内 N–D baseline；`OPEN` 或 `PARTIALLY RESOLVED` 均禁止。达到第三档须有可复核的 Loss 来源、验证语料/tokenizer、模型与检查点/轨迹对齐；与基线无关且来源不明的 metadata 可隔离，但不得假装已核。当前仍为 `NOT YET ELIGIBLE`，不推断 Loss 伪造。
