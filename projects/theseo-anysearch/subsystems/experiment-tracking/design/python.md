# Python tracking responsibilities

This page maps publication at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/experiments/models.py` owns `MLflowConfig` and experiment selectors.
`theseo_anysearch/experiments/tracking.py` owns disabled/enabled lifecycle, config
flattening, MLflow calls, nesting, warnings, and degraded state.

`theseo_anysearch/rllib/trainer/trainer.py` invokes tracking around training.
`theseo_anysearch/rllib/trainer/reporting/metrics.py` normalizes values,
`tensorboard.py` writes event files, and `theseo_anysearch/rllib/trainer/results.py`
persists local results. `theseo_anysearch/experiments/tune_runner.py` adds parent/trial
relationships and trial-local histories.
