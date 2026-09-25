"""Repair stale Round8 paper-source hashes without changing source results.

The inherited evidence map names two tracked Q1 files whose stored byte hashes
do not match HEAD. Verify every affected numerical selector before recording
current source hashes in a new version; keep v1 as historical evidence.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "08_paper/round9_reference_transfer"
REVIEW = ROOT / "10_review/round9_reference_transfer"


def same(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)
    return a == b


def expected_value(claim_id, source):
    if claim_id == "E01":
        return {m: source["metrics"]["1M"][m]["R0_RMSE_raw"] for m in ("M0", "M1")}
    if claim_id == "E02":
        m0 = source["metrics"]["1M"]["M0"]["domain_RMSE_raw"]
        m1 = source["metrics"]["1M"]["M1"]["domain_RMSE_raw"]
        return {"M0": m0, "M1": m1, "improved": sum(x < y for x, y in zip(m1, m0))}
    if claim_id == "E03":
        return {scale: source["metrics"][scale]["M1"]["R0_centered_RMSE_ratio_to_M0"] for scale in ("60M", "1B")}
    if claim_id == "E04":
        return source["support_counts"]
    if claim_id == "E05":
        return source["role_counts"]
    raise ValueError(f"Unrecognized stale claim: {claim_id}")


claims = json.loads((PAPER / "FINAL_PAPER_EVIDENCE_MAP_v1.json").read_text(encoding="utf-8"))
changed = []
for claim in claims:
    path = ROOT / claim["source_file"]
    content = path.read_bytes()
    actual = hashlib.sha256(content).hexdigest()
    if actual == claim["source_sha256"]:
        continue
    value = expected_value(claim["claim_id"], json.loads(content))
    if not same(value, claim["numerical_value"]):
        raise ValueError(f"Numerical selector changed for {claim['claim_id']}")
    changed.append({
        "claim_id": claim["claim_id"],
        "source_file": claim["source_file"],
        "previous_recorded_sha256": claim["source_sha256"],
        "current_tracked_sha256": actual,
        "numerical_selector_unchanged": True,
    })
    claim["source_sha256"] = actual

if {item["claim_id"] for item in changed} != {"E01", "E02", "E03", "E04", "E05"}:
    raise ValueError("Unexpected stale evidence-map entries")

(PAPER / "FINAL_PAPER_EVIDENCE_MAP_v2.json").write_text(
    json.dumps(claims, ensure_ascii=False, indent=2), encoding="utf-8"
)
REVIEW.mkdir(parents=True, exist_ok=True)
(REVIEW / "EVIDENCE_MAP_HASH_REPAIR_v1.json").write_text(
    json.dumps({"status": "PASS", "entries_checked": len(claims), "hashes_repaired": changed}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps({"status": "PASS", "entries_checked": len(claims), "hashes_repaired": len(changed)}))
