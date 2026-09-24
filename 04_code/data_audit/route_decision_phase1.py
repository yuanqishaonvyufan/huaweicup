"""Read-only, source-traced route-decision diagnostics for F 2026 Phase 1.

This does not fit a final Q1-Q4 model or promote audit evidence to validated
research results. Raw files are never changed. Run from the project root:

    python 04_code/data_audit/route_decision_phase1.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import lzma
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data" / "raw" / "real_attachments"
OUT = ROOT / "01_data" / "audits" / "phase1"
MANIFEST = ROOT / "01_data" / "raw" / "RAW_SHA256.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def as_py(value):
    if isinstance(value, dict):
        return {str(k): as_py(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [as_py(v) for v in value]
    if isinstance(value, np.ndarray):
        return [as_py(v) for v in value.tolist()]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value, (float,)):
        return value if np.isfinite(value) else None
    return value


with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
    EXPECTED = {row["relative_path"].replace("\\", "/"): row for row in csv.DictReader(f)}
USED: dict[str, dict] = {}


def use(relative: str, verify: bool = True) -> Path:
    relative = relative.replace("\\", "/")
    path = RAW / relative
    expected = EXPECTED.get(relative)
    # One supplied C8 path exceeds the legacy Windows MAX_PATH limit.
    if not path.is_file() and len(str(path)) >= 260:
        path = Path("\\\\?\\" + str(path))
    if expected is None or not path.is_file():
        raise FileNotFoundError(f"Raw manifest/path mismatch: {relative}")
    if verify:
        actual = sha256(path)
        if actual != expected["sha256"]:
            raise ValueError(f"Raw SHA256 mismatch: {relative}")
    USED[relative] = {
        "relative_path": f"01_data/raw/real_attachments/{relative}",
        "sha256": expected["sha256"],
        "bytes": int(expected["bytes"]),
        "verified_this_run": verify,
    }
    return path


def read(relative: str) -> pd.DataFrame:
    return pd.read_csv(use(relative), low_memory=False)


def quality_file_scan(relative: str, inferred_domain: str | None = None) -> tuple[dict, set[str]]:
    path = use(relative)  # stream hash check before reading compressed JSONL
    keys = Counter()
    domains = Counter()
    rows = 0
    bad_json = 0
    run_key_rows = 0
    unique_ids: set[str] = set()
    duplicate_ids = 0
    with lzma.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                bad_json += 1
                continue
            rows += 1
            keys.update(record.keys())
            domains[str(record.get("_source_domain", inferred_domain or "MISSING"))] += 1
            if any(k in record for k in ("index", "run_id", "mixture_id", "experiment_id")):
                run_key_rows += 1
            if "id" in record:
                record_id = str(record["id"])
                duplicate_ids += int(record_id in unique_ids)
                unique_ids.add(record_id)
    return {
        "rows": rows,
        "bad_json_lines": bad_json,
        "keys": dict(keys),
        "source_domain_counts": dict(domains),
        "rows_with_candidate_run_key": run_key_rows,
        "unique_sample_ids": len(unique_ids),
        "duplicate_sample_id_rows": duplicate_ids,
    }, unique_ids


def mixture(relative: str) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    frame = read(relative)
    columns = [c for c in frame.columns if c.startswith("train_the_pile_")]
    return frame, frame[columns].to_numpy(dtype=float), columns


def loss(relative: str) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    frame = read(relative)
    columns = [c for c in frame.columns if c.endswith("_val_loss")]
    return frame, frame[columns].to_numpy(dtype=float), columns


def row_support(matrix: np.ndarray) -> dict:
    sums = matrix.sum(axis=1)
    return {
        "n_rows": len(matrix),
        "sum_min": float(sums.min()),
        "sum_median": float(np.median(sums)),
        "sum_max": float(sums.max()),
        "negative_cells": int(np.count_nonzero(matrix < 0)),
        "zero_cell_fraction": float(np.mean(matrix == 0)),
        "nonzero_domains_median": float(np.median(np.count_nonzero(matrix > 0, axis=1))),
        "pure_single_domain_rows": int(np.count_nonzero(np.count_nonzero(matrix > 0, axis=1) == 1)),
        "domain_min": matrix.min(axis=0).tolist(),
        "domain_max": matrix.max(axis=0).tolist(),
    }


def hull_membership(train: np.ndarray, targets: np.ndarray) -> dict:
    # The supplied shares are rounded; renormalization is only for this
    # geometry diagnostic. We do not rewrite or model on the raw table.
    a = train / train.sum(axis=1, keepdims=True)
    b = targets / targets.sum(axis=1, keepdims=True)
    constraints = np.vstack([a.T[:-1], np.ones(len(a))])
    inside = 0
    failed = 0
    for point in b:
        target = np.r_[point[:-1], 1.0]
        result = linprog(
            np.zeros(len(a)), A_eq=constraints, b_eq=target,
            bounds=(0, None), method="highs",
            options={"primal_feasibility_tolerance": 1e-8,
                     "dual_feasibility_tolerance": 1e-8},
        )
        if result.success:
            inside += 1
        elif result.status != 2:
            failed += 1
    return {
        "target_rows": len(b),
        "inside_observed_train_convex_hull": inside,
        "outside_observed_train_convex_hull": len(b) - inside - failed,
        "solver_uncertain": failed,
        "geometry": "17 rounded shares renormalized for 16-coordinate LP only",
    }


def hull_membership_with_rounding(train: np.ndarray, targets: np.ndarray) -> dict:
    # Shares are displayed to 0.001. Each true source/target coordinate may
    # differ by 0.0005, so 0.001 is the implied pairwise comparison envelope.
    eps = 0.001
    bounds_matrix = np.vstack([train.T, -train.T])
    inside = 0
    uncertain = 0
    for point in targets:
        result = linprog(
            np.zeros(len(train)), A_ub=bounds_matrix,
            b_ub=np.r_[point + eps, -point + eps],
            A_eq=np.ones((1, len(train))), b_eq=[1.0],
            bounds=(0, None), method="highs",
        )
        inside += bool(result.success)
        uncertain += bool(not result.success and result.status != 2)
    return {
        "printed_share_resolution": 0.001,
        "coordinate_envelope": eps,
        "target_rows": len(targets),
        "inside_or_within_rounding_envelope": inside,
        "outside_rounding_envelope": len(targets) - inside - uncertain,
        "solver_uncertain": uncertain,
    }


def audit_a() -> dict:
    prefix = "A_data_value/"
    a4, p, pcols = mixture(prefix + "regmix_tables/train_mixture_1m.csv")
    a5, y, ycols = loss(prefix + "regmix_tables/train_pile_loss_1m.csv")
    if a4["index"].duplicated().any() or a5["index"].duplicated().any():
        raise ValueError("A4/A5 index is not unique")
    paired = set(a4["index"]) == set(a5["index"])
    amap = read(prefix + "domain_mapping_guide.csv")
    summary = read(prefix + "regmix_domain_summary.csv")
    quality = {}
    quality_ids = {}
    quality_sources = (
        ("A1", "slimpajama_quality_signal_sample.jsonl.xz", None),
        ("A2", "slimpajama_quality_extended/arxiv_part-6777d8857c6e-000486.jsonl.xz", "arxiv"),
        ("A3", "slimpajama_quality_extended/github_part-6777d8857c6e-000275.jsonl.xz", "github"),
    )
    for label, name, domain in quality_sources:
        stats, ids = quality_file_scan(prefix + name, domain)
        quality[label] = {"relative_path": prefix + name, **stats}
        quality_ids[label] = ids
    if any(entry["rows_with_candidate_run_key"] for entry in quality.values()):
        raise ValueError("A1-A3 now contain a candidate run key; reassess Q matching")
    p_norm = p / p.sum(axis=1, keepdims=True)
    legal_x0 = np.column_stack([np.ones(len(p)), p_norm[:, :16]])
    x0_singular = np.linalg.svd(legal_x0, compute_uv=False)
    x0_tol = max(legal_x0.shape) * np.finfo(legal_x0.dtype).eps * x0_singular[0]
    legal_rank = int(np.count_nonzero(x0_singular > x0_tol))
    corr = np.corrcoef(y, rowvar=False)
    pair_corr = corr[np.triu_indices(len(ycols), 1)]
    z = (y - y.mean(axis=0)) / y.std(axis=0, ddof=0)
    singular = np.linalg.svd(z, compute_uv=False)
    variance = singular ** 2 / np.sum(singular ** 2)
    holdouts = {}
    holdout_arrays = {}
    for stem in ("test_mixture_1m", "test_mixture_60m", "test_mixture_1B"):
        f, x, cols = mixture(prefix + f"regmix_tables/{stem}.csv")
        if cols != pcols:
            raise ValueError(f"p columns differ: {stem}")
        holdouts[stem] = {"count": len(f), "index_unique": int(f["index"].nunique()),
                          "support": row_support(x)}
        holdout_arrays[stem] = x
    for stem in ("test_pile_loss_1m", "test_pile_loss_60m", "test_pile_loss_1B"):
        f, _, cols = loss(prefix + f"regmix_tables/{stem}.csv")
        holdouts[stem] = {"count": len(f), "index_unique": int(f["index"].nunique()),
                          "same_response_columns": cols == ycols}
    holdouts["test_mixture_1m"]["hull"] = hull_membership(p, holdout_arrays["test_mixture_1m"])
    holdouts["test_mixture_1m"]["rounding_aware_hull"] = hull_membership_with_rounding(
        p, holdout_arrays["test_mixture_1m"])
    holdouts["test_mixture_60m"]["same_shares_as_1m"] = bool(
        np.array_equal(holdout_arrays["test_mixture_1m"], holdout_arrays["test_mixture_60m"]))
    holdouts["test_mixture_1B"]["hull"] = hull_membership(p, holdout_arrays["test_mixture_1B"])
    holdouts["test_mixture_1B"]["rounding_aware_hull"] = hull_membership_with_rounding(
        p, holdout_arrays["test_mixture_1B"])
    return {
        "A4_A5": {
            "p_rows": len(a4), "loss_rows": len(a5), "paired_index_sets_equal": paired,
            "p_unique_index": int(a4["index"].nunique()),
            "loss_unique_index": int(a5["index"].nunique()),
            "p_columns": pcols, "loss_columns": ycols,
            "p_support": row_support(p), "legal_simplex_X0_rank": legal_rank,
            "legal_simplex_X0_columns": 17,
            "legal_simplex_X0_singular_values": x0_singular.tolist(),
            "legal_simplex_X0_svd_tolerance": float(x0_tol),
            "legal_simplex_X0_svd_tolerance_method": "max(matrix_shape) * float64_epsilon * largest_singular_value",
            "quality_run_column_present": bool(set(a4.columns) & {"Q", "Q_score", "quality", "run_q"}),
        },
        "quality_files": quality,
        "quality_sample_id_overlap": {
            "A1_A2": len(quality_ids["A1"] & quality_ids["A2"]),
            "A1_A3": len(quality_ids["A1"] & quality_ids["A3"]),
            "A2_A3": len(quality_ids["A2"] & quality_ids["A3"]),
        },
        "A16_mapping": {"rows": len(amap), "mapping_types": amap["mapping_type"].value_counts().to_dict(),
                         "quality_domains": sorted(set(amap["quality_domain"]) - {"(none)"})},
        "domain_summary_rows": len(summary),
        "loss_structure_train_only": {
            "n_domains": len(ycols), "missing_cells": int(np.isnan(y).sum()),
            "means": dict(zip(ycols, y.mean(axis=0).tolist())),
            "stds": dict(zip(ycols, y.std(axis=0, ddof=1).tolist())),
            "pairwise_corr_min": float(pair_corr.min()),
            "pairwise_corr_median": float(np.median(pair_corr)),
            "pairwise_corr_max": float(pair_corr.max()),
            "negative_pair_count": int(np.count_nonzero(pair_corr < 0)),
            "pair_count": len(pair_corr),
            "standardized_pca_variance_first_3": variance[:3].tolist(),
        },
        "heldout_schema_and_p_support_only": holdouts,
    }


def audit_b() -> dict:
    prefix = "B_scaling_laws/"
    b1 = read(prefix + "pythia_training_log_existing.csv")
    b4 = read(prefix + "scaling_baseline.csv")
    b5 = read(prefix + "published_scaling_data.csv")
    files = {}
    dfs = {}
    for name in ("supplementary_NQ_experiment.csv",
                 "supplementary_NQ_experiment_expanded.csv",
                 "supplementary_NQ_experiment_large.csv"):
        df = read(prefix + name)
        dfs[name] = df
        groups = df.groupby(["N_params_B", "D_tokens_B"], dropna=False)
        quality_levels = groups["Q_score"].nunique()
        slope_signs = []
        for _, g in groups:
            if g["Q_score"].nunique() > 1:
                slope_signs.append(float(np.polyfit(g["Q_score"], g["val_loss"], 1)[0]))
        design = np.column_stack([np.ones(len(df)), np.log(df["N_params_B"]),
                                  np.log(df["D_tokens_B"]), df["Q_score"]])
        files[name] = {
            "rows": len(df), "unique_experiment_id": int(df["experiment_id"].nunique()),
            "N_levels": int(df["N_params_B"].nunique()),
            "D_levels": int(df["D_tokens_B"].nunique()),
            "Q_levels": int(df["Q_score"].nunique()),
            "Q_range": [float(df["Q_score"].min()), float(df["Q_score"].max())],
            "N_range_B": [float(df["N_params_B"].min()), float(df["N_params_B"].max())],
            "D_range_B": [float(df["D_tokens_B"].min()), float(df["D_tokens_B"].max())],
            "missing_cells": int(df.isna().sum().sum()),
            "base_design_rank_intercept_logN_logD_Q": int(np.linalg.matrix_rank(design)),
            "Q_levels_per_ND_min_max": [int(quality_levels.min()), int(quality_levels.max())],
            "within_ND_quality_loss_slope_negative_fraction": float(np.mean(np.array(slope_signs) < 0)),
            "within_ND_quality_loss_slope_min_median_max":
                [float(np.min(slope_signs)), float(np.median(slope_signs)), float(np.max(slope_signs))],
            "data_type_counts": df["data_type"].value_counts().to_dict() if "data_type" in df else {},
        }
    keys = ["N_params_B", "D_tokens_B", "Q_score"]
    joined_67 = pd.merge(dfs["supplementary_NQ_experiment.csv"],
                         dfs["supplementary_NQ_experiment_expanded.csv"],
                         on=keys, suffixes=("_B6", "_B7"))
    joined_78 = pd.merge(dfs["supplementary_NQ_experiment_expanded.csv"],
                         dfs["supplementary_NQ_experiment_large.csv"],
                         on=keys, suffixes=("_B7", "_B8"))
    return {
        "B1": {"rows": len(b1), "row_id_count": int(b1["run_id"].nunique()),
               "independent_model_size_levels": int(b1.N_params_B.nunique()),
               "checkpoints_per_size_min_max": [int(b1.groupby("N_params_B").size().min()),
                                                int(b1.groupby("N_params_B").size().max())],
               "N_range_B": [float(b1.N_params_B.min()), float(b1.N_params_B.max())],
               "D_range_B": [float(b1.D_tokens_B.min()), float(b1.D_tokens_B.max())],
               "val_loss_range": [float(b1.val_loss.min()), float(b1.val_loss.max())],
               "has_validation_corpus_column": any("corpus" in x.lower() or "tokenizer" in x.lower()
                                                    for x in b1.columns)},
        "B4": {"rows": len(b4), "families": int(b4.family.nunique()),
               "has_validation_corpus_column": any("corpus" in x.lower() or "tokenizer" in x.lower()
                                                    for x in b4.columns)},
        "B5": {"rows": len(b5), "families": int(b5.family.nunique()),
               "has_validation_corpus_column": any("corpus" in x.lower() or "tokenizer" in x.lower()
                                                    for x in b5.columns)},
        "B6_B8": files,
        "grid_overlap_B6_B7": len(joined_67),
        "B6_B7_overlap_loss_max_abs_diff": float((joined_67.val_loss_B6 - joined_67.val_loss_B7).abs().max()),
        "grid_overlap_B7_B8": len(joined_78),
        "B7_B8_overlap_loss_median_abs_diff": float((joined_78.val_loss_B7 - joined_78.val_loss_B8).abs().median()),
        "B7_B8_overlap_loss_correlation": float(joined_78[["val_loss_B7", "val_loss_B8"]].corr().iloc[0, 1]),
    }


def parse_dates(frame: pd.DataFrame, column: str) -> dict:
    dates = pd.to_datetime(frame[column], errors="coerce")
    valid = dates.dropna()
    return {"valid": len(valid), "missing_or_invalid": int(dates.isna().sum()),
            "earliest": str(valid.min().date()) if len(valid) else None,
            "latest": str(valid.max().date()) if len(valid) else None}


def audit_c() -> dict:
    prefix = "C_efficiency_evolution/"
    arch = read(prefix + "model_architecture_metadata.csv")
    clean = read(prefix + "leaderboard_cleaned.csv")
    enhanced = read(prefix + "leaderboard_enhanced.csv")
    history = read(prefix + "leaderboard_extended_timeseries.csv")
    epoch = read(prefix + "epoch_all_ai_models.csv")
    bridge = read(prefix + "loss_benchmark_bridge.csv")
    bridge_ex = read(prefix + "loss_benchmark_bridge_expanded.csv")
    lengths = arch["max_position_embeddings"].astype(int)
    benchmark_cols = ["IFEval", "BBH", "MATH Lvl 5", "GPQA", "MUSR", "MMLU-PRO"]
    leaderboard_models = set(clean["Model"].dropna().astype(str))
    epoch_models = set(epoch["Model"].dropna().astype(str))
    c8_root = RAW / prefix / "detailed_results"
    detail_files = sorted(c8_root.glob("*/results*.json"))
    detail_models = Counter()
    task_counts = []
    broken = []
    details = []
    for path in detail_files:
        rel = path.relative_to(RAW).as_posix()
        readable_path = use(rel, verify=False)  # covered by init manifest
        try:
            with readable_path.open(encoding="utf-8") as f:
                record = json.load(f)
            name = str(record.get("model_name", ""))
            detail_models[name] += 1
            task_counts.append(len(record.get("results", {})))
            details.append({"relative_path": rel, "sha256": EXPECTED[rel]["sha256"],
                            "model_name": name, "task_count": task_counts[-1]})
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
            broken.append({"relative_path": rel, "error": type(exc).__name__,
                           "bytes": int(EXPECTED[rel]["bytes"]), "sha256": EXPECTED[rel]["sha256"]})
    detail_manifest = OUT / "C8_file_manifest.json"
    detail_manifest.write_text(json.dumps(details, ensure_ascii=False, indent=2), encoding="utf-8")
    if len(detail_files) + len(broken) == 0:
        raise ValueError("No C8 files found")
    def bridge_stats(df: pd.DataFrame) -> dict:
        high = df["Loss_Comparability"].astype(str).str.startswith("High")
        return {"rows": len(df), "unique_models": int(df["Model"].nunique()),
                "comparability": df["Loss_Comparability"].value_counts(dropna=False).to_dict(),
                "high_family_prefixes": df.loc[high, "Model"].astype(str).str.split("/").str[0].value_counts().to_dict(),
                "exact_leaderboard_matches": int(df["Model"].isin(leaderboard_models).sum()),
                "complete_loss_and_benchmark": int(df[["Val_Loss", "LB_Average"]].notna().all(axis=1).sum())}
    return {
        "C7": {"rows": len(arch), "unique_models": int(arch.model_name.nunique()),
               "length_counts": {str(k): int(v) for k, v in lengths.value_counts().sort_index().items()},
               "length_min_max": [int(lengths.min()), int(lengths.max())],
               "architecture_caps_at_least_30000": int((lengths >= 30000).sum()),
               "training_context_length_column_present": any("training_context" in c.lower()
                                                             for c in arch.columns)},
        "C1": {"rows": len(clean), "unique_models": int(clean.Model.nunique()),
               "duplicate_model_rows": int(clean.Model.duplicated().sum()),
               "dates": parse_dates(clean, "Submission Date"),
               "all_six_benchmarks_present": int(clean[benchmark_cols].notna().all(axis=1).sum()),
               "param_B_present": int(clean["#Params (B)"].notna().sum()),
               "license_present": int(clean["Hub License"].notna().sum()),
               "type_counts": clean["Type"].value_counts(dropna=False).to_dict()},
        "C2": {"rows": len(enhanced), "unique_models": int(enhanced.Model.nunique()),
               "epoch_date_present": int(enhanced["Epoch_AI_Publication_Date"].notna().sum()),
               "epoch_open_weights_present": int(enhanced["Epoch_AI_Open_Weights"].notna().sum())},
        "C3": {"rows": len(history), "unique_models": int(history.Model.nunique()),
               "source_counts": history.Source.value_counts(dropna=False).to_dict(),
               "year_range": [int(history.Year.min()), int(history.Year.max())]},
        "C4": {"rows": len(epoch), "unique_models": int(epoch.Model.nunique()),
               "dates": parse_dates(epoch, "Publication date"),
               "exact_C1_model_name_overlap": len(epoch_models & leaderboard_models),
               "parameters_present": int(epoch.Parameters.notna().sum()),
               "training_compute_present": int(epoch["Training compute (FLOP)"].notna().sum()),
               "training_dataset_size_present": int(epoch["Training dataset size (total)"].notna().sum()),
               "open_weights_present": int(epoch["Open model weights?"].notna().sum())},
        "C5": bridge_stats(bridge), "C6": bridge_stats(bridge_ex),
        "C5_models_subset_C6": set(bridge.Model.astype(str)).issubset(set(bridge_ex.Model.astype(str))),
        "C8": {"files_found": len(detail_files), "files_parsed": len(details),
               "files_broken": len(broken), "broken_examples": broken[:20],
               "unique_model_names": len(detail_models),
               "duplicate_model_files": sum(n - 1 for n in detail_models.values()),
               "exact_C1_model_name_overlap": len(set(detail_models) & leaderboard_models),
               "task_count_min_max": [min(task_counts), max(task_counts)] if task_counts else None,
               "per_file_hash_manifest": str(detail_manifest.relative_to(ROOT)),
               "per_file_hash_manifest_sha256": sha256(detail_manifest)},
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    a = audit_a()
    print("A audit measures complete", flush=True)
    b = audit_b()
    print("B audit measures complete", flush=True)
    c = audit_c()
    print("C audit measures complete", flush=True)
    payload = {
        "audit_id": "F2026-ROUTE-PHASE1-20260923",
        "status": "AUDIT_EVIDENCE",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_relative_path": str(Path(__file__).relative_to(ROOT)),
        "script_sha256": sha256(Path(__file__)),
        "raw_manifest_sha256": sha256(MANIFEST),
        "input_paths_and_sha256": list(USED.values()),
        "A": a, "B": b, "C": c,
    }
    path = OUT / "route_audit_metrics.json"
    path.write_text(json.dumps(as_py(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {path}", flush=True)
    summary = {
        "audit_id": "F2026-AUDIT-01-20260923",
        "audit_evidence_path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "audit_evidence_sha256": sha256(path),
        "score_version": "NONE",
        "score_provenance_valid": True,
        "score_provenance_id": "RAW-SIGNAL-PROVENANCE-ONLY: source_manifest.json and RAW_SHA256.csv; no Q score constructed",
        "score_uses_target_loss": False,
        "nested_crossfit_valid": False,
        "paired_quality_available": False,
        "deterministic_from_p_fixed_q": False,
        "rank_state": "NOT_TESTED",
        "precision_state": "NOT_CALIBRATED",
        "support_state": "NOT_CALIBRATED",
        "oos_gain_state": "NOT_TESTED",
        "quality_evidence_source": "REAL_DIRECT",
        "paired_p_loss_rows": a["A4_A5"]["p_rows"] if a["A4_A5"]["paired_index_sets_equal"] else 0,
        "paired_p_Q_loss_rows": 0,
        "rank_X0_legal_simplex": a["A4_A5"]["legal_simplex_X0_rank"],
        "rank_Xfull": "NOT_TESTED: no matched run-level Q",
        "qualification": "score_provenance_valid refers only to traceable raw quality-signal files; it does not assert a constructed or validated Q score.",
    }
    summary_path = OUT / "identifiability_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    subprocess.run([
        sys.executable, str(ROOT / "04_code" / "utils" / "identifiability_decision.py"),
        "--input", str(summary_path),
        "--output", str(OUT / "identifiability_branch.json"),
    ], check=True, capture_output=True, text=True)
    print("AUDIT-01 branch decision saved", flush=True)


if __name__ == "__main__":
    main()
