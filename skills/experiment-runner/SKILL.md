---
name: experiment-runner
description: "Implement and run a confirmed F题 model with recorded data, code, config, seed and output lineage."
---

# experiment-runner

## When to use
Use after model-spec yields a CONFIRMED specification and data inputs pass audit.

## Inputs
Read the confirmed specification, processed input hashes, EXPERIMENT_REGISTRY.md and PROJECT_RULES.md.

## Work
Implement in 04_code/, create immutable config and run directory, record environment and random seed, execute the real program, preserve logs and raw results. Do not adjust mathematical definitions to make code run without returning to the decision process.

## Output
An Experiment ID with reproducible config, code entry and hashes, output path, metrics and failures; write raw outputs to 06_results/raw/ and registry rows. Do not mark a result VALIDATED before validation-audit.
