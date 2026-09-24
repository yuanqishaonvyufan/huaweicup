"""Round 2 B1 source trace; no N-D baseline is estimated.

Public Pythia configuration files are read at a pinned repository commit.
They serve as provenance comparators, never as a substitute for a B1 row log.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data/raw/real_attachments"
OUT = ROOT / "01_data/audits/modeling_phase1/q2"
PDF = ROOT / "00_problem/original/F_2026_data_description_user_supplied.pdf"
SOURCE_MANIFEST = RAW / "source_manifest.json"
HASH_MANIFEST = ROOT / "01_data/raw/RAW_SHA256.csv"
B1 = RAW / "B_scaling_laws/pythia_training_log_existing.csv"
INDEX = RAW / "B_scaling_laws/pythia_checkpoint_index.csv"
B1_HASH = "529a59644b0f57bf3a76037838b614bfedc35e58bb26b93052e34ffc63e454c2"
PDF_HASH = "f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835"
PYTHIA_COMMIT = "a19eecb807ec2c79a39ebf18108816e6ffffc1d5"
RAW_URL = f"https://raw.githubusercontent.com/EleutherAI/pythia/{PYTHIA_COMMIT}/"
REPO_URL = f"https://github.com/EleutherAI/pythia/tree/{PYTHIA_COMMIT}"
RUN_ID = "AUDIT-B1-PROVENANCE-20260924-v1"

SIZES = [
    ("70m", 0.070542, "70M/pythia-70m.yml", 0.001, "fp16"),
    ("160m", 0.162405, "160M/pythia-160m.yml", 0.0006, "fp16"),
    ("410m", 0.409009, "410M/pythia-410m.yml", 0.0003, "fp16"),
    ("1b", 1.040867, "1B/pythia-1b.yml", 0.0003, "bf16"),
    ("1.4b", 1.416184, "1.4B/pythia-1.4b.yml", 0.0002, "fp16"),
    ("2.8b", 2.782831, "2.8B/pythia-2.8b.yml", 0.00016, "fp16"),
    ("6.9b", 6.86104, "6.9B/pythia-6.9b.yml", 0.00012, "fp16"),
    ("12b", 11.965825, "12B/pythia-12b.yml", 0.00012, "fp16"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Codex-F2026-source-audit"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def find_config_value(content: str, name: str) -> str:
    matches = re.findall(r'"' + re.escape(name) + r'"\s*:\s*([^,\n]+)', content)
    return matches[0].strip() if matches else "NOT_FOUND"


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if sha256(PDF) != PDF_HASH or sha256(B1) != B1_HASH:
        raise RuntimeError("Official PDF or B1 raw hash changed")
    with HASH_MANIFEST.open(encoding="utf-8-sig", newline="") as stream:
        hashes = {r["relative_path"]: r["sha256"] for r in csv.DictReader(stream)}
    if hashes.get("B_scaling_laws/pythia_training_log_existing.csv") != B1_HASH:
        raise RuntimeError("B1 manifest hash mismatch")
    idx_path = "B_scaling_laws/pythia_checkpoint_index.csv"
    if hashes.get(idx_path) != sha256(INDEX):
        raise RuntimeError("Checkpoint index hash mismatch")
    source_manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8-sig"))
    b1_manifest = next(x for x in source_manifest if x.get("file") == "B_scaling_laws/pythia_training_log_existing.csv")
    if "retained from current contest data" not in b1_manifest.get("source", ""):
        raise RuntimeError("B1 source manifest changed; recheck provenance")

    data = pd.read_csv(B1)
    idx = pd.read_csv(INDEX)
    if len(data) != 1176 or len(data.columns) != 15:
        raise RuntimeError("Unexpected B1 shape")
    if len(idx[idx.model_size.isin([x[0] for x in SIZES])]) != 8 * 154:
        raise RuntimeError("Unexpected checkpoint-index shape")

    upstream = []
    for label, n_params, config_path, readme_lr, readme_precision in SIZES:
        url = RAW_URL + "models/" + config_path
        payload = fetch(url)
        content = payload.decode("utf-8")
        upstream.append({
            "size": label, "n_params_B": n_params, "config_url": url,
            "config_sha256": hashlib.sha256(payload).hexdigest(),
            "config_lr": float(find_config_value(content, "lr")),
            "config_weight_decay": float(find_config_value(content, "weight-decay")),
            "config_eval_interval": int(find_config_value(content, "eval-interval")),
            "config_valid_data_path": find_config_value(content, "valid-data-paths"),
            "config_tokenizer_type": find_config_value(content, "tokenizer-type"),
            "config_vocab_file": find_config_value(content, "vocab-file"),
            "readme_lr": readme_lr, "readme_precision": readme_precision,
        })

    official_steps = set(idx[idx.model_size == "70m"].step.astype(int))
    b1_steps = set(data.steps.astype(int))
    excluded_steps = sorted(official_steps - b1_steps)
    if len(b1_steps) != 147 or excluded_steps != [0, 1, 2, 4, 8, 16, 32]:
        raise RuntimeError("B1 checkpoint selection is not the expected 147-step subset")

    rows = []
    for reference in upstream:
        label = reference["size"]
        n_params = reference["n_params_B"]
        group = data[np.isclose(data.N_params_B, n_params, atol=1e-9, rtol=0)].sort_values("steps")
        candidates = idx[idx.model_size == label]
        if len(group) != 147 or set(group.steps) != b1_steps or set(group.steps) - set(candidates.step):
            raise RuntimeError(f"B1 step mapping failed for {label}")
        precision = group.precision.tolist()
        expected = reference["readme_precision"]
        sample_step = 64 if label == "70m" else 1000 if label == "1b" else 143000
        sample_commit = candidates.loc[candidates.step == sample_step, "commit"].iloc[0]
        rows.append({
            "size": label, "N_params_B": n_params, "B1_rows": len(group),
            "candidate_standard_repo": "EleutherAI/pythia-" + label,
            "B1_repo_or_variant_observed": "NO", "B1_original_run_uri_observed": "NO",
            "B1_seed_observed": "NO", "B1_validation_set_observed": "NO",
            "B1_tokenizer_observed": "NO", "B1_loss_extraction_recipe_observed": "NO",
            "B1_steps_match_local_standard_index": len(set(group.steps) & set(candidates.step)),
            "candidate_index_commit_example": sample_commit,
            "candidate_index_example_step": sample_step,
            "B1_fp16_rows": int((group.precision == "fp16").sum()),
            "B1_bf16_rows": int((group.precision == "bf16").sum()),
            "B1_precision_transitions": sum(a != b for a, b in zip(precision, precision[1:])),
            "README_expected_training_precision": expected,
            "B1_precision_mismatch_if_training": int((group.precision != expected).sum()),
            "B1_unique_wd": int(group.wd.nunique()),
            "B1_wd_min": float(group.wd.min()), "B1_wd_max": float(group.wd.max()),
            "pinned_config_weight_decay": reference["config_weight_decay"],
            "B1_unique_lr": int(group.lr.nunique()), "B1_lr": float(group.lr.iloc[0]),
            "pinned_config_lr": reference["config_lr"],
            "README_lr": reference["readme_lr"],
            "pinned_config_eval_interval": reference["config_eval_interval"],
            "pinned_config_valid_data_path": reference["config_valid_data_path"],
            "pinned_config_tokenizer_type": reference["config_tokenizer_type"],
            "pinned_config_vocab_file": reference["config_vocab_file"],
            "pinned_config_url": reference["config_url"],
            "pinned_config_sha256": reference["config_sha256"],
            "Loss_row_level_provenance": "UNKNOWN",
        })

    # Verify a small, prespecified index sample against the public repository
    # metadata API. These calls do not download model weights.
    checks = []
    for model, step in [("70m", 64), ("1b", 1000), ("12b", 143000)]:
        repo = f"EleutherAI/pythia-{model}"
        branch = f"step{step}"
        api_url = f"https://huggingface.co/api/models/{repo}/revision/{branch}"
        upstream_sha = json.loads(fetch(api_url))["sha"]
        local_sha = idx[(idx.model_repo == repo) & (idx.step == step)].commit.iloc[0]
        checks.append({"model_repo": repo, "step": step, "branch": branch,
                       "index_commit": local_sha, "api_commit": upstream_sha,
                       "match": local_sha == upstream_sha, "api_url": api_url})
    if not all(c["match"] for c in checks):
        raise RuntimeError("Local index sample did not match public repository API")

    fields = [
        ("run_id", "SOURCE_ROW_LABEL", "Each row has a unique ID; no training-run ID or seed is encoded"),
        ("N_params_B", "SUPPLIED_CANDIDATE_SIZE", "Numerical sizes map plausibly to Pythia labels; repo variant unknown"),
        ("D_tokens_B", "DETERMINISTIC_DERIVATION_SUPPORTED", "Rounded steps x 2,097,152 / 1e9"),
        ("C_FLOPs_1e21", "DETERMINISTIC_DERIVATION_SUPPORTED", "Approximately 0.006 x N_params_B x D_tokens_B"),
        ("steps", "CHECKPOINT_LABEL_CORROBORATED", "Matches 147 of 154 published standard index labels"),
        ("batch_tokens_M", "ROUNDED_DERIVATION_CANDIDATE", "Around 2.09/2.10 million tokens; source run not verified"),
        ("lr", "UNKNOWN_OR_AUGMENTED", "Constant within each B1 size trajectory and differs from pinned public config"),
        ("wd", "UNKNOWN_OR_AUGMENTED", "Varies within each B1 trajectory; pinned public config has fixed weight decay"),
        ("precision", "UNKNOWN_OR_AUGMENTED", "Switches within every B1 trajectory; meaning not supplied"),
        ("gpu_days", "UNKNOWN", "No row-level original training log or derivation identified"),
        ("step_time_ms", "UNKNOWN", "No row-level original training log or derivation identified"),
        ("train_loss", "UNKNOWN", "No row-level original training log or evaluation recipe identified"),
        ("val_loss", "UNKNOWN_CRITICAL", "Validation corpus/tokenizer/version/checkpoint extraction missing"),
        ("ppl", "DETERMINISTIC_DERIVATION_SUPPORTED", "Numerically agrees with exp(val_loss), so not independent source proof"),
        ("grad_norm_avg", "UNKNOWN", "No row-level original training log or derivation identified"),
    ]
    field_rows = [{"field": f, "lineage_status": status, "basis": explanation,
                   "baseline_use": "BLOCKED_BY_VAL_LOSS_PROVENANCE"} for f, status, explanation in fields]
    write_csv(OUT / "B1_PROVENANCE_MATRIX_v1.csv", rows)
    write_csv(OUT / "B1_FIELD_LINEAGE_v1.csv", field_rows)
    write_csv(OUT / "B1_CHECKPOINT_SAMPLE_VERIFICATION_v1.csv", checks)
    result = {
        "run_id": RUN_ID, "run_class": "AUDIT_RUN_NO_BASELINE_FIT",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)), "b1_sha256": B1_HASH,
        "pdf_sha256": PDF_HASH, "index_sha256": sha256(INDEX),
        "source_manifest_sha256": sha256(SOURCE_MANIFEST),
        "pythia_repository_commit": PYTHIA_COMMIT,
        "pythia_repository_url": REPO_URL,
        "candidate_checkpoint_selection": {"selected_count_per_size": 147,
                                            "published_count_per_size": 154,
                                            "excluded_early_steps": excluded_steps},
        "summary": {"precision_transitions": sum(x["B1_precision_transitions"] for x in rows),
                    "precision_mismatch_if_training": sum(x["B1_precision_mismatch_if_training"] for x in rows),
                    "all_eight_lr_differ_from_pinned_config": all(not math.isclose(x["B1_lr"], x["pinned_config_lr"], rel_tol=1e-9) for x in rows),
                    "all_eight_wd_vary": all(x["B1_unique_wd"] > 1 for x in rows),
                    "public_api_commit_samples_verified": len(checks)},
        "alert_status": "PARTIALLY RESOLVED",
        "eligibility": "NOT YET ELIGIBLE",
        "critical_remaining": ["B1 val_loss lacks original run/revision, validation corpus, tokenizer and extraction recipe",
                               "B1 precision/wd/lr have no documented training-vs-augmented meaning",
                               "B1 standard/deduped/v0 variant and seed are not observed in the table"],
        "caution": "Matching a published step index is not proof that B1 Loss was copied from those checkpoints",
    }
    (OUT / "B1_PROVENANCE_TRACE_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": RUN_ID, **result["summary"], "alert_status": result["alert_status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
