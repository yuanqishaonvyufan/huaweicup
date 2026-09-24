# B1 `val_loss` 来源追踪停止规则 v1

**状态：FROZEN FOR ROUND 3 SOURCE TRACE。**本规则只决定何时停止搜索和如何表述剩余不确定性，不能自动将 B1 放行。继承 B1 Alert v2 的 `OPEN / PARTIALLY RESOLVED / RESOLVED FOR BASELINE USE` 三档。

## 有界检索顺序

1. 比赛《数据说明》可见正文、B 组全部附带元数据/说明、`source_manifest.json`、原始 B1 CSV、B12 索引及项目已核原件哈希；只查 B1 关键字段，不重跑 Round 1 九维审计。
2. EleutherAI Pythia 官方仓库固定提交的 README、训练配置、评估脚本/结果索引与其明示的 W&B run 链接；Hugging Face 发布模型的轻量级 revision/config 元数据。只取小型文本/API 元数据，不下载模型权重或大语料。
3. Pythia 原论文及官方公开训练/评估日志中可追溯的 Loss 说明。再用少量预定的 B1 检查点数值作定向匹配；第三方解释只帮助定位，不作为解除 Alert 的独立证据。

上述三个层级均查过仍无 B1 的 `val_loss` 原始 run 或明确转换链、验证语料/tokenizer、计算/平均/掩码/序列长度口径时，停止继续低收益网页搜索，记录 **SOURCE NOT RECOVERABLE FROM AVAILABLE PRIMARY MATERIALS** 和实际已查位置。无搜索命中不等于证明数值伪造。

## 解除 Alert 的必要锚

`RESOLVED FOR BASELINE USE` 至少需要足以解释：八条 N 轨迹的具体模型/变体与检查点-D 映射；B1 `val_loss` 的来源或可复核加工过程；跨 N/D 行可比较的验证语料、tokenizer、Loss 单位、序列/平均/掩码约定。有代表性的行值应能按原日志或已文档化的处理规则核对；非基线 `precision/wd/lr` 可标后加/未知并排除。内部几何满秩、单调 Loss 和 `ppl≈exp(val_loss)` 不能代替这些锚。

若主来源找不到，后续可**另立独立证据判断**研究 `restricted / attachment-internal baseline` 的价值与极限，但不得由本停止规则自动放行，也不得称该基线是经核实的官方 Pythia 原始验证曲线。当前阶段正式 N–D Scaling Law 仍暂停。
