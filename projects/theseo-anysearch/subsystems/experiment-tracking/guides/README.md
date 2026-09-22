# Using experiment tracking

This guide explains how to enable optional tracking without making it a run dependency.
It assumes a valid experiment and writable local output directory. The expected result
is a complete local run plus optional TensorBoard and MLflow views.

1. Keep the resolved experiment and output directory as the authoritative record.
2. Configure an MLflow URI and experiment name only when publication is wanted. With
   no URI, the tracker is intentionally disabled.
3. Launch training/tuning normally; do not use a separate tracking execution path.
4. Open TensorBoard on the emitted local log directory. Use MLflow to search parent
   runs and nested Tune trials when configured.
5. Inspect persisted run metadata for tracking state. `degraded` means publication was
   requested but failed; it does not mean training failed.

For recovery, use local checkpoints, histories, and resolved settings. MLflow's
flattened/truncated parameters cannot reconstruct a run exactly. A missing chart point
may mean the metric was absent, not that its value was zero.
