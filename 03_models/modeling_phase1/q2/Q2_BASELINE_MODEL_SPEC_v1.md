# Q2 B1 attachment-internal N–D baseline specification v1

**状态：ROUND 5 BASELINE MODELING AUTHORIZED — NOT YET FITTED。**[Gate 2 共识 v1](../../../02_analysis/consensus/GATE2_CONSENSUS_v1.md)已允许 B 级附件内受限入口；Round 5 开始计算前须冻结完整训练/验证与选择合同并登记 Run。依据 [Round 4 B1 双层裁决](../../../01_data/audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md)，只研究竞赛附件内部 `N_params_B,D_tokens_B,val_loss`；外部原始 Pythia 验证集/tokenizer 未获核，Alert 仍 `PARTIALLY RESOLVED`。

## 目标与候选

目标是对八条相关规模轨迹拟合**来源内** N–D Loss 曲面。以题面给出的经典可解释候选 `L(N,D)=E+A N^(−α)+B D^(−β)` 为受限基线规格，`N,D` 均按十亿参数/Token 输入，`A,B,α,β≥0`；是否需要共享/分规模偏移、相关误差或其他受限候选，只能在 Round 5 根据训练残差和留组证据另立版本。禁止把 `precision/wd/lr` 等未溯源字段当预测变量或因果调节量。

## 训练与验证门槛

1. 原件 SHA-256 与字段角色再核；按 N 的八条轨迹分组，整个 N 轨迹轮流留出，不能按 1,176 行随机拆分。对 D 早/中/晚段及末尾外推另作难度分层。
2. 对原始 Loss 单位报告轨迹级 MAE/RMSE、残差随 N/D、参数可识别性、约束边界与不确定性。只有八个规模分组，统计独立性仍依赖假设，区间须反映群组数量小与检查点依赖，不能以逐行独立标准误给虚假精度。
3. B2/B3 的半合成/插值性质显式标注，B4/B5 外部 Loss 目标若不共标尺，仅作形状/方向或另行校准测试；不直接合并绝对 Loss。B8 保持隔离，独立 Q 质量弹性不估。
4. 若整轨迹留出或 D 段外推失败，合法结果是 **NO RELIABLE ATTACHMENT-INTERNAL BASELINE** 或仅局部描述；不得因 B 级入口资格而强造有效 Scaling Law。

模型系数若获得后，论文必须写“竞赛附件 B1 内部 Loss 标尺的条件参数”，并并列披露 `val_loss` 来源未核、公开 W&B 候选值不一致但目标未证明同一、八组独立性限制及可运输性未知。Round 4 **没有运行本规格**；Gate 2 已允许 Round 5 受限启动；本轮裁决不执行拟合。
