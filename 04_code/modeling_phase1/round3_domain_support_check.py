"""Targeted Round 3 source/domain support checks for two observed risks.

No new DQ or response candidate is fitted. This checks DQ2 grouping transport
and clarifies Pearson versus Spearman domain-pair counts from A5.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from scipy.stats import rankdata


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "01_data/processed/modeling_phase1/round3"
OUT = ROOT / "03_models/modeling_phase1/q1/round3"
CORE = ["fineweb_edu", "fluency_en", "ad_en", "modernbert_cleanliness", "modernbert_readability"]
RUN_ID = "DIAG-Q1-DOMAIN-R3-20260924-v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def corrs(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pearson = np.corrcoef(x, rowvar=False)
    ranked = np.column_stack([rankdata(x[:, j]) for j in range(x.shape[1])])
    spearman = np.corrcoef(ranked, rowvar=False)
    return pearson, spearman


def grouping(corr: np.ndarray, k: int) -> np.ndarray:
    distance = np.maximum(0.0, 1 - corr)
    np.fill_diagonal(distance, 0)
    return fcluster(linkage(squareform(distance, checks=False), method="average"),
                    t=k, criterion="maxclust").astype(int)


def pairwise_membership_agreement(a: np.ndarray, b: np.ndarray) -> float:
    pairs = [(i, j) for i in range(len(a)) for j in range(i + 1, len(a))]
    return sum((a[i] == a[j]) == (b[i] == b[j]) for i, j in pairs) / len(pairs)


def main() -> None:
    manifest = json.loads((INPUT / "INPUT_MANIFEST_v1.json").read_text(encoding="utf-8"))
    q_path = INPUT / "q1_quality_features_v1.csv.gz"
    l_path = INPUT / "a5_13_domain_loss_v1.csv.gz"
    if sha256(q_path) != manifest["processed"]["quality"]["sha256"] or sha256(l_path) != manifest["processed"]["response"]["sha256"]:
        raise RuntimeError("Frozen input hash mismatch")
    q = pd.read_csv(q_path, compression="gzip", usecols=["id", "source", "domain", *CORE], dtype={"id": str})
    base = json.loads((OUT / "Q1_DESCRIPTIVE_QUALITY_METRICS_v1.json").read_text(encoding="utf-8"))
    base_labels = np.array([base["DQ2"]["k2_groups"][s] for s in CORE])
    a1_ids = set(q.loc[q.source == "A1", "id"])
    scopes = {f"A1_{d}": sub for d, sub in q[q.source == "A1"].groupby("domain")}
    for source in ("A2", "A3"):
        scopes[source + "_new_ids"] = q[(q.source == source) & ~q.id.isin(a1_ids)]
    rows = []
    for scope, subset in scopes.items():
        x = subset[CORE].to_numpy(float)
        if not np.isfinite(x).all():
            raise RuntimeError(f"Nonfinite core metric in {scope}")
        _, r = corrs(x)
        labels = grouping(r, 2)
        rows.append({"scope": scope, "n": len(subset),
                     "k2_grouping": "|".join(f"{s}:{int(labels[j])}" for j, s in enumerate(CORE)),
                     "ad_en_singleton": int(np.sum(labels == labels[CORE.index("ad_en")]) == 1),
                     "pairwise_membership_agreement_to_A1_train": pairwise_membership_agreement(base_labels, labels),
                     "rho_cleanliness_readability": float(r[CORE.index("modernbert_cleanliness"), CORE.index("modernbert_readability")]),
                     "rho_ad_readability": float(r[CORE.index("ad_en"), CORE.index("modernbert_readability")])})
    pd.DataFrame(rows).to_csv(OUT / "Q1_DQ2_DOMAIN_GROUP_SUPPORT_v1.csv", index=False, encoding="utf-8-sig")

    loss = pd.read_csv(l_path, compression="gzip").iloc[:, 1:].to_numpy(float)
    pearson, spearman = corrs(loss)
    pearson_negative = int(np.sum(np.triu(pearson < 0, 1)))
    spearman_negative = int(np.sum(np.triu(spearman < 0, 1)))
    if pearson_negative != 24 or spearman_negative != 29:
        raise RuntimeError("A5 prior/current pair-count reconciliation failed")
    response = json.loads((OUT / "Q1_13_DOMAIN_RESPONSE_METRICS_v1.json").read_text(encoding="utf-8"))
    if abs(response["R2_variance_share"][0] - 0.22778044228057512) > 1e-10:
        raise RuntimeError("A5 PCA spectrum mismatch with preregistration evidence")
    result = {
        "run_id": RUN_ID, "status": "DIAGNOSTIC_NON_FINAL",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)),
        "input_sha256": {"Q1": sha256(q_path), "A5": sha256(l_path)},
        "A5_domain_pairs": 78,
        "A5_negative_pearson_pairs": pearson_negative,
        "A5_negative_spearman_pairs": spearman_negative,
        "interpretation": "Different correlation definitions; not a data contradiction",
        "DQ2_scope_rows": len(rows),
        "DQ2_ad_singleton_scope_count": sum(x["ad_en_singleton"] for x in rows),
        "outputs": {"domain_support_csv_sha256": sha256(OUT / "Q1_DQ2_DOMAIN_GROUP_SUPPORT_v1.csv")},
    }
    (OUT / "Q1_DOMAIN_SUPPORT_DIAGNOSTICS_v1.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": RUN_ID, "pearson_negative": pearson_negative,
                      "spearman_negative": spearman_negative,
                      "ad_singleton_scopes": result["DQ2_ad_singleton_scope_count"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
