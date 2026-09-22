# Experiment tracking design

One normalized training result fans out to local persistence, TensorBoard, optional
MLflow, and Tune trial histories. This avoids backend-specific metric computation and
keeps publication failures outside the learning state machine.

The local run directory is the recovery boundary. TensorBoard provides streaming
visualization; MLflow provides searchable run/trial relationships; Tune owns its trial
status/history. Shared names aid comparison, but their storage and lifecycle differ.

Best-effort MLflow improves robustness for local training but means a successful run
does not imply successful remote publication. The explicit degraded state preserves
that distinction. Lossy parameter flattening is acceptable for search, provided the
full resolved configuration remains authoritative locally.

See [Python responsibilities](python.md) for the module sequence.
