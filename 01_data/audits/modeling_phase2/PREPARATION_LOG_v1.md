# Round 5 preprocessing log

2026-09-24。在正式拟合前，前两次输入冻结尝试于B9正值校验停止，部分输出分别隔离在failed_preparation_v1、v2；无模型拟合、参数或选择结果产生。第一次断言未区分元数据与拟合数据，第二次检查确认问题为零值而非缺失。

B9有132条模型元数据，其中 DLRM-2020、InstructGPT 175B、Med-PaLM 2、LMSI-Palm 的D_tokens_B=0。B10有128条正N/D估算Loss。B9零值只作为来源事实保留，增加valid_for_ND_scenario=False，不填补、不解释为真实零token训练、不进入幂律计算；B9从未进入拟合。这是缺失/无效元数据的输入审计处置，不改变B1数学规格、选择标准或训练验证划分。全部原件未改。

成功冻结输入将由INPUT_MANIFEST_v1.json识别；失败目录不得作为模型输入。B1/B2/B4/B5/B6/B7/B10核心字段均通过有限正值检查；B6的360行与B7精确重合，不重复累计证据。
