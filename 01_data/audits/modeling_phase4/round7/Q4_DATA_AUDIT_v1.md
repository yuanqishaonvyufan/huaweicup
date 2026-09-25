# Q4 data audit v1

ACTIVE / CHECKED — data audit only, before model fitting.

Official roles and every raw SHA are in Q4_C1_C10_ROLE_MATRIX_v1.json. PDF visible mapping rendered and inspected; near-white margin interference excluded. Raw files are read-only. Main input has 853 exact-ID / parameter-checked C1–C8 records, evaluated 2024-06-16 to 2025-03-14. C9 supplies hub availability and flagged status; no duplicate observations appended.

C1 has 81 ambiguous normalized model IDs (162 rows); excluded rather than choosing the highest score. C2 core numeric cells differ from C1 in last-digit CSV roundoff and are not used as additional observations; exact deviations must be measured in final QA. C3 has 26 historical rows, 23 with average differing from six-dimension mean by >1 point. They are a comparability stress test, excluded from the homogeneous time model. Its 4573 leaderboard rows are another snapshot, not an independent longitudinal panel. No inference of benchmark redesign date from these mixed records.

C8: all 1958 files parsed or failure recorded; 4 truncated files remain untouched. Latest parseable per directory: 1860; six-complete: 1854. Every BBH subtask is extracted and task mean/median/count/std calculated. C10 seven README files remain documentation, not evaluation evidence. C7 TB is not token count and maximum context is not actual training context.

C4 compute/data/open-weight fields are used in macro context and conservative name+parameter matching (96 matches). Token notes, estimated quantities and training-stage ambiguity remain visible. Main sample has only 9 nonmissing D values; some are post-training or estimated. They cannot support a population-wide N–D adjustment. The primary decomposition MUST be called PARAMETER-SCALE ASSOCIATION plus PARAMETER-ADJUSTED RESIDUAL, with D/compute-confounding unresolved. A true scale-versus-non-scale causal percentage is NOT IDENTIFIED.

C6 has 75 unique models; C5 43 IDs are a subset and never doubled. Only seven Pythia rows have high supplied comparability, not independent external provenance. Medium-comparability losses are not pooled into an absolute global bridge.

Snapshot survivorship, name-based family uncertainty, historical license availability and C8 coverage selection persist. The C8 six-raw-score composite is explicitly distinct from C1's normalized leaderboard average; no numeric interchangeability is assumed.

