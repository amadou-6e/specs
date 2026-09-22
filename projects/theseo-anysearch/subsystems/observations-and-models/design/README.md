# Observation and model design

Observation data flows from native sampling through a typed Python conversion boundary
into RLlib models. Native code performs world-local sampling; Python declares spaces,
owns normalization, and reuses preallocated arrays; the model separates spatial,
auxiliary, and mask paths before producing policy and value outputs.

Keeping normalization at the policy boundary permits editors and explainers to retain
raw categories while models see bounded numeric arrays. Keeping masks outside the
encoder prevents legality from becoming an accidental shortcut feature. Preserving
spatial tensors through the convolutional encoder avoids the directional information
loss caused by global pooling.

Single-agent and multi-agent schemas are separate rather than forced through one
lowest-common-denominator representation. This improves expressiveness but requires
explicit model compatibility checks.

See [Python responsibilities](python.md). Native sampling is owned by the environment
runtime; its observation bridge is cited in the interface contract.
