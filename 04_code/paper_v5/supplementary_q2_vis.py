"""Plot frozen Q2 whole-trajectory bootstrap without fitting any model.

Run: SUPP-Q2-VIS-20260925-v1.
"""
from __future__ import annotations

import csv
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version


ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "06_results/raw/EXP-Q2-ND-R5-20260924-v1/cluster_bootstrap.csv"
SUMMARY = ROOT / "06_results/raw/EXP-Q2-ND-R5-20260924-v1/summary.json"
RUN = ROOT / "06_results/raw/SUPP-Q2-VIS-20260925-v1"
FIG = ROOT / "06_results/figures/paper_v5/FIG-Q2-V5-001_bootstrap_joint.png"
FONT = Path("C:/Windows/Fonts/msyh.ttc")
KEYS = ["E", "A", "B", "alpha", "beta"]
LABEL = {"E": "E", "A": "A", "B": "B", "alpha": "α", "beta": "β"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def f(size: int):
    return ImageFont.truetype(str(FONT), size)


def main() -> None:
    RUN.mkdir(parents=True, exist_ok=True)
    FIG.parent.mkdir(parents=True, exist_ok=True)
    with CSV.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert len(rows) == summary["bootstrap_valid"] == 200
    assert summary["bootstrap_boundary"] == 0
    assert all(row["boundary"].lower() == "false" for row in rows)
    main = summary["parameters"]
    values = {key: np.array([float(row[key]) for row in rows]) for key in KEYS}
    assert all(np.isfinite(v).all() for v in values.values())
    quantiles = {key: np.quantile(values[key], [.025, .5, .975]) for key in KEYS}
    for key in KEYS:
        assert np.allclose(quantiles[key], summary["parameter_conditional_interval"][key], rtol=0, atol=1e-10)
    rel = {key: 100 * (values[key] / main[key] - 1) for key in KEYS}
    im = Image.new("RGB", (2400, 1360), "white")
    d = ImageDraw.Draw(im)
    d.text((100, 48), "Q2 整轨迹重抽样参数稳定性", fill="#172238", font=f(68))
    d.text((100, 142), "200次；左为五参数相对主估计的条件分位，右为 α–β 联合散点。", fill="#526277", font=f(45))
    d.line((100, 213, 2300, 213), fill="#cbd5e1", width=3)
    # Parameter intervals in percentage deviation from the unchanged primary fit.
    lx0, lx1, ly0, ly1 = 250, 1190, 350, 1040
    def px(v): return int(lx0 + (v + .08) / .16 * (lx1 - lx0))
    for v in [-.08, -.04, 0, .04, .08]:
        x = px(v)
        d.line((x, ly0 - 30, x, ly1 + 32), fill="#dbe3ec" if v else "#75859a", width=2)
        d.text((x - 60, ly1 + 55), f"{v:+.2f}%", fill="#526277", font=f(39))
    d.text((lx0 + 130, 255), "相对主估计偏移（%）", fill="#243249", font=f(48))
    summary_rows = []
    for i, key in enumerate(KEYS):
        y = ly0 + i * 143
        q = 100 * (quantiles[key] / main[key] - 1)
        d.text((120, y - 35), LABEL[key], fill="#243249", font=f(53))
        d.line((px(q[0]), y, px(q[2]), y), fill="#175eaa", width=14)
        for v in [q[0], q[2]]:
            x = px(v)
            d.line((x, y - 20, x, y + 20), fill="#175eaa", width=6)
        x = px(q[1])
        d.ellipse((x - 13, y - 13, x + 13, y + 13), fill="#cb5a40")
        summary_rows.append({"parameter": key, "main": main[key], "p025": float(quantiles[key][0]),
                             "p50": float(quantiles[key][1]), "p975": float(quantiles[key][2])})
    # Joint alpha-beta draws, each whole trajectory sampled as a block.
    rx0, rx1, ry0, ry1 = 1480, 2210, 345, 1060
    ax = rel["alpha"]; by = rel["beta"]
    assert np.max(np.abs(ax)) < .18 and np.max(np.abs(by)) < .04
    def sx(v): return int(rx0 + (v + .18) / .36 * (rx1 - rx0))
    def sy(v): return int(ry1 - (v + .04) / .08 * (ry1 - ry0))
    for v in [-.15, -.075, 0, .075, .15]:
        x = sx(v)
        d.line((x, ry0, x, ry1), fill="#e1e7ee" if v else "#8796a9", width=2)
        d.text((x - 37, ry1 + 27), f"{v:+.2f}", fill="#526277", font=f(35))
    for v in [-.03, 0, .03]:
        y = sy(v)
        d.line((rx0, y, rx1, y), fill="#e1e7ee" if v else "#8796a9", width=2)
        d.text((rx0 - 115, y - 24), f"{v:+.2f}", fill="#526277", font=f(35))
    for x, y in zip(ax, by):
        xx, yy = sx(x), sy(y)
        d.ellipse((xx - 5, yy - 5, xx + 5, yy + 5), fill="#356d9d")
    d.text((1675, 255), "α–β 联合偏移（%）", fill="#243249", font=f(48))
    d.text((1660, 1140), "横轴 α，纵轴 β；每点为一整轨迹重抽样。", fill="#526277", font=f(37))
    d.text((100, 1275), "窄带仅说明八条附件轨迹及所选加性幂律下的数值稳定，不代表外部泛化区间。", fill="#526277", font=f(42))
    im.save(FIG, dpi=(300, 300))
    csv_out = RUN / "parameter_conditional_quantiles.csv"
    with csv_out.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]))
        writer.writeheader(); writer.writerows(summary_rows)
    manifest = {
        "run_id": "SUPP-Q2-VIS-20260925-v1",
        "purpose": "Display the frozen 200 whole-trajectory bootstrap draws without refitting",
        "evidence_boundary": "Eight attachment trajectories and one selected additive law only",
        "inputs_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (CSV, SUMMARY)},
        "code_sha256": sha(Path(__file__)),
        "outputs_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (FIG, csv_out)},
        "checks": {"rows": len(rows), "all_finite": True, "boundary_draws": 0,
                   "quantiles_match_upstream": True},
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "pillow": pillow_version},
    }
    (RUN / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run_id": manifest["run_id"], "figure": str(FIG)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
