# Evidence map v2 reconciliation for v5

The archived v2 evidence map has 27 claim entries. This check leaves both v1 and v2 unchanged.

- 21 entries match the current Windows working-tree file SHA-256 byte for byte.
- Five Q1 entries E01–E05 differ only because Git checkout converted LF to CRLF. After normalizing CRLF to LF, each file hash matches the v2 recorded SHA-256 and the current Git blob. Their numerical selectors were already verified unchanged by `EVIDENCE_MAP_HASH_REPAIR_v1.json`.
- E20, the Q3 joint-parameter propagation claim, points to the mutable `RESULTS_REGISTRY.md`. Its v2 recorded SHA-256 is `09110cb4ca8cbefb391b554cebd13756c6c79a1e725245c4c1fdc0333e27d6ad`; the current Git blob is `fde8f9a6ee1e5f0b08180462d90fbf8d0fb8e49a697d008173492543c24bded7`. The registry still says 200 joint vectors and 51,000 configurations. More directly, the frozen uncertainty Run's `summary.json` records `joint_draws=200` and `conditional_configurations=51000` (current working-tree SHA-256 `7f1a3addaa94cc33132a68bc2619eff7b45e97b8ea9f7945d1a85f4a3123c666`). Thus E20's registry-file hash is stale while the reported numerical result remains supported by the machine output.

No historical mapping or original model result was rewritten. v5 uses the unchanged numerical result and cites its direct machine source in the scientific interpretation. The 43-Result-ID coverage report separately describes each item's presentation status.
