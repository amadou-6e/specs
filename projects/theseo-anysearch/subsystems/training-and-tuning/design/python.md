# Python training responsibilities

This page maps execution modules at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.

`theseo_anysearch/cli/commands/train.py` and `tune.py` retain deprecated command
surfaces; the current run command resolves experiment settings represented by
`theseo_anysearch/experiments/models.py` and `theseo_anysearch/settings/training.py`.

`theseo_anysearch/rllib/trainer/trainer.py` coordinates construction. `runtime.py`,
`results.py`, `lifecycle.py`, `checkpointing.py`, `early_stop.py`, and
`stage_sampling.py` divide iteration execution, normalization, transitions, persistence,
stopping, and stage assignment. The `curriculum/`, `evaluation/`, and `reporting/`
packages own their corresponding flows.

`theseo_anysearch/experiments/tune_runner.py` and
`theseo_anysearch/rllib/tune/` own Tune validation, Ray trial resources, scheduling,
continuation, and persisted search results.
