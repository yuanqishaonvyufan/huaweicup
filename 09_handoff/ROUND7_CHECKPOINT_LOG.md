# Round7 checkpoint log

Run date: 2026-09-25 Asia/Shanghai. Forecast targets: 2027-09-25 and 2028-09-25.

Preflight: preserved local R6 receipt patch at ../round6_local_checkpoint_preserved.patch; its content already exists on latest main. Fast-forwarded main to Gate4 PASS 3562c1294f4355edfa6e5ac13a7724f25fbcef26. Windows Schannel trust failed; git per-command OpenSSL backend succeeds with TLS verification enabled.

CP0: state recovery and C1–C10 official mapping. Checkpoint receipt hashes recorded after each remote verification; next commit persists prior receipt.

CP0 VERIFIED: 9c54c3e43aba7fbac38fa01142005d96a73bd212 = remote refs/heads/main.

CP1 VERIFIED: f3f0a4e0dc34782a9f0a00da42fc21a85ca4ce4f = remote main.
CP2 VERIFIED: 10c30f90549fe85f9ef298d9e965c651dc887e50 = remote main. Numerical outputs complete. Markdown generation lacked optional tabulate; replaced with deterministic local formatter at CP3, no model rerun.
CP3: run-date 12/24 forecasts, separate uncertainty and robustness completed.


CP3 VERIFIED: cc34495a2b1902b3a84adde8241847443161ac44 = remote main.

CP4 ready: paper-ready Q4,42/42 QA,8 figures,7 tables,registries and final-modeling handoff. Final receipt will record verified CP4 hash. Numerical outputs retained; Q3 derived copy corrected for exact decimal preservation only.
