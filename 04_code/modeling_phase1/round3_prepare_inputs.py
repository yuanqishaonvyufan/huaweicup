"""Freeze Round 3 Q1 comparison inputs without reading held-out A6-A11 Loss.

All source attachments are verified by the checked official mapping or the
frozen raw SHA-256 manifest. Raw files are never modified.
"""

from __future__ import annotations

import csv
import hashlib
import json
import lzma
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from sys import path as sys_path

sys_path.insert(0, str(Path(__file__).resolve().parents[1] / "data_audit"))
from modeling_phase1_q1_audit import LIST_LENGTHS, SIGNALS, scalar_value, validate_mapping  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data/raw/real_attachments"
OUT = ROOT / "01_data/processed/modeling_phase1/round3"
P = RAW / "A_data_value/regmix_tables/train_mixture_1m.csv"
LOSS = RAW / "A_data_value/regmix_tables/train_pile_loss_1m.csv"
ROUTE = ROOT / "01_data/audits/phase1/route_audit_metrics.json"
RAW_MANIFEST = ROOT / "01_data/raw/RAW_SHA256.csv"
SIGNAL_SET = ROOT / "03_models/modeling_phase1/q1/Q1_DESCRIPTIVE_SIGNAL_SET_v1.csv"
CONTRACT = ROOT / "03_models/modeling_phase1/q1/Q1_ROUND3_COMPARISON_CONTRACT_v1.md"
P_HASH = "04a32ef4ab594376bf90e11404c033668f887c351d6a03ad3744824c7296a2d8"
LOSS_HASH = "49a959aa07ce5c20831d5abe3a7896ff0cd90a398bd407c8913fd5588be0465a"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def softmax_probability(logits: list[float]) -> float:
    delta = float(logits[1]) - float(logits[0])
    return float(1 / (1 + math.exp(-max(-700.0, min(700.0, delta)))))


def quality_features(mapping: dict[str, str]) -> pd.DataFrame:
    source = mapping["official_id"]
    records = []
    with lzma.open(RAW / mapping["actual_relative_path"], "rt", encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            row = {
                "id": str(item["id"]), "source": source,
                "domain": str(item.get("_source_domain") or ("arxiv" if source == "A2" else "github")),
            }
            for signal in SIGNALS:
                value, status, parts = scalar_value(signal, item[signal])
                row[signal] = value
                if signal in LIST_LENGTHS:
                    row[signal + "_valid"] = int(status == "OK")
                if signal in ("fluency_en", "ad_en"):
                    row[signal + "_argmax"] = int(np.argmax(parts)) if status == "OK" else math.nan
                    row[signal + "_prob_positive"] = softmax_probability(parts) if status == "OK" else math.nan
                elif signal.startswith("modernbert_"):
                    row[signal + "_argmax"] = int(np.argmax(parts)) if status == "OK" else math.nan
                elif signal == "qurater":
                    for j in range(4):
                        row[f"qurater_facet_{j}"] = parts[j] if status == "OK" else math.nan
            records.append(row)
    return pd.DataFrame.from_records(records)


def main() -> None:
    mappings, _, mapping_sha = validate_mapping()
    with RAW_MANIFEST.open(encoding="utf-8-sig", newline="") as stream:
        hashes = {r["relative_path"]: r["sha256"] for r in csv.DictReader(stream)}
    for path, expected in ((P, P_HASH), (LOSS, LOSS_HASH)):
        relative = str(path.relative_to(RAW)).replace("\\", "/")
        if hashes.get(relative) != expected or sha256(path) != expected:
            raise RuntimeError(f"A4/A5 path/hash changed: {relative}")
    if not SIGNAL_SET.is_file() or not CONTRACT.is_file():
        raise RuntimeError("Round 3 signal set and comparison contract must be frozen first")
    signal_set = pd.read_csv(SIGNAL_SET, encoding="utf-8-sig")
    if len(signal_set) != 22 or set(signal_set["Signal ID"]) != set(SIGNALS):
        raise RuntimeError("Frozen 22-signal set mismatch")

    frames = [quality_features(m) for m in mappings]
    expected_rows = [51230, 17523, 203752]
    if [len(x) for x in frames] != expected_rows or any(x.id.duplicated().any() for x in frames):
        raise RuntimeError("A1/A2/A3 row count or within-source ID uniqueness changed")
    physical = pd.concat(frames, ignore_index=True)
    if len(physical) != 272505 or physical.id.nunique() != 261086:
        raise RuntimeError("Physical or unique ID count changed")

    with ROUTE.open(encoding="utf-8") as stream:
        loss_columns = json.load(stream)["A"]["A4_A5"]["loss_columns"]
    p_index = pd.read_csv(P, usecols=["index"])
    loss = pd.read_csv(LOSS)
    if len(loss) != 512 or len(p_index) != 512 or loss["index"].duplicated().any() or p_index["index"].duplicated().any():
        raise RuntimeError("A4/A5 training run count/index uniqueness changed")
    if set(loss["index"]) != set(p_index["index"]):
        raise RuntimeError("A4/A5 run index sets changed")
    if list(loss.columns) != ["index", *loss_columns] or not np.isfinite(loss[loss_columns].to_numpy(float)).all():
        raise RuntimeError("A5 13-domain Loss schema/value mismatch")

    OUT.mkdir(parents=True, exist_ok=True)
    q_path = OUT / "q1_quality_features_v1.csv.gz"
    l_path = OUT / "a5_13_domain_loss_v1.csv.gz"
    physical.to_csv(q_path, index=False, compression="gzip", float_format="%.17g")
    loss[["index", *loss_columns]].to_csv(l_path, index=False, compression="gzip", float_format="%.17g")
    manifest = {
        "status": "FROZEN_INPUT_FOR_NONFINAL_ROUND3_COMPARISON",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)),
        "round1_mapping_sha256": mapping_sha,
        "signal_set_sha256": sha256(SIGNAL_SET),
        "comparison_contract_sha256": sha256(CONTRACT),
        "raw_input_sha256": {m["official_id"]: m["sha256"] for m in mappings} | {"A4": P_HASH, "A5": LOSS_HASH},
        "processed": {
            "quality": {"path": str(q_path.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(q_path),
                        "rows": len(physical), "unique_ids": int(physical.id.nunique()),
                        "columns": list(physical.columns)},
            "response": {"path": str(l_path.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(l_path),
                         "rows": len(loss), "columns": list(loss[["index", *loss_columns]].columns)},
        },
        "heldout_A6_A11_read": False,
    }
    (OUT / "INPUT_MANIFEST_v1.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"quality_rows": len(physical), "unique_ids": int(physical.id.nunique()),
                      "response_rows": len(loss), "quality_sha256": manifest["processed"]["quality"]["sha256"],
                      "response_sha256": manifest["processed"]["response"]["sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
