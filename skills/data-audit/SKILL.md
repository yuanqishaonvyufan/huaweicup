---
name: data-audit
description: "Audit the F题 A/B/C data by file role, quality, leakage, units and provenance before preprocessing."
---

# data-audit

## When to use
Use before any formal preprocessing or fitting and whenever raw inputs change.

## Inputs
Read DATA_INVENTORY.md, DATA_DICTIONARY.md, DATA_LINEAGE.md, IDENTIFIABILITY_AUDIT_SPEC.md and the required raw files. Treat raw as immutable; stream large xz and C8 JSON instead of assuming they fit memory.

## OFFICIAL_MAPPING_FIRST hard rule
Before classifying, scanning, transforming or modeling a numbered attachment, first write and check its **Official ID → official role/nature → actual relative path → field grain → raw SHA-256** against the user-provided data description's visible body, the on-disk file and RAW_SHA256.csv. Use actual paths when the description and disk differ; record the mismatch explicitly. Never infer A/B/C numbering or experimental role from similar filenames, file size or a previous audit summary. The Phase 1 v1 A18-for-A2/A3 error is a preserved counterexample: A1 is the SlimPajama sample, A2/A3 are the arxiv/github quality extensions, and A18 is optional RegMix source text. Stop dependent conclusions when the mapping or hash cannot be resolved.

## Work
Check completeness, missingness, duplicates, anomalies, units, distributions, correlation or collinearity, leakage and fit/validation/extrapolation roles. Distinguish observed, half-synthetic, interpolated, estimated and mixed sources. For Q/p identifiability, first establish whether quality and Loss are paired at the same run grain; produce the rank, variation, precision, support and held-out evidence required by IDENTIFIABILITY_AUDIT_SPEC.md. Preregister noise-relative precision and support rules before viewing held-out gains, then run 04_code/utils/identifiability_decision.py on the saved audit summary. Keep the PDF's nearly invisible margin text outside official data claims.

## Output
Update DATA_AUDIT.md and DATA_DICTIONARY.md with measured counts, field evidence, the source-backed identifiability branch decision and unresolved issues. A design-level CLOSED P0 does not mean the empirical branch passed. Propose, but do not silently execute, transformations that change data meaning.
