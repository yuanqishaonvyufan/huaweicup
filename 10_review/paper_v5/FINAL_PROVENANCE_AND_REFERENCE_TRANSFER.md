# v5 numerical provenance and reference-paper transfer

The user-designated v3 DOCX is preserved as `08_paper/v5/baseline_v3_user.docx` with SHA-256 `a34984fbefd0f4488f8b2ce94beff34e9e0c599df4eaf48b531ea46eda446353`. The 32-page reference-transfer manuscript remains a separate pre-draft. v5 was rebuilt from the preserved v3 on every checkpoint. The original Q1–Q4 models, parameters, and machine result files were not rewritten; comparison with the `7b8990a` recovery point shows only four newly added supplementary visualization Run directories under `06_results/raw`.

|v5 quantitative content|Local machine evidence used|Boundary retained|
|---|---|---|
|Q1 22-item scoring, A1/A2/A3, seven-domain ranking|Q1 task-repair domain and rank tables; fixed six-pair correlation scan|Constructed score and within-system replication, not observed training gain|
|Q1 1M validation and larger-scale failure|Frozen A6–A11 response validation outputs; A12–A15 estimated extrapolation table|1M local relation; larger tables are partial transfer or estimates|
|Q2 law, holdouts, marginal effects, bootstrap|B1 five-parameter summary, three validation designs, marginal effects, 200 whole-trajectory draws|Attachment-internal Loss; bootstrap does not cover external sources|
|Q2 quality and mixture scenarios|B7 semi-synthetic quality cells; inherited A-source mixture diagnostics|Conditional coefficients, not a fitted unified quality law|
|Q3 51 budgets, active sets, cost shares, shadow price|Frozen budget path and summary, quality break-even, five context scenarios, uncertainty and shadow-price outputs|Problem FLOPs proxy and B1 statistical support; scenario envelopes are not CIs|
|Q4 frontier, tasks, bridge, family, rolling validation|Frozen C8/C1 frontier results, six-task endpoint table, bridge validation, family variants, rolling metrics|Descriptive parameter association; bridge fails; only 4/13-week validation|
|Q4 two-date positive-reference slowdown figure|Q4 task-repair scenario table and summary|Fixed D and C≈6ND exogenous benchmark-space scenario, not identified real compute effect|

The new Q1–Q4 figures have independent visualization Run manifests with input, script, and output SHA-256 checks. Final QA rechecked all four manifests, all 37 contents entries, 25 numbered figures, 20 numbered body tables, three appendix tables, 28 numbered equations, and preservation of every embedded media byte from the v3 source. The five older Q1 evidence-map hash repairs are retained as history; a separate reconciliation records one stale registry-file hash for Q3 while verifying the unchanged number against its direct machine summary.

The reference PDF contributed the question-by-question reasoning order, formula-before-and-after explanations, result charts tied to a claim, a concentrated validation/sensitivity section, and a limitation-to-future-data structure for model improvement. It contributed no parameter, RMSE/R², quality factor, mixture optimum, Q3 configuration, reliable bridge claim, 12%/88% split, or forecast value. The new figures were redrawn from this project's stored outputs; no reference image or PDF numerical result was copied into v5.
