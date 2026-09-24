# DATA_LINEAGE

## 初始化复制

来源：项目上级 real_attachments/。目标：01_data/raw/real_attachments/。2026-09-23 使用保留时间戳的复制方式建立独立原始数据副本，未移动或修改上级原件。复制后两处文件数均为 2,012，字节总数均为 551,191,693。逐文件 SHA256 核验结果记于 raw/RAW_SHA256.csv，2,012 项全部一致。目标中有一条绝对路径超过传统 Windows 260 字符限制；校验使用扩展长度路径成功读取，后续脚本也需注意此问题。

用户提供的题面与数据说明，以及平台下载的格式附件，保存在 00_problem/original/；SHA256 见该目录 SOURCE_MANIFEST.md。

## 后续证据链合同

Raw file SHA256 → preprocessing script/config → interim dataset → processed dataset SHA256 → model specification/version → experiment ID → raw result → validation report → VALIDATED result ID → paper location。

每个 processed 数据集必须记录输入路径与哈希、处理脚本版本、参数、时间、输出哈希、字段/样本数变化及用途。初始化阶段尚无 interim 或 processed 数据版本。

## Phase 1 审计修订

2026-09-23 首轮路线审计 v1 将可选 RegMix 原文样本 A18 误归类为扩展质量信号，未读取 A2/A3。发现后保留 v1 报告、指标、分支输入/输出和脚本于 `01_data/audits/phase1/superseded_v1/`；当前 `route_decision_phase1.py` 修订 v2 按可见《数据说明》与实际路径流式读取 A1、A2、A3，重新生成指标及分支输出。A1/A2/A3 分别为 51,230/17,523/203,752 条，仍无 A4/A5 同运行键；`NO_MATCHED_Q` 结论未变，但 A1 与扩展集的样本重叠纳入后续 Q1 设计。原始附件未修改，processed 仍无。
