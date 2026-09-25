# Q4 rolling-origin validation v1

Selected logit-linear by equal-horizon MAE; persistence not within 5% of best.

| model | horizon_weeks | MAE | RMSE | coverage95 | n |
| --- | --- | --- | --- | --- | --- |
| linear | 4 | 1.7635 | 2.0728 | 1 | 20 |
| linear | 13 | 1.5644 | 1.6643 | 1 | 11 |
| local_logit | 4 | 1.9146 | 2.6512 | 0.8 | 20 |
| local_logit | 13 | 2.8674 | 3.4466 | 1 | 11 |
| logit | 4 | 1.7566 | 2.0744 | 1 | 20 |
| logit | 13 | 1.5293 | 1.6148 | 1 | 11 |
| persistence | 4 | 1.9957 | 2.5068 | 1 | 20 |
| persistence | 13 | 3.6833 | 4.1104 | 1 | 11 |

Minimum 16 weekly endpoints. 26/52-week validation unavailable, not passed. All target windows use evaluation dates <= endpoint and dynamic fits only use observations through origin. Overlapping windows and folds are dependent. Current snapshot/license screening and latest revisions imply retrospective pseudo-out-of-sample; not a live historical leaderboard recreation. Validation is reused for model selection; no independent final test or post-selection interval guarantee. Fixed-midpoint AIC does not favor a break (45.61 linear vs47.50 broken); this short/dependent series has low break-detection power.

