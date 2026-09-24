"""Build five inspectable Q1 Round 4 paper-table candidates from frozen CSVs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "03_models/modeling_phase1/q1/round4"
OUT = BASE / "tables"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown(title: str, headers: list[str], rows: list[list[str]], note: str) -> str:
    parts = ["# " + title, "", "| " + " | ".join(headers) + " |",
             "|" + "|".join(["---"] * len(headers)) + "|"]
    parts.extend("| " + " | ".join(str(x) for x in row) + " |" for row in rows)
    parts.extend(["", "注：" + note, ""])
    return "\n".join(parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    roles_path = BASE / "Q1_FULL22_ROLE_MAP_v1.csv"
    core_path = BASE / "Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv"
    train_path = BASE / "P_RESPONSE_TRAIN_CV_RESULTS_v1.csv"
    valid_path = BASE / "P_RESPONSE_VALIDATION_METRICS_v2.csv"
    domain_path = BASE / "P_RESPONSE_DOMAIN_VALIDATION_v2.csv"
    support_path = BASE / "P_SUPPORT_VALIDATION_ROWS_v2.csv"
    roles = pd.read_csv(roles_path)
    core = pd.read_csv(core_path)
    train = pd.read_csv(train_path)
    valid = pd.read_csv(valid_path)
    domain = pd.read_csv(domain_path)
    support = pd.read_csv(support_path)
    outputs = []

    rows = [[r.signal_id, r.full22_role, r.DOWNSTREAM_ELIGIBILITY, r.direction_status]
            for r in roles.itertuples()]
    title = "TABLE-Q1-R4-001 全 22 项信号角色与下游资格"
    note = "角色是 Q1 完整画像的展示/建模职责，不等于通用质量方向；TYPE E=0。来源：Q1_FULL22_ROLE_MAP_v1.csv。"
    path = OUT / "TABLE_Q1_R4_001_full22_roles.md"
    path.write_text(markdown(title, ["指标", "Full-22 角色", "下游资格", "方向"], rows, note), encoding="utf-8")
    outputs.append((path, roles_path, False, "appendix_candidate"))

    groups = ["A1_arxiv", "A2_new_ids", "A1_github", "A3_new_ids"]
    names = {"fineweb_edu": "教育", "fluency_en": "流畅", "ad_en": "无广告",
             "modernbert_cleanliness": "整洁", "modernbert_readability": "可读"}
    rows = []
    for group in groups:
        sub = core[core.group == group].set_index("signal_id")
        vals = [float(sub.loc[x, "mean_relative_percentile"]) for x in names]
        rows.append([group, f"{int(sub.n_physical.iloc[0]):,}", *[f"{v:.3f}" for v in vals],
                     f"{sum(vals)/5:.3f}"])
    path = OUT / "TABLE_Q1_R4_002_core_domain_comparison.md"
    note = "五维值为相对 A1 训练参考的均值分位，DQ0 是其等权摘要；A2/A3 用非重叠 ID，不是独立训练干预。来源：Q1_CORE_DOMAIN_QUALITY_PROFILE_v1.csv。"
    path.write_text(markdown("TABLE-Q1-R4-002 质量抽样与扩展域对照",
                             ["来源域", "n", *names.values(), "DQ0"], rows, note), encoding="utf-8")
    outputs.append((path, core_path, True, "body_candidate"))

    rows = []
    for name in ("M0", "M1", "M2"):
        t = train[train.model == name].iloc[0]
        v = valid[(valid.scale == "1M") & (valid.model == name)].iloc[0]
        rows.append([name, f"{t.alpha:.4g}", f"{t.cv_balanced_score:.4f}",
                     f"{v.R0_RMSE_raw:.4f}", f"{v.mean_domain_RMSE_raw:.4f}",
                     "暂选" if name == "M1" else "基线" if name == "M0" else "未获稳定验证增益"])
    path = OUT / "TABLE_Q1_R4_003_model_comparison.md"
    note = "A5 五折综合分数是训练内选参指标；A7 为 1M 同尺度外部验证。M3 训练门槛未触发。来源：训练/验证机器记录与对应 CSV。"
    path.write_text(markdown("TABLE-Q1-R4-003 p 响应模型比较",
                             ["模型", "ridge α", "A5 五折综合分数↓", "A7 R0 RMSE↓", "A7 逐域平均 RMSE↓", "决定"],
                             rows, note), encoding="utf-8")
    outputs.append((path, valid_path, True, "body_candidate"))

    d = domain[(domain.scale == "1M") & (domain.model == "M1")].sort_values("RMSE_ratio_to_M0_raw")
    rows = [[r.domain, f"{r.RMSE_raw:.4f}", f"{r.RMSE_ratio_to_M0_raw:.3f}",
             f"{r.rank_spearman:.3f}"] for r in d.itertuples()]
    path = OUT / "TABLE_Q1_R4_004_domain_validation.md"
    note = "比率 <1 表示 A7 M1 比 M0 误差小；13 域必须与 R0 并报。来源：P_RESPONSE_DOMAIN_VALIDATION_v2.csv。"
    path.write_text(markdown("TABLE-Q1-R4-004 A7 逐域验证",
                             ["验证域", "M1 RMSE↓", "M1/M0 RMSE↓", "运行排序 ρ"], rows, note), encoding="utf-8")
    outputs.append((path, domain_path, True, "body_candidate"))

    counts = support.groupby(["scale", "support_class"]).size().unstack(fill_value=0)
    rows = []
    for scale in ("1M", "60M", "1B"):
        v = valid[(valid.scale == scale) & (valid.model == "M1")].iloc[0]
        c = counts.loc[scale]
        rows.append([scale, int(v.n), f"{v.R0_centered_RMSE_ratio_to_M0:.3f}",
                     f"{v.mean_domain_centered_RMSE_ratio_to_M0:.3f}",
                     int(c.get("IN_SUPPORT", 0)), int(c.get("NEAR_SUPPORT", 0)),
                     int(c.get("OUT_OF_SUPPORT", 0))])
    path = OUT / "TABLE_Q1_R4_005_scale_support.md"
    note = "中心化比值仅是跨规模配比形状检验；A6/A8 为同一 p，1B 失败。经验支持类别不等于现实可实施域。来源：P_RESPONSE_VALIDATION_METRICS_v2.csv 与 P_SUPPORT_VALIDATION_ROWS_v2.csv。"
    path.write_text(markdown("TABLE-Q1-R4-005 规模转移与支持域",
                             ["规模", "n", "R0 中心化 RMSE 比↓", "13 域平均中心化 RMSE 比↓", "IN", "NEAR", "OUT"],
                             rows, note), encoding="utf-8")
    outputs.append((path, support_path, True, "body_candidate"))

    manifest = {"status": "PAPER_TABLE_CANDIDATES_PENDING_GATE2",
                "script_sha256": sha256(Path(__file__)),
                "tables": [{"path": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(p),
                            "source": str(s.relative_to(ROOT)).replace("\\", "/"),
                            "source_sha256": sha256(s), "publish_candidate": publish,
                            "placement": placement} for p, s, publish, placement in outputs]}
    (OUT / "table_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"table_count": len(outputs), "files": [p.name for p, _, _, _ in outputs]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
