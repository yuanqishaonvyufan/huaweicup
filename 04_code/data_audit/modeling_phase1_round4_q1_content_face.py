"""Deterministic A1 content spot-check for Q1 descriptive face validity.

The snippets are local audit evidence, not independent human quality labels.
No source text is uploaded or used to tune DQ0.
"""

from __future__ import annotations

import hashlib
import json
import lzma
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
A1 = ROOT / "01_data/raw/real_attachments/A_data_value/slimpajama_quality_signal_sample.jsonl.xz"
SCORES = ROOT / "03_models/modeling_phase1/q1/round3/Q1_DESCRIPTIVE_QUALITY_RESULTS_v1.csv.gz"
R3_METRICS = ROOT / "03_models/modeling_phase1/q1/round3/Q1_DESCRIPTIVE_QUALITY_METRICS_v1.json"
OUT = ROOT / "01_data/audits/modeling_phase1/q1"
RUN_ID = "AUDIT-Q1-CONTENT-FACE-R4-20260924-v1"
A1_SHA = "14a4eeec4c7d98efd78942ddd9c1329640527f2108e73227be449bc1a8dbe579"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def key(identifier: str) -> str:
    return hashlib.sha256(identifier.encode("utf-8")).hexdigest()


def main() -> None:
    if sha256(A1) != A1_SHA:
        raise RuntimeError("A1 original content hash changed")
    metrics = json.loads(R3_METRICS.read_text(encoding="utf-8"))
    if sha256(SCORES) != metrics["outputs"]["scores"]["sha256"]:
        raise RuntimeError("Frozen DQ0 score file changed")
    scores = pd.read_csv(SCORES, compression="gzip", usecols=["id", "source", "domain", "DQ0_global_core"],
                         dtype={"id": str})
    a1 = scores[scores.source == "A1"]
    if len(a1) != 51230 or a1.id.duplicated().any():
        raise RuntimeError("A1 score grain changed")
    selected = []
    for domain, group in a1.groupby("domain"):
        for label, quantile in (("LOW_Q05", 0.05), ("HIGH_Q95", 0.95)):
            target = float(group.DQ0_global_core.quantile(quantile))
            ordered = group.assign(distance=(group.DQ0_global_core - target).abs(),
                                   tiehash=group.id.map(key)).sort_values(["distance", "tiehash"])
            record = ordered.iloc[0]
            selected.append({"id": record.id, "domain": domain, "stratum": label,
                             "target_quantile": quantile, "DQ0": float(record.DQ0_global_core)})
    lookup = {row["id"]: row for row in selected}
    with lzma.open(A1, "rt", encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            identifier = str(item["id"])
            if identifier not in lookup:
                continue
            content = str(item["content"])
            row = lookup[identifier]
            lines = [x.strip() for x in content.splitlines() if x.strip()]
            words = re.findall(r"\S+", content)
            row.update({"content_chars": len(content), "word_like_tokens": len(words),
                        "nonalnum_fraction": sum(not c.isalnum() and not c.isspace() for c in content) / max(len(content), 1),
                        "nonempty_lines": len(lines),
                        "duplicate_line_fraction": (len(lines) - len(set(lines))) / max(len(lines), 1),
                        "url_marker_count": content.lower().count("http") + content.lower().count("www."),
                        "snippet_first_280_chars": re.sub(r"\s+", " ", content[:400]).strip()[:280]})
    if len(selected) != 14 or any("content_chars" not in row for row in selected):
        raise RuntimeError("A1 deterministic content cases missing")
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "Q1_CONTENT_FACE_CASES_R4_v1.csv"
    pd.DataFrame(selected).sort_values(["domain", "stratum"]).to_csv(path, index=False, encoding="utf-8-sig")
    result = {"audit_id": RUN_ID, "run_utc": datetime.now(timezone.utc).isoformat(),
              "script_sha256": sha256(Path(__file__)), "A1_sha256": A1_SHA,
              "DQ0_score_sha256": sha256(SCORES), "cases": len(selected),
              "selection": "one record closest to each A1 domain DQ0 5th/95th percentile; ID hash tie-break",
              "purpose": "FACE_VALIDITY_SPOT_CHECK_NOT_INDEPENDENT_LABELS",
              "output_sha256": sha256(path)}
    (OUT / "Q1_CONTENT_FACE_AUDIT_R4_v1.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_id": RUN_ID, "cases": len(selected)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
