# Q4 parameter-scale / residual decomposition v1

ACTIVE restricted descriptive result. Full N–D scale and true non-scale percentages NOT IDENTIFIED: only 9 primary D entries, including post-training and estimates.

| model | start | end | delta_F | delta_S | delta_R | parameter_share | residual_share | beta_logN | time_score_per_year |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N_only | 2024-06-16 | 2025-03-14 | 15.88 | 2.8229 | 13.057 | 0.17777 | 0.82223 | 4.7994 | NA |
| pooled | 2024-06-16 | 2025-03-14 | 15.88 | 2.6541 | 13.226 | 0.16714 | 0.83286 | 4.5123 | 5.1449 |
| family | 2024-06-16 | 2025-03-14 | 15.88 | 2.7032 | 13.176 | 0.17023 | 0.82977 | 4.5959 | 4.574 |

S(t)=beta logN at the SAME two quantile-interpolation records; R(t)=F(t)-S(t), so endpoint changes add exactly. Primary 17.0233% parameter association / 82.9767% residual. This residual includes omitted D, post-training, family composition, selection, noise and possible technology, NOT causal technical progress. The earliest window has only 16 records; changing its definition changes the shares. Family bootstrap conditional coefficient-only share interval: [0.13904913694337953, 0.2300078380513423]; endpoints fixed, not total decomposition uncertainty. Family-controlled row time slope 4.57404 points/year; pooled 5.14488. Same-family time signs differ (Gemma/Yi negative). Full-history descriptive coefficients do not enter rolling forecasting.

Historical endpoint change and fitted temporal slope are distinct: parameter endpoint change +2.70325 points but all-window S slope is -0.0297394 point/week. Neither can be substituted for the other. The residual slope is +0.284911 point/week, but it cannot identify D-adjusted technical progress. N-only/pooled/family endpoint shares are close; screening/window/start sensitivities can reverse the sign.

