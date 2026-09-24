# B1 Baseline Eligibility Audit v1

**Audit ID:** `AUDIT-B1-ELIGIBILITY-v1`  
**Run class:** AUDIT RUN; no model parameters estimated.  
**Verdict:** **NOT YET ELIGIBLE** for a formal source-internal N–D baseline.  
**Code version/hash:** `1.0.0` / `864686d808ae857a0629d68f1c45d0800f9f3433833f9e4e80c324758ce30a1a`.  
**Raw SHA-256:** `529a59644b0f57bf3a76037838b614bfedc35e58bb26b93052e34ffc63e454c2`.

## 1. Official mapping and grain

The visible body of the user-supplied F data description, pages 3, 10 and 11, assigns **B1** to `B_scaling_laws/pythia_training_log_existing.csv`: Pythia training log, **real**, 1,176 rows × 15 fields, Question 2 primary-fitting input. It defines `N_params_B` as parameter count in billions, `D_tokens_B` as training tokens in billions, `C_FLOPs_1e21` as cumulative FLOPs in 10²¹, and `val_loss` as validation cross entropy. The copied raw file exists at `01_data/raw/real_attachments/B_scaling_laws/pythia_training_log_existing.csv`. Its hash and 111,459 bytes match `RAW_SHA256.csv`; `source_manifest.json` identifies the same path and Pythia suite. **Mapping status: CONFIRMED_OFFICIAL_ID_ROLE_PATH_HASH.** The PDF's faint margin text is excluded from all official claims.

Actual 15 fields: `run_id, N_params_B, D_tokens_B, C_FLOPs_1e21, steps, batch_tokens_M, lr, wd, precision, gpu_days, step_time_ms, train_loss, val_loss, ppl, grad_norm_avg`. The row grain is an inferred model-size × checkpoint observation. `run_id` is unique per row; no field explicitly identifies the training run, repository revision, seed, evaluation corpus, tokenizer, or loss logging recipe. A model-size label below is inferred from the eight N levels and is not an observed B1 identifier.

## 2. Shape and N–D support

There are **1,176 rows**, **8 N levels** (0.070542–11.965825 B), **147 D levels** (0.134–299.893 B tokens), and **1,176 unique N–D pairs**. Every N has 147 D levels; every D has 8 N levels. The full 8 × 147 Cartesian grid is present, with **zero N–D replicate rows**. Natural-log ranges are 5.134 for N and 7.713 for D; Pearson correlation of log N and log D is 5.51e-18. The centered `[1, log N, log D]` *design* has rank 3/3 and condition number 1.664. This establishes geometric independent variation, **not stable scaling-law coefficients**.

No missing values, exact duplicate rows, repeated `run_id`, repeated N–D pairs, or repeated N–step pairs were found. Each inferred size has 147 increasing steps and increasing D values. The 1,176 rows are repeated checkpoints of at most eight observed size trajectories; their residuals and errors must not be treated as 1,176 independent training experiments. No separate seed/replicate is identified. A future validation split must leave out entire N trajectories, with only eight candidate groups.

## 3. Unit and Loss checks

The maximum absolute difference between reported D and `steps × 2,097,152 / 10⁹` is 0.000496 B tokens, consistent with D rounded to three decimals. For `C_FLOPs_1e21`, the ratio to `0.006 × N_params_B × D_tokens_B` has median 1.00000; early C values are rounded to four decimals, so per-row relative errors at very small compute need care. `val_loss` ranges from 2.0933 to 4.7388. It is greater than or equal to `train_loss` in all rows and has 0 increases across the 1,168 adjacent within-size checkpoint intervals. `ppl` agrees with `exp(val_loss)` to median relative error 0.0211% (max 0.0610%). These checks support internal arithmetic and a shared column convention; they do **not** verify the validation corpus, tokenizer, or that values were copied from the original Pythia logs. The official PDF names `val_loss` as validation cross entropy but gives no validation set/version. The table contains no such identifier.

## 4. Source/provenance contradiction and hidden structure

The official data description marks B1 as *real Pythia training trajectories*. The [Pythia primary repository](https://github.com/EleutherAI/pythia/blob/main/README.md#models) states that standard Pythia models were trained with fp16 except the 1B model, which used bf16. In B1, **all eight inferred size trajectories mix fp16 and bf16**; there are **503 within-trajectory precision changes** and **748 rows** disagree with the corresponding official training precision if the field denotes training precision. For example, the 70M trajectory has 96 bf16 rows even though official Pythia 70M used fp16; the 1B trajectory has 49 fp16 rows even though official 1B used bf16. `wd` also varies within every size trajectory (see group CSV), while its exact intended meaning is undocumented. The discrepancy could be mislabeled or augmented metadata, a different meaning of `precision`, or a distinct data compilation; the audit does **not** infer that `val_loss` is fabricated. It requires a row-level provenance explanation.

The same repository documents 154 released checkpoints per model; B1 uses a 147-checkpoint subset starting at step 64. This subset alone is not a contradiction. B1 gives no standard/deduplicated/v0 version, model repository, seed, validation set, or raw logging URI. Thus `val_loss` consistency across sizes remains **UNVERIFIED**, despite its internal `ppl` relation.

## 5. Decision by intended use

| Intended use | Decision | Reason |
|---|---|---|
| N–D geometry and checkpoint-dependence diagnostics | PASS | Complete crossed support and stable row keys; audit only. |
| Formal Pythia source-internal N–D baseline estimation | **FAIL / NOT YET ELIGIBLE** | Training-metadata contradiction and unverified `val_loss` provenance/definition. |
| Infer independent N and D effects from row count alone | FAIL | Only eight size trajectories; no independent seed/replicate metadata. |
| Pool absolute Loss with A or estimate Q elasticity | FAIL | No common target scale or matched quality variation. |

Minimum release condition: trace B1 `val_loss`, N, D, model version, tokenizer/validation corpus and `precision`/`wd` definitions to original logs or a documented transformation; resolve the mismatch in an explicit data contract. Then freeze source-internal baseline specification, preserve an entire-trajectory holdout and disclose the eight-group limitation. No B1 scaling law was fitted in this audit.

## 6. Reproducibility and limits

Run `python 04_code/data_audit/modeling_phase1_b1_audit.py` from the project root or an arbitrary working directory. It refuses unexpected raw/PDF hashes or schema. The script, raw file, official PDF, manifest hashes, numeric checks, group table and verdict are recorded in `B1_ELIGIBILITY_DIAGNOSTICS_v1.json`. All computations are deterministic; random seed is not applicable. The two CSVs are machine-readable audit evidence. Public Pythia documentation is used only to check source claims, not to replace the user-provided official numbering.
