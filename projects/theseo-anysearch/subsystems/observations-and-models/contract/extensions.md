# Observation and model extensions

This page defines the obligations of optional encoders and representation packages.
An extension may add a compatible implementation; it may not silently change the
host observation schema.

## Model implementation boundary

A custom RLlib model must declare supported observation keys and shapes, preserve
action-space cardinality, keep the action mask outside learned feature input, and emit
the algorithm-required policy/action-value and value outputs. Unsupported schemas
must fail during construction rather than during a later training batch.

## Representation package boundary

A reusable package must identify its observation schema, architecture, normalization,
output representation, checkpoint contents, and initialization scope. Loading must
verify those fields before applying weights. Absence of the optional package leaves
the base model path usable.

The external [Theseo Model Garden](../../../../theseo-model-garden/README.md) hosts
pretrained packages. This contract governs Anysearch consumption only. Model Garden's
training, qualification, artifact registry, and release lifecycle belong to that
peer project. Research metrics do not promote a package into the stable contract
without an explicit decision.
