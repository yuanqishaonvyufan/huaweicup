# Q1 model specification v1 — provisional final candidate

**状态：Q1 PROVISIONALLY CLOSED；M1 PROVISIONAL PREFERRED Q1 p-RESPONSE MODEL。**[Gate 2 共识](../../../../02_analysis/consensus/GATE2_CONSENSUS_v1.md)已按 Verdict B 接受限定用途；无 ACTIVE FINAL MODEL 晋升。该模型是两条并行、证据等级不同的输出链，不伪造同运行 Q–Loss 连接。A1–A3 质量画像与 A4/A5 的 p 响应来自不同观察粒度；`NO_MATCHED_Q`、TYPE E=0、A/B Loss 分源继续有效。

## Track A：全 22 项质量画像与多维描述

主输出为[全 22 项两层表示](../Q1_QUALITY_REPRESENTATION_FINAL_CANDIDATE_v1.md)：Layer 1 保留全部指标的来源角色、方向/单位限制、缺失、统计分歧、冗余及域别分布；Layer 2 只用五项语义有依据的 CORE 信号，对 A1 固定训练参考作经验分位，得到文档向量 `u_i∈[0,1]^5`。域级输出是五维分布/均值/中位数与非重叠扩展对照，机器表见[核心域画像](Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv)和 [Full-22 域画像](Q1_FULL22_DOMAIN_PROFILE_v1.csv)。DQ0 `5^-1∑u_ij` 是随附的 **DESCRIPTIVE SUMMARY BASELINE**，必须与五维剖面并列；DQ1/DQ2/DQ3 分别仅为共变、分组和域归一化敏感性。确认的语义冲突数为 0；统计分歧、域别反转、重复证据和长度/尺度伪象分开写，不合成虚构冲突指数。

## Track B：17 域配比到 13 域 Loss

正式首选**候选**是 M1：对每行 17 域配比 `p` 只做总和舍入校正，保留真实零值；令 `H∈R^(17×16)` 是固定正交 Helmert 基，`Hᵀ1=0`，`z=(p−p̄_A4)H`。对每个验证域 `m=1,…,13`，拟合 `L_m(p)=a_m+zᵀβ_m+ε_m`；预测的主报告响应按已冻结 P1-1 取 `R0(p)=13^-1∑_m L_m(p)`，并**始终**报告 R3 十三维预测/误差。该坐标是零值安全的 Euclidean simplex contrast，**不是**声称无需处理零值的 Aitchison ILR；不把 17 原始 p 与截距一起回归。M0 各域训练均值作为对照；M2 ridge 在训练条件数 45.44 下进入比较但未显示稳定 A7 收益；M3 未触发训练残差升级门槛。

训练只用 A4/A5 512 组同 `index` 运行，模型与超参数在接触 A6–A11 Loss 前冻结；[正式训练](P_RESPONSE_TRAIN_METRICS_v1.json)与[留出验证 v2](P_RESPONSE_VALIDATION_METRICS_v2.json)有输入/代码哈希。A7 的 1M 同尺度检验支持 M1：R0 RMSE 从 M0 的 0.2846 降至 0.2278，13 域各自误差均改善；A9 60M 只支持部分**中心化配比形状**，A11 1B 形状转移失败。模型只在附件 A 的 1M/相邻训练 p 支持范围具相对预测证据，不能据此宣称跨规模统一、full-simplex 可实施最优或质量 Q 的独立系数。

本规格的结果、验证与限制分别见 [Q1_RESULTS_REPORT_v1](Q1_RESULTS_REPORT_v1.md)、[Q1_VALIDATION_REPORT_v1](Q1_VALIDATION_REPORT_v1.md)、[Q1_LIMITATIONS_v1](Q1_LIMITATIONS_v1.md)；论文图表仅引用登记的数据源。Gate 2 已接受暂定关闭和受限下游用途，`ACTIVE FINAL MODEL` 仍未授予。A7 用于冻结候选的预定验收与偏好判定；未用它搜索结构、选择超参数或回填模型。
