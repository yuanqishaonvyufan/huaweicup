---
name: paper-consistency
description: "Audit F题 paper text, formulas, tables, figures and claims against the active model and validated result registry."
---

# paper-consistency

## When to use
Use on a paper draft or after models/results/figures change.

## Inputs
Read the draft, ACTIVE model specifications, validated result IDs, figure registry, code/config summaries and official paper format rules.

## Work
Check question coverage, formula and notation consistency, units, quantitative citations, chart values, source references, summary claims and model validation. Classify findings P0/P1/P2; distinguish formatting fixes from changes to core mathematics or conclusions.

## Output
A detection report under 10_review/detection_reports/ and issue rows. Do not rewrite a core conclusion without a Decision ID.
