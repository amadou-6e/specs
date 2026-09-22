# Training and tuning interfaces

This page describes the user and artifact boundaries at audited product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

The supported entry point is `anysearch run <experiment-directory>`, optionally with
the tag/options accepted by the run command. The older `anysearch train` and
`anysearch tune` commands in `theseo_anysearch/cli/commands/train.py` and
`theseo_anysearch/cli/commands/tune.py` are explicitly deprecated and must not be the
basis of new runbooks.

Training produces local run metadata, normalized iteration results, TensorBoard event
files, scheduled checkpoints, trajectories, and early-stop state where enabled. Tune
adds parent/search metadata and per-trial configuration, JSONL history, status, and
checkpoints. Artifact paths are part of the resolved run, not a substitute for the
experiment definition.

Canonical metric names are defined by the training metric contract documented in
`docs/training/metrics.md`, `docs/training/custom_metrics.md`, and
`docs/training/performance.md`; tracking backends publish those names but do not define
their semantics.
