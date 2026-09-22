---
title: Pretraining and qualification interfaces
status: draft
kind: subsystem-interfaces
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [README.md, configuration.md]
---

# Pretraining and qualification interfaces

This page inventories the callable and command-line surfaces through which callers
start training or tuning and receive results. Artifact lookup and loading are owned by
the model-registry subsystem.

## Python training interface

[`theseo_anysearch.garden.trainer.train`](../../../../../../theseo_anysearch/garden/trainer.py)
accepts a Torch model, train and validation datasets, `GardenTrainingConfig`, objective
name, device, optional epoch callback, and optional checkpoint path. It returns a
Pydantic `TrainResult`:

| Field | Meaning |
|---|---|
| `epochs_trained` | Last epoch number reached, not the count newly executed after resume. |
| `loss_curve` | Ordered dictionaries containing `epoch`, `train`, and `val`. |
| `final_val_loss` | Lowest observed validation loss. |
| `stopped_early` | Whether patience ended the loop. |

The callback signature is `(epoch: int, train_loss: float, val_loss: float) -> None`.
Callback exceptions propagate.

## Tune interface

[`GardenTuneRunner`](../../../../../../theseo_anysearch/garden/tune_runner.py) validates
that a Tune block exists at construction. `run(output_dir)` initializes Ray if needed,
runs the sweep, and returns `best_config`, `best_val_loss`, `run_name`, and
`num_trials`.

Supported search functions are `choice`, `grid_search`, `loguniform`, `uniform`,
`randint`, and `randn`. Each leaf must contain exactly one function name and its
arguments; malformed or unsupported leaves raise `ValueError` before the sweep.

## Command-line interface

The commands are defined in
[`garden.py`](../../../../../../theseo_anysearch/cli/commands/garden.py):

```text
anysearch garden train CONFIG [--output-dir PATH] [--tag TAG]
                       [--resume] [--device cpu|cuda|cuda:N|auto]

anysearch garden tune CONFIG [--output-dir PATH] [--tag TAG]
                      [--save-best|--no-save-best] [--garden-dir PATH]
```

`CONFIG` can be a literal YAML path, a built-in preset, or a name from the local
configuration registry. Direct training defaults artifacts to `runtime/garden`; Tune
defaults Ray results to `runtime/garden/tune` and saved models to `runtime/garden`.
There is no `qualify` or `certify` command at the inspected revision.
