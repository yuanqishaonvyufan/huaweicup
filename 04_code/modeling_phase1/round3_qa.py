"""Cross-file QA for Round 3 candidate comparisons and source containment."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "03_models/modeling_phase1/q1"
BASE = MODEL / "round3"
INPUT = ROOT / "01_data/processed/modeling_phase1/round3"
Q2 = ROOT / "01_data/audits/modeling_phase1/q2"
CODE = ROOT / "04_code/modeling_phase1"
RAW = ROOT / "01_data/raw/real_attachments"
OUT = ROOT / "10_review/MODELING_PHASE1_R3_QA_20260924.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def local_links(files: list[Path]) -> int:
    count = 0
    for source in files:
        content = source.read_text(encoding="utf-8")
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
            if link.startswith(("http:", "https:", "#")):
                continue
            count += 1
            check((source.parent / link.split("#")[0]).resolve().exists(),
                  f"Broken link in {source}: {link}")
    return count


def main() -> None:
    set_meta = json.loads((MODEL / "Q1_DESCRIPTIVE_SIGNAL_SET_v1.json").read_text(encoding="utf-8"))
    signal_set = MODEL / "Q1_DESCRIPTIVE_SIGNAL_SET_v1.csv"
    check(sha256(signal_set) == set_meta["output_sha256"], "Signal set hash")
    check(sha256(CODE / "round3_freeze_signal_set.py") == set_meta["script_sha256"], "Signal freeze script hash")
    roles = pd.read_csv(signal_set, encoding="utf-8-sig")
    check(len(roles) == 22 and roles["Signal ID"].is_unique, "22 signal set")
    check(roles["Use in descriptive representation?"].value_counts().to_dict() == {
        "SENSITIVITY_ONLY_SIGNAL": 12, "CORE_DESCRIPTIVE_SIGNAL": 5,
        "UNKNOWN": 3, "EXCLUDED_FOR_NOW": 2}, "Signal use roles")
    check(roles.DOWNSTREAM_ELIGIBILITY.value_counts().to_dict() == {
        "DESCRIPTIVE_ONLY": 17, "UNKNOWN": 5}, "Downstream eligibility preserved")

    prep = json.loads((INPUT / "INPUT_MANIFEST_v1.json").read_text(encoding="utf-8"))
    check(sha256(CODE / "round3_prepare_inputs.py") == prep["script_sha256"], "Preprocessing script hash")
    check(sha256(signal_set) == prep["signal_set_sha256"], "Preprocessing signal set hash")
    contract = MODEL / "Q1_ROUND3_COMPARISON_CONTRACT_v1.md"
    check(sha256(contract) == prep["comparison_contract_sha256"], "Frozen comparison contract")
    check(prep["heldout_A6_A11_read"] is False, "No held-out Loss input")
    with (ROOT / "03_models/modeling_phase1/q1/A1_A3_OFFICIAL_MAPPING_v1.csv").open(
            encoding="utf-8-sig", newline="") as stream:
        mapping = {row["official_id"]: row for row in csv.DictReader(stream)}
    for source in ("A1", "A2", "A3"):
        check(sha256(RAW / mapping[source]["actual_relative_path"]) == prep["raw_input_sha256"][source],
              f"{source} frozen raw hash")
    for source, relative in (("A4", "A_data_value/regmix_tables/train_mixture_1m.csv"),
                             ("A5", "A_data_value/regmix_tables/train_pile_loss_1m.csv")):
        check(sha256(RAW / relative) == prep["raw_input_sha256"][source], f"{source} raw hash")
    q_path = INPUT / "q1_quality_features_v1.csv.gz"
    l_path = INPUT / "a5_13_domain_loss_v1.csv.gz"
    check(sha256(q_path) == prep["processed"]["quality"]["sha256"], "Frozen Q1 processed hash")
    check(sha256(l_path) == prep["processed"]["response"]["sha256"], "Frozen A5 processed hash")
    check(prep["processed"]["quality"]["rows"] == 272505 and prep["processed"]["quality"]["unique_ids"] == 261086,
          "Q1 processed counts")
    check(prep["processed"]["response"]["rows"] == 512, "A5 processed count")

    dq = json.loads((BASE / "Q1_DESCRIPTIVE_QUALITY_METRICS_v1.json").read_text(encoding="utf-8"))
    check(sha256(CODE / "round3_q1_descriptive.py") == dq["script_sha256"], "DQ code hash")
    check(dq["input_sha256"] == prep["processed"]["quality"]["sha256"] and dq["no_loss_used"] is True,
          "DQ input and no-Loss gate")
    check(dq["counts"] == {"physical_records": 272505, "unique_ids": 261086,
                            "A1_train": 40926, "A1_check": 10304,
                            "A2_new": 16104, "A3_new": 193752}, "DQ split counts")
    check(abs(dq["DQ1"]["variance_share"][0] - 0.4811446000892458) < 1e-10, "DQ PC1 share")
    check(dq["DSIR"]["residual_status"] == "DIAGNOSTIC_ONLY_NOT_QUALITY", "DSIR containment")
    scores = BASE / "Q1_DESCRIPTIVE_QUALITY_RESULTS_v1.csv.gz"
    check(sha256(scores) == dq["outputs"]["scores"]["sha256"], "DQ score output hash")
    score_frame = pd.read_csv(scores, compression="gzip", usecols=["id", "source", "DQ0_global_core", "DQ3_within_domain"])
    check(len(score_frame) == 272505 and score_frame.id.nunique() == 261086, "DQ score grain")
    check(score_frame[["DQ0_global_core", "DQ3_within_domain"]].apply(lambda x: x.between(0, 1).all()).all(),
          "DQ rank score bounds")
    domain_probe = json.loads((BASE / "Q1_DOMAIN_SUPPORT_DIAGNOSTICS_v1.json").read_text(encoding="utf-8"))
    check(sha256(CODE / "round3_domain_support_check.py") == domain_probe["script_sha256"], "Domain probe code hash")
    check(domain_probe["A5_negative_pearson_pairs"] == 24 and domain_probe["A5_negative_spearman_pairs"] == 29,
          "Pearson/Spearman distinction")
    check(domain_probe["DQ2_scope_rows"] == 9 and domain_probe["DQ2_ad_singleton_scope_count"] == 3,
          "DQ2 domain transport limitation")

    rsp = json.loads((BASE / "Q1_13_DOMAIN_RESPONSE_METRICS_v1.json").read_text(encoding="utf-8"))
    check(sha256(CODE / "round3_q1_response.py") == rsp["script_sha256"], "Response code hash")
    check(rsp["input_sha256"] == prep["processed"]["response"]["sha256"] and
          rsp["heldout_A6_A11_read"] is False and rsp["p_response_fitted"] is False,
          "Response input/held-out/p-fit gates")
    prereg = MODEL / "P1_1_13_DOMAIN_RESPONSE_PREREG_FINAL_v1.md"
    check(sha256(prereg) == rsp["prereg_sha256"], "P1-1 prereg hash")
    response_csv = BASE / "Q1_13_DOMAIN_RESPONSE_RESULTS_v1.csv"
    check(sha256(response_csv) == rsp["outputs"]["response_results"]["sha256"], "Response output hash")
    response = pd.read_csv(response_csv, encoding="utf-8-sig")
    loss_columns = [x for x in response if x.startswith("metric/the_pile_")]
    check(len(response) == 512 and len(loss_columns) == 13, "R0-R3 response dimensions")
    loss = response[loss_columns].to_numpy(float)
    check(np.max(np.abs(loss.mean(axis=1) - response.R0_equal_raw_loss.to_numpy(float))) < 1e-10,
          "P1-1 R0 exact definition")
    check(np.max(np.abs(((loss - loss.mean(axis=0)) / loss.std(axis=0, ddof=1)).mean(axis=1)
                        - response.R1_equal_train_z.to_numpy(float))) < 1e-10,
          "P1-1 R1 exact definition")
    domain_rows = pd.read_csv(BASE / "DOMAIN_HETEROGENEITY_RESULTS_v1.csv")
    check(len(domain_rows) == 13 and abs(domain_rows.R0_variance_contribution.sum() - 1) < 1e-10,
          "R3 domain contribution accounting")
    loadings = domain_rows.R2_PC1_loading.to_numpy(float)
    z = (loss - loss.mean(axis=0)) / loss.std(axis=0, ddof=1)
    check(np.max(np.abs(z @ loadings - response.R2_train_z_PC1.to_numpy(float))) < 1e-10,
          "P1-1 R2 exact definition")
    check(abs(rsp["R2_variance_share"][0] - 0.22778044228057506) < 1e-10,
          "R2 PC1 share")

    b1 = json.loads((Q2 / "B1_PUBLIC_LOG_PROBE_v1.json").read_text(encoding="utf-8"))
    check(sha256(ROOT / "04_code/data_audit/modeling_phase1_round3_b1_public_log_probe.py") == b1["script_sha256"],
          "B1 source probe code hash")
    check(b1["candidate_final_step_run_rows"] == 2 and len(b1["group_checks"]) == 4,
          "B1 bounded primary-log probe")
    check(sha256(Q2 / "B1_PUBLIC_LOG_PROBE_v1.csv") == b1["output_sha256"], "B1 log comparison output hash")
    check("PARTIALLY RESOLVED" in (Q2 / "EVIDENCE_ALERT_B1_SOURCE_METADATA_v3.md").read_text(encoding="utf-8") and
          "SOURCE NOT RECOVERABLE" in (Q2 / "B1_PROVENANCE_TRACE_v2.md").read_text(encoding="utf-8"),
          "B1 Alert and stop rule status")
    check("GENERATOR UNKNOWN / QUARANTINED" in
          (ROOT / "01_data/audits/modeling_phase1/parallel/B8_ROUND3_STATUS_v1.md").read_text(encoding="utf-8"),
          "B8 quarantine")

    fig = json.loads((BASE / "figures/FIGURES_MANIFEST_v1.json").read_text(encoding="utf-8"))
    check(sha256(CODE / "round3_figures.py") == fig["script_sha256"] and len(fig["figures"]) == 4,
          "Figure code/count")
    for item in fig["figures"]:
        image = BASE / "figures" / item["file"]
        check(sha256(image) == item["sha256"], "Figure hash")
        with Image.open(image) as im:
            check(im.width >= 1000 and im.height >= 600, "Diagnostic figure size")

    docs = [
        MODEL / "Q1_DESCRIPTIVE_SIGNAL_SET_v1.md",
        MODEL / "Q1_ROUND3_COMPARISON_CONTRACT_v1.md",
        *list(BASE.glob("*v1.md")),
        BASE / "figures/FIGURES_MANIFEST_v1.md",
        Q2 / "B1_PROVENANCE_TRACE_v2.md",
        Q2 / "B1_PROVENANCE_STOP_RULE_v1.md",
        Q2 / "EVIDENCE_ALERT_B1_SOURCE_METADATA_v3.md",
        ROOT / "02_analysis/consensus/Q1_TO_Q2_INTERFACE_v1_1_DRAFT.md",
        ROOT / "09_handoff/PROJECT_STATE.md",
        ROOT / "09_handoff/NEXT_ACTION.md",
        ROOT / "09_handoff/JOINT_CONTEXT.md",
    ]
    links = local_links(docs)
    state = (ROOT / "09_handoff/PROJECT_STATE.md").read_text(encoding="utf-8")
    check("ROUND 3 CANDIDATE COMPARISONS CHECKED" in state and "VALIDATED FINAL RESULTS：**NONE**" in state,
          "Active project state gate")
    check("**当前无获准变量**" in
          (ROOT / "02_analysis/consensus/Q1_TO_Q2_INTERFACE_v1_1_DRAFT.md").read_text(encoding="utf-8"),
          "Q1-to-Q2 no-variable interface")
    result_registry = (ROOT / "06_results/RESULTS_REGISTRY.md").read_text(encoding="utf-8")
    check(result_registry.count("| CAND-") == 5 and "VALIDATED FINAL RESULTS：NONE" in result_registry,
          "Only candidate results registered")

    result = {
        "qa_id": "QA-MP1-R3-20260924-v1", "status": "PASS",
        "qa_script_sha256": sha256(Path(__file__)),
        "signal_set_rows": len(roles), "physical_quality_rows": len(score_frame),
        "unique_quality_ids": int(score_frame.id.nunique()),
        "A5_training_runs": len(response), "domain_count": len(loss_columns),
        "model_comparison_runs_nonfinal": 2, "diagnostic_runs_cumulative": 4,
        "formal_p_response_fits": 0, "formal_ND_scaling_law_fits": 0,
        "validated_final_results": 0, "B1_alert": "PARTIALLY RESOLVED",
        "B8": "GENERATOR UNKNOWN / QUARANTINED",
        "figures_verified": len(fig["figures"]), "local_links_checked": links,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
