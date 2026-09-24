---
name: handoff-builder
description: "Maintain one shared F题 research context and compact task-specific Sol/Opus handoffs during sequential joint collaboration."
---

# handoff-builder

## When to use
Use at stage transitions, material decisions or after validated results change.

## Inputs
Read JOINT_CONTEXT.md, PROJECT_STATE.md, DECISION_LOG.md, OPEN_QUESTIONS.md, JOINT_WORK_LOG.md and active evidence. In default joint mode, the next model must receive the preceding model's latest saved contribution. Apply isolation only to a specifically triggered independent review.

## Work
Update the single shared context with confirmed definitions, current data/model versions, both models' latest contributions, validated results, disputes and the next task. Keep SOL_CONTEXT.md and OPUS_CONTEXT.md limited to their current model-specific assignment. Separate CONFIRMED, DATA_AUDIT_REQUIRED, CANDIDATE, OPEN, REJECTED and FALLBACK, and include source IDs instead of whole chat histories.

## Output
Update JOINT_CONTEXT.md, PROJECT_STATE.md, the task-specific SOL_CONTEXT.md and OPUS_CONTEXT.md, JOINT_WORK_LOG.md and NEXT_ACTION.md; use HANDOFF_TEMPLATE.md for a stage package.
