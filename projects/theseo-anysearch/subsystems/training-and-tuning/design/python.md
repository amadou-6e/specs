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

## Design-map refresh still needed

The map above was inspected at an older product revision; it is not a claim that
all modules or responsibilities remain unchanged. At a fresh pinned revision,
trace iteration control, checkpoint-local auxiliary state, curriculum stages,
evaluation timing, trajectory capture, pretraining handoff, Tune trial identity,
and clone/apply recipes through their current source and tests. Record which
paths are active versus scaffolds, and distinguish continuation, fine-tuning,
and evaluation. Mark each finding current, obsolete, or unverified before
revising the map. RLlib object/API touch points belong in the
[RLlib implementation inventory](../../../implementation/rllib/integration.md);
actor/worker execution and vectorization belong in the
[Ray implementation investigation](../../../implementation/ray/execution.md).
