# B1 Baseline Eligibility Audit v3 — Round 3 `val_loss` trace

**Verdict: NOT YET ELIGIBLE。Evidence Alert: PARTIALLY RESOLVED。**继承 [v1 几何审计](B1_BASELINE_ELIGIBILITY_AUDIT_v1.md)及 [v2 结构溯源](B1_BASELINE_ELIGIBILITY_AUDIT_v2.md)，本版只重审关键 `val_loss` 来源，**没有正式 N–D 参数估计**。

已核 8×147 N–D 完整网格、D/计算量算术、147 个候选 Pythia 检查点标签；Round 3 [有界主来源检索](B1_PROVENANCE_TRACE_v2.md)仍未取得 B1 行级运行与统一验证设置锚。两个官方 README 链接 W&B run 的末步 `validation/lm_loss` 与 B1 相应末行数值不同，但来源/评估目标未证明相同，故不作虚假数据断言。

正式来源内 baseline 的当前阻断项：模型/变体与八条轨迹的真实连接、`val_loss` 原始运行或文档化转换、共同验证语料/tokenizer/单位/平均规则。元数据 `precision/wd/lr` 可在未来标为附加或未知并从基线排除，但不能把关键 Loss 来源也这样绕过。当前停止低收益检索，保留后续获取赛事生成记录/作者日志或另立附件内受限基线证据审查的可能；这两条均不在本轮执行正式拟合。
