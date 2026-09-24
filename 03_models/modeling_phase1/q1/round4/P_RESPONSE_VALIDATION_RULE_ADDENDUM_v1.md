# Q1 p 响应验证前逐域警戒补充 v1

**FROZEN AFTER A4/A5 TRAINING, BEFORE A6–A11 LOSS READ。**训练合同 [P_RESPONSE_PREFIT_CONTRACT_v1](P_RESPONSE_PREFIT_CONTRACT_v1.md)及其模型/超参数已哈希冻结，本补充不改变 M0–M3 结构、M2 α、M3 未触发的决定或训练结果。此处仅把合同中的“明显逐域灾难性劣化”操作化。

在 A7 的 1M 同尺度正式验证中，相对更简单候选（M1 对 M0、M2 对 M1、若启用 M3 则对 M2），如**任一 13 域 RMSE > 1.5 × 对照域 RMSE**，标记 `CATASTROPHIC_DOMAIN_DEGRADATION`，不得仅因 R0/平均域改善而升为无条件 preferred。1.5 是本轮验证前冻结的内部警戒线，不是官方任务阈值、显著性界或现实可实施要求。无论是否触发，全部 13 域的误差增减和 bootstrap 区间都须报告。

支持域内与域外分别评价；若只有 IN/NEAR_SUPPORT 表现可靠，preferred 候选必须明示其经验适用范围，不能推广到 full simplex。A9/A11 的跨规模比较只检查中心化配比效应和排序，不能使用未知规模偏移来宣称绝对 Loss 预测成功。
