# Modeling Phase 1 Round 2 QA — 2026-09-24

**结论：PASS，限于定向审计/来源追踪。**程序化复核入口 `python -X utf8 04_code/data_audit/modeling_phase1_round2_qa.py`；机器结果在 [QA JSON](MODELING_PHASE1_R2_QA_20260924.json)。本结论不升级任何模型或论文结果。

## 已核质量门槛

1. 原始《数据说明》PDF SHA-256、A1/A2/A3 原始哈希、B1/辅助检查点索引哈希均与项目冻结清单一致；原始 2,012 附件未修改。PDF 第 2–13 页的 96 段近白色边缘文字由坐标/颜色/字号识别并隔离，不进入官方定义或算法指令。
2. Round 2 三个脚本的当前 SHA-256 与各机器运行记录完全一致。Q1 语义表 22 个唯一指标，`DOWNSTREAM_ELIGIBILITY` 只使用四档允许值；五项仍仅为正向候选，没有当前可进入 Q2 独立质量项。
3. Q1 冲突表保持 Round 1 的 42 个 QCI ID，每条有六类之一；`SEMANTIC CONFLICT` 确认数为 0。分位阈值 0.75/0.80/0.90 全部可查；总汇按 ID 去重为 261,086。A1 两个 n-gram 超 100 ID 的四次上游公式复算误差小于 `1e-9`。区间只覆盖固定分位界下不同 ID 的比例，不伪称外部验证。
4. B1 八条各 147 行；503 次精度切换、748 行条件不符与 Round 1 相同。三处辅助索引 commit 与公开模型 API 一致；15 字段谱系完整。Alert 为 `PARTIALLY RESOLVED`，eligibility 仍 `NOT YET ELIGIBLE`，正式 N–D baseline 运行 0。
5. B8 生成器仍 `UNKNOWN`、`QUARANTINED`。`RESULTS_REGISTRY` 无 VALIDATED FINAL RESULT；正式模型运行仍为 0。Gate 1 路线状态未修改，Gate 2–4 未启动。

## 工具、能力与未用路线

使用项目专用 `skills/data-audit/SKILL.md` 的 `OFFICIAL_MAPPING_FIRST`、既有 Round 1 脚本/清单、Python 本地流式读取和统计诊断；以 `meta-model-agent` 的证据门槛作阶段约束。按 PDF skill 只读检查原始 PDF 的文字对象与渲染；未生成或改写 PDF。公开来源限 Meta-rater 数据卡、RedPajama 与 Pythia 原仓库/模型 API，均只作源义/配置对照；没有向外部服务发送比赛原件或私人内容。

未用 Firecrawl：普通官方页面和小型公开配置已足够，避免不必要 credits。未用 `data-analytics:analyze-data-quality` 的通用流程：本项目 `data-audit` 与冻结映射/哈希合同更具体，数值核验已在上述脚本完成。未用 Office/Spreadsheet 技能：本轮无文档排版或工作簿交付。未调用 Opus：没有新的未控制 Critical 数据定义冲突、主路线取舍或 B8 新机制；B1 仍在原 Alert 的隔离范围内。未安装插件。

## 尚未通过的研究门槛

DSIR 的比赛数据生成版本/目标分布与 A3 n-gram 超界记录的原文复算仍缺；17 项指标仍无通用质量方向。五项正向候选的统计分歧不等于语义冲突。B1 的 `val_loss` 原始运行/验证语料/tokenizer/抽取方式尚无锚，不能启动正式 Scaling Law。B8 生成器未知。Q1 的描述性 Q、R0–R3 的最终响应、A6–A11 留出验证以及 Q2–Q4 正式模型都未完成。

## 开发运行记录与解释界限

Q1 定向脚本在登记最终审计前进行过一次开发检查，随后补充域别符号反转的探索性分类并重新运行；开发输出被最终机器结果覆盖，未被用于模型选择或论文结论。最终登记的脚本哈希和机器输出通过本 QA 逐项核对。今后已登记诊断如需改代码重跑，须另立 Run ID 并保留前版，不复用本轮最终 ID。域别反转的 `|ρ|≥0.1` 分类界为结果查看后的探索性约定，不是预注册门槛。
