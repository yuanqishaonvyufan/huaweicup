"""Separate B1 external provenance from attachment-internal numeric eligibility.

No N-D Scaling Law parameter is estimated here.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data/raw/real_attachments/B_scaling_laws/pythia_training_log_existing.csv"
PDF = ROOT / "00_problem/original/F_2026_data_description_user_supplied.pdf"
CONTRACT = ROOT / "03_models/modeling_phase1/q2/B1_TWO_LAYER_ELIGIBILITY_CONTRACT_R4_v1.md"
TRACE = ROOT / "01_data/audits/modeling_phase1/q2/B1_PROVENANCE_TRACE_v2.md"
OUT = ROOT / "01_data/audits/modeling_phase1/q2"
RAW_SHA = "529a59644b0f57bf3a76037838b614bfedc35e58bb26b93052e34ffc63e454c2"
PDF_SHA = "f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835"
RUN_ID = "AUDIT-B1-INTERNAL-ELIGIBILITY-R4-20260924-v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    if sha256(RAW) != RAW_SHA or sha256(PDF) != PDF_SHA:
        raise RuntimeError("Official B1 raw or data-description hash changed")
    if not CONTRACT.is_file() or "SOURCE NOT RECOVERABLE" not in TRACE.read_text(encoding="utf-8"):
        raise RuntimeError("B1 two-layer contract/source stop rule missing")
    data = pd.read_csv(RAW)
    required = ["run_id", "N_params_B", "D_tokens_B", "C_FLOPs_1e21", "steps",
                "train_loss", "val_loss", "ppl", "precision", "wd", "lr"]
    if len(data) != 1176 or len(data.columns) != 15 or not set(required) <= set(data):
        raise RuntimeError("B1 official shape/fields changed")
    if data[required].isna().any().any() or data.run_id.duplicated().any():
        raise RuntimeError("B1 missing key value or duplicate row ID")
    if (data.N_params_B <= 0).any() or (data.D_tokens_B <= 0).any() or not np.isfinite(
            data[["N_params_B", "D_tokens_B", "val_loss"]].to_numpy(float)).all():
        raise RuntimeError("B1 N/D/Loss invalid")
    if data[["N_params_B", "D_tokens_B"]].duplicated().any():
        raise RuntimeError("B1 N-D pair duplication")
    levels_n = sorted(data.N_params_B.unique())
    levels_d = sorted(data.D_tokens_B.unique())
    if len(levels_n) != 8 or len(levels_d) != 147 or len(data) != len(levels_n) * len(levels_d):
        raise RuntimeError("B1 8x147 crossed design changed")
    grid = data.pivot(index="D_tokens_B", columns="N_params_B", values="val_loss").sort_index(axis=0).sort_index(axis=1)
    if grid.isna().any().any():
        raise RuntimeError("Incomplete B1 crossed grid")
    g = grid.to_numpy(float)
    cross_n_diff = np.diff(g, axis=1)
    cross_n_increase = int(np.sum(cross_n_diff > 1e-10))
    cross_n_rows_any = int(np.sum(np.any(cross_n_diff > 1e-10, axis=1)))
    cross_n_rows = [{"D_tokens_B": float(d), "N_adjacent_increase_count": int(np.sum(row > 1e-10)),
                     "max_increase": float(max(0.0, np.max(row))),
                     "loss_min": float(np.min(g[i])), "loss_max": float(np.max(g[i]))}
                    for i, (d, row) in enumerate(zip(grid.index, cross_n_diff))]
    within_d_increase = 0
    trajectory_rows = []
    for n, group in data.groupby("N_params_B"):
        group = group.sort_values("steps")
        increases = int(np.sum(np.diff(group.val_loss.to_numpy(float)) > 1e-10))
        within_d_increase += increases
        trajectory_rows.append({"N_params_B": float(n), "rows": len(group),
                                "step_min": int(group.steps.min()), "step_max": int(group.steps.max()),
                                "D_min_B": float(group.D_tokens_B.min()), "D_max_B": float(group.D_tokens_B.max()),
                                "val_loss_first": float(group.val_loss.iloc[0]),
                                "val_loss_last": float(group.val_loss.iloc[-1]),
                                "val_loss_increase_intervals": increases,
                                "precision_unique": int(group.precision.nunique()),
                                "wd_unique": int(group.wd.nunique()), "lr_unique": int(group.lr.nunique())})
    d_error = np.abs(data.D_tokens_B - data.steps * 2_097_152 / 1e9)
    c_ratio = data.C_FLOPs_1e21 / (0.006 * data.N_params_B * data.D_tokens_B)
    ppl_rel = np.abs(data.ppl - np.exp(data.val_loss)) / np.exp(data.val_loss)
    if d_error.max() > 0.00051 or np.median(np.abs(c_ratio - 1)) > 0.01 or ppl_rel.max() > 0.001:
        raise RuntimeError("B1 attachment-internal arithmetic outside predeclared rounding tolerance")
    if within_d_increase > 0:
        raise RuntimeError("B1 within-size Loss ordering changed")
    if any(x["rows"] != 147 or x["step_min"] != 64 or x["step_max"] != 143000 for x in trajectory_rows):
        raise RuntimeError("B1 trajectory grid changed")

    OUT.mkdir(parents=True, exist_ok=True)
    cross_path = OUT / "B1_CROSS_N_ORDER_R4_v1.csv"
    traj_path = OUT / "B1_INTERNAL_TRAJECTORY_R4_v1.csv"
    pd.DataFrame(cross_n_rows).to_csv(cross_path, index=False, encoding="utf-8-sig")
    pd.DataFrame(trajectory_rows).to_csv(traj_path, index=False, encoding="utf-8-sig")
    result = {
        "audit_id": RUN_ID, "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)), "B1_sha256": RAW_SHA,
        "official_pdf_sha256": PDF_SHA, "contract_sha256": sha256(CONTRACT),
        "rows": len(data), "N_levels": len(levels_n), "D_levels": len(levels_d),
        "unique_ND_pairs": len(data[["N_params_B", "D_tokens_B"]].drop_duplicates()),
        "within_N_D_loss_increase_intervals": within_d_increase,
        "cross_N_loss_increase_adjacent_cells": cross_n_increase,
        "cross_N_D_rows_with_any_increase": cross_n_rows_any,
        "D_from_step_max_abs_Btokens": float(d_error.max()),
        "C_to_6ND_ratio_median": float(np.median(c_ratio)),
        "ppl_exp_loss_max_relative_error": float(ppl_rel.max()),
        "precision_varies_within_all_N": all(x["precision_unique"] > 1 for x in trajectory_rows),
        "wd_varies_within_all_N": all(x["wd_unique"] > 1 for x in trajectory_rows),
        "metadata_quarantine": ["precision", "wd", "lr", "gpu_days", "step_time_ms", "grad_norm_avg"],
        "permitted_baseline_variables_if_released": ["N_params_B", "D_tokens_B", "val_loss"],
        "external_empirical_eligibility": "NOT_ELIGIBLE_PROVENANCE_UNRESOLVED",
        "attachment_internal_numeric_integrity": "PASS",
        "no_scaling_law_fit": True,
        "outputs": {"cross_N": {"sha256": sha256(cross_path), "rows": len(cross_n_rows)},
                    "trajectories": {"sha256": sha256(traj_path), "rows": len(trajectory_rows)}},
    }
    (OUT / "B1_INTERNAL_ELIGIBILITY_R4_v1.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_id": RUN_ID, "external": result["external_empirical_eligibility"],
                      "internal": result["attachment_internal_numeric_integrity"],
                      "cross_N_increases": cross_n_increase}, ensure_ascii=False))


if __name__ == "__main__":
    main()
