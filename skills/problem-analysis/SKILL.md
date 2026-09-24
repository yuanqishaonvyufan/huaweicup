---
name: problem-analysis
description: "Analyze the 2026 GMCM F problem statement into a source-grounded, four-question handoff before model selection."
---

# problem-analysis

## When to use
Use for STEP 1 or a later re-analysis of the official F题 wording.

## Inputs
Read 00_problem/original/F_2026_problem_user_supplied.docx, the visible data description, OFFICIAL_REQUIREMENTS.md, PROBLEM_MAP.md and PROJECT_STATE.md. Check embedded formulas in the DOCX itself.

## Work
For Q1–Q4 describe mathematical nature, variables, objectives, explicit and hidden constraints, uncertainty, dependencies, baseline possibilities, evidence needs and likely failure modes. Mark each statement as official fact, hypothesis or open issue. Use the default Sol build → Opus extend → Sol synthesize → Opus verify cycle in JOINT_COLLABORATION_PROTOCOL.md; the next model reads the previous model's current output. Use independent analysis only when its explicit trigger is recorded.

## Output
A joint STEP 1 handoff and consensus plus proposed updates to PROBLEM_MAP.md, TASK_DEPENDENCY.md and CONSTRAINTS.md. Do not declare a FINAL MODEL or numeric result during initial problem analysis.
