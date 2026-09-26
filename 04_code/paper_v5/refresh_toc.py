"""Replace v3's static contents page numbers using the rendered v5 PDF."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "08_paper/v5"
STEM = "F_final_candidate_v5_参考论文深度吸收完整版"
DOCX = ROOT / "11_delivery/v5" / (STEM + ".docx")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rendered-pdf", type=Path, required=True)
    opt = parser.parse_args()
    pdf = opt.rendered_pdf.resolve()
    pages = PdfReader(pdf).pages
    lines = [set(line.strip() for line in (page.extract_text() or "").splitlines()) for page in pages]
    doc = Document(DOCX)
    rows = []
    for p in doc.paragraphs:
        if p.style is None or p.style.name != "PaperTOC":
            continue
        title = p.text.split("\t")[0]
        found = [i + 1 for i, page_lines in enumerate(lines[3:], 3) if title in page_lines]
        if len(found) != 1:
            raise ValueError(f"Contents heading {title!r} occurs on {found}")
        physical = found[0]
        printed = physical - 1  # cover has no page number; abstract starts at 1
        p.text = f"{title}\t{printed}"
        rows.append({"heading": title, "physical_page": physical, "printed_page": printed})
    if len(rows) != 37:
        raise ValueError(f"Expected 37 v3 contents headings, got {len(rows)}")
    temp = DOCX.with_name(STEM + ".toc.tmp.docx")
    doc.save(temp)
    temp.replace(DOCX)
    map_path = SRC / "TOC_PAGE_MAP_v5.json"
    map_path.write_text(json.dumps({"rendered_pdf_sha256": sha(pdf), "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest_path = SRC / "BUILD_MANIFEST_v5.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["toc_refreshed"] = True
    manifest["toc_rows"] = len(rows)
    manifest["docx_sha256"] = sha(DOCX)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"rows": len(rows), "first": rows[0], "last": rows[-1]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
