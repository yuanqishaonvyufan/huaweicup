"""Plot Q3 budget utilization and active sets from the frozen 51-point path.

Run: SUPP-Q3-VIS-20260925-v1. No optimizer is called here.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version


ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "06_results/raw/EXP-Q3-BASE-R6-20260924-v1/budget_path.csv"
SUMMARY = ROOT / "06_results/raw/EXP-Q3-BASE-R6-20260924-v1/summary.json"
RUN = ROOT / "06_results/raw/SUPP-Q3-VIS-20260925-v1"
FIG = ROOT / "06_results/figures/paper_v5/FIG-Q3-V5-001_budget_composition.png"
FONT = Path("C:/Windows/Fonts/msyh.ttc")


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
    assert len(rows) == summary["rows"] == 51
    budgets = [float(r["Budget_FLOPs"]) for r in rows]
    assert budgets == sorted(budgets) and len(set(budgets)) == 51
    records = []
    for row, budget in zip(rows, budgets):
        train = float(row["train_FLOPs"])
        attention = float(row["attention_FLOPs"])
        quality = float(row["quality_FLOPs"])
        used = float(row["total_FLOPs"])
        slack = float(row["budget_slack_FLOPs"])
        assert abs(used - (train + attention + quality)) <= max(1e-8 * budget, 1)
        assert abs(budget - used - slack) <= max(1e-8 * budget, 1)
        assert quality == 0
        records.append({"budget": budget, "train": train / budget, "attention": attention / budget,
                        "unused": slack / budget, "active": row["active_constraints"]})
    transitions = summary["transitions"]
    d_cap = transitions["unconstrained_D_upper_C"]
    both = transitions["both_upper_saturation_C"]
    assert 1e19 < d_cap < both < 1e24
    assert all("BUDGET_ACTIVE" in r["active"] for r in records if r["budget"] < d_cap)
    assert all("BUDGET_SLACK" in r["active"] for r in records if r["budget"] > both)
    im = Image.new("RGB", (2400, 1450), "white")
    d = ImageDraw.Draw(im)
    d.text((100, 58), "Q3 预算使用与支持约束转移", fill="#172238", font=f(67))
    d.text((100, 145), "51档预算；基础情景 Q=0.5、上下文2048，质量增量成本为零。", fill="#526277", font=f(46))
    d.line((100, 215, 2300, 215), fill="#cbd5e1", width=3)
    x0, x1, y0, y1 = 300, 2250, 355, 1060
    def xp(b): return int(x0 + (math.log10(b) - 19) / 5 * (x1 - x0))
    def yp(s): return int(y1 - s * (y1 - y0))
    for v in [0, .25, .5, .75, 1]:
        y = yp(v)
        d.line((x0, y, x1, y), fill="#e0e7ef", width=2)
        d.text((165, y - 25), f"{100*v:.0f}%", fill="#526277", font=f(45))
    for e in range(19, 25):
        x = xp(10 ** e)
        d.line((x, y0, x, y1), fill="#e0e7ef", width=2)
        d.text((x - 35, y1 + 35), f"10^{e}", fill="#526277", font=f(45))
    points = [(xp(r["budget"]), r["train"], r["train"] + r["attention"]) for r in records]
    train_poly = [(x0, y1)] + [(x, yp(t)) for x, t, _ in points] + [(x1, y1)]
    attention_poly = [(x, yp(t)) for x, t, _ in points] + [(x, yp(a)) for x, _, a in reversed(points)]
    unused_poly = [(x, yp(a)) for x, _, a in points] + [(x1, y0), (x0, y0)]
    d.polygon(unused_poly, fill="#d6dde7")
    d.polygon(attention_poly, fill="#239987")
    d.polygon(train_poly, fill="#245d9a")
    for threshold, label, x_offset in [(d_cap, "D 支持上界", -250), (both, "N、D 双上界", 24)]:
        x = xp(threshold)
        for yy in range(y0, y1, 20):
            d.line((x, yy, x, min(yy + 10, y1)), fill="#bf573b", width=4)
        d.text((x + x_offset, 265), label, fill="#a44c33", font=f(42))
    d.text((700, 1140), "预算 C（FLOPs，对数刻度）", fill="#243249", font=f(49))
    for x, color, label in [(170, "#245d9a", "基础训练"), (760, "#239987", "注意力"), (1180, "#d6dde7", "未使用预算")]:
        d.rectangle((x, 1230, x + 50, 1270), fill=color)
        d.text((x + 68, 1220), label, fill="#243249", font=f(47))
    d.text((170, 1352), "高预算未使用份额上升源于统计支持上界；不表示现实算力无收益。", fill="#526277", font=f(43))
    im.save(FIG, dpi=(300, 300))
    manifest = {
        "run_id": "SUPP-Q3-VIS-20260925-v1",
        "purpose": "Visual derivation of cost shares and support transitions from the frozen 51-budget path",
        "evidence_boundary": "B1 support rectangle and problem-provided FLOPs proxy; not industry saturation",
        "inputs_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (CSV, SUMMARY)},
        "code_sha256": sha(Path(__file__)),
        "outputs_sha256": {str(FIG.relative_to(ROOT)): sha(FIG)},
        "checks": {"rows": 51, "monotone_budget": True, "cost_components_balance": True,
                   "budget_balance": True, "quality_cost_zero_in_baseline": True,
                   "D_cap_FLOPs": d_cap, "both_caps_FLOPs": both,
                   "utilization_at_1e24": 1 - records[-1]["unused"]},
        "environment": {"python": platform.python_version(), "pillow": pillow_version},
    }
    (RUN / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run_id": manifest["run_id"], "figure": str(FIG)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
