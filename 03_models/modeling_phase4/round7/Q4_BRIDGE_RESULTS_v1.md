# Q4 bridge results v1

Verdict: **NO RELIABLE BRIDGE**. Operational B0. High Pythia n=7, Spearman(-Loss, C6 normalized LB_Average)=0.6071428571428572. Linear LOO RMSE 0.552834 versus mean 0.424448; monotone 0.436635. Both fail frozen held-out criteria. Five small Pythia N values differ from C1 by >2%; exact source-internal B1 Loss and C6 values match all seven final checkpoints, but benchmark revision/loss timestamps and tokenizer alignment are not verified. Strong impossible with one high-comparability family.

Family and temporal holdout NOT IDENTIFIABLE, not passed. Medium strata remain within-family diagnostic curves, never global absolute mapping. C8 raw6 high overlap 7 is insufficient for a separate raw6 bridge. Therefore neither Q2 nor Q3 source Loss is translated into predicted raw6 benchmark. Saved bridge_holdout_predictions, bridge_validation, bridge_residuals and bridge_identity_audit give all model/scale diagnostics.

