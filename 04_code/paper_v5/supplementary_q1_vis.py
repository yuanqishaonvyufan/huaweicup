"""Render preregistered Q1 diagnostics from frozen machine outputs only.

Run: SUPP-Q1-VIS-20260925-v1. No model is fitted in this script.
"""
from __future__ import annotations

import csv
import hashlib
import json
import platform
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "06_results/raw/SUPP-Q1-VIS-20260925-v1"
FIG = ROOT / "06_results/figures/paper_v5"
DOMAIN = ROOT / "06_results/raw/Q1_TASK_REPAIR_20260925_v1/Q_FULL_DOMAIN_RESULTS_v1.csv"
RANKS = ROOT / "06_results/raw/Q1_TASK_REPAIR_20260925_v1/Q_FULL_A1_RANKS_v1.csv"
PAIRS = ROOT / "01_data/audits/modeling_phase1/q1/QUALITY_CORRELATION_PAIRS_v1.csv"
FONT = Path("C:/Windows/Fonts/msyh.ttc")
SIGNALS = [
    ("dsir_books", "dsir_wiki", "书籍相似性–百科相似性"),
    ("dsir_books", "dsir_math", "书籍相似性–数学相似性"),
    ("rps_doc_word_count", "rps_doc_unigram_entropy", "词数–一元熵"),
    ("dsir_math", "rps_doc_word_count", "数学相似性–词数"),
    ("rps_doc_word_count", "rps_doc_num_sentences", "词数–句数"),
    ("fluency_en", "modernbert_cleanliness", "流畅度–清洁度"),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT), size)


def base(title: str, subtitle: str, size=(2400, 1450)):
    im = Image.new("RGB", size, "#ffffff")
    d = ImageDraw.Draw(im)
    d.text((110, 60), title, fill="#172238", font=font(66))
    d.text((112, 145), subtitle, fill="#526277", font=font(50))
    d.line([(110, 216), (size[0] - 110, 216)], fill="#cbd5e1", width=3)
    return im, d


def rank_figure(rows: list[dict[str, str]], domains: list[dict[str, str]], target: Path) -> dict:
    selected = [r for r in rows if r["group"].startswith("A1_")]
    assert len(selected) == 7
    for key, stored in [("Q_full_mean", "W0_rank"), ("W1_mean", "W1_rank")]:
        order = sorted(selected, key=lambda r: -float(r[key]))
        calc = {r["group"]: i for i, r in enumerate(order, 1)}
        assert all(calc[r["group"]] == int(r[stored]) for r in selected)
    dq_order = sorted(selected, key=lambda r: -float(r["DQ0_mean"]))
    dq = {r["group"]: i for i, r in enumerate(dq_order, 1)}
    selected.sort(key=lambda r: int(r["W0_rank"]))
    colors = {"W0": "#175eaa", "W1": "#1c9b82", "DQ0": "#cb5a40"}
    im, d = base("Q1 领域排序与评分规则", "A1七域；三列各自排序。排序不是训练收益真值。")
    left, right, top, bottom = 830, 2160, 340, 1100
    for rank in range(1, 8):
        x = left + (rank - 1) * (right - left) / 6
        d.line([(x, top - 25), (x, bottom + 25)], fill="#e1e7ef", width=3)
        d.text((x - 23, top - 85), str(rank), fill="#243249", font=font(51))
    for i, row in enumerate(selected):
        y = top + i * (bottom - top) / 6
        label = row["group"].replace("A1_", "")
        d.text((140, y - 39), label, fill="#243249", font=font(54))
        d.line([(left, y), (right, y)], fill="#dbe3ec", width=2)
        for kind, rank, dy in [
            ("W0", int(row["W0_rank"]), -24),
            ("W1", int(row["W1_rank"]), 0),
            ("DQ0", dq[row["group"]], 24),
        ]:
            x = int(left + (rank - 1) * (right - left) / 6)
            d.ellipse((x - 11, y + dy - 11, x + 11, y + dy + 11), fill=colors[kind])
    y = 1220
    for kind, label, x in [("W0", "Q_full等权", 340), ("W1", "去冗余对照", 930), ("DQ0", "五维描述摘要", 1550)]:
        d.ellipse((x, y, x + 26, y + 26), fill=colors[kind])
        d.text((x + 40, y - 16), label, fill="#243249", font=font(48))
    d.text((140, 1350), "A2/A3非重叠扩展均值与对应A1领域接近；仅属同标注体系复现。", fill="#526277", font=font(46))
    # Source correspondence is checked by group and mean, not inferred from the plotted ranks.
    domain_map = {r["group"]: r for r in domains}
    assert all(abs(float(r["Q_full_mean"]) - float(domain_map[r["group"]]["Q_full_mean"])) < 1e-12 for r in selected)
    im.save(target, dpi=(300, 300))
    return {r["group"]: {"W0": int(r["W0_rank"]), "W1": int(r["W1_rank"]), "DQ0": dq[r["group"]]} for r in selected}


def diverging(v: float) -> str:
    # Negative blue, positive rust, zero near white; all values remain in [-1, 1].
    target = (39, 101, 166) if v < 0 else (185, 66, 50)
    t = abs(v)
    rgb = tuple(round(245 * (1 - t) + target[k] * t) for k in range(3))
    return "#%02x%02x%02x" % rgb


def correlation_figure(rows: list[dict[str, str]], target: Path, csv_target: Path) -> list[dict]:
    lookup = {frozenset((r["signal_a"], r["signal_b"])): r for r in rows}
    assert len(lookup) == len(rows)
    selected = []
    for a, b, label in SIGNALS:
        row = lookup[frozenset((a, b))]
        values = [float(row[f"spearman_{group}"]) for group in ("A1", "A2", "A3")]
        assert all(-1 <= v <= 1 for v in values)
        selected.append({"signal_a": a, "signal_b": b, "label": label,
                         "A1": values[0], "A2": values[1], "A3": values[2]})
    with csv_target.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(selected[0]))
        writer.writeheader(); writer.writerows(selected)
    im, d = base("Q1 预先选定的六组相关诊断", "有符号Spearman相关；每列在对应数据层独立计算。", (2400, 1530))
    x0, cw, y0, ch = 1130, 315, 360, 140
    for j, group in enumerate(("A1", "A2", "A3")):
        d.text((x0 + j * cw + 110, y0 - 85), group, fill="#243249", font=font(56))
    for i, row in enumerate(selected):
        y = y0 + i * ch
        d.text((145, y + 35), row["label"], fill="#243249", font=font(50))
        for j, group in enumerate(("A1", "A2", "A3")):
            x = x0 + j * cw
            value = row[group]
            fill = diverging(value)
            d.rounded_rectangle((x + 7, y + 7, x + cw - 12, y + ch - 10), radius=12, fill=fill)
            d.text((x + 83, y + 39), f"{value:+.3f}", fill="#ffffff" if abs(value) > .45 else "#243249", font=font(50))
    d.text((145, 1280), "蓝：负相关        浅色：接近零        红：正相关", fill="#526277", font=font(48))
    d.text((145, 1360), "相关可提示冗余或长度混杂；不能单独证明语义冲突或因果效应。", fill="#526277", font=font(46))
    im.save(target, dpi=(300, 300))
    return selected


def main() -> None:
    RUN.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    domains, ranks, pairs = read(DOMAIN), read(RANKS), read(PAIRS)
    fig_a = FIG / "FIG-Q1-V5-001_rank_rules.png"
    fig_b = FIG / "FIG-Q1-V5-002_fixed_pair_correlations.png"
    csv_out = RUN / "fixed_six_pairs.csv"
    checked_ranks = rank_figure(ranks, domains, fig_a)
    checked_pairs = correlation_figure(pairs, fig_b, csv_out)
    manifest = {
        "run_id": "SUPP-Q1-VIS-20260925-v1",
        "purpose": "Visualization derivation from frozen Q1 outputs; no model refit",
        "evidence_boundary": "Constructed score ranks and within-layer correlations; no causal quality effect",
        "inputs_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (DOMAIN, RANKS, PAIRS)},
        "code_sha256": sha(Path(__file__)),
        "outputs_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (fig_a, fig_b, csv_out)},
        "checks": {"seven_ranked_domains": len(checked_ranks), "fixed_pairs": len(checked_pairs),
                   "rank_matches_upstream": True, "coefficient_bounds": True,
                   "unordered_pair_lookup_unique": True},
        "environment": {"python": platform.python_version(), "pillow": pillow_version},
    }
    (RUN / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run_id": manifest["run_id"], "figures": [str(fig_a), str(fig_b)]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
