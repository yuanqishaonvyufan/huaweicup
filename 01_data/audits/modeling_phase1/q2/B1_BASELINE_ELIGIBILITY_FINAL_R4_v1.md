# B1 Baseline Eligibility — Round 4 final decision v1

**四选一裁决：B. ELIGIBLE FOR ATTACHMENT-INTERNAL RESTRICTED BASELINE — ALLOWED FOR ROUND 5 BY G2-SINGLE-001。**[Gate 2 共识 v1](../../../../02_analysis/consensus/GATE2_CONSENSUS_v1.md)已接受受限入口；本状态更新不改变内部审计或外部来源事实。这是比赛附件内部数值建模资格，**不是**经核实的外部 Pythia 原始验证曲线资格；Round 4 没有拟 N–D Scaling Law。判据在[双层资格合同](../../../../03_models/modeling_phase1/q2/B1_TWO_LAYER_ELIGIBILITY_CONTRACT_R4_v1.md)中预先冻结，程序化证据见 [机器记录](B1_INTERNAL_ELIGIBILITY_R4_v1.json)、[八轨迹表](B1_INTERNAL_TRAJECTORY_R4_v1.csv)与[固定 D 跨规模表](B1_CROSS_N_ORDER_R4_v1.csv)。

| 层级 | 判定 | 依据与范围 |
|---|---|---|
| EXTERNAL EMPIRICAL ELIGIBILITY | **NOT ELIGIBLE** | `val_loss` 无 B1 行级原始 run/验证语料/tokenizer/平均规则锚；`precision/wd/lr` 与公开训练说明或配置不对齐。官方 README 链接的两处 W&B 末步 Loss 与 B1 不同，但目标未证相同，不能判断伪造或按真实 Pythia 曲线外推。 |
| ATTACHMENT-INTERNAL MODELING ELIGIBILITY | **B：受限资格** | 官方可见说明明确 B1 是 Q2 主表并定义 `val_loss` 为验证交叉熵；原件哈希和 1,176×15 结构稳定。8×147 N–D 全网格，八条 D 轨迹均无 Loss 反增，147 个固定 D 点的七个相邻 N 比较共 **0** 次 Loss 反增；`D≈steps×2,097,152/10^9` 最大差约 `0.000496` B tokens，`C/(6ND)` 单位校正中位约 1，`ppl` 与 `exp(val_loss)` 最大相对误差低于 0.1%。这些只证明**附件内部口径可计算且一致**，不证明外部真实性。 |

**B 级模型措辞：**“基于竞赛附件 B1 提供的内部 Loss 标尺，研究八条规模轨迹上 N 与 D 对表内 `val_loss` 的条件性/相对关系”。未来参数可用于**附件范围内**的拟合、弹性/边际量及敏感性描述；不能把其数值称为经核实的 EleutherAI 原始训练规律、不能直接运输到其他语料/tokenizer/模型族或与 A 的绝对 Loss 合并，更不能推出独立 Q 弹性。`precision/wd/lr/gpu_days/step_time/grad_norm` 及未经溯源的训练元数据隔离，Round 5 核心只用 `N_params_B,D_tokens_B,val_loss`。

只有八条 N 轨迹可作留出分组单位，其统计独立性仍需假设，1,176 行是相关检查点。Round 5 必须预注册整轨迹留出、D 段外推、误差与条件数、对 B2/B3 插值/半合成及 B4/B5 外部数据的分级解释；不得随机按行切分后声称独立验证。若这些模型检验失败，应降低或撤销 B 级模型用途。

**Alert 关系：**最新权威[Evidence Alert v4](EVIDENCE_ALERT_B1_SOURCE_METADATA_v4.md)继续 `PARTIALLY RESOLVED`，并继承[v3](EVIDENCE_ALERT_B1_SOURCE_METADATA_v3.md)记录的未解原始来源；本次 B 级资格是独立、范围更窄的裁决，不等同把 Alert 升至 `RESOLVED FOR BASELINE USE`。Gate 2 已允许附件内部受限用途；外部经验资格仍未恢复，当前仍无正式 N–D 拟合。
