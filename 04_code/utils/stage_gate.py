"""Structural preflight for the project's meta-model-agent stage mapping.

This checker never declares mathematical or paper quality complete. A passing
run means that the expected evidence files exist and need substantive review.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


def file_check(root: Path, relative: str) -> dict:
    path = root / relative
    return {
        "check": "file",
        "target": relative,
        "pass": path.is_file() and path.stat().st_size > 0,
    }


def glob_check(root: Path, pattern: str, minimum: int = 1) -> dict:
    matches = [p for p in root.glob(pattern) if p.is_file() and p.stat().st_size > 0]
    return {
        "check": "glob_min",
        "target": pattern,
        "minimum": minimum,
        "found": len(matches),
        "pass": len(matches) >= minimum,
    }


def alternative_globs_check(root: Path, patterns: list[str], minimum: int = 1) -> dict:
    matches = {
        p
        for pattern in patterns
        for p in root.glob(pattern)
        if p.is_file() and p.stat().st_size > 0
    }
    return {
        "check": "alternative_globs_min",
        "target": patterns,
        "minimum": minimum,
        "found": len(matches),
        "pass": len(matches) >= minimum,
    }


def csv_rows_check(root: Path, relative: str, minimum: int) -> dict:
    path = root / relative
    rows = 0
    if path.is_file():
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = sum(1 for _ in csv.DictReader(stream))
    return {
        "check": "csv_rows_min",
        "target": relative,
        "minimum": minimum,
        "found": rows,
        "pass": rows >= minimum,
    }


def empty_dir_check(root: Path, relative: str) -> dict:
    path = root / relative
    return {
        "check": "empty_dir",
        "target": relative,
        "pass": path.is_dir() and not any(path.iterdir()),
    }


def register_rows_check(root: Path, relative: str) -> dict:
    path = root / relative
    count = 0
    if path.is_file():
        count = sum(
            line.startswith("|") and not line.startswith("|---")
            for line in path.read_text(encoding="utf-8").splitlines()
        )
    return {
        "check": "markdown_table_has_data_row",
        "target": relative,
        "found": max(0, count - 1),
        "pass": count >= 2,
    }


def checks_for_stage(root: Path, stage: str) -> list[dict]:
    f = lambda relative: file_check(root, relative)
    g = lambda pattern, minimum=1: glob_check(root, pattern, minimum)
    r = lambda relative: register_rows_check(root, relative)
    if stage == "INITIALIZATION":
        checks = [
            f("README.md"),
            f("PROJECT_RULES.md"),
            f("META_MODEL_AGENT_ADAPTER.md"),
            f("00_problem/OFFICIAL_REQUIREMENTS.md"),
            f("00_problem/EXTERNAL_ADVICE.md"),
            f("00_problem/PROBLEM_MAP.md"),
            f("01_data/DATA_AUDIT.md"),
            f("09_handoff/PROJECT_STATE.md"),
            f("09_handoff/STAGE_GATES.md"),
            f("09_handoff/NEXT_ACTION.md"),
            f("09_handoff/JOINT_CONTEXT.md"),
            f("09_handoff/JOINT_CONTEXT_v1.md"),
            f("02_analysis/consensus/JOINT_COLLABORATION_PROTOCOL.md"),
            f("02_analysis/consensus/JOINT_WORK_LOG.md"),
            g("00_problem/original/*", 7),
            g("skills/*/SKILL.md", 13),
            csv_rows_check(root, "01_data/raw/RAW_SHA256.csv", 2012),
            empty_dir_check(root, "05_experiments/runs"),
            empty_dir_check(root, "06_results/validated"),
        ]
    elif stage == "DISCOVERY":
        checks = [
            f("09_handoff/JOINT_CONTEXT_v1.md"),
            f("02_analysis/sol/SOL_F_PROBLEM_ANALYSIS_v1.md"),
            f("02_analysis/opus/OPUS_F_EXTENSION_v1.md"),
            f("02_analysis/consensus/JOINT_F_PROBLEM_SYNTHESIS_v1.md"),
            f("02_analysis/cross_review/JOINT_F_PROBLEM_REVIEW_v1.md"),
            f("02_analysis/consensus/CONSENSUS_F_PROBLEM_ANALYSIS_v1.md"),
            r("02_analysis/consensus/JOINT_WORK_LOG.md"),
            f("00_problem/PROBLEM_MAP.md"),
            f("00_problem/TASK_DEPENDENCY.md"),
            f("00_problem/CONSTRAINTS.md"),
        ]
    elif stage == "DATA_AUDIT":
        checks = [
            f("01_data/DATA_INVENTORY.md"),
            f("01_data/DATA_DICTIONARY.md"),
            f("01_data/DATA_AUDIT.md"),
            f("01_data/IDENTIFIABILITY_AUDIT_SPEC.md"),
            f("04_code/utils/identifiability_decision.py"),
            f("01_data/PREPROCESSING_LOG.md"),
            g("01_data/processed/**/*", 1),
        ]
    elif stage == "FORMULATION":
        checks = [
            g("02_analysis/consensus/CONSENSUS_v*.md", 1),
            g("03_models/q1/MODEL_SPEC_v*.md", 1),
            g("03_models/q2/MODEL_SPEC_v*.md", 1),
            g("03_models/q3/MODEL_SPEC_v*.md", 1),
            g("03_models/q4/MODEL_SPEC_v*.md", 1),
            f("09_handoff/DECISION_LOG.md"),
        ]
    elif stage == "COMPUTATION":
        checks = [
            alternative_globs_check(root, [f"04_code/{q}/*.{ext}" for ext in ("py", "R", "m", "jl")])
            for q in ("q1", "q2", "q3", "q4")
        ] + [
            f("04_code/ENTRYPOINT.md"),
            f("04_code/code_manifest.json"),
            g("05_experiments/runs/**/*", 1),
            g("06_results/raw/**/*", 1),
            r("05_experiments/EXPERIMENT_REGISTRY.md"),
            r("06_results/RESULTS_REGISTRY.md"),
        ]
    elif stage == "VALIDATION":
        checks = [
            f("07_validation/VALIDATION_REPORT.md"),
            g("06_results/validated/**/*", 1),
            r("06_results/RESULTS_REGISTRY.md"),
        ]
    elif stage == "EVIDENCE":
        checks = [
            g("06_results/figures/**/*", 1),
            r("06_results/FIGURE_REGISTRY.md"),
            alternative_globs_check(
                root, [f"04_code/visualization/*.{ext}" for ext in ("py", "R", "m", "jl")]
            ),
        ]
    elif stage == "MANUSCRIPT":
        checks = [
            f("08_paper/PAPER_STATE.md"),
            alternative_globs_check(root, ["08_paper/latex/*.tex", "08_paper/word/*.docx"]),
            g("08_paper/references/**/*", 1),
        ]
    elif stage == "ASSURANCE":
        checks = [
            g("11_delivery/paper/*.pdf", 1),
            g("11_delivery/final_check/*REPORT*.md", 1),
            f("11_delivery/final_check/DELIVERY_CHECKLIST.md"),
        ]
    else:
        raise ValueError(f"Unknown stage: {stage}")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--stage",
        required=True,
        choices=[
            "INITIALIZATION", "DISCOVERY", "DATA_AUDIT", "FORMULATION",
            "COMPUTATION", "VALIDATION", "EVIDENCE", "MANUSCRIPT", "ASSURANCE",
        ],
    )
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    root = args.workspace.resolve()
    checks = checks_for_stage(root, args.stage)
    passed = all(item["pass"] for item in checks)
    report = {
        "workspace": str(root),
        "stage": args.stage,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "structural_status": "READY_FOR_MANUAL_REVIEW" if passed else "MISSING_STRUCTURE",
        "manual_review_required": True,
        "upstream_stages_checked": False,
        "completion_decision": "NOT_MADE_BY_PREFLIGHT",
        "checks": checks,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
