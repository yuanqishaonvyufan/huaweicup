# Gate4 pre-review package v1

READY FOR PRE-REVIEW / NOT DECIDED。Round6 CP5；Q3 PROVISIONALLY CLOSED，Q4 NOT STARTED。无独立Opus/另一账号审查宣称。源内曲面及场景身份保持，不自动晋升FINAL。

## Reading order

1. 09_handoff/PROJECT_STATE.md、ROUND6_CHECKPOINT_LOG.md。
2. 03_models/modeling_phase3/round6/Q3_DATA_COST_AUDIT的实际位置为01_data/audits/modeling_phase3/round6/Q3_DATA_COST_AUDIT_v1.md；成本与规格在03_models/modeling_phase3/round6/。
3. Q3_RESULTS_REPORT_v1.md、Q3_LIMITATIONS_v1.md、Q3_DELIVERY_FIGURE_TABLE_PLAN_v1.md。
4. 07_validation/round6/Q3_VALIDATION_REPORT_v1.md、10_review/MODELING_PHASE3_R6_QA_20260924.md及机器QA。
5. 02_analysis/consensus/Q3_TO_Q4_INTERFACE_v1.md与Q3_TO_Q4_INTERFACE_v1.json。

## Decision questions

- FLOPs代理、十亿单位、同D、题面三条质量成本和C7外生档位是否正确？不得要求虚构美元价格。
- 基线解析/KKT与204次数值对照能否支持条件配置？支持cap造成高预算闲置是否明确，不能写现实算力无收益。
- 质量情景与局部/全局break-even是否区分？17劣局部起点和4线搜索失败是否透明，嵌套搜索/加密/最佳数值一致是否足够？
- 主配比运输0是否正确处理1M/60M与B1支持不重合？513凸包内候选是否仅限A源，13域权衡与真实供给未知是否保留？
- architecture max≠训练窗口、30000只是两代理交点、当前Loss无context收益项是否说明？
- 200联合向量的条件分位与情景包络是否分开？影子价是否仅曲面/代理条件值？
- Q3→Q4是否只传带来源的Loss/资源情景，不提前产生Benchmark、桥接或预测？

## Proposed use, not a Gate decision

建议审查后允许受限配置作为Q4解释输入；不把情景/供给/域外误差当实证。若发现具体P0，指明公式/输入/规则及受影响Run；普通文字与图表问题在Round6修复，不扩成新Round。Q4需另行授权启动，本轮到预审准备为止。

有效Run：EXP-Q3-BASE-R6-20260924-v1、SCEN-Q3-R6-20260924-v1、UNC-Q3-R6-20260924-v1。六图、九表及全量原始机器输出可追溯，失败起点原始记录仍在。Gate4未PASS。
