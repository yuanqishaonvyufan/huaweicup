# Q3 baseline optimization v1

CP2 actual Run EXP-Q3-BASE-R6-20260924-v1，PASS。公式/KKT推导见已冻结Q3_MODEL_SPEC_v1。51预算，4初值×51=204次SLSQP全部成功；max objective gap=4.86e-13，projected KKT=2.78e-17。quality OFF、mixture OFF，L=2048场景。

| Budget FLOPs | N billion | D billion | Loss | Active |
|---|---|---|---|---|
| 1e19 | .221309 | 7.049698 | 2.998935 | budget |
| 1e22 | 5.202388 | 299.893 | 2.143211 | D support cap + budget |
| 1e24 | 11.965825 | 299.893 | 2.093379 | N/D support caps; budget slack |

内点N/D预算弹性=.451522/.548478。实际路径先在9.325359e21触及D上限，两上限饱和点2.300064e22；无界公式的N上限交点6.886597e22已被D边界路径取代，不能当实际第二转移。

结构转移来自统计支持约束；固定L训练/注意力成本比不随预算改变。高预算未花完是证据域限制，不是现实训练无收益或官方N/D硬上限。dLoss*/dC=-mu，见budget_path.csv；支持范围外不外推配置。

CP2必须远端确认后再运行质量情景。Q4未启动。
