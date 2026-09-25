"""Classify every registered F-question result against the supplied v3 paper.

Status is intentionally conservative: Q1-Q3 remain checked/provisional and
Q4 remains validated only for restricted reporting, per PROJECT_STATE.md.
"""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "06_results/RESULTS_REGISTRY.md"
OUT = ROOT / "10_review/LOCAL_EVIDENCE_MASTER_INVENTORY_v2.csv"
Q1 = "03_models/modeling_phase1/q1"
Q2 = "06_results/raw/EXP-Q2-ND-R5-20260924-v1"
Q2S = "06_results/raw/SCEN-Q2-R5-20260924-v3"
Q3 = "06_results/raw/EXP-Q3-BASE-R6-20260924-v1"
Q3S = "06_results/raw/SCEN-Q3-R6-20260924-v1"
Q3U = "06_results/raw/UNC-Q3-R6-20260924-v1"
Q4 = "06_results/raw/EXP-Q4-R7-20260925-v1"
Q1R = "06_results/raw/Q1_TASK_REPAIR_20260925_v1"
Q4R = "06_results/raw/Q4_TASK_REPAIR_20260925_v1"

# category, v3 coverage, source artifact, v5 treatment, coverage reason
META = {
    "CAND-Q1-DQ-R3-001": ("DIAGNOSTIC", "ONE SENTENCE ONLY", f"{Q1}/round3/Q1_DESCRIPTIVE_QUALITY_METRICS_v1.json", "Expand PCA rejection evidence", "Only first-component variance is stated"),
    "CAND-Q1-DQ-R3-002": ("DIAGNOSTIC", "ONE SENTENCE ONLY", f"{Q1}/round3/Q1_DQ2_DOMAIN_GROUP_SUPPORT_v1.csv", "Add domain support contrast", "3/9 result lacks a compact visual"),
    "CAND-Q1-RSP-R3-001": ("APPENDIX-ONLY", "NOT IN PAPER", f"{Q1}/round3/Q1_13_DOMAIN_RESPONSE_CANDIDATE_SUMMARY_v1.csv", "Keep appendix diagnostic only", "Exploratory R2 component is not main 13-domain response"),
    "CAND-Q1-RSP-R3-002": ("DIAGNOSTIC", "NOT IN PAPER", f"{Q1}/round3/Q1_13_DOMAIN_RESPONSE_CANDIDATE_SUMMARY_v1.csv", "Summarize response aggregation disagreement", "R0/R2 rank relation absent"),
    "CAND-Q1-RSP-R3-003": ("DIAGNOSTIC", "NOT IN PAPER", f"{Q1}/round3/Q1_13_DOMAIN_RESPONSE_CANDIDATE_SUMMARY_v1.csv", "Add domain heterogeneity matrix if verified", "Negative domain-pair diagnostics absent"),
    "CAND-Q1-R4-QUAL-001": ("CORE", "IN PAPER PARTIALLY", f"{Q1}/round4/Q1_QUALITY_CLOSURE_METRICS_v1.json", "Expand 22-signal roles and missingness", "v3 adds an unregistered scalar; frozen main evidence is multidimensional"),
    "CAND-Q1-R4-VAL-001": ("VALIDATION", "IN PAPER FULLY", f"{Q1}/round4/P_RESPONSE_VALIDATION_METRICS_v2.json", "Retain verified comparison", "M0/M1 RMSE and uncertainty already shown"),
    "CAND-Q1-R4-VAL-002": ("VALIDATION", "IN PAPER FULLY", f"{Q1}/round4/P_RESPONSE_DOMAIN_VALIDATION_v2.csv", "Retain 13-domain table and figure", "All 13 domains and RMSE summarized"),
    "CAND-Q1-R4-TRANSFER-001": ("NEGATIVE RESULT", "IN PAPER PARTIALLY", f"{Q1}/round4/P_RESPONSE_VALIDATION_METRICS_v2.json", "Add scale-transfer failure figure", "Ratios stated without dedicated transfer visual"),
    "CAND-Q1-R4-SUPPORT-001": ("DIAGNOSTIC", "IN PAPER PARTIALLY", f"{Q1}/round4/P_RESPONSE_VALIDATION_METRICS_v2.json", "Add support geometry figure", "Support counts appear but geometry is not visualized"),
    "CAND-Q1-R4-CV-001": ("SUPPORTING", "ONE SENTENCE ONLY", f"{Q1}/round4/P_RESPONSE_TRAIN_METRICS_v1.json", "Put M0/M1 choice into candidate table", "Training five-fold score is one sentence"),
    "CAND-Q1-R4-CV-002": ("SUPPORTING", "ONE SENTENCE ONLY", f"{Q1}/round4/P_RESPONSE_TRAIN_METRICS_v1.json", "Show M2 tradeoff in candidate table", "Ridge difference not explained in a table"),
    "CAND-Q1-R4-SELECT-001": ("SUPPORTING", "ONE SENTENCE ONLY", f"{Q1}/round4/P_RESPONSE_TRAIN_METRICS_v1.json", "State why M3 was not fitted", "Nonlinear trigger appears without rationale"),
    "CAND-Q1-R4-SELECT-002": ("VALIDATION", "IN PAPER PARTIALLY", f"{Q1}/round4/P_RESPONSE_VALIDATION_METRICS_v2.json", "Add M2/M1 interval to model comparison", "Selection-stop evidence is abbreviated"),
    "CAND-Q2-R5-ND-001": ("CORE", "IN PAPER FULLY", f"{Q2}/summary.json", "Keep estimated five-parameter law", "Parameter table and model form are present"),
    "CAND-Q2-R5-VAL-001": ("VALIDATION", "IN PAPER FULLY", f"{Q2}/validation_metrics.csv", "Keep three holdout designs", "Three validation metrics and figure are present"),
    "CAND-Q2-R5-UNC-001": ("SENSITIVITY", "IN PAPER PARTIALLY", f"{Q2}/cluster_bootstrap.csv", "Add bootstrap distribution or compact uncertainty plot", "Interval table lacks joint-distribution view"),
    "CAND-Q2-R5-MARG-001": ("CORE", "IN PAPER FULLY", f"{Q2}/marginal_effects.csv", "Retain derivative and elasticity path", "Formulae and heatmap are present"),
    "CAND-Q2-R5-QUAL-001": ("SCENARIO", "IN PAPER PARTIALLY", f"{Q2S}/quality_cell_slopes.csv", "Add separate semi-synthetic response panel", "Quality evidence and source boundary condensed"),
    "SCEN-Q2-R5-SUB-001": ("SCENARIO", "IN PAPER PARTIALLY", f"{Q2S}/quality_substitution_scenarios.csv", "Keep conditional substitutions clearly separate", "Example is reported without full condition map"),
    "CAND-Q2-R5-EXT-001": ("DIAGNOSTIC", "IN PAPER PARTIALLY", f"{Q2S}/external_shape_diagnostics.csv", "Add source-separated diagnostic chart", "Shape ratios are text/table only"),
    "CAND-Q2-R5-EXT-002": ("APPENDIX-ONLY", "ONE SENTENCE ONLY", f"{Q2S}/B9_extrapolation_scope.csv", "Add scope table to appendix", "Estimated values cannot validate out-of-range loss"),
    "CAND-Q2-R5-MIX-001": ("SCENARIO", "ONE SENTENCE ONLY", f"{Q2S}/mixture_tangent_scenarios.csv", "Retain conditional tangent explanation", "Cross-source transport is unestimated"),
    "CAND-Q3-R6-BASE-001": ("CORE", "IN PAPER FULLY", f"{Q3}/budget_path.csv", "Retain 51-budget path; explain beyond three rows", "Representative table and continuous path are present"),
    "CAND-Q3-R6-SHIFT-001": ("CORE", "IN PAPER PARTIALLY", f"{Q3}/budget_path.csv", "Add active-constraint state path", "Transition locations are text and dotted lines"),
    "SCEN-Q3-R6-QUAL-001": ("SCENARIO", "IN PAPER FULLY", f"{Q3S}/quality_context_path.csv", "Retain cost-family comparison", "Three cost choices and conditional curves present"),
    "SCEN-Q3-R6-BREAK-001": ("SCENARIO", "IN PAPER PARTIALLY", f"{Q3S}/quality_break_even.csv", "Add local-versus-global threshold figure", "Threshold example lacks full path"),
    "SCEN-Q3-R6-MIX-001": ("SCENARIO", "ONE SENTENCE ONLY", f"{Q3S}/mixture_local_candidates.csv", "Give 13-domain tradeoff in appendix", "513-candidate search is only summarized"),
    "SCEN-Q3-R6-CTX-001": ("SENSITIVITY", "IN PAPER PARTIALLY", f"{Q3S}/context_baseline.csv", "Add five-context path and cost split", "Only endpoint example and critical length stated"),
    "SENS-Q3-R6-UNC-001": ("SENSITIVITY", "IN PAPER PARTIALLY", f"{Q3U}/conditional_quantiles.csv", "Expand 51,000 conditional configurations", "Uncertainty figure lacks detailed budget-region reading"),
    "SENS-Q3-R6-SHADOW-001": ("SENSITIVITY", "ONE SENTENCE ONLY", f"{Q3U}/shadow_prices.csv", "Add shadow-price path", "Formula is stated without path figure"),
    "Q4-R7-001": ("CORE", "IN PAPER PARTIALLY", f"{Q4}/frontier_family.csv", "Add historical and six-task frontier figure", "Historical increase is text; no dedicated task trends"),
    "Q4-R7-002": ("CORE", "IN PAPER FULLY", f"{Q4}/decomposition_changes.csv", "Retain descriptive decomposition and caveat", "Main shares and figure/table are present"),
    "Q4-R7-003": ("NEGATIVE RESULT", "IN PAPER FULLY", f"{Q4}/bridge_validation.csv", "Add failure-diagnostic figure", "Failure table is present but graphic strengthens explanation"),
    "Q4-R7-004": ("VALIDATION", "IN PAPER FULLY", f"{Q4}/rolling_metrics.csv", "Add rolling-origin figure", "Short-horizon metrics and absence of long folds are present"),
    "Q4-R7-005": ("SCENARIO", "IN PAPER FULLY", f"{Q4}/forecast_summary.json", "Retain dated conditional forecast", "Centers, intervals and fan are present"),
    "Q4-R7-006": ("SENSITIVITY", "IN PAPER PARTIALLY", f"{Q4}/robustness_variants.csv", "Add family/window robustness figure", "Reversal table is present; mechanism not visualized"),
    "Q4-R7-007": ("SENSITIVITY", "IN PAPER FULLY", f"{Q4}/forecast_all_models_scenarios.csv", "Retain model-center range separately", "Ranges are in forecast table"),
    "Q4-R7-008": ("NEGATIVE RESULT", "IN PAPER PARTIALLY", f"{Q4}/scenario_decomposition.csv", "Add collapsed-scenario diagnostic if useful", "Scenario table omits visual reason for overlap"),
    "Q1-REPAIR-001": ("CORE", "IN PAPER FULLY", f"{Q1R}/Q_FULL_DOMAIN_RESULTS_v1.csv", "Keep constructed-score method and scope", "v3 table and methods match the new independently run supplement"),
    "Q1-REPAIR-002": ("NEGATIVE RESULT", "IN PAPER FULLY", f"{Q1R}/A12_A15_EXTRAPOLATION_CHECK_v1.csv", "Clarify estimated 10B/70B failures", "v3 pressure-test table is present; estimates are not true holdout"),
    "Q4-REPAIR-001": ("DIAGNOSTIC", "IN PAPER PARTIALLY", f"{Q4R}/FULL_SCALE_SUBSET_LOO_v1.csv", "Explain six-record instability", "v3 C4 table condenses small-sample identifiability failure"),
    "Q4-REPAIR-002": ("SCENARIO", "IN PAPER FULLY", f"{Q4R}/EXOGENOUS_COMPUTE_SLOWDOWN_SCENARIOS_v1.csv", "Retain exogenous-path assumption", "v3 scenario table gives conditional centers without calibrated coverage"),
}


def main() -> None:
    ids = []
    registry_text = REGISTRY.read_text(encoding="utf-8")
    for line in registry_text.splitlines():
        match = re.match(r"^\|\s*((?:CAND|SCEN|SENS)-Q[1-4]-[^| ]+|Q4-R7-\d{3})\s*\|", line)
        if match:
            ids.append(match.group(1))
    ids.extend(sorted(set(re.findall(r"\b(?:Q1|Q4)-REPAIR-\d{3}\b", registry_text))))
    if len(ids) != 43 or set(ids) != set(META):
        raise ValueError(f"Registry set changed: {len(ids)} IDs, unmatched={set(ids)^set(META)}")
    rows = []
    for result_id in ids:
        category, coverage, source, action, reason = META[result_id]
        if not (ROOT / source).is_file():
            raise FileNotFoundError(source)
        question = re.search(r"Q([1-4])", result_id).group(1)
        if result_id == "Q1-REPAIR-001":
            status = "CHECKED_SUPPLEMENTARY_CONSTRUCTED_SCORE"
        elif result_id == "Q1-REPAIR-002":
            status = "CHECKED_ESTIMATED_EXTRAPOLATION"
        elif result_id == "Q4-REPAIR-001":
            status = "CHECKED_DIAGNOSTIC_NOT_IDENTIFIED"
        elif result_id == "Q4-REPAIR-002":
            status = "CHECKED_SCENARIO_CONDITIONAL"
        elif question == "1" and "-R3-" in result_id:
            status = "CANDIDATE_DIAGNOSTIC_NOT_FINAL"
        elif question == "4":
            status = "VALIDATED_FOR_RESTRICTED_REPORTING"
        else:
            status = "CHECKED_PROVISIONAL_LIMITED_USE"
        rows.append({
            "result_id": result_id,
            "question": "Q" + question,
            "evidence_status": status,
            "primary_category": category,
            "v3_coverage": coverage,
            "source_artifact": source,
            "v5_recovery_action": action,
            "coverage_reason": reason,
        })
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("registered", len(rows), "coverage", dict(Counter(row["v3_coverage"] for row in rows)))
    for question in ("Q1", "Q2", "Q3", "Q4"):
        selected = [row for row in rows if row["question"] == question]
        print(question, len(selected), dict(Counter(row["v3_coverage"] for row in selected)))


if __name__ == "__main__":
    main()
