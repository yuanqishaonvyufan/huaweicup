"""Check completeness of the reference and local-evidence audit package."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "10_review"
REFERENCE = Path(r"D:\work document\codex_work\f_reference_transfer\reference_pdf")
BASELINE = Path(r"D:\work document\codex_work\f_reference_transfer\baseline_v3\extract")


def rows(name: str) -> list[dict]:
    with (AUDIT / name).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference_pdf", type=Path)
    parser.add_argument("baseline_v3_docx", type=Path)
    args = parser.parse_args()
    reference = json.loads((REFERENCE / "structure_counts.json").read_text(encoding="utf-8"))
    text_inventory = json.loads((REFERENCE / "text_inventory.json").read_text(encoding="utf-8"))
    v3 = json.loads((BASELINE / "v3_structure_counts.json").read_text(encoding="utf-8"))
    files = json.loads((AUDIT / "LOCAL_FILE_SCAN_SUMMARY_v2.json").read_text(encoding="utf-8"))
    captions, decisions, results, file_rows = (
        rows("REFERENCE_FIGURE_TABLE_INVENTORY_v1.csv"),
        rows("REFERENCE_TRANSFER_DECISIONS_v2.csv"),
        rows("LOCAL_EVIDENCE_MASTER_INVENTORY_v2.csv"),
        rows("LOCAL_FILE_SCAN_v2.csv"),
    )
    checks = {
        "reference_pdf_sha": hashlib.sha256(args.reference_pdf.read_bytes()).hexdigest() == text_inventory["sha256"],
        "reference_29_pages": reference["physical_pages"] == text_inventory["pages"] == 29,
        "reference_20_figures": reference["figure_count"] == sum(x["Kind"] == "Figure" for x in captions) == 20,
        "reference_11_tables": reference["table_count"] == sum(x["Kind"] == "Table" for x in captions) == 11,
        "reference_54_equations": reference["numbered_equation_count"] == 54,
        "reference_8_citations": reference["reference_count"] == 8,
        "reference_all_pages_extracted": all((REFERENCE / f"page_{p:02d}.txt").is_file() for p in range(1, 30)),
        "reference_figure_table_decisions": len([x for x in decisions if x["Reference item ID"].startswith(("F", "T"))]) == 31,
        "forbidden_transfer_rows": sum(x["Decision"] == "REJECT_RESULT_TRANSFER" for x in decisions) == 5,
        "no_reference_results_copied": all(x["Decision"] == "REJECT_RESULT_TRANSFER" for x in decisions if x["Transfer type"] == "RESULT — FORBIDDEN"),
        "v3_34_pages": v3["physical_pages"] == 34,
        "v3_9_figures_16_main_tables_24_equations": (v3["figure_count"], v3["main_table_count"], v3["numbered_equation_count"]) == (9, 16, 24),
        "v3_docx_present": args.baseline_v3_docx.is_file(),
        "registered_43": len(results) == len({x["result_id"] for x in results}) == 43,
        "registered_q4_restricted": sum(x["evidence_status"] == "VALIDATED_FOR_RESTRICTED_REPORTING" for x in results) == 8,
        "registered_repair_runs": {x["result_id"] for x in results if "-REPAIR-" in x["result_id"]} == {"Q1-REPAIR-001", "Q1-REPAIR-002", "Q4-REPAIR-001", "Q4-REPAIR-002"},
        "all_result_sources_present": all((ROOT / x["source_artifact"]).is_file() for x in results),
        "all_files_hashed": files["files"] == len(file_rows) and not files["errors"] and all(x["scan_status"] == "OK" for x in file_rows),
        "required_reports_present": all((AUDIT / name).is_file() for name in ("REFERENCE_PAPER_DEEP_STRUCTURE_AUDIT_v1.md", "PAPER_EXPANSION_OPPORTUNITY_MAP_v1.md")),
    }
    failed = [name for name, passed in checks.items() if not passed]
    report = {"status": "PASS" if not failed else "FAIL", "passed": len(checks) - len(failed), "total": len(checks), "failed": failed, "reference_sha256": text_inventory["sha256"], "baseline_v3_sha256": hashlib.sha256(args.baseline_v3_docx.read_bytes()).hexdigest(), "file_scan_count": files["files"]}
    (AUDIT / "REFERENCE_ABSORPTION_STAGE1_QA_v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
