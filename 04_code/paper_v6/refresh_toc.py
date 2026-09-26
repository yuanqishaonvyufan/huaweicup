"""Set v6's static contents entries to the final Word PDF's printed pages."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from docx import Document
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
STEM = "F_final_candidate_v6_获奖范文格式语言优化版"
DOCX = ROOT / "11_delivery/v6" / (STEM + ".docx")
MAP = ROOT / "08_paper/v6/TOC_PAGE_MAP_v6.json"
MANIFEST = ROOT / "08_paper/v6/BUILD_MANIFEST_v6.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rendered-pdf", type=Path, required=True)
    parser.add_argument("--docx", type=Path, default=DOCX)
    args = parser.parse_args()
    pdf = args.rendered_pdf.resolve()
    docx_path = args.docx.resolve()
    map_path = MAP if docx_path == DOCX.resolve() else docx_path.parent / MAP.name
    manifest_path = MANIFEST if docx_path == DOCX.resolve() else docx_path.parent / MANIFEST.name
    pages = PdfReader(pdf).pages
    lines = [set(line.strip() for line in (page.extract_text() or "").splitlines())
             for page in pages]
    doc = Document(docx_path)
    rows = []
    for p in doc.paragraphs:
        if not p.style or p.style.name != "PaperTOC":
            continue
        title = p.text.split("\t")[0]
        found = [idx + 1 for idx in range(3, len(lines)) if title in lines[idx]]
        if len(found) != 1:
            raise ValueError(f"Expected one body heading for {title!r}, found {found}")
        physical = found[0]
        printed = physical - 1  # cover unnumbered; abstract is page 1
        p.text = f"{title}\t{printed}"
        rows.append({"heading": title, "physical_page": physical,
                     "printed_page": printed})
    if len(rows) != 37:
        raise ValueError(f"Expected 37 contents entries, got {len(rows)}")
    temp = docx_path.with_suffix(".toc.docx")
    doc.save(temp)
    temp.replace(docx_path)
    map_path.write_text(json.dumps({"source_pdf_sha256": sha(pdf), "rows": rows},
                                   ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["toc_rows_verified"] = len(rows)
    manifest["docx_sha256"] = sha(docx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                             encoding="utf-8")
    print(json.dumps({"rows": len(rows), "first": rows[0], "last": rows[-1]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
