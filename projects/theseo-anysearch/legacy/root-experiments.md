---
title: Historical experiment workflow proposal
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: [subsystems/training-and-tuning, subsystems/trajectory-and-replay]
---

# Historical experiment workflow proposal

> This imported design mixes proposals and old implementation claims. Do not
> use its CLI, YAML, protobuf, checkpoint, or output examples as current
> instructions. Frozen studies live under [experiments](../experiments/README.md);
> current run behavior belongs to [training and tuning](../subsystems/training-and-tuning/README.md)
> and [trajectory and replay](../subsystems/trajectory-and-replay/README.md).

## Original imported text

# Experiments

An *experiment* is a fully-specified, reproducible run. It is described by a YAML file,
produces a self-contained output directory, and is tracked live in MLflow.
There are three experiment kinds:

| Kind | Discriminator | Description |
|---|---|---|
| **Training run** | no `tune_config` key | Single fixed-config training run |
| **Sweep** | top-level `sweep:` key | Sequential fixed-config runs over a list of hyperparameter overrides |
| **Tuning run** | `tune_config:` key present | Ray Tune-driven search over a declared search space; produces one trial per sample |

All three kinds share the same CLI, output conventions, MLflow tracking, and artifact format.

---

## CLI

```bash
anysearch add <yaml-or-dir> [<name>]          # register under a short name (global registry)
anysearch run <name> [--tag <tag>]            # start a run or sweep
anysearch list [<name>]                       # list all runs for an experiment or all experiments
anysearch inspect <name:run_id>               # print resolved config, metrics, artifact paths
anysearch resume  <name:run_id>               # continue from latest checkpoint
anysearch repeat  <name:run_id>               # re-run from scratch with same config
```

Direct paths work without registration:

```bash
anysearch run usage/experiments/train/ppo_baseline.yaml
```

> **Deprecated** (kept for backward compatibility):
> `anysearch experiment run --config <path>`, `anysearch experiment resume/repeat/inspect --run-id <id>`

---

## YAML Schema

### Single experiment

```yaml
experiment:
  name: surface-ppo-baseline       # used as MLflow experiment name and output subdirectory
  output_dir: ../../../runtime/experiments  # relative to this YAML file's location
  seed: 42

env:
  stl_path: configs/geometry.stl
  scale: 40.0
  agent_count: 4
  max_steps: 200

training:
  algorithm: ppo
  runner: local                     # local | anyscale
  iterations: 500
  checkpoint_interval: 50           # save checkpoint every N iterations
  trajectory_every: 10              # record trajectory protobuf every N iterations
  video_every: 100                  # render GIF every N iterations

algorithm_config:
  lr: 3.0e-4
  train_batch_size: 4096
  clip_param: 0.2
  num_sgd_iter: 10

model_config:
  use_position_encoding: true
  encoder_depth: 3

renders:
  camera_positions:
    - name: front
      yaw: 245.0
      pitch: 20.0
    - name: top
      yaw: 0.0
      pitch: 90.0

mlflow:
  tracking_uri: http://localhost:5000   # omit to use local ./mlruns
  artifact_store: null                  # null = same as output_dir; or a URI
```

All fields except `experiment.name` and `env.stl_path` have defaults matching the base models.
`experiment.output_dir` defaults to `./runtime/experiments`.

### Sweep (list of experiments)

A sweep shares a `base` config and declares a list of named overrides.
Each entry produces an independent run with its own `run_id` and output subdirectory.

```yaml
sweep:
  base:
    experiment:
      output_dir: ./runtime/experiments/sweep-lr
    env:
      stl_path: configs/geometry.stl
      agent_count: 4
      max_steps: 200
    training:
      algorithm: ppo
      iterations: 300
      checkpoint_interval: 50
      trajectory_every: 10
      video_every: 100
    model_config:
      use_position_encoding: true
    mlflow:
      tracking_uri: http://localhost:5000

  experiments:
    - name: ppo-lr-1e-4
      algorithm_config:
        lr: 1.0e-4
    - name: ppo-lr-3e-4
      algorithm_config:
        lr: 3.0e-4
    - name: ppo-lr-1e-3
      algorithm_config:
        lr: 1.0e-3
```

Each entry deep-merges its keys over `base`. The top-level `experiment.name` for each run is the
entry's `name` field. Missing `experiment.name` in base is filled from the entry.

### Tuning run

A tuning run adds a `tune_config` section to a standard experiment YAML.
The fixed `algorithm_config` and `model_config` values serve as defaults; `tune_config.search_space`
overrides specific fields with distributions that Ray Tune samples per trial.

```yaml
experiment:
  name: surface-ppo-lr-search
  output_dir: ./runtime/experiments
  seed: 42

env:
  stl_path: configs/geometry.stl
  scale: 40.0
  agent_count: 4
  max_steps: 200

training:
  algorithm: ppo
  runner: local
  iterations: 200              # max iterations per trial
  checkpoint_interval: 50
  trajectory_every: 10
  video_every: 50

algorithm_config:              # defaults; overridden per trial by search_space
  train_batch_size: 4096
  clip_param: 0.2
  num_sgd_iter: 10

model_config:
  use_position_encoding: true
  encoder_depth: 3

tune_config:
  scheduler: asha              # asha | pbt
  num_samples: 30              # number of trials to run
  metric: episode_reward_mean  # metric to optimise (reported by trainer each iteration)
  mode: max                    # max | min
  max_concurrent: 4            # max trials running in parallel (local runner: 1 recommended)
  search_space:
    algorithm_config:
      lr:               {loguniform: [1.0e-5, 1.0e-2]}
      train_batch_size: {choice: [2048, 4096, 8192]}
    model_config:
      encoder_depth:    {choice: [2, 3, 4]}

renders:
  camera_positions:
    - name: front
      yaw: 245.0
      pitch: 20.0

mlflow:
  tracking_uri: http://localhost:5000
```

**Search space syntax** — each leaf value is a dict with one key naming the Ray Tune sampler and
a list of arguments:

| YAML | Ray Tune equivalent |
|---|---|
| `{loguniform: [lo, hi]}` | `tune.loguniform(lo, hi)` |
| `{uniform: [lo, hi]}` | `tune.uniform(lo, hi)` |
| `{choice: [a, b, c]}` | `tune.choice([a, b, c])` |
| `{randint: [lo, hi]}` | `tune.randint(lo, hi)` |
| `{grid_search: [a, b]}` | `tune.grid_search([a, b])` |

The search space dict is deep-merged over the base `algorithm_config` / `model_config` at trial
launch, so only the fields being searched need to appear in `search_space`.

**PBT scheduler** requires `pbt_config` for mutation and perturbation settings:

```yaml
tune_config:
  scheduler: pbt
  num_samples: 16
  metric: episode_reward_mean
  mode: max
  pbt_config:
    perturbation_interval: 20  # iterations between perturbations
    hyperparam_mutations:       # same sampler syntax as search_space
      algorithm_config:
        lr: {loguniform: [1.0e-5, 1.0e-2]}
  search_space:
    algorithm_config:
      lr: {loguniform: [1.0e-5, 1.0e-2]}
```

---

## Output Directory Structure

### Training run / sweep entry

```
{output_dir}/
└── {experiment.name}/
    └── {run_id}/                         # run_id = 8-char hex; assigned at run start
        ├── experiment.yaml               # fully resolved config snapshot (no defaults hidden)
        ├── run.json                      # run_id, start_time, end_time, status, mlflow_run_url
        ├── checkpoints/
        │   ├── iter_000050/              # written by our Trainer at checkpoint_interval
        │   │   ├── state.json            # project state: iteration, episodes_total
        │   │   │
        │   │   # Ray RLlib checkpoint files (written by algo.save()):
        │   │   ├── algorithm_state.pkl   # algorithm metadata (small)
        │   │   ├── class_and_ctor_args.pkl
        │   │   ├── rllib_checkpoint.json
        │   │   ├── env_runner/           # env runner state
        │   │   └── learner_group/
        │   │       └── learner/
        │   │           ├── state.pkl     # learner weights (~1 MB)
        │   │           └── rl_module/
        │   │               └── default_policy/
        │   │                   └── module_state.pkl  # policy weights (~500 KB)
        │   ├── iter_000100/
        │   └── latest.json               # JSON pointer: {"path": "…/iter_000100", "iteration": 100}
        ├── trajectories/
        │   ├── iter_000010.pb            # TrajectoryCollection protobuf (see schema below)
        │   ├── iter_000020.pb
        │   └── ...
        └── renders/
            ├── iter_000100_front.gif
            ├── iter_000100_top.gif
            └── ...
```

> **Note on checkpoint format**: Ray RLlib 2.x uses its own binary checkpoint format
> (`algorithm_state.pkl`, nested `state.pkl` files). Restore is done via
> `algo.restore(path)` pointing at the `iter_XXXXXX/` directory.
> The project's own `state.json` is written alongside RLlib's files and carries
> iteration and episode counters needed to resume the training loop.
> `latest.json` is a JSON pointer file (not a symlink) for portability on Windows.

### Tuning run

```
{output_dir}/
└── {experiment.name}/
    └── {run_id}/
        ├── experiment.yaml               # fully resolved config including tune_config
        ├── run.json                      # run_id, best_trial_id, status, mlflow_run_url
        └── trials/
            ├── {trial_id}/               # one subdirectory per trial; structure mirrors training run
            │   ├── trial.json            # trial_id, sampled hyperparams, status, metric history
            │   ├── checkpoints/
            │   │   ├── iter_000050/
            │   │   │   ├── state.json
            │   │   │   ├── algorithm_state.pkl
            │   │   │   └── …             # (same RLlib structure as training run)
            │   │   └── latest.json
            │   ├── trajectories/
            │   │   └── iter_000010.pb
            │   └── renders/
            │       └── iter_000050_front.gif
            └── ...
```

`trial.json` contains:
```json
{
  "trial_id": "a3f1c2b0",
  "hyperparams": {"algorithm_config": {"lr": 3.2e-4, "train_batch_size": 4096}},
  "status": "COMPLETED",
  "best_iteration": 180,
  "metric_history": [{"iteration": 10, "episode_reward_mean": 0.4}, "..."]
}
```

`experiment.yaml` is written before any trial starts and is the authoritative record.
It resolves all defaults so the file is self-contained — no fallback to code defaults is needed
to understand or repeat the run.

---

## Protobuf Schema

Trajectory data is stored as binary protobuf. The `.proto` source lives at `core/proto/trajectory.proto`.

```proto
syntax = "proto3";
package theseo;

message Step {
  uint32 index          = 1;
  repeated float obs    = 2;   // flattened observation vector (row-major)
  int32  action         = 3;
  float  reward         = 4;
  bool   done           = 5;
  map<string, float> info = 6;
}

message AgentTrajectory {
  string agent_id       = 1;
  repeated Step steps   = 2;
}

message Episode {
  uint32 iteration      = 1;
  uint32 episode        = 2;
  float  total_reward   = 3;
  bool   success        = 4;
  repeated AgentTrajectory agents = 5;
}

message TrajectoryCollection {
  string experiment_name = 1;
  string run_id          = 2;
  uint32 iteration       = 3;
  repeated Episode episodes = 4;
}
```

One `.pb` file per recorded iteration. Reading any file is independent of the rest.

---

## Resume

**Training run:** `anysearch experiment resume --run-id <id>` reads `checkpoints/latest.json`
to find the path of the most recent checkpoint, calls `algo.restore(path)` to reload RLlib
state, and reads the accompanying `state.json` to recover the iteration counter.
Training continues from that iteration.

**Tuning run:** `anysearch experiment resume --run-id <id>` calls Ray Tune with `resume=True`,
pointing at the existing `trials/` directory. Ray Tune restores each trial's state from its
`latest.json` checkpoint pointer and continues incomplete trials. Completed trials are not re-run.

In both cases the original `experiment.yaml` is preserved unchanged. The resumed run appends to
the same output directory and logs to the same MLflow run (identified by `run_id` in `run.json`).

---

## Repeat

`anysearch experiment repeat --run-id <id>` reads `experiment.yaml` from an existing run and
launches a brand-new run from scratch: new `run_id`, new output subdirectory, same config.

This enables exact reproducibility: the new run uses the same seed, algorithm config, and model
config as the original.

---

## Inspect

`anysearch experiment inspect --run-id <id>` prints:

**Training run:**
- Full resolved config from `experiment.yaml`
- Run status and timing from `run.json`
- Checkpoint iterations available
- Trajectory files recorded
- Renders produced
- MLflow run URL

**Tuning run** (all of the above plus):
- Total trials, completed, failed, in-progress
- Best trial: `trial_id`, sampled hyperparams, best metric value and iteration
- Per-trial summary table: `trial_id`, status, best metric value

Output is plain JSON on stdout, suitable for piping.

---

## MLflow Integration

### Training run

Each run opens one MLflow run under the experiment named `experiment.name`.

| Event | MLflow action |
|---|---|
| Run start | `mlflow.start_run()`, log all config as params |
| Each iteration | `mlflow.log_metrics({episode_reward_mean, success_rate, …}, step=iteration)` |
| Each checkpoint | `mlflow.log_artifact(checkpoint_dir)` |
| Each trajectory file | `mlflow.log_artifact(iter_N.pb)` |
| Each render | `mlflow.log_artifact(iter_N_camera.gif)` |
| Run end | `mlflow.end_run(status="FINISHED"` or `"FAILED"`)` |

### Tuning run

A tuning run uses MLflow's nested run model: one **parent run** for the overall tuning job, and
one **child run** per trial. This lets the MLflow UI show all trials under a single collapsible
experiment entry while still supporting per-trial metric comparison.

| Event | MLflow action |
|---|---|
| Tune run start | `mlflow.start_run(run_name=experiment.name)`, log `tune_config` as params |
| Trial start | `mlflow.start_run(nested=True, run_name=trial_id)`, log sampled hyperparams as params |
| Trial iteration | `mlflow.log_metrics({metric: value}, step=iteration)` on child run |
| Trial checkpoint | `mlflow.log_artifact(trial_checkpoint_dir)` on child run |
| Trial trajectory | `mlflow.log_artifact(trial/iter_N.pb)` on child run |
| Trial render | `mlflow.log_artifact(trial/iter_N_camera.gif)` on child run |
| Trial end | `mlflow.end_run(status=…)` on child run |
| Tune run end | log `best_trial_id`, `best_metric_value` as metrics; `mlflow.end_run()` on parent |

### Sweeps

Each sweep entry logs to the same MLflow experiment name as separate (non-nested) runs,
enabling side-by-side comparison in the MLflow UI.

---

If `mlflow.tracking_uri` is omitted, tracking falls back to `./mlruns` (MLflow default).
If `mlflow.artifact_store` is set, artifacts are uploaded there instead of the default store.

---

## Cloud Output

`experiment.output_dir` accepts any URI supported by `fsspec`:

| Prefix | Backend |
|---|---|
| `./path` or `/abs/path` | local filesystem |
| `s3://bucket/prefix` | AWS S3 (requires `s3fs`) |
| `gs://bucket/prefix` | Google Cloud Storage (requires `gcsfs`) |
| `az://container/prefix` | Azure Blob Storage (requires `adlfs`) |

Checkpoints, trajectories, and renders are all written through the same `fsspec` handle.
No code change is needed to switch from local to cloud — only the YAML `output_dir` changes.

Credentials are resolved from the environment (AWS credentials, GCP ADC, Azure CLI) — the YAML
does not store secrets.

---

## Module Layout

```
theseo-anysearch/
├── experiments/
│   ├── __init__.py
│   ├── models.py         # ExperimentConfig, SweepConfig, TuneConfig, MLflowConfig, RendersConfig
│   ├── runner.py         # ExperimentRunner: load → run → checkpoint → track → render
│   ├── sweep.py          # SweepRunner: iterate over experiments, sequential by default
│   ├── tune.py           # TuneRunner: build search space, drive Ray Tune, write per-trial artifacts
│   ├── output.py         # OutputStore: fsspec-backed read/write for artifacts
│   ├── trajectory.py     # TrajectoryWriter: serialise episodes to protobuf
│   └── tracking.py       # MLflowTracker: thin wrapper around mlflow client
└── cli/
    └── commands/
        └── experiment.py # anysearch experiment {run,resume,repeat,inspect,list}
```

`run` dispatches to `ExperimentRunner`, `TuneRunner`, or `SweepRunner` based on which keys are
present in the YAML (`tune_config` → `TuneRunner`; `sweep` → `SweepRunner`; otherwise
`ExperimentRunner`).

### Key classes

| Class | Responsibility |
|---|---|
| `ExperimentConfig` | Pydantic model for a single experiment YAML; deep-merges sweep base |
| `SweepConfig` | Pydantic model for a sweep YAML; expands to `list[ExperimentConfig]` |
| `TuneConfig` | `scheduler`, `num_samples`, `metric`, `mode`, `max_concurrent`, `search_space`, optional `pbt_config` |
| `MLflowConfig` | `tracking_uri`, `artifact_store` |
| `RendersConfig` | `camera_positions: list[CameraPosition]` |
| `CameraPosition` | `name`, `yaw`, `pitch` |
| `ExperimentRunner` | Drives one training run: init output store, open MLflow run, call trainer loop |
| `SweepRunner` | Iterates `ExperimentRunner` over each entry; propagates failures without aborting sweep |
| `TuneRunner` | Translates `TuneConfig.search_space` to Ray Tune space; wraps `ExperimentRunner` as a trainable; opens parent + child MLflow runs; writes `trial.json` per trial |
| `OutputStore` | `write(path, data)`, `read(path)`, `list(prefix)` — all paths relative to `run_dir` |
| `TrajectoryWriter` | Accumulates `Episode` messages, serialises to `.pb` at configured interval |
| `MLflowTracker` | `log_params`, `log_metrics(step)`, `log_artifact(path)`, `start_child_run()`, `end_run(status)` |

---

## Additions to Existing Modules

### `training` config fields (added to `TrainingConfig`)

```
trajectory_every: int = 10   # record trajectory protobuf every N iterations
```

### `models.py` (top-level)

`ExperimentConfig` subclasses `Settings` and adds `experiment`, `renders`, `mlflow`, and optional
`tune_config` sections.

### `settings.py`

`load_experiment(path)` — variant of `load_settings` that returns `ExperimentConfig` or `SweepConfig`
depending on which top-level key is present.
Callers do not need to distinguish the kind — dispatch happens inside `ExperimentRunner.run()`.

---

## Dependencies

```toml
# add to pyproject.toml dependencies
"mlflow>=2.13",
"protobuf>=4.25",
"fsspec>=2024.2",
# optional cloud backends — not installed by default:
# "s3fs", "gcsfs", "adlfs"
```

The `experiments/` package imports `mlflow` and `fsspec` at the module level.
`protobuf` is required to write/read trajectory files; the generated Python bindings from
`core/proto/trajectory.proto` are committed to `experiments/proto/trajectory_pb2.py`.
