"""Bounded read-only probe of Pythia's officially linked public W&B groups.

The official README calls the mapping rough/partial. Any public run values are
comparators, not proof that B1 was derived from those runs.
"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "01_data/raw/real_attachments/B_scaling_laws/pythia_training_log_existing.csv"
OUT = ROOT / "01_data/audits/modeling_phase1/q2"
EXPECTED_HASH = "529a59644b0f57bf3a76037838b614bfedc35e58bb26b93052e34ffc63e454c2"
ENDPOINT = "https://api.wandb.ai/graphql"
README = "https://github.com/EleutherAI/pythia/blob/a19eecb807ec2c79a39ebf18108816e6ffffc1d5/README.md"
RUN_ID = "AUDIT-B1-VALLOSS-R3-20260924-v1"
GROUPS = [
    ("160m", 0.162405, "Pythia 125M_1mpgqyzx"),
    ("1b", 1.040867, "800M Pythia_1zw5etef"),
    ("1.4b", 1.416184, "Pythia 1.3B_lepj8rtx"),
    ("2.8b", 2.782831, "2.7B New_36751euw"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graphql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    request = urllib.request.Request(ENDPOINT, data=payload,
                                     headers={"Content-Type": "application/json",
                                              "User-Agent": "Codex-F2026-source-audit"},
                                     method="POST")
    with urllib.request.urlopen(request, timeout=20) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError(f"W&B public API returned errors: {result['errors'][:1]}")
    return result["data"]


def main() -> None:
    if sha256(RAW) != EXPECTED_HASH:
        raise RuntimeError("B1 raw hash changed")
    b1 = pd.read_csv(RAW)
    rows, group_checks = [], []
    query = ('query($f: JSONString) { project(name:"pythia", entityName:"eleutherai") '
             '{ runs(first:100, filters:$f) { edges { node '
             '{ name displayName group summaryMetrics } } } } }')
    for size, n_params, group in GROUPS:
        result = graphql(query, {"f": json.dumps({"group": group})})
        edges = result["project"]["runs"]["edges"]
        group_checks.append({"size": size, "group": group, "runs_returned": len(edges),
                             "truncated_at_100_possible": len(edges) == 100})
        final_b1 = b1[b1.N_params_B == n_params].sort_values("steps").iloc[-1]
        if int(final_b1.steps) != 143000:
            raise RuntimeError("Unexpected B1 final step")
        for edge in edges:
            node = edge["node"]
            metrics = json.loads(node.get("summaryMetrics") or "{}")
            if "validation/lm_loss" not in metrics or metrics.get("_step", 0) < 143000:
                continue
            uri = f"https://wandb.ai/eleutherai/pythia/runs/{node['name']}"
            rows.append({
                "README_model_label": size, "README_group": group,
                "public_run_id": node["name"], "public_run_display_name": node["displayName"],
                "public_run_uri": uri, "public_run_summary_step": metrics.get("_step"),
                "public_validation_lm_loss": metrics["validation/lm_loss"],
                "public_validation_lm_loss_ppl": metrics.get("validation/lm_loss_ppl", ""),
                "B1_N_params_B": n_params, "B1_step": 143000,
                "B1_final_val_loss": float(final_b1.val_loss),
                "B1_minus_public_validation_loss": float(final_b1.val_loss) - float(metrics["validation/lm_loss"]),
                "proves_same_target": "NO",
            })
    if not rows:
        raise RuntimeError("No public final-step validation metrics found in bounded groups")
    # A tiny second request per distinct candidate run captures only fields
    # relevant to possible validation comparability, never full history.
    config_query = ('query($name: String!) { project(name:"pythia", entityName:"eleutherai") '
                    '{ run(name:$name) { config } } }')
    for row in rows:
        data = graphql(config_query, {"name": row["public_run_id"]})
        config = json.loads(data["project"]["run"]["config"] or "{}")
        def val(key: str):
            item = config.get(key, "")
            return item.get("value", "") if isinstance(item, dict) else item
        for key in ("seed", "seq_length", "eval_iters", "split", "data_path",
                    "valid_data_paths", "vocab_file", "tokenizer_type", "lr", "weight_decay"):
            row["public_config_" + key] = str(val(key))
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "B1_PUBLIC_LOG_PROBE_v1.csv"
    pd.DataFrame(rows).to_csv(target, index=False, encoding="utf-8-sig")
    meta = {
        "audit_id": RUN_ID, "status": "SOURCE_TRACE_NON_FINAL",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)), "B1_sha256": EXPECTED_HASH,
        "primary_readme": README, "public_api_endpoint": ENDPOINT,
        "group_checks": group_checks,
        "candidate_final_step_run_rows": len(rows),
        "output_sha256": sha256(target),
        "limitation": "README gives rough partial W&B group links; group summary cannot prove B1 row provenance",
    }
    (OUT / "B1_PUBLIC_LOG_PROBE_v1.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_id": RUN_ID, "group_checks": group_checks,
                      "candidate_rows": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
