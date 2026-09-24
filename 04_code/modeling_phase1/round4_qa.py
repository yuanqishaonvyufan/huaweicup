"""Read-only Round 4 artifact audit; standard library only, no model fitting."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import struct
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "03_models/modeling_phase1/q1/round4"
RAW = ROOT / "01_data/raw/real_attachments"
REVIEW = ROOT / "10_review"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def records(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def data(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean(values) -> float:
    items = list(values)
    return sum(items) / len(items)


def rmse(values) -> float:
    return math.sqrt(mean(x * x for x in values))


def audit() -> dict:
    errors: list[str] = []
    checks: dict[str, object] = {}

    def demand(ok: bool, description: str) -> None:
        if not ok:
            errors.append(description)

    def near(actual: float, expected: float, description: str) -> None:
        if not math.isclose(float(actual), float(expected), rel_tol=1e-10, abs_tol=1e-10):
            errors.append(f"{description}: {actual} != {expected}")

    bp = R4 / "P_RESPONSE_FROZEN_MODEL_BUNDLE_v1.json"
    b = data(bp)
    t = data(R4 / "P_RESPONSE_TRAIN_METRICS_v1.json")
    v = data(R4 / "P_RESPONSE_VALIDATION_METRICS_v2.json")
    q = data(R4 / "Q1_QUALITY_CLOSURE_METRICS_v1.json")
    demand(b["run_id"] == t["run_id"] == "EXP-Q1-PRESP-TRAIN-R4-20260924-v1", "train Run ID")
    demand(v["run_id"] == "VAL-Q1-PRESP-A6A11-R4-20260924-v2", "validation Run ID")
    demand(b["status"] == "FROZEN_BEFORE_A6_A11_VALIDATION", "bundle freeze status")
    demand(b["A6_A11_loss_read"] is False and t["A6_A11_loss_read"] is False, "A6–A11 training leakage flag")
    demand(digest(bp) == t["bundle_sha256"] == v["train_bundle_sha256"], "frozen bundle SHA-256")
    fixed = [
        ("04_code/modeling_phase1/round4_train_p_response.py", b["training_script_sha256"]),
        ("04_code/modeling_phase1/round4_validate_p_response.py", v["script_sha256"]),
        ("03_models/modeling_phase1/q1/round4/P_RESPONSE_PREFIT_CONTRACT_v1.md", b["contract_sha256"]),
        ("03_models/modeling_phase1/q1/round4/P_RESPONSE_VALIDATION_RULE_ADDENDUM_v1.md", v["validation_addendum_sha256"]),
        ("03_models/modeling_phase1/q1/P1_1_13_DOMAIN_RESPONSE_PREREG_FINAL_v1.md", b["P1_1_prereg_sha256"]),
    ]
    for relative, expected in fixed:
        demand(digest(ROOT / relative) == expected, f"frozen file hash: {relative}")
    code = (ROOT / fixed[0][0]).read_text(encoding="utf-8")
    demand(code.count("pd.read_csv(") == 2 and "train_mixture_1m.csv" in code
           and "train_pile_loss_1m.csv" in code and "test_pile_loss_" not in code,
           "training script input scope")
    demand(b["training_design_rank"] == 16 and 40 < b["training_design_condition"] < 50,
           "16D design rank/condition")
    demand(set(b["models"]) == {"M0", "M1", "M2"} and b["M3_gate_passed"] is False
           and t["M3_pattern_trigger"] is False and v["M3_activated"] is False, "M3 trigger/model set")
    demand(bp.stat().st_mtime_ns < (R4 / "P_RESPONSE_VALIDATION_METRICS_v2.json").stat().st_mtime_ns,
           "freeze/validation file chronology")
    checks["freeze"] = {"train_run": b["run_id"], "validation_run": v["run_id"],
                        "bundle_sha256": digest(bp), "rank": b["training_design_rank"],
                        "condition": b["training_design_condition"], "A6_A11_training_loss_read": False}

    raw_hash = {r["relative_path"]: r["sha256"] for r in records(ROOT / "01_data/raw/RAW_SHA256.csv")}
    for key, relative in [("A4", "A_data_value/regmix_tables/train_mixture_1m.csv"),
                          ("A5", "A_data_value/regmix_tables/train_pile_loss_1m.csv")]:
        expected = b["raw_input_sha256"][key]
        demand(raw_hash.get(relative) == expected and digest(RAW / relative) == expected,
               f"raw input hash {key}")
    for key, item in v["official_mapping"].items():
        relative, expected = item["path"], item["sha256"]
        demand(raw_hash.get(relative) == expected and digest(RAW / relative) == expected,
               f"raw input hash {key}")
    demand(v["official_mapping"]["A6"]["sha256"] == v["official_mapping"]["A8"]["sha256"]
           and v["A6_A8_identical_p"] is True, "A6/A8 shared composition")
    checks["raw_inputs"] = "A4/A5 and A6–A11 match official raw SHA-256 manifest"

    demand(digest(R4 / "P_RESPONSE_TRAIN_CV_RESULTS_v1.csv") == b["outputs"]["train_results_sha256"],
           "training CV output hash")
    demand(digest(R4 / "P_RESPONSE_TRAIN_OOF_PREDICTIONS_v1.csv") == b["outputs"]["oof_sha256"],
           "training OOF output hash")
    for name, item in v["outputs"].items():
        path = ROOT / item["path"]
        demand(digest(path) == item["sha256"] and len(records(path)) == item["rows"],
               f"validation output {name} hash/rows")
    for name, item in q["outputs"].items():
        demand(digest(ROOT / item["path"]) == item["sha256"], f"quality output {name} hash")
    demand(sum(q["role_counts"].values()) == 22 and q["semantic_conflicts_confirmed"] == 0
           and q["q2_identifiable_quality_variables"] == 0 and q["no_loss_used"] is True,
           "quality representation and TYPE E")
    checks["quality"] = {"physical_rows": q["physical_rows"], "unique_ids": q["unique_ids"],
                         "roles": q["role_counts"], "semantic_conflicts": 0, "TYPE_E": 0}

    cv = records(R4 / "P_RESPONSE_TRAIN_CV_RESULTS_v1.csv")
    demand({r["model"] for r in cv} == {"M0", "M1", "M2"}, "CV model set")
    for row in cv:
        near(float(row["cv_balanced_score"]), t["cv_candidates"][row["model"]]["score"],
             f"{row['model']} CV score")
    domains = [x.removeprefix("metric/the_pile_").removesuffix("_val_loss") for x in b["loss_columns"]]
    pred = records(R4 / "P_RESPONSE_VALIDATION_PREDICTIONS_v2.csv")
    dom = records(R4 / "P_RESPONSE_DOMAIN_VALIDATION_v2.csv")
    support = records(R4 / "P_SUPPORT_VALIDATION_ROWS_v2.csv")
    demand(len(domains) == 13 and len(pred) == len(support) == 576 and len(dom) == 117,
           "prediction/support/domain row count")
    demand(all((a["scale"], a["index"], a["support_class"]) ==
               (z["scale"], z["index"], z["support_class"]) for a, z in zip(pred, support)),
           "prediction/support row mapping")
    recomputed = {}
    for scale, expected_n, hull_n in [("1M", 256, 2), ("60M", 256, 2), ("1B", 64, 17)]:
        rows = [r for r in pred if r["scale"] == scale]
        demand(len(rows) == expected_n and len({r["index"] for r in rows}) == expected_n,
               f"{scale} validation grain")
        observed = [[float(r[f"observed_{d}"]) for d in domains] for r in rows]
        r0 = [mean(x) for x in observed]
        demand(all(math.isclose(a, float(r["R0_observed"]), abs_tol=1e-10)
                   for a, r in zip(r0, rows)), f"{scale} observed R0 formula")
        centered_base = rmse(x - mean(r0) for x in r0)
        recomputed[scale] = {}
        for model in ("M0", "M1", "M2"):
            predicted = [[float(r[f"{model}_pred_{d}"]) for d in domains] for r in rows]
            pr0 = [mean(x) for x in predicted]
            demand(all(math.isclose(a, float(r[f"{model}_R0_pred"]), abs_tol=1e-10)
                       for a, r in zip(pr0, rows)), f"{scale} {model} predicted R0 formula")
            score = rmse(a - z for a, z in zip(r0, pr0))
            near(score, v["metrics"][scale][model]["R0_RMSE_raw"], f"{scale} {model} R0 RMSE")
            c_ratio = rmse((a - mean(r0)) - (z - mean(pr0)) for a, z in zip(r0, pr0)) / centered_base
            near(c_ratio, v["metrics"][scale][model]["R0_centered_RMSE_ratio_to_M0"],
                 f"{scale} {model} centered ratio")
            for j, domain in enumerate(domains):
                dscore = rmse(observed[i][j] - predicted[i][j] for i in range(len(rows)))
                match = [r for r in dom if (r["scale"], r["model"], r["domain"]) ==
                         (scale, model, domain)]
                demand(len(match) == 1, f"{scale} {model} {domain} domain row")
                if len(match) == 1:
                    near(dscore, float(match[0]["RMSE_raw"]), f"{scale} {model} {domain} RMSE")
            recomputed[scale][model] = score
        demand(dict(Counter(r["support_class"] for r in rows)) == v["support_counts"][scale],
               f"{scale} support counts")
        demand(sum(r["in_observed_convex_hull"].lower() == "true" for r in rows) == hull_n,
               f"{scale} convex hull count")
        q95 = v["support_thresholds"]["train_loo_NN_q95"]
        q99 = v["support_thresholds"]["train_loo_NN_q99"]
        for row in rows:
            inside = row["in_observed_convex_hull"].lower() == "true"
            distance = float(row["nearest_train_helmert_distance"])
            expected_class = ("IN_SUPPORT" if inside and distance <= q95 else
                              "NEAR_SUPPORT" if inside or distance <= q99 else "OUT_OF_SUPPORT")
            demand(row["support_class"] == expected_class,
                   f"{scale} support classification index {row['index']}")
    d1 = [r for r in dom if (r["scale"], r["model"]) == ("1M", "M1")]
    demand(len(d1) == 13 and all(float(r["RMSE_ratio_to_M0_raw"]) < 1 for r in d1),
           "A7 13/13 domain improvement")
    cmp = v["model_comparisons_1M"]
    one_m = [r for r in pred if r["scale"] == "1M"]
    std = b["response_sd_ddof1"]
    for model, control in [("M1", "M0"), ("M2", "M1")]:
        r0_delta = []
        domain_delta = []
        for row in one_m:
            y = [float(row[f"observed_{d}"]) for d in domains]
            a = [float(row[f"{model}_pred_{d}"]) for d in domains]
            c = [float(row[f"{control}_pred_{d}"]) for d in domains]
            r0_delta.append((mean(y) - mean(a)) ** 2 - (mean(y) - mean(c)) ** 2)
            domain_delta.append(mean(((y[j] - a[j]) / std[j]) ** 2 -
                                     ((y[j] - c[j]) / std[j]) ** 2 for j in range(13)))
        near(mean(r0_delta), cmp[model]["R0_MSE_model_minus_control"], f"{model} R0 paired MSE delta")
        near(mean(domain_delta), cmp[model]["domain_std_MSE_model_minus_control"],
             f"{model} domain paired standardized MSE delta")
    demand(cmp["M1"]["adopted"] is True and cmp["M1"]["stable_two_layer_gain"] is True
           and cmp["M1"]["R0_boot_p975"] < 0 and cmp["M1"]["domain_boot_p975"] < 0,
           "M1 validation selection")
    demand(cmp["M2"]["adopted"] is False and cmp["M2"]["stable_two_layer_gain"] is False
           and cmp["M2"]["R0_boot_p025"] < 0 < cmp["M2"]["R0_boot_p975"]
           and cmp["M2"]["domain_boot_p025"] < 0 < cmp["M2"]["domain_boot_p975"],
           "M2 no stable holdout gain")
    demand(v["preferred_candidate_provisional"] == "M1" and v["cross_scale_absolute_claim_allowed"] is False
           and v["metrics"]["60M"]["M1"]["R0_centered_RMSE_ratio_to_M0"] < 1
           and v["metrics"]["1B"]["M1"]["R0_centered_RMSE_ratio_to_M0"] > 1,
           "scale-transfer scope")
    checks["model_results"] = {"CV": {r["model"]: float(r["cv_balanced_score"]) for r in cv},
                               "R0_RMSE_recomputed": recomputed, "A7_improved_domains": len(d1),
                               "support": v["support_counts"],
                               "60M_centered_ratio": v["metrics"]["60M"]["M1"]["R0_centered_RMSE_ratio_to_M0"],
                               "1B_centered_ratio": v["metrics"]["1B"]["M1"]["R0_centered_RMSE_ratio_to_M0"]}

    failed = R4 / "failed_validation_v1"
    demand((R4 / "P_RESPONSE_VALIDATION_RUN_v1_FAILED.md").is_file()
           and len(list(failed.glob("*.csv"))) == 5
           and not (R4 / "P_RESPONSE_VALIDATION_METRICS_v1.json").exists(),
           "failed v1 artifact isolation")
    experiment_registry = (ROOT / "05_experiments/EXPERIMENT_REGISTRY.md").read_text(encoding="utf-8")
    demand("VAL-Q1-PRESP-A6A11-R4-20260924-v1" in experiment_registry
           and "FAILED — NO VALIDATION DECISION" in experiment_registry
           and v["run_id"] in experiment_registry, "experiment registry run states")

    figures = data(R4 / "figures/figure_manifest.json")
    tables = data(R4 / "tables/table_manifest.json")
    demand(digest(ROOT / "04_code/modeling_phase1/round4_q1_figures.py") == figures["script_sha256"],
           "figure script hash")
    demand(digest(ROOT / "04_code/modeling_phase1/round4_q1_tables.py") == tables["script_sha256"],
           "table script hash")
    for fig in figures["figures"]:
        for key, hk in [("source", "source_sha256"), ("path", "pdf_sha256"), ("preview", "png_sha256")]:
            demand(digest(ROOT / fig[key]) == fig[hk], f"{fig['figure_id']} {key} hash")
        with (ROOT / fig["preview"]).open("rb") as f:
            header = f.read(24)
        demand(header[:8] == b"\x89PNG\r\n\x1a\n" and min(struct.unpack(">II", header[16:24])) >= 1200,
               f"{fig['figure_id']} PNG dimensions")
    for table in tables["tables"]:
        demand(digest(ROOT / table["path"]) == table["sha256"]
               and digest(ROOT / table["source"]) == table["source_sha256"],
               f"{table['path']} table/source hash")
    checks["figures_tables"] = {"figures": len(figures["figures"]), "tables": len(tables["tables"]),
                                "visual_review": "four PNG previews inspected; no obvious clipping"}

    result_registry = (ROOT / "06_results/RESULTS_REGISTRY.md").read_text(encoding="utf-8")
    figure_registry = (ROOT / "06_results/FIGURE_REGISTRY.md").read_text(encoding="utf-8")
    demand("VALIDATED FINAL RESULTS：NONE" in result_registry, "final-result status")
    demand(result_registry.count("| CAND-") == 14, "result registry candidate count")
    demand(figure_registry.count("| FIG-Q1-R4-") == 4, "figure registry candidate count")
    for fig in figures["figures"]:
        demand(fig["figure_id"] in figure_registry, f"figure registry {fig['figure_id']}")
    linked_docs = [ROOT / name for name in [
        "README.md", "03_models/modeling_phase1/MODELING_PHASE1_STATE.md",
        "07_validation/VALIDATION_REPORT.md",
        "09_handoff/R4_TAKEOVER_RECOVERY_CHECK_v1.md",
        "09_handoff/PROJECT_STATE.md", "09_handoff/NEXT_ACTION.md", "09_handoff/JOINT_CONTEXT.md",
        "09_handoff/STAGE_GATES.md",
        "10_review/MODELING_PHASE1_R4_QA_20260924.md",
        "10_review/GATE2_PRE_REVIEW_PACKAGE_v1_1.md",
        "01_data/audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_FINAL_R4_v1.md",
        "03_models/modeling_phase1/gate2/GATE2_READINESS_CHECKLIST.md",
    ]]
    checked_links = 0
    for doc in linked_docs:
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "#")):
                continue
            checked_links += 1
            demand((doc.parent / target.split("#", 1)[0]).exists(),
                   f"broken local link {doc.relative_to(ROOT)} -> {target}")
    checks["registries"] = {"final_results": 0, "result_candidates": 14,
                             "figure_ids": [f["figure_id"] for f in figures["figures"]],
                             "local_links_checked": checked_links}

    outcome = {"qa_id": "QA-MODELING-PHASE1-R4-20260924-v1",
               "status": "PASS" if not errors else "FAIL", "failures": errors, "checks": checks,
               "model_training_rerun": False, "holdout_validation_rerun": False,
               "qa_script_sha256": digest(Path(__file__))}
    REVIEW.mkdir(parents=True, exist_ok=True)
    (REVIEW / "MODELING_PHASE1_R4_QA_20260924.json").write_text(
        json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return outcome


if __name__ == "__main__":
    result = audit()
    print(json.dumps({"status": result["status"], "failures": result["failures"]}, ensure_ascii=False))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
