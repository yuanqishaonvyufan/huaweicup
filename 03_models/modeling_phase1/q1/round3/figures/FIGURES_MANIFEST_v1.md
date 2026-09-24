# Round 3 diagnostic figure manifest

All four figures are **decision diagnostics, not paper figures or validated results**. Generation code: `04_code/modeling_phase1/round3_figures.py`; PNG/source hashes: [machine manifest](FIGURES_MANIFEST_v1.json). Inputs are the frozen Round 3 candidate and A5 response metrics; no A6–A11 Loss was read. Rendered PNGs were visually inspected for labels, clipping and legibility.

| Figure ID | File | Claim / reader task | Data grain |
|---|---|---|---|
| FIG-Q1-R3-001 | [Core spectrum and loadings](FIG-Q1-R3-001_core_spectrum_loadings.png) | Five-signal PC1 explains 48.1%; `ad_en` contributes little | A1 train 40,926 documents, 200 domain-stratified bootstraps |
| FIG-Q1-R3-002 | [Domain normalization](FIG-Q1-R3-002_domain_normalization.png) | DQ3 moves each domain mean near 0.5 by construction, hiding global location | A1 seven domains plus 16,104/193,752 non-overlap A2/A3 records |
| FIG-Q1-R3-003 | [13-domain correlation](FIG-Q1-R3-003_13_domain_correlation.png) | A5 domain response contains positive and negative rank associations | A5 512 training runs × 13 domains, Spearman |
| FIG-Q1-R3-004 | [Response spectrum and loadings](FIG-Q1-R3-004_response_spectrum_loadings.png) | R2 PC1 explains only 22.8%, with uneven domain loadings | A5 512 training runs × 13 domains, 500 run bootstraps |
