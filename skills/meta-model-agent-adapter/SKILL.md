---
name: meta-model-agent-adapter
description: Apply the installed meta-model-agent stage protocols and evidence gates to this 2026 GMCM F project without replacing its six-step workflow or directory layout.
---

# meta-model-agent-adapter

Use for stage routing, gate review, rework or resuming this HuaweiCup_F_2026 project. Read PROJECT_RULES.md, META_MODEL_AGENT_ADAPTER.md, 09_handoff/PROJECT_STATE.md and 09_handoff/STAGE_GATES.md first.

Load only the installed meta-model-agent protocol for the active stage, following its progressive loading rule. DISCOVERY maps to problem-intelligence, FORMULATION to model-formulation, COMPUTATION to computational-realization, EVIDENCE to evidence-visualization, SCHEMATICS to systems-diagramming, MANUSCRIPT to manuscript-synthesis and ASSURANCE to delivery-assurance. The project's DATA_AUDIT and VALIDATION gates supplement that sequence.

Run 04_code/utils/stage_gate.py for structural preflight, then inspect substantive evidence before marking a stage complete. A passing script result means READY_FOR_MANUAL_REVIEW, never COMPLETE. Record decisions and downstream invalidations in 09_handoff/ and 10_review/.

Keep 09_handoff/PROJECT_STATE.md as the only active stage state. Do not run the installed Skill's workspace_init.py or stage_executor.py directly in this project: their fixed Chinese runtime paths and state files do not match this layout. Use JOINT COLLABORATION MODE for the first F题 analysis; do not enter formal modeling before the relevant mathematical specification is CONFIRMED.
