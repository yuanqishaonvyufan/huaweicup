# Q2 delivery, figure and table plan v1

STATUS: ACTIVE navigation for existing CHECKED CANDIDATES。本文件是合并的 Q2_FIGURE_PLAN / Q2_TABLE_PLAN 与交付索引；不复制现有模型、弹性、质量或配比报告。Gate 3 待审，最终论文嵌入未验收。

## 正式文件对应

以下路径相对于仓库根目录。冻结模型使用本目录 `Q2_ROUND5_SPEC_v1.md`，结果使用 `Q2_RESULTS_REPORT_v1.md`，限制使用 `Q2_LIMITATIONS_v1.md`，验证使用 `07_validation/round5/Q2_VALIDATION_REPORT_v1.md`。结果报告第 4 节为等价 Q2_ELASTICITY_SUBSTITUTION，第 6 节为等价 Q2_QUALITY_SCENARIO_REPORT，第 7 节为等价 Q2_MIXTURE_SCENARIO_REPORT。中文论文候选为 `08_paper/sections/Q2_ROUND5_PAPER_CANDIDATE_v1.md`，与结果报告正文一致。

准入规则以 `02_analysis/consensus/Q2_TO_Q3_INTERFACE_v1.md` 和本目录同名 JSON 为准。预审包为 `10_review/GATE3_PRE_REVIEW_PACKAGE_v1.md`，接管索引为 `09_handoff/ROUND5_TAKEOVER_RECOVERY_CHECK_v1.md`。

## 证据层级

| Level | 内容 | 必须保留的标签 | 可写结论 |
|---|---|---|---|
| 0 | B1 N–D 条件拟合 | ATTACHMENT-INTERNAL ESTIMATED | 附件给定 Loss 标尺的五参数经验代理 |
| 1 | 轨迹验证、导数/弹性、替代 | ATTACHMENT-INTERNAL ESTIMATED；区间 DIAGNOSTIC ONLY | 三类预定验证支持附件内用途；非外部验证 |
| 2 | B7 质量斜率和规模调节 | SEMI-SYNTHETIC CALIBRATED | 生成表内条件关系；运输到 B1 另标 SCENARIO-CONDITIONAL |
| 3 | A 源配比/规模及跨源情景 | EMPIRICALLY ESTIMATED（仅 A 源关联）；SCENARIO-CONDITIONAL（运输） | 1M 限定，60M 部分 centered-shape transfer，1B 失败；g/k/rho 默认零 |
| 4 | B8 隔离证据 | QUARANTINED | B8 不进入参数；另保留 B9 零 D 禁用和失败 Run 隔离；B9/B10 外推讨论仍为 SCENARIO-CONDITIONAL，B10 不作真值 |

## 四张候选图

统一生成脚本 `04_code/visualization/round5_figures.py`；PNG/PDF、源数据和哈希见 `06_results/figures/round5/figure_manifest.json`。主运行为 EXP-Q2-ND-R5-20260924-v1，情景运行只取 SCEN-Q2-R5-20260924-v3。

| 图 | 正文位置与论点 | 来源 / Result ID | 交付边界 |
|---|---|---|---|
| FIG-Q2-R5-001 | 结果第 2–3 节；八轨迹拟合及残差 | 主运行 training_predictions；ND-001 / UNC-001 | 规则曲面不证明外部真实性 |
| FIG-Q2-R5-002 | 第 3 节；三类验证与 S0/Slog 对照 | 主运行 validation_metrics；VAL-001 | 18 splits，非随机行划分；仅附件内部 |
| FIG-Q2-R5-003 | 第 4 节；状态依赖总 Loss 弹性 | 主运行 marginal_effects；MARG-001 | 幂指数与总 Loss 弹性不同 |
| FIG-Q2-R5-004 | 第 6 节；B7 单元斜率、条件资源替代 | 有效 v3 quality_cell_slopes / quality_substitution_scenarios；QUAL-001 / SCEN-Q2-R5-SUB-001 | 上部半合成，下部假设情景；不是实测节省 |

上表简写 ND/UNC/VAL/MARG/QUAL 的前缀均为 CAND-Q2-R5-。优先嵌入 PDF 向量图，建议宽度 15 cm，既有单图 QA 最小有效字号约 9.525 pt；最终模板中须再检查。接管仅核图哈希，未重画、未冒称新的目视审稿。

## 五张候选表

统一位于 `06_results/tables/round5/`，每张含 `.csv` 和 `.md`，生成来源为 `04_code/modeling_phase2/round5_package.py`。冻结生成程序保留不改；本次接口和导航补充不得用旧 package 生成程序覆盖。

| 表 | 正文位置 | 来源 / 任务 |
|---|---|---|
| TABLE-Q2-R5-001_parameters | 第 2 节 | 主运行 summary、bootstrap；五参数与条件区间 |
| TABLE-Q2-R5-002_validation | 第 3 节 | 主运行 validation；三类 macro/worst RMSE 与对照 |
| TABLE-Q2-R5-003_evidence | 第 5 节 | 冻结来源分级和有效 v3；证据可用/不可用边界 |
| TABLE-Q2-R5-004_marginal_example | 第 4 节 | 主运行 marginal_effects；N=1,D=100 的插值示例，不是优化解 |
| TABLE-Q2-R5-005_quality_scenarios | 第 6 节 | 有效 v3 quality_substitution_scenarios；机制/运输敏感性 |

## 十二项数学问题的定位

| 问题 | 已有回答 |
|---|---|
| 1 N scaling | 结果第 1/2/4 节；alpha 与负边际 |
| 2 D scaling | 第 1/2/4 节；beta 与负边际 |
| 3 exponents/stability | 第 2/3 节；summary、fold_parameters、bootstrap、parameter_sensitivity |
| 4 N/D marginals | 第 4 节及 marginal_effects |
| 5 N/D elasticity | 第 4 节；总 Loss 与超额 Loss 区分 |
| 6 fixed-Loss N/D substitution | 第 4 节；ND_finite_substitution，正余项与支持检查 |
| 7 conditional quality | 第 6 节；B7 45 单元、9 N 组 centered LONO |
| 8 quality vs N/D substitution | 第 6 节；常数 g 和有效 D 两机制；SCENARIO-CONDITIONAL |
| 9 mixture evidence level | 第 7 节；A 源限定关联，跨 A/B 仅外生运输 |
| 10 mixture scale dependence | 第 7 节；1M/60M/1B；没有已识别通用交互系数 |
| 11 Q3 allowed | Q2→Q3 A–H，待 Gate 3；区间仅敏感性 |
| 12 Q3 forbidden | Q2→Q3 I/J、limitations；TYPE E=0、B8、跨源绝对 pooling、实际成本缺口 |

收口状态：Round 5 COMPLETE；Q2 PROVISIONALLY CLOSED（受限候选）；Gate 3 READY FOR PRE-REVIEW / NOT PASSED；Q3 NOT STARTED。
