# FIGURE_REGISTRY

Round 4 有四张已生成并核来源哈希的 Q1 候选图；Gate 2 已接受其受限 Q1 证据用途，仍保留论文候选状态。PDF 向量文件与 PNG 预览、脚本哈希见 `03_models/modeling_phase1/q1/round4/figures/figure_manifest.json`。正式嵌入仍须按论文版面检查中文字形和实际尺寸。

| Figure ID | Question | Purpose / claim | Source Run | Source data | Result ID | Generation script | Filename | Axes / unit | Limitation | Paper location | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FIG-Q1-R4-001 | Q1 | 比较五核心描述坐标的域差与扩展对照 | AUDIT-Q1-QUALITY-CLOSURE-R4-20260924-v1 | `Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv` | CAND-Q1-R4-QUAL-001 | `04_code/modeling_phase1/round4_q1_figures.py` | `figures/FIG-Q1-R4-001_core_domain_profile.pdf`；同名 PNG | 横轴五核心语义；纵轴来源域和 n；颜色为 A1 参考平均分位，0–1 | 同标注体系对照，不是独立质量干预；DQ0 非真 Q | 正文候选 | CHECKED PAPER CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE |
| FIG-Q1-R4-002 | Q1 | 显示 A7/1M M1 对 M0 的 13 域 RMSE 比，检查是否有域恶化 | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | `P_RESPONSE_DOMAIN_VALIDATION_v2.csv` | CAND-Q1-R4-VAL-001；CAND-Q1-R4-VAL-002 | `04_code/modeling_phase1/round4_q1_figures.py` | `figures/FIG-Q1-R4-002_domain_validation_gain.pdf`；同名 PNG | 横轴 M1/M0 RMSE 无量纲比；纵轴 13 域；1 为无改善 | 仅 1M 同尺度，主要 near-support；非因果效应 | 正文候选 | CHECKED PAPER CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE |
| FIG-Q1-R4-003 | Q1 | 对照 1M/60M/1B 的中心化误差比，突出 1B 迁移失败 | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | `P_RESPONSE_VALIDATION_METRICS_v2.csv` | CAND-Q1-R4-TRANSFER-001 | `04_code/modeling_phase1/round4_q1_figures.py` | `figures/FIG-Q1-R4-003_scale_transfer_failure.pdf`；同名 PNG | 横轴规模与 n；纵轴 M1/M0 中心化 RMSE 比，无量纲 | 跨规模只检相对配比形状，不代表绝对 Loss 预测 | 正文候选 | CHECKED PAPER CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE |
| FIG-Q1-R4-004 | Q1 | 显示经验凸包和训练近邻的验证配比分层 | VAL-Q1-PRESP-A6A11-R4-20260924-v2 | `P_SUPPORT_VALIDATION_ROWS_v2.csv` | CAND-Q1-R4-SUPPORT-001 | `04_code/modeling_phase1/round4_q1_figures.py` | `figures/FIG-Q1-R4-004_support_strata.pdf`；同名 PNG | 横轴配比组数；纵轴规模；堆叠 IN/NEAR/OUT | A6/A8 同一 p；经验支持不等于现实供给或最终 Q3 域 | 附录候选 | CHECKED PAPER CANDIDATE — GATE2 ACCEPTED — PROVISIONAL USE |

图形宣称、来源、SHA-256 与 PNG 分辨率由 Round 4 QA 检查；四张 PNG 亦已人工查看无明显裁切。论文最终位图参考至少 300 dpi；当前优先采用 PDF 向量文件。
