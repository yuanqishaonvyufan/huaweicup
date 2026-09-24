"""Route a completed Q/p audit summary to a conservative Q2/Q3 action.

This tool does not read raw competition data or compute rank, uncertainty, or
held-out metrics. Those diagnostics must be generated and preregistered by the
later data-audit stage under 01_data/IDENTIFIABILITY_AUDIT_SPEC.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED = {
    "audit_id",
    "score_provenance_valid",
    "score_uses_target_loss",
    "nested_crossfit_valid",
    "paired_quality_available",
    "deterministic_from_p_fixed_q",
    "rank_state",
    "precision_state",
    "support_state",
    "oos_gain_state",
    "quality_evidence_source",
}

RANK_STATES = {"NOT_TESTED", "X0_DEFICIENT", "FULL_DEFICIENT", "FULL_RANK"}
PRECISION_STATES = {"NOT_CALIBRATED", "WEAK", "STABLE"}
SUPPORT_STATES = {"NOT_CALIBRATED", "INSUFFICIENT", "ADEQUATE"}
OOS_STATES = {"NOT_TESTED", "NO_STABLE_GAIN", "STABLE_GAIN"}
EVIDENCE_SOURCES = {"REAL_DIRECT", "SEMI_SYNTHETIC", "MIXED"}


def _check_summary(summary: dict[str, Any]) -> None:
    missing = sorted(REQUIRED - summary.keys())
    if missing:
        raise ValueError(f"Missing audit summary fields: {', '.join(missing)}")
    for key in (
        "score_provenance_valid",
        "score_uses_target_loss",
        "nested_crossfit_valid",
        "paired_quality_available",
        "deterministic_from_p_fixed_q",
    ):
        if not isinstance(summary[key], bool):
            raise ValueError(f"{key} must be a boolean, not an implicit pass")
    for key, allowed in (
        ("rank_state", RANK_STATES),
        ("precision_state", PRECISION_STATES),
        ("support_state", SUPPORT_STATES),
        ("oos_gain_state", OOS_STATES),
        ("quality_evidence_source", EVIDENCE_SOURCES),
    ):
        if summary[key] not in allowed:
            raise ValueError(f"{key} must be one of {sorted(allowed)}")
    if not isinstance(summary["audit_id"], str) or not summary["audit_id"].strip():
        raise ValueError("audit_id must identify a saved, source-backed audit")
    def require_ref(key: str) -> None:
        if not isinstance(summary.get(key), str) or not summary[key].strip():
            raise ValueError(f"{key} must identify saved evidence before this branch can pass")

    if not summary["score_provenance_valid"]:
        return
    require_ref("score_provenance_id")
    if summary["score_uses_target_loss"] and not summary["nested_crossfit_valid"]:
        return
    if not summary["paired_quality_available"]:
        return
    require_ref("pairing_evidence_id")
    if summary["deterministic_from_p_fixed_q"] or summary["rank_state"] == "NOT_TESTED":
        return
    require_ref("rank_evidence_id")
    if summary["rank_state"] in {"X0_DEFICIENT", "FULL_DEFICIENT"}:
        return
    if summary["quality_evidence_source"] == "MIXED":
        return
    if summary["precision_state"] != "NOT_CALIBRATED":
        require_ref("precision_rule_id")
    if summary["support_state"] != "NOT_CALIBRATED":
        require_ref("support_rule_id")
    if summary["precision_state"] == "WEAK" or summary["support_state"] == "INSUFFICIENT":
        return
    if summary["oos_gain_state"] != "NOT_TESTED":
        require_ref("oos_split_id")
        require_ref("oos_metrics_id")


def route(summary: dict[str, Any]) -> dict[str, Any]:
    """Return one primary branch plus source overlays and permitted claims."""
    _check_summary(summary)
    flags: list[str] = []
    if summary["score_uses_target_loss"] and summary["nested_crossfit_valid"]:
        flags.append("SUPERVISED_SCORE_CROSS_FIT: predictive use only")
    if summary["quality_evidence_source"] == "MIXED":
        flags.append("MIXED_SOURCE: stratify real and semi-synthetic results")

    def result(
        branch: str,
        q2: str,
        q3: str,
        allowed: str,
        forbidden: str,
        fallback: str,
    ) -> dict[str, Any]:
        return {
            "audit_id": summary["audit_id"],
            "primary_branch": branch,
            "evidence_classification": summary["quality_evidence_source"],
            "evidence_refs": {
                key: summary.get(key, "")
                for key in (
                    "score_provenance_id",
                    "pairing_evidence_id",
                    "rank_evidence_id",
                    "precision_rule_id",
                    "support_rule_id",
                    "oos_split_id",
                    "oos_metrics_id",
                )
            },
            "risk_flags": flags,
            "Q2_ACTION": q2,
            "Q3_ACTION": q3,
            "allowed_claim": allowed,
            "forbidden_claim": forbidden,
            "fallback_branch": fallback,
            "mathematical_model_confirmed": False,
        }

    if not summary["score_provenance_valid"]:
        return result(
            "HOLD_SCORE_PROVENANCE",
            "Recover quality-score construction and source lineage before adding Q.",
            "Do not optimize independent Q investment.",
            "Quality-score provenance is unresolved.",
            "Q has an independently validated effect on Loss.",
            "Rebuild or trace the score, then rerun the audit.",
        )
    if summary["score_uses_target_loss"] and not summary["nested_crossfit_valid"]:
        return result(
            "LEAKED_SCORE",
            "Rebuild unsupervised Q or use strict nested cross-fitting and independent evaluation.",
            "Do not optimize independent Q investment.",
            "The present score is target-supervised without valid separation.",
            "Quality causally or independently predicts the same Loss used to construct it.",
            "Use an independent score or rerun with valid cross-fitting.",
        )
    if not summary["paired_quality_available"]:
        return result(
            "NO_MATCHED_Q",
            "Fit only source-supported p response; keep separate Q effect OPEN.",
            "Treat Q as an explicit scenario, not an empirically estimated decision response.",
            "Quality indicators and mixture Loss exist at different observational grains.",
            "A1 text-level Q variation identifies a mixture-run quality coefficient.",
            "Joint p/q description or conditional Q scenario.",
        )
    if summary["deterministic_from_p_fixed_q"]:
        return result(
            "STRUCTURAL_ALIAS",
            "Do not fit an interpretable separate Q coefficient with free p effects.",
            "Only use joint p/q representation or externally supported Q scenarios.",
            "Fixed-domain q and p determine the constructed quality variable.",
            "p⊙q or regularization identifies an independent quality effect.",
            "Joint p/q response, semi-synthetic scenario, or omit independent elasticity.",
        )
    if summary["rank_state"] == "NOT_TESTED":
        return result(
            "PENDING_RANK_AUDIT",
            "Compute legal-design X0 and Xfull ranks before Q specification.",
            "Keep Q investment as a scenario.",
            "Matched Q exists, but rank has not been tested.",
            "Q is statistically identified.",
            "Run the preregistered rank procedure.",
        )
    if summary["rank_state"] in {"X0_DEFICIENT", "FULL_DEFICIENT"}:
        return result(
            "SPEC_RANK_DEFICIENT",
            "Revise p basis, duplicate controls, or model dimension; rerun the audit.",
            "Do not optimize with unstable separate Q coefficients.",
            "The current design matrix does not identify the proposed coefficient set.",
            "Regularization alone makes the coefficients uniquely interpretable.",
            "Reduced specification or joint response after rank repair.",
        )
    if summary["quality_evidence_source"] == "MIXED":
        return result(
            "PENDING_STRATIFIED_EVIDENCE",
            "Separate real and semi-synthetic diagnostics and held-out results.",
            "Keep Q investment conditional until real evidence is separately evaluated.",
            "Quality evidence comes from mixed sources requiring distinct labels.",
            "The pooled quality coefficient is directly observed in real training runs.",
            "Source-specific model or semi-synthetic scenario.",
        )
    if summary["precision_state"] == "NOT_CALIBRATED" or summary["support_state"] == "NOT_CALIBRATED":
        return result(
            "PENDING_CALIBRATION",
            "Freeze noise-relative precision and common-support rules before inspecting held-out gain.",
            "Use Q only as a scenario.",
            "Rank is full, but the precision/support decision rule is not yet fixed.",
            "Full rank alone establishes a stable independent quality contribution.",
            "Preregister diagnostics and rerun.",
        )
    if summary["precision_state"] == "WEAK":
        return result(
            "WEAK_IDENTIFICATION",
            "Simplify or report broad intervals and source sensitivity; do not use one gamma point estimate.",
            "Use interval/scenario optimization only.",
            "A separate coefficient is algebraically possible but unstable.",
            "A precise quality elasticity is established.",
            "Reduced or joint model; conditional Q scenario.",
        )
    if summary["support_state"] == "INSUFFICIENT":
        return result(
            "INSUFFICIENT_SUPPORT",
            "Restrict the claim to observed common support or seek independent real runs.",
            "Do not extrapolate an independent Q optimum beyond support.",
            "The coefficient may be algebraically identifiable locally.",
            "The coefficient generalizes across unseen quality and mixture ranges.",
            "Local model with explicit uncertainty.",
        )
    if summary["oos_gain_state"] == "NOT_TESTED":
        return result(
            "PENDING_HELDOUT_COMPARISON",
            "Compare P, Q, P+Q and joint alternatives on the same grouped holdout.",
            "Keep Q effects conditional.",
            "Rank and support checks passed, but predictive distinction is untested.",
            "Q adds reproducible predictive information.",
            "Run preregistered held-out comparison.",
        )
    if summary["oos_gain_state"] == "NO_STABLE_GAIN":
        return result(
            "NO_INCREMENTAL_PREDICTION",
            "Omit separate Q predictor from the empirical main specification.",
            "Use joint effects or quality scenarios, not a deterministic Q optimum.",
            "Adding Q did not show stable held-out gain over p alone.",
            "Quality independently improves real Loss.",
            "Joint p/q description or conditional Q scenario.",
        )
    if summary["quality_evidence_source"] == "SEMI_SYNTHETIC":
        flags.append("SEMI_SYNTHETIC_IDENTIFICATION_SUPPORT")
        return result(
            "SEMI_SYNTHETIC_ONLY",
            "Estimate Q sensitivity only within the declared semi-synthetic generator.",
            "Run scenario/interval optimization and keep source label visible.",
            "Q adds held-out information in a semi-synthetic design.",
            "Real training runs establish a quality elasticity.",
            "Separate real-data p response plus semi-synthetic Q scenario.",
        )
    return result(
        "PREDICTIVE_Q_ASSOCIATION",
        "Q may enter a restricted candidate model with intervals, pending external validation.",
        "Propagate coefficient uncertainty; do not declare an optimal quality level yet.",
        "Matched real-run Q adds stable held-out predictive information under the audited design.",
        "A causal quality intervention effect or final model has been proved.",
        "If external validation fails, return to joint/conditional response.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Saved audit summary JSON")
    parser.add_argument("--output", type=Path, required=True, help="Decision JSON")
    args = parser.parse_args()
    summary = json.loads(args.input.read_text(encoding="utf-8"))
    decision = route(summary)
    decision["input_audit_summary_sha256"] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(decision, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
