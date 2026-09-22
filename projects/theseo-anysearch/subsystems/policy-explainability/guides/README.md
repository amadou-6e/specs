# Explaining a policy decision

This guide describes the safe interpretation workflow. It assumes a supported DQN or
PPO checkpoint and either a replayable trajectory, a valid environment scenario, or a
schema-complete fictional observation. The result is a report about score sensitivity,
not a proof that the policy reasoned correctly.

1. Select the checkpoint and source using the CLI implemented by
   `theseo_anysearch/cli/commands/explain.py`, or launch the interactive command in
   `explain_ui.py`.
2. Prefer replay/environment sources when asking about observed behavior. Use a
   fictional observation only for controlled probes and retain its
   `not_environment_validated` label.
3. Select steps and feature groups, then choose a background. Use trace/mean only with
   at least two observations; remember that zero represents open/empty input.
4. Inspect chosen and best-safe scores using algorithm-correct terminology: Q-values
   for DQN, logits and separate state value for PPO.
5. Preserve the emitted identities and parameters with any conclusion.

Stop if trace replay reports cursor divergence. Do not treat a large attribution as a
causal explanation, and do not compare reports with different backgrounds as though
they used the same reference distribution.
