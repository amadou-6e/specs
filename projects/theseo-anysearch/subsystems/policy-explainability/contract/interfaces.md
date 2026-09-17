# Policy-explainability interfaces

The backend Python API and CLI select checkpoints, trajectories/states, algorithms,
targets, feature groupings, and output locations. DQN explains Q-values; PPO explains
the documented policy score without pretending both targets are identical.

See [CLI](../../../rllib/explain/cli.md) and
[policy attribution](../../../rllib/explain/policy-attribution.md).
