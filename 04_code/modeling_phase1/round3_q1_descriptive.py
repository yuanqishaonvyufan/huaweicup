"""Non-final Q1 descriptive representation comparison (DQ0-DQ3).

No Loss file is opened. All learned reference transforms use A1 training IDs
only; A1 check IDs and A2/A3 new IDs are evaluation strata.
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
from scipy.stats import rankdata, spearmanr


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "01_data/processed/modeling_phase1/round3"
SOURCE = INPUT / "q1_quality_features_v1.csv.gz"
MANIFEST = INPUT / "INPUT_MANIFEST_v1.json"
SIGNAL_SET = ROOT / "03_models/modeling_phase1/q1/Q1_DESCRIPTIVE_SIGNAL_SET_v1.csv"
CONTRACT = ROOT / "03_models/modeling_phase1/q1/Q1_ROUND3_COMPARISON_CONTRACT_v1.md"
OUT = ROOT / "03_models/modeling_phase1/q1/round3"
CORE = ["fineweb_edu", "fluency_en", "ad_en", "modernbert_cleanliness", "modernbert_readability"]
ARGMAX = ["fineweb_edu", "fluency_en_argmax", "ad_en_argmax",
          "modernbert_cleanliness_argmax", "modernbert_readability_argmax"]
DSIR = ["dsir_books", "dsir_wiki", "dsir_math"]
PRRC = ["modernbert_cleanliness", "modernbert_readability",
        "modernbert_reasoning", "modernbert_professionalism"]
SEED = 20260924
BOOTSTRAP = 200
RUN_ID = "MC-Q1-DQ-R3-20260924-v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rho(x: np.ndarray, y: np.ndarray) -> float:
    good = np.isfinite(x) & np.isfinite(y)
    if good.sum() < 5 or np.unique(x[good]).size < 2 or np.unique(y[good]).size < 2:
        return math.nan
    return float(spearmanr(x[good], y[good]).statistic)


def ecdf(reference: np.ndarray, values: np.ndarray) -> np.ndarray:
    reference = np.sort(reference[np.isfinite(reference)].astype(float))
    if not len(reference):
        raise ValueError("Empty ECDF reference")
    values = values.astype(float)
    left = np.searchsorted(reference, values, side="left")
    right = np.searchsorted(reference, values, side="right")
    output = (left + right) / (2 * len(reference))
    output[~np.isfinite(values)] = math.nan
    return output


def transform_ecdf(reference: pd.DataFrame, target: pd.DataFrame, columns: list[str]) -> np.ndarray:
    return np.column_stack([ecdf(reference[column].to_numpy(float), target[column].to_numpy(float))
                            for column in columns])


def fit_pca(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    mean = x.mean(axis=0)
    std = x.std(axis=0, ddof=1)
    if (std <= 0).any():
        raise ValueError("Constant core signal prevents PCA")
    z = (x - mean) / std
    eigenvalues, vectors = np.linalg.eigh(np.cov(z, rowvar=False, ddof=1))
    order = np.argsort(eigenvalues)[::-1]
    return mean, std, eigenvalues[order], vectors[:, order], z


def cluster_labels(core: np.ndarray, k: int) -> np.ndarray:
    ranked = np.column_stack([rankdata(core[:, j]) for j in range(core.shape[1])])
    corr = np.corrcoef(ranked, rowvar=False)
    distances = np.maximum(0.0, 1.0 - corr)
    np.fill_diagonal(distances, 0)
    tree = linkage(squareform(distances, checks=False), method="average")
    return fcluster(tree, t=k, criterion="maxclust").astype(int)


def group_scores(values: np.ndarray, labels: np.ndarray) -> np.ndarray:
    return np.column_stack([values[:, labels == group].mean(axis=1)
                            for group in sorted(np.unique(labels))])


def quantiles(values: list[float] | np.ndarray) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    return {"median": float(np.nanmedian(values)),
            "p025": float(np.nanquantile(values, 0.025)),
            "p975": float(np.nanquantile(values, 0.975))}


def split_is_check(ids: pd.Series) -> np.ndarray:
    return np.fromiter((int.from_bytes(hashlib.sha256(str(x).encode("utf-8")).digest()[:8], "big") % 5 == 0
                        for x in ids), dtype=bool, count=len(ids))


def top_decile_overlap(x: np.ndarray, y: np.ndarray, ids: np.ndarray) -> float:
    n = len(x)
    if n < 20:
        return math.nan
    k = max(1, math.ceil(n * 0.1))
    # Category outputs have many exact ties. An ID hash is a deterministic
    # tie-breaker; this overlap is a sensitivity diagnostic, not a unique top
    # decile implied by the coarse argmax labels.
    tie = np.fromiter((int.from_bytes(hashlib.sha256(str(i).encode("utf-8")).digest()[:8], "big")
                        for i in ids), dtype=np.uint64, count=n)
    a = set(np.lexsort((tie, x))[-k:].tolist())
    b = set(np.lexsort((tie, y))[-k:].tolist())
    return len(a & b) / k


def list_comparison(frame: pd.DataFrame) -> list[dict]:
    rows = []
    for name, subset in [("A1", frame[frame.source == "A1"]),
                         ("A2", frame[frame.source == "A2"]),
                         ("A3", frame[frame.source == "A3"])]:
        rows.append({"source": name, "signal": "fineweb_edu", "variant": "list[0]",
                     "n": len(subset), "unique_values": int(subset.fineweb_edu.nunique()),
                     "rank_rho_to_continuous": 1.0, "argmax_majority_fraction": ""})
        for signal in ("fluency_en", "ad_en", *PRRC):
            continuous = subset[signal].to_numpy(float)
            argmax = subset[signal + "_argmax"].to_numpy(float)
            good = np.isfinite(continuous) & np.isfinite(argmax)
            counts = Counter(argmax[good])
            rows.append({"source": name, "signal": signal, "variant": "argmax_vs_continuous",
                         "n": int(good.sum()), "unique_values": len(counts),
                         "rank_rho_to_continuous": rho(continuous, argmax),
                         "argmax_majority_fraction": max(counts.values()) / good.sum() if good.any() else math.nan})
        for signal in ("fluency_en", "ad_en"):
            continuous = subset[signal].to_numpy(float)
            prob = subset[signal + "_prob_positive"].to_numpy(float)
            rows.append({"source": name, "signal": signal, "variant": "sigmoid_probability_vs_margin",
                         "n": len(subset), "unique_values": int(pd.Series(prob).nunique()),
                         "rank_rho_to_continuous": rho(continuous, prob),
                         "argmax_majority_fraction": ""})
        facets = subset[[f"qurater_facet_{i}" for i in range(4)]].to_numpy(float)
        mean = np.nanmean(facets, axis=1)
        for i in range(4):
            rows.append({"source": name, "signal": f"qurater_facet_{i}", "variant": "facet_vs_unjustified_mean",
                         "n": len(subset), "unique_values": int(pd.Series(facets[:, i]).nunique()),
                         "rank_rho_to_continuous": rho(facets[:, i], mean),
                         "argmax_majority_fraction": ""})
    return rows


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if sha256(SOURCE) != manifest["processed"]["quality"]["sha256"]:
        raise RuntimeError("Frozen Q1 input hash mismatch")
    if sha256(SIGNAL_SET) != manifest["signal_set_sha256"] or sha256(CONTRACT) != manifest["comparison_contract_sha256"]:
        raise RuntimeError("Signal set or comparison contract changed after input freeze")
    frame = pd.read_csv(SOURCE, compression="gzip", dtype={"id": str, "source": str, "domain": str})
    if len(frame) != 272505 or frame.id.nunique() != 261086:
        raise RuntimeError("Q1 processed input count mismatch")
    source_a1 = frame.source.to_numpy() == "A1"
    check = split_is_check(frame.id)
    train_mask = source_a1 & ~check
    check_mask = source_a1 & check
    train = frame.loc[train_mask]
    check_frame = frame.loc[check_mask]
    if len(train) < 35000 or len(check_frame) < 8000:
        raise RuntimeError("Unexpected A1 fixed split size")
    core_values = frame[CORE].to_numpy(float)
    if not np.isfinite(core_values).all():
        raise RuntimeError("Core five signals contain nonfinite values")

    u = transform_ecdf(train, frame, CORE)
    dq0 = u.mean(axis=1)
    alt_u = transform_ecdf(train, frame, ARGMAX)
    dq0_argmax = alt_u.mean(axis=1)
    within = np.empty_like(u)
    for domain in sorted(frame.domain.unique()):
        mask = frame.domain.to_numpy() == domain
        reference = train[train.domain == domain]
        if len(reference) < 100:
            raise RuntimeError(f"Domain ECDF reference too small: {domain}")
        within[mask] = transform_ecdf(reference, frame.loc[mask], CORE)
    dq3 = within.mean(axis=1)

    mean, std, eigenvalues, vectors, z_train = fit_pca(u[train_mask])
    if np.corrcoef(z_train @ vectors[:, 0], dq0[train_mask])[0, 1] < 0:
        vectors[:, 0] *= -1
    z_all = (u - mean) / std
    dq1_pc1 = z_all @ vectors[:, 0]
    evr = eigenvalues / eigenvalues.sum()
    groups2 = cluster_labels(u[train_mask], 2)
    groups3 = cluster_labels(u[train_mask], 3)
    dq2_k2 = group_scores(u, groups2)
    dq2_k3 = group_scores(u, groups3)

    # Stability on fixed A1 check IDs: all references and PCs are re-learned
    # from domain-stratified bootstrap samples of the A1 training reference.
    rng = np.random.default_rng(SEED)
    train_index = np.flatnonzero(train_mask)
    train_domains = frame.domain.to_numpy()[train_index]
    domain_positions = {d: np.flatnonzero(train_domains == d) for d in np.unique(train_domains)}
    check_target = frame.loc[check_mask]
    baseline_check = dq0[check_mask]
    pc1_cosines, pc1_evr, check_rank_rhos, bootstrap_loadings = [], [], [], []
    cocluster2 = np.zeros((len(CORE), len(CORE)), dtype=float)
    for _ in range(BOOTSTRAP):
        sampled_local = np.concatenate([rng.choice(pos, size=len(pos), replace=True)
                                        for pos in domain_positions.values()])
        sampled_global = train_index[sampled_local]
        ref = frame.iloc[sampled_global]
        boot_check_u = transform_ecdf(ref, check_target, CORE)
        check_rank_rhos.append(rho(boot_check_u.mean(axis=1), baseline_check))
        boot_train_u = transform_ecdf(train, ref, CORE)
        _, _, e_b, v_b, _ = fit_pca(boot_train_u)
        if np.dot(v_b[:, 0], vectors[:, 0]) < 0:
            v_b[:, 0] *= -1
        pc1_cosines.append(float(np.dot(v_b[:, 0], vectors[:, 0])))
        pc1_evr.append(float(e_b[0] / e_b.sum()))
        bootstrap_loadings.append(v_b[:, 0].copy())
        labs = cluster_labels(boot_train_u, 2)
        cocluster2 += (labs[:, None] == labs[None, :]).astype(float)
    cocluster2 /= BOOTSTRAP
    bootstrap_loadings = np.asarray(bootstrap_loadings)

    source_a1_ids = set(frame.loc[source_a1, "id"])
    new_mask = (frame.source.to_numpy() != "A1") & (~frame.id.isin(source_a1_ids).to_numpy())
    scopes = {
        "A1_all": source_a1,
        "A1_train": train_mask,
        "A1_check": check_mask,
        "A2_all": frame.source.to_numpy() == "A2",
        "A3_all": frame.source.to_numpy() == "A3",
        "A2_new_ids": (frame.source.to_numpy() == "A2") & new_mask,
        "A3_new_ids": (frame.source.to_numpy() == "A3") & new_mask,
        **{f"A1_{d}": source_a1 & (frame.domain.to_numpy() == d) for d in sorted(frame.domain.unique())},
    }
    summary_rows = []
    for scope, mask in scopes.items():
        if not mask.any():
            continue
        d0, d1, d3, alt = dq0[mask], dq1_pc1[mask], dq3[mask], dq0_argmax[mask]
        summary_rows.append({
            "scope": scope, "n": int(mask.sum()),
            "DQ0_mean": float(np.mean(d0)), "DQ0_std": float(np.std(d0, ddof=1)),
            "DQ0_p10": float(np.quantile(d0, 0.1)), "DQ0_p50": float(np.median(d0)),
            "DQ0_p90": float(np.quantile(d0, 0.9)),
            "DQ1_PC1_mean": float(np.mean(d1)), "DQ1_PC1_std": float(np.std(d1, ddof=1)),
            "DQ3_mean": float(np.mean(d3)), "DQ3_std": float(np.std(d3, ddof=1)),
            "rho_DQ0_DQ1": rho(d0, d1), "rho_DQ0_DQ3": rho(d0, d3),
            "rho_DQ0_argmax": rho(d0, alt),
            "top_decile_overlap_DQ0_argmax": top_decile_overlap(d0, alt, frame.loc[mask, "id"].to_numpy()),
        })

    # DSIR alternative representations remain diagnostics, never Q predictors.
    dsir_train_raw = train[DSIR].to_numpy(float)
    dsir_corr = np.corrcoef(np.column_stack([rankdata(dsir_train_raw[:, j]) for j in range(3)]), rowvar=False)
    mean_abs_corr = np.mean(np.abs(dsir_corr - np.eye(3)), axis=1)
    medoid_index = int(np.argmax(mean_abs_corr))
    dsir_train_rank = transform_ecdf(train, train, DSIR)
    _, _, dsir_eigen, dsir_vec, _ = fit_pca(dsir_train_rank)
    if np.corrcoef((dsir_train_rank - dsir_train_rank.mean(axis=0)) @ dsir_vec[:, 0],
                   dsir_train_rank[:, medoid_index])[0, 1] < 0:
        dsir_vec[:, 0] *= -1
    dsir_boot_evr, dsir_boot_cos = [], []
    for _ in range(BOOTSTRAP):
        sampled_local = np.concatenate([rng.choice(pos, size=len(pos), replace=True)
                                        for pos in domain_positions.values()])
        sampled_raw = dsir_train_raw[sampled_local]
        ranked = np.column_stack([rankdata(sampled_raw[:, j]) for j in range(3)])
        _, _, ev, vec, _ = fit_pca(ranked)
        if np.dot(vec[:, 0], dsir_vec[:, 0]) < 0:
            vec[:, 0] *= -1
        dsir_boot_evr.append(float(ev[0] / ev.sum()))
        dsir_boot_cos.append(float(np.dot(vec[:, 0], dsir_vec[:, 0])))
    # Length-adjusted residual is only an exploratory source-ambiguity probe.
    ranked = np.column_stack([rankdata(dsir_train_raw[:, j]) for j in range(3)])
    length_rank = rankdata(np.log1p(train.rps_doc_word_count.to_numpy(float)))
    dummies = pd.get_dummies(train.domain, drop_first=True).to_numpy(float)
    design = np.column_stack([np.ones(len(train)), length_rank, dummies])
    residual = ranked - design @ np.linalg.lstsq(design, ranked, rcond=None)[0]
    dsir_residual_length_rho = [rho(residual[:, j], length_rank) for j in range(3)]
    dsir_original_length_rho = [rho(dsir_train_raw[:, j], length_rank) for j in range(3)]

    list_rows = list_comparison(frame)
    domain_pca = []
    for domain, group in train.groupby("domain"):
        mask = train.domain.to_numpy() == domain
        _, _, local_evr, local_vec, _ = fit_pca(u[train_mask][mask])
        cosine = abs(float(np.dot(local_vec[:, 0], vectors[:, 0])))
        domain_pca.append({"domain": domain, "n": len(group),
                           "pc1_variance_share": float(local_evr[0] / local_evr.sum()),
                           "pc1_loading_abs_cosine_to_global": cosine})
    length = frame.rps_doc_word_count.to_numpy(float)
    low, high = np.quantile(length[train_mask], [0.01, 0.99])
    trimmed = train_mask & (length >= low) & (length <= high)
    _, _, trim_e, trim_v, _ = fit_pca(u[trimmed])
    trim_cos = abs(float(np.dot(trim_v[:, 0], vectors[:, 0])))

    result_columns = {"id": frame.id, "source": frame.source, "domain": frame.domain,
                      "A1_fixed_split": np.where(source_a1, np.where(check, "check", "train"), "extension"),
                      "DQ0_global_core": dq0, "DQ0_argmax_sensitivity": dq0_argmax,
                      "DQ1_PC1": dq1_pc1, "DQ3_within_domain": dq3}
    for k, group_values in ((2, dq2_k2), (3, dq2_k3)):
        for j in range(group_values.shape[1]):
            result_columns[f"DQ2_k{k}_group{j+1}"] = group_values[:, j]
    OUT.mkdir(parents=True, exist_ok=True)
    result_path = OUT / "Q1_DESCRIPTIVE_QUALITY_RESULTS_v1.csv.gz"
    pd.DataFrame(result_columns).to_csv(result_path, index=False, compression="gzip", float_format="%.17g")
    pd.DataFrame(summary_rows).to_csv(OUT / "Q1_DESCRIPTIVE_DOMAIN_SUMMARY_v1.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(list_rows).to_csv(OUT / "LIST_SIGNAL_REPRESENTATION_RESULTS_v1.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(domain_pca).to_csv(OUT / "Q1_DOMAIN_PCA_STABILITY_v1.csv", index=False, encoding="utf-8-sig")
    load_rows = [{"signal": signal, "PC1_loading": float(vectors[j, 0]),
                  "PC1_loading_boot_median": float(np.median(bootstrap_loadings[:, j])),
                  "PC1_loading_boot_p025": float(np.quantile(bootstrap_loadings[:, j], 0.025)),
                  "PC1_loading_boot_p975": float(np.quantile(bootstrap_loadings[:, j], 0.975)),
                  "DQ2_k2_group": int(groups2[j]), "DQ2_k3_group": int(groups3[j])}
                 for j, signal in enumerate(CORE)]
    pd.DataFrame(load_rows).to_csv(OUT / "Q1_DQ_LOADINGS_AND_GROUPS_v1.csv", index=False, encoding="utf-8-sig")
    summary = {
        "run_id": RUN_ID, "status": "MODEL_COMPARISON_NON_FINAL_CANDIDATE",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)), "input_sha256": sha256(SOURCE),
        "signal_set_sha256": sha256(SIGNAL_SET), "contract_sha256": sha256(CONTRACT),
        "seed": SEED, "bootstrap_replicates": BOOTSTRAP,
        "counts": {"physical_records": len(frame), "unique_ids": int(frame.id.nunique()),
                   "A1_train": int(train_mask.sum()), "A1_check": int(check_mask.sum()),
                   "A2_new": int(scopes["A2_new_ids"].sum()), "A3_new": int(scopes["A3_new_ids"].sum())},
        "DQ0": {"five_core_signals": CORE, "A1_check_reference_bootstrap_rank_rho": quantiles(check_rank_rhos),
                "core_rank_correlations": {signal: rho(dq0[train_mask], u[train_mask, j])
                                           for j, signal in enumerate(CORE)}},
        "DQ1": {"eigenvalues": eigenvalues.tolist(), "variance_share": evr.tolist(),
                "PC1_loadings": {s: float(vectors[j, 0]) for j, s in enumerate(CORE)},
                "PC1_loading_bootstrap_cosine": quantiles(pc1_cosines),
                "PC1_variance_share_bootstrap": quantiles(pc1_evr),
                "length_trim_1_99_PC1_loading_abs_cosine": trim_cos,
                "length_trim_1_99_PC1_variance_share": float(trim_e[0] / trim_e.sum())},
        "DQ2": {"k2_groups": {s: int(groups2[j]) for j, s in enumerate(CORE)},
                "k3_groups": {s: int(groups3[j]) for j, s in enumerate(CORE)},
                "k2_bootstrap_coclustering_frequency": cocluster2.tolist()},
        "DQ3": {"caution": "Within-domain normalization removes between-domain location by construction"},
        "DSIR": {"raw_rank_spearman": dsir_corr.tolist(), "medoid": DSIR[medoid_index],
                 "rank_PC1_variance_share": float(dsir_eigen[0] / dsir_eigen.sum()),
                 "rank_PC1_loadings": {s: float(dsir_vec[j, 0]) for j, s in enumerate(DSIR)},
                 "rank_PC1_evr_bootstrap": quantiles(dsir_boot_evr),
                 "rank_PC1_loading_cosine_bootstrap": quantiles(dsir_boot_cos),
                 "original_rho_word_count": dict(zip(DSIR, dsir_original_length_rho)),
                 "residual_rho_word_count_exploratory": dict(zip(DSIR, dsir_residual_length_rho)),
                 "residual_status": "DIAGNOSTIC_ONLY_NOT_QUALITY"},
        "outputs": {"scores": {"path": str(result_path.relative_to(ROOT)).replace("\\", "/"),
                               "sha256": sha256(result_path)},
                    "domain_summary_rows": len(summary_rows), "list_rows": len(list_rows),
                    "domain_pca_rows": len(domain_pca), "loadings_rows": len(load_rows)},
        "no_loss_used": True,
    }
    (OUT / "Q1_DESCRIPTIVE_QUALITY_METRICS_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": RUN_ID, "counts": summary["counts"],
                      "DQ1_PC1_share": evr[0], "DSIR_PC1_share": summary["DSIR"]["rank_PC1_variance_share"],
                      "score_sha256": summary["outputs"]["scores"]["sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
