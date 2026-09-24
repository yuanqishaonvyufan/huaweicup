# Modeling Phase 1 Round 4 QA — 2026-09-24

**Verdict: PASS.** 这是 Round 4 既有产物的只读核查，不是新的模型训练或留出验证，也不构成 Gate 2 PASS。机器记录为 [QA JSON](MODELING_PHASE1_R4_QA_20260924.json)；执行命令：`python -X utf8 04_code/modeling_phase1/round4_qa.py`。QA 脚本只用 Python 标准库，核查原件/产物哈希，并从已保存逐行预测独立复算关键误差。脚本及完整检查摘要的 SHA-256 记录于机器 JSON。

## 断点与修复

接管前 Round 4 训练、验证、Q1 文字包、五张表、四张图与 Gate 2 v1 包已存在；正式 QA 报告不存在。首次运行 QA 仅发现四张候选图未进入 Figure Registry；补登后最终机器结果 `PASS / failures=[]`。同时补全 Results Registry 的模型选择条目、把 B1 活跃裁决的 Alert 引用改至 v4，并用 Gate 2 v1.1 替代 v1 中“QA 已完成”的过早措辞。旧 v1 包保留为历史。

本次新发现的收口问题：**P0=0，P1=1，P2=5**，均已作文件级修复或由新版本取代。P1 是缺失 Round 4 QA；P2 分别是 Results Registry 漏登记模型选择量、Figure Registry 漏四图、B1 Alert 引用停在 v3、Gate 2 v1 对 QA 的过早声明及相关总览文件仍留旧阶段、B1 双层裁决到预冻结合同的相对链接少一级目录。此计数不覆盖 Issue Tracker 中原有的 P1/DA 待办，也不把 Gate 2 外部审查计为完成。

## 核查证据

| 门槛 | 检查与结论 |
|---|---|
| 输入与映射 | 原始清单与实际 A4/A5、A6–A11 文件 SHA-256 全部相符；A6/A8 配比字节哈希相同，只算一份 p 支持。质量审计五个输出文件哈希相符，22 项角色合计 22。 |
| 训练冻结与泄漏 | `EXP-Q1-PRESP-TRAIN-R4-20260924-v1` 的 bundle SHA-256 同时匹配训练指标和有效验证 JSON；训练脚本仅有两个 `pd.read_csv`，路径为 A4/A5，未出现 A6–A11 验证 Loss 路径；`A6_A11_loss_read=false`；bundle 文件时间早于有效验证。此为代码/产物/时间一致性证据，不声称能重建旧电脑全部交互历史。 |
| 参数与模型选择 | 16 自由坐标满秩，条件数 45.4356；M1/M2 五折分数分别 0.750417/0.749715，M2 α=0.01；M3 残差触发为 false，冻结包仅含 M0/M1/M2。训练/验证合同、预注册和脚本哈希一致。 |
| 失败运行隔离 | `VAL-Q1-PRESP-A6A11-R4-20260924-v1` 因 JSON NumPy int64 序列化异常失败，五个 CSV 留在 `failed_validation_v1/`，根目录无 v1 验证 JSON；Experiment Registry 记为 `FAILED — NO VALIDATION DECISION`。有效结果只取 v2。 |
| 有效留出 | `VAL-Q1-PRESP-A6A11-R4-20260924-v2` 的五个输出 CSV 哈希/行数与 JSON 相符。由 576 行已存预测逐行复算 R0 定义、各规模各模型 R0 RMSE、中心化 R0 比以及 117 个逐域 RMSE，均与机器结果一致。A7/1M M1 0.227765、M0 0.284615，13/13 域改善；M1 两层 bootstrap 上界均小于 0。 |
| M2 与跨规模 | 从逐行预测复算 M1−M0、M2−M1 的 R0 与标准化逐域成对 MSE 点差；M2 相对 M1 的两层 bootstrap 区间跨零，不升级。60M 中心化 R0 比 0.887574，1B 为 3.108487；跨规模绝对预测资格为 false，1B 失败已明示。 |
| 支持域 | 复核 1M/60M 各 2 IN、252 NEAR、2 OUT，1B 为 15/46/3；由固定 q95/q99 阈值、凸包标签和逐行近邻距离重建支持类别；1M 凸包严格覆盖 2/256。凸包 LP 本身未在本次重新求解，原验证产物哈希已锁定。 |
| 质量与接口 | Full-22 角色为 CORE 5、SECONDARY 2、SENSITIVITY 12、UNKNOWN 1、REDUNDANT 2；语义冲突确认 0，Q2 可独立估计质量变量 TYPE E=0；质量闭合运行未读取 Loss。 |
| 表图与登记 | 四图 PDF/PNG、五表、各自源 CSV 与脚本 SHA-256 均和 manifest 相符；PNG 边长均至少 1200 px，四张预览已人工查看无明显裁切。Figure Registry 已登记四图；Results Registry 仅给 CHECKED/CANDIDATE，VALIDATED FINAL 仍 0。 |

## QA 边界

本 QA 不重新运行五折、bootstrap 随机抽样、凸包线性规划或 A6–A11 验证脚本；针对既有机器结果、代码合同、输入/输出哈希和逐行输出做交叉核查，并核对本轮活跃文档的本地链接。A7 的 1M 证据主要来自 NEAR_SUPPORT，OUT 仅两点；60M 是部分形状转移，1B 迁移失败。Q1 是 **PROVISIONAL FINAL CANDIDATE / READY FOR GATE 2 PRE-REVIEW**，无 ACTIVE FINAL MODEL 或 VALIDATED FINAL RESULT。B1 外部来源 Alert v4 仍 PARTIALLY RESOLVED，附件内 B 级受限入口待 Gate 2，Round 5 未启动。
