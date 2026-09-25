# FINAL DOCUMENT INTERFERENCE CONTAMINATION AUDIT v1

**HuaweiCup_F_2026 · 独立只读审计 · 2026-09-25**
**静态搜索基线：** 1b0a1734befe3994972f2d336a9c7ae35fbfc10c（Round8终稿/一致性QA之前）
**Checkpoint 1：** fb78d31be8d012688520cc43c5f12d94fe302314（已推送）

## 1. Executive verdict

**A. PASS — NO MATERIAL CONTAMINATION**

原件中20类隐藏/近白/小字号干扰内容、96处出现得到复核。没有完整隐藏句、独特公式、方法+参数+结果组合进入正式模型或论文，也没有正式核心结果只能追溯到隐藏文本。仓库筛查表记录726行指纹相关命中：3个是明确的反泄漏审计引用，723个是经字段/数据/Run ID追溯的独立数值巧合。CLASS C=0、CLASS D=0。

| 问题 | 隐藏文本相关命中 | 核心结果有独立证据链 | 实质污染 |
|---|---|---|---|
| Q1 | QA guard片段；PCA/Aitchison等低特异性方法词 | YES | NO |
| Q2 | .081/.075/.87等数字出现在无关输入字段；B1拟合参数不同 | YES | NO |
| Q3 | 10²²是题面预算；Q=1只在部分情景最优 | YES | NO |
| Q4 | .32/.18/.68是原始任务分数/家族份额；桥接被验证拒绝 | YES | NO |

20个完整canonical隐藏文本均未复制到活动模型、结果或论文中。3个短片段只出现在防泄漏QA断言中；没有进入核心模型输入。完整详情见[Inventory](INTERFERENCE_INVENTORY_v1.csv)、[Fingerprints](INTERFERENCE_FINGERPRINTS_v1.csv)、[Repo Hits](INTERFERENCE_REPO_HITS_v1.csv)、[Temporal Trace](INTERFERENCE_TEMPORAL_TRACE_v1.csv)和[Core Result Provenance](CORE_RESULT_PROVENANCE_AUDIT_v1.csv)。

## 2. 20类隐藏内容 / 96处出现

原始《数据说明》PDF的SHA-256为f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835，与既有DOCUMENT_INTERFERENCE_AUDIT_v1.json一致。按原排除规则（RGB≥#f0f0f0、字号≤5.1pt、页面顶/底边缘）重新抽取，并逐页对照96个span hash：13页、96个span、Unicode/大小写/空白规范化后20类；第1页0处，第2–13页各8处。

清单列出20类canonical文本、页码/页边位置、出现次数、数值/方法/结论指纹和风险类别。Inventory现已逐行标记为**不可信指纹专用**，不得当作官方定义、建模指令、证据、参数来源或预设答案。

## 3. Search methodology

**只读与项目配置。** 按项目MODE B独立复核；没有改Q1–Q4模型、参数、结果、论文或历史提交，也没有重新训练/优化。开始时工作树干净；git fetch后本地main与origin/main均为1b0a1734…。

**先例与信任边界。** 复用仓库DOCUMENT_INTERFERENCE_AUDIT_v1的RGB/字号/位置与哈希核对规则。D:\work document\codex_work中未发现同题可直接复用审计；另一个论文合规审计仅作记录方式参考。公开安全先例只核对了OWASP GenAI LLM01:2025关于不可见/间接输入及隔离外部内容的说明：[OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)。该页面只支持信任边界方法，不作为竞赛模型证据；没有上传项目文件或原PDF。

**检索覆盖。** baseline包含719个tracked文件。纳入686个可搜索文本/表格文件：Markdown/TXT/Python/Notebook/JSON/YAML/CSV/TeX/log/SVG、5个DOCX、15个非指纹源PDF、4个本地解压CSV.GZ和2个仓库配置文本。DOCX用本地python-docx，PDF用本地文本层。原数据说明PDF只作指纹源单独审计、不加入命中目标；未纳入检索的33项是该源PDF、旧式官方.doc模板和31张PNG二进制图。终稿PDF、DOCX和Markdown均纳入文本检索。

**指纹检索。** 逐项筛精确句、NFKC/大小写/空白规范化短语、特别数值、数值组合、算法组合、公式结构、阈值/超参数。单一数字要结合字段与结果语境；单一方法名不自动判污染。检索快照固定在baseline HEAD，新增指纹和结果文件没有回流进自己的静态搜索。首次出现信息使用Git blame或文件首次入库commit proxy，并在核心结果中继续追Run、代码和输出。

**工具和Skills。** 使用项目validation-audit、paper-consistency、Meta-model-agent阶段适配及PDF/Spreadsheets Skills；工具为Git、PyMuPDF、pypdf、python-docx、ripgrep、Python CSV和Git blame。Excel/OfficeCLI和Codex Security插件不适用于这项本地结果provenance审计；旧式.doc无本地转换器。未跑建模、优化、训练或新QA流程。

## 4. Repository hit statistics

| 类别 | 行数 | 判读 |
|---|---:|---|
| CLASS A：QA反泄漏片段 | 3 | guard检查活动题目/共识/状态/handoff没有这些片段 |
| CLASS B：数字单点巧合 | 723 | 已追到独立字段、数据、题面预算或机器输出 |
| CLASS C：确认的短暂提示暴露 | 0 | 没有隐藏建议的独特文本/组合进入模型prompt/handoff |
| CLASS D：材料性污染 | 0 | 无核心结果只能由隐藏文本解释 |
| 完整隐藏句/高特异性数值组合/方法+参数+结果组合 | 0 | 正式模型、结果、handoff和终稿无此类命中 |
| 低特异性方法词命中 | 519行 | 规范、模型、代码和handoff文本；原始数据行不计作方法命中；逐项按语义核查，不计作污染命中 |

723条独立数值行中，650条来自C8的raw_accuracy任务分数，29条来自Q1 training_p_matrix，另2条来自压缩的A1/A3质量特征表；其余主要是官方预算文本、图轴、Q4家族份额或派生量。.32/.18/.68等单点数字不是隐藏弹性/相关系数。方法名也须结合用途核查：Pythia是数据/模型家族名，complementarity是Q3的KKT检查，Softmax在Q1处理列表型信号。 词级出现数：complementarity 264、Pythia 150、PCA 61、OLS 19、Softmax 15、Aitchison 6、decision tree 3、Kendall 1；共519条不同文本行，均无方法+隐藏参数/结果组合。

## 5. Q1 audit

**指标、DQ0和PCA。** A1–A3保留全部22项及字段角色；5项方向有数据卡依据，形成描述性主坐标。DQ0是这5项A1参考百分位的透明等权均值，不是隐藏文本建议的K-means类别占比。DQ1 PCA PC1解释48.11%；A5的13域响应PC1解释22.78%；两者都被限制为诊断，不作为唯一质量分。隐藏的K-means三类评分与“1–2个PC直接加权”没有进入ACTIVE主分。

**冲突定义。** Round2对42项候选按REDUNDANCY、SCALE ARTIFACT、STATISTICAL DISAGREEMENT、UNRESOLVED等分类；语义冲突确认0项，但统计逆序和分歧仍被量化，q=.75/.80/.90是分位阈值。它不是隐藏文本的“z分数差>.5”规则，也没有把Kendall W汇总为单一置信度。三个短片段只在Round2 QA的反泄漏检查中出现；QA记录96个额外span已排除、状态PASS。

**M1与尺度验证。** A4/A5的512个配方输入形成16D零值安全Euclidean Helmert contrast；bundle在读取A6–A11 Loss前冻结。Run VAL-Q1-PRESP-A6A11-R4-20260924-v2给出：A7/1M M1 R0 RMSE=.2278（M0=.2846），13/13域改善；A9/60M只保留中心化配比形状；A11/1B误差比3.108、判为失败。系数确实被原样带到不同尺度作为transfer test，但结论由留出结果决定；没有“跨尺度必定成立”的承诺。

**Q1 verdict：** PASS。核心指标处理、冲突定义、M1、RMSE和跨尺度结论均可追到源数据、冻结契约、Run和机器输出；隐藏方法没有决定核心结果。

## 6. Q2 audit

B1提供8个N级、1,176个checkpoint。受限加性幂律为L=E+A·N^(−alpha)+B·D^(−beta)。EXP-Q2-ND-R5-20260924-v1的12个有界初值均收敛，拟合为E=L∞=1.68979756、A=.35398032、B=1.24030558、alpha=.33997658、beta=.27987813。三个留出结构的S1 RMSE分别为LONO .000146888、FORWARD .000111642、BLOCK2D .000114134。

隐藏Pythia数值E=3.52、alpha=.081、beta=.075、R²=.87没有进入B1参数；仓库里.081/.075/.87的单点命中出现在Q1配比输入矩阵，而不是拟合系数。B7质量响应是半合成：45/45 N-D单元斜率为负，共同斜率−.361995；不是因果质量弹性。替代例由拟合曲面精确反解，支持域外的D明确标记越界；没有CES生产函数。

**Q2 verdict：** PASS。参数、三种validation RMSE、质量斜率和替代例都有独立数据、脚本、Run ID和机器输出；没有隐藏值成为拟合参数。

## 7. Q3 audit

Q3基线在质量收益OFF、p固定、L外生、B1支持范围内优化。基线Run EXP-Q3-BASE-R6-20260924-v1的代表解为：

| Budget | N (B) | D (B) | Loss |
|---:|---:|---:|---:|
| 10^19 | .221309 | 7.049698 | 2.998935 |
| 10^22 | 5.202388 | 299.893 | 2.143211 |
| 10^24 | 11.96583 | 299.893 | 2.093379 |

这些数值由解析消元和204个SLSQP起点核对。隐藏预填tuple在10^22给N=.0012B、D=850B、Q=1、Loss=3.41；其中N低于支持下界.070542，D高于上界299.893，Loss也不同。10^22预算本身来自题面，不是隐藏段独有指纹。

SCEN-Q3-R6包含1,377个质量/成本配置、4,131个数值起点并保留失败行。10^19时指数/幂成本的Q最优分别约.6748/.5068，对数成本Q=1；高预算才常到Q上界。因此“任何预算都应Q=1”不是无条件结果。结构转移约9.325359e21与2.300064e22来自活动约束集合变化；Lcrit=6/eta=30,000是成本两项相等的解析点，不是实测产业阈值。

**Q3 verdict：** PASS。优化配置来自冻结的B1参数、题面成本、支持边界和数值核验；隐藏固定tuple不可行，惩罚函数和分类模型没有决定最终求解器。

## 8. Q4 audit

EXP-Q4-R7-20260925-v1的最终桥接 verdict 是NO RELIABLE BRIDGE，操作分支B0禁止数量运输。高可比层只有7个ID、1个家族；high-family Spearman=.60714仍未通过holdout/尺度条件。隐藏+.68在项目里主要是C8 raw_accuracy或Q4 family-share，不是拟合出的Loss–Benchmark相关系数。

最终动态模型选中bounded logit，而不是ARIMA、Markov等级迁移或10分分箱。853条主样本的28天滚动Q90前沿由36.453073升至52.332722。参数关联/残差分解为17.0233%/82.9767%，但对筛选和窗口敏感、可反号；完整N-D贡献与真实技术进步份额仍未识别。2027/2028条件中心79.75536/87.12751，95%条件PI分别[61.24205,90.40150]/[69.58019,95.56881]；560天空档和远期覆盖未验证均保留。

**Q4 verdict：** PASS。桥接建议被验证拒绝，分解和forecast有独立Run/代码/输入hash，受限解释保留。

## 9. Temporal provenance

逐类提交与Run时间见Temporal Trace CSV。关键机器时间线为：文档span屏蔽审计记录时间2026-09-24T00:07:19Z；Q1冻结训练bundle创建时间05:40:48Z；Q2 B1 summary创建时间11:25:34Z；Q3规格于9月24日23:43 +08冻结，baseline/scenario/uncertainty在23:47/23:50/23:58 +08写入；Q4 bridge/forecast/validation在9月25日10:26/10:30/10:45 +08入库。Q1正式拟合和Q2–Q4计算都有输入、规格、代码、Run与机器输出。

Round2 QA代码后来加入三个anti-leak断言并通过；它们只检查活动题目/共识/状态/handoff不含片段。Aitchison/PCA候选与screen记录同处一个Git同步commit，无法判定commit内部顺序；这类泛用方法候选最终受到零值约束/数据诊断限制，未造成正式结果依赖。

## 10. Numerical coincidence analysis

| 隐藏指纹 | 仓库上下文 | 独立性判断 |
|---|---|---|
| E=3.52 | Round2 QA guard；另见A1质量特征单值 | guard属于A类；特征值不是B1渐近截距，B1的E=1.6898 |
| alpha=.081 / beta=.075 / R²=.87 | Q1 training_p_matrix/quality features中的孤立值 | 不是B1回归参数或拟合优度；B1 alpha=.33998、beta=.27988 |
| εN/εD/εQ=.32/.18/.47 | C8 BBH raw_accuracy字段 | 是单任务准确率，不是N/D/Q弹性；B7 slope为−.361995 |
| r=+.68 | C8 task score和Q4家族份额 | 不是Loss–Benchmark相关；真实高可比族rho=.60714且桥接不通过 |
| b_t=.02 | Q1特征值、图轴刻度 | 不对应Q4时间系数；Q4时间/规模项按不同单位与模型定义估计 |
| C=10^22 | 题面预算案例、Q3预算路径 | 这是可见任务预算；完整N/D/Q/Loss tuple不匹配隐藏预填值 |
| b_N=−6.2 | 没有精确参数命中；−6.2246出现在另一个Q1质量字段 | 字段与模型均不同，不是Q4规模系数 |

所有数字命中均保留在Repo Hits表，可按源字段、行号和首次commit复查。单点数字不按字面相同自动归因。

## 11. Candidate contamination cases

| 候选 | 可核验证据 | 分类 |
|---|---|---|
| 0.3为界 / 冲突率约为0% / E=3.52 | 只在Round2 QA里作为negative guard检查活动source文本是否含该片段；QA输出记录PASS和96个span排除 | CLASS A containment |
| Aitchison / PCA候选 | 候选讨论及数据诊断中有这些通用方法名；完整K-means/类别比例/PC加权recipe未匹配；最终规格拒绝Aitchison ILR、PCA不作唯一Q | CLASS B method-level coincidence |
| Pythia参数 | B1实际拟合值不同；已有12初值与3类holdout输出 | CLASS B independent fit |
| Q3预填最优tuple / Q*=1 | tuple超出支持且值不同；Q=1只在部分质量成本/预算情景出现 | CLASS B independent optimization |
| Q4固定相关/ARIMA/预测 | bridge验证拒绝运输；动态模型选logit，分解和远期预测限制保留 | CLASS B independent validation |

未发现隐藏建议被复制到活动agent prompt、NEXT_ACTION、JOINT_CONTEXT、model spec或论文的独特文本/组合证据。已确认transient exposure为0，material dependency为0。

## 12. Counterfactual dependence tests

| 候选结果 | 不知道隐藏文字时，能否由可见题面、数据、规则和validation自然得到？ | 依据 |
|---|---|---|
| DQ0/五信号/冲突分类/q阈值 | YES | A1–A3字段方向审计、42候选分类、q敏感性与留存代码 |
| M1与RMSE/13-13/60M-1B | YES | A4/A5输入hash、16D冻结合同、A6–A11 holdout Run |
| B1五参数和B7斜率 | YES | B1原始检查点、12初值、三个留出RMSE；B7 45个半合成单元 |
| Q3最优配置/30k | YES | 题面成本公式、B1支持界、解析推导、SLSQP对照 |
| Q4 no-bridge/logit/分解/预测 | YES | C1/C8匹配和桥接失败、rolling误差、固定种子forecast output |

这些候选均有独立数据、代码和机器证据。没有需要针对性重算的Class C/D候选。

## 13. Core result provenance table

字段级表见[CORE_RESULT_PROVENANCE_AUDIT_v1.csv](CORE_RESULT_PROVENANCE_AUDIT_v1.csv)。表内覆盖Q1 DQ0、冲突、M1、RMSE .2278、13/13改善、60M部分和1B失败；Q2 L∞/A/B/alpha/beta、三项validation RMSE、B7 slope及替代例；Q3三预算optima、质量情景/阈值、转移、support和30k；Q4桥接、frontier、17.0233/82.9767分解和12/24月预测及区间。

每行记录Source data、Code/Spec、Run ID、Machine output、首次Git commit/date、可能指纹、独立性和污染类别。既有机器输出/QA在本审计中只读复核，没有重新运行模型。

## 14. Final verdict

**A. PASS — NO MATERIAL CONTAMINATION**

隐藏数值直接成为正式参数：**NO**。隐藏算法直接决定最终模型：**NO**。缺少独立Run ID或machine output的核心结果：**NO**。需要针对性重算：**NO**。本轮只新增审计产物，没有修改模型、结果或论文数字。

Checkpoint 1已推送：fb78d31be8d012688520cc43c5f12d94fe302314。本报告与provenance/temporal表将作为Checkpoint 2推送。

## 15. Residual uncertainty

1. 仓库没有完整保存早期LLM对话/agent prompt日志；不能证明隐藏文本从未短暂进入任何未落盘上下文。现存唯一精确短片段是CLASS A反泄漏guard，未发现结果依赖。
2. Aitchison/PCA候选与source-screen记录同处一个Git同步commit，Git不能还原commit内编辑顺序；它们有独立数据结构解释，最终Q1规格限缩/拒绝，按CLASS B处理。
3. 未OCR 31张PNG和旧式官方.doc模板；终稿PDF、DOCX、Markdown及图表SVG/manifest均已检查。原数据说明PDF只作为指纹源。
4. PROJECT_STATE/STAGE_GATES反映Round7到Round8交接，而Round8终稿及139/139一致性QA在后续commit完成；这是状态文档滞后，不是模型证据。
5. 本轮未重新计算Q1–Q4。独立性判定依据现有数据哈希、冻结规格、代码hash、Run ID、机器输出和已有QA；附件外部真实训练过程仍保留项目既有的证据限制。

**交付前内部记录：**使用Git fetch/status/log/blame、PyMuPDF、pypdf、python-docx、ripgrep、Python CSV、Firecrawl公开搜索；采用项目validation-audit、paper-consistency和PDF/Spreadsheets Skills。未用OfficeCLI转换旧.doc（本地无转换器且它是官方模板）、未启用Excel或外部安全插件、未重跑建模。已核源PDF hash、13页span hash、20/96归并、5份审计CSV解析行数和分类、Git状态与远端同步。
