"""Evaluate frozen Round 4 p models on A6-A11; no retraining or tuning."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linprog
from scipy.spatial import cKDTree
from scipy.stats import spearmanr

from round4_train_p_response import predict


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data/raw/real_attachments"
RAW_MANIFEST = ROOT / "01_data/raw/RAW_SHA256.csv"
OUT = ROOT / "03_models/modeling_phase1/q1/round4"
BUNDLE = OUT / "P_RESPONSE_FROZEN_MODEL_BUNDLE_v1.json"
TRAIN_META = OUT / "P_RESPONSE_TRAIN_METRICS_v1.json"
CONTRACT = OUT / "P_RESPONSE_PREFIT_CONTRACT_v1.md"
ADDENDUM = OUT / "P_RESPONSE_VALIDATION_RULE_ADDENDUM_v1.md"
R3_DOMAINS = ROOT / "03_models/modeling_phase1/q1/round3/DOMAIN_HETEROGENEITY_RESULTS_v1.csv"
RUN_ID = "VAL-Q1-PRESP-A6A11-R4-20260924-v2"
SEED = 20260924
BOOTSTRAP = 500
PAIRS = [
    ("1M", "A6", "A7", "A_data_value/regmix_tables/test_mixture_1m.csv",
     "A_data_value/regmix_tables/test_pile_loss_1m.csv", 256),
    ("60M", "A8", "A9", "A_data_value/regmix_tables/test_mixture_60m.csv",
     "A_data_value/regmix_tables/test_pile_loss_60m.csv", 256),
    ("1B", "A10", "A11", "A_data_value/regmix_tables/test_mixture_1B.csv",
     "A_data_value/regmix_tables/test_pile_loss_1B.csv", 64),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def json_safe(value):
    """Convert NumPy scalars and nonfinite diagnostics to strict JSON values."""
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def decode_model(source: dict) -> dict:
    arrays = {"pmean", "ymean", "coef", "pc", "sqmean"}
    return {k: np.asarray(v, dtype=float) if k in arrays and v is not None else v
            for k, v in source.items()}


def read_pair(p_rel: str, y_rel: str, n: int, p_cols: list[str],
              y_cols: list[str], hashes: dict[str, str]) -> dict:
    for relative in (p_rel, y_rel):
        if hashes.get(relative) != sha256(RAW / relative):
            raise RuntimeError(f"Official validation mapping/hash mismatch: {relative}")
    pf = pd.read_csv(RAW / p_rel)
    yf = pd.read_csv(RAW / y_rel)
    if len(pf) != n or len(yf) != n:
        raise RuntimeError("Unexpected A6-A11 row count")
    if list(pf.columns) != ["index", *p_cols] or list(yf.columns) != ["index", *y_cols]:
        raise RuntimeError("Unexpected A6-A11 fields")
    if pf["index"].duplicated().any() or yf["index"].duplicated().any():
        raise RuntimeError("Repeated validation run index")
    joined = pf.merge(yf, on="index", validate="one_to_one").sort_values("index")
    if len(joined) != n:
        raise RuntimeError("Validation p/Loss pairing failed")
    raw_p = joined[p_cols].to_numpy(float)
    y = joined[y_cols].to_numpy(float)
    if (raw_p < 0).any() or not np.isfinite(raw_p).all() or not np.isfinite(y).all():
        raise RuntimeError("Invalid validation numeric cell")
    sums = raw_p.sum(axis=1)
    if sums.min() < 0.99 or sums.max() > 1.01:
        raise RuntimeError("Validation p sum outside rounding correction")
    return {"index": joined["index"].to_numpy(), "p": raw_p / sums[:, None], "y": y,
            "p_path": p_rel, "y_path": y_rel,
            "p_sha256": hashes[p_rel], "y_sha256": hashes[y_rel],
            "raw_sum_min": float(sums.min()), "raw_sum_max": float(sums.max()),
            "max_abs_normalization_change": float(np.max(np.abs(raw_p / sums[:, None] - raw_p)))}


def support_reference(train_p: np.ndarray, basis: np.ndarray) -> dict:
    pmean = train_p.mean(axis=0)
    z = (train_p - pmean) @ basis
    tree = cKDTree(z)
    loo, _ = tree.query(z, k=2)
    _, singular, vt = np.linalg.svd(z, full_matrices=False)
    share = singular ** 2 / np.sum(singular ** 2)
    k95 = int(np.searchsorted(np.cumsum(share), 0.95) + 1)
    low_basis = vt[:k95].T
    resid = np.linalg.norm(z - (z @ low_basis) @ low_basis.T, axis=1)
    return {"pmean": pmean, "tree": tree, "nn_q95": float(np.quantile(loo[:, 1], 0.95)),
            "nn_q99": float(np.quantile(loo[:, 1], 0.99)),
            "pmin": train_p.min(axis=0), "pmax": train_p.max(axis=0),
            "pca_k95": k95, "pca_share_k95": float(share[:k95].sum()),
            "low_basis": low_basis, "low_resid_q95": float(np.quantile(resid, 0.95))}


def hull_membership(train_p: np.ndarray, targets: np.ndarray) -> tuple[list[dict], int]:
    unique, inverse = np.unique(np.round(targets, 12), axis=0, return_inverse=True)
    records = []
    for target in unique:
        res = linprog(np.zeros(len(train_p)), A_eq=train_p.T, b_eq=target,
                      bounds=(0, None), method="highs")
        if res.status not in (0, 2):
            raise RuntimeError(f"Hull LP undecided: {res.status} {res.message}")
        if res.success:
            gap = float(np.max(np.abs(train_p.T @ res.x - target)))
            sum_gap = abs(float(np.sum(res.x)) - 1)
            feasible = gap <= 1e-7 and sum_gap <= 1e-7
        else:
            gap, sum_gap, feasible = math.nan, math.nan, False
        records.append({"feasible": bool(feasible), "lp_status": int(res.status),
                        "max_reconstruction_gap": gap, "weight_sum_gap": sum_gap})
    return [records[i] for i in inverse], len(unique)


def support_for(train_p: np.ndarray, target: np.ndarray, basis: np.ndarray,
                reference: dict, hull: list[dict]) -> list[dict]:
    z = (target - reference["pmean"]) @ basis
    distance, _ = reference["tree"].query(z, k=1)
    low_resid = np.linalg.norm(z - (z @ reference["low_basis"]) @ reference["low_basis"].T, axis=1)
    bound_violation = np.sum((target < reference["pmin"] - 1e-9) |
                             (target > reference["pmax"] + 1e-9), axis=1)
    rows = []
    for i, check in enumerate(hull):
        inside = check["feasible"]
        if inside and distance[i] <= reference["nn_q95"]:
            category = "IN_SUPPORT"
        elif inside or distance[i] <= reference["nn_q99"]:
            category = "NEAR_SUPPORT"
        else:
            category = "OUT_OF_SUPPORT"
        rows.append({"support_class": category, "in_observed_convex_hull": inside,
                     "hull_lp_status": check["lp_status"],
                     "hull_reconstruction_gap": check["max_reconstruction_gap"],
                     "nearest_train_helmert_distance": float(distance[i]),
                     "NN_distance_ratio_to_train_q95": float(distance[i] / reference["nn_q95"]),
                     "empirical_bound_violation_count": int(bound_violation[i]),
                     "lowdim_reconstruction_residual": float(low_resid[i]),
                     "lowdim_residual_ratio_to_train_q95": float(low_resid[i] / reference["low_resid_q95"])
                     if reference["low_resid_q95"] > 0 else math.nan})
    return rows


def rank_rho(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 4 or np.unique(a).size < 2 or np.unique(b).size < 2:
        return math.nan
    return float(spearmanr(a, b).statistic)


def metrics(y: np.ndarray, pred: np.ndarray, baseline: np.ndarray,
            train_sd: np.ndarray, same_scale: bool) -> dict:
    err = y - pred
    c_err = (y - y.mean(axis=0)) - (pred - pred.mean(axis=0))
    c_base = (y - y.mean(axis=0)) - (baseline - baseline.mean(axis=0))
    domain_rmse = np.sqrt(np.mean(err ** 2, axis=0))
    c_domain_rmse = np.sqrt(np.mean(c_err ** 2, axis=0))
    c_base_rmse = np.sqrt(np.mean(c_base ** 2, axis=0))
    r0_y, r0_pred = y.mean(axis=1), pred.mean(axis=1)
    r0_err = r0_y - r0_pred
    c_r0_err = (r0_y - r0_y.mean()) - (r0_pred - r0_pred.mean())
    c_r0_base = r0_y - r0_y.mean()
    rank_values = [rank_rho(y[:, j], pred[:, j]) for j in range(y.shape[1])]
    finite_rank_values = [v for v in rank_values if np.isfinite(v)]
    return {
        "R0_MAE_raw": float(np.mean(np.abs(r0_err))),
        "R0_RMSE_raw": float(np.sqrt(np.mean(r0_err ** 2))),
        "mean_domain_RMSE_raw": float(domain_rmse.mean()),
        "mean_domain_train_std_RMSE_raw": float(np.mean(domain_rmse / train_sd)),
        "R0_centered_RMSE": float(np.sqrt(np.mean(c_r0_err ** 2))),
        "R0_centered_RMSE_ratio_to_M0": float(np.sqrt(np.mean(c_r0_err ** 2)) /
                                               np.sqrt(np.mean(c_r0_base ** 2))),
        "mean_domain_centered_RMSE_ratio_to_M0": float(np.mean(c_domain_rmse /
                                                               np.maximum(c_base_rmse, 1e-12))),
        "R0_rank_spearman": rank_rho(r0_y, r0_pred),
        "domain_rank_spearman_mean": float(np.mean(finite_rank_values)) if finite_rank_values else math.nan,
        "same_scale_absolute_prediction_eligible": bool(same_scale),
        "domain_RMSE_raw": domain_rmse.tolist(),
        "domain_centered_RMSE": c_domain_rmse.tolist(),
        "domain_centered_RMSE_ratio_to_M0": (c_domain_rmse /
                                             np.maximum(c_base_rmse, 1e-12)).tolist(),
    }


def bootstrap_delta(y: np.ndarray, pred: np.ndarray, control: np.ndarray,
                    train_sd: np.ndarray, rng: np.random.Generator) -> dict:
    r0_diff = (y.mean(axis=1) - pred.mean(axis=1)) ** 2 - (
        y.mean(axis=1) - control.mean(axis=1)) ** 2
    domain_diff = np.mean(((y - pred) / train_sd) ** 2 -
                          ((y - control) / train_sd) ** 2, axis=1)
    b_r0, b_domain = [], []
    for _ in range(BOOTSTRAP):
        take = rng.integers(0, len(y), size=len(y))
        b_r0.append(float(r0_diff[take].mean()))
        b_domain.append(float(domain_diff[take].mean()))
    return {"R0_MSE_model_minus_control": float(r0_diff.mean()),
            "R0_boot_p025": float(np.quantile(b_r0, 0.025)),
            "R0_boot_p975": float(np.quantile(b_r0, 0.975)),
            "domain_std_MSE_model_minus_control": float(domain_diff.mean()),
            "domain_boot_p025": float(np.quantile(b_domain, 0.025)),
            "domain_boot_p975": float(np.quantile(b_domain, 0.975)),
            "stable_two_layer_gain": bool(np.quantile(b_r0, 0.975) < 0 and
                                          np.quantile(b_domain, 0.975) < 0)}


def main() -> None:
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    train_meta = json.loads(TRAIN_META.read_text(encoding="utf-8"))
    if bundle["status"] != "FROZEN_BEFORE_A6_A11_VALIDATION" or bundle["A6_A11_loss_read"] is not False:
        raise RuntimeError("Training model not frozen")
    if sha256(BUNDLE) != train_meta["bundle_sha256"] or sha256(CONTRACT) != bundle["contract_sha256"]:
        raise RuntimeError("Training bundle/contract hash changed")
    if sha256(ROOT / "04_code/modeling_phase1/round4_train_p_response.py") != bundle["training_script_sha256"]:
        raise RuntimeError("Training script changed after freeze")
    if not ADDENDUM.is_file():
        raise RuntimeError("Validation decision addendum missing")
    with RAW_MANIFEST.open(encoding="utf-8-sig", newline="") as stream:
        hashes = {r["relative_path"]: r["sha256"] for r in csv.DictReader(stream)}
    basis = np.asarray(bundle["basis"], dtype=float)
    train_p = np.asarray(bundle["training_p_matrix"], dtype=float)
    if basis.shape != (17, 16) or train_p.shape != (512, 17):
        raise RuntimeError("Frozen training geometry mismatch")
    models = {name: decode_model(item) for name, item in bundle["models"].items()}
    if not {"M0", "M1"} <= set(models):
        raise RuntimeError("Required models missing")
    reference = support_reference(train_p, basis)

    loaded, official_map = {}, {}
    for scale, pid, yid, p_rel, y_rel, count in PAIRS:
        item = read_pair(p_rel, y_rel, count, bundle["p_columns"], bundle["loss_columns"], hashes)
        loaded[scale] = item
        official_map[pid] = {"path": p_rel, "sha256": item["p_sha256"], "role": "validation_composition"}
        official_map[yid] = {"path": y_rel, "sha256": item["y_sha256"], "role": "validation_loss"}
    if not np.array_equal(loaded["1M"]["index"], loaded["60M"]["index"]) or not np.allclose(
            loaded["1M"]["p"], loaded["60M"]["p"], atol=1e-12, rtol=0):
        raise RuntimeError("A6/A8 shared p support changed")

    all_p = np.vstack([loaded[s]["p"] for s in ("1M", "60M", "1B")])
    hull, n_unique = hull_membership(train_p, all_p)
    offset = 0
    for scale in ("1M", "60M", "1B"):
        item = loaded[scale]
        n = len(item["p"])
        item["support"] = support_for(train_p, item["p"], basis, reference, hull[offset:offset+n])
        offset += n

    domain_names = [x.removeprefix("metric/the_pile_").removesuffix("_val_loss")
                    for x in bundle["loss_columns"]]
    train_sd = np.asarray(bundle["response_sd_ddof1"], dtype=float)
    response_mean = np.asarray(bundle["response_mean"], dtype=float)
    r2_loadings = pd.read_csv(R3_DOMAINS).R2_PC1_loading.to_numpy(float)
    metric_rows, domain_rows, support_rows, support_metric_rows, prediction_rows = [], [], [], [], []
    all_metrics, all_preds = {}, {}
    for scale in ("1M", "60M", "1B"):
        item = loaded[scale]
        p, y, index = item["p"], item["y"], item["index"]
        support = item["support"]
        preds = {name: predict(model, p, basis) for name, model in models.items()}
        all_preds[scale] = preds
        base = preds["M0"]
        all_metrics[scale] = {}
        for name in (key for key in ("M0", "M1", "M2", "M3") if key in preds):
            pred = preds[name]
            met = metrics(y, pred, base, train_sd, scale == "1M")
            distance = np.array([s["nearest_train_helmert_distance"] for s in support])
            raw_abs = np.abs(y.mean(axis=1) - pred.mean(axis=1))
            centered_abs = np.abs((y.mean(axis=1) - y.mean()) -
                                  (pred.mean(axis=1) - pred.mean()))
            met["distance_vs_R0_abs_error_spearman"] = rank_rho(
                distance, raw_abs if scale == "1M" else centered_abs)
            all_metrics[scale][name] = met
            metric_rows.append({"scale": scale, "model": name, "n": len(y),
                                **{k: met[k] for k in (
                                    "R0_MAE_raw", "R0_RMSE_raw", "mean_domain_RMSE_raw",
                                    "mean_domain_train_std_RMSE_raw", "R0_centered_RMSE",
                                    "R0_centered_RMSE_ratio_to_M0",
                                    "mean_domain_centered_RMSE_ratio_to_M0",
                                    "R0_rank_spearman", "distance_vs_R0_abs_error_spearman")},
                                "same_scale_absolute_prediction_eligible": scale == "1M"})
            for j, domain in enumerate(domain_names):
                m0_rmse = all_metrics[scale]["M0"]["domain_RMSE_raw"][j]
                domain_rows.append({"scale": scale, "model": name, "domain": domain, "n": len(y),
                                    "RMSE_raw": met["domain_RMSE_raw"][j],
                                    "RMSE_ratio_to_M0_raw": met["domain_RMSE_raw"][j] / m0_rmse,
                                    "RMSE_centered": met["domain_centered_RMSE"][j],
                                    "RMSE_centered_ratio_to_M0": met["domain_centered_RMSE_ratio_to_M0"][j],
                                    "rank_spearman": rank_rho(y[:, j], pred[:, j])})
            for category in ("IN_SUPPORT", "NEAR_SUPPORT", "OUT_OF_SUPPORT"):
                mask = np.array([s["support_class"] == category for s in support])
                r0_err = y.mean(axis=1) - pred.mean(axis=1)
                centered = (y.mean(axis=1) - y.mean()) - (pred.mean(axis=1) - pred.mean())
                support_metric_rows.append({
                    "scale": scale, "model": name, "support_class": category, "n": int(mask.sum()),
                    "R0_RMSE_raw": float(np.sqrt(np.mean(r0_err[mask] ** 2))) if mask.any() else math.nan,
                    "R0_RMSE_centered_global_offset": float(np.sqrt(np.mean(centered[mask] ** 2)))
                    if mask.any() else math.nan})
        for i, run_id in enumerate(index):
            record = {"scale": scale, "index": int(run_id), **support[i],
                      "R0_observed": float(y[i].mean())}
            for j, domain in enumerate(domain_names):
                record["observed_" + domain] = float(y[i, j])
            for name, pred in preds.items():
                record[name + "_R0_pred"] = float(pred[i].mean())
                for j, domain in enumerate(domain_names):
                    record[name + "_pred_" + domain] = float(pred[i, j])
            prediction_rows.append(record)
            support_rows.append({"scale": scale, "index": int(run_id), **support[i]})

    y1 = loaded["1M"]["y"]
    sensitivity = {}
    for name, pred in all_preds["1M"].items():
        yz, pz = (y1 - response_mean) / train_sd, (pred - response_mean) / train_sd
        sensitivity[name] = {
            "R1_RMSE": float(np.sqrt(np.mean((yz.mean(axis=1) - pz.mean(axis=1)) ** 2))),
            "R2_RMSE": float(np.sqrt(np.mean((yz @ r2_loadings - pz @ r2_loadings) ** 2)))}

    rng = np.random.default_rng(SEED)
    comparisons = {}
    preferred = "M0"
    for candidate in (name for name in ("M1", "M2", "M3") if name in models):
        control = preferred
        result = bootstrap_delta(y1, all_preds["1M"][candidate],
                                 all_preds["1M"][control], train_sd, rng)
        ratio = np.asarray(all_metrics["1M"][candidate]["domain_RMSE_raw"]) / np.asarray(
            all_metrics["1M"][control]["domain_RMSE_raw"])
        result["control"] = control
        result["max_domain_RMSE_ratio_to_control"] = float(np.max(ratio))
        result["catastrophic_domain_degradation"] = bool(np.any(ratio > 1.5))
        result["adopted"] = bool(result["stable_two_layer_gain"] and
                                 not result["catastrophic_domain_degradation"])
        comparisons[candidate] = result
        if result["adopted"]:
            preferred = candidate

    paths = {"predictions": OUT / "P_RESPONSE_VALIDATION_PREDICTIONS_v2.csv",
             "metrics": OUT / "P_RESPONSE_VALIDATION_METRICS_v2.csv",
             "domains": OUT / "P_RESPONSE_DOMAIN_VALIDATION_v2.csv",
             "support": OUT / "P_SUPPORT_VALIDATION_ROWS_v2.csv",
             "support_metrics": OUT / "P_RESPONSE_SUPPORT_STRATA_v2.csv"}
    for key, rows in (("predictions", prediction_rows), ("metrics", metric_rows),
                      ("domains", domain_rows), ("support", support_rows),
                      ("support_metrics", support_metric_rows)):
        pd.DataFrame(rows).to_csv(paths[key], index=False, encoding="utf-8-sig")

    result = {
        "run_id": RUN_ID, "status": "OUT_OF_SAMPLE_VALIDATION_CHECKED_PENDING_GATE2",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)), "train_bundle_sha256": sha256(BUNDLE),
        "training_contract_sha256": sha256(CONTRACT), "validation_addendum_sha256": sha256(ADDENDUM),
        "official_mapping": official_map,
        "validation_counts": {scale: len(item["index"]) for scale, item in loaded.items()},
        "A6_A8_identical_p": True,
        "support_thresholds": {
            "train_loo_NN_q95": reference["nn_q95"], "train_loo_NN_q99": reference["nn_q99"],
            "train_PCA_k95": reference["pca_k95"], "train_PCA_variance_share_k95": reference["pca_share_k95"],
            "train_PCA_residual_q95": reference["low_resid_q95"]},
        "support_counts": {scale: {k: int(v) for k, v in pd.Series(
            [s["support_class"] for s in item["support"]]).value_counts().items()}
                           for scale, item in loaded.items()},
        "hull_unique_p_count": n_unique,
        "metrics": all_metrics, "R1_R2_1M_sensitivity": sensitivity,
        "model_comparisons_1M": comparisons,
        "preferred_candidate_provisional": preferred,
        "selection_rule": "paired validation bootstrap two-layer gain, no >1.5x domain RMSE degradation",
        "cross_scale_absolute_claim_allowed": False,
        "M3_activated": bool(bundle["M3_gate_passed"]),
        "outputs": {key: {"path": str(path.relative_to(ROOT)).replace("\\", "/"),
                          "sha256": sha256(path), "rows": len(pd.read_csv(path))}
                    for key, path in paths.items()},
        "formal_ND_scaling_law_fits": 0,
    }
    result = json_safe(result)
    (OUT / "P_RESPONSE_VALIDATION_METRICS_v2.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": RUN_ID, "support_counts": result["support_counts"],
                      "comparisons": comparisons, "preferred": preferred}, ensure_ascii=False))


if __name__ == "__main__":
    main()
