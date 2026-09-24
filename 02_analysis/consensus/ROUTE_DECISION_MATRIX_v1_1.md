# Route Decision Matrix v1.1 — Gate 1 convergence draft

状态：**CONFIRMED ROUTE DECISIONS UNDER [ACTIVE GATE 1](GATE1_CONSENSUS_v1.md)**。保留 Round A 的 RD-01–RD-19 全部 ID。Opus 的 16 KEEP / 2 MODIFY / 1 DEFER 按其主题意见映射到 RD 行：MODIFY-2→RD-11，DEFER-1→RD-15，MODIFY-1→RD-17；RD-18 原本就是限族 Weak 的 CONDITIONAL 候选，更新边界而不另计一次 MODIFY。`Final converged decision` 与 `Current status` 只使用用户允许的八种状态；“Final”意为Gate 1 已确认路线状态，**不是最终数学模型**。证据见 [Phase 1 v2](../../01_data/audits/phase1/ROUTE_DECISION_AUDIT_PHASE1.md)、[桥接定向核查](../../01_data/audits/phase1/bridge_pythia_focus_check.json)和[Opus 引用更正](../../10_review/GATE1_ROUND_B_EVIDENCE_ERRATA.md)。

| Route ID | Question / candidate route | Sol v1 decision | Opus decision | Final converged decision | Change from v1 | Evidence | Reason | Current status | Next gate |
|---|---|---|---|---|---|---|---|---|---|
| RD-01 | Q1 A1–A3 质量描述/冲突 | KEEP AS BASELINE | KEEP | KEEP AS BASELINE | 保持；注明 A1 与扩展 ID 重叠 | A1/A2/A3 为 51,230/17,523/203,752，22 键一致 | 必用且可溯源，样本并非独立重复 | KEEP AS BASELINE | Q1 九维审计、Gate 2 |
| RD-02 | Q1→Q2 独立 Q 弹性主线 | DOWNGRADE | KEEP | DOWNGRADE | 保持；只限当前 A 证据 | `NO_MATCHED_Q` | 当前无同运行 Q，不代表全题永远无质量效应 | DOWNGRADE | 新真实配对后重审 Gate 1/3 |
| RD-03 | Q1 由现有 A4/A5 直接估 γ_Q | REJECT | KEEP | REJECT | 保持 | A4/A5 512 p/Loss、Q_full 未构造 | 缺待估的 Q 列 | REJECT | 新数据另立路线 |
| RD-04 | Q1 零值安全 simplex 对比 | KEEP AS BASELINE | KEEP | KEEP AS BASELINE | 保持 | 17 比例、45.1% 零格、合法 p 基线秩 17 | 零值与闭合需要合法坐标 | KEEP AS BASELINE | Gate 2 零值/留出 |
| RD-05 | Q1 R0 等权 Loss + R3 逐域 | KEEP AS BASELINE | KEEP | KEEP AS BASELINE | 明确只冻结比较规则，R0 不是最终赢家 | PC1 22.8%，24/78 负相关；P1-1 v1.1 | 透明 baseline 与异质性必须并行 | KEEP AS BASELINE | P1-1 比较、Gate 2 |
| RD-06 | Q1 PCA 单因子作唯一主响应 | DOWNGRADE | KEEP | DOWNGRADE | 保持 | PC1 22.8%，领域关系混合 | 不足以代表全部 13 域 | DOWNGRADE | 训练稳定性/用途证据 |
| RD-07 | Q1 多响应/多目标 | CONDITIONAL | KEEP | CONDITIONAL | 保持 | 13 域异质性 | 冲突主导时作为更强主叙事 | CONDITIONAL | Gate 2 域别误差 |
| RD-08 | Q2 B1 N–D baseline | KEEP AS BASELINE | KEEP | KEEP AS BASELINE | 收紧为来源内候选，不能称已稳健估计 | 1,176 行=8 轨迹×147 检查点，简约设计秩 3 | 独立簇少，需整轨迹留出 | KEEP AS BASELINE | Gate 3 分组/族外验证 |
| RD-09 | Q2 A/B 绝对 Loss 直接联合拟合 | REJECT | KEEP | REJECT | 保持 | 无同验证语料/tokenizer 锚 | 名称相同不等于标尺相同 | REJECT | 可核共同锚后新版本 |
| RD-10 | Q2 相对变化与两阶段桥梁 | CONDITIONAL | KEEP | CONDITIONAL | 相对变化是探针；two-stage 须另等运输证据 | A p 与 B N–D 分源 | 标准化不自动消除来源差异 | CONDITIONAL | Gate 2/3 与锚定 |
| RD-11 | Q2 B6/B7 质量条件情景 | CONDITIONAL | MODIFY | CONDITIONAL | 加“生成/校准机制不透明，可能预置 Q 效应” | B6 360 完嵌 B7 450，E3；B7 生成器缺 | 仅是给定半合成机制下的条件关联，不能估真实普适 γ_Q | CONDITIONAL | 生成假设/参数/组成敏感性、Gate 3 |
| RD-12 | Q2 B8 主质量参数 | QUARANTINE | KEEP | QUARANTINE | 保持；calibrated/extrapolated 分查 | 150 组 Q 斜率全反，224 重叠点冲突 | 机制未知，不当错误先验 | QUARANTINE | DA-01 调查 |
| RD-13 | Q2 高维 Q×p×N 交互 | REJECT | KEEP | REJECT | 保持 | 无同粒度联合设计 | 参数数目不能制造识别 | REJECT | 新联合设计+留出 |
| RD-14 | Q3 外生 L_ctx 敏感性 | CONDITIONAL | KEEP | CONDITIONAL | 保持 | C7 12/45 架构上限达 30k，无实训长度 | 仅架构情景参照 | CONDITIONAL | Q3 成本/长度证据 |
| RD-15 | Q3 有限观测配比作最终可行域 | KEEP AS BASELINE | DEFER | DEFER | DEFER-1：所有具体可行域选择推迟；有限集只是候选 | A4 512；A6/A10 大量在训练凸包外 | Q1 拟合/留出误差与供给未给最终域 | DEFER | Gate 2 配比验证、P1-3 |
| RD-16 | Q3 完整 simplex 为现实最优 | REJECT | KEEP | REJECT | 保持 | 经验支持/现实供给不足 | 理论解不可直接称可实施 | REJECT | 新供给与可靠外推另立版本 |
| RD-17 | Q4 Strong Loss–Benchmark Bridge | DOWNGRADE | MODIFY | DOWNGRADE | 当前上层状态改为限 Pythia Weak 待验证；Strong 仍不放行 | 7 High 同族同 D，B1 Loss 末点完全对齐，尚无留出 | 高可比点存在但运输/校准不足 | DOWNGRADE | Gate 4 留出、误差/区间 |
| RD-18 | Q4 限族 Weak Bridge 候选 | CONDITIONAL | KEEP | CONDITIONAL | 明示 `WEAK BRIDGE — PYTHIA-CONFINED, PENDING VALIDATION`，非已验证映射 | 7 High；综合相关弱且任务方向混合 | 只准限族探索，不给全模型能力点预测 | CONDITIONAL | Gate 4 留族/时间与残差 |
| RD-19 | Q4 无可靠桥接时独立能力分析 | FALLBACK | KEEP | FALLBACK | 改为后续验证失败时触发 | C1/C3/C4/C8 可审计，强桥接未建 | Q4 可独立完成并披露映射缺口 | FALLBACK | Gate 4 FAIL/CONDITIONAL |
