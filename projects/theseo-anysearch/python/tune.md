# `anysearch tune` — Hyperparameter Search

## Overview

Runs a Ray Tune hyperparameter search over PPO training configs.
Trials are scheduled by the chosen scheduler (ASHA by default), with MLflow and TensorBoard logging.

---

## YAML Config Structure

```yaml
experiment:
  name: <string>
  output_dir: <path>
  seed: <int>

env:
  stl_path: <path>
  scale: <float>
  agent_count: <int>
  max_steps: <int>

training:
  algorithm: ppo
  runner: local
  iterations: <int>          # max iterations per trial; scheduler stops bad ones early
  checkpoint_interval: <int>
  trajectory_every: <int>
  video_every: <int>
  num_gpus: <int>            # GPUs per trial worker; 0 = CPU-only; required

algorithm_config:            # fixed defaults for params NOT in search_space
  clip_param: 0.2
  num_sgd_iter: 10
  lambda_: 0.95
  # Any PPOConfig field can appear here as a fixed default.

model_config:                # fixed defaults for model params NOT in search_space
  encoder_depth: 3           # alias for num_layers (number of hidden layers)
  # layer_size: 256          # width per layer (default 256)

tune_config:
  scheduler: asha            # asha | pbt | random | hyperband | bohb | optuna | cmaes | flaml
  num_samples: 30            # total number of trials
  max_concurrent: 4          # max trials running in parallel
  metric: episode_reward_mean
  mode: max                  # max | min
  search_space:
    algorithm_config:
      lr:               {loguniform: [1.0e-5, 1.0e-2]}
      train_batch_size: {choice: [1024, 2048, 4096, 8192]}
      kl_coeff:         {uniform: [0.05, 0.5]}
    model_config:
      encoder_depth:    {choice: [2, 3, 4]}
```

---

## Parameter Resolution Order

For each trial, every parameter is resolved in this priority order (highest wins):

1. **Search-space sample** — value drawn by Ray Tune for this trial
2. **`algorithm_config` / `model_config` in YAML** — fixed defaults for untuned params
3. **Pydantic model default** — `PPOConfig` / `ModelConfig` field defaults

This means only params in the search space vary between trials. Everything else is fixed by the YAML, making results reproducible.

---

## Known Tuneable Params

| Section | Param | Type | Pydantic default |
|---|---|---|---|
| `algorithm_config` | `lr` | float | `3e-4` |
| `algorithm_config` | `gamma` | float | `0.99` |
| `algorithm_config` | `train_batch_size` | int | `4096` |
| `algorithm_config` | `clip_param` | float | `0.2` |
| `algorithm_config` | `num_sgd_iter` | int | `10` |
| `algorithm_config` | `lambda_` | float | `0.95` |
| `algorithm_config` | `kl_coeff` | float | `0.2` |
| `model_config` | `num_layers` / `encoder_depth` | int | `2` |
| `model_config` | `layer_size` | int | `256` |
| `model_config` | `use_position_encoding` | bool | `True` |

`encoder_depth` is a YAML alias for `num_layers` (number of hidden layers).

> **TODO — `use_position_encoding`**: field is accepted and stored but not yet wired into
> any model. When implemented it will append `(dx, dy, dz)` relative coordinates to each
> cell in the flat obs before the FC layers, giving the network explicit spatial context.
> Not needed for CNN models (spatial structure is preserved by convolution kernels).

Any key not in this table is flagged as a warning during pre-flight validation.

---

## GPU Configuration

`training.num_gpus` controls how many GPUs each trial worker requests from Ray.

- `num_gpus: 1` — each trial uses one GPU (requires CUDA-enabled torch)
- `num_gpus: 0` — CPU-only; useful for testing or machines without GPUs
- **Omitted** — auto-detected via `torch.cuda.device_count()` (capped at 1)

The pre-flight check warns if `num_gpus > 0` but no CUDA device is found, preventing all trials from erroring at startup.

---

## Pre-flight Validation

Before launching Ray, `anysearch tune` runs a config check that prints warnings for:

- Params in `algorithm_config` / `model_config` or `search_space` that are not in the known param table (typos, unsupported fields)
- `num_gpus > 0` with no CUDA device detected

Warnings are printed but do not abort the run. Fix them to avoid trial errors.

---

## Run Tags

Each run gets a tag used as its Ray Tune experiment name and output subdirectory:

- **Default**: `{algorithm}_{scheduler}` (e.g. `ppo_asha`)
- **Custom**: `--tag my_run`

Same tag → same directory. Running with an existing tag prints a summary of the previous run and exits. Use `--overwrite` to delete the previous run and start fresh.

---

## Outputs

```
runtime/tune/
└── {run_tag}/                    # Ray Tune experiment dir (one subdir per trial)
    ├── trial_<id>/
    │   ├── params.json           # hyperparams for this trial
    │   └── result.json           # JSONL: one line per training iteration
    └── experiment_state-*.json   # Ray Tune internal state (partially binary)

runtime/tune/ray_runtime.json     # tensorboard_logdir + ray session path
```

Monitor live:
```bash
tensorboard --logdir runtime/tune/{run_tag}
```

---

## CLI Reference

```
anysearch tune --stl <path> [OPTIONS]

  --algorithm     ppo               Base RLlib algorithm
  --scheduler     asha              Trial scheduler
  --config        <path>            YAML config file
  --tag           <string>          Run tag (default: {algorithm}_{scheduler})
  --overwrite                       Delete existing run with same tag
  --num-samples   20                Total trials (overridden by YAML)
  --max-concurrent 2                Parallel trials (overridden by YAML)
  --max-iterations 50               Max iterations per trial (overridden by YAML)
  --metric        episode_reward_mean
  --mode          max
  --output-dir    runtime/tune
  --agents        4
  --max-steps     200
  --seed          42
  --mlflow-tracking-uri  sqlite:///experiments/mlflow.db
```
