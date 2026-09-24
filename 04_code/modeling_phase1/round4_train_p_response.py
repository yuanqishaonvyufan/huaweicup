"""Formal Round 4 Q1 A4/A5 p -> 13-domain Loss candidate training.

This script NEVER opens A6-A11. It freezes M0/M1 and conditionally M2/M3,
their training-only hyperparameters, and a bundle for a separate validation run.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.linalg import helmert
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data/raw/real_attachments"
P_PATH = RAW / "A_data_value/regmix_tables/train_mixture_1m.csv"
Y_PATH = RAW / "A_data_value/regmix_tables/train_pile_loss_1m.csv"
RAW_MANIFEST = ROOT / "01_data/raw/RAW_SHA256.csv"
ROUTE = ROOT / "01_data/audits/phase1/route_audit_metrics.json"
CONTRACT = ROOT / "03_models/modeling_phase1/q1/round4/P_RESPONSE_PREFIT_CONTRACT_v1.md"
PREREG = ROOT / "03_models/modeling_phase1/q1/P1_1_13_DOMAIN_RESPONSE_PREREG_FINAL_v1.md"
OUT = ROOT / "03_models/modeling_phase1/q1/round4"
RUN_ID = "EXP-Q1-PRESP-TRAIN-R4-20260924-v1"
SEED = 20260924
BOOTSTRAP = 200
ALPHAS = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]
P_HASH = "04a32ef4ab594376bf90e11404c033668f887c351d6a03ad3744824c7296a2d8"
Y_HASH = "49a959aa07ce5c20831d5abe3a7896ff0cd90a398bd407c8913fd5588be0465a"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check_mapping() -> tuple[list[str], list[str]]:
    with RAW_MANIFEST.open(encoding="utf-8-sig", newline="") as stream:
        hashes = {row["relative_path"]: row["sha256"] for row in csv.DictReader(stream)}
    for path, expected in ((P_PATH, P_HASH), (Y_PATH, Y_HASH)):
        relative = str(path.relative_to(RAW)).replace("\\", "/")
        if hashes.get(relative) != expected or sha256(path) != expected:
            raise RuntimeError(f"Official A4/A5 path/hash mismatch: {relative}")
    info = json.loads(ROUTE.read_text(encoding="utf-8"))["A"]["A4_A5"]
    if not CONTRACT.is_file() or not PREREG.is_file():
        raise RuntimeError("P-response prefit contract or P1-1 missing")
    return info["p_columns"], info["loss_columns"]


def folds(indices: np.ndarray) -> np.ndarray:
    return np.array([int.from_bytes(hashlib.sha256(str(i).encode()).digest()[:8], "big") % 5
                     for i in indices], dtype=int)


def design_pca(z: np.ndarray) -> np.ndarray:
    _, _, vt = np.linalg.svd(z, full_matrices=False)
    v = vt[:3].T.copy()
    for j in range(3):
        if v[np.argmax(np.abs(v[:, j])), j] < 0:
            v[:, j] *= -1
    return v


def fit(kind: str, p: np.ndarray, y: np.ndarray, basis: np.ndarray, alpha: float = 0.0) -> dict:
    pmean = p.mean(axis=0)
    z = (p - pmean) @ basis
    ymean = y.mean(axis=0)
    pc = None
    sqmean = None
    features = z
    if kind == "M3":
        pc = design_pca(z)
        sq = (z @ pc) ** 2
        sqmean = sq.mean(axis=0)
        features = np.column_stack([z, sq - sqmean])
    if kind == "M0":
        coef = np.zeros((0, y.shape[1]))
    elif kind == "M1":
        coef, *_ = np.linalg.lstsq(features, y - ymean, rcond=None)
    elif kind in ("M2", "M3"):
        gram = features.T @ features + alpha * np.eye(features.shape[1])
        coef = np.linalg.solve(gram, features.T @ (y - ymean))
    else:
        raise ValueError(kind)
    return {"kind": kind, "pmean": pmean, "ymean": ymean, "coef": coef,
            "alpha": alpha, "pc": pc, "sqmean": sqmean}


def predict(model: dict, p: np.ndarray, basis: np.ndarray) -> np.ndarray:
    if model["kind"] == "M0":
        return np.tile(model["ymean"], (len(p), 1))
    z = (p - model["pmean"]) @ basis
    features = z
    if model["kind"] == "M3":
        features = np.column_stack([z, (z @ model["pc"]) ** 2 - model["sqmean"]])
    return model["ymean"] + features @ model["coef"]


def fold_score(y_true: np.ndarray, y_pred: np.ndarray, train_sd: np.ndarray) -> tuple[float, float, float]:
    residual = y_true - y_pred
    domain_rmse = np.sqrt(np.mean(residual ** 2, axis=0))
    r0_sd = float(np.std(y_true.mean(axis=1), ddof=1))
    # The fold's training R0 scale is provided as train_sd[-1].
    r0_norm = float(np.sqrt(np.mean(residual.mean(axis=1) ** 2)) / train_sd[-1])
    domain_norm = float(np.mean(domain_rmse / train_sd[:-1]))
    return 0.5 * r0_norm + 0.5 * domain_norm, r0_norm, domain_norm


def cv_model(kind: str, p: np.ndarray, y: np.ndarray, index: np.ndarray,
             basis: np.ndarray, alpha: float = 0.0) -> dict:
    groups = folds(index)
    oof = np.empty_like(y)
    scores, r0_scores, domain_scores = [], [], []
    for fold in range(5):
        train = groups != fold
        test = groups == fold
        model = fit(kind, p[train], y[train], basis, alpha)
        out = predict(model, p[test], basis)
        oof[test] = out
        train_sd = np.concatenate([y[train].std(axis=0, ddof=1),
                                   [y[train].mean(axis=1).std(ddof=1)]])
        if (train_sd <= 0).any():
            raise RuntimeError("Zero training response SD")
        score, r0_s, domain_s = fold_score(y[test], out, train_sd)
        scores.append(score)
        r0_scores.append(r0_s)
        domain_scores.append(domain_s)
    return {"kind": kind, "alpha": alpha, "oof": oof,
            "fold_scores": scores, "mean_cv_score": float(np.mean(scores)),
            "cv_r0_norm_rmse": float(np.mean(r0_scores)),
            "cv_domain_norm_rmse": float(np.mean(domain_scores))}


def residual_pattern(p: np.ndarray, y: np.ndarray, oof: np.ndarray,
                     index: np.ndarray, basis: np.ndarray) -> dict:
    z = (p - p.mean(axis=0)) @ basis
    squared = (z @ design_pca(z)) ** 2
    residual = y - oof
    fold = folds(index)
    axes = []
    for axis in range(3):
        passed = []
        rho_all = []
        for domain in range(y.shape[1]):
            r = float(spearmanr(squared[:, axis], residual[:, domain]).statistic)
            rho_all.append(r)
            if abs(r) < 0.15:
                continue
            signs = [np.sign(spearmanr(squared[fold == f, axis], residual[fold == f, domain]).statistic)
                     for f in range(5)]
            if sum(s == np.sign(r) for s in signs) >= 4:
                passed.append(domain)
        axes.append({"axis": axis + 1, "passed_domains": passed,
                     "passed_count": len(passed), "full_oof_rho": rho_all})
    return {"axis_checks": axes, "trigger": any(x["passed_count"] >= 4 for x in axes)}


def bootstrap_coefficients(p: np.ndarray, y: np.ndarray, basis: np.ndarray,
                           model: dict, rng: np.random.Generator) -> dict:
    if model["kind"] == "M0":
        return {"replicates": 0}
    coefs = []
    for _ in range(BOOTSTRAP):
        idx = rng.integers(0, len(p), size=len(p))
        boot = fit(model["kind"], p[idx], y[idx], basis, model["alpha"])
        # M3 quadratic axes can rotate across bootstraps, so report only
        # prediction stability for M3 later, not naive coefficient signs.
        if model["kind"] != "M3":
            coefs.append(boot["coef"])
    if not coefs:
        return {"replicates": BOOTSTRAP, "coefficient_sign_stability": "NOT_COMPARABLE_FOR_ROTATING_M3_AXES"}
    array = np.asarray(coefs)
    full = model["coef"]
    stability = np.mean(np.sign(array) == np.sign(full), axis=0)
    active = np.abs(full) >= np.maximum(1e-12, np.max(np.abs(full), axis=0, keepdims=True) * 0.1)
    return {"replicates": BOOTSTRAP,
            "median_sign_agreement_active_coefficients": float(np.median(stability[active])) if active.any() else math.nan,
            "active_coefficient_count": int(active.sum()),
            "fraction_active_below_0_8_sign_agreement": float(np.mean(stability[active] < 0.8)) if active.any() else math.nan}


def serializable(model: dict) -> dict:
    return {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in model.items()}


def main() -> None:
    p_cols, y_cols = check_mapping()
    p_frame = pd.read_csv(P_PATH)
    y_frame = pd.read_csv(Y_PATH)
    if len(p_frame) != 512 or len(y_frame) != 512 or p_frame["index"].duplicated().any() or y_frame["index"].duplicated().any():
        raise RuntimeError("A4/A5 training grain changed")
    if list(p_frame.columns) != ["index", *p_cols] or list(y_frame.columns) != ["index", *y_cols]:
        raise RuntimeError("A4/A5 official fields/order changed")
    joined = p_frame.merge(y_frame, on="index", validate="one_to_one").sort_values("index")
    if len(joined) != 512:
        raise RuntimeError("A4/A5 index pairing failed")
    p_raw = joined[p_cols].to_numpy(float)
    y = joined[y_cols].to_numpy(float)
    if not np.isfinite(p_raw).all() or not np.isfinite(y).all() or (p_raw < 0).any():
        raise RuntimeError("Nonfinite or negative A4/A5 cell")
    sums = p_raw.sum(axis=1)
    if np.min(sums) < 0.99 or np.max(sums) > 1.01:
        raise RuntimeError("A4 sum outside rounding-repair contract")
    p = p_raw / sums[:, None]
    basis = helmert(17, full=False).T
    if basis.shape != (17, 16) or not np.allclose(basis.T @ basis, np.eye(16), atol=1e-12):
        raise RuntimeError("Helmert contrast basis invalid")
    z = (p - p.mean(axis=0)) @ basis
    singular = np.linalg.svd(z, compute_uv=False)
    condition = float(singular[0] / singular[-1])
    if np.linalg.matrix_rank(z) != 16:
        raise RuntimeError("A4 16-coordinate design rank deficient")

    index = joined["index"].to_numpy()
    cv = {}
    cv["M0"] = cv_model("M0", p, y, index, basis)
    cv["M1"] = cv_model("M1", p, y, index, basis)
    m2_trigger = condition > 30 or cv["M1"]["mean_cv_score"] > cv["M0"]["mean_cv_score"]
    if m2_trigger:
        grid = [cv_model("M2", p, y, index, basis, alpha) for alpha in ALPHAS]
        cv["M2"] = min(grid, key=lambda d: d["mean_cv_score"])
    else:
        grid = []
    best_linear = min([v for k, v in cv.items() if k in ("M1", "M2")], key=lambda d: d["mean_cv_score"])
    pattern = residual_pattern(p, y, best_linear["oof"], index, basis)
    m3_grid = []
    m3_gate = False
    if pattern["trigger"]:
        m3_grid = [cv_model("M3", p, y, index, basis, alpha) for alpha in ALPHAS]
        best_m3 = min(m3_grid, key=lambda d: d["mean_cv_score"])
        diff = np.asarray(best_linear["fold_scores"]) - np.asarray(best_m3["fold_scores"])
        m3_gate = float(np.mean(diff)) > float(np.std(diff, ddof=1) / math.sqrt(5))
        if m3_gate:
            cv["M3"] = best_m3
    models = {kind: fit(kind, p, y, basis, item["alpha"])
              for kind, item in cv.items()}
    rng = np.random.default_rng(SEED)
    rows = []
    for kind, model in models.items():
        pred = predict(model, p, basis)
        residual = y - pred
        cv_item = cv[kind]
        boot = bootstrap_coefficients(p, y, basis, model, rng)
        rows.append({"model": kind, "alpha": model["alpha"],
                     "train_R0_RMSE": float(np.sqrt(np.mean(residual.mean(axis=1) ** 2))),
                     "train_mean_domain_RMSE": float(np.mean(np.sqrt(np.mean(residual ** 2, axis=0)))),
                     "train_R0_rank_spearman": float(spearmanr(y.mean(axis=1), pred.mean(axis=1)).statistic)
                     if kind != "M0" else math.nan,
                     "cv_balanced_score": cv_item["mean_cv_score"],
                     "cv_R0_normalized_RMSE": cv_item["cv_r0_norm_rmse"],
                     "cv_mean_domain_normalized_RMSE": cv_item["cv_domain_norm_rmse"],
                     "cv_fold_scores": "|".join(f"{v:.9g}" for v in cv_item["fold_scores"]),
                     "bootstrap_active_sign_agreement_median": boot.get("median_sign_agreement_active_coefficients", ""),
                     "bootstrap_active_fraction_below_0_8": boot.get("fraction_active_below_0_8_sign_agreement", ""),
                     "status": "TRAINED_FROZEN_CANDIDATE"})

    OUT.mkdir(parents=True, exist_ok=True)
    train_results = OUT / "P_RESPONSE_TRAIN_CV_RESULTS_v1.csv"
    pd.DataFrame(rows).to_csv(train_results, index=False, encoding="utf-8-sig")
    oof = pd.DataFrame({"index": index, "R0_observed": y.mean(axis=1)})
    for kind, item in cv.items():
        oof[kind + "_R0_OOF_pred"] = item["oof"].mean(axis=1)
    oof_path = OUT / "P_RESPONSE_TRAIN_OOF_PREDICTIONS_v1.csv"
    oof.to_csv(oof_path, index=False, encoding="utf-8-sig")
    bundle = {
        "run_id": RUN_ID, "status": "FROZEN_BEFORE_A6_A11_VALIDATION",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "training_script_sha256": sha256(Path(__file__)),
        "raw_input_sha256": {"A4": P_HASH, "A5": Y_HASH},
        "contract_sha256": sha256(CONTRACT), "P1_1_prereg_sha256": sha256(PREREG),
        "p_columns": p_cols, "loss_columns": y_cols,
        "basis": basis.tolist(),
        "training_p_normalization": "row divide by raw sum; zeros preserved",
        "training_p_sum_minmax": [float(sums.min()), float(sums.max())],
        "training_p_max_abs_normalization_change": float(np.max(np.abs(p - p_raw))),
        "training_design_condition": condition,
        "training_design_rank": 16,
        "seed": SEED, "cv_fold_definition": "SHA256(index) first 8 bytes modulo 5",
        "alpha_grid": ALPHAS,
        "M2_triggered": bool(m2_trigger),
        "M3_residual_pattern": pattern,
        "M3_gate_passed": bool(m3_gate),
        "models": {kind: serializable(model) for kind, model in models.items()},
        "response_mean": y.mean(axis=0).tolist(),
        "response_sd_ddof1": y.std(axis=0, ddof=1).tolist(),
        "R0_train_sd_ddof1": float(y.mean(axis=1).std(ddof=1)),
        "training_p_matrix": p.tolist(),
        "A6_A11_loss_read": False,
        "outputs": {"train_results_sha256": sha256(train_results), "oof_sha256": sha256(oof_path)},
    }
    bundle_path = OUT / "P_RESPONSE_FROZEN_MODEL_BUNDLE_v1.json"
    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {"run_id": RUN_ID, "code_sha256": sha256(Path(__file__)),
               "bundle_sha256": sha256(bundle_path), "train_results_sha256": sha256(train_results),
               "oof_sha256": sha256(oof_path), "cv_candidates": {k: {"alpha": v["alpha"],
                   "score": v["mean_cv_score"]} for k, v in cv.items()},
               "M2_triggered": bool(m2_trigger), "M3_pattern_trigger": bool(pattern["trigger"]),
               "M3_gate_passed": bool(m3_gate), "design_condition": condition,
               "A6_A11_loss_read": False}
    (OUT / "P_RESPONSE_TRAIN_METRICS_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
