# Training and tuning design

Python orchestrates a state machine around RLlib rather than embedding research logic
inside algorithms. The CLI resolves a directory into typed settings; the trainer builds
registered components; runtime code performs iterations; evaluation and reporting
produce deterministic, normalized outputs; lifecycle/checkpoint components decide how
execution advances or stops.

Tune reuses this training unit within Ray trials and adds search, scheduling, resource
bundles, continuation, and trial classification. Local artifacts remain durable even
when optional tracking systems fail.

Fresh deterministic evaluation reduces coupling to rollout state, at the cost of
extra environment construction. Parallel evaluation improves throughput but can lag
one update. Stage rebuilds make policy-contract changes explicit; refusing replay
preservation prevents subtly invalid off-policy state.

See [Python responsibilities](python.md) for exact modules.
