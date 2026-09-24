---
name: model-spec
description: "Turn a CONFIRMED Sol/Opus consensus for one F题 question into an implementable mathematical specification without changing its logic."
---

# model-spec

## When to use
Use only after the joint Sol/Opus cycle yields a CONFIRMED mathematical specification or Decision ID. A stage-level problem-analysis consensus may leave final model choices OPEN; that does not authorize formal implementation.

## Inputs
Read the relevant 03_models/q*/MODEL_INTERFACE.md, consensus, decision log and data audit.

## Work
Specify variables, indices, units, objective or response relation, constraints, assumptions, estimation, identifiability, domain and validation. Separate mathematical model from solver algorithm. If a source is ambiguous, mark OPEN and return it to the debate instead of deciding in code.

## Output
Versioned specification in 03_models/q*/ with source IDs and acceptance checks; update ACTIVE state only through DECISION_LOG.md.
