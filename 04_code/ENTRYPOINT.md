# Execution entrypoints

Round5 frozen programs: round5_prepare.py (input freeze), round5_fit.py (B1), round5_scenarios.py (valid v3), round5_qa.py (read-only arithmetic audit), visualization/round5_figures.py, round5_package.py. All under04_code/modeling_phase2 unless otherwise noted.

From project root: `python -X utf8 04_code/modeling_phase2/round5_qa.py` safely rechecks saved runs. Frozen inputs and outputs are immutable; fitting/prepare refuse existing run directories. Reproduction requires an isolated copy or a newly registered run/version/config with updated hashes, never deletion/overwrite of the canonical run. Raw attachments are Git-ignored but their SHA manifests and frozen Q2 inputs are versioned.

Dependencies used: Python3.13.14, numpy2.5.1, pandas3.0.3, scipy1.18.0, matplotlib3.11.1. No Q1 refits or Q3 optimization invoked. Code manifest lists current file hashes; initial failure snapshots are retained in failed run directories.

Takeover integrity entry: `python -X utf8 04_code/modeling_phase2/round5_takeover_audit.py`. It verifies saved SHA-256 records and package consistency without fitting or repeating numerical validation. The one-time `--restore-checkout` repair is already recorded and refuses a second execution; normal audits are read-only except their new audit report. `.gitattributes` preserves original mixed CSV newlines and frozen code formats. Do not rerun the old package generator over the documented takeover interface additions.


Round6只读复核：python -X utf8 04_code/modeling_phase3/round6_qa.py。配置Q3_R6_FROZEN_v1.json；core+baseline/scenarios/uncertainty为冻结计算入口，已有Run拒绝覆盖。figure/package脚本只派生图文，不重估参数。依赖同Round5，固定raw/config/source hashes；正式复现须新Run或隔离副本，禁止覆盖现有输出。


Gate4只读证据入口：python -X utf8 04_code/modeling_phase3/gate4_review.py。只检查既有结果/哈希/代表点算术，不调用求解器、Q2拟合或Q4。裁决与接口以GATE4_CONSENSUS_v1和freeze manifest为准。


## Round7 reproducibility

Read frozen specs/config first. Source attachments restored by RAW_SHA256 manifest. Python dependencies numpy,pandas,scipy,matplotlib,pymupdf,pyarrow. Run round7_mapping.py, round7_audit.py to reproduce audit; do not rerun round7_freeze.py on an existing frozen experiment. Numeric entries round7_models.py then round7_forecast.py; they reproduce the fixed run in an isolated checkout. Reports/figures/package then round7_qa.py. No network or Q1–Q3 re-fitting required. Use new experiment ID for changed assumptions/data; never overwrite established evidence as a new run.
