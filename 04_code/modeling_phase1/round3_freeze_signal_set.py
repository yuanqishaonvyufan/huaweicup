"""Freeze Round 3 descriptive signal roles from checked Round 2 evidence.

This reads only checked audit tables; no raw data, Loss, or model comparison.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
Q1 = ROOT / "01_data/audits/modeling_phase1/q1"
OUT = ROOT / "03_models/modeling_phase1/q1/Q1_DESCRIPTIVE_SIGNAL_SET_v1.csv"
CORE = ["fineweb_edu", "fluency_en", "ad_en", "modernbert_cleanliness", "modernbert_readability"]
UNKNOWN = ["dsir_books", "dsir_wiki", "dsir_math"]
EXCLUDED = ["rps_doc_word_count", "rps_doc_num_sentences"]
ROLES = {
    "fineweb_edu": ("CORE_DESCRIPTIVE_SIGNAL", "list[0]", "Educational-value source meaning; no Loss supervision"),
    "fluency_en": ("CORE_DESCRIPTIVE_SIGNAL", "fluent minus not-fluent logit; argmax sensitivity", "Positive-class meaning; continuous ordering is diagnostic"),
    "ad_en": ("CORE_DESCRIPTIVE_SIGNAL", "no-ad minus has-ad logit; argmax sensitivity", "Positive class is explicitly no-ad"),
    "modernbert_cleanliness": ("CORE_DESCRIPTIVE_SIGNAL", "softmax expected level; argmax sensitivity", "Higher source rating describes less noise; logits not calibrated quality truth"),
    "modernbert_readability": ("CORE_DESCRIPTIVE_SIGNAL", "softmax expected level; argmax sensitivity", "Higher source rating describes clarity; logits not calibrated quality truth"),
    "modernbert_reasoning": ("SENSITIVITY_ONLY_SIGNAL", "argmax and softmax expected level separately", "Complexity has no universal quality direction"),
    "modernbert_professionalism": ("SENSITIVITY_ONLY_SIGNAL", "argmax and softmax expected level separately", "Required expertise has no universal quality direction"),
    "qurater": ("SENSITIVITY_ONLY_SIGNAL", "retain four source facets; do not average as main", "Four distinct facets lack justified common weight/direction"),
    "dsir_books": ("UNKNOWN", "raw score in DSIR comparison only", "Target similarity, strong length relation, exact pipeline unknown"),
    "dsir_wiki": ("UNKNOWN", "raw score in DSIR comparison only", "Target similarity, strong length relation, exact pipeline unknown"),
    "dsir_math": ("UNKNOWN", "raw score in DSIR comparison only", "Target similarity, strong length relation, exact pipeline unknown"),
    "rps_doc_word_count": ("EXCLUDED_FOR_NOW", "log1p length covariate only", "Length is not a monotone quality target and confounds DSIR"),
    "rps_doc_num_sentences": ("EXCLUDED_FOR_NOW", "log1p length covariate only", "Length-related count is not a monotone quality target"),
    "rps_doc_unigram_entropy": ("SENSITIVITY_ONLY_SIGNAL", "raw scalar / rank diagnostic", "Lexical diversity and length share inputs; no universal orientation"),
    "rps_doc_frac_unique_words": ("SENSITIVITY_ONLY_SIGNAL", "raw scalar / rank diagnostic", "Ratio is length-dependent; no universal orientation"),
    "rps_doc_frac_no_alph_words": ("SENSITIVITY_ONLY_SIGNAL", "raw scalar / rank diagnostic", "Text-form feature depends on domain"),
    "rps_doc_frac_chars_top_2gram": ("SENSITIVITY_ONLY_SIGNAL", "raw scalar / rank diagnostic; no clipping", "A1 >100 formula checked; A2/A3 pipeline not proven"),
    "rps_doc_frac_chars_top_3gram": ("SENSITIVITY_ONLY_SIGNAL", "raw scalar / rank diagnostic; no clipping", "A1 >100 formula checked; A2/A3 pipeline not proven"),
    "rps_lines_uppercase_letter_fraction": ("SENSITIVITY_ONLY_SIGNAL", "raw scalar / rank diagnostic", "Domain-dependent text-form feature"),
    "rps_lines_ending_with_terminal_punctution_mark": ("SENSITIVITY_ONLY_SIGNAL", "raw scalar / rank diagnostic", "Domain-dependent text-form feature"),
    "rps_lines_numerical_chars_fraction": ("SENSITIVITY_ONLY_SIGNAL", "raw scalar / rank diagnostic", "Domain-dependent text-form feature"),
    "rps_doc_mean_word_length": ("SENSITIVITY_ONLY_SIGNAL", "raw scalar / rank diagnostic", "Domain-dependent text-form feature"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    prior = pd.read_csv(Q1 / "QUALITY_SIGNAL_SEMANTICS_v1.csv", encoding="utf-8-sig")
    diagnostics = pd.read_csv(Q1 / "QUALITY_SIGNAL_DIAGNOSTICS_v1.csv", encoding="utf-8-sig")
    if len(prior) != 22 or set(prior.signal_id) != set(ROLES):
        raise RuntimeError("Round 2 22-signal contract changed")
    if set(diagnostics.source_id) != {"A1", "A2", "A3"}:
        raise RuntimeError("Round 1 diagnostics source mapping changed")
    rows = []
    for _, signal in prior.iterrows():
        sid = signal.signal_id
        role, compression, reason = ROLES[sid]
        subset = diagnostics[diagnostics.signal_id == sid]
        missing = "|".join(f"{r.source_id}:{int(r.missing_n)}" for _, r in subset.iterrows())
        if len(subset) != 3:
            raise RuntimeError(f"Missing audit diagnostic for {sid}")
        length_status = ("HIGH" if sid in UNKNOWN else
                         "DEFINITIONAL" if sid in EXCLUDED else
                         "POSSIBLE" if sid.startswith("rps_") or sid == "modernbert_reasoning" else
                         "NOT_ESTABLISHED")
        redundancy = ("DSIR_NEAR_DUPLICATE" if sid in UNKNOWN else
                      "LENGTH_DERIVED_CLUSTER" if sid in EXCLUDED or sid in
                      ("rps_doc_unigram_entropy", "rps_doc_frac_unique_words") else
                      "MODEL_RATER_SHARED_INPUT_POSSIBLE" if sid in CORE or sid.startswith("modernbert_") else
                      "TEXT_RULE_SHARED_INPUT_POSSIBLE" if sid.startswith("rps_") else
                      "MULTIFACET_NOT_COMPRESSIBLE_BY_DEFAULT")
        rows.append({
            "Signal ID": sid,
            "Semantic status": signal.source_meaning,
            "Direction status": signal.direction_status,
            "Unit status": signal.unit_status,
            "Redundancy status": redundancy,
            "Length-confounding status": length_status,
            "Missingness": missing,
            "Domain coverage": "A1_7_domains|A2_arxiv|A3_github",
            "Compression rule": compression,
            "DOWNSTREAM_ELIGIBILITY": signal.DOWNSTREAM_ELIGIBILITY,
            "Use in descriptive representation?": role,
            "Reason": reason,
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False, encoding="utf-8-sig")
    meta = {
        "status": "FROZEN_BEFORE_ROUND3_MODEL_COMPARISON",
        "script_sha256": sha256(Path(__file__)),
        "round2_semantics_sha256": sha256(Q1 / "QUALITY_SIGNAL_SEMANTICS_v1.csv"),
        "round1_diagnostics_sha256": sha256(Q1 / "QUALITY_SIGNAL_DIAGNOSTICS_v1.csv"),
        "output_sha256": sha256(OUT),
        "counts": pd.DataFrame(rows)["Use in descriptive representation?"].value_counts().to_dict(),
    }
    (OUT.with_suffix(".json")).write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
