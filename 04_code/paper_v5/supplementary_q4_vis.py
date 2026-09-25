"""Display frozen exogenous Q4 slowdown centers; no forecast is refitted.

Run: SUPP-Q4-VIS-20260925-v1.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import platform
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version


ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "06_results/raw/Q4_TASK_REPAIR_20260925_v1/EXOGENOUS_COMPUTE_SLOWDOWN_SCENARIOS_v1.csv"
SUMMARY = ROOT / "06_results/raw/Q4_TASK_REPAIR_20260925_v1/summary.json"
TASK = ROOT / "06_results/tables/round7/TABLE-Q4-R7-007.csv"
RUN = ROOT / "06_results/raw/SUPP-Q4-VIS-20260925-v1"
FIG = ROOT / "06_results/figures/paper_v5/FIG-Q4-V5-001_exogenous_slowdown.png"
FIG_TASK = ROOT / "06_results/figures/paper_v5/FIG-Q4-V5-002_six_task_deltas.png"
FONT = Path("C:/Windows/Fonts/msyh.ttc")
COLOR = {1.0: "#215e9c", .5: "#1d9584", 0.0: "#c6593e"}
LABEL = {1.0: "ρ=1 参考", .5: "ρ=0.5 中度", 0.0: "ρ=0 强放缓"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def f(size: int):
    return ImageFont.truetype(str(FONT), size)


def main() -> None:
    RUN.mkdir(parents=True, exist_ok=True)
    FIG.parent.mkdir(parents=True, exist_ok=True)
    with CSV.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    upstream = json.loads(SUMMARY.read_text(encoding="utf-8"))
    targets = sorted({r["target"] for r in rows})
    assert len(rows) == 6 and targets == ["2027-09-25", "2028-09-25"]
    by_target = {target: {float(r["rho"]): r for r in rows if r["target"] == target} for target in targets}
    assert all(set(group) == {0.0, .5, 1.0} for group in by_target.values())
    for target, group in by_target.items():
        ref = group[1.0]
        base = float(ref["baseline_dynamic_center"])
        increment = float(ref["reference_parameter_associated_increment"])
        assert increment > 0
        for rho, row in group.items():
            assert abs(float(row["conditional_frontier_center"]) - (base - (1 - rho) * increment)) < 1e-10
            assert row["source_kind"] == "EXOGENOUS_CONDITIONAL_NOT_IDENTIFIED_EFFECT"
            if rho != 1:
                assert not row["conditional_PI95_only_for_reference"]
                assert not row["model_center_range_only_for_reference"]
        interval = ast.literal_eval(ref["conditional_PI95_only_for_reference"])
        assert interval[0] < base < interval[1]
    assert upstream["scenario_reference"]["compute_assumption"].startswith("C≈6ND")
    im = Image.new("RGB", (2400, 1380), "white")
    d = ImageDraw.Draw(im)
    d.text((100, 54), "Q4 外生算力放缓的条件中心", fill="#172238", font=f(67))
    d.text((100, 142), "训练D固定，C≈6ND；ρ为参考正增长的保留比例。", fill="#526277", font=f(50))
    d.line((100, 215, 2300, 215), fill="#cbd5e1", width=3)
    x_centers = {targets[0]: 770, targets[1]: 1800}
    offsets = {1.0: -165, .5: 0, 0.0: 165}
    y_top, y_bottom = 300, 1060
    def yp(v): return int(y_bottom - (v - 50) / 50 * (y_bottom - y_top))
    for v in (50, 60, 70, 80, 90, 100):
        y = yp(v)
        d.line((320, y, 2230, y), fill="#e1e7ef", width=2)
        d.text((180, y - 26), str(v), fill="#526277", font=f(50))
    for target, xc in x_centers.items():
        group = by_target[target]
        ref = group[1.0]
        low, high = ast.literal_eval(ref["conditional_PI95_only_for_reference"])
        x = xc + offsets[1.0]
        d.line((x, yp(low), x, yp(high)), fill="#8ba6c5", width=9)
        d.line((x - 28, yp(low), x + 28, yp(low)), fill="#8ba6c5", width=7)
        d.line((x - 28, yp(high), x + 28, yp(high)), fill="#8ba6c5", width=7)
        for rho in (1.0, .5, 0.0):
            row = group[rho]
            center = float(row["conditional_frontier_center"])
            x = xc + offsets[rho]
            y = yp(center)
            d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=COLOR[rho])
            d.text((x - 70, y - 90 if rho == 1 else y + 28), f"{center:.2f}", fill=COLOR[rho], font=f(50))
        d.text((xc - 190, 1110), target, fill="#243249", font=f(51))
    for x, rho in ((240, 1.0), (870, .5), (1570, 0.0)):
        d.ellipse((x, 1230, x + 30, 1260), fill=COLOR[rho])
        d.text((x + 46, 1216), LABEL[rho], fill="#243249", font=f(50))
    d.text((100, 1318), "灰蓝线仅用于ρ=1；情景差异不是实际算力因果效应。", fill="#526277", font=f(50))
    im.save(FIG, dpi=(300, 300))
    with TASK.open(encoding="utf-8-sig", newline="") as handle:
        tasks = list(csv.DictReader(handle))
    assert len(tasks) == 6 and len({r["benchmark"] for r in tasks}) == 6
    assert all(float(r["delta_F"]) > 0 and float(r["delta_S"]) >= 0 for r in tasks)
    im2 = Image.new("RGB", (2400, 1380), "white")
    q = ImageDraw.Draw(im2)
    q.text((100, 54), "Q4 六任务前沿的端点变化", fill="#172238", font=f(67))
    q.text((100, 142), "同一28天 q90 规则；两栏采用不同横轴量尺。", fill="#526277", font=f(50))
    q.line((100, 215, 2300, 215), fill="#cbd5e1", width=3)
    q.text((575, 260), "六任务前沿增量 ΔF（分）", fill="#243249", font=f(49))
    q.text((1510, 260), "参数关联分量 ΔS（分）", fill="#243249", font=f(49))
    for i, row in enumerate(tasks):
        y = 390 + i * 130
        name = row["benchmark"]
        full = float(row["delta_F"])
        associated = float(row["delta_S"])
        q.text((105, y - 18), name, fill="#243249", font=f(50))
        q.line((540, y, 1260, y), fill="#e1e7ef", width=2)
        q.line((1480, y, 2180, y), fill="#e1e7ef", width=2)
        q.rounded_rectangle((540, y - 26, 540 + int(full / 36 * 690), y + 26), radius=8, fill="#245d9a")
        q.rounded_rectangle((1480, y - 26, 1480 + int(associated / 5 * 650), y + 26), radius=8, fill="#bf6047")
        q.text((1290, y - 28), f"{full:.2f}", fill="#245d9a", font=f(47))
        q.text((2210, y - 28), f"{associated:.2f}", fill="#a84b36", font=f(47))
    q.text((110, 1220), "蓝：观测前沿端点变化    红：当前回归规格的参数关联描述分量", fill="#526277", font=f(48))
    q.text((110, 1310), "ΔS 不是完整规模贡献；剩余变化也不能归为纯技术因果效果。", fill="#526277", font=f(48))
    im2.save(FIG_TASK, dpi=(300, 300))
    manifest = {
        "run_id": "SUPP-Q4-VIS-20260925-v1",
        "purpose": "Display six frozen exogenous slowdown scenario centers and reference-only intervals",
        "evidence_boundary": "Benchmark-space condition under fixed D and C≈6ND; actual compute effect not identified",
        "inputs_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (CSV, SUMMARY, TASK)},
        "code_sha256": sha(Path(__file__)),
        "outputs_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (FIG, FIG_TASK)},
        "checks": {"rows": 6, "two_target_dates": True, "scenario_center_identity": True,
                   "interval_only_reference": True, "positive_exogenous_reference": True,
                   "six_task_rows": 6},
        "environment": {"python": platform.python_version(), "pillow": pillow_version},
    }
    (RUN / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run_id": manifest["run_id"], "figures": [str(FIG), str(FIG_TASK)]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
