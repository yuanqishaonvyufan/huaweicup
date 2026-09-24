"""P1-1 R0-R3 training-only 13-domain response comparison (non-final).

The definitions and IDs are inherited without alteration. No A6-A11 held-out
Loss or p-response model is read or estimated.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from scipy.stats import kendalltau, rankdata, spearmanr


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "01_data/processed/modeling_phase1/round3"
SOURCE = INPUT / "a5_13_domain_loss_v1.csv.gz"
MANIFEST = INPUT / "INPUT_MANIFEST_v1.json"
PREREG = ROOT / "03_models/modeling_phase1/q1/P1_1_13_DOMAIN_RESPONSE_PREREG_FINAL_v1.md"
CONTRACT = ROOT / "03_models/modeling_phase1/q1/Q1_ROUND3_COMPARISON_CONTRACT_v1.md"
OUT = ROOT / "03_models/modeling_phase1/q1/round3"
RUN_ID = "MC-Q1-RSP-R3-20260924-v1"
SEED = 20260924
BOOTSTRAP = 500


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rho(x: np.ndarray, y: np.ndarray) -> float:
    return float(spearmanr(x, y).statistic)


def quantiles(values: list[float] | np.ndarray) -> dict[str, float]:
    array = np.asarray(values, dtype=float)
    return {"median": float(np.median(array)),
            "p025": float(np.quantile(array, 0.025)),
            "p975": float(np.quantile(array, 0.975))}


def fit_r1_r2(loss: np.ndarray, reference_r0: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    mean = loss.mean(axis=0)
    std = loss.std(axis=0, ddof=1)
    if (std <= 0).any():
        raise ValueError("P1-1 R1/R2 NOT COMPUTABLE: zero-variance domain")
    z = (loss - mean) / std
    eigenvalues, vectors = np.linalg.eigh(np.cov(z, rowvar=False, ddof=1))
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, vectors = eigenvalues[order], vectors[:, order]
    if reference_r0 is None:
        reference_r0 = loss.mean(axis=1)
    if np.corrcoef(z @ vectors[:, 0], reference_r0)[0, 1] < 0:
        vectors[:, 0] *= -1
    return mean, std, eigenvalues, vectors


def top_decile_overlap_lower(x: np.ndarray, y: np.ndarray) -> float:
    k = math.ceil(len(x) * 0.1)
    return len(set(np.argpartition(x, k - 1)[:k]) & set(np.argpartition(y, k - 1)[:k])) / k


def pairwise_reversal(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    tau = float(kendalltau(x, y).statistic)
    n = len(x)
    total = n * (n - 1) // 2
    ties_x = sum(c * (c - 1) // 2 for c in Counter(x).values())
    ties_y = sum(c * (c - 1) // 2 for c in Counter(y).values())
    ties_both = sum(c * (c - 1) // 2 for c in Counter(zip(x, y)).values())
    comparable = total - ties_x - ties_y + ties_both
    if comparable <= 0:
        return math.nan, tau
    c_minus_d = tau * math.sqrt((total - ties_x) * (total - ties_y))
    return float((comparable - c_minus_d) / (2 * comparable)), tau


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if sha256(SOURCE) != manifest["processed"]["response"]["sha256"]:
        raise RuntimeError("Frozen A5 response input hash changed")
    if sha256(CONTRACT) != manifest["comparison_contract_sha256"]:
        raise RuntimeError("Comparison contract changed after input freeze")
    frame = pd.read_csv(SOURCE, compression="gzip")
    columns = list(frame.columns[1:])
    if list(frame.columns) != manifest["processed"]["response"]["columns"] or len(frame) != 512 or len(columns) != 13:
        raise RuntimeError("P1-1 A5 schema or row count changed")
    if frame["index"].duplicated().any():
        raise RuntimeError("Duplicate A5 training run index")
    loss = frame[columns].to_numpy(float)
    if not np.isfinite(loss).all():
        raise RuntimeError("A5 Loss contains nonfinite values")
    r0 = loss.mean(axis=1)
    mean, std, eigenvalues, vectors = fit_r1_r2(loss, r0)
    z = (loss - mean) / std
    r1 = z.mean(axis=1)
    r2 = z @ vectors[:, 0]
    if np.corrcoef(r0, r2)[0, 1] <= 0:
        raise RuntimeError("R2 sign not aligned with R0")
    evr = eigenvalues / eigenvalues.sum()
    domain_corr = np.corrcoef(np.column_stack([rankdata(loss[:, j]) for j in range(13)]), rowvar=False)
    negative_domain_pairs = int(np.sum(np.triu(domain_corr < 0, 1)))
    clusters = {}
    for k in (2, 3, 4):
        distance = np.maximum(0.0, 1 - domain_corr)
        np.fill_diagonal(distance, 0)
        clusters[k] = fcluster(linkage(squareform(distance, checks=False), method="average"),
                               t=k, criterion="maxclust").astype(int)

    rng = np.random.default_rng(SEED)
    load_cos, pc1_evr, r1_rank, r2_rank = [], [], [], []
    loadings = []
    for _ in range(BOOTSTRAP):
        index = rng.integers(0, len(loss), size=len(loss))
        boot_loss = loss[index]
        b_mean, b_std, b_eigen, b_vectors = fit_r1_r2(boot_loss)
        if np.dot(b_vectors[:, 0], vectors[:, 0]) < 0:
            b_vectors[:, 0] *= -1
        boot_z_on_full = (loss - b_mean) / b_std
        load_cos.append(float(np.dot(b_vectors[:, 0], vectors[:, 0])))
        pc1_evr.append(float(b_eigen[0] / b_eigen.sum()))
        r1_rank.append(rho(boot_z_on_full.mean(axis=1), r1))
        r2_rank.append(rho(boot_z_on_full @ b_vectors[:, 0], r2))
        loadings.append(b_vectors[:, 0].copy())
    loadings = np.asarray(loadings)

    # A5-only fixed half split is an independent stability check of learned
    # standardization/loadings, not a validation set for p-response prediction.
    half = np.asarray([int.from_bytes(hashlib.sha256(str(i).encode()).digest()[:8], "big") % 2
                       for i in frame["index"]], dtype=int)
    half_models = []
    for side in (0, 1):
        local = loss[half == side]
        m, s, e, v = fit_r1_r2(local)
        if np.dot(v[:, 0], vectors[:, 0]) < 0:
            v[:, 0] *= -1
        full_z = (loss - m) / s
        half_models.append({"side": side, "n": len(local),
                            "R1_rho_to_full": rho(full_z.mean(axis=1), r1),
                            "R2_rho_to_full": rho(full_z @ v[:, 0], r2),
                            "R2_loading_cosine_to_full": float(np.dot(v[:, 0], vectors[:, 0])),
                            "PC1_variance_share": float(e[0] / e.sum())})

    var_r0 = float(np.var(r0, ddof=1))
    r0_contribution = np.asarray([np.cov(loss[:, j], r0, ddof=1)[0, 1] / (13 * var_r0)
                                   for j in range(13)])
    pc1_recon = np.outer(r2, vectors[:, 0])
    residual_variance = ((z - pc1_recon) ** 2).mean(axis=0)
    domain_rows = []
    for j, column in enumerate(columns):
        without = np.delete(loss, j, axis=1).mean(axis=1)
        reversal, tau = pairwise_reversal(r0, loss[:, j])
        domain_rows.append({
            "domain": column.removeprefix("metric/the_pile_").removesuffix("_val_loss"),
            "loss_column": column, "mean_loss": float(mean[j]), "sd_loss": float(std[j]),
            "mean_deviation_from_R0": float(np.mean(loss[:, j] - r0)),
            "R0_variance_contribution": float(r0_contribution[j]),
            "R2_PC1_loading": float(vectors[j, 0]),
            "R2_loading_boot_p025": float(np.quantile(loadings[:, j], 0.025)),
            "R2_loading_boot_p975": float(np.quantile(loadings[:, j], 0.975)),
            "R2_standardized_residual_MSE": float(residual_variance[j]),
            "rho_domain_to_R0": rho(loss[:, j], r0),
            "pairwise_ranking_reversal_vs_R0": reversal,
            "kendall_tau_b_vs_R0": tau,
            "leave_one_domain_out_R0_rank_rho": rho(without, r0),
            "leave_one_domain_out_R0_best_decile_overlap": top_decile_overlap_lower(without, r0),
            "cluster_k2": int(clusters[2][j]),
            "cluster_k3": int(clusters[3][j]),
            "cluster_k4": int(clusters[4][j]),
        })

    outlier = np.max(np.abs(z), axis=1)
    trim_mask = outlier <= np.quantile(outlier, 0.99)
    _, _, trim_e, trim_v = fit_r1_r2(loss[trim_mask])
    trim_cos = abs(float(np.dot(trim_v[:, 0], vectors[:, 0])))
    results = frame[["index", *columns]].copy()
    results["R0_equal_raw_loss"] = r0
    results["R1_equal_train_z"] = r1
    results["R2_train_z_PC1"] = r2
    results["R3_is_13_original_columns"] = True
    OUT.mkdir(parents=True, exist_ok=True)
    result_path = OUT / "Q1_13_DOMAIN_RESPONSE_RESULTS_v1.csv"
    results.to_csv(result_path, index=False, encoding="utf-8-sig", float_format="%.17g")
    pd.DataFrame(domain_rows).to_csv(OUT / "DOMAIN_HETEROGENEITY_RESULTS_v1.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(domain_corr, index=[x["domain"] for x in domain_rows],
                 columns=[x["domain"] for x in domain_rows]).to_csv(
                     OUT / "Q1_13_DOMAIN_CORRELATION_v1.csv", encoding="utf-8-sig")
    comparison_rows = [
        {"candidate": "R0", "definition": "raw equal mean of 13 domain Loss", "unit": "A5 original Loss",
         "status": "COMPUTABLE_CANDIDATE", "bootstrap_score_rank_rho_p025": 1.0,
         "bootstrap_score_rank_rho_median": 1.0},
        {"candidate": "R1", "definition": "equal mean of A5 train-standardized domain Loss", "unit": "dimensionless",
         "status": "COMPUTABLE_CANDIDATE", "bootstrap_score_rank_rho_p025": float(np.quantile(r1_rank, 0.025)),
         "bootstrap_score_rank_rho_median": float(np.median(r1_rank))},
        {"candidate": "R2", "definition": "PC1 of A5 train z, sign aligned with R0", "unit": "dimensionless",
         "status": "COMPUTABLE_CANDIDATE", "bootstrap_score_rank_rho_p025": float(np.quantile(r2_rank, 0.025)),
         "bootstrap_score_rank_rho_median": float(np.median(r2_rank))},
        {"candidate": "R3", "definition": "13 original domain Loss vector", "unit": "A5 original Loss per domain",
         "status": "MANDATORY_HETEROGENEITY", "bootstrap_score_rank_rho_p025": "",
         "bootstrap_score_rank_rho_median": ""},
    ]
    pd.DataFrame(comparison_rows).to_csv(OUT / "Q1_13_DOMAIN_RESPONSE_CANDIDATE_SUMMARY_v1.csv",
                                         index=False, encoding="utf-8-sig")
    metrics = {
        "run_id": RUN_ID, "status": "MODEL_COMPARISON_NON_FINAL_CANDIDATE",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)), "input_sha256": sha256(SOURCE),
        "prereg_sha256": sha256(PREREG), "contract_sha256": sha256(CONTRACT),
        "seed": SEED, "bootstrap_replicates": BOOTSTRAP,
        "rows": len(frame), "domain_count": len(columns),
        "R0_R1_spearman": rho(r0, r1), "R0_R2_spearman": rho(r0, r2),
        "R1_R2_spearman": rho(r1, r2),
        "R0_R1_best_decile_overlap": top_decile_overlap_lower(r0, r1),
        "R0_R2_best_decile_overlap": top_decile_overlap_lower(r0, r2),
        "R0_R2_sign_correlation": float(np.corrcoef(r0, r2)[0, 1]),
        "R2_eigenvalues": eigenvalues.tolist(),
        "R2_variance_share": evr.tolist(),
        "R2_PC1_bootstrap_evr": quantiles(pc1_evr),
        "R2_PC1_bootstrap_loading_cosine": quantiles(load_cos),
        "R1_bootstrap_score_rank_rho": quantiles(r1_rank),
        "R2_bootstrap_score_rank_rho": quantiles(r2_rank),
        "negative_domain_pair_count": negative_domain_pairs,
        "domain_pair_count": 78,
        "R0_domain_variance_contribution_sum": float(r0_contribution.sum()),
        "fixed_half_models": half_models,
        "R2_1pct_outlier_trim_PC1_loading_abs_cosine": trim_cos,
        "R2_1pct_outlier_trim_PC1_variance_share": float(trim_e[0] / trim_e.sum()),
        "domain_clusters": {f"k{k}": {row["domain"]: int(clusters[k][j])
                                       for j, row in enumerate(domain_rows)} for k in (2, 3, 4)},
        "outputs": {"response_results": {"path": str(result_path.relative_to(ROOT)).replace("\\", "/"),
                                         "sha256": sha256(result_path)},
                    "domain_rows": len(domain_rows)},
        "heldout_A6_A11_read": False,
        "p_response_fitted": False,
    }
    (OUT / "Q1_13_DOMAIN_RESPONSE_METRICS_v1.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": RUN_ID, "R2_PC1_share": evr[0],
                      "negative_domain_pairs": negative_domain_pairs,
                      "R0_R1_rho": metrics["R0_R1_spearman"],
                      "R0_R2_rho": metrics["R0_R2_spearman"],
                      "response_results_sha256": metrics["outputs"]["response_results"]["sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
