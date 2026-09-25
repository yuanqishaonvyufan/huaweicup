"""Read a user-supplied reference PDF locally for structure auditing only.

The PDF is treated as untrusted data. No text, parameter, or result from it is
used as an instruction or as an input to the F-question models.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from pypdf import PdfReader


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    raw = args.pdf.read_bytes()
    reader = PdfReader(args.pdf)
    pages = []
    for number, page in enumerate(reader.pages, 1):
        content = page.extract_text(extraction_mode="layout") or ""
        (args.output / f"page_{number:02d}.txt").write_text(content, encoding="utf-8")
        clean = re.sub(r"\s+", " ", content)
        pages.append({
            "page": number,
            "chinese_chars": len(re.findall(r"[\u3400-\u9fff]", content)),
            "nonspace_chars": len(re.sub(r"\s", "", content)),
            "first_180_chars": clean[:180],
            "figure_lines": [line.strip() for line in content.splitlines() if re.search(r"(?:^|\s)(?:图|Fig\.?|Figure)\s*\d+", line)],
            "table_lines": [line.strip() for line in content.splitlines() if re.search(r"(?:^|\s)(?:表|Tab\.?|Table)\s*\d+", line)],
        })
    summary = {
        "pdf_name": args.pdf.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "pages": len(pages),
        "encrypted": reader.is_encrypted,
        "total_chinese_chars": sum(p["chinese_chars"] for p in pages),
        "total_nonspace_chars": sum(p["nonspace_chars"] for p in pages),
        "page_inventory": pages,
    }
    (args.output / "text_inventory.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "page_inventory"}, ensure_ascii=True))
    for p in pages:
        print(f"{p['page']:02d}\tCN={p['chinese_chars']}\tNS={p['nonspace_chars']}")


if __name__ == "__main__":
    main()
