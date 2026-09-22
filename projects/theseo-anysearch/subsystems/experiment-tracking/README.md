---
title: Experiment tracking
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
related: []
---

# Experiment tracking

Experiment tracking publishes resolved run facts so executions can be found,
monitored, and compared. Local run artifacts are authoritative; TensorBoard, MLflow,
and Tune indexes are derived views and must never be the sole copy of checkpoints,
configuration, or evidence.

This specification was audited at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`. Tests were inspected, not run, and MLflow
evidence uses mocks rather than a live server.

Training writes local metadata and normalized results regardless of MLflow. TensorBoard
receives the same normalized metric names in local event files. When MLflow is enabled,
it receives a top-level run, nested Tune trial runs, flattened parameters, scalar
metrics, tags, and artifact references. Failures degrade tracking with a recorded
reason while training continues.

Metric meaning belongs to [Training and tuning](../training-and-tuning/README.md), and
trajectory payloads belong to [Trajectory and replay](../trajectory-and-replay/README.md).

## Reading map

- [Contract](contract/README.md)
- [Interfaces](contract/interfaces.md)
- [Configuration](contract/configuration.md)
- [Design](design/README.md)
- [Guide](guides/README.md)
- [Validation](validation.md)
