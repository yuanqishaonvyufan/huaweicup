# B1 来源与字段谱系追踪 v1

**Audit Run:** `AUDIT-B1-PROVENANCE-20260924-v1`。**性质：来源审计；没有拟合 Scaling Law。**脚本 `04_code/data_audit/modeling_phase1_round2_b1_trace.py` 在读取前校验 B1、《数据说明》和本地检查点索引的 SHA-256，按固定仓库提交 `a19eecb807ec2c79a39ebf18108816e6ffffc1d5` 读取小型 [Pythia 配置](https://github.com/EleutherAI/pythia/tree/a19eecb807ec2c79a39ebf18108816e6ffffc1d5/models)，没有下载模型权重。机器记录、逐规模矩阵和字段谱系分别见 `B1_PROVENANCE_TRACE_v1.json`、[逐规模矩阵](B1_PROVENANCE_MATRIX_v1.csv)与[15 字段谱系](B1_FIELD_LINEAGE_v1.csv)。

## 已溯清的部分

B1 的八条推断规模轨迹各有 147 个 step，恰好等于[官方 Pythia 说明](https://github.com/EleutherAI/pythia/blob/a19eecb807ec2c79a39ebf18108816e6ffffc1d5/README.md)中的 154 个发布检查点删去最早 `0,1,2,4,8,16,32` 七个；每条轨迹的 step 标签均在本地 `pythia_checkpoint_index.csv` 中。对预定的 70M/step64、1B/step1000、12B/step143000 三个本地 commit 抽样核 Hugging Face 模型 API，三者逐字一致，见[抽样核对](B1_CHECKPOINT_SAMPLE_VERIFICATION_v1.csv)。因此 **检查点标签的候选映射**与本地索引得到部分证实。

这不等于 B1 表内 `val_loss` 来自上述仓库/版本。B1 没有 `model_repo`、standard/deduped/v0 变体、原始 run URI、seed 或逐行 commit 字段；本地 `source_manifest.json` 对 B1 只写 Pythia suite 和“retained from current contest data”。辅助索引给出**可能对齐的发布检查点**，没有将 B1 的 Loss 行连接到原始评估日志。

## 元数据对照和限制

- [官方 README](https://github.com/EleutherAI/pythia/blob/a19eecb807ec2c79a39ebf18108816e6ffffc1d5/README.md)称标准训练一般为 fp16、1B 为 bf16；B1 八条规模轨迹各混用 fp16/bf16，共 503 次轨迹内切换；若字段意指训练精度，748/1,176 行不合该说明。它也可能是评估精度或后加元数据，**当前语义 UNKNOWN**。
- 八条轨迹的 `wd` 各有 69–76 个不同值，范围大致 0.010–0.100；固定提交的八份 Pythia YAML 中 `weight-decay` 均为 0.1。B1 的 `lr` 在每条轨迹内固定，却与八份对应 YAML 的 `lr` 数值均不同。配置属于公开版本的比较锚；这些差异要求字段来源解释，**不能由此单独断言 Loss 是合成的**。
- 公开来源自身有版本线索需要谨慎处理：该仓库 1B YAML 的学习率为 0.00025，而 README 表为 0.0003；1B 训练精度应以具体发布运行/模型配置锁定，不凭文件名猜版本。公开 YAML 中验证语料路径指向 Pile 的 `pile_20B_tokenizer_text_document`，tokenizer 类型/词表路径也可见，但 B1 **没有证据说明使用的就是这套版本化验证和 tokenizer 配置**。
- 公开 YAML 的评估间隔因型号而异，并非自动解释 B1 147 个检查点均有 `val_loss`。若比赛表来自事后逐检查点评估，需要原始运行/评估代码、语料版本、tokenizer 和抽取方法。`ppl≈exp(val_loss)` 只核表内算术，不核独立来源。

## 三档 Alert 判据

| 状态 | 必要证据 | 能否正式拟 B1 N–D baseline |
|---|---|---|
| `OPEN` | 关键来源尚无可核映射 | 否 |
| `PARTIALLY RESOLVED` | 一部分结构或字段来源可核，但关键 Loss/轨迹口径仍缺 | 否 |
| `RESOLVED FOR BASELINE USE` | 八条轨迹与具体模型/检查点对齐；`val_loss` 的来源、验证语料、tokenizer、计算/抽取口径足以确认跨 N/D 可比；有冲突的非基线字段明确标为后加/未知并排除 | 可以先冻结规格、再开始受限来源内 baseline；仍须整轨迹留出和误差披露 |

**本轮结论：`PARTIALLY RESOLVED`；B1 eligibility 仍为 `NOT YET ELIGIBLE`。**能解决的只是候选 step/commit 索引，关键 `val_loss`、模型变体/运行对齐和 metadata 语义仍缺。即使部分非关键字段最终无法追到源头，只要将其排除且上述基线必要证据齐全，未来仍可按第三档重新审定；本轮没有以行数或算术一致性越过该门槛。
