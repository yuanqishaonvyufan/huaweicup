"""Make four decision-focused Round 3 diagnostic PNGs from checked metrics."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "03_models/modeling_phase1/q1/round3"
OUT = BASE / "figures"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 10,
        "axes.titlesize": 12, "axes.labelsize": 10,
        "xtick.labelsize": 9, "ytick.labelsize": 9,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.spines.top": False, "axes.spines.right": False,
        "savefig.dpi": 190,
    })


def save(fig: plt.Figure, name: str) -> Path:
    path = OUT / name
    fig.savefig(path, bbox_inches="tight", dpi=190)
    plt.close(fig)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    style()
    dq = json.loads((BASE / "Q1_DESCRIPTIVE_QUALITY_METRICS_v1.json").read_text(encoding="utf-8"))
    rsp = json.loads((BASE / "Q1_13_DOMAIN_RESPONSE_METRICS_v1.json").read_text(encoding="utf-8"))
    loads = pd.read_csv(BASE / "Q1_DQ_LOADINGS_AND_GROUPS_v1.csv")
    domains = pd.read_csv(BASE / "Q1_DESCRIPTIVE_DOMAIN_SUMMARY_v1.csv")
    resp_domains = pd.read_csv(BASE / "DOMAIN_HETEROGENEITY_RESULTS_v1.csv")
    corr = pd.read_csv(BASE / "Q1_13_DOMAIN_CORRELATION_v1.csv", index_col=0)
    outputs = []

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3), constrained_layout=True)
    share = np.asarray(dq["DQ1"]["variance_share"])
    axes[0].bar(np.arange(1, 6), share * 100, color="#4E79A7")
    axes[0].set_xticks(np.arange(1, 6))
    axes[0].set_xlabel("Core-signal principal component")
    axes[0].set_ylabel("Variance explained (%)")
    axes[0].set_title("Five-signal spectrum (A1 train, n=40,926)")
    axes[0].set_ylim(0, 55)
    axes[0].text(1, share[0] * 100 + 1, f"{share[0]*100:.1f}%", ha="center")
    y = np.arange(len(loads))
    val = loads.PC1_loading.to_numpy(float)
    err = np.vstack([val - loads.PC1_loading_boot_p025, loads.PC1_loading_boot_p975 - val])
    axes[1].barh(y, val, color=["#E15759" if x == "ad_en" else "#59A14F" for x in loads.signal])
    axes[1].errorbar(val, y, xerr=err, fmt="none", color="black", capsize=2, linewidth=0.8)
    axes[1].set_yticks(y, loads.signal)
    axes[1].invert_yaxis()
    axes[1].set_xlabel("PC1 loading (2.5–97.5% bootstrap)")
    axes[1].set_title("Ad-free signal has small PC1 loading")
    outputs.append(save(fig, "FIG-Q1-R3-001_core_spectrum_loadings.png"))

    selected = domains[domains.scope.str.startswith("A1_") & ~domains.scope.isin(["A1_all", "A1_train", "A1_check"])].copy()
    extra = domains[domains.scope.isin(["A2_new_ids", "A3_new_ids"])].copy()
    selected = pd.concat([selected, extra], ignore_index=True)
    labels = [f"{r.scope} (n={int(r.n):,})" for _, r in selected.iterrows()]
    y = np.arange(len(selected))
    fig, ax = plt.subplots(figsize=(8.7, 5.1), constrained_layout=True)
    ax.scatter(selected.DQ0_mean, y - 0.13, color="#4E79A7", label="DQ0 global reference", s=40)
    ax.scatter(selected.DQ3_mean, y + 0.13, color="#E15759", label="DQ3 within-domain reference", s=40)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0.2, 0.85)
    ax.set_xlabel("Mean descriptive rank score")
    ax.set_title("Within-domain normalization erases between-domain location")
    ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="x", alpha=0.2)
    outputs.append(save(fig, "FIG-Q1-R3-002_domain_normalization.png"))

    fig, ax = plt.subplots(figsize=(8.7, 7.2), constrained_layout=True)
    im = ax.imshow(corr.to_numpy(float), vmin=-1, vmax=1, cmap="RdBu_r", aspect="equal")
    ax.set_xticks(np.arange(len(corr)), corr.columns, rotation=75, ha="right")
    ax.set_yticks(np.arange(len(corr)), corr.index)
    ax.set_title("A5 training-domain Spearman correlation (13 domains, n=512)")
    fig.colorbar(im, ax=ax, fraction=0.045, pad=0.04, label="Spearman rho")
    outputs.append(save(fig, "FIG-Q1-R3-003_13_domain_correlation.png"))

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 5), constrained_layout=True)
    share = np.asarray(rsp["R2_variance_share"])
    axes[0].bar(np.arange(1, 14), share * 100, color="#4E79A7")
    axes[0].set_xticks([1, 3, 5, 7, 9, 11, 13])
    axes[0].set_xlabel("A5 domain-loss principal component")
    axes[0].set_ylabel("Variance explained (%)")
    axes[0].set_title("R2 PC1 retains only 22.8%")
    axes[0].set_ylim(0, 27)
    axes[0].text(1, share[0] * 100 + 0.6, f"{share[0]*100:.1f}%", ha="center")
    order = np.argsort(resp_domains.R2_PC1_loading.to_numpy(float))
    ordered = resp_domains.iloc[order]
    y = np.arange(len(ordered))
    val = ordered.R2_PC1_loading.to_numpy(float)
    err = np.vstack([val - ordered.R2_loading_boot_p025.to_numpy(float),
                     ordered.R2_loading_boot_p975.to_numpy(float) - val])
    axes[1].barh(y, val, color=["#E15759" if v < 0 else "#59A14F" for v in val])
    axes[1].errorbar(val, y, xerr=err, fmt="none", color="black", capsize=2, linewidth=0.8)
    axes[1].set_yticks(y, ordered.domain)
    axes[1].set_xlabel("R2 PC1 loading (2.5–97.5% bootstrap)")
    axes[1].set_title("Many domains weakly represented")
    outputs.append(save(fig, "FIG-Q1-R3-004_response_spectrum_loadings.png"))

    manifest = {
        "status": "DIAGNOSTIC_FIGURES_NOT_PAPER_RESULTS",
        "script_sha256": sha256(Path(__file__)),
        "sources": {"DQ": sha256(BASE / "Q1_DESCRIPTIVE_QUALITY_METRICS_v1.json"),
                    "RSP": sha256(BASE / "Q1_13_DOMAIN_RESPONSE_METRICS_v1.json")},
        "figures": [{"file": x.name, "sha256": sha256(x)} for x in outputs],
    }
    (OUT / "FIGURES_MANIFEST_v1.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"figure_count": len(outputs), "files": [x.name for x in outputs]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
