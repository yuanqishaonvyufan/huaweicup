"""Cross-check Round 2 evidence outputs against frozen inputs and boundaries."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "01_data/audits/modeling_phase1"
Q1 = AUDIT / "q1"
Q2 = AUDIT / "q2"
CODE = ROOT / "04_code/data_audit"
RAW = ROOT / "01_data/raw/real_attachments"
OUT = ROOT / "10_review/MODELING_PHASE1_R2_QA_20260924.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    doc = json.loads((AUDIT / "DOCUMENT_INTERFERENCE_AUDIT_v1.json").read_text(encoding="utf-8"))
    q1 = json.loads((Q1 / "Q1_ROUND2_DIAGNOSTICS_v1.json").read_text(encoding="utf-8"))
    b1 = json.loads((Q2 / "B1_PROVENANCE_TRACE_v1.json").read_text(encoding="utf-8"))
    check(doc["script_sha256"] == sha256(CODE / "modeling_phase1_round2_document_screen.py"), "PDF screen script hash")
    check(q1["script_sha256"] == sha256(CODE / "modeling_phase1_round2_q1.py"), "Q1 script hash")
    check(b1["script_sha256"] == sha256(CODE / "modeling_phase1_round2_b1_trace.py"), "B1 script hash")
    check(doc["excluded_span_count"] == 96, "PDF extra span total")
    check([p["excluded_span_count"] for p in doc["pages"]] == [0] + [8] * 12,
          "PDF extra span page distribution")
    check(all(x["color_rgb"] == "#fcfcfc" for p in doc["pages"] for x in p["excluded_spans"]),
          "PDF extra span color")
    check(sha256(ROOT / doc["source_path"]) == doc["source_sha256"], "PDF input hash")

    for source, record in q1["input_sha256"].items():
        with (ROOT / "03_models/modeling_phase1/q1/A1_A3_OFFICIAL_MAPPING_v1.csv").open(
                encoding="utf-8-sig", newline="") as stream:
            mapping = {r["official_id"]: r for r in csv.DictReader(stream)}
        check(sha256(RAW / mapping[source]["actual_relative_path"]) == record, f"{source} input hash")
    check(q1["counts"]["physical_rows"] == 272505 and q1["counts"]["unique_ids"] == 261086,
          "Q1 source count / ID overlap")
    semantic = pd.read_csv(Q1 / "QUALITY_SIGNAL_SEMANTICS_v1.csv")
    check(len(semantic) == 22 and semantic.signal_id.is_unique, "22 semantic rows")
    check(set(semantic.DOWNSTREAM_ELIGIBILITY) <= {
        "DESCRIPTIVE_ONLY", "POTENTIALLY_MODEL_ELIGIBLE", "NOT_ELIGIBLE", "UNKNOWN"},
        "eligibility enum")
    check((semantic.DOWNSTREAM_ELIGIBILITY == "POTENTIALLY_MODEL_ELIGIBLE").sum() == 0,
          "no current Q2 model-eligible signal")
    check((semantic.direction_status == "POSITIVE_CANDIDATE").sum() == 5,
          "five positive candidates")
    check(len(pd.read_csv(Q1 / "Q1_DSIR_LENGTH_DIAGNOSTICS_v1.csv")) == q1["output_rows"]["dsir"],
          "DSIR output count")
    ngram = pd.read_csv(Q1 / "Q1_NGRAM_SOURCE_FORMULA_CHECK_v1.csv")
    check(len(ngram) == 4 and ngram.id.nunique() == 2 and ngram.absolute_difference.max() < 1e-9,
          "A1 ngram source-formula match")
    check(len(pd.read_csv(Q1 / "Q1_NGRAM_BOUNDARY_DIAGNOSTICS_v1.csv")) == q1["output_rows"]["ngram"],
          "ngram output count")
    conflict = pd.read_csv(Q1 / "QUALITY_CONFLICT_CANDIDATES_v1.csv")
    stability = pd.read_csv(Q1 / "Q1_CONFLICT_STABILITY_v1.csv")
    old = pd.read_csv(Q1 / "QUALITY_CONFLICT_INPUT_v1.csv")
    check(len(conflict) == 42 and conflict.candidate_id.is_unique and
          set(conflict.candidate_id) == set(old.candidate_id), "42 conflict IDs preserved")
    check(set(conflict.conflict_class) <= {
        "SEMANTIC CONFLICT", "STATISTICAL DISAGREEMENT", "REDUNDANCY",
        "SCALE ARTIFACT", "DOMAIN-SPECIFIC REVERSAL", "UNRESOLVED"},
        "conflict taxonomy")
    check((conflict.conflict_class == "SEMANTIC CONFLICT").sum() == 0,
          "no unproven semantic conflict")
    check(len(stability) == q1["output_rows"]["conflict_stability"] and
          set(stability.q) == {0.75, 0.8, 0.9}, "conflict sensitivity output")
    check(int(stability[stability.scope == "UNIQUE_ALL"].n_unique_in_scope.iloc[0]) == 261086,
          "pooled unique ID grain")
    a1_main = stability[(stability.candidate_id == "QCI-025") &
                        (stability.scope == "A1_all") & (stability.q == 0.8)].iloc[0]
    check(abs(a1_main.extreme_discordance_rate - 0.08811243412063244) < 1e-12,
          "QCI-025 A1 main statistic")

    check(sha256(RAW / "B_scaling_laws/pythia_training_log_existing.csv") == b1["b1_sha256"],
          "B1 raw hash")
    check(sha256(RAW / "B_scaling_laws/pythia_checkpoint_index.csv") == b1["index_sha256"],
          "checkpoint index hash")
    matrix = pd.read_csv(Q2 / "B1_PROVENANCE_MATRIX_v1.csv")
    fields = pd.read_csv(Q2 / "B1_FIELD_LINEAGE_v1.csv")
    sample = pd.read_csv(Q2 / "B1_CHECKPOINT_SAMPLE_VERIFICATION_v1.csv")
    check(len(matrix) == 8 and (matrix.B1_rows == 147).all(), "B1 eight trajectories")
    check(int(matrix.B1_precision_transitions.sum()) == 503 and
          int(matrix.B1_precision_mismatch_if_training.sum()) == 748,
          "B1 precision conflict")
    check(len(fields) == 15 and fields.field.is_unique, "B1 field lineage")
    check(len(sample) == 3 and sample.match.all(), "public commit sample")
    check(b1["alert_status"] == "PARTIALLY RESOLVED" and
          b1["eligibility"] == "NOT YET ELIGIBLE", "B1 eligibility gate")
    check("PARTIALLY RESOLVED" in (Q2 / "EVIDENCE_ALERT_B1_SOURCE_METADATA_v2.md").read_text(encoding="utf-8"),
          "B1 Alert document")
    check("GENERATOR UNKNOWN" in (AUDIT / "parallel/B8_GENERATOR_TRACE_v1.md").read_text(encoding="utf-8"),
          "B8 quarantine trace")
    check("VALIDATED FINAL RESULTS：NONE" in
          (ROOT / "06_results/RESULTS_REGISTRY.md").read_text(encoding="utf-8"),
          "no validated final results")
    check("正式模型运行 0" in
          (ROOT / "05_experiments/EXPERIMENT_REGISTRY.md").read_text(encoding="utf-8"),
          "zero formal model runs")
    state = (ROOT / "09_handoff/PROJECT_STATE.md").read_text(encoding="utf-8")
    next_action = (ROOT / "09_handoff/NEXT_ACTION.md").read_text(encoding="utf-8")
    check("ROUND 2 CHECKED" in state and "PARTIALLY RESOLVED" in state,
          "active state reflects Round 2 and B1 containment")
    check("RESOLVED FOR BASELINE USE" in next_action and "QUARANTINED" in next_action,
          "next action preserves B1/B8 gates")
    active_source_claims = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in [
        "00_problem/OFFICIAL_REQUIREMENTS.md",
        "02_analysis/consensus/GATE1_CONSENSUS_v1.md",
        "09_handoff/PROJECT_STATE.md",
        "09_handoff/JOINT_CONTEXT.md",
        "09_handoff/NEXT_ACTION.md",
    ])
    check(not any(term in active_source_claims for term in ["E=3.52", "冲突率约为0%", "0.3为界"]),
          "known hidden-page claims did not leak into active source documents")

    result = {
        "qa_id": "QA-MP1-R2-20260924-v1",
        "status": "PASS",
        "source_pdf_extra_spans_excluded": 96,
        "q1_semantic_rows": len(semantic),
        "q1_conflict_rows": len(conflict),
        "q1_semantic_conflicts_confirmed": 0,
        "b1_trajectories": len(matrix),
        "b1_alert": b1["alert_status"],
        "b1_eligibility": b1["eligibility"],
        "formal_model_runs": 0,
        "validated_final_results": 0,
        "qa_script_sha256": sha256(Path(__file__)),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
