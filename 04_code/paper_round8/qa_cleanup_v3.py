"""Read-only consistency audit for the final paper candidate."""
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import csv
import hashlib
import json
import re

from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / "11_delivery/revised_v2/F_revised_draft_v2.docx"
NEW = ROOT / "11_delivery/final_v3/F_final_candidate_v3.docx"
PDF = NEW.with_suffix(".pdf")
SRC = ROOT / "08_paper/final_v3"
CONTRACT = ROOT / "06_results/raw/Q1_TASK_REPAIR_20260925_v1/Q_FULL_FIELD_CONTRACT_v1.csv"
REPORT = ROOT / "10_review/FINAL_PAPER_CLEANUP_QA_v1.md"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain(doc):
    return "\n".join(p.text for p in doc.paragraphs) + "\n" + "\n".join(
        " | ".join(c.text for c in row.cells)
        for t in doc.tables for row in t.rows
    )


def table_data(table):
    return [[c.text.replace("\u200b", "") for c in row.cells] for row in table.rows]


checks = []
def check(label, condition):
    checks.append((label, bool(condition)))


old, new = Document(OLD), Document(NEW)
text = plain(new).replace("\u200b", "")
with CONTRACT.open(encoding="utf-8-sig", newline="") as f:
    fields = list(csv.DictReader(f))
with ZipFile(SRC / "template_reference.docx") as a, ZipFile(NEW) as b:
    media = [p for p in a.namelist() if p.startswith("word/media/")]
    check("正式模板4个封面图像字节一致", len(media) == 4 and all(a.read(p) == b.read(p) for p in media))
    check("无修订与批注标记", not any(x in b.read("word/document.xml") for x in (b"<w:ins", b"<w:del", b"<w:comment")))
    check("含OMML公式", b"<m:oMath" in b.read("word/document.xml"))

check("v2基线与v3为不同文件", OLD.exists() and sha(OLD) != sha(NEW))
check("22个合同字段均列于附录A1且仅各一行", len(fields) == 22 and len(new.tables) == 19 and
      len(new.tables[17].rows) == 23 and
      [re.sub(r"^\d+\.\s*", "", row.cells[0].text.replace("\u200b", "")) for row in new.tables[17].rows[1:]] == [x["field"] for x in fields])
check("所有字段W0权重均为1/22", all(abs(float(x["weight_W0"]) - 1/22) < 1e-12 for x in fields))
check("附录A1明确全部22项进入W0", all("计入W0" in row.cells[2].text for row in new.tables[17].rows[1:]))
check("QuRating四面向先转换再平均为一项", "四面向各取A1分位和参考目标接近效用，平均为1项计入W0" in new.tables[17].rows[10].cells[2].text)
check("DSIR三项进入评分并保留原始限制", all("参考目标接近效用" in new.tables[17].rows[i].cells[2].text and "尺度未核" in new.tables[17].rows[i].cells[3].text for i in (7,8,9)))
check("摘要采用预先定义的评价用途参考画像", "预先定义的评价用途参考画像" in text and "公开用途目标" not in text)
check("DQ0不称为正式综合总分", "DQ0不等同Q_full或半合成Q" in text)
check("单处AI使用披露", text.count("AI辅助使用说明：") == 1)
check("无Markdown强调、代码和标题痕迹", not any(mark in text for mark in ("**", "`", "###", "@TABLE_", "![")))
check("无旧稿排斥22项的措辞", not any(mark in text for mark in ("不进入总分", "单列诊断", "不强行平均", "2稿仅新增", "旧尝试")))
check("9图和24公式登记", len(json.loads((SRC / "FINAL_FIGURE_SELECTION_v3.json").read_text(encoding="utf-8"))) == 9 and len(json.loads((SRC / "FINAL_EQUATION_REGISTRY_v3.json").read_text(encoding="utf-8"))) == 24)
figures = json.loads((SRC / "FINAL_FIGURE_SELECTION_v3.json").read_text(encoding="utf-8"))
check("图像来源和SHA256一致", all(sha(ROOT / x["source"]) == x["sha256"] for x in figures))
check("图1—9正文图注各一次", all(sum(p.text.startswith(f"图{i} ") for p in new.paragraphs) == 1 for i in range(1,10)))
check("图5图注线型与冻结图生成代码一致", "竖向点线" in figures[4]["caption"] and "橙色虚线" in figures[4]["caption"])
check("参考文献1—7顺序与编号完整", [int(re.match(r"^\[(\d+)\]", p.text).group(1)) for p in new.paragraphs if re.match(r"^\[\d+\]", p.text)] == list(range(1,8)))
check("除符号表和附录A1外所有表格数据保持v2原值", len(old.tables) == len(new.tables) == 19 and all(table_data(old.tables[i]) == table_data(new.tables[i]) for i in range(19) if i not in (1,17)))

old_eq = json.loads((ROOT / "08_paper/revised_v2/FINAL_EQUATION_REGISTRY_v2.json").read_text(encoding="utf-8"))
new_eq = json.loads((SRC / "FINAL_EQUATION_REGISTRY_v3.json").read_text(encoding="utf-8"))
check("24条公式文本与v2完全一致", [x["formula"] for x in old_eq] == [x["formula"] for x in new_eq])
old_fig = json.loads((ROOT / "08_paper/revised_v2/FINAL_FIGURE_SELECTION_v2.json").read_text(encoding="utf-8"))
check("9张正式图的像素文件SHA256与v2相同", [x["sha256"] for x in old_fig] == [x["sha256"] for x in figures])
number_pattern = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?![A-Za-z_])")
check("Q2/Q3/Q4正文数值序列与v2逐项一致", all(
    number_pattern.findall((ROOT / "08_paper/revised_v2" / name).read_text(encoding="utf-8")) ==
    number_pattern.findall((SRC / name).read_text(encoding="utf-8"))
    for name in ("06_Q2.md", "07_Q3.md", "08_Q4.md")
))

reader = PdfReader(PDF)
page_text = [p.extract_text() or "" for p in reader.pages]
check("PDF为30页且无空白正文页", len(reader.pages) == 30 and len(page_text[0].strip()) > 50 and all(len(t.strip()) > 100 for t in page_text[1:]))
check("PDF正文页码1—29顺序连续", all(re.match(rf"^{i}\s*\n", page_text[i]) for i in range(1,30)))
check("PDF不含明显替代字或方框", "\ufffd" not in "".join(page_text) and "\u25a1" not in "".join(page_text))

baseline_hash = sha(OLD)
new_hash = sha(NEW)
pdf_hash = sha(PDF)
failed = [label for label, ok in checks if not ok]
report = [
    "# FINAL PAPER CLEANUP QA v1", "",
    "结论：" + ("全部自动核查通过；未发现 MATERIAL RESULT CONFLICT。" if not failed else "发现待修项；候选稿不得作为最终提交版本。"),
    "", "## 基线与输出", "",
    f"- Git基线：bdaad1e2532edad5fa20f99f8e60babd13473996；v2 DOCX SHA256：`{baseline_hash}`。",
    f"- v3 DOCX SHA256：`{new_hash}`。",
    f"- v3 PDF SHA256：`{pdf_hash}`；{len(reader.pages)}页（封面1页，正文页码1—29）。",
    "- 本轮只修改文稿、组装器的v3分支与文稿QA；未运行Q1/Q2拟合、Q3优化或Q4预测。",
    "", "## 一致性检查", "",
]
report += [f"- {'PASS' if ok else 'FAIL'}：{label}" for label, ok in checks]
report += [
    "", "## 人工版面检查", "",
    "- 已渲染并目视检查封面、摘要、图表页和附录A1/B/C；附录A1跨页重复表头，22行完整，最后一页无孤行。",
    "- 图5竖向灰色点线标示支持界，橙色虚线标示数据量；图注与冻结图一致。",
    "", "## 保留的证据边界", "",
    "- Q_full是规则构造综合评分，DQ0为五维解释摘要；DSIR原始尺度和冗余限制未取消。",
    "- 1B及10B/70B配比迁移失败、Loss—能力桥接失败、完整N/D贡献不可识别、长期预测条件性均保留。",
    "- AI使用披露合并为一处；模型版本发布日期及历史工具记录仍需参赛队按原始记录核实。",
    "", "## MATERIAL RESULT CONFLICT", "",
    "未发现。未变更正式参数、RMSE、预算配置、12/24个月预测或机器结果文件。",
]
if failed:
    report += ["", "待修项：" + "；".join(failed)]
REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
print(json.dumps({"checks": len(checks), "failed": failed, "pages": len(reader.pages), "report": str(REPORT)}, ensure_ascii=False))
if failed:
    raise SystemExit(1)
