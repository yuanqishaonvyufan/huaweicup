# Gate 2 → Round 5 handoff v1

**授权来源：[GATE2_CONSENSUS_v1](../02_analysis/consensus/GATE2_CONSENSUS_v1.md)，G2-SINGLE-001，ACTIVE。**Gate 2 Verdict B：PASS WITH DOCUMENT-ONLY CORRECTIONS；文档修正已完成。Q1 PROVISIONALLY CLOSED；Round 4 COMPLETE / QA PASS；Round 5 READY TO START，但本交接生成时 N–D 拟合仍为 0。Q2 BASELINE MODELING AUTHORIZED；Q3/Q4 NOT STARTED。

## 1. Q1 传入 Q2

沿用[接口 v1.1](../02_analysis/consensus/Q1_TO_Q2_INTERFACE_v1_1.md)：TYPE A 为 Full-22/五核心多维描述、DQ0 摘要；TYPE B 为 M1 的 1M 领域/配比关联与 R0+R3、跨规模限制；TYPE C 为条件质量情景；TYPE D 为支持与外推约束；TYPE E 为 **0 independently estimable quality variables**。M1 是 PROVISIONAL PREFERRED Q1 p-RESPONSE MODEL，无 ACTIVE FINAL MODEL 晋升。

A7/1M M1 R0 RMSE 0.2278 vs M0 0.2846，13/13 域改善；M2 无稳定额外留出收益，M3 未触发。训练结构和超参数只由 A4/A5 确定；A7 参与冻结候选的预定比较与偏好判定，不再称完全未参与选模的最终测试。训练/验证原 Run 和失败隔离状态不变。

## 2. B1 受限 baseline 边界

[双层资格](../01_data/audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md)的附件内部 **B 级入口已获 Gate 2 许可**。核心变量只用 `N_params_B,D_tokens_B,val_loss`。目标是“竞赛附件 B1 内部 Loss 标尺上的条件/相对 N–D 关系”；[Alert v4](../01_data/audits/modeling_phase1/q2/EVIDENCE_ALERT_B1_SOURCE_METADATA_v4.md)继续 PARTIALLY RESOLVED，外部原始 run/验证语料/tokenizer/损失抽取锚未恢复。

下一轮从[已有 Q2 规格](../03_models/modeling_phase1/q2/Q2_BASELINE_MODEL_SPEC_v1.md)出发，先固定模型/约束/单位、训练与检验切分、选择规则、失败条件并登记新 Experiment ID。按八条 N 轨迹分组留出，另查 D 段外推、残差、参数可识别性和不确定性；1,176 个相关检查点不作独立样本。分组数只有八个且其统计独立性未获外部证据证明，区间须明示假设。B2/B3 插值/半合成与 B4/B5 外部来源按证据等级解释。若检验失败，允许 NO RELIABLE ATTACHMENT-INTERNAL BASELINE 或局部描述，不因入口授权而预定成功。

## 3. TYPE E = 0

没有同运行质量干预或新的识别证据，不引入或估计独立 quality coefficient。DQ0、五核心分位与 DSIR 只作描述/情景；不可把 B6/B7 半合成斜率改写为真实质量弹性。A/B 绝对 Loss 不池化。

## 4. scale-dependent mixture effect 是候选问题

60M 仅部分中心化形状转移，1B 为 transfer failure。现有结果提示配比响应不具规模不变性，但没有建立配比×规模交互模型；不能将 M1 系数直接作为 B1 的 p 修正项。后续扩展若需要，应另立规格和独立检验，保留当前 1B 失败。

## 5. support-aware constraints

1M 的训练观测凸包覆盖 2/256；分类 2 IN、252 NEAR、2 OUT；A6/A8 同 p。主要证据来自局部近邻外推。Q3 将来必须把经验支持、域外不确定性与实际供给成本分开建约束；禁止 full-simplex deployable optimum 宣称。训练 q95/q99 不是自动成立的现实可行边界。

## 6. B8

维持 GENERATOR UNKNOWN / QUARANTINED / SEARCH PAUSED，不入主参数；无新机制证据不重启搜索，不阻塞 B1 受限主线。

## 7. Round 5 禁止事项

- 不重新打开 Q1 全流程，不重训 M0/M1/M2 或重跑 A6–A11，也不启用未触发的 M3。
- 不把 B1 表内参数说成经核实的真实 Pythia 普适规律；不使用隔离元数据估因果调节项。
- 不随机按检查点行划分后声称独立验证；不在看检验结果后重写已冻结选择规则。
- 不池化 A/B 绝对 Loss，不虚构 TYPE E 变量，不向 1B/全 simplex 无条件运输 M1。
- 不以 Gate 2 通过代替 Q2 baseline 拟合与检验，不自动宣布 ACTIVE FINAL MODEL 或 VALIDATED FINAL RESULT。
- 本次只完成 Gate 2 与交接；实际 Round 5 计算由下一轮按上述授权开始。
