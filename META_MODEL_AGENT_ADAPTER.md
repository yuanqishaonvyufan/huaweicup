# meta-model-agent 项目适配契约

状态：ACTIVE WORKFLOW REFERENCE；不是 meta-model-agent 原生运行时。此项目保留用户指定的 00_problem–11_delivery 目录、六步主流程、默认 Sol/Opus 联合协作协议和 09_handoff/PROJECT_STATE.md 单一状态源。已安装的 meta-model-agent Skill 提供阶段实施协议、证据门槛和返工逻辑；不复制它的另一套工作区或状态机。

## 来源与优先顺序

使用已安装 Skill 的 SKILL.md、references/workflow-map.md、references/gate-matrix.md，并在实际进入某阶段时才读取对应 references/stage_protocols/<name>/SKILL.md。赛题与格式事实以本项目 00_problem/OFFICIAL_REQUIREMENTS.md 和 2026 原件为准；通用 Skill 内其他竞赛年份、模板或目录假设不直接成为本题要求。用户本项目规则优先于通用工作流的默认设置。

## 七阶段与本项目六步对照

| meta-model-agent 阶段 | 本项目六步落点 | 对应材料与执行边界 |
|---|---|---|
| DISCOVERY / problem-intelligence | STEP 1 赛题分析 | 共享上下文 → Sol 草稿 → Opus 延伸 → Sol 整合 → Opus 复核 → 阶段共识；形成问题图、依赖和约束。 |
| FORMULATION / model-formulation | STEP 3 建模求解的规格前半段 | 在 STEP 2 数据审计基础上定义数学机制、模型身份、参数化假设、模型专属预处理合同和验证输入；只有 CONFIRMED 规格进入代码。 |
| COMPUTATION / computational-realization | STEP 2 的冻结输入与 STEP 3 的实现运行 | STEP 2 先完成与模型无关的数据审计和基础清洗；模型专属变换在 FORMULATION 确认后冻结，再执行代码、实验和结构化结果。STEP 2 不能以原始数据复制冒充审计完成。 |
| EVIDENCE / evidence-visualization | STEP 4 检验与 STEP 5 论文写作前的证据图 | 仅从真实结果生成有明确论点、来源和读者任务的图表；纳入 FIGURE_REGISTRY 和视觉检查。 |
| SCHEMATICS / systems-diagramming | STEP 4/5 的必要机制图或流程图 | 仅当逻辑需要时制作可编辑图；不为凑数强制增加，不能覆盖已有数据图。 |
| MANUSCRIPT / manuscript-synthesis | STEP 5 论文写作 | 以当届官方模板、已确认模型和 VALIDATED 结果组稿；摘要最后写。 |
| ASSURANCE / delivery-assurance | STEP 6 图表与最终交付 | 最终图表嵌入质量、格式、匿名、引用、可打开性、结果与源码一致性、提交文件完整性核验。 |

STEP 4 的 validation-audit 是本项目对七阶段之间的补充硬门槛：无验证则结果不能从 RAW/CHECKED 升为 VALIDATED。STEP 6 可做图表最终调整，但调整后必须重做视觉、论文和交付检查。可选 championship-review 只在有完整成稿后、ASSURANCE 前启动；初始化阶段不启用。

## 阶段推进与返工

1. 读取 PROJECT_STATE.md 和 09_handoff/STAGE_GATES.md 确认当前阶段；只加载对应阶段协议，避免提前进入后续阶段。
2. 运行 04_code/utils/stage_gate.py 做结构预检。此脚本只核对文件、非空证据和若干状态，不把存在的占位文本当作数学正确性的证明。
3. 由 Sol/Opus、参赛队或针对性审计核对公式、数据、运行与解释；审查结论和来源落入 10_review/ 与 DECISION_LOG.md。只有结构预检和实质审查都通过，才可在 PROJECT_STATE.md 标为阶段完成。
4. 上游模型、数据或结果改变时，标记其下游实验、VALIDATED 结果、图表和论文主张为待重检；按证据链重算与复检，不靠旧状态放行。

原生 scripts/workspace_init.py、stage_executor.py 和 gate_contracts.py 假定另一套中文目录及固定产物名，不能直接对本项目根目录运行。若以后决定使用原生状态机，应另建隔离工作区并做显式双向映射；不得让两套状态文件同时声称自己是 ACTIVE 来源。
