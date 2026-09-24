# PROBLEM_MAP

以下仅是题面明确要求的依赖骨架，不预设最终数学模型、估计方法或求解算法。细节以 original/F_2026_problem_user_supplied.docx 内嵌公式为准。

| 问题 | 输入 | 题面要求的输出 | 传给下一问 |
|---|---|---|---|
| Q1 | A1–A3 质量信号；A4–A15 配比与 Loss；A16 参考映射 | 质量 Q、指标冲突及消解、17 域配比 P 与 Loss 关系、检验和外推讨论 | Q 与 P 的定义、尺度、配比效应及可靠性 |
| Q2 | Q1 输出；B1–B12 按指定角色分层使用 | 含 N、D、Q、P 的广义 Loss 关系、参数、边际效用、弹性、替代/互补、验证 | 经检验的损失关系、参数和适用范围 |
| Q3 | Q1/Q2 输出；附录 B 成本方案；C7 上下文长度可行值 | 预算约束下配置、成本形式比较、结构性转移、解析临界值、敏感性 | 资源配置情景与规模效应解释 |
| Q4 | C1/C2、C3、C4、C8 及 C5/C6 桥接；前三问结果 | 规模与非规模技术贡献、综合 Benchmark 能力、Loss–Benchmark 映射、12/24 个月前沿及不确定性 | 最终结论与现实解释 |

每问统一接口字段：INPUT、OUTPUT、DECISION VARIABLES、PARAMETERS、ASSUMPTIONS、BASELINE、CANDIDATE MODEL、FINAL MODEL、VALIDATION、OUTPUT TO NEXT QUESTION。初始化时 BASELINE/CANDIDATE/FINAL 仍为 OPEN。

Q1 → Q2 → Q3 → Q4。另有 Q1 → Q3 的质量/配比输入，以及 Q2 → Q4 的 Loss 解释与 Q3 → Q4 的资源情景联系；后两条是否用于最终模型，须在联合分析与证据核验后判定。
