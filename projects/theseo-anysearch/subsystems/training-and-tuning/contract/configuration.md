# Training and tuning configuration

This page summarizes behaviorally significant blocks. Exact validation is implemented
by `theseo_anysearch/settings/training.py` and
`theseo_anysearch/experiments/models.py` at the audited revision.

`training` selects algorithm, model family, runner, hard iteration maximum, checkpoint
and trajectory cadence, early stop, and learner/EnvRunner resources. Learner GPU
allocation is distinct from `num_gpus_per_env_runner`; changing one must not silently
change the other.

`algorithm_config` contains algorithm hyperparameters. `model_config` contains network
settings. `evaluation` defines deterministic evaluation episodes and cadence. Staging
defines ordered tasks, recursively merged overrides, sampling, and a composable
completion tree with a finite cap. Tune configuration defines validated search spaces,
scheduler/search behavior, sample count, concurrency, and trial resources.

Inactive and unknown Tune parameters must produce validation feedback rather than a
silent no-op. Algorithm, model architecture, observation/action contracts, stage
definitions, evaluation seeds, and pretraining identity all affect reproducibility.
