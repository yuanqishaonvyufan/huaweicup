"""Synchronize the static contents page numbers with a Word-rendered PDF."""

import argparse
import json
from pathlib import Path

from docx import Document
from pypdf import PdfReader


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docx", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    args = parser.parse_args()
    doc = Document(args.docx)
    lines = [set(s.strip() for s in (page.extract_text() or "").splitlines())
             for page in PdfReader(args.pdf).pages]
    changes = []
    rows = 0
    for paragraph in doc.paragraphs:
        if paragraph.style.name != "PaperTOC":
            continue
        rows += 1
        title, old = paragraph.text.rsplit("\t", 1)
        hits = [index for index in range(3, len(lines)) if title in lines[index]]
        if len(hits) != 1:
            raise ValueError(f"Contents heading {rows} has {len(hits)} body matches")
        printed = hits[0]  # cover is unnumbered; PDF index equals printed page
        if int(old) != printed:
            paragraph.text = f"{title}\t{printed}"
            changes.append({"row": rows, "old": int(old), "new": printed})
    if rows != 37:
        raise ValueError(f"Expected 37 contents entries, found {rows}")
    if changes:
        doc.save(args.docx)
    print(json.dumps({"rows": rows, "changes": changes}, ensure_ascii=False))


if __name__ == "__main__":
    main()
