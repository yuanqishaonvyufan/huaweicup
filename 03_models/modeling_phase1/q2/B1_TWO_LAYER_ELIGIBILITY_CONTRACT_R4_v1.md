# B1 双层 baseline 资格合同 — Round 4 v1

**状态：FROZEN BEFORE R4 RECHECK。**本合同在已停止无边界 provenance 检索之后，分开判断 **EXTERNAL EMPIRICAL ELIGIBILITY** 与 **ATTACHMENT-INTERNAL MODELING ELIGIBILITY**。第二层若放行，只能解释竞赛附件自身的数值关系，不会逆向证明附件是原始 Pythia 公开验证日志。Round 4 不估正式 N–D 系数。

## 外部经验资格

要称“经核实的 Pythia 真实验证 Loss 标度律”，必须有模型/变体/run、检查点、验证集/tokenizer/Loss 定义与 B1 行的可复核连接。现有 B1 来源追踪 v2 未取得，故外部经验资格为 **NOT ELIGIBLE**；官方 README 链接的两处 W&B 末步 Loss 与附件不同但目标未证相同，也不能据此断言数据伪造。

## 附件内部受限资格

只检查既有竞赛附件本身是否构成统一的可计算响应曲面，条件如下：

1. 官方可见数据说明把 B1 列为 Q2 主表，定义 `N_params_B,D_tokens_B,val_loss` 单位/目标；原件哈希、1176 行/15 字段、8×147 N–D 网格、同一检查点序列与唯一行键均核对。原始数据不改写。
2. `N,D>0`、`val_loss` 有限且同一列；`D≈steps×2,097,152/10^9`、`C≈6ND`（单位换算）、`ppl≈exp(val_loss)` 的误差只来自公布精度；同一 N 轨迹的 Loss 随 D 不出现无法解释的符号乱跳。再报告固定 D 的跨 N 排序及任何逆转，不以单调性本身证明数据真实。
3. 对 `precision/wd/lr/gpu_days/step_time/grad_norm` 等无可靠谱系或与公开配置不符的元数据，**整体隔离出 Round 5 baseline 自变量**；只允许 `N,D,val_loss` 和由其确定性计算的算力审计列进入模型。缺失外部验证集仍须论文显著披露。
4. 以八条 N 轨迹为独立组，预留整轨迹留出；不得把 1,176 行作独立训练运行。B2/B3 插值或半合成不是独立真值，B4/B5 分级族外/文献验证，A/B 绝对 Loss 不池化。

若内部结构满足 1–4，可给 **B. ELIGIBLE FOR ATTACHMENT-INTERNAL RESTRICTED BASELINE**，其含义是“基于比赛附件内部 Loss 标尺拟合条件性/相对 N–D 曲面”；外部真实性仍未证，结果只按附件内解释，且在 Gate 2/Opus 预审前标 PROVISIONAL。若内部目标或映射不自洽则选 C；若明确损坏/不可用选 D。A 只在外部经验锚充分时选。搜索停止本身不是 B 放行证据。
