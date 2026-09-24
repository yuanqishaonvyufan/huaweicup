---
name: repair-audit
description: "Repair verified F题 paper or code defects and recheck the affected evidence chain while routing core changes through decisions."
---

# repair-audit

## When to use
Use for MODE C after paper-consistency, validation-audit or delivery-audit finds a concrete issue.

## Inputs
Read ISSUE_TRACKER.md, the detection report and affected active artifacts.

## Work
For local reversible defects such as formatting, numbering, broken links or obvious implementation bugs, repair and rerun necessary checks. For mathematical model, key assumption, data meaning, core result or conclusion changes, first open a debate or Decision ID and wait for CONFIRMED specification. Do not relabel an unverified result as validated.

## Output
A repair report with before/after files, rerun IDs, remaining risk and recheck outcome; close the issue only after evidence passes.
