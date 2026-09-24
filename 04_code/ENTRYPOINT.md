# Execution entrypoints

Round5 frozen programs: round5_prepare.py (input freeze), round5_fit.py (B1), round5_scenarios.py (valid v3), round5_qa.py (read-only arithmetic audit), visualization/round5_figures.py, round5_package.py. All under04_code/modeling_phase2 unless otherwise noted.

From project root: `python -X utf8 04_code/modeling_phase2/round5_qa.py` safely rechecks saved runs. Frozen inputs and outputs are immutable; fitting/prepare refuse existing run directories. Reproduction requires an isolated copy or a newly registered run/version/config with updated hashes, never deletion/overwrite of the canonical run. Raw attachments are Git-ignored but their SHA manifests and frozen Q2 inputs are versioned.

Dependencies used: Python3.13.14, numpy2.5.1, pandas3.0.3, scipy1.18.0, matplotlib3.11.1. No Q1 refits or Q3 optimization invoked. Code manifest lists current file hashes; initial failure snapshots are retained in failed run directories.
