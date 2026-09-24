#!/usr/bin/env python3
"""B1 audit run v1.0.0. Read raw B1; never estimate a scaling law.

Run from any working directory:
    python 04_code/data_audit/modeling_phase1_b1_audit.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parents[2]
RAW_REL = "B_scaling_laws/pythia_training_log_existing.csv"
RAW = ROOT / "01_data/raw/real_attachments" / RAW_REL
RAW_MANIFEST = ROOT / "01_data/raw/RAW_SHA256.csv"
SOURCE_MANIFEST = ROOT / "01_data/raw/real_attachments/source_manifest.json"
OFFICIAL_PDF = ROOT / "00_problem/original/F_2026_data_description_user_supplied.pdf"
OUT = ROOT / "01_data/audits/modeling_phase1/q2"
EXPECTED_RAW_SHA256 = "529a59644b0f57bf3a76037838b614bfedc35e58bb26b93052e34ffc63e454c2"
EXPECTED_OFFICIAL_SHA256 = "f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835"
EXPECTED_FIELDS = [
    "run_id", "N_params_B", "D_tokens_B", "C_FLOPs_1e21", "steps",
    "batch_tokens_M", "lr", "wd", "precision", "gpu_days",
    "step_time_ms", "train_loss", "val_loss", "ppl", "grad_norm_avg",
]
NUMERIC_FIELDS = [x for x in EXPECTED_FIELDS if x != "precision"]
# Order and approximate model-size labels follow the Pythia suite. The CSV lacks
# model_repo/version/seed, so these labels are inferred and never used as keys.
MODEL_SIZES = ["70m", "160m", "410m", "1b", "1.4b", "2.8b", "6.9b", "12b"]
PYTHIA_README = "https://github.com/EleutherAI/pythia/blob/main/README.md#models"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def finite(value: float) -> float | None:
    x = float(value)
    return x if math.isfinite(x) else None


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    raw_hash = sha256(RAW)
    pdf_hash = sha256(OFFICIAL_PDF)
    if raw_hash != EXPECTED_RAW_SHA256:
        raise RuntimeError(f"B1 raw hash mismatch: {raw_hash}")
    if pdf_hash != EXPECTED_OFFICIAL_SHA256:
        raise RuntimeError(f"Official data-description hash mismatch: {pdf_hash}")

    with RAW_MANIFEST.open(encoding="utf-8-sig", newline="") as stream:
        manifest_rows = [r for r in csv.DictReader(stream) if r["relative_path"] == RAW_REL]
    if len(manifest_rows) != 1 or manifest_rows[0]["sha256"] != raw_hash:
        raise RuntimeError("B1 hash not uniquely confirmed in RAW_SHA256.csv")
    if int(manifest_rows[0]["bytes"]) != RAW.stat().st_size:
        raise RuntimeError("B1 byte size differs from RAW_SHA256.csv")
    with SOURCE_MANIFEST.open(encoding="utf-8") as stream:
        source_rows = [r for r in json.load(stream) if r.get("file") == RAW_REL]
    if len(source_rows) != 1 or source_rows[0].get("problem") != "B":
        raise RuntimeError("B1 provenance entry missing or ambiguous")

    frame = pd.read_csv(RAW)
    if frame.columns.tolist() != EXPECTED_FIELDS:
        raise RuntimeError(f"DATA_SCHEMA_DISCREPANCY: actual fields {frame.columns.tolist()}")
    for field in NUMERIC_FIELDS:
        frame[field] = pd.to_numeric(frame[field], errors="coerce")
    if frame[NUMERIC_FIELDS].isna().any().any():
        raise RuntimeError("Required numeric field contains invalid values")
    if (frame[["N_params_B", "D_tokens_B", "val_loss", "ppl", "steps"]] <= 0).any().any():
        raise RuntimeError("Required positive field has zero/negative values")

    OUT.mkdir(parents=True, exist_ok=True)
    sizes = sorted(frame.N_params_B.unique())
    model_by_n = dict(zip(sizes, MODEL_SIZES, strict=True))
    global_missing = frame.isna().sum().to_dict()
    exact_duplicates = int(frame.duplicated().sum())
    id_duplicates = int(frame.run_id.duplicated().sum())
    nd_duplicates = int(frame.duplicated(["N_params_B", "D_tokens_B"]).sum())
    step_duplicates = int(frame.duplicated(["N_params_B", "steps"]).sum())
    d_levels = sorted(frame.D_tokens_B.unique())
    n_levels = sorted(frame.N_params_B.unique())
    step_levels = sorted(frame.steps.unique())
    full_grid = len(frame) == len(n_levels) * len(d_levels) and nd_duplicates == 0

    log_n = np.log(frame.N_params_B.to_numpy())
    log_d = np.log(frame.D_tokens_B.to_numpy())
    design = np.column_stack([np.ones(len(frame)), log_n - log_n.mean(), log_d - log_d.mean()])
    singular = np.linalg.svd(design, compute_uv=False)
    design_rank = int(np.linalg.matrix_rank(design))
    log_corr = finite(np.corrcoef(log_n, log_d)[0, 1])
    log_spearman = finite(pd.Series(log_n).corr(pd.Series(log_d), method="spearman"))
    expected_d = frame.steps.to_numpy() * 2097152 / 1e9
    d_absolute_error = np.abs(frame.D_tokens_B.to_numpy() - expected_d)
    expected_c = 0.006 * frame.N_params_B.to_numpy() * frame.D_tokens_B.to_numpy()
    c_ratio = frame.C_FLOPs_1e21.to_numpy() / expected_c
    ppl_expected = np.exp(frame.val_loss.to_numpy())
    ppl_relative_error = np.abs(frame.ppl.to_numpy() - ppl_expected) / ppl_expected

    group_rows: list[dict] = []
    for n, raw_group in frame.groupby("N_params_B", sort=True):
        group = raw_group.sort_values("steps")
        label = model_by_n[n]
        expected_precision = "bf16" if label == "1b" else "fp16"
        precision_series = group.precision.astype(str)
        changes = int((precision_series != precision_series.shift()).sum() - 1)
        row = {
            "inferred_model_size": label,
            "N_params_B": n,
            "rows": len(group),
            "independent_training_run_count_confirmed": "UNKNOWN",
            "step_min": int(group.steps.min()),
            "step_max": int(group.steps.max()),
            "unique_steps": int(group.steps.nunique()),
            "D_min_Btokens": float(group.D_tokens_B.min()),
            "D_max_Btokens": float(group.D_tokens_B.max()),
            "unique_D": int(group.D_tokens_B.nunique()),
            "val_loss_min": float(group.val_loss.min()),
            "val_loss_max": float(group.val_loss.max()),
            "val_loss_increase_intervals": int((np.diff(group.val_loss) > 0).sum()),
            "train_loss_increase_intervals": int((np.diff(group.train_loss) > 0).sum()),
            "step_strictly_increasing": bool((np.diff(group.steps) > 0).all()),
            "D_strictly_increasing": bool((np.diff(group.D_tokens_B) > 0).all()),
            "unique_lr": int(group.lr.nunique()),
            "lr_value": float(group.lr.iloc[0]) if group.lr.nunique() == 1 else "MIXED",
            "unique_wd": int(group.wd.nunique()),
            "fp16_rows": int((precision_series == "fp16").sum()),
            "bf16_rows": int((precision_series == "bf16").sum()),
            "precision_transitions": changes,
            "official_expected_training_precision": expected_precision,
            "precision_mismatch_rows_if_training_metadata": int((precision_series != expected_precision).sum()),
            "run_id_min": int(group.run_id.min()),
            "run_id_max": int(group.run_id.max()),
            "run_id_unique": int(group.run_id.nunique()),
        }
        group_rows.append(row)
    total_precision_mismatch = sum(x["precision_mismatch_rows_if_training_metadata"] for x in group_rows)
    total_precision_transitions = sum(x["precision_transitions"] for x in group_rows)

    diagnostics: list[dict] = []
    def add(section: str, metric: str, value: object, unit: str = "", note: str = "") -> None:
        diagnostics.append({"section": section, "metric": metric, "value": value, "unit": unit, "note": note})

    add("mapping", "official_id", "B1")
    add("mapping", "mapping_status", "CONFIRMED_OFFICIAL_ID_ROLE_PATH_HASH")
    add("shape", "rows", len(frame), "rows")
    add("shape", "fields", len(frame.columns), "columns")
    add("shape", "exact_duplicate_rows", exact_duplicates, "rows")
    add("shape", "duplicate_run_id_rows", id_duplicates, "rows", "run_id is a checkpoint row ID, not training-run ID")
    add("shape", "duplicate_N_D_rows", nd_duplicates, "rows")
    add("shape", "duplicate_N_step_rows", step_duplicates, "rows")
    for field in EXPECTED_FIELDS:
        add("field", f"{field}.missing", int(global_missing[field]), "rows")
        add("field", f"{field}.unique", int(frame[field].nunique(dropna=True)), "values")
        if field in NUMERIC_FIELDS:
            add("field", f"{field}.min", float(frame[field].min()), "raw column units")
            add("field", f"{field}.max", float(frame[field].max()), "raw column units")
    add("coverage", "unique_N", len(n_levels), "levels")
    add("coverage", "unique_D", len(d_levels), "levels")
    add("coverage", "unique_steps", len(step_levels), "levels")
    add("coverage", "unique_N_D", len(frame) - nd_duplicates, "pairs")
    add("coverage", "full_N_D_cartesian_grid", full_grid)
    add("coverage", "replicate_N_D_rows", nd_duplicates, "rows")
    add("coverage", "log_N_range", finite(log_n.max() - log_n.min()), "natural-log units")
    add("coverage", "log_D_range", finite(log_d.max() - log_d.min()), "natural-log units")
    add("coverage", "N_decades", finite(np.log10(max(n_levels) / min(n_levels))), "log10 units")
    add("coverage", "D_decades", finite(np.log10(max(d_levels) / min(d_levels))), "log10 units")
    add("coverage", "log_N_log_D_pearson", log_corr)
    add("coverage", "log_N_log_D_spearman", log_spearman)
    add("coverage", "centered_design_rank_1_logN_logD", design_rank, "of 3", "Geometric rank only; no Loss fit")
    add("coverage", "centered_design_condition", finite(singular[0] / singular[-1]))
    add("coverage", "min_unique_D_per_N", int(frame.groupby("N_params_B").D_tokens_B.nunique().min()))
    add("coverage", "min_unique_N_per_D", int(frame.groupby("D_tokens_B").N_params_B.nunique().min()))
    add("consistency", "max_D_minus_step_times_2097152", finite(d_absolute_error.max()), "B tokens")
    add("consistency", "median_C_over_6ND", finite(np.median(c_ratio)), "ratio", "C rounded to 4 decimals")
    add("consistency", "median_ppl_relative_error", finite(np.median(ppl_relative_error)), "fraction")
    add("consistency", "max_ppl_relative_error", finite(ppl_relative_error.max()), "fraction")
    add("consistency", "val_loss_below_train_loss_rows", int((frame.val_loss < frame.train_loss).sum()), "rows")
    add("source", "precision_mismatch_rows_if_training_metadata", total_precision_mismatch, "rows", PYTHIA_README)
    add("source", "precision_transitions_within_inferred_N_trajectories", total_precision_transitions, "transitions")
    add("source", "trajectory_groups_by_N", len(n_levels), "groups", "No explicit model_repo/seed/version in B1")
    add("source", "validation_corpus_field_present", False)
    add("source", "model_repo_or_commit_field_present", False)
    add("source", "seed_field_present", False)

    summary = {
        "audit_id": "AUDIT-B1-ELIGIBILITY-v1",
        "audit_version": VERSION,
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "classification": "AUDIT RUN",
        "eligibility_verdict": "NOT YET ELIGIBLE",
        "input": {
            "official_id": "B1",
            "official_description": "Pythia training log, 1,176 rows; real; Question 2 primary fitting input",
            "official_description_pdf_pages": [3, 10, 11],
            "official_description_path": str(OFFICIAL_PDF.relative_to(ROOT)),
            "official_description_sha256": pdf_hash,
            "relative_path": str(RAW.relative_to(ROOT)),
            "sha256": raw_hash,
            "bytes": RAW.stat().st_size,
            "raw_sha256_manifest_sha256": sha256(RAW_MANIFEST),
            "source_manifest_sha256": sha256(SOURCE_MANIFEST),
            "actual_fields": EXPECTED_FIELDS,
            "expected_core_fields_official": ["N_params_B", "D_tokens_B", "C_FLOPs_1e21", "val_loss"],
            "source_manifest_entry": source_rows[0],
            "mapping_status": "CONFIRMED_OFFICIAL_ID_ROLE_PATH_HASH",
        },
        "code": {
            "relative_path": str(Path(__file__).resolve().relative_to(ROOT)),
            "sha256": sha256(Path(__file__).resolve()),
            "python_dependencies": {"numpy": np.__version__, "pandas": pd.__version__},
            "random_seed": "NOT_APPLICABLE_DETERMINISTIC_AUDIT",
        },
        "shape": {
            "rows": len(frame), "fields": len(frame.columns),
            "missing_by_field": {k: int(v) for k, v in global_missing.items()},
            "exact_duplicate_rows": exact_duplicates,
            "duplicate_run_id_rows": id_duplicates,
            "duplicate_N_D_rows": nd_duplicates,
            "duplicate_N_step_rows": step_duplicates,
        },
        "coverage": {
            "unique_N": len(n_levels), "unique_D": len(d_levels),
            "N_min_B": min(n_levels), "N_max_B": max(n_levels),
            "D_min_B": min(d_levels), "D_max_B": max(d_levels),
            "unique_N_D": len(frame) - nd_duplicates,
            "full_N_D_cartesian_grid": full_grid,
            "replicate_N_D_rows": nd_duplicates,
            "log_N_range": finite(log_n.max() - log_n.min()),
            "log_D_range": finite(log_d.max() - log_d.min()),
            "N_decades": finite(np.log10(max(n_levels) / min(n_levels))),
            "D_decades": finite(np.log10(max(d_levels) / min(d_levels))),
            "log_N_log_D_pearson": log_corr,
            "log_N_log_D_spearman": log_spearman,
            "geometric_design_rank": design_rank,
            "geometric_design_singular_values": [finite(x) for x in singular],
            "geometric_design_condition": finite(singular[0] / singular[-1]),
            "min_unique_D_per_N": int(frame.groupby("N_params_B").D_tokens_B.nunique().min()),
            "min_unique_N_per_D": int(frame.groupby("D_tokens_B").N_params_B.nunique().min()),
        },
        "consistency": {
            "max_D_minus_step_times_2097152_Btokens": finite(d_absolute_error.max()),
            "median_C_over_6ND": finite(np.median(c_ratio)),
            "C_over_6ND_p05": finite(np.quantile(c_ratio, .05)),
            "C_over_6ND_p95": finite(np.quantile(c_ratio, .95)),
            "median_ppl_relative_error": finite(np.median(ppl_relative_error)),
            "max_ppl_relative_error": finite(ppl_relative_error.max()),
            "val_loss_below_train_loss_rows": int((frame.val_loss < frame.train_loss).sum()),
            "val_loss_increase_intervals": sum(x["val_loss_increase_intervals"] for x in group_rows),
        },
        "provenance_alert": {
            "id": "EVIDENCE_ALERT_B1_SOURCE_METADATA_v1",
            "severity": "CRITICAL_FOR_B1_BASELINE_ELIGIBILITY",
            "precision_mismatch_rows_if_training_metadata": total_precision_mismatch,
            "precision_transitions_within_inferred_N_trajectories": total_precision_transitions,
            "public_primary_source": PYTHIA_README,
            "interpretive_limit": "precision field meaning and each row's origin unresolved; this does not prove val_loss is fabricated",
        },
        "groups": group_rows,
    }

    write_csv(OUT / "B1_COVERAGE_DIAGNOSTICS_v1.csv", ["section", "metric", "value", "unit", "note"], diagnostics)
    write_csv(OUT / "B1_GROUP_STRUCTURE_v1.csv", list(group_rows[0]), group_rows)
    (OUT / "B1_ELIGIBILITY_DIAGNOSTICS_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit_md = f"""# B1 Baseline Eligibility Audit v1

**Audit ID:** `AUDIT-B1-ELIGIBILITY-v1`  
**Run class:** AUDIT RUN; no model parameters estimated.  
**Verdict:** **NOT YET ELIGIBLE** for a formal source-internal N–D baseline.  
**Code version/hash:** `{VERSION}` / `{summary['code']['sha256']}`.  
**Raw SHA-256:** `{raw_hash}`.

## 1. Official mapping and grain

The visible body of the user-supplied F data description, pages 3, 10 and 11, assigns **B1** to `B_scaling_laws/pythia_training_log_existing.csv`: Pythia training log, **real**, 1,176 rows × 15 fields, Question 2 primary-fitting input. It defines `N_params_B` as parameter count in billions, `D_tokens_B` as training tokens in billions, `C_FLOPs_1e21` as cumulative FLOPs in 10²¹, and `val_loss` as validation cross entropy. The copied raw file exists at `01_data/raw/real_attachments/{RAW_REL}`. Its hash and 111,459 bytes match `RAW_SHA256.csv`; `source_manifest.json` identifies the same path and Pythia suite. **Mapping status: CONFIRMED_OFFICIAL_ID_ROLE_PATH_HASH.** The PDF's faint margin text is excluded from all official claims.

Actual 15 fields: `{', '.join(EXPECTED_FIELDS)}`. The row grain is an inferred model-size × checkpoint observation. `run_id` is unique per row; no field explicitly identifies the training run, repository revision, seed, evaluation corpus, tokenizer, or loss logging recipe. A model-size label below is inferred from the eight N levels and is not an observed B1 identifier.

## 2. Shape and N–D support

There are **{len(frame):,} rows**, **{len(n_levels)} N levels** ({min(n_levels):.6f}–{max(n_levels):.6f} B), **{len(d_levels)} D levels** ({min(d_levels):.3f}–{max(d_levels):.3f} B tokens), and **{len(frame)-nd_duplicates:,} unique N–D pairs**. Every N has {min(x['unique_D'] for x in group_rows)} D levels; every D has {int(frame.groupby('D_tokens_B').N_params_B.nunique().min())} N levels. The full 8 × 147 Cartesian grid is present, with **zero N–D replicate rows**. Natural-log ranges are {summary['coverage']['log_N_range']:.3f} for N and {summary['coverage']['log_D_range']:.3f} for D; Pearson correlation of log N and log D is {log_corr:.3g}. The centered `[1, log N, log D]` *design* has rank {design_rank}/3 and condition number {summary['coverage']['geometric_design_condition']:.3f}. This establishes geometric independent variation, **not stable scaling-law coefficients**.

No missing values, exact duplicate rows, repeated `run_id`, repeated N–D pairs, or repeated N–step pairs were found. Each inferred size has 147 increasing steps and increasing D values. The 1,176 rows are repeated checkpoints of at most eight observed size trajectories; their residuals and errors must not be treated as 1,176 independent training experiments. No separate seed/replicate is identified. A future validation split must leave out entire N trajectories, with only eight candidate groups.

## 3. Unit and Loss checks

The maximum absolute difference between reported D and `steps × 2,097,152 / 10⁹` is {summary['consistency']['max_D_minus_step_times_2097152_Btokens']:.6f} B tokens, consistent with D rounded to three decimals. For `C_FLOPs_1e21`, the ratio to `0.006 × N_params_B × D_tokens_B` has median {summary['consistency']['median_C_over_6ND']:.5f}; early C values are rounded to four decimals, so per-row relative errors at very small compute need care. `val_loss` ranges from {frame.val_loss.min():.4f} to {frame.val_loss.max():.4f}. It is greater than or equal to `train_loss` in all rows and has {summary['consistency']['val_loss_increase_intervals']} increases across the 1,168 adjacent within-size checkpoint intervals. `ppl` agrees with `exp(val_loss)` to median relative error {100*summary['consistency']['median_ppl_relative_error']:.4f}% (max {100*summary['consistency']['max_ppl_relative_error']:.4f}%). These checks support internal arithmetic and a shared column convention; they do **not** verify the validation corpus, tokenizer, or that values were copied from the original Pythia logs. The official PDF names `val_loss` as validation cross entropy but gives no validation set/version. The table contains no such identifier.

## 4. Source/provenance contradiction and hidden structure

The official data description marks B1 as *real Pythia training trajectories*. The [Pythia primary repository]({PYTHIA_README}) states that standard Pythia models were trained with fp16 except the 1B model, which used bf16. In B1, **all eight inferred size trajectories mix fp16 and bf16**; there are **{total_precision_transitions} within-trajectory precision changes** and **{total_precision_mismatch} rows** disagree with the corresponding official training precision if the field denotes training precision. For example, the 70M trajectory has {group_rows[0]['bf16_rows']} bf16 rows even though official Pythia 70M used fp16; the 1B trajectory has {group_rows[3]['fp16_rows']} fp16 rows even though official 1B used bf16. `wd` also varies within every size trajectory (see group CSV), while its exact intended meaning is undocumented. The discrepancy could be mislabeled or augmented metadata, a different meaning of `precision`, or a distinct data compilation; the audit does **not** infer that `val_loss` is fabricated. It requires a row-level provenance explanation.

The same repository documents 154 released checkpoints per model; B1 uses a 147-checkpoint subset starting at step 64. This subset alone is not a contradiction. B1 gives no standard/deduplicated/v0 version, model repository, seed, validation set, or raw logging URI. Thus `val_loss` consistency across sizes remains **UNVERIFIED**, despite its internal `ppl` relation.

## 5. Decision by intended use

| Intended use | Decision | Reason |
|---|---|---|
| N–D geometry and checkpoint-dependence diagnostics | PASS | Complete crossed support and stable row keys; audit only. |
| Formal Pythia source-internal N–D baseline estimation | **FAIL / NOT YET ELIGIBLE** | Training-metadata contradiction and unverified `val_loss` provenance/definition. |
| Infer independent N and D effects from row count alone | FAIL | Only eight size trajectories; no independent seed/replicate metadata. |
| Pool absolute Loss with A or estimate Q elasticity | FAIL | No common target scale or matched quality variation. |

Minimum release condition: trace B1 `val_loss`, N, D, model version, tokenizer/validation corpus and `precision`/`wd` definitions to original logs or a documented transformation; resolve the mismatch in an explicit data contract. Then freeze source-internal baseline specification, preserve an entire-trajectory holdout and disclose the eight-group limitation. No B1 scaling law was fitted in this audit.

## 6. Reproducibility and limits

Run `python 04_code/data_audit/modeling_phase1_b1_audit.py` from the project root or an arbitrary working directory. It refuses unexpected raw/PDF hashes or schema. The script, raw file, official PDF, manifest hashes, numeric checks, group table and verdict are recorded in `B1_ELIGIBILITY_DIAGNOSTICS_v1.json`. All computations are deterministic; random seed is not applicable. The two CSVs are machine-readable audit evidence. Public Pythia documentation is used only to check source claims, not to replace the user-provided official numbering.
"""
    (OUT / "B1_BASELINE_ELIGIBILITY_AUDIT_v1.md").write_text(audit_md, encoding="utf-8")

    executive_md = f"""# B1 Baseline Eligibility Executive v1

**Verdict: NOT YET ELIGIBLE.** B1 has a complete 8 × 147 N–D grid (1,176 rows), so N and D vary independently in the observed geometry. The centered log-design rank is 3/3 and log N–log D correlation is {log_corr:.3g}. There are no repeated N–D cells and only eight inferred training trajectories; checkpoint rows cannot be counted as independent runs.

`ppl ≈ exp(val_loss)` and `C ≈ 6ND` in the official units, but those arithmetic checks do not establish the validation-Loss source. B1 lacks model version, seed, validation corpus and tokenizer. More seriously, all eight size trajectories alternate `precision` values, contrary to the [Pythia primary description]({PYTHIA_README}) if `precision` is training precision. {total_precision_mismatch} rows conflict under that interpretation. The discrepancy is logged in [EVIDENCE_ALERT_B1_SOURCE_METADATA_v1.md](EVIDENCE_ALERT_B1_SOURCE_METADATA_v1.md). B1 remains usable for **data-geometry diagnostics**; formal N–D estimation awaits provenance reconciliation. No Scaling Law was fitted.

The next evidence request is a row-level source or transformation record for N, D, `val_loss`, `precision`, validation corpus, tokenizer and Pythia version, followed by an entire-trajectory holdout design. Full checks and raw/code hashes: [audit](B1_BASELINE_ELIGIBILITY_AUDIT_v1.md), [machine JSON](B1_ELIGIBILITY_DIAGNOSTICS_v1.json), [coverage CSV](B1_COVERAGE_DIAGNOSTICS_v1.csv), [group CSV](B1_GROUP_STRUCTURE_v1.csv).
"""
    (OUT / "B1_BASELINE_ELIGIBILITY_EXECUTIVE_v1.md").write_text(executive_md, encoding="utf-8")

    alert_md = f"""# EVIDENCE ALERT — B1 source metadata v1

**Status:** OPEN — affected B1 baseline estimation PAUSED.  
**Severity:** CRITICAL for B1 formal baseline eligibility.  
**Class:** SOURCE_PROVENANCE_CONTRADICTION / possible DATA_SCHEMA_DISCREPANCY.  
**Audit ID:** `AUDIT-B1-ELIGIBILITY-v1`.  
**Raw SHA-256:** `{raw_hash}`.  
**Code SHA-256:** `{summary['code']['sha256']}`.

The visible official F data description calls B1 a **real** Pythia training log and assigns it to Question 2 primary fitting. The [EleutherAI Pythia repository]({PYTHIA_README}) says its standard eight sizes trained with fp16 except 1B with bf16. The supplied B1 CSV has both fp16 and bf16 within **each** inferred size trajectory, {total_precision_transitions} transitions total and {total_precision_mismatch}/1,176 rows differing from the official per-size precision if the column denotes training precision. The file also has no `model_repo`, revision, seed, validation-corpus or tokenizer field; `source_manifest.json` names only the Pythia suite, with no row-level original-log URL. This conflicts with a straightforward interpretation of the `precision` metadata in a real training log. It does not by itself prove the `val_loss` column is synthetic or wrong.

**Containment:** No formal B1 N–D Scaling Law estimation or source-internal baseline claim until origin/transformations of B1 rows and Loss definition are documented and precision discrepancy is resolved. Geometric diagnostics are safe to retain as audit evidence. Preserve the raw file unchanged.

**Needed resolution:** Identify whether `precision` is training precision, evaluation precision, or appended/simulated metadata; provide source URI/run/revision for each N trajectory, Pythia version, training data variant, validation set/tokenizer, and any transformation of N, D, `val_loss`, `ppl` and metadata. If nonobserved fields were appended, mark them as derived/augmented and reassess the official “real” classification at column level. Re-run eligibility after reconciliation.
"""
    (OUT / "EVIDENCE_ALERT_B1_SOURCE_METADATA_v1.md").write_text(alert_md, encoding="utf-8")
    print(json.dumps({"verdict": summary["eligibility_verdict"], "rows": len(frame), "precision_mismatch": total_precision_mismatch, "precision_transitions": total_precision_transitions, "out": str(OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
