# Workstream B — B1 baseline eligibility task v1

**STATUS: INITIALIZED / B0 NOT RUN.** 目标是判定 B1 是否可进入来源内 N–D baseline 候选估计；本文件不是 eligibility 已通过的报告。

输入：`01_data/raw/real_attachments/B_scaling_laws/pythia_training_log_existing.csv`，官方 B1，真实 Pythia 训练轨迹；原始 SHA-256 为 `529a59644b0f57bf3a76037838b614bfedc35e58bb26b93052e34ffc63e454c2`。已知基线为 1,176 行、8 个 N 水平、每规模 147 检查点；`run_id` 在原表逐行唯一，不能当独立训练簇。N/D 的 B 为十亿，模型族与验证 Loss 的具体口径仍须核实。

B0 必查：字段/类型/缺失/重复、N/D/Loss 单位与量级、来源/模型版本/验证语料、每条 N 轨迹的 D/step 顺序和重复、固定与变化变量、N–D 覆盖/共线性、`C≈6ND` 量纲、检查点依赖和潜在隐藏组。按真实轨迹/规模建立候选留出，避免随机行切分泄漏；对不可验证的来源口径标限制。

输出到 `01_data/audits/modeling_phase1/q2/B1_BASELINE_ELIGIBILITY_AUDIT_v1.md`，附机器诊断与哈希。报告须给 PASS/CONDITIONAL/FAIL 的具体用途、剩余条件和禁止用途。B0 通过后再冻结来源内 baseline 规格与 processed 输入，登记 Experiment ID，开展透明经典 N–D 候选、参数不确定性/稳定性、残差、整轨迹留出、初值敏感性及适用的 B2/B3/B4/B5 分级检查。当前不加入独立 γ_Q、不与 A 的绝对 Loss 池化、不作最终 Scaling Law。
