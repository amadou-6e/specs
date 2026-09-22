# Experiment tracking contract

This page defines disabled, enabled, and degraded tracking behavior. Tracking is
observability, not a precondition for successful learning.

Local run metadata, resolved configuration, metric histories, checkpoints, and other
owned artifacts are written independently of optional MLflow. With no tracking URI,
`MLflowTracker` is a no-op and does not alter run behavior.

When configured, the tracker creates/selects the requested MLflow experiment, opens a
top-level run, and creates nested child runs for Tune trials. It logs flattened
resolved parameters, shared scalar metrics, tags, and artifacts. Parameters omit local
output paths and selected infrastructure/render/tracking blocks; collections are JSON
encoded and values may be truncated. MLflow is therefore not a full-fidelity copy of
the resolved configuration.

All MLflow failures are caught and warned. The tracker records a degraded state and
reason so local run metadata can distinguish disabled tracking from requested tracking
that failed. Training and local persistence continue.

Metrics missing from normalized upstream results are omitted, not recorded as zero.
Parameter immutability and metric step ordering must follow the destination backend's
rules without changing the authoritative local history.
