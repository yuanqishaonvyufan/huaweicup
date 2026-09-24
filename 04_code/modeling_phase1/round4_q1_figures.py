"""Create four source-backed Q1 Round 4 decision figures (PDF + PNG)."""

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
BASE = ROOT / "03_models/modeling_phase1/q1/round4"
OUT = BASE / "figures"
FONT = "C:/Windows/Fonts/msyh.ttc"
CORE = ["fineweb_edu", "fluency_en", "ad_en", "modernbert_cleanliness", "modernbert_readability"]
CORE_CN = ["教育价值", "流畅度", "无广告", "整洁度", "可读性"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def style() -> None:
    from matplotlib.font_manager import FontProperties
    font = FontProperties(fname=FONT)
    plt.rcParams.update({"font.family": font.get_name(), "font.size": 14,
                         "axes.labelsize": 14, "xtick.labelsize": 12, "ytick.labelsize": 12,
                         "legend.fontsize": 12, "pdf.fonttype": 42,
                         "figure.facecolor": "white", "axes.facecolor": "white",
                         "axes.spines.top": False, "axes.spines.right": False})


def save(fig: plt.Figure, base: str) -> tuple[Path, Path]:
    pdf = OUT / (base + ".pdf")
    png = OUT / (base + ".png")
    fig.savefig(pdf, bbox_inches="tight", facecolor="white")
    fig.savefig(png, bbox_inches="tight", dpi=300, facecolor="white")
    plt.close(fig)
    return pdf, png


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    style()
    core_path = BASE / "Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv"
    domain_path = BASE / "P_RESPONSE_DOMAIN_VALIDATION_v2.csv"
    metric_path = BASE / "P_RESPONSE_VALIDATION_METRICS_v2.csv"
    support_path = BASE / "P_SUPPORT_VALIDATION_ROWS_v2.csv"
    core = pd.read_csv(core_path)
    domain = pd.read_csv(domain_path)
    metric = pd.read_csv(metric_path)
    support = pd.read_csv(support_path)
    specs = []

    groups = ["A1_arxiv", "A1_book", "A1_c4", "A1_commoncrawl", "A1_github",
              "A1_stackexchange", "A1_wikipedia", "A2_new_ids", "A3_new_ids"]
    matrix = core.pivot(index="group", columns="signal_id", values="mean_relative_percentile").loc[groups, CORE]
    n_map = core.groupby("group").n_physical.first().to_dict()
    labels = [g.replace("_", " ") + f"  n={n_map[g]:,}" for g in groups]
    fig, ax = plt.subplots(figsize=(8.5, 5.4), constrained_layout=True)
    im = ax.imshow(matrix.to_numpy(float), vmin=0, vmax=1, cmap="Blues", aspect="auto")
    ax.set_xticks(range(5), CORE_CN)
    ax.set_yticks(range(9), labels)
    for i in range(9):
        for j in range(5):
            v = matrix.iloc[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    fontsize=13, color="white" if v > 0.55 else "black")
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.03, label="相对 A1 训练参考的平均分位")
    pdf, png = save(fig, "FIG-Q1-R4-001_core_domain_profile")
    specs.append(("FIG-Q1-R4-001", pdf, png, "五维质量画像存在明显域差；样本与扩展域可对照",
                  "比较五项 CORE 在各来源域的相对位置", core_path, True, "body"))

    d = domain[(domain.scale == "1M") & (domain.model == "M1")].sort_values("RMSE_ratio_to_M0_raw")
    fig, ax = plt.subplots(figsize=(7.5, 6.6), constrained_layout=True)
    y = np.arange(len(d))
    ax.axvline(1, color="black", linestyle="--", linewidth=1.2)
    ax.hlines(y, d.RMSE_ratio_to_M0_raw, 1, color="#5B5B5B", linewidth=1.0)
    ax.scatter(d.RMSE_ratio_to_M0_raw, y, color="#245A81", s=58, zorder=3)
    ax.set_yticks(y, d.domain)
    ax.invert_yaxis()
    ax.set_xlim(0.35, 1.12)
    ax.set_xlabel("M1 / M0 逐域 RMSE（A7，1M）")
    ax.grid(axis="x", alpha=0.15)
    for yy, v in zip(y, d.RMSE_ratio_to_M0_raw):
        ax.text(v - 0.02, yy, f"{v:.2f}", ha="right", va="center", fontsize=12)
    pdf, png = save(fig, "FIG-Q1-R4-002_domain_validation_gain")
    specs.append(("FIG-Q1-R4-002", pdf, png, "M1 在 A7 1M 的 13 个域均低于 M0 误差",
                  "检查综合改善是否遮蔽任一领域恶化", domain_path, True, "body"))

    d = metric[metric.model == "M1"].set_index("scale").loc[["1M", "60M", "1B"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.5), constrained_layout=True)
    x = np.arange(3)
    width = 0.34
    a = ax.bar(x - width / 2, d.R0_centered_RMSE_ratio_to_M0, width,
               color="#245A81", label="R0 中心化误差")
    b = ax.bar(x + width / 2, d.mean_domain_centered_RMSE_ratio_to_M0, width,
               color="#B66A29", hatch="//", label="13 域平均中心化误差")
    ax.axhline(1, color="black", linestyle="--", linewidth=1.2)
    ax.set_xticks(x, ["1M (n=256)", "60M (n=256)", "1B (n=64)"])
    ax.set_ylabel("M1 / M0 中心化 RMSE 比")
    ax.set_ylim(0, 3.55)
    ax.legend(frameon=False, loc="upper left")
    for bars in (a, b):
        for bar in bars:
            low_near_line = 0.75 < bar.get_height() < 1
            label_y = bar.get_height() - 0.05 if low_near_line else bar.get_height() + 0.04
            ax.text(bar.get_x() + bar.get_width() / 2, label_y,
                    f"{bar.get_height():.2f}", ha="center",
                    va="top" if low_near_line else "bottom", fontsize=12,
                    color="white" if low_near_line and bars is a else "black")
    pdf, png = save(fig, "FIG-Q1-R4-003_scale_transfer_failure")
    specs.append(("FIG-Q1-R4-003", pdf, png, "配比效应在 1M/60M 可见，但 1B 中心化迁移失败",
                  "区分同尺度验证与跨规模转移", metric_path, True, "body"))

    counts = support.groupby(["scale", "support_class"]).size().unstack(fill_value=0).loc[["1M", "60M", "1B"]]
    fig, ax = plt.subplots(figsize=(7.3, 4.4), constrained_layout=True)
    left = np.zeros(3)
    colors = {"IN_SUPPORT": "#245A81", "NEAR_SUPPORT": "#9B9B9B", "OUT_OF_SUPPORT": "#B66A29"}
    names = {"IN_SUPPORT": "凸包内且近邻", "NEAR_SUPPORT": "局部近邻", "OUT_OF_SUPPORT": "远离支持"}
    for category in ("IN_SUPPORT", "NEAR_SUPPORT", "OUT_OF_SUPPORT"):
        values = counts.get(category, pd.Series([0, 0, 0], index=counts.index)).to_numpy(int)
        bars = ax.barh(np.arange(3), values, left=left, color=colors[category], label=names[category])
        for bar, value in zip(bars, values):
            if value >= 15:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                        str(value), ha="center", va="center", color="white" if category == "IN_SUPPORT" else "black", fontsize=12)
        left += values
    ax.set_yticks(np.arange(3), ["1M", "60M", "1B"])
    ax.invert_yaxis()
    ax.set_xlabel("验证配比组数")
    ax.legend(frameon=False, ncol=3, loc="lower right")
    pdf, png = save(fig, "FIG-Q1-R4-004_support_strata")
    specs.append(("FIG-Q1-R4-004", pdf, png, "观测凸包窄；验证主要落在训练近邻范围",
                  "对照经验凸包与局部近邻覆盖", support_path, False, "appendix_candidate"))

    manifest = {"version": 1, "status": "PAPER_FIGURE_CANDIDATES_PENDING_COMPILED_LAYOUT_QA",
                "script_sha256": sha256(Path(__file__)), "figures": []}
    for fig_id, pdf, png, claim, task, source, publish, placement in specs:
        manifest["figures"].append({"figure_id": fig_id,
                                     "path": str(pdf.relative_to(ROOT)).replace("\\", "/"),
                                     "preview": str(png.relative_to(ROOT)).replace("\\", "/"),
                                     "claim": claim, "source": str(source.relative_to(ROOT)).replace("\\", "/"),
                                     "source_sha256": sha256(source), "reader_task": task,
                                     "publish": publish, "placement": placement,
                                     "pdf_sha256": sha256(pdf), "png_sha256": sha256(png)})
    (OUT / "figure_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"figures": len(specs), "pdfs": [x[1].name for x in specs]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
