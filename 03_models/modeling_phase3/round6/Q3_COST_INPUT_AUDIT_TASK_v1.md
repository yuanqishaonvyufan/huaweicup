# Q3 targeted cost input audit task

ACTIVE / AUDIT-Q3-COST-R6-20260924-v1。映射见 01_data/audits/modeling_phase3/round6/Q3_OFFICIAL_DATA_ROLE_MATRIX_v1.md/json，原题可见公式见 Q3_OFFICIAL_VISIBLE_SOURCE_v1.json。

目标：核 6ND、eta=.0002、三类 g(Q)、N/D 原始个数到十亿单位转换；区分 PROVIDED 数学代理与实际 OBSERVED 成本。核 C7 max_position_embeddings 与训练长度边界；传入已冻结 Q2 参数及 Q1 支持，不重训。没有真实成本/供给则只用题面代理与显式情景，禁止伪造。下一步完成审计报告和模型规格，先 checkpoint 1 再优化。Q4 不启动。
