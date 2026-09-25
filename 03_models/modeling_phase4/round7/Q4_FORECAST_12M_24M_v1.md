# Q4 12/24-month conditional forecasts v1

Forecast origin **2026-09-25 Asia/Shanghai**, verified clock 2026-09-25 02:20:43 UTC. Last evaluation **2025-03-14**; gap **560 days**. Target is the 28-day q90 of C8 raw six-score average, on 0–100, not the normalized C1 average or absolute record maximum.

| target | central | lower95_conditional | upper95_conditional | horizon_weeks_from_data |
| --- | --- | --- | --- | --- |
| 2027-09-25 | 79.755 | 61.242 | 90.402 | 132.14 |
| 2028-09-25 | 87.128 | 69.58 | 95.569 | 184.43 |

Both horizons are EXTRAPOLATION-DOMINATED; the model extends about 30/42 months beyond last data, despite only nine months of historical coverage. Intervals are conditional on stationary residuals, four-week block and diffusion assumptions; 12/24-month empirical coverage is unavailable. The selected logit mathematical ceiling imposes saturation, not empirically established technological saturation.

CONSERVATIVE / BASELINE / ACCELERATED retain 0 / 0.5 / 1 of positive extrapolated parameter-scale association. Estimated historical S trend is negative, so positive expansion A(h)=0 and all three scenarios collapse. This is a result of the frozen rule; no artificial scenario spread is invented. Full compute slowdown cannot be identified because D and industry resource paths are missing. No claim that technology is immune to compute constraints. Non-scale-proxy future contribution is conditional forecast minus assumed parameter component; residual includes omitted scale and selection.

All-model/scenario forecasts and last-data+12/+24 sensitivities are in forecast_all_models_scenarios.csv. Last-data targets are separate and never replace requested run-date targets. The Q3 51 conditional N/D/Loss paths are saved in Q3_conditional_interface.csv with benchmark_prediction NOT_IDENTIFIED; not used as future industry compute history.

