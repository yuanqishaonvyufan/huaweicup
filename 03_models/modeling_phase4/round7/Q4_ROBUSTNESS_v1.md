# Q4 robustness v1

| variant | status | n | parameter_share | target | central |
| --- | --- | --- | --- | --- | --- |
| drop_largest_llama | CHECKED_SENSITIVITY | 574 | 0.16392 | 2027-09-25 | 85.652 |
| drop_largest_llama | CHECKED_SENSITIVITY | 574 | 0.16392 | 2028-09-25 | 92.212 |
| known_families | CHECKED_SENSITIVITY | 607 | -0.15917 | 2027-09-25 | 81.059 |
| known_families | CHECKED_SENSITIVITY | 607 | -0.15917 | 2028-09-25 | 88.245 |
| strict_license | CHECKED_SENSITIVITY | 614 | -0.26817 | 2027-09-25 | 81.709 |
| strict_license | CHECKED_SENSITIVITY | 614 | -0.26817 | 2028-09-25 | 85.93 |
| base_only | CHECKED_SENSITIVITY | 92 | 0.65127 | 2027-09-25 | 5.1135 |
| base_only | CHECKED_SENSITIVITY | 92 | 0.65127 | 2028-09-25 | 2.4685 |
| posttrained_only | CHECKED_SENSITIVITY | 539 | -0.27042 | 2027-09-25 | 65.024 |
| posttrained_only | CHECKED_SENSITIVITY | 539 | -0.27042 | 2028-09-25 | 71.096 |
| start_2024_09 | CHECKED_SENSITIVITY | 702 | -0.75886 | 2027-09-25 | 80.559 |
| start_2024_09 | CHECKED_SENSITIVITY | 702 | -0.75886 | 2028-09-25 | 87.884 |
| window56 | CHECKED_SENSITIVITY | 853 | -0.028285 | 2027-09-25 | 79.862 |
| window56 | CHECKED_SENSITIVITY | 853 | -0.028285 | 2028-09-25 | 87.187 |
| q95 | CHECKED_SENSITIVITY | 853 | 0.18208 | 2027-09-25 | 79.031 |
| q95 | CHECKED_SENSITIVITY | 853 | 0.18208 | 2028-09-25 | 86.084 |
| submission_date | RETROSPECTIVE_TIME_SENSITIVITY_NOT_CAUSAL | 853 | -0.81071 | 2027-09-25 | 82.196 |
| submission_date | RETROSPECTIVE_TIME_SENSITIVITY_NOT_CAUSAL | 853 | -0.81071 | 2028-09-25 | 89.32 |
| release_date_available | INSUFFICIENT_FRONTIER_ENDPOINTS | 101 | NA | NA | NA |
| exclude_Feb_cluster | CHECKED_SENSITIVITY | 557 | 0.17881 | 2027-09-25 | 85.771 |
| exclude_Feb_cluster | CHECKED_SENSITIVITY | 557 | 0.17881 | 2028-09-25 | 92.253 |

**Decomposition NOT STABLE across screening/time definitions.** Known-family, strict-license, later-start and 56-day cases reverse the parameter-share sign. Drop-largest-family forecast changes materially; unknown ancestry and merged-model composition remain unresolved. Base-only and post-trained subsets define different target populations and cannot be treated as uncertainty bounds for the pooled target. Release-date subset has too few eligible frontier endpoints; no fabricated alternate-date forecast. Submission-date sensitivity re-dates later evaluated scores and is explicitly retrospective, not a valid real-time holdout.

| benchmark | delta_F | delta_S | beta_logN | time_score_per_year | frontier_linear_slope_week |
| --- | --- | --- | --- | --- | --- |
| IFEval | 22.344 | 1.5179 | 5.686 | 3.6958 | 0.24522 |
| BBH | 13.815 | 3.8778 | 6.6022 | 1.9035 | 0.15254 |
| MATH Lvl 5 | 34.018 | 2.1243 | 4.1892 | 17.259 | 0.71658 |
| GPQA | 4.7483 | 1.767 | 1.9888 | 1.8284 | 0.060609 |
| MUSR | 2.5265 | 1.9593 | 1.8459 | 0.22056 | 0.054637 |
| MMLU-PRO | 14.481 | 3.7356 | 7.2636 | 2.5371 | 0.25535 |

All six task frontiers improve over the primary endpoints, but magnitude varies strongly (MATH largest). This is broad score improvement, not evidence of causal technology. February 2025 has a large evaluation cluster (204 primary records in one week); exclude-Feb sensitivity remains positive but raises forecasts. C8 coverage is selected, not a random subset of the full open-weight ecosystem.

