# Policy explainability contract

This page defines what an explanation means, the provenance required for its inputs,
and conditions that fail rather than produce misleading output.

An explanation identifies the run, checkpoint, observation/action schema, state source,
selected step, action target, feature groups, background, and method parameters. A
replayed or environment-created state is labelled according to its validation source.
A fictional observation is bounds/schema/finiteness checked and labelled
`not_environment_validated`; validation must not imply that it is reachable.

DQN scores are Q-values. PPO scores are policy logits and the report may separately
include critic `state_value`; PPO logits must never be called Q-values. Chosen-versus-
best-safe margin uses the applicable score and current legal-action information.

Trace replay aborts on the first cursor divergence. It must not continue attributing a
state sequence that no longer matches the recorded episode.

Grouped occlusion compares a score with selected feature groups replaced by zeros or a
trace-derived background. Zero means open/empty semantics, not neutral absence.
`auto` uses trace background for multi-step requests and zeros for one step. Explicit
trace/mean backgrounds require at least two observations to avoid degenerate
identically-zero attribution.

Unsupported algorithms, vector actions, malformed scenarios, divergent traces, shape
mismatches, and invalid values fail explicitly. Reports describe sensitivity under a
perturbation, not causal necessity or policy quality.
