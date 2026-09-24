# TABLE-Q1-R4-004 A7 逐域验证

| 验证域 | M1 RMSE↓ | M1/M0 RMSE↓ | 运行排序 ρ |
|---|---|---|---|
| pubmed_abstracts | 0.2626 | 0.460 | 0.923 |
| pile_cc | 0.1532 | 0.478 | 0.902 |
| uspto_backgrounds | 0.2725 | 0.534 | 0.848 |
| wikipedia_en | 0.2957 | 0.541 | 0.878 |
| hackernews | 0.1900 | 0.565 | 0.843 |
| gutenberg_pg_19 | 0.2564 | 0.571 | 0.890 |
| pubmed_central | 0.5312 | 0.632 | 0.829 |
| ubuntu_irc | 0.6487 | 0.649 | 0.763 |
| github | 0.6129 | 0.649 | 0.835 |
| freelaw | 0.4806 | 0.651 | 0.771 |
| stackexchange | 0.4487 | 0.664 | 0.818 |
| arxiv | 0.5888 | 0.739 | 0.738 |
| dm_mathematics | 1.1605 | 0.754 | 0.763 |

注：比率 <1 表示 A7 M1 比 M0 误差小；13 域必须与 R0 并报。来源：P_RESPONSE_DOMAIN_VALIDATION_v2.csv。
