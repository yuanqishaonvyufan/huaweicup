# EVIDENCE ALERT — B1 source metadata v1

**Status:** OPEN — affected B1 baseline estimation PAUSED.  
**Severity:** CRITICAL for B1 formal baseline eligibility.  
**Class:** SOURCE_PROVENANCE_CONTRADICTION / possible DATA_SCHEMA_DISCREPANCY.  
**Audit ID:** `AUDIT-B1-ELIGIBILITY-v1`.  
**Raw SHA-256:** `529a59644b0f57bf3a76037838b614bfedc35e58bb26b93052e34ffc63e454c2`.  
**Code SHA-256:** `864686d808ae857a0629d68f1c45d0800f9f3433833f9e4e80c324758ce30a1a`.

The visible official F data description calls B1 a **real** Pythia training log and assigns it to Question 2 primary fitting. The [EleutherAI Pythia repository](https://github.com/EleutherAI/pythia/blob/main/README.md#models) says its standard eight sizes trained with fp16 except 1B with bf16. The supplied B1 CSV has both fp16 and bf16 within **each** inferred size trajectory, 503 transitions total and 748/1,176 rows differing from the official per-size precision if the column denotes training precision. The file also has no `model_repo`, revision, seed, validation-corpus or tokenizer field; `source_manifest.json` names only the Pythia suite, with no row-level original-log URL. This conflicts with a straightforward interpretation of the `precision` metadata in a real training log. It does not by itself prove the `val_loss` column is synthetic or wrong.

**Containment:** No formal B1 N–D Scaling Law estimation or source-internal baseline claim until origin/transformations of B1 rows and Loss definition are documented and precision discrepancy is resolved. Geometric diagnostics are safe to retain as audit evidence. Preserve the raw file unchanged.

**Needed resolution:** Identify whether `precision` is training precision, evaluation precision, or appended/simulated metadata; provide source URI/run/revision for each N trajectory, Pythia version, training data variant, validation set/tokenizer, and any transformation of N, D, `val_loss`, `ppl` and metadata. If nonobserved fields were appended, mark them as derived/augmented and reassess the official “real” classification at column level. Re-run eligibility after reconciliation.
