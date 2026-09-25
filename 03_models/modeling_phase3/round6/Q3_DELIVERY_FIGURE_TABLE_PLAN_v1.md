# Q3 delivery map / figure and table plan v1

不建立平行重复文档，以下按等价章节归档：

| Requested artifact | Authoritative file / section |
|---|---|
| Q3_DATA_COST_AUDIT_v1 | 01_data/audits/modeling_phase3/round6/Q3_DATA_COST_AUDIT_v1.md |
| Q3_COST_MODEL_v1 | 本目录同名 |
| baseline/generalized spec | Q3_MODEL_SPEC_v1.md，前两节分别冻结 |
| Q3_BASELINE_OPTIMIZATION_v1 | 本目录同名、EXP-Q3-BASE输出 |
| Q3_GENERALIZED_OPTIMIZATION_v1 | 本目录同名、SCEN-Q3输出 |
| budget/quality/mixture/context/structure results | Q3_RESULTS_REPORT_v1.md §2–6，九张表、active_set_transitions.csv |
| uncertainty/shadow analysis | Q3_RESULTS_REPORT_v1.md §7–8，UNC-Q3输出 |
| validation/limitations | 07_validation/round6/Q3_VALIDATION_REPORT_v1.md；本目录Q3_LIMITATIONS_v1.md |
| Q3_FIGURE_PLAN / TABLE_PLAN | 本文件；六图manifest与九表逐项下列 |
| Q3_TO_Q4_INTERFACE | 02_analysis/consensus/Q3_TO_Q4_INTERFACE_v1.md及本目录JSON |
| Gate4 package / final QA | 10_review/GATE4_PRE_REVIEW_PACKAGE_v1.md；MODELING_PHASE3_R6_QA_20260924.md |

六图：001基线配置/支持边界；002三成本质量路径；003局部/全局激活；004外生上下文/成本交点；005参数带与情景范围分离；006影子价与quality cap。每图对应来源/Result ID/脚本/300dpi PNG及PDF/15cm字号见figure_manifest。都是正文候选，Gate4与最终模板检查后才正式采用。

九表：001三档baseline；002REFERENCE质量；003五context低预算；004break-even；005条件分位；006影子价；007有限配比；008供应压力；009quality cap压力。来源分别为有效Run的原始CSV，生成入口round6_package.py。原全路径结果保留，候选精简表不替代机器结果。
