"""Account for all 43 registered local Result IDs in the final v5 paper."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "10_review/LOCAL_EVIDENCE_MASTER_INVENTORY_v2.csv"
OUT = ROOT / "10_review/paper_v5/FINAL_LOCAL_RESULT_COVERAGE_v2.md"

APPENDIX = {
    "CAND-Q1-DQ-R3-001": "首主成分只解释五维结构，详细数值列于附录D；不升级为质量主分。",
    "CAND-Q1-DQ-R3-002": "3/9分层复现属于表示稳定性诊断，详细数值列于附录D。",
    "CAND-Q1-RSP-R3-001": "R2首主成分为训练内探索轴，不能替代十三域留出响应；列于附录D。",
    "CAND-Q1-RSP-R3-002": "R0/R2排序差异仅训练内观察，列于附录D而不作主预测结果。",
    "CAND-Q1-RSP-R3-003": "域对负相关仅训练内异质性，列于附录D，不声明因果冲突。",
}
PARTIAL = {
    "CAND-Q1-R4-SUPPORT-001": "正文及附录D解释支持分层；域外配比数量过少，无可报告的单独稳定误差。",
    "CAND-Q2-R5-EXT-001": "只报B2/B4/B5来源内中心化形状比；共同绝对Loss量尺未建立。",
    "CAND-Q2-R5-EXT-002": "B9/B10为估算外推范围说明，缺少可作为外部验证的真实Loss。",
    "CAND-Q2-R5-MIX-001": "A来源局部配比证据进入条件接口；跨来源系数及较大规模运输未识别。",
    "SCEN-Q3-R6-MIX-001": "513候选与3域恶化进入正文，但现实供应和B1量尺运输未核实。",
    "Q4-R7-008": "旧参数趋势非正导致三情景重合；只作为失败的代理说明，不复用退化图。",
}
NO_FIGURE_TABLE = {
    "CAND-Q1-R4-SUPPORT-001", "CAND-Q2-R5-EXT-001", "CAND-Q2-R5-EXT-002",
    "CAND-Q2-R5-MIX-001", "SCEN-Q3-R6-MIX-001", "Q4-R7-008",
}
SECTIONS = {"Q1": "5.1、附录D", "Q2": "5.2、6.1、6.2", "Q3": "5.3、6.1、6.2", "Q4": "5.4、6.1、6.2"}


def main() -> None:
    with INVENTORY.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = [r["result_id"] for r in rows]
    assert len(rows) == len(set(ids)) == 43
    assert set(APPENDIX | PARTIAL) <= set(ids)
    counts = Counter()
    ft = 0
    lines = ["# Final local result coverage v2", "",
             "以最新版登记的43个不同 Result ID 为分母。FULL、PARTIAL、APPENDIX、NOT INCLUDED 是互斥的主要呈现位置；Figure/Table支持为可与这些类别重叠的独立计数。覆盖只表示论文呈现，不改变登记的证据等级或模型状态。", "",
             "|Result ID|问题|v5主要覆盖|Figure/Table支持|论文位置|仍受限或未充分进入原因|",
             "|---|---|---|---|---|---|"]
    for row in rows:
        rid, question = row["result_id"], row["question"]
        if rid in APPENDIX:
            category, reason, location = "APPENDIX", APPENDIX[rid], "附录D；5.1仅概述"
        elif rid in PARTIAL:
            category, reason, location = "PARTIAL", PARTIAL[rid], SECTIONS[question]
        else:
            category, reason, location = "FULL", "已按原证据等级呈现；不外推为更强结论。", SECTIONS[question]
        support = rid not in NO_FIGURE_TABLE
        counts[category] += 1
        ft += int(support)
        lines.append(f"|{rid}|{question}|{category}|{'是' if support else '否'}|{location}|{reason}|")
    assert counts == {"FULL": 32, "PARTIAL": 6, "APPENDIX": 5}
    assert ft == 37
    lines += ["", "## 汇总", "",
              f"- 正文 FULL：{counts['FULL']}/43。",
              f"- 正文 PARTIAL：{counts['PARTIAL']}/43。",
              f"- Figure/Table 支持：{ft}/43（交叉计数，不能与上列相加）。",
              f"- Appendix 为主要详细位置：{counts['APPENDIX']}/43。",
              "- 未进入：0/43；因此没有未进入项需要列出排除理由。探索性结果仅在附录D保留，并标明训练内性质。", "",
              "证据边界：43项包含训练内探索、受限候选、半合成情景与Q4受限验证结果，不是43个无条件最终结论。v5没有改变原始结果、旧证据映射历史记录或冻结参数。"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print({"results": len(rows), "categories": dict(counts), "figure_table_support": ft})


if __name__ == "__main__":
    main()
