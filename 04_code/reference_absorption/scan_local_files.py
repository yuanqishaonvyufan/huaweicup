"""Inventory project files by path, hash, stage, round and artifact role.

This is a file audit, not a claim that every file contains a validated result.
Registered scientific findings are classified separately in the master index.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "10_review"
EXTENSIONS = {".csv", ".json", ".parquet", ".xlsx", ".md", ".png", ".svg", ".pdf", ".py", ".ipynb", ".docx", ".gz", ".zip"}
ROLES = {
    "00_problem": "problem_and_rules", "01_data": "data_and_audit", "02_analysis": "analysis",
    "03_models": "model_and_diagnostics", "04_code": "source_code", "05_experiments": "experiment",
    "06_results": "result_and_figure", "07_validation": "validation", "08_paper": "paper_source",
    "09_handoff": "handoff", "10_review": "review", "11_delivery": "delivery", "tmp": "scratch",
}


def main() -> None:
    rows = []
    for current, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", ".venv", "node_modules"}]
        for name in files:
            path = Path(current) / name
            if path.suffix.lower() not in EXTENSIONS:
                continue
            relative = path.relative_to(ROOT).as_posix()
            group = relative.split("/", 1)[0]
            # Raw model names often contain strings such as "-R1-". They are
            # model revisions, not this project's research rounds.
            if relative.startswith("01_data/raw/"):
                round_name = ""
            else:
                match = re.search(r"(?:round|ROUND)[-_]?([1-7])", relative)
                if match:
                    round_name = "R" + match.group(1)
                else:
                    match = re.search(r"(?:^|[-_/])R([1-7])(?:[-_/]|$)", relative)
                    round_name = "R" + match.group(1) if match else ""
            filename = str(path)
            if os.name == "nt" and not filename.startswith("\\\\?\\"):
                filename = "\\\\?\\" + filename
            digest = hashlib.sha256()
            size = 0
            try:
                with open(filename, "rb") as stream:
                    while chunk := stream.read(8 * 1024 * 1024):
                        digest.update(chunk)
                        size += len(chunk)
                scan_status = "OK"
            except OSError as exc:
                scan_status = f"ERROR:{type(exc).__name__}:{exc}"
            if group == "06_results" and "/raw/" in relative:
                role = "run_output"
            elif group == "06_results" and "/figures/" in relative or path.suffix.lower() in {".png", ".svg"}:
                role = "figure"
            else:
                role = ROLES.get(group, "other")
            rows.append({
                "relative_path": relative,
                "extension": path.suffix.lower(),
                "bytes": size,
                "sha256": digest.hexdigest() if scan_status == "OK" else "",
                "top_level": group,
                "round": round_name,
                "artifact_role": role,
                "formal_result_status": "SEE_MASTER_INVENTORY" if role in {"run_output", "figure", "model_and_diagnostics", "validation"} else "NOT_A_RESULT_BY_PATH_ALONE",
                "scan_status": scan_status,
            })
    rows.sort(key=lambda row: row["relative_path"])
    OUT.mkdir(exist_ok=True)
    with (OUT / "LOCAL_FILE_SCAN_v2.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts = {
        "files": len(rows),
        "bytes": sum(row["bytes"] for row in rows),
        "by_top_level": dict(Counter(row["top_level"] for row in rows)),
        "by_extension": dict(Counter(row["extension"] for row in rows)),
        "by_round": dict(Counter(row["round"] or "unlabeled" for row in rows)),
        "by_role": dict(Counter(row["artifact_role"] for row in rows)),
        "errors": [row["relative_path"] for row in rows if row["scan_status"] != "OK"],
    }
    (OUT / "LOCAL_FILE_SCAN_SUMMARY_v2.json").write_text(json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(counts, ensure_ascii=True))


if __name__ == "__main__":
    main()
