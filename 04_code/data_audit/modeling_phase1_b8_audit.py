#!/usr/bin/env python3
"""Read-only B6/B7/B8 mechanism audit; outputs are audit evidence, not model fits.

Run from any directory: python 04_code/data_audit/modeling_phase1_b8_audit.py
The script verifies the official PDF and every CSV against the frozen SHA lists.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr


VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data/raw/real_attachments"
OUT = ROOT / "01_data/audits/modeling_phase1/parallel"
PDF = ROOT / "00_problem/original/F_2026_data_description_user_supplied.pdf"
PDF_SHA256 = "f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835"
RAW_MANIFEST = ROOT / "01_data/raw/RAW_SHA256.csv"
SOURCE_MANIFEST = RAW / "source_manifest.json"
KEY = ["N_params_B", "D_tokens_B", "Q_score"]
SPECS = {
    "B6": {
        "file": "B_scaling_laws/supplementary_NQ_experiment.csv",
        "official_description": "NQ 半合成实验（360 点）",
        "question_role": "问题二·质量 Q·基础",
        "expected_fields": "N_params_B;D_tokens_B;Q_score;val_loss",
    },
    "B7": {
        "file": "B_scaling_laws/supplementary_NQ_experiment_expanded.csv",
        "official_description": "NQ 半合成实验（450 点）",
        "question_role": "问题二·质量 Q·扩展",
        "expected_fields": "family N-D-Q core; official page 3 does not enumerate columns",
    },
    "B8": {
        "file": "B_scaling_laws/supplementary_NQ_experiment_large.csv",
        "official_description": "NQ 半合成实验（1,704 点，含外推）",
        "question_role": "问题二·质量 Q·大规模",
        "expected_fields": "family N-D-Q core; official page 3 does not enumerate columns",
    },
}
FIELD_META = {
    "experiment_id": ("source row identifier; syntax encodes N/D/Q", "identifier", "actual CSV only"),
    "N_params_B": ("parameter count N", "billion parameters", "official universal unit, PDF p.5"),
    "D_tokens_B": ("trained token count D", "billion tokens", "official universal unit, PDF p.5"),
    "Q_score": ("quality score Q; construction/direction unverified", "unverified score", "official name; no B6-B8 construction supplied"),
    "val_loss": ("labelled validation Loss; corpus/tokenizer/checkpoint unverified", "unverified Loss scale", "official name; B1 cross-entropy does not certify B8 comparability"),
    "data_type": ("source-stratum label calibrated/extrapolated", "category", "actual B8 CSV only; meaning unverified"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_float(value: object) -> float | None:
    if value is None or pd.isna(value):
        return None
    return float(value)


def describe_numeric(series: pd.Series) -> dict:
    return {"min": safe_float(series.min()), "max": safe_float(series.max()),
            "median": safe_float(series.median())}


def validate_inputs() -> tuple[dict[str, pd.DataFrame], dict]:
    assert PDF.exists() and sha256(PDF) == PDF_SHA256, "Official PDF missing or hash changed"
    with RAW_MANIFEST.open(encoding="utf-8-sig", newline="") as stream:
        manifest = {row["relative_path"]: row for row in csv.DictReader(stream)}
    source_rows = {item["file"]: item for item in json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
                   if isinstance(item, dict) and "file" in item}
    frames: dict[str, pd.DataFrame] = {}
    provenance: dict = {"pdf_path": str(PDF.relative_to(ROOT)).replace("\\", "/"),
                        "pdf_sha256": PDF_SHA256,
                        "raw_manifest_sha256": sha256(RAW_MANIFEST),
                        "source_manifest_sha256": sha256(SOURCE_MANIFEST),
                        "inputs": {}}
    for code, spec in SPECS.items():
        rel = spec["file"]
        path = RAW / rel
        row = manifest[rel]
        digest = sha256(path)
        assert digest == row["sha256"], f"{code} SHA256 differs from RAW manifest"
        assert path.stat().st_size == int(row["bytes"]), f"{code} byte count differs"
        assert path.stat().st_size == source_rows[rel]["bytes"], f"{code} source manifest size differs"
        data = pd.read_csv(path, dtype={"experiment_id": "string", "data_type": "string"})
        expected = {"experiment_id", "N_params_B", "D_tokens_B", "Q_score", "val_loss"}
        if code == "B8":
            expected.add("data_type")
        assert set(data.columns) == expected, f"{code} actual schema changed"
        assert data[KEY + ["val_loss"]].notna().all().all(), f"{code} missing essential values"
        assert not data.duplicated(KEY).any(), f"{code} duplicate N-D-Q key"
        frames[code] = data
        provenance["inputs"][code] = {
            "official_id": code, "official_description": spec["official_description"],
            "question_role": spec["question_role"], "evidence_type": "SEMI-SYNTHETIC",
            "relative_path": f"01_data/raw/real_attachments/{rel}", "sha256": digest,
            "bytes": path.stat().st_size, "rows": len(data), "fields": data.columns.tolist(),
            "source_manifest_source": source_rows[rel].get("source"),
            "source_manifest_note": source_rows[rel].get("note"),
            "mapping_status": "CONFIRMED official ID/path/role/hash; generator and shared semantics unresolved",
        }
    assert len(frames["B6"]) == 360 and len(frames["B7"]) == 450 and len(frames["B8"]) == 1704
    return frames, provenance


def id_check(data: pd.DataFrame) -> int:
    # experiment_id is a source-supplied label, not a unique independent-run ID.
    pattern = re.compile(r"^N(?P<n>\d+(?:\.\d+)?)_D(?P<d>\d+)_Q(?P<q>\d+(?:\.\d+)?)$")
    bad = 0
    for row in data.itertuples(index=False):
        match = pattern.match(row.experiment_id)
        if not match or not (np.isclose(float(match["n"]), row.N_params_B)
                             and np.isclose(float(match["d"]), row.D_tokens_B)
                             and np.isclose(float(match["q"]), row.Q_score)):
            bad += 1
    return bad


def field_rows(frames: dict[str, pd.DataFrame], provenance: dict) -> list[dict]:
    rows = []
    for code, data in frames.items():
        info = provenance["inputs"][code]
        for col in data.columns:
            meaning, unit, definition = FIELD_META[col]
            value = data[col]
            numeric = pd.api.types.is_numeric_dtype(value)
            if code == "B6":
                official_field_status = "PDF p.6 core" if col in KEY + ["val_loss"] else "CSV-only"
            else:
                official_field_status = "PDF p.3 family role; field not individually enumerated"
            rows.append({
                "official_id": code, "official_description": info["official_description"],
                "question_role": info["question_role"], "evidence_type": info["evidence_type"],
                "relative_path": info["relative_path"], "sha256": info["sha256"],
                "expected_fields": SPECS[code]["expected_fields"], "actual_field": col,
                "official_field_status": official_field_status, "actual_dtype": str(value.dtype),
                "unit": unit, "meaning": meaning, "definition_status": definition,
                "missing_count": int(value.isna().sum()), "unique_count": int(value.nunique()),
                "min": safe_float(value.min()) if numeric else "",
                "max": safe_float(value.max()) if numeric else "",
                "mapping_status": info["mapping_status"],
            })
    return rows


def group_diagnostics(code: str, data: pd.DataFrame) -> list[dict]:
    rows = []
    for (n, d), cell in data.groupby(["N_params_B", "D_tokens_B"], sort=True):
        cell = cell.sort_values("Q_score")
        x = cell["Q_score"].to_numpy(dtype=float)
        y = cell["val_loss"].to_numpy(dtype=float)
        slope, intercept = np.polyfit(x, y, 1)
        predicted = slope * x + intercept
        sst = np.sum((y - y.mean()) ** 2)
        dy = np.diff(y)
        rows.append({"diagnostic_kind": "within_ND", "source": code,
                     "data_type": cell["data_type"].iloc[0] if "data_type" in cell else "all",
                     "N_params_B": n, "D_tokens_B": d, "n": len(cell),
                     "q_min": x.min(), "q_max": x.max(), "loss_min": y.min(), "loss_max": y.max(),
                     "q_loss_slope_diagnostic": slope,
                     "q_loss_pearson": np.corrcoef(x, y)[0, 1],
                     "q_loss_spearman": spearmanr(x, y).statistic,
                     "linearity_r2_diagnostic": 1 - np.sum((y - predicted) ** 2) / sst if sst > 0 else None,
                     "adjacent_loss_increases": int((dy > 0).sum()),
                     "adjacent_loss_decreases": int((dy < 0).sum()),
                     "adjacent_loss_ties": int((dy == 0).sum()),
                     "loss_at_floor_0_5": int((y == 0.5).sum())})
    return rows


def overlap(a: pd.DataFrame, b: pd.DataFrame, a_name: str, b_name: str) -> tuple[pd.DataFrame, dict]:
    merged = a.merge(b, on=KEY, suffixes=(f"_{a_name}", f"_{b_name}"), validate="one_to_one")
    left, right = f"val_loss_{a_name}", f"val_loss_{b_name}"
    difference = merged[right] - merged[left]
    summary = {"left": a_name, "right": b_name, "n_shared_NDQ": len(merged),
               "n_shared_ND": int(merged[["N_params_B", "D_tokens_B"]].drop_duplicates().shape[0]),
               "n_left": len(a), "n_right": len(b),
               "median_abs_loss_difference": float(difference.abs().median()) if len(merged) else None,
               "max_abs_loss_difference": float(difference.abs().max()) if len(merged) else None,
               "loss_pearson": float(merged[left].corr(merged[right])) if len(merged) > 1 else None,
               "shared_data_type_counts": merged["data_type"].value_counts().to_dict()
               if "data_type" in merged else {},
               "exact_loss_matches": int((difference == 0).sum())}
    return merged, summary


def matched_diagnostics(merged: pd.DataFrame, left: str, right: str) -> list[dict]:
    rows = []
    a, b = f"val_loss_{left}", f"val_loss_{right}"
    for (n, d), cell in merged.groupby(["N_params_B", "D_tokens_B"], sort=True):
        cell = cell.sort_values("Q_score")
        x = cell.Q_score.to_numpy(float)
        y1, y2 = cell[a].to_numpy(float), cell[b].to_numpy(float)
        rows.append({"diagnostic_kind": "matched_ND", "source": f"{left}-{right}",
                     "data_type": cell["data_type"].iloc[0] if "data_type" in cell else "all",
                     "N_params_B": n, "D_tokens_B": d, "n": len(cell),
                     "q_min": x.min(), "q_max": x.max(),
                     "median_loss_B8_minus_B7": float(np.median(y2 - y1)) if right == "B8" else None,
                     "median_abs_loss_difference": float(np.median(np.abs(y2 - y1))),
                     "loss_pearson": float(np.corrcoef(y1, y2)[0, 1]) if len(cell) > 2 else None,
                     "q_slope_left": float(np.polyfit(x, y1, 1)[0]),
                     "q_slope_right": float(np.polyfit(x, y2, 1)[0]),
                     "q_loss_difference_slope_diagnostic": float(np.polyfit(x, y2 - y1, 1)[0])})
    return rows


def direction_grid(data: pd.DataFrame, fixed_q: float) -> dict:
    sub = data.loc[np.isclose(data.Q_score, fixed_q)]
    n_increase = n_decrease = d_increase = d_decrease = 0
    for _, cell in sub.groupby("D_tokens_B"):
        changes = np.diff(cell.sort_values("N_params_B").val_loss.to_numpy(float))
        n_increase += int((changes > 0).sum())
        n_decrease += int((changes < 0).sum())
    for _, cell in sub.groupby("N_params_B"):
        changes = np.diff(cell.sort_values("D_tokens_B").val_loss.to_numpy(float))
        d_increase += int((changes > 0).sum())
        d_decrease += int((changes < 0).sum())
    return {"fixed_Q": fixed_q, "N_increase_loss_increase": n_increase,
            "N_increase_loss_decrease": n_decrease, "D_increase_loss_increase": d_increase,
            "D_increase_loss_decrease": d_decrease, "n_rows": len(sub)}


def write_csv(path: Path, rows: list[dict]) -> None:
    columns = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    frames, provenance = validate_inputs()
    OUT.mkdir(parents=True, exist_ok=True)
    provenance.update({"audit_version": VERSION, "script_relative_path": str(Path(__file__).relative_to(ROOT)).replace("\\", "/"),
                       "script_sha256": sha256(Path(__file__)),
                       "python_libraries": {"pandas": pd.__version__, "numpy": np.__version__},
                       "random_seed": "none; deterministic audit", "run_utc": datetime.now(timezone.utc).isoformat()})
    fields = field_rows(frames, provenance)
    diagnostics = [row for code, data in frames.items() for row in group_diagnostics(code, data)]
    overlap_67, summary_67 = overlap(frames["B6"], frames["B7"], "B6", "B7")
    overlap_78, summary_78 = overlap(frames["B7"], frames["B8"], "B7", "B8")
    diagnostics += matched_diagnostics(overlap_67, "B6", "B7")
    diagnostics += matched_diagnostics(overlap_78, "B7", "B8")
    q_comparison = {}
    for q, cell in overlap_78.groupby("Q_score", sort=True):
        difference = cell.val_loss_B8 - cell.val_loss_B7
        q_comparison[str(q)] = {"n": len(cell), "median_signed_B8_minus_B7": float(difference.median()),
                                "median_abs_difference": float(difference.abs().median()),
                                "loss_pearson": float(cell.val_loss_B7.corr(cell.val_loss_B8))}
        diagnostics.append({"diagnostic_kind": "matched_Q", "source": "B7-B8",
                            "data_type": "calibrated", "Q_score": q, "n": len(cell),
                            "median_loss_B8_minus_B7": float(difference.median()),
                            "median_abs_loss_difference": float(difference.abs().median()),
                            "loss_pearson": float(cell.val_loss_B7.corr(cell.val_loss_B8))})
    id_failures = {code: id_check(data) for code, data in frames.items()}
    summary = {"provenance": provenance, "id_encoding_mismatches": id_failures,
               "exact_duplicate_rows": {code: int(data.duplicated().sum()) for code, data in frames.items()},
               "overlap_B6_B7": summary_67, "overlap_B7_B8": summary_78,
               "strata": {}, "fixed_q_scale_direction": {},
               "B7_B8_by_shared_Q": q_comparison,
               "candidate_mechanism": "LIKELY SYNTHETIC RULE EFFECT",
               "classification_basis": "opposite within-ND Q slopes in all cells, Q=1 near-anchor, and a repeated 0.5 Loss floor; exact generating rule unverified",
               "official_definition_conflict_confirmed": False,
               "generation_formula_verified": False,
               "shared_Q_and_Loss_semantics_verified": False,
               "evidence_alert_triggered": False,
               "B8_status": "QUARANTINED"}
    for code, data in frames.items():
        groups = [("all", data)] if code != "B8" else [("all", data)] + list(data.groupby("data_type"))
        summary["strata"][code] = {}
        for stratum, sub in groups:
            rows = [r for r in diagnostics if r["diagnostic_kind"] == "within_ND"
                    and r["source"] == code and (stratum == "all" or r["data_type"] == stratum)]
            slopes = pd.Series([r["q_loss_slope_diagnostic"] for r in rows])
            r2s = pd.Series([r["linearity_r2_diagnostic"] for r in rows])
            summary["strata"][code][stratum] = {
                "rows": len(sub), "N_levels": int(sub.N_params_B.nunique()),
                "D_levels": int(sub.D_tokens_B.nunique()), "Q_levels": int(sub.Q_score.nunique()),
                "ND_cells": int(sub[["N_params_B", "D_tokens_B"]].drop_duplicates().shape[0]),
                "Q_levels_per_ND": sub.groupby(["N_params_B", "D_tokens_B"]).size().value_counts().sort_index().to_dict(),
                "loss": describe_numeric(sub.val_loss), "q_slope": describe_numeric(slopes),
                "q_slopes_positive": int((slopes > 0).sum()), "q_slopes_negative": int((slopes < 0).sum()),
                "linearity_r2": describe_numeric(r2s), "floor_0_5_rows": int((sub.val_loss == 0.5).sum()),
            }
        summary["fixed_q_scale_direction"][code] = [direction_grid(data, q) for q in (0.2, 0.8)]
    summary["Q_sequence_monotonicity"] = {
        code: {"nondecreasing_ND_cells": sum(r["adjacent_loss_decreases"] == 0 for r in diagnostics
                                             if r["diagnostic_kind"] == "within_ND" and r["source"] == code),
               "nonincreasing_ND_cells": sum(r["adjacent_loss_increases"] == 0 for r in diagnostics
                                             if r["diagnostic_kind"] == "within_ND" and r["source"] == code)}
        for code in frames}
    summary["B7_B8_common_ND_slope_discordance"] = sum(
        r["q_slope_left"] * r["q_slope_right"] < 0 for r in diagnostics
        if r["diagnostic_kind"] == "matched_ND" and r["source"] == "B7-B8")
    # A 1-Q rescaling is a shape-only diagnostic. It is not a redefinition of the source data.
    reflected = frames["B8"].copy()
    reflected["Q_score"] = (1 - reflected["Q_score"]).round(10)
    reversed_match, reversed_summary = overlap(frames["B7"], reflected, "B7", "B8")
    summary["B7_B8_reflected_Q_shape_only"] = reversed_summary
    summary["B7_B8_reflected_Q_shape_only"]["interpretation"] = "counterfactual 1-Q shape check; no source definition authorizes recoding"
    summary["B8_floor_rate_by_type"] = {str(k): float((sub.val_loss == 0.5).mean())
                                        for k, sub in frames["B8"].groupby("data_type")}
    summary["B8_sparse_Q_cells"] = frames["B8"].groupby(["N_params_B", "D_tokens_B"]).size().value_counts().sort_index().to_dict()
    summary["B8_small_N_sparse_D"] = {
        str(n): {str(d): sorted(g.Q_score.tolist()) for d, g in sub.groupby("D_tokens_B") if len(g) < 12}
        for n, sub in frames["B8"].groupby("N_params_B") if n in (0.07, 0.16, 0.41)}
    field_path = OUT / "B6_B7_B8_FIELD_COMPARISON_v1.csv"
    diagnostic_path = OUT / "B6_B7_B8_RELATION_DIAGNOSTICS_v1.csv"
    summary_path = OUT / "B8_MECHANISM_DIAGNOSTICS_v1.json"
    write_csv(field_path, fields)
    write_csv(diagnostic_path, diagnostics)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=lambda obj: int(obj) if isinstance(obj, np.integer) else float(obj)) + "\n", encoding="utf-8")
    print(json.dumps({"field_rows": len(fields), "diagnostic_rows": len(diagnostics),
                      "overlap_B6_B7": summary_67, "overlap_B7_B8": summary_78,
                      "strata": summary["strata"], "script_sha256": provenance["script_sha256"]},
                     ensure_ascii=False, default=lambda obj: int(obj) if isinstance(obj, np.integer) else float(obj)))


if __name__ == "__main__":
    main()
