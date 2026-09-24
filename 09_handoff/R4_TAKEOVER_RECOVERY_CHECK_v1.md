# Round 4 takeover recovery check v1

日期：2026-09-24（Asia/Shanghai）。角色：CONTINUATION LEAD SOL。依据当前磁盘文件恢复，不以交接提示代替产物核查。本报告记录接管时状态；后续收口见 Round 4 QA 与 Gate 2 v1.1 包。

## A. 已完整存在、直接复用

| 类别 | 已有产物 | 接管核查 |
|---|---|---|
| 冻结训练 | `EXP-Q1-PRESP-TRAIN-R4-20260924-v1`；`P_RESPONSE_FROZEN_MODEL_BUNDLE_v1.json`、训练指标/五折/OOF、预拟合合同 | bundle SHA-256 `9c1e8887098595f05aaa37e94d21658d0010cf6fb8bb8702bc965e8b73246e39` 与登记一致；训练脚本 SHA-256 `68a6a1b2...`；只读 A4/A5，`A6_A11_loss_read=false`；16D 满秩、条件数 45.4356 |
| 正式验证 | `VAL-Q1-PRESP-A6A11-R4-20260924-v2`；验证 JSON、CSV、逐行预测、逐域及支持表 | JSON 引用上述 bundle；验证脚本 SHA-256 `0839b12b...`；五个 CSV 的 SHA-256 与验证 JSON 一致；A7/1M M1 R0 RMSE 0.227765、M0 0.284615，13/13 域改善 |
| 失败运行 | `VAL-Q1-PRESP-A6A11-R4-20260924-v1` | JSON NumPy int64 序列化错误；说明文件及五个 CSV 在 `failed_validation_v1/`，不作模型选择 |
| Q1 文字收口 | `Q1_MODEL_SPEC_v1`、`Q1_RESULTS_REPORT_v1`、`Q1_VALIDATION_REPORT_v1`、`Q1_LIMITATIONS_v1`、`P_RESPONSE_MODEL_COMPARISON_v1`、`P_RESPONSE_VALIDATION_A6_A11_v1`、`P_FEASIBLE_REGION_EVIDENCE_v1`、`Q1_FIGURE_PLAN_v1`、`Q1_TABLE_PLAN_v1` | 均存在；现有结论为暂定候选、非 ACTIVE FINAL MODEL |
| 接口与 B1 | `Q1_TO_Q2_INTERFACE_v1_1.md`、`B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md` | 均存在；TYPE E=0；B1 附件内 B 级受限入口待 Gate 2 |
| 表图 | `tables/` 五张 Markdown 表及 manifest；`figures/` 四张 PDF、四张 PNG 及 manifest | 文件均存在，人工查看四张 PNG：轴/单位或无量纲比、样本量及主要边界可辨；未重新生成 |

## B. 存在但收口未完成

- `RESULTS_REGISTRY.md` 有 Round 4 五项候选结果，但未单独登记 M1/M2 五折分数、M3 未触发及 M2 验证无稳定增益。
- `FIGURE_REGISTRY.md` 仍写“当前无正式图表”，未登记已生成的四张 Round 4 候选图。正式论文图资格仍待 Gate 2/整体排版。
- `GATE2_PRE_REVIEW_PACKAGE_v1.md` 已存在，但声称不存在的 Round 4 QA 已完成，应保留为历史 v1 并新建 v1.1。
- `B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md` 末尾引用 Alert v3；最新权威 Alert 已是 v4。v3 是继承来源缺口的历史版本，不删除。
- B1 双层裁决至预冻结合同的相对链接少一级目录；后续活跃文档链接 QA 中修正。
- handoff 文件仍称 Round 4 QA 存在、Gate 2 预审待办；须在 QA 后同步。
- `README.md`、`MODELING_PHASE1_STATE.md`、`STAGE_GATES.md` 与 `VALIDATION_REPORT.md` 仍留在 Round 1 或“未计算/未验证”描述；须随收口同步，归入同一状态文档陈旧问题。

## C. 接管时完全不存在的预期文件

- `10_review/MODELING_PHASE1_R4_QA_20260924.md` 及机器 QA JSON。
- `10_review/GATE2_PRE_REVIEW_PACKAGE_v1_1.md`。

## D–E. 最近图与来源

| Figure ID | 文件 | 来源 | 状态 |
|---|---|---|---|
| FIG-Q1-R4-001 | `figures/FIG-Q1-R4-001_core_domain_profile.pdf/.png` | `Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv`；质量闭合审计 | manifest 含来源、脚本及文件哈希；五维质量域画像 |
| FIG-Q1-R4-002 | `figures/FIG-Q1-R4-002_domain_validation_gain.pdf/.png` | 正式验证 v2 的 `P_RESPONSE_DOMAIN_VALIDATION_v2.csv` | manifest 含哈希；13 域 M1/M0 RMSE 比 |
| FIG-Q1-R4-003 | `figures/FIG-Q1-R4-003_scale_transfer_failure.pdf/.png` | 正式验证 v2 的 `P_RESPONSE_VALIDATION_METRICS_v2.csv` | manifest 含哈希；1M/60M/1B 仅中心化形状比较 |
| FIG-Q1-R4-004 | `figures/FIG-Q1-R4-004_support_strata.pdf/.png` | 正式验证 v2 的 `P_SUPPORT_VALIDATION_ROWS_v2.csv` | manifest 含哈希；经验支持分层，附录候选 |

图形生成脚本 `04_code/modeling_phase1/round4_q1_figures.py` 已存在；接管时 manifest 为 `PAPER_FIGURE_CANDIDATES_PENDING_COMPILED_LAYOUT_QA`。四图均可见且未发现明显裁切。完整哈希/数值一致性由后续 QA 复核。

## F–J. 登记、QA、Gate 2、Alert 与真实断点

- Experiment Registry 已登记训练 v1、失败验证 v1、有效验证 v2；正式 N–D 拟合为 0。Results Registry 有十项候选/诊断、VALIDATED FINAL 为 0。Figure Registry 尚未同步四图。
- 接管时 **Round 4 QA 不存在**；Gate 2 包最新为 `GATE2_PRE_REVIEW_PACKAGE_v1.md`，其 QA 已通过的措辞不成立。
- B1 权威来源警报：`EVIDENCE_ALERT_B1_SOURCE_METADATA_v4.md`，明确继承 v3 未解外部来源，同时记录独立的附件内 B 级提案；v1–v3 保留历史。
- **第一个真正未完成任务：基于冻结包和既有输出补做 Round 4 只读 QA。**之后同步结果/图形登记与状态，再生成 Gate 2 v1.1 包。训练、验证和现有图表不重做。
