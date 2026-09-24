# A1–A3 official mapping confirmation v1

**STATUS: CONFIRMED_OFFICIAL_ID_ROLE_PATH_HASH — 2026-09-24 (Asia/Shanghai).** 先核用户提供的 [F 题《数据说明》原件](../../../../00_problem/original/F_2026_data_description_user_supplied.pdf) 可见正文第 1–2、5–9 页（SHA-256 `f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835`），再核实际文件、`RAW_SHA256.csv` 与每行字段。PDF 页边极浅文字不作为官方定义。文件路径均相对 `01_data/raw/real_attachments/`。

| Official ID | 官方描述/问题角色 | Actual filename/path | SHA-256 | 实测行×字段 | 主键与连接 | 类型/单位/证据 |
|---|---|---|---|---:|---|---|
| A1 | SlimPajama 质量信号抽样集；Q1 全量 22 指标、冲突及与扩展集对照 | `A_data_value/slimpajama_quality_signal_sample.jsonl.xz` | `14a4eeec4c7d98efd78942ddd9c1329640527f2108e73227be449bc1a8dbe579` | 51,230×27 | `id` 各行唯一；含 `content,sub_path,_source_domain,_source_path`；无配方运行键 | JSONL.xz；14 标量+8 列表，单位逐指标审计；E1 样本级派生/模型标注信号 |
| A2 | arxiv 扩展质量信号；Q1 必用全量与 A1 arxiv 对照 | `A_data_value/slimpajama_quality_extended/arxiv_part-6777d8857c6e-000486.jsonl.xz` | `ae1e3399f84f605d994fc60b46984d742e14abb3355d8e7a91822eae1b99e16a` | 17,523×24 | `id` 唯一；`sub_path`；域来自官方路径；无 content/配方运行键 | 同 22 信号和逐指标单位；E1 扩展样本级标注 |
| A3 | github 扩展质量信号；Q1 必用全量与 A1 github 对照 | `A_data_value/slimpajama_quality_extended/github_part-6777d8857c6e-000275.jsonl.xz` | `7af069c71c6027a10f2013cc14dd9d5d17855c264734f69c955544ff6cff7382` | 203,752×24 | `id` 唯一；`sub_path`；域来自官方路径；无 content/配方运行键 | 同 22 信号和逐指标单位；E1 扩展样本级标注 |

三个实际文件共同有完全相同的 22 个质量指标键，A1 的另外五个辅助字段和 A2/A3 的两个辅助字段与官方说明一致。A1 与 A2/A3 分别有 1,419/10,000 个相同 `id`，重叠记录的 22 信号逐值一致；这些行不能当独立实验重复。A2/A3 缺 `content,_source_domain,_source_path` 是官方结构性缺列，不算指标缺失。当前**无 DATA_SCHEMA_DISCREPANCY**，可以进入完整九维审计。

可选 A18 `regmix_domain_sample.jsonl.xz` 是 RegMix 原文样本，不能替代 A2/A3；项目 [OFFICIAL_MAPPING_FIRST](../../../../skills/data-audit/SKILL.md) 规则及 Phase 1 v2 修订记录已固化此边界。质量指标分量语义另以[数据源的 Dataset Card](https://huggingface.co/datasets/opendatalab/SlimPajama-Meta-rater/blob/main/README.md)作**非题面来源**交叉核对；方向、单位与是否能进 Q 均未在本映射表提前确定。
