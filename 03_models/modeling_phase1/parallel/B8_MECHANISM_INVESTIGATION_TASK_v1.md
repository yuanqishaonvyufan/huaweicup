# Workstream C — B8 mechanism investigation task v1

**STATUS: INITIALIZED / NOT RUN. B8: QUARANTINED — GENERATION MECHANISM UNDER REVIEW.** 本支线不阻塞 Q1 E1 质量/配比或 B1 N–D 资格审计。

执行依据为 [B8_CONFLICT_INVESTIGATION_PLAN](../../../10_review/B8_CONFLICT_INVESTIGATION_PLAN.md)。先核 B6/B7/B8 的官方角色、实际路径与哈希，再查生成脚本/版本/随机种子、Q 与 Loss 定义和方向、N/D 单位、基线、变换/校准、样本组成；B8 的 `calibrated` 984 与 `extrapolated` 720 分层核查。B6 360 嵌于 B7 450，不双计；224 个共同 N/D/Q 点只是比较锚，不能作独立重复实验。

输出到 `01_data/audits/modeling_phase1/parallel/B8_MECHANISM_INVESTIGATION_v1.md`，结论只能以证据区分 DATA ERROR、DIFFERENT GENERATION REGIME、DIFFERENT DEFINITION、ALTERNATIVE SCENARIO、REAL OPPOSITE EFFECT 或 UNKNOWN；“真实反向效应”尤其需要真实训练证据，不能从半合成方向推出。未查清则保留 QUARANTINE。方向不符合预期不能成为删除理由；机制解释充分后才考虑单独 stress test/alternative regime，不合估主参数。
