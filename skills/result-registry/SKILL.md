---
name: result-registry
description: "Maintain the F题 experiment, quantitative result and figure registries with consistent IDs and evidence states."
---

# result-registry

## When to use
Use whenever experiments, result validation or figures are created or revised.

## Inputs
Read EXPERIMENT_REGISTRY.md, RESULTS_REGISTRY.md, FIGURE_REGISTRY.md and source run artifacts.

## Work
Check uniqueness of IDs, active versions, units, source dataset/model/code paths, confidence interval provenance and evidence status. A new version supersedes rather than overwrites an older record. Reject numbers without an actual run or paper numbers lacking a VALIDATED Result ID.

## Output
Updated registries and any inconsistencies recorded in ISSUE_TRACKER.md.
