# Experiment tracking interfaces

This page distinguishes authoritative local artifacts from optional publication
surfaces at product revision `72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

Local training results and status are produced by
`theseo_anysearch/rllib/trainer/results.py` and reporting modules. TensorBoard writing
in `theseo_anysearch/rllib/trainer/reporting/tensorboard.py` stores normalized scalar
series in event files. Tune additionally stores per-trial configuration, JSONL result
history, status, and checkpoints through `theseo_anysearch/experiments/tune_runner.py`.

`theseo_anysearch/experiments/tracking.py` is the MLflow adapter. Its parent run
represents the resolved training/tuning execution; Tune trial runs are nested children.
The adapter's flattened parameters are a searchable summary, not a lossless config
serialization.

Canonical metric names and meanings are referenced from `docs/training/metrics.md`,
`docs/training/custom_metrics.md`, and `docs/training/performance.md`.
