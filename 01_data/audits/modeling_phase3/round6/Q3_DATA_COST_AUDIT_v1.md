# Q3 targeted data/cost audit v1

CP0 RECOVERED — NO RE-RUN；f253450b31dccfe6670e719836840acbe909010c。本轮从该干净提交恢复，现有源哈希与C系列mapping沿用；仅定向读题面B.2，确认没有独立领域成本。近白色干扰继续排除。无Q4解析。

| 输入 | 等级 | 值/用途 | 限制 |
|---|---|---|---|
| C_train | PROBLEM-PROVIDED | 6ND | N/D按原始个数；转十亿时乘1e18 |
| C_attn | PROBLEM-PROVIDED | eta ND L，eta=.0002 | 简化算力代理，不是真实账单 |
| C_quality | PROBLEM-PROVIDED | D[g(q)-g(q0)]+；三曲线参数见cost spec | 原参数不重标，非实测投入产出 |
| C_mix | UNKNOWN | 无独立给定项；固定p时不新增项 | 不暗造实际零价格 |
| 预算 | PROBLEM-PROVIDED / SCENARIO | 1e19/1e22/1e24；51点log网格细化 | FLOPs，不是美元 |
| N/D上下界 | ATTACHMENT-EMPIRICAL | Q2范围 | 统计支持不是供应实测 |
| L档位 | ATTACHMENT-EMPIRICAL | C7 2048/4096/8192/32768/131072 | architecture max，不是训练长度 |
| reference L=2048 | SCENARIO | 参考Pythia架构档位 | 不声称实训 |
| L临界 | DETERMINISTIC DERIVED | 6/eta=30000 | 两代理相等，不是经验阈值 |
| q0=.5、qcap=1/.75 | SCENARIO | 刻度与上限 | 无DQ0映射；.75仅压力情景 |
| h/g运输 | SCENARIO | 0/.5/1/1.5×B7 g | 不能作真实质量弹性 |
| p统计支持 | ATTACHMENT-EMPIRICAL / DETERMINISTIC DERIVED | Q1凸包内513有限候选 | 不保证实际供应 |
| 现实供应/领域价格 | UNKNOWN | 不补造 | dmax比例压力明确SCENARIO |

核验：G3允许的冻结参数/接口已读，CP0 cost metrics与可见题面一致。四问官方需求以题面为准；不把上阶段“缺现实美元价格”作为无法使用题面算力代理的阻断。Q3主问题先quality OFF/mix OFF；质量与配比情景分开，B8始终不进入。
