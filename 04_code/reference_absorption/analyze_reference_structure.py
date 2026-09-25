"""Count the visible reference paper's structure from page-wise text extraction.

Counts are reproducible text-layer counts and are checked against rendered PDF
pages before being used in the human-readable audit.
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
from pathlib import Path

HAN = re.compile(r"[\u3400-\u9fff]")
CAPTION = re.compile(r"^\s*(图|表)\s*(\d{1,2})\s+(.+)$")
SECTIONS = [
    ("introduction", r"(?m)^\s*一、\s*引言"),
    ("overall_analysis", r"(?m)^\s*二、\s*总体分析"),
    ("assumptions", r"(?m)^\s*三、\s*模型假设"),
    ("symbols", r"(?m)^\s*四、\s*符号说明"),
    ("q1", r"(?m)^\s*5\.1\s*问题一的模型的建立和求解"),
    ("q2", r"(?m)^\s*5\.2\s*问题二的模型的建立和求解"),
    ("q3", r"(?m)^\s*5\.3\s*问题三的模型的建立和求解"),
    ("q4", r"(?m)^\s*5\.4\s*问题四的模型的建立和求解"),
    ("validation", r"(?m)^\s*六、\s*模型检验与分析"),
    ("error_analysis", r"(?m)^\s*6\.1\s*误差分析"),
    ("sensitivity", r"(?m)^\s*6\.2\s*灵敏度分析"),
    ("evaluation", r"(?m)^\s*七、\s*模型的评价"),
    ("advantages", r"(?m)^\s*7\.1\s*模型的优点"),
    ("disadvantages", r"(?m)^\s*7\.2\s*模型的缺点"),
    ("improvement_promotion", r"(?m)^\s*八、\s*模型的改进与推广"),
    ("improvement", r"(?m)^\s*8\.1\s*模型的改进"),
    ("promotion", r"(?m)^\s*8\.2\s*模型的推广"),
]


def count(text: str) -> dict[str, int]:
    return {"chinese_chars": len(HAN.findall(text)), "nonspace_chars": len(re.sub(r"\s", "", text))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("extraction", type=Path)
    args = parser.parse_args()
    pages = [(i, (args.extraction / f"page_{i:02d}.txt").read_text(encoding="utf-8")) for i in range(1, 30)]
    body_pages = pages[4:26]  # physical pages 5..26, excluding cover, abstract, TOC, AI note, references, appendix
    starts = []
    pieces = []
    offset = 0
    for number, content in body_pages:
        starts.append(offset)
        pieces.append(content)
        offset += len(content) + 1
    body = "\n".join(pieces)

    positions = {}
    for name, pattern in SECTIONS:
        hits = list(re.finditer(pattern, body))
        if len(hits) != 1:
            raise ValueError(f"Expected one {name} heading, found {len(hits)}")
        positions[name] = hits[0].start()

    def page_of(pos: int) -> int:
        return body_pages[bisect.bisect_right(starts, pos) - 1][0]

    major = ["introduction", "overall_analysis", "assumptions", "symbols", "q1", "q2", "q3", "q4", "validation", "evaluation", "improvement_promotion"]
    sections = {}
    for idx, name in enumerate(major):
        start = positions[name]
        stop = positions[major[idx + 1]] if idx + 1 < len(major) else len(body)
        sections[name] = {**count(body[start:stop]), "start_page": page_of(start), "end_page": page_of(stop - 1)}
    for name, stop_name in [("error_analysis", "sensitivity"), ("sensitivity", "evaluation"), ("advantages", "disadvantages"), ("disadvantages", "improvement_promotion"), ("improvement", "promotion"), ("promotion", None)]:
        start = positions[name]
        stop = positions[stop_name] if stop_name else len(body)
        sections[name] = {**count(body[start:stop]), "start_page": page_of(start), "end_page": page_of(stop - 1)}
    for q in range(1, 5):
        prefix = f"5.{q}"
        q_start, q_stop = positions[f"q{q}"], positions[f"q{q+1}"] if q < 4 else positions["validation"]
        found = []
        for part, label in [(1, "analysis"), (2, "preparation"), (3, "formulation"), (4, "solution")]:
            pattern = rf"(?m)^\s*{re.escape(prefix)}\.{part}\s*{['具体分析', '模型准备', '模型建立', '模型求解'][part-1]}"
            hits = list(re.finditer(pattern, body[q_start:q_stop]))
            if len(hits) != 1:
                raise ValueError(f"Expected one {prefix}.{part} heading, found {len(hits)}")
            found.append((label, q_start + hits[0].start()))
        for idx, (label, start) in enumerate(found):
            stop = found[idx + 1][1] if idx + 1 < len(found) else q_stop
            sections[f"q{q}_{label}"] = {**count(body[start:stop]), "start_page": page_of(start), "end_page": page_of(stop - 1)}

    captions = []
    for number, page in pages:
        if number == 4:  # TOC uses figure/table words only as references
            continue
        for line in page.splitlines():
            match = CAPTION.match(line)
            if match:
                captions.append({"kind": "figure" if match.group(1) == "图" else "table", "number": int(match.group(2)), "page": number, "title": match.group(3).strip()})
    figures = [c for c in captions if c["kind"] == "figure"]
    tables = [c for c in captions if c["kind"] == "table"]
    if sorted(c["number"] for c in figures) != list(range(1, 21)):
        raise ValueError("Figure sequence differs from 1..20")
    if sorted(c["number"] for c in tables) != list(range(1, 12)):
        raise ValueError("Table sequence differs from 1..11")
    equations = {int(m) for m in re.findall(r"\((\d{1,2})\)", body)}
    if equations != set(range(1, 55)):
        raise ValueError("Equation sequence differs from 1..54")
    references = re.findall(r"(?m)^\s*\[(\d+)\]", pages[27][1])
    if references != [str(i) for i in range(1, 9)]:
        raise ValueError("Reference sequence differs from 1..8")
    result = {
        "physical_pages": 29,
        "page_roles": {"cover": [1], "abstract": [2, 3], "contents": [4], "body": [5, 26], "ai_note": [27], "references": [28], "appendix": [29]},
        "all_pages": count("\n".join(x[1] for x in pages)),
        "body": count(body),
        "sections": sections,
        "figure_count": len(figures),
        "table_count": len(tables),
        "numbered_equation_count": len(equations),
        "reference_count": len(references),
        "captions": captions,
    }
    (args.extraction / "structure_counts.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in ("sections", "captions")}, ensure_ascii=True))
    for key in major + ["error_analysis", "sensitivity", "advantages", "disadvantages", "improvement", "promotion"]:
        print(key, json.dumps(sections[key], ensure_ascii=True))


if __name__ == "__main__":
    main()
