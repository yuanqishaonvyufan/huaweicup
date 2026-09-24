"""Round 4 Q1 quality closure: full-22 profile plus five-core domain vector.

Uses only frozen Round 3 quality input and representation outputs. No Loss or
benchmark data are opened, and no Q2-identifiable quality effect is inferred.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from round3_q1_descriptive import CORE, ecdf, split_is_check


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "01_data/processed/modeling_phase1/round3"
Q_INPUT = INPUT / "q1_quality_features_v1.csv.gz"
R3 = ROOT / "03_models/modeling_phase1/q1/round3"
SCORES = R3 / "Q1_DESCRIPTIVE_QUALITY_RESULTS_v1.csv.gz"
ROLE_SOURCE = ROOT / "03_models/modeling_phase1/q1/Q1_DESCRIPTIVE_SIGNAL_SET_v1.csv"
PREREG = ROOT / "03_models/modeling_phase1/q1/Q1_QUALITY_REPRESENTATION_FINAL_CANDIDATE_v1.md"
CONFLICT = ROOT / "01_data/audits/modeling_phase1/q1/Q1_CONFLICT_STABILITY_v1.csv"
OUT = ROOT / "03_models/modeling_phase1/q1/round4"
RUN_ID = "AUDIT-Q1-QUALITY-CLOSURE-R4-20260924-v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def role(signal: str, prior: str) -> str:
    if prior == "CORE_DESCRIPTIVE_SIGNAL":
        return "CORE"
    if prior == "SENSITIVITY_ONLY_SIGNAL":
        return "SENSITIVITY"
    if prior == "EXCLUDED_FOR_NOW":
        return "SECONDARY"
    if signal == "dsir_books":
        return "UNKNOWN"
    if signal in ("dsir_wiki", "dsir_math"):
        return "REDUNDANT"
    raise ValueError(f"Unexpected role for {signal}: {prior}")


def main() -> None:
    manifest = json.loads((INPUT / "INPUT_MANIFEST_v1.json").read_text(encoding="utf-8"))
    r3 = json.loads((R3 / "Q1_DESCRIPTIVE_QUALITY_METRICS_v1.json").read_text(encoding="utf-8"))
    if sha256(Q_INPUT) != manifest["processed"]["quality"]["sha256"]:
        raise RuntimeError("Frozen Q1 input hash changed")
    if sha256(SCORES) != r3["outputs"]["scores"]["sha256"]:
        raise RuntimeError("Round 3 DQ scores hash changed")
    if sha256(ROLE_SOURCE) != manifest["signal_set_sha256"] or not PREREG.is_file():
        raise RuntimeError("Round 4 quality representation contract not frozen")
    x = pd.read_csv(Q_INPUT, compression="gzip", dtype={"id": str, "source": str, "domain": str})
    score = pd.read_csv(SCORES, compression="gzip", dtype={"id": str, "source": str, "domain": str})
    if len(x) != len(score) or not x[["id", "source", "domain"]].equals(score[["id", "source", "domain"]]):
        raise RuntimeError("Round 3 scores do not align to Q1 feature rows")
    roles = pd.read_csv(ROLE_SOURCE, encoding="utf-8-sig")
    if len(roles) != 22 or roles["Signal ID"].duplicated().any():
        raise RuntimeError("Frozen signal roles changed")
    role_rows = [{"signal_id": r["Signal ID"],
                  "full22_role": role(r["Signal ID"], r["Use in descriptive representation?"]),
                  "DOWNSTREAM_ELIGIBILITY": r["DOWNSTREAM_ELIGIBILITY"],
                  "direction_status": r["Direction status"],
                  "unit_status": r["Unit status"],
                  "encoding": r["Compression rule"]} for _, r in roles.iterrows()]
    role_map = {r["signal_id"]: r for r in role_rows}
    counts = pd.Series([r["full22_role"] for r in role_rows]).value_counts().to_dict()
    if counts != {"SENSITIVITY": 12, "CORE": 5, "SECONDARY": 2, "REDUNDANT": 2, "UNKNOWN": 1}:
        raise RuntimeError("Full-22 role counts changed")

    is_a1 = x.source.to_numpy() == "A1"
    is_check = split_is_check(x.id)
    ref = x.loc[is_a1 & ~is_check]
    u = np.column_stack([ecdf(ref[c].to_numpy(float), x[c].to_numpy(float)) for c in CORE])
    if np.max(np.abs(u.mean(axis=1) - score.DQ0_global_core.to_numpy(float))) > 1e-12:
        raise RuntimeError("DQ0 not reproducible from frozen A1 reference")
    a1_ids = set(x.loc[is_a1, "id"])
    source = x.source.to_numpy()
    domains = x.domain.to_numpy()
    groups = {f"A1_{d}": is_a1 & (domains == d) for d in sorted(x.loc[is_a1, "domain"].unique())}
    for code in ("A2", "A3"):
        mask = source == code
        groups[code + "_all"] = mask
        groups[code + "_new_ids"] = mask & ~x.id.isin(a1_ids).to_numpy()
    if len(groups) != 11:
        raise RuntimeError("Unexpected source/domain groups")

    full_rows, core_rows, facet_rows = [], [], []
    for group_name, mask in groups.items():
        count = int(mask.sum())
        if count == 0:
            raise RuntimeError(f"Empty group {group_name}")
        for sid in roles["Signal ID"]:
            vals = x.loc[mask, sid].to_numpy(float)
            finite = vals[np.isfinite(vals)]
            rr = role_map[sid]
            full_rows.append({"group": group_name, "n_physical": count, "signal_id": sid,
                              "full22_role": rr["full22_role"],
                              "DOWNSTREAM_ELIGIBILITY": rr["DOWNSTREAM_ELIGIBILITY"],
                              "direction_status": rr["direction_status"],
                              "encoding": rr["encoding"],
                              "n_finite": len(finite), "n_nonfinite": count - len(finite),
                              "mean_diagnostic_value": float(np.mean(finite)) if len(finite) else math.nan,
                              "p25": float(np.quantile(finite, 0.25)) if len(finite) else math.nan,
                              "median": float(np.median(finite)) if len(finite) else math.nan,
                              "p75": float(np.quantile(finite, 0.75)) if len(finite) else math.nan,
                              "min": float(np.min(finite)) if len(finite) else math.nan,
                              "max": float(np.max(finite)) if len(finite) else math.nan})
        for j, sid in enumerate(CORE):
            vals = u[mask, j]
            se = float(np.std(vals, ddof=1) / math.sqrt(count)) if count > 1 else math.nan
            core_rows.append({"group": group_name, "n_physical": count, "signal_id": sid,
                              "reference": "A1_fixed_train_ECDF",
                              "mean_relative_percentile": float(np.mean(vals)),
                              "median_relative_percentile": float(np.median(vals)),
                              "p25_relative_percentile": float(np.quantile(vals, 0.25)),
                              "p75_relative_percentile": float(np.quantile(vals, 0.75)),
                              "record_level_mean_95pct_lower": float(np.mean(vals) - 1.96 * se),
                              "record_level_mean_95pct_upper": float(np.mean(vals) + 1.96 * se),
                              "interval_limit": "Within-record descriptive SE; not population/sampling-design inference"})
        for j in range(4):
            vals = x.loc[mask, f"qurater_facet_{j}"].to_numpy(float)
            facet_rows.append({"group": group_name, "n": count, "facet_index": j,
                               "facet_name": ["writing_style", "required_expertise", "facts_trivia", "educational_value"][j],
                               "median_raw_logit_or_rating": float(np.nanmedian(vals)),
                               "p25": float(np.nanquantile(vals, 0.25)),
                               "p75": float(np.nanquantile(vals, 0.75))})

    old = pd.read_csv(CONFLICT, encoding="utf-8-sig")
    conflict = old[(old.q == 0.8) &
                   old.scope.isin(["A1_all", "A2_new_ids", "A3_new_ids"])].copy()
    conflict["relation_label"] = "STATISTICAL_DISAGREEMENT_NOT_SEMANTIC_CONFLICT"
    if len(conflict) != 30:
        raise RuntimeError("Expected 10 direction-candidate pairs x 3 disjoint-source scopes")

    OUT.mkdir(parents=True, exist_ok=True)
    paths = {
        "roles": OUT / "Q1_FULL22_ROLE_MAP_v1.csv",
        "full22": OUT / "Q1_FULL22_DOMAIN_PROFILE_v1.csv",
        "core": OUT / "Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv",
        "facets": OUT / "Q1_QURATER_FACET_PROFILE_v1.csv",
        "disagreement": OUT / "Q1_STATISTICAL_DISAGREEMENT_SUMMARY_v1.csv",
    }
    pd.DataFrame(role_rows).to_csv(paths["roles"], index=False, encoding="utf-8-sig")
    pd.DataFrame(full_rows).to_csv(paths["full22"], index=False, encoding="utf-8-sig")
    pd.DataFrame(core_rows).to_csv(paths["core"], index=False, encoding="utf-8-sig")
    pd.DataFrame(facet_rows).to_csv(paths["facets"], index=False, encoding="utf-8-sig")
    conflict.to_csv(paths["disagreement"], index=False, encoding="utf-8-sig")
    meta = {
        "audit_id": RUN_ID, "status": "Q1_QUALITY_PROVISIONAL_FINAL_CANDIDATE_NOT_GATE2_VALIDATED",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)),
        "inputs": {"quality_features_sha256": sha256(Q_INPUT), "DQ_scores_sha256": sha256(SCORES),
                   "role_source_sha256": sha256(ROLE_SOURCE), "candidate_spec_sha256": sha256(PREREG)},
        "role_counts": counts, "physical_rows": len(x), "unique_ids": int(x.id.nunique()),
        "group_count": len(groups), "full22_rows": len(full_rows), "core_rows": len(core_rows),
        "facet_rows": len(facet_rows), "disagreement_rows": len(conflict),
        "outputs": {k: {"path": str(v.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(v)}
                    for k, v in paths.items()},
        "semantic_conflicts_confirmed": 0,
        "q2_identifiable_quality_variables": 0,
        "no_loss_used": True,
    }
    (OUT / "Q1_QUALITY_CLOSURE_METRICS_v1.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_id": RUN_ID, "full22_rows": len(full_rows),
                      "core_rows": len(core_rows), "role_counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
