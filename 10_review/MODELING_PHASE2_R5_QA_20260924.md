# Round5 QA

**VERDICT: PASS WITH DOCUMENT CORRECTIONS。全部列明整改已完成。** 适用范围为 Q2 附件内部受限候选包；非 Gate3 通过。原数值 QA 59 项全部通过，保留 `MODELING_PHASE2_R5_NUMERICAL_QA_20260924.json` 原文件、时间戳与结论。本次没有重新拟合或复算整套验证。源码/规格/原件/规范输入/输出哈希核对，18 切分隔离、逐行预测、全部 RMSE、有限差分、等 Loss 反函数、整轨迹 bootstrap 均有原核验记录。

单图检查：4 PNG/PDF已生成并逐张目视；字体缺字已修，边界刻度误报已消除；文字bbox全部在画布内。建议15cm嵌入，最低有效字号约9.525pt。没有宣称最终模板编译后的版面通过；原生rendered_visual_audit依赖另一工作区，采用项目适配的figure_manifest字体/bbox记录与真实PNG查看。最终论文嵌入仍须重新检查。

失败隔离与限制见PREPARATION_LOG及SCEN v1/v2 FAILED.md；不掩盖或重写失败。新P0=0；外部来源、真实质量识别、跨来源运输、实际供应、1B转移仍是范围限制，不标已解决。

关键能力：meta-model-agent适配、model-formulation、computational-realization、evidence-visualization，项目model-spec/experiment-runner/validation-audit/result-registry/figure-generator/handoff-builder，本机Python/Git。GitHub插件404后本机Git成功。无需Firecrawl、PDF OCR、Word、图像生成、新插件；没有重开Discovery/Q1/B1来源搜索。配置按AGENTS在恢复/建模/计算/图表/交付阶段复核。范围仅Q2，故全项目四问结构检查器的Q3/Q4缺项不能靠占位文件伪造通过。

未调用独立审稿者；Gate3预审包准备完成。全部数字/表格/图形来自有效Run；报告明确候选身份，ACTIVE FINAL MODEL=NONE，VALIDATED FINAL RESULT=NONE。

## 接管核查十五项

接管核查见 `ROUND5_TAKEOVER_INTEGRITY_v1.json`；字节恢复见 `ROUND5_CHECKOUT_BYTE_RESTORATION_v1.json`。本次发现 P0=0、P1=1、P2=3，均已关闭；科学证据边界继续保留。

| 核查 | 证据 / 结果 |
|---|---|
| 1 规格先冻结 | config、input manifest、summary 引用同一冻结 SHA；记录时间依次为 11:23:17、11:25:20、11:25:34 UTC，沿用 R5-SPEC-001。Git 上传把该轮产物一起提交，不能额外声称有独立第三方时间戳或拟合前单独 Git commit。 |
| 2 splits 无泄漏 | 原 QA 中各 split 的 N/row/D_rank 隔离与逐行预测检查 PASS；本次严格核保存文件原 SHA。 |
| 3 18 splits | LONO 8 + forward 2 + blocked 8；保存切分计数一致。 |
| 4 多初值一致 | 12/12 成功，最大参数差 1.4771e-10；Jacobian rank=5、condition=33.8347，无边界接触。 |
| 5 指标与报告 | summary、三类表格及原 QA 的全部 RMSE 复算记录一致；报告/论文候选全文一致；macro RMSE 为 0.0001468881868 / 0.0001116419818 / 0.0001141339802。 |
| 6 边际公式 | 原 finite-difference / elasticity 检查 PASS；报告使用 -alpha U/N、-beta V/D，总 Loss 弹性有 L 分母。 |
| 7 替代回代 | 原 N–D 与两类质量情景 inverse checks PASS；接口补正余项与支持检查；有限步长不直接用导数外推。 |
| 8 quality 分级 | B7 表内为 SEMI-SYNTHETIC CALIBRATED；转入 B1 为 SCENARIO-CONDITIONAL，默认 g/rho=0。 |
| 9 无 real causal elasticity | TYPE E=0，empirical_quality_coefficient=null；DQ0 不映射 Q_score。 |
| 10 A/B 不池化 | 来源分层 spec 与报告一致；跨源只 centered/relative 形状或显式运输假设，默认 k=0。 |
| 11 B8 不入主参数 | 冻结输入清单无 B8；有效 v3 为 QUARANTINED_UNREAD。 |
| 12 failed v1/v2 隔离 | 两个 FAILED.md 与失败源码快照保留；不作为有效结果。 |
| 13 v3 有效 | SCEN-Q2-R5-20260924-v3 summary 与 15 个输出 SHA 对应；B10 无多行族指标保留 null。 |
| 14 四图与源数据 | 4 PNG + 4 PDF 命中原图 manifest SHA；源码/源数据/Result ID 可追踪，继承单图视觉 QA；本次不重画。 |
| 15 registry/文件 | 有效主 Run 1、有效 scenario 1、失败 scenario 2；9 项 Q2 结果、4 图、5 表齐全；接口 A–J 与导航补全；FINAL 仍 0。 |

## 修复与参数稳定性

R5-TAKE-01 修复 Git 的 checkout 换行转换。14 个文件恢复到原 SHA 对应的字节；其中四个 B9/B10 CSV 含模型名字段内 LF，必须把记录 CRLF 与字段 LF 分开保存。`.gitattributes` 对它们使用 `-text`，对其他冻结文件逐路径规定原 EOL。没有改原件、数据值、模型、阈值或历史哈希；接管审计还比较四个 CSV 在基准 Git 提交和修复后的全部单元，确保无内容更改。

R5-TAKE-02/03/04 补交付导航、接口准入、标准 verdict 和当前状态。已有合并结果报告的弹性/质量/配比章节已足够，不重复创建内容相同的专门报告。

8 折 LONO 的 alpha 范围 [0.3399575823, 0.3400666769]，beta 范围 [0.2798608373, 0.2798961835]。200 次整轨迹 bootstrap 全有效、无边界；alpha 条件 2.5–97.5% 区间 [0.3398079088, 0.3401368564]，beta [0.2798238332, 0.2799344422]。这些仅是附件/模型/小组数交换性假设下的数值稳定性，不是外部真实性、因果识别或域外误差保证。

**Round 5 COMPLETE；Q2 PROVISIONALLY CLOSED — ATTACHMENT-INTERNAL RESTRICTED CANDIDATE；Gate 3 READY FOR PRE-REVIEW / NOT PASSED；Q3 NOT STARTED。**

接管实际核验：82 项检查 PASS，其中 64 项严格 SHA（含新增审计源码；原冻结链为 63 项）。另以暂存区 Git checkout filters 分别模拟 core.autocrlf=true/false，112 项严格 SHA 检查全部 PASS，见 ROUND5_GIT_CHECKOUT_QA_v1.json。与原 59 项数值 QA 分开计数，不把文件校验说成新增模型验证。
