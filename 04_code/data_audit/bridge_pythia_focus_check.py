"""Focused verification of the seven C6 High Pythia bridge rows.

This checks lineage and descriptive association only. It does not fit or
validate a Loss-to-Benchmark mapping. Raw files stay read-only.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data" / "raw" / "real_attachments"
OUT = ROOT / "01_data" / "audits" / "phase1" / "bridge_pythia_focus_check.json"
BRIDGE = RAW / "C_efficiency_evolution" / "loss_benchmark_bridge_expanded.csv"
LOG = RAW / "B_scaling_laws" / "pythia_training_log_existing.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


bridge = pd.read_csv(BRIDGE)
log = pd.read_csv(LOG)
high = bridge[bridge["Loss_Comparability"].astype(str).str.startswith("High")].copy()
paired = high.merge(log[["N_params_B", "D_tokens_B", "val_loss"]],
                    on=["N_params_B", "D_tokens_B"], how="left", validate="one_to_one")
if len(paired) != 7 or paired["val_loss"].isna().any():
    raise ValueError("Expected exactly seven High bridge rows with B1 matches")

benchmark_columns = ["LB_Average", "LB_IFEval", "LB_BBH", "LB_MATH",
                     "LB_GPQA", "LB_MUSR", "LB_MMLU_PRO"]
associations = {}
for column in benchmark_columns:
    associations[column] = {
        "pearson_with_val_loss": float(high["Val_Loss"].corr(high[column], method="pearson")),
        "spearman_with_val_loss": float(high["Val_Loss"].corr(high[column], method="spearman")),
    }

result = {
    "status": "AUDIT_EVIDENCE_ONLY_NOT_VALIDATED_BRIDGE",
    "input_paths_sha256": {str(BRIDGE.relative_to(ROOT)).replace("\\", "/"): sha256(BRIDGE),
                           str(LOG.relative_to(ROOT)).replace("\\", "/"): sha256(LOG)},
    "high_rows": len(high),
    "family_prefixes": high["Model"].astype(str).str.split("/").str[0].value_counts().to_dict(),
    "D_tokens_B_unique": sorted(high["D_tokens_B"].unique().tolist()),
    "N_params_B_min_max": [float(high["N_params_B"].min()), float(high["N_params_B"].max())],
    "matched_B1_final_checkpoints": int(paired["val_loss"].notna().sum()),
    "max_abs_C6_B1_loss_difference": float((paired["Val_Loss"] - paired["val_loss"]).abs().max()),
    "B1_design": {
        "rows": len(log),
        "N_levels": int(log["N_params_B"].nunique()),
        "D_levels_per_N": sorted(log.groupby("N_params_B")["D_tokens_B"].nunique().unique().tolist()),
        "N_range_B": [float(log["N_params_B"].min()), float(log["N_params_B"].max())],
        "D_range_B": [float(log["D_tokens_B"].min()), float(log["D_tokens_B"].max())],
        "val_loss_range": [float(log["val_loss"].min()), float(log["val_loss"].max())],
        "logN_logD_correlation": float(np.corrcoef(np.log(log["N_params_B"]),
                                                    np.log(log["D_tokens_B"]))[0, 1]),
        "rank_intercept_logN_logD": int(np.linalg.matrix_rank(np.column_stack(
            [np.ones(len(log)), np.log(log["N_params_B"]), np.log(log["D_tokens_B"])]))),
    },
    "associations": associations,
    "limit": "Seven correlated model sizes in one family, with D fixed; no held-out mapping, residual assessment, interval calibration, Q/p variation, or cross-family transport.",
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(OUT)
