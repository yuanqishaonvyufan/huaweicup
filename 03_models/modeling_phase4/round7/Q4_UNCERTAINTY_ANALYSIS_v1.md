# Q4 uncertainty v1

| target | conditional_statistical_PI95 | model_range_NOT_CI | scenario_range_NOT_CI |
| --- | --- | --- | --- |
| 2027-09-25 | [61.24204722669209, 90.40150198993967] | [52.16859687691628, 83.77111309771917] | [79.75536356779305, 79.75536356779305] |
| 2028-09-25 | [69.58018633055818, 95.56880507036963] | [52.33272228155908, 97.11295319946106] | [87.12751211384048, 87.12751211384048] |

A STATISTICAL: 1000 seeded circular four-week residual-block refits plus model-scale Gaussian diffusion SD*sqrt(1+h/4); percentile 2.5/97.5, bounded inverse link. Under explicit stationarity and diffusion assumptions only; process variance over long unobserved horizons is not estimated/validated by the data.

B MODEL: central-prediction range of persistence, linear, logit and local-logit, all preregistered. Model-choice uncertainty is not merged into the statistical PI.

C SCENARIO: retained positive parameter-scale growth 0/.5/1; collapsed because historical scale slope is negative. This scenario class is narrow and does not quantify all possible technical/compute futures. Missing D, source selection, benchmark contamination/redesign and future task relevance are unquantified structural uncertainty. No calibrated probability is attached to the scenario range. An unrestricted evidence-compatible future score could cover the full logical 0–100 range; the reported PI is conditional rather than an identified empirical bound.

Historical family-bootstrap coefficient/endpoint interval does not cover changing frontiers, unknown ancestry or missing D. The model with bounded link avoids >100 but its asymptote is mathematical, not evidence of real saturation.

