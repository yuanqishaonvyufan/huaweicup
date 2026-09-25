"""Create explicit page-level transfer decisions from the audited PDF inventory."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "10_review/REFERENCE_FIGURE_TABLE_INVENTORY_v1.csv"
OUT = ROOT / "10_review/REFERENCE_TRANSFER_DECISIONS_v2.csv"
SECTION = {"Overall": "总体分析/符号说明", "Q1": "5.1", "Q2": "5.2", "Q3": "5.3", "Q4": "5.4", "Validation": "6.1", "Sensitivity": "6.2", "Appendix": "附录"}
FIELDS = ["Reference item ID", "Reference page", "Reference section", "Idea", "Transfer type", "Local evidence needed", "Local evidence found?", "Decision", "Reason"]


def add(rows, item, page, section, idea, transfer, needed, found, decision, reason):
    rows.append(dict(zip(FIELDS, [item, page, section, idea, transfer, needed, found, decision, reason])))


def main() -> None:
    with INVENTORY.open(encoding="utf-8-sig", newline="") as stream:
        inventory = list(csv.DictReader(stream))
    rows = []
    flow = {1, 2, 7, 12, 16}
    for entry in inventory:
        fig = entry["Kind"] == "Figure"
        number = int(entry["Figure No."] if fig else entry["Table No."])
        kind = "F" if fig else "T"
        question = entry["Question"]
        transfer = "STRUCTURE" if fig and number in flow or not fig and number in {1, 11} else "VISUALIZATION" if fig else "STYLE"
        needed = entry["Local source"]
        found = "YES" if (ROOT / needed).exists() else "PARTIAL"
        if fig and number in {3, 5, 11, 13, 20}:
            decision = "INDEPENDENTLY_TEST_PENDING"
            reason = "需按本地原始数据另立补充Run；只转图形问题类型，不转参考数值"
        elif fig and number in flow:
            decision = "ADOPT_STRUCTURE"
            reason = "可按本项目实际证据链重绘；参考流程的可靠桥接等节点不直接采用"
        else:
            decision = "ADAPT_PRESENTATION"
            reason = "已有对应结果或设计空间；只用本地验证数据，按证据边界重写图题/表题"
        add(rows, f"{kind}{number:02d}", entry["Page"], SECTION[question], entry["Title"], transfer, needed, found, decision, reason)

    extras = [
        ("S01", "4,7–24", "5.1–5.4", "每问先具体分析、模型准备、模型建立、模型求解", "STRUCTURE", "四问冻结规格及结果", "YES", "ADOPT_STRUCTURE", "v5分问重组，但不强造额外模型"),
        ("S02", "8–9,12–13,16–17,20–21", "5.1.2–5.4.2", "模型准备解释数据、变量、量纲与候选方法", "STYLE", "本地候选比较与单位审计", "YES", "ADOPT_STYLE", "补理由和适用范围，不照抄句子"),
        ("S03", "9,13,17,21", "5.1–5.4", "逐问用方法比较表说明取舍", "STYLE", "Q1 M0/M1/M2、Q2基准、Q3求解、Q4动态比较", "YES", "ADAPT_PRESENTATION", "只列已运行的方法与实测验证表现"),
        ("S04", "11–12,15–16,19–20,23–24", "5.1.4–5.4.4", "结果结合数值、图形和机制解释", "STYLE", "正式运行与图形清单", "YES", "ADOPT_STYLE", "每个核心结果写现象、机制、后续意义"),
        ("S05", "24–25", "6.1/6.2", "集中展示误差与灵敏度", "STRUCTURE", "四问验证报告", "YES", "ADOPT_STRUCTURE", "本地检验更丰富，明确非同一误差量尺"),
        ("S06", "25–26", "7/8", "优缺点和改进推广对应具体数据限制", "STRUCTURE", "Q1–Q4限制和未来数据条件", "YES", "ADOPT_STRUCTURE", "保留负结果，不写空泛优点或无条件推广"),
        ("S07", "29", "附录", "代码、结果、图形按清单组织", "STRUCTURE", "本项目代码入口和Result ID", "YES", "ADAPT_PRESENTATION", "附件目录结构可借鉴；不暴露本机账号路径"),
        ("M01", "9–10", "5.1", "PCA作为唯一综合质量主轴", "METHOD CANDIDATE", "Q1 DQ1与多维表示比较", "YES", "REJECT_METHOD_UPGRADE", "本地PC1只解释约48.11%，冻结主表示仍为多维"),
        ("M02", "14–16", "5.2", "统一可运输质量因子", "METHOD CANDIDATE", "同运行Q-N-D-p-Loss", "NO", "REJECT_METHOD_UPGRADE", "本地B7仅半合成；跨来源量尺与同运行键缺失"),
        ("M03", "21–23", "5.4", "可靠Loss–Benchmark数值桥接", "METHOD CANDIDATE", "跨规模及跨家族留出", "YES", "REJECT_METHOD_UPGRADE", "本地桥接检验失败，仅可转失败诊断的展示方式"),
        ("R01", "2,11–12", "摘要/5.1", "参考质量分、领域排名与配比最优比例", "RESULT — FORBIDDEN", "本地Q1原始运行", "YES", "REJECT_RESULT_TRANSFER", "参考PCA分和配比最优不进入本项目"),
        ("R02", "2,15–17", "摘要/5.2", "参考规模律系数、质量因子和跨族拟合指标", "RESULT — FORBIDDEN", "本地Q2 Run与验证", "YES", "REJECT_RESULT_TRANSFER", "所有系数与R²/RMSE均须从本地独立估计"),
        ("R03", "2,19–20", "摘要/5.3", "参考最优N/D/Q、预算阈值与平台解释", "RESULT — FORBIDDEN", "本地Q3预算路径", "YES", "REJECT_RESULT_TRANSFER", "参考配置与真实产业阈值推断不采用"),
        ("R04", "3,22–24", "摘要/5.4", "参考规模/技术贡献比例、可靠桥接与未来分数", "RESULT — FORBIDDEN", "本地Q4受限结果", "YES", "REJECT_RESULT_TRANSFER", "本地桥接失败、比例反号、远外推；参考结论不适用"),
        ("R05", "24–26", "6–8", "参考误差、灵敏度数值和优劣判断", "RESULT — FORBIDDEN", "本地四问验证报告", "YES", "REJECT_RESULT_TRANSFER", "仅借分类和写法，不借任何检测数值与判断"),
    ]
    for row in extras:
        add(rows, *row)
    with OUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"rows={len(rows)} figures_tables={len(inventory)} structures=7 methods=3 forbidden=5")


if __name__ == "__main__":
    main()
