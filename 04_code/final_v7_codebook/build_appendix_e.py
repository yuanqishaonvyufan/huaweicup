"""Assemble the concise Appendix E from core snippets and source manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUTLINE = {
    "E1": ("E.1 问题一", [
        ("q1_quality_score.py", "计算22项质量信号的统一效用、Q_full、W1和DQ0。",
         ["04_code/paper_round8/q1_task_repair.py", "04_code/modeling_phase1/round3_q1_descriptive.py"]),
        ("q1_mixture_model.py", "构造17域Helmert正交坐标，并拟合13个响应域的M1配比模型。",
         ["04_code/modeling_phase1/round4_train_p_response.py", "04_code/modeling_phase1/round4_validate_p_response.py"]),
    ]),
    "E2": ("E.2 问题二", [
        ("q2_scaling_fit.py", "拟合五参数N–D标度律，并执行轨迹留出、前向和N–D分块验证。",
         ["04_code/modeling_phase2/round5_fit.py", "04_code/modeling_phase2/round5_prepare.py"]),
    ]),
    "E3": ("E.3 问题三", [
        ("q3_resource_allocation.py", "计算给定算力预算下的N–D最优分配，并求解质量情景扩展。",
         ["04_code/modeling_phase3/round6_core.py", "04_code/modeling_phase3/round6_baseline.py", "04_code/modeling_phase3/round6_scenarios.py"]),
    ]),
    "E4": ("E.4 问题四", [
        ("q4_frontier_forecast.py", "构造滚动能力前沿，比较Loss桥接方法，拟合动态预测并计算条件放缓情景。",
         ["04_code/modeling_phase4/round7_models.py", "04_code/modeling_phase4/round7_forecast.py", "04_code/paper_round8/q4_task_repair.py"]),
    ]),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prompt_text() -> str:
    return (HERE / "prompts" / "ALL.md").read_text(encoding="utf-8").strip()


def snippet_records(key: str) -> list[dict]:
    _, modules = OUTLINE[key]
    rows = []
    for filename, purpose, sources in modules:
        code_path = HERE / "appendix_e" / filename
        source_hashes = {path: sha(ROOT / path) for path in sources}
        rows.append({
            "filename": filename,
            "purpose": purpose,
            "code": code_path.read_text(encoding="utf-8"),
            "code_sha256": sha(code_path),
            "sources": source_hashes,
        })
    return rows


def render_markdown(key: str) -> None:
    heading, _ = OUTLINE[key]
    rows = snippet_records(key)
    out = [f"# 附录 E · {heading}", "",
           "以下是论文中实际使用的核心函数。完整程序、数据处理、验证、作图和运行记录见本目录相应问题的完整源码支撑材料。", ""]
    for row in rows:
        out += [f"## {row['filename']}", "", f"功能：{row['purpose']}", "",
                "支撑源程序："]
        out += [f"- `{path}`（SHA-256 `{digest}`）" for path, digest in row["sources"].items()]
        out += ["", "```python", row["code"].rstrip(), "```", ""]
    (HERE / f"{key}.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
    manifest = [{k: v for k, v in row.items() if k == "filename" or k == "purpose" or k == "code_sha256" or k == "sources"} for row in rows]
    (HERE / f"{key}_manifest.json").write_text(
        json.dumps({"section": heading, "modules": manifest}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )


def set_east_asia(style, name: str) -> None:
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.rFonts
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    fonts.set(qn("w:eastAsia"), name)


def build_docx(target: Path) -> None:
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11)
    section.top_margin, section.bottom_margin = Inches(.68), Inches(.65)
    section.left_margin, section.right_margin = Inches(.75), Inches(.75)
    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = "Microsoft YaHei", Pt(10.5)
    set_east_asia(normal, "Microsoft YaHei")
    normal.paragraph_format.space_after = Pt(6)
    for name, size in (("Title", 20), ("Heading 1", 15), ("Heading 2", 11.5)):
        style = doc.styles[name]
        style.font.name, style.font.size = "Microsoft YaHei", Pt(size)
        style.font.color.rgb = RGBColor(25, 49, 77)
        set_east_asia(style, "Microsoft YaHei")
        style.paragraph_format.keep_with_next = True
    code_style = doc.styles.add_style("AppendixCode", WD_STYLE_TYPE.PARAGRAPH)
    code_style.font.name, code_style.font.size = "Consolas", Pt(8.4)
    code_style.font.color.rgb = RGBColor(33, 40, 48)
    set_east_asia(code_style, "Microsoft YaHei")
    code_style.paragraph_format.space_before = Pt(0)
    code_style.paragraph_format.space_after = Pt(0)
    code_style.paragraph_format.line_spacing = 1.0
    code_style.paragraph_format.left_indent = Inches(.12)
    code_style.paragraph_format.widow_control = False
    prompt_style = doc.styles.add_style("PromptText", WD_STYLE_TYPE.PARAGRAPH)
    prompt_style.base_style = normal
    prompt_style.font.size = Pt(9.5)
    prompt_style.paragraph_format.space_after = Pt(3)
    prompt_style.paragraph_format.left_indent = Inches(.12)

    doc.add_paragraph("附录 E 主要源程序及支撑材料", style="Title")
    doc.add_paragraph("对应论文：F_final_candidate_v7_最终投稿版")
    doc.add_paragraph("本附录收录论文模型与结果所需的核心计算函数。代码段保留模型定义和求解逻辑；完整数据处理、验证、作图程序及运行证据列于各问的支撑材料。")
    doc.add_paragraph("复制代码段单独运行前，请按对应支撑源程序补齐输入表、参数配置和运行环境。原始完整程序已在 GitHub 项目分问登记 SHA-256。")

    for key, (heading, _) in OUTLINE.items():
        doc.add_page_break()
        doc.add_heading(heading, level=1)
        for row in snippet_records(key):
            doc.add_heading(row["filename"], level=2)
            doc.add_paragraph(f"功能：{row['purpose']}")
            doc.add_paragraph("完整支撑源程序：")
            for source, digest in row["sources"].items():
                doc.add_paragraph(f"{source}    SHA-256：{digest}")
            for line in row["code"].splitlines():
                p = doc.add_paragraph(style="AppendixCode")
                p.add_run(line)

    doc.add_page_break()
    doc.add_heading("支撑材料与 Codex 提示词", level=1)
    for key, (heading, _) in OUTLINE.items():
        manifest_path = HERE / f"{key}_manifest.json"
        if not manifest_path.is_file():
            raise FileNotFoundError(f"Generate {key}.md and its manifest before building the Word file")
        doc.add_paragraph(f"{heading}：04_code/final_v7_codebook/{key}.md（含完整支撑源码快照与哈希清单）")
    doc.add_paragraph("完整程序的原始位置：项目 04_code/modeling_phase1、modeling_phase2、modeling_phase3、modeling_phase4、paper_round8、paper_v5 和 visualization 目录。")
    doc.add_heading("可直接粘贴到 Codex 的提示词", level=2)
    for line in prompt_text().splitlines():
        doc.add_paragraph(line, style="PromptText")
    target.parent.mkdir(parents=True, exist_ok=True)
    doc.core_properties.title = "附录 E 主要源程序及支撑材料"
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    doc.save(target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=list(OUTLINE))
    parser.add_argument("--docx", type=Path)
    args = parser.parse_args()
    if not args.section and not args.docx:
        parser.error("Specify --section or --docx")
    if args.section:
        render_markdown(args.section)
    if args.docx:
        build_docx(args.docx)


if __name__ == "__main__":
    main()
