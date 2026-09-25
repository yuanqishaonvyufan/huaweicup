"""Measure the user-supplied v3 DOCX via its read-only Word PDF render."""
from __future__ import annotations

import bisect
import json
import re
from pathlib import Path

BASE = Path(r"D:\work document\codex_work\f_reference_transfer\baseline_v3\extract")
PAGE_RANGE = range(4, 32)
HAN = re.compile(r"[\u3400-\u9fff]")
PATS = [
    ("introduction", r"(?m)^\s*一、引言"),
    ("overall_analysis", r"(?m)^\s*二、总体分析"),
    ("assumptions", r"(?m)^\s*三、模型假设"),
    ("symbols", r"(?m)^\s*四、符号说明"),
    ("q1", r"(?m)^\s*5\.1\s*问题一的模型的建立和求解"),
    ("q2", r"(?m)^\s*5\.2\s*问题二的模型的建立和求解"),
    ("q3", r"(?m)^\s*5\.3\s*问题三的模型的建立和求解"),
    ("q4", r"(?m)^\s*5\.4\s*问题四的模型的建立和求解"),
    ("validation", r"(?m)^\s*六、模型检验与分析"),
    ("error_analysis", r"(?m)^\s*6\.1\s*误差分析"),
    ("sensitivity", r"(?m)^\s*6\.2\s*灵敏度分析"),
    ("evaluation", r"(?m)^\s*七、模型的评价"),
    ("improvement_promotion", r"(?m)^\s*八、模型的改进与推广"),
    ("references", r"(?m)^\s*参考文献\s*$"),
]


def main() -> None:
    page_text = {i: (BASE / f"page_{i:02d}.txt").read_text(encoding="utf-8") for i in range(1, 35)}
    starts = []
    offset = 0
    for page in PAGE_RANGE:
        starts.append(offset)
        offset += len(page_text[page]) + 1
    body_with_refs = "\n".join(page_text[i] for i in PAGE_RANGE)
    positions = {}
    for name, pattern in PATS:
        hits = list(re.finditer(pattern, body_with_refs))
        if len(hits) != 1:
            raise ValueError(f"{name}: expected one heading, got {len(hits)}")
        positions[name] = hits[0].start()

    def page_of(position: int) -> int:
        return list(PAGE_RANGE)[bisect.bisect_right(starts, position) - 1]

    major = ["introduction", "overall_analysis", "assumptions", "symbols", "q1", "q2", "q3", "q4", "validation", "evaluation", "improvement_promotion", "references"]
    sections = {}
    for idx, name in enumerate(major[:-1]):
        start, end = positions[name], positions[major[idx + 1]]
        chunk = body_with_refs[start:end]
        sections[name] = {"chinese_chars": len(HAN.findall(chunk)), "nonspace_chars": len(re.sub(r"\s", "", chunk)), "start_page": page_of(start), "end_page": page_of(end - 1)}
    for name, end_name in (("error_analysis", "sensitivity"), ("sensitivity", "evaluation")):
        start, end = positions[name], positions[end_name]
        sections[name] = {"chinese_chars": len(HAN.findall(body_with_refs[start:end])), "start_page": page_of(start), "end_page": page_of(end - 1)}
    captions = []
    for page, text in page_text.items():
        if page == 3:
            continue
        for line in text.splitlines():
            match = re.match(r"^\s*(图|表)\s*([AB]?\d{1,2})\s+(.+)$", line)
            if match:
                captions.append({"kind": "Figure" if match.group(1) == "图" else "Table", "number": match.group(2), "page": page, "title": match.group(3).strip()})
    figure_numbers = sorted({int(c["number"]) for c in captions if c["kind"] == "Figure" and c["number"].isdigit()})
    table_numbers = sorted({int(c["number"]) for c in captions if c["kind"] == "Table" and c["number"].isdigit()})
    equation_text = "\n".join(page_text[i] for i in range(4, 32))
    equation_numbers = sorted({int(x) for x in re.findall(r"（(\d{1,2})）", equation_text)})
    if figure_numbers != list(range(1, 10)) or table_numbers != list(range(1, 17)) or equation_numbers != list(range(1, 25)):
        raise ValueError("Numbering sequence unexpected")
    result = {
        "physical_pages": 34,
        "all_pages_chinese_chars": sum(len(HAN.findall(text)) for text in page_text.values()),
        "page_roles": {"cover": [1], "abstract": [2], "contents": [3], "body_with_references": [4, 31], "appendix": [32, 34]},
        "body_chinese_chars_excluding_references": len(HAN.findall(body_with_refs[:positions["references"]])),
        "sections": sections,
        "figure_count": 9,
        "main_table_count": 16,
        "appendix_table_count": 2,
        "numbered_equation_count": 24,
        "captions": captions,
    }
    (BASE / "v3_structure_counts.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in ("sections", "captions")}, ensure_ascii=True))
    for name in major[:-1]:
        print(name, json.dumps(sections[name], ensure_ascii=True))


if __name__ == "__main__":
    main()
