# B1 `val_loss` 来源追踪 v2 — Round 3 有界检索

**Audit ID:** `AUDIT-B1-VALLOSS-R3-20260924-v1`。**结论：SOURCE NOT RECOVERABLE FROM AVAILABLE PRIMARY MATERIALS。Alert 仍 PARTIALLY RESOLVED；正式 N–D baseline PAUSED。**依据已冻结的 [停止规则](B1_PROVENANCE_STOP_RULE_v1.md)执行，不扩大到模型权重或大语料下载。原始 B1 哈希不变：`529a59644b0f57bf3a76037838b614bfedc35e58bb26b93052e34ffc63e454c2`。

## 实际核查的来源

1. **比赛附件：**《数据说明》可见正文把 B1 标为 Pythia 真实训练轨迹，并定义 `val_loss` 为验证集交叉熵；原表、`source_manifest.json`、B12 检查点索引、B 组文件及 C10 Pythia 评测说明，均未给出 B1 行级原始 run URI、模型 standard/deduped/v0 变体、验证语料/tokenizer 版本、序列长度、masking/平均规则或逐检查点评估脚本。B3 插值轨迹不能作 B1 独立来源。
2. **Pythia 官方仓库/论文：**[固定提交 README](https://github.com/EleutherAI/pythia/blob/a19eecb807ec2c79a39ebf18108816e6ffffc1d5/README.md)和公开配置给出模型检查点、Pile 路径、tokenizer 类型/词表文件等**候选环境信息**；[原论文](https://proceedings.mlr.press/v202/biderman23a/biderman23a.pdf)明确标准/去重两套模型及 Pile BPE tokenizer。它们没有将比赛 B1 的每个 `val_loss` 连接到可核运行或相同评估设置。配置的评估间隔也不能自行解释 B1 每个发布检查点都有 Loss。
3. **官方 README 链接的 W&B 公开项目：**定向查询 README 所列四个“粗略且不完整”模型组（160M、1B、1.4B、2.8B），分别返回 8、8、16、8 个 run，未触及 100 条查询上限。只在其中两个组的公开最终 step 汇总中发现可核 `validation/lm_loss`：1B 为 2.044498、2.8B 为 1.871449；B1 相应末行是 2.2904、2.1911，差值 B1−公开汇总分别为 +0.245902、+0.319651。见[机器对照](B1_PUBLIC_LOG_PROBE_v1.csv)及[检索记录](B1_PUBLIC_LOG_PROBE_v1.json)，公开 [1B run](https://wandb.ai/eleutherai/pythia/runs/2i9stqg2)、[2.8B run](https://wandb.ai/eleutherai/pythia/runs/12vuw5ef)。这些 run 的公开配置指向 Pile `pile_20B_tokenizer_text_document`、`HFTokenizer`、序列长度 2048，但比赛 B1 没有 run 键；**不能假设它们与 B1 使用同一评估目标或直接判 B1 数值错误**。
4. 对 B1 文件名及少量末检查点值的精准公开检索未找到可复核的原始生成/转换说明。未找到不等于证明不存在私人日志或赛事编制记录。

## 资格判断

Round 2 已核的 147/154 检查点**标签**候选映射继续有效，但这不是 `val_loss` 的行级锚。公开训练配置和 W&B 运行汇总可作为不一致的比较线索，不能代替比赛表的 Loss 来源、验证集/tokenizer/平均规则。`precision/wd/lr` 的训练/评估/后加语义仍未明。

依 [三档规则](EVIDENCE_ALERT_B1_SOURCE_METADATA_v3.md)，本轮仍为 **PARTIALLY RESOLVED / NOT YET ELIGIBLE**。正式 N–D Scaling Law 拟合继续暂停；内部几何、单调性和 `ppl≈exp(val_loss)` 不足以越级。若要评估 `restricted / attachment-internal baseline`，须另立单独证据判断与验证合同，不能因停止检索自动放行。此结论不声称 `val_loss` 为伪造。
