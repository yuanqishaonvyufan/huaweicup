# Q2 validation report v1

Numerical QA: PASS，59项。建议CHECKED / ATTACHMENT-INTERNAL RESTRICTED CANDIDATE；Gate3待审，不晋升最终结果。

| validation | S0 | Slog | S1 | S1_worst |
| --- | --- | --- | --- | --- |
| LONO | 0.351306 | 0.117987 | 0.000146888 | 0.00022023 |
| FORWARD | 0.271274 | 0.120386 | 0.000111642 | 0.000176509 |
| BLOCK2D | 0.290069 | 0.122919 | 0.000114134 | 0.00018963 |

证据：18个切分、96条按模型/轨迹指标、逐行预测、fold参数、splits.json；独立QA重算全部RMSE并核N与D隔离，差值小于1e-12。数学检查涵盖有限差分、弹性定义、N-D和质量替代反函数回代、哈希、原件不变和失败隔离。原始8条规模轨迹未随机拆行。

参数多初值、Jacobian、200次整轨迹重抽样、晚期截断/logD权重均已完成。升级触发False，不新增正式候选。B2/B4/B5为来源中心化形状诊断，B7为生成表内中心化Q检验，均不升级为跨来源外部验证。B10无多行族，分组指标记null，不以NaN或0冒充成功。

失败隔离：SCEN v1 numpy.bool序列化，v2无多行B10族导致空中位数；有效v3保留原公式/输入/规则。输入冻结v1/v2因B9四个D零值被正值门槛拦截，元数据保留并加无效标签，不影响B1。无对Q1重新训练或验证。

完整限制见03_models/modeling_phase2/round5/Q2_LIMITATIONS_v1.md。图表4张候选单图已检，最终论文嵌入/完整模板尚未执行。
