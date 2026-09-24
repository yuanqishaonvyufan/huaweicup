"""Round 2 targeted Q1 semantics and conflict diagnostics; no final Q fit.

Uses the checked Round 1 mapping and raw hashes. Outputs a versioned evidence
table, focused DSIR/ngram/list checks, and explicitly provisional conflicts.
"""

from __future__ import annotations

import csv
import hashlib
import json
import lzma
import math
import re
import string
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, rankdata, spearmanr

from modeling_phase1_q1_audit import scalar_value, sha256, validate_mapping


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data/raw/real_attachments"
OUT = ROOT / "01_data/audits/modeling_phase1/q1"
OLD_DICTIONARY = OUT / "QUALITY_SIGNAL_DICTIONARY_v1.csv"
OLD_CONFLICT = OUT / "QUALITY_CONFLICT_INPUT_v1.csv"
RUN_ID = "AUDIT-Q1-SEMANTICS-CONFLICT-20260924-v1"
META_RATER = "https://huggingface.co/datasets/opendatalab/SlimPajama-Meta-rater/blob/main/README.md"
REDPAJAMA = "https://github.com/togethercomputer/RedPajama-Data/tree/6d2cee9df2b0204dd2bcb00bf06b5a7b1d7432d7"
REPETITION_CODE = REDPAJAMA.replace("/tree/", "/blob/") + "/app/src/core/quality_signals/repetitions.py"
DSIR_CODE = "https://github.com/p-lambda/dsir"
REDPAJAMA_IMPORTANCE_CODE = REDPAJAMA.replace("/tree/", "/blob/") + "/app/src/core/quality_signals/importance_weights.py"
POSITIVE = ["fineweb_edu", "fluency_en", "modernbert_cleanliness",
            "modernbert_readability", "ad_en"]
DSIR = ["dsir_books", "dsir_wiki", "dsir_math"]
NGRAM = ["rps_doc_frac_chars_top_2gram", "rps_doc_frac_chars_top_3gram"]
PRRC = ["modernbert_reasoning", "modernbert_professionalism",
        "modernbert_cleanliness", "modernbert_readability"]
LIST_SIGNALS = ["fineweb_edu", "fluency_en", "ad_en", "qurater", *PRRC]
TRANSLATE = str.maketrans("", "", string.punctuation)


def write_csv(path: Path, rows: list[dict], columns: list[str] | None = None) -> None:
    if columns is None:
        columns = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalized_words(text: str) -> list[str]:
    # RedPajama source-code normalization. Comparison only: no claim that
    # Meta-rater used the same version for every supplied annotation.
    text = text.translate(TRANSLATE).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return unicodedata.normalize("NFD", text).split()


def redpajama_top_ngram_percent(text: str, n: int) -> float:
    words = normalized_words(text)
    if len(words) < n:
        return 0.0
    grams = Counter(zip(*(words[i:] for i in range(n))))
    if not grams:
        return 0.0
    gram, count = grams.most_common(1)[0]
    if count <= 1:
        return 0.0
    total_chars = sum(map(len, words))
    return 100.0 * sum(map(len, gram)) * count / total_chars if total_chars else 0.0


def read_source(mapping: dict[str, str]) -> tuple[pd.DataFrame, list[dict]]:
    source = mapping["official_id"]
    rows, examples = [], []
    path = RAW / mapping["actual_relative_path"]
    with lzma.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            row = {"id": str(item["id"]), "source": source,
                   "domain": str(item.get("_source_domain") or ("arxiv" if source == "A2" else "github"))}
            for signal in ["rps_doc_word_count", "rps_doc_num_sentences", "rps_doc_unigram_entropy",
                           "rps_doc_frac_unique_words", *DSIR, *NGRAM]:
                row[signal] = float(item[signal])
            for signal in LIST_SIGNALS:
                scalar, status, parts = scalar_value(signal, item[signal])
                row[signal] = scalar
                if signal in PRRC:
                    row[signal + "_argmax"] = int(np.argmax(parts)) if status == "OK" else math.nan
                if signal in ("fluency_en", "ad_en"):
                    row[signal + "_argmax"] = int(np.argmax(parts)) if status == "OK" else math.nan
                if signal == "qurater":
                    for part_number in range(4):
                        row[f"qurater_{part_number}"] = parts[part_number] if status == "OK" else math.nan
            rows.append(row)
            if source == "A1" and any(row[x] > 100 for x in NGRAM):
                for n, signal in ((2, NGRAM[0]), (3, NGRAM[1])):
                    if row[signal] > 100:
                        predicted = redpajama_top_ngram_percent(item["content"], n)
                        examples.append({"id": row["id"], "domain": row["domain"], "signal": signal,
                                         "stored_percent": row[signal], "redpajama_formula_percent": predicted,
                                         "absolute_difference": abs(row[signal] - predicted),
                                         "normalized_word_count": len(normalized_words(item["content"]))})
    return pd.DataFrame(rows), examples


def rho(a: pd.Series | np.ndarray, b: pd.Series | np.ndarray) -> float:
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 4 or np.unique(a[ok]).size < 2 or np.unique(b[ok]).size < 2:
        return math.nan
    return float(spearmanr(a[ok], b[ok]).statistic)


def partial_rank_rho(a: np.ndarray, b: np.ndarray, length: np.ndarray) -> float:
    ok = np.isfinite(a) & np.isfinite(b) & np.isfinite(length)
    if ok.sum() < 10:
        return math.nan
    ra, rb, rl = [rankdata(v[ok]) for v in (a, b, np.log1p(length))]
    design = np.column_stack([np.ones(len(rl)), rl])
    resa = ra - design @ np.linalg.lstsq(design, ra, rcond=None)[0]
    resb = rb - design @ np.linalg.lstsq(design, rb, rcond=None)[0]
    return float(np.corrcoef(resa, resb)[0, 1])


def dsir_diagnostics(frames: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    scopes = {**frames, **{f"A1_{domain}": group for domain, group in frames["A1"].groupby("domain")}}
    for name, frame in scopes.items():
        length = frame["rps_doc_word_count"].to_numpy(float)
        for signal in DSIR:
            values = frame[signal].to_numpy(float)
            rows.append({"scope": name, "n": len(frame), "signal": signal,
                         "comparison": "word_count", "raw_spearman": rho(values, length),
                         "partial_rank_rho_controlling_word_count": "",
                         "median_score": float(np.median(values))})
        for i, left in enumerate(DSIR):
            for right in DSIR[i + 1:]:
                a, b = frame[left].to_numpy(float), frame[right].to_numpy(float)
                rows.append({"scope": name, "n": len(frame), "signal": left,
                             "comparison": right, "raw_spearman": rho(a, b),
                             "partial_rank_rho_controlling_word_count": partial_rank_rho(a, b, length),
                             "median_score": ""})
    return rows


def ngram_diagnostics(frames: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    for source, frame in frames.items():
        for domain, group in [("ALL", frame), *list(frame.groupby("domain"))]:
            for signal in NGRAM:
                values = group[signal].to_numpy(float)
                rows.append({"source": source, "domain": domain, "signal": signal, "n": len(group),
                             "gt_100_count": int(np.sum(values > 100)),
                             "gt_100_rate": float(np.mean(values > 100)),
                             "max": float(np.max(values))})
    return rows


def list_diagnostics(frames: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    for source, frame in frames.items():
        for signal in [*PRRC, "fluency_en", "ad_en"]:
            left, right = frame[signal], frame[signal + "_argmax"]
            ok = np.isfinite(left) & np.isfinite(right)
            rows.append({"source": source, "signal": signal, "n_finite": int(ok.sum()),
                         "spearman_margin_or_expectation_vs_argmax": rho(left, right),
                         "argmax_unique_levels": int(right[ok].nunique())})
    return rows


def percentile(values: np.ndarray) -> np.ndarray:
    return (rankdata(values, method="average") - 0.5) / len(values)


def pairwise_discordance(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    # Kendall tau-b plus exact tie counts gives D/(C+D), where pairs tied in
    # either metric are not comparable. scipy computes tau in O(n log n).
    n = len(x)
    tau = float(kendalltau(x, y).statistic)
    if not np.isfinite(tau):
        return math.nan, math.nan
    total = n * (n - 1) // 2
    ties_x = int(sum(c * (c - 1) // 2 for c in Counter(x).values()))
    ties_y = int(sum(c * (c - 1) // 2 for c in Counter(y).values()))
    ties_both = int(sum(c * (c - 1) // 2 for c in Counter(zip(x, y)).values()))
    comparable = total - ties_x - ties_y + ties_both
    if comparable <= 0:
        return math.nan, tau
    c_minus_d = tau * math.sqrt((total - ties_x) * (total - ties_y))
    discordant = max(0.0, min(float(comparable), (comparable - c_minus_d) / 2))
    return discordant / comparable, tau


def wilson_interval(events: int, n: int) -> tuple[float, float]:
    if n == 0:
        return math.nan, math.nan
    z = 1.959963984540054
    p = events / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, center - half), min(1.0, center + half)


def conflict_diagnostics(frames: dict[str, pd.DataFrame]) -> list[dict]:
    a1_ids = set(frames["A1"]["id"])
    a2_new = frames["A2"].loc[~frames["A2"]["id"].isin(a1_ids)]
    a3_new = frames["A3"].loc[~frames["A3"]["id"].isin(a1_ids)]
    scopes = {
        "A1_all": frames["A1"], "A2_all_overlap_included": frames["A2"],
        "A3_all_overlap_included": frames["A3"],
        "A2_new_ids": a2_new, "A3_new_ids": a3_new,
        "UNIQUE_ALL": pd.concat([frames["A1"], a2_new, a3_new], ignore_index=True),
        **{f"A1_{domain}": group for domain, group in frames["A1"].groupby("domain")},
    }
    with OLD_CONFLICT.open(encoding="utf-8-sig", newline="") as stream:
        candidates = [r for r in csv.DictReader(stream) if r["kind"] == "RANK_DISCORDANCE_CANDIDATE"]
    rows = []
    for old in candidates:
        left, right = old["signal_a"], old["signal_b"]
        assert left in POSITIVE and right in POSITIVE
        for name, frame in scopes.items():
            pair = frame[[left, right]].to_numpy(float)
            ok = np.isfinite(pair).all(axis=1)
            x, y = pair[ok, 0], pair[ok, 1]
            if len(x) < 10:
                continue
            px, py = percentile(x), percentile(y)
            reversal, tau = pairwise_discordance(x, y)
            pair_rho = rho(x, y)
            for q in (0.75, 0.80, 0.90):
                events = ((px >= q) & (py <= 1 - q)) | ((py >= q) & (px <= 1 - q))
                count = int(events.sum())
                lo, hi = wilson_interval(count, len(x))
                rows.append({"candidate_id": old["candidate_id"], "scope": name,
                             "signal_a": left, "signal_b": right,
                             "n_unique_in_scope": len(x), "q": q,
                             "extreme_discordant_count": count,
                             "extreme_discordance_rate": count / len(x),
                             "wilson95_low_fixed_rank_cutoffs": lo,
                             "wilson95_high_fixed_rank_cutoffs": hi,
                             "pairwise_reversal_rate_excluding_ties": reversal,
                             "kendall_tau_b": tau, "spearman_rho": pair_rho})
    return rows


def semantic_table() -> list[dict]:
    with OLD_DICTIONARY.open(encoding="utf-8-sig", newline="") as stream:
        old = list(csv.DictReader(stream))
    assert len(old) == 22
    rows = []
    for row in old:
        signal = row["Signal ID"]
        family = ("DSIR_TARGET_SIMILARITY" if signal in DSIR else
                  "RPS_TEXT_RULE" if signal.startswith("rps_") else
                  "MODEL_ANNOTATION")
        direction = ("POSITIVE_CANDIDATE" if signal in POSITIVE else "CONTEXT_DEPENDENT")
        eligibility = "UNKNOWN" if signal in [*DSIR, *NGRAM] else "DESCRIPTIVE_ONLY"
        source = META_RATER
        if signal.startswith("rps_"):
            source += " | " + (REPETITION_CODE if signal in NGRAM else REDPAJAMA)
        if signal in DSIR:
            source += " | " + DSIR_CODE + " | " + REDPAJAMA_IMPORTANCE_CODE
        unit = row["Unit"]
        if signal in NGRAM:
            unit = "A1: 100*RedPajama ratio matches both >100 cases; A2/A3: pipeline not verified"
        elif signal in DSIR:
            unit = "raw negative score; exact scale/normalization unresolved"
        compression = row["Transformation candidate"]
        if signal == "qurater":
            compression = "retain four facets; mean is Round 1 diagnostic only"
        elif signal in PRRC:
            compression = "argmax rating (source card) vs softmax expected level (Round 1 diagnostic)"
        elif signal in ("ad_en", "fluency_en"):
            compression = "source card argmax vs Round 1 positive-class margin"
        rows.append({"signal_id": signal, "source_family": family,
                     "source_meaning": row["Meaning"], "raw_type": row["Data type"],
                     "unit_status": unit, "direction_status": direction,
                     "compression_candidates": compression,
                     "redundancy_or_derivation": row["Redundancy group"] + "; " + row["Derived-variable risk"],
                     "DOWNSTREAM_ELIGIBILITY": eligibility,
                     "q2_current_use": "NO_MATCHED_Q_NO_INDEPENDENT_Q_EFFECT",
                     "evidence_url": source,
                     "evidence_limit": "Public source describes a signal family; contest extraction/calibration not fully traceable"})
    return rows


def classify_input(conflict_rows: list[dict]) -> list[dict]:
    by_pair_scope = {(r["candidate_id"], r["scope"], r["q"]): r for r in conflict_rows}
    with OLD_CONFLICT.open(encoding="utf-8-sig", newline="") as stream:
        old = list(csv.DictReader(stream))
    assert len(old) == 42
    rows = []
    for row in old:
        number = int(row["candidate_id"].split("-")[1])
        if number <= 3 or number in (4, 5, 9):
            category, note = "REDUNDANCY", "Shared generator/length structure; association is not quality conflict"
        elif 13 <= number <= 24:
            category, note = "SCALE ARTIFACT", "Length/ratio/DSIR coupling candidate; mechanism not fully proven"
        elif 25 <= number <= 34:
            category, note = "STATISTICAL DISAGREEMENT", "Both diagnostic margins oriented; no proven semantic tradeoff"
        else:
            category, note = "UNRESOLVED", "Raw association or PC1 residual alone is insufficient"
        if 6 <= number <= 12:
            category, note = "UNRESOLVED", "Raw correlation; semantic direction or independent content not established"
        if 25 <= number <= 34:
            scope_rows = [r for r in conflict_rows
                          if r["candidate_id"] == row["candidate_id"] and r["q"] == 0.8
                          and (r["scope"].startswith("A1_") and r["scope"] != "A1_all"
                               or r["scope"] in ("A2_new_ids", "A3_new_ids"))
                          and r["n_unique_in_scope"] >= 1000]
            positive_scopes = [r["scope"] for r in scope_rows if r["spearman_rho"] >= 0.1]
            negative_scopes = [r["scope"] for r in scope_rows if r["spearman_rho"] <= -0.1]
            if positive_scopes and negative_scopes:
                category = "DOMAIN-SPECIFIC REVERSAL"
                note = ("Descriptive sign reversal across adequately sized strata: positive="
                        + "|".join(positive_scopes) + "; negative=" + "|".join(negative_scopes)
                        + "; not a semantic quality conflict")
        diag = by_pair_scope.get((row["candidate_id"], "A1_all", 0.8), {})
        rows.append({"candidate_id": row["candidate_id"], "signal_a": row["signal_a"],
                     "signal_b": row["signal_b"], "round1_kind": row["kind"],
                     "conflict_class": category, "status": "PROVISIONAL_NOT_FINAL_CONFLICT",
                     "reason": note, "rho_A1_round1": row["rho_A1"],
                     "A1_q80_extreme_rate": diag.get("extreme_discordance_rate", ""),
                     "A1_pairwise_reversal_rate": diag.get("pairwise_reversal_rate_excluding_ties", "")})
    return rows


def main() -> None:
    mappings, _, mapping_sha = validate_mapping()
    frames, examples = {}, []
    for mapping in mappings:
        frame, sample_examples = read_source(mapping)
        frames[mapping["official_id"]] = frame
        examples.extend(sample_examples)
        expected = {"A1": 51230, "A2": 17523, "A3": 203752}[mapping["official_id"]]
        if len(frame) != expected or frame["id"].duplicated().any():
            raise RuntimeError("Unexpected row count or within-source duplicate ID")
    if len(set(frames["A1"].id) & set(frames["A2"].id)) != 1419:
        raise RuntimeError("A1/A2 overlap changed")
    if len(set(frames["A1"].id) & set(frames["A3"].id)) != 10000:
        raise RuntimeError("A1/A3 overlap changed")

    semantic = semantic_table()
    dsir = dsir_diagnostics(frames)
    ngram = ngram_diagnostics(frames)
    lists = list_diagnostics(frames)
    conflict = conflict_diagnostics(frames)
    classified = classify_input(conflict)
    write_csv(OUT / "QUALITY_SIGNAL_SEMANTICS_v1.csv", semantic)
    write_csv(OUT / "Q1_DSIR_LENGTH_DIAGNOSTICS_v1.csv", dsir)
    write_csv(OUT / "Q1_NGRAM_BOUNDARY_DIAGNOSTICS_v1.csv", ngram)
    write_csv(OUT / "Q1_NGRAM_SOURCE_FORMULA_CHECK_v1.csv", examples)
    write_csv(OUT / "Q1_LIST_ENCODING_SENSITIVITY_v1.csv", lists)
    write_csv(OUT / "Q1_CONFLICT_STABILITY_v1.csv", conflict)
    write_csv(OUT / "QUALITY_CONFLICT_CANDIDATES_v1.csv", classified)
    result = {
        "run_id": RUN_ID, "run_class": "AUDIT_RUN_WITH_DIAGNOSTICS_NO_MODEL_FIT",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)), "mapping_sha256": mapping_sha,
        "input_sha256": {m["official_id"]: m["sha256"] for m in mappings},
        "output_rows": {"semantics": len(semantic), "dsir": len(dsir), "ngram": len(ngram),
                        "ngram_examples": len(examples), "list_encoding": len(lists),
                        "conflict_stability": len(conflict), "conflict_candidates": len(classified)},
        "counts": {"physical_rows": sum(len(f) for f in frames.values()),
                   "unique_ids": len(set().union(*(set(f.id) for f in frames.values()))),
                   "A1_ngram_over_100_cases": len(set(x["id"] for x in examples))},
        "method_limits": [
            "Wilson intervals treat document IDs as independent and hold empirical rank cutoffs fixed",
            "No A4/A5 or A6-A11 Loss used to orient or select quality signals",
            "Upstream RedPajama formula match on A1 cases does not prove A2/A3 pipeline identity",
        ],
    }
    (OUT / "Q1_ROUND2_DIAGNOSTICS_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                                       encoding="utf-8")
    print(json.dumps({"run_id": RUN_ID, **result["output_rows"], **result["counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
