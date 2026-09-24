# B8 mechanism investigation v1

**Run type:** AUDIT RUN, with diagnostic within-cell linear slopes; no formal model experiment.  
**Mechanism classification:** **LIKELY SYNTHETIC RULE EFFECT** (pattern inference, not generator verification).  
**B8 use status:** **QUARANTINED**. Exact generating rule, Q semantics, and Loss comparability remain unresolved.  
**Evidence Alert:** none. The official description does not define a competing B8 formula or an opposite Q coding, so the observed conflict is not a confirmed official-definition contradiction.

## 1. Mapping and provenance before analysis

The 13-page user-supplied F题《数据说明》 identifies B6/B7/B8 on page 3 and lists their question roles; pages 4, 5, 6, 11, and 13 establish the semi-synthetic status, B6 core fields, and the universal N/D units. The PDF is a user-supplied copy and has not been byte-compared with an authenticated platform copy. Its [source record](../../../../00_problem/original/SOURCE_MANIFEST.md) records SHA-256 `f5c851bbe4b3d8c9079609c37f2c3b0835244067711d6d761c66adeaa8357835`; this run verified that hash. The page-edge extra text noted in that source record was excluded from data definitions.

| Official ID | Official description and role | Actual source CSV under `01_data/raw/real_attachments/` | Actual rows/fields | SHA-256 |
|---|---|---|---|---|
| B6 | NQ 半合成实验（360 点）；问题二·质量 Q·基础 | `B_scaling_laws/supplementary_NQ_experiment.csv` | 360 × 5 | `c7450ce0d67d8692535fef4709e60e2da60b2c184738bf96df160a4be0a33a7f` |
| B7 | NQ 半合成实验（450 点）；问题二·质量 Q·扩展 | `B_scaling_laws/supplementary_NQ_experiment_expanded.csv` | 450 × 5 | `880fd265ca3e1d9bc93b4559af7ed7c18f89040634266c50bae03d88486e0f3a` |
| B8 | NQ 半合成实验（1,704 点，含外推）；问题二·质量 Q·大规模 | `B_scaling_laws/supplementary_NQ_experiment_large.csv` | 1,704 × 6 | `bda0d449f75c73bbd04141e5cffbf4bea7002073e34b7fa95a638570fa095ffe` |

All three paths, byte sizes, and hashes match [RAW_SHA256.csv](../../../raw/RAW_SHA256.csv) and `source_manifest.json`. Mapping status is **CONFIRMED for official ID, role, path, evidence type, actual fields, and hash**; **UNRESOLVED for generator and shared Q/Loss semantics**. `N_params_B` and `D_tokens_B` are in billions of parameters/tokens. `experiment_id` encodes the numeric grid but is only a source row label, not evidence of independent training. The common columns are `experiment_id,N_params_B,D_tokens_B,Q_score,val_loss`; B8 adds `data_type`. All required numeric cells are present, N–D–Q keys are unique, exact duplicate rows are absent, and all experiment-ID components match their numeric columns. The official PDF enumerates B6's core fields but does not individually define B7/B8's columns. See [field comparison](B6_B7_B8_FIELD_COMPARISON_v1.csv).

The local `source_manifest.json` describes B6 as “Semi-synthetic, calibrated from Pythia training log + RegMix quality signals.” Its B7 and B8 entries provide byte counts but no generator, seed, transformation, or validation-corpus definition. Targeted search of project code found a prior route-audit reader, not a B8 generator. The public [RegMix repository](https://github.com/sail-sg/regmix) and [Pythia repository](https://github.com/EleutherAI/pythia) describe their original workflows, but neither establishes how this B8 CSV was synthesized.

## 2. Overlap, sampling, and source layers

- **B6 is contained in B7:** all 360 B6 N–D–Q rows appear in B7 with exactly equal `val_loss`. B7 adds Q=0.5 and Q=0.7 across its 45 N–D cells (90 new rows). These files are one nested semi-synthetic family, not 810 independent experiments.
- **B7/B8 exact overlap:** 224 N–D–Q points across 32 N–D cells. Every one of those 224 B8 rows is `calibrated`; no `extrapolated` row overlaps B7. The shared N values stop at 6.9B because B7 uses 11.97B while B8 uses 12B; those two values were not silently equated. B7/B8 share D=10, 50, 150, and 300B tokens.
- **B8 strata:** `calibrated` has 984 rows, 9 N levels (0.07–12B) and 90 N–D cells; `extrapolated` has 720 rows, 6 N levels (20–700B) and 60 cells. Thus the source label is separated by N grid, not a random validation split. All 60 extrapolated cells have 12 Q levels. Of 90 calibrated cells, 78 have 12 Q levels and 12 have only four. Those 12 are N=0.07/0.16/0.41B with D=10/50/150/300B; their Q set is `{0.05,0.5,0.7,0.95}`. This explains why some shared cells have only two matching Q points, while the other 20 shared cells have ten.

## 3. Direction and scale diagnostics

Within each fixed N–D cell, the diagnostic least-squares slope of `val_loss` against `Q_score` is negative in **45/45 B6** and **45/45 B7** cells, but positive in **90/90 calibrated B8** and **60/60 extrapolated B8** cells. The median slopes are −0.339 for B7, +2.028 for calibrated B8, and +1.811 for extrapolated B8. These are descriptive slopes of generated table entries, not estimates of a real quality elasticity. In the 32 shared N–D cells, the two source slopes have opposite signs in **32/32**. B8's Q sequence is nondecreasing in 148/150 cells; B7's is nonincreasing in only 1/45, with local noise around its negative overall trend.

The 224 exactly matched B7/B8 rows have median absolute Loss difference **1.1393**, maximum absolute difference **2.5769**, zero exact matches, and raw Loss correlation **−0.026**. Raw correlation mixes Q and N–D variation, so the within-cell comparison controls the direction claim. At common Q=1, 20 matched points have median signed B8−B7 difference **+0.0017** and median absolute difference **0.0290** (Loss correlation 0.961). At Q=0.1, the 20 matched points have median signed difference **−2.14785**. This near alignment at Q=1 followed by divergence toward lower Q is a specific signature of changed Q response around a similar high-Q anchor; it does not prove the common baseline or the generating formula.

B8 has an exact lower Loss value of **0.5 in 362/1,704 rows (21.2%)**, including **129/984 calibrated (13.1%)** and **233/720 extrapolated (32.4%)**. B6/B7 contain no value at 0.5 (their minima are 2.0161). An exact repeated boundary is consistent with a floor/clipping rule, but only the generator can confirm it. B8's median within-cell linearity R² is 0.997 in calibrated cells and 0.941 in extrapolated cells, another rule-like pattern. Neither summary proves which source columns or calibration parameters were used.

The conflict is specific to Q direction; it is not merely a reversal of all Loss ordering. At fixed Q=0.2 and 0.8, most adjacent N/D increases reduce Loss in both B7 and B8; full counts and group-level diagnostics are in [relation diagnostics](B6_B7_B8_RELATION_DIAGNOSTICS_v1.csv). A counterfactual `1−Q` key reflection finds 204 overlap points and raises raw paired correlation to 0.628, but there are still zero exact Loss matches and median absolute difference 1.2246. This calculation is only a shape diagnostic; no source document authorizes flipping or re-encoding Q.

## 4. Mechanism questions and route decision

| Check | Finding | Status |
|---|---|---|
| Sample overlap / B6 nesting | B6 360/360 exact subset of B7; B7/B8 224 matches all in calibrated layer | CHECKED |
| Same Q definition and direction | Same field name; no shared formula, normalization, or “higher means better” definition supplied for all three | UNRESOLVED |
| Same Loss definition and baseline | B6/B7 overlap exactly; B8 Q=1 values nearly align on 20 shared points, but corpus/tokenizer/checkpoint and calibration baseline are undocumented | UNRESOLVED |
| Same transformation / N–D units | Official universal N/D units match; any B8 Loss or Q transformation is undocumented | PARTIAL |
| Different scenario | B8 `calibrated`/`extrapolated` map to distinct N ranges; opposite Q direction is present already in calibrated layer | CHECKED observed split; causal meaning unresolved |
| Formula / data issue | Strong smooth Q response and 0.5 floor support a synthetic-rule hypothesis; generator, seed, and source calibration records absent | LIKELY pattern; exact cause UNKNOWN |
| Rank-only reversal | All 32 common N–D cells reverse the Q slope; at low Q the absolute Loss gap is large, at Q=1 small | REJECTED as full explanation |
| Q1 interface | No verified map from these semi-synthetic `Q_score` values to A1–A3's eventual descriptive Q or a same-run real quality intervention | NOT ESTABLISHED |

**Classification: LIKELY SYNTHETIC RULE EFFECT.** This is a source-table pattern judgment with moderate confidence. Whether its root cause is an alternative scenario, a different Q definition, or a data issue is **UNKNOWN** because the generating code and definitions are missing. The official file role remains semi-synthetic; no real opposite quality effect is inferred. **B8 remains QUARANTINED** for primary parameters, B6/B7 validation, Q2→Q3 derivatives, and joint estimation. There is no confirmed `DATA_SCHEMA_DISCREPANCY` or new Critical official-definition conflict, so no EVIDENCE_ALERT was opened. DA-01 remains open.

To reassess, obtain the B8 generator with version/seed, input data and calibration fit, explicit Q direction and transformation, Loss corpus/tokenizer/checkpoint, and the rule behind `calibrated`, `extrapolated`, and 0.5. Reproduce the CSV cellwise against the frozen hash or version any corrected table separately. Only then may a reviewer consider B8 as its own alternative-regime stress test. No source CSV was altered, filtered, or recoded in this audit.

## 5. Reproduction and QA

Run `python -X utf8 04_code/data_audit/modeling_phase1_b8_audit.py` from the project root. The script works from its own absolute location, checks all three input hashes and byte sizes before analyzing, uses deterministic computations (random seed: none), and writes the [field CSV](B6_B7_B8_FIELD_COMPARISON_v1.csv), [relation CSV](B6_B7_B8_RELATION_DIAGNOSTICS_v1.csv), and [machine summary](B8_MECHANISM_DIAGNOSTICS_v1.json). Script version is **1.0.0** and SHA-256 for this run is `4c72e942458dc45028f685a0f099db8c2c3735f96567cd4eedf7e1ccf531cdb5`. The CSVs contain 16 field rows and 327 relation rows; the JSON records verified input paths/hashes, code hash, library versions, and group summaries. All reported counts and differences were checked against that run. This is an audit of the three source tables, not a new model fit or an independent validation study.

The execution used the local data-quality audit skill, local PDF extraction, Python CSV/statistical diagnostics, and a targeted check of the two public primary repositories. Firecrawl was unnecessary because ordinary search and direct repository pages supplied the small public-source check; the broad computational-realization workflow applies after a formal mathematical specification, which this data audit does not create. The QA gate checked mapping, input hashes, unique keys, 16/327 output-row counts, core numeric assertions, and local report links.
