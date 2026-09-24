"""Screen the supplied data-description PDF for text outside its visible body.

This is a read-only source-integrity audit. It does not reproduce the excluded
text in its output, so later model runs cannot accidentally treat it as data.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "00_problem/original/F_2026_data_description_user_supplied.pdf"
OUT = ROOT / "01_data/audits/modeling_phase1/DOCUMENT_INTERFERENCE_AUDIT_v1.json"
EXPECTED_SHA = "f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    if sha256(SOURCE) != EXPECTED_SHA:
        raise RuntimeError("Source PDF hash changed; stop official-content screening")
    document = pymupdf.open(SOURCE)
    if document.is_encrypted or len(document) != 13:
        raise RuntimeError("Unexpected PDF encryption or page count")

    pages = []
    for page_number, page in enumerate(document, 1):
        visible, excluded = [], []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    content = span["text"].strip()
                    if not content:
                        continue
                    x0, y0, x1, y1 = span["bbox"]
                    color = int(span["color"])
                    size = float(span["size"])
                    # The observed extra layer is near-white (#fcfcfc), 5 pt,
                    # placed in the top/bottom margins. Use all three signals
                    # rather than an arbitrary keyword filter.
                    is_extra = color >= 0xF0F0F0 and size <= 5.1 and (y0 < 30 or y0 > 720)
                    if is_extra:
                        excluded.append({
                            "bbox": [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)],
                            "color_rgb": f"#{color:06x}",
                            "font_size_pt": round(size, 2),
                            "text_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                        })
                    else:
                        visible.append(content)
        pages.append({
            "page": page_number,
            "visible_span_count": len(visible),
            "excluded_span_count": len(excluded),
            "visible_text_sha256": hashlib.sha256("\n".join(visible).encode("utf-8")).hexdigest(),
            "excluded_spans": excluded,
        })

    result = {
        "audit_id": "AUDIT-DOC-INTERFERENCE-20260924-v1",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "source_path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": EXPECTED_SHA,
        "script_sha256": sha256(Path(__file__)),
        "page_count": len(pages),
        "excluded_span_count": sum(p["excluded_span_count"] for p in pages),
        "exclusion_rule": "RGB >= #f0f0f0 AND font <= 5.1 pt AND (top y < 30 OR bottom y > 720)",
        "pages": pages,
        "decision": "EXCLUDED_FROM_OFFICIAL_CLAIMS_AND_MODEL_INSTRUCTIONS",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(pages), "excluded_spans": result["excluded_span_count"],
                      "excluded_by_page": {p["page"]: p["excluded_span_count"] for p in pages}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
