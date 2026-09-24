---
name: validation-audit
description: "Validate F题 model outputs against baselines, errors, sensitivity, uncertainty, extrapolation and feasibility as relevant."
---

# validation-audit

## When to use
Use after an experiment produces raw results and before any paper claim is approved.

## Inputs
Read experiment records, model specification, raw outputs and dataset provenance.

## Work
Select checks by question and explain omissions. Q1 needs scale and conflict checks; Q2 needs source and family validation plus extrapolation caution; Q3 needs feasible region, boundaries and cost sensitivity; Q4 needs bridge error, time/screening stability and forecast uncertainty. Recompute from actual outputs.

## Output
Update 07_validation/VALIDATION_REPORT.md and per-check evidence. Recommend VALIDATED or REJECTED with reasons; result-registry performs final state update.
