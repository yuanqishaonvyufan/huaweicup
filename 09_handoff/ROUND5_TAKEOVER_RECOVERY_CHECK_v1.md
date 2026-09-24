# Round 5 takeover recovery check v1

接管日期：2026-09-24。事实源：已 fetch 并 fast-forward 的 GitHub main `47b88843c43b55e1fd822ac0b5344ba1387e9fb9`。同步前本地 HEAD 为 `052ba706464fa9a1d092ba1f8d01d50a328b61c8`，工作区干净，无覆盖未提交工作。首次 schannel 证书链失败后以 Git OpenSSL 后端完成验证连接；未关闭 TLS 验证。

旧账号真实断点：**Round 5 计算、论文候选、数值 QA、4 图/5 表、registry 和 Gate 3 预审包均已提交；Gate 3 尚未裁决，Q3 未开始。** 本次不重新拟合或运行情景，不重做 Q1，不重画完整图形。

## 恢复矩阵

状态限定为 COMPLETED / PARTIAL / MISSING / SUPERSEDED。下表“接管时”反映远端基准提交；后续修正不倒改历史。

| 项 | 接管时 | 真实产物 / 剩余事项 |
|---|---|---|
| A baseline spec | COMPLETED | `03_models/modeling_phase2/round5/Q2_ROUND5_SPEC_v1.md`，等价正式模型规格；不得另造重复 spec |
| B fit / parameters | COMPLETED | `06_results/raw/EXP-Q2-ND-R5-20260924-v1/summary.json` |
| C trajectory validation | COMPLETED | 同运行 `splits.json`、`validation_predictions.csv`、`validation_metrics.csv`；18 splits |
| D stability | COMPLETED | 同运行 `fold_parameters.csv`、`cluster_bootstrap.csv`、`parameter_sensitivity.csv` |
| E residuals | COMPLETED | 同运行 `residual_diagnostics.csv` |
| F marginals | COMPLETED | 同运行 `marginal_effects.csv`；结果报告第 4 节 |
| G N–D substitution | COMPLETED | `SCEN-Q2-R5-20260924-v3/ND_finite_substitution.json`（位于 raw 下）；结果报告第 4 节 |
| H quality scenarios | COMPLETED | 有效 v3 的斜率、centered LONO、替代情景；结果报告第 6 节为等价正式报告 |
| I mixture / scale | COMPLETED | 有效 v3 的 inherited evidence / tangent scenarios；结果报告第 7 节为等价正式报告 |
| J elasticity evidence | COMPLETED | `06_results/tables/round5/TABLE-Q2-R5-003_evidence.csv` + `TABLE-Q2-R5-004_marginal_example.csv` + 结果报告第 4/6/7 节 |
| K four figures | COMPLETED | `06_results/figures/round5/FIG-Q2-R5-001` 至 `004`，各 PNG/PDF；manifest、脚本、来源 Run 均在库 |
| L model/results/validation/limitations | COMPLETED | round5 模型目录、`07_validation/round5/Q2_VALIDATION_REPORT_v1.md`、论文候选；合并报告覆盖弹性和情景，不复制同文 |
| M Q2→Q3 | PARTIAL | 已有 Markdown/JSON 边界；补 A–J 显式准入分类与缺失成本输入清单 |
| N Round 5 QA | PARTIAL | 原 59 项数值 QA PASS 已存在；本机 checkout 换行造成哈希不一致，须修保存规则并实测复核；统一 verdict 用语 |
| O Gate 3 package | COMPLETED | `10_review/GATE3_PRE_REVIEW_PACKAGE_v1.md`，READY / NO DECISION |
| P registries | COMPLETED | 9 项 Q2 结果、4 图、有效/失败 Run 已登记；顶部已有当前状态，旧 Round 4 统计明确是历史；本次只追加接管记录 |
| Q state / next action | COMPLETED | 已推进到 Round 5 complete、Gate 3 ready；本次补充“受限候选的暂定关闭”与接管结论，不作 Gate 3 裁决 |
| figure/table reading plan | MISSING | manifest/registry 已有实质内容；补一个合并导航计划，不重画图、不再造表 |
| 本地旧状态 052ba70 | SUPERSEDED | 同步前“Round 5 NOT EXECUTED”已由 main 47b8884 取代，不是需要重新执行的任务 |

## 核验发现与修复范围

R5-TAKE-01（P1，已修复）：`core.autocrlf=true` 改写了冻结脚本/spec 的 LF；B9/B10 两个规范输入及其两个派生 CSV 中模型名 `Solar Open 100B\n` 的字段内换行也被转为 CRLF。已验证按记录的原始 LF/CRLF 或 CSV 记录分隔格式重建，可精确命中既有 SHA-256；不调整任何数值、不重算。已添加精确路径 `.gitattributes`，保留原哈希并在接管机器审计中记录前后对照。

R5-TAKE-02/03/04（P2）：补合并交付导航、接口 A–J 分类、接管状态与 QA verdict 用语同步。原有效主运行 v1、情景 v3、失败情景 v1/v2 全部保留。

## 最终收口

恢复清单 checkpoint `f838ca4` 已推送。M/N 补充项与合并图表导航现均 COMPLETED，A–Q 全部收口；历史失败保留。字节恢复逐文件前后 SHA 见 `10_review/ROUND5_CHECKOUT_BYTE_RESTORATION_v1.json`；接管严格哈希/交付核查见 `10_review/ROUND5_TAKEOVER_INTEGRITY_v1.json`。原 59 项数值 QA 不重跑、不改写。

Q2 PROVISIONALLY CLOSED 仅指本轮受限候选研究关闭；Gate 3 READY FOR PRE-REVIEW / NOT PASSED；Q3 NOT STARTED。最终交付提交通过后续 handoff checkpoint 记录，当前提交不自引用自身 SHA。

最终本机核验：82 项完整性/交付检查 PASS（64 项严格哈希），112 项 Git checkout 换行配置复现检查 PASS。QA verdict：PASS WITH DOCUMENT CORRECTIONS（全部修正已完成）。新问题 P0=0、P1=1、P2=3，未解决=0；继承的来源/识别/尺度/供给限制仍保留。
