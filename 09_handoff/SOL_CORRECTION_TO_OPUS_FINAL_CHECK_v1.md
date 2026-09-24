# SOL_CORRECTION_TO_OPUS_FINAL_CHECK_v1

当前状态：P0-1 CLOSED — DESIGN LEVEL / AWAITING EMPIRICAL AUDIT；整体 AWAITING OPUS FINAL CHECK。Round 5 只修复研究设计合同，未执行真实数据审计、模型、实验或论文结果。本包供快速复核，不重新交付整段聊天史。

## 必读四件

1. 02_analysis/consensus/JOINT_F_PROBLEM_SYNTHESIS_v1_1.md，SHA256 DB66F1D8319BAF4ACE91F6648DE1EFA998AF190C6D0541E893BF00E222ABCE12。先看 Changes from v1、§5 P0 决策树和 §15 P1 合同；原 v1 未覆盖。
2. 01_data/IDENTIFIABILITY_AUDIT_SPEC.md，SHA256 301D2CA1619D89A4088C557FD10A314B52883748F4AC00AD4ABD8D5983B3BB90。定义同运行配对、合法 simplex 设计、秩/弱识别/支持/样本外/半合成分支与输出字段。
3. 10_review/P0_CLOSURE_REPORT_v1.md，SHA256 79E52C1C335230AF7E1B725DC08849371436926328ABB6593FEA0284003FB1C0。只关闭“没有输出决策树”的设计缺陷。
4. 10_review/ISSUE_TRACKER.md。列出 1 P0、6 P1、5 P2 的设计修复与待审计状态。

机器路由辅助：04_code/utils/identifiability_decision.py，SHA256 772B618DAFB4686823837F7BF6D1FF62494188F6866CA7A81661748EA95F1B16。14 个**非真实**逻辑摘要已覆盖来源未知、泄漏、无配对 Q、固定 q 别名、秩亏、弱识别、支持不足、无样本外增益、半合成唯一支持等分支；缺少留出指标证据 ID 的积极输出会被拒绝。脚本只消费未来的审计摘要，不计算真实矩阵秩。

## 本轮实际修改

- **P0-1**：Step 0 来源/泄漏 → A 配对独立变化 → B 固定 q 确定性构造 → C 合法设计秩 → D 精度与支持 → E 样本外区分 → F 半合成叠加。每个失败或通过分支输出 Q2_ACTION、Q3_ACTION、允许/禁止措辞及 fallback；无固定 0.05、20 等未校准阈值。真实 Q/p 是否可识别仍 OPEN。
- **P1-1 至 P1-6**：13 域主响应、Strong/Weak/No Bridge、p 现实供给、Q4 规模变量、Q3 非平凡结构转移、Conservative Story 最低完整性均写成使用前预注册/后续审计合同；没有确定具体模型或桥接等级。
- **P2**：生成明确标记 RETROSPECTIVE RECORD / NOT ORIGINAL ROUND-2 ARTIFACT 的 OPUS_TO_SOL_HANDOFF_v1_RETROSPECTIVE.md；统一配比/配方和核心符号于 03_models/shared/NOTATION.md。原始 Round-2 handoff 仍不存在，不能引用回溯件冒充原件。
- **状态修正**：Opus Verify 原稿中的“P0 BLOCKER”优先于“READY FOR DATA AUDIT”。v4 记录临时 HOLD，v5 记录设计级关闭；Opus Final Check 前仍不正式进入 Data Audit 或生成 CONSENSUS。

## 仅需回答六问

1. 决策树是否在所有真实可能路径下给出明确、保守且互斥的主状态，并保留并存的风险 flags？
2. Fallback 是否禁止把 p⊙q、正则化或半合成 Q 变化误称真实独立质量效应？
3. 六项 P1 是否已变成可执行的使用前预注册或 Data Audit 项，且无拍脑袋放行阈值？
4. v1.1 是否仍保持 Q1 评分法、Q2 Scaling Law、Q3 优化形式、Q4 分解和 Strong Bridge 为 OPEN/CANDIDATE？
5. P0-1 能否保持 CLOSED — DESIGN LEVEL / AWAITING EMPIRICAL AUDIT？若不能，请指出最小返工项。
6. 是否具备进入逐项 CONSENSUS 的设计条件？这不等于实际数据质量或模型已通过。

建议输出 02_analysis/cross_review/JOINT_F_PROBLEM_FINAL_CHECK_v1.md。若发现 P0 设计缺口则重开并继续 HOLD；若通过，下一轮才考虑 CONSENSUS。当前请勿启动正式数据审计。
