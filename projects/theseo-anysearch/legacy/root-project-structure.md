---
title: Historical project structure map
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: [implementation/python/module-ownership, implementation/rust/module-ownership]
---

# Historical project structure map

> This imported tree describes an earlier repository and spec layout. Its
> `spec/`, `tests/unit/`, `tests/integration/`, and missing-infrastructure
> claims are not current. Use [architecture](../architecture/README.md) for
> system relationships, [Python module ownership](../implementation/python/module-ownership.md)
> and [Rust module ownership](../implementation/rust/module-ownership.md) for
> source layout, and their testing pages for actual test placement.

## Original imported text

# Project Structure

## Repository Layout

```
pyproject.toml                        # Single installable package: theseo-anysearch
configs/                              # Outside repo — user-supplied, not version controlled
├── anyscale.yaml                     # Anyscale cluster/compute/project config
└── experiment.yaml                   # Settings file (see settings.md for schema)
usage/                                # Example experiment YAMLs and STL geometries
├── experiments/train/                # Single-run YAML configs
├── experiments/tune/                 # Sweep / hyperparameter-search YAMLs
└── geometries/                       # Sample STL meshes

theseo_anysearch/                     # Python package (pip install -e .)
├── __init__.py
├── settings.py                       # YAML loader: reads config file, resolves algo/model classes
├── models.py                         # Base Pydantic models: EnvConfig, TrainingConfig, AlgorithmConfig, ModelConfig, Settings
├── cli/                              # CLI entry point (console_scripts in pyproject.toml)
│   ├── __init__.py
│   ├── main.py                       # Command registration
│   └── commands/
│       ├── train.py                  # Run training (local or distributed via --runner flag)
│       ├── tune.py                   # Run hyperparameter search via Ray Tune
│       ├── experiment.py             # anysearch experiment {run,resume,repeat,inspect,list}
│       ├── replay.py                 # anysearch replay {run_id,file,list} — open trajectory JSON in eframe viewer
│       └── mlflow_ui.py              # anysearch mlflow-ui — launch MLflow tracking UI
├── environments/                     # Python wrappers around Rust environments (PyO3 bound)
│   ├── __init__.py
│   ├── gymnasium/                    # Single-agent Gymnasium-compatible wrappers
│   │   ├── __init__.py
│   │   ├── models.py                 # GymnasiumEnvConfig (subclasses EnvConfig)
│   │   ├── base.py                   # Abstract RustGymnasiumEnv (gym.Env subclass)
│   │   └── voxel_env.py              # Gymnasium wrapper for VoxelEnv
│   └── pettingzoo/                   # Multi-agent PettingZoo parallel API wrappers
│       ├── __init__.py
│       ├── models.py                 # ParallelEnvConfig (subclasses EnvConfig)
│       ├── base.py                   # Abstract RustParallelEnv (ParallelEnv subclass)
│       ├── surface_env.py            # PettingZoo wrapper for SurfaceEnv
│       └── multi_voxel_env.py        # PettingZoo wrapper for MultiAgentVoxelEnv (N agents, shared grid)
├── experiments/                      # Experiment lifecycle: run, resume, repeat, inspect, sweep
│   ├── __init__.py
│   ├── models.py                     # ExperimentConfig, SweepConfig, MLflowConfig, RendersConfig
│   ├── runner.py                     # ExperimentRunner: drives one run end-to-end
│   ├── sweep.py                      # SweepRunner: iterate over experiment list
│   ├── output.py                     # OutputStore: fsspec-backed artifact read/write
│   ├── tune.py                       # TuneRunner: search space translation, Ray Tune driver, per-trial artifacts
│   ├── trajectory.py                 # TrajectoryWriter: serialise episodes to protobuf
│   └── tracking.py                   # MLflowTracker: thin wrapper around mlflow client
├── rllib/                            # RLlib training orchestration
│   ├── __init__.py
│   ├── trainer/                      # Training loop orchestration + concrete trainers
│   │   ├── __init__.py
│   │   ├── models.py                 # TrainerConfig (subclasses TrainingConfig)
│   │   ├── base.py                   # Abstract Trainer (constructs Algorithm, drives train())
│   │   ├── ppo.py                    # PPOTrainer; also VoxelEnvPathHelper, _ensure_ray_runtime()
│   │   ├── sac.py                    # SACTrainer (discrete VoxelEnv; MultiAgentPrioritizedReplayBuffer)
│   │   ├── dqn.py                    # DQNTrainer (configurable off-policy replay buffer)
│   │   ├── rainbow.py                # RainbowTrainer (DQN + PER + dueling + n-step + distributional Q + noisy)
│   │   ├── multi_voxel_ppo.py        # MultiAgentVoxelPPOTrainer (MultiVoxelEnv via ParallelPettingZooEnv)
│   │   ├── ddpg.py                   # DDPGTrainer stub — NotImplementedError (needs Box action space)
│   │   └── td3.py                    # TD3Trainer stub — NotImplementedError (needs Box action space)
│   ├── algorithms/                   # Custom RLlib Algorithm subclasses and configs
│   │   ├── __init__.py
│   │   ├── models.py                 # PPOConfig, SACConfig, … (subclass AlgorithmConfig)
│   │   └── base.py                   # Abstract base algorithm config and hooks
│   ├── models/                       # Custom RLlib model definitions (RLModule subclasses)
│   │   ├── __init__.py
│   │   ├── models.py                 # VoxelEncoderConfig, … (subclass ModelConfig)
│   │   ├── base.py                   # Abstract base RLModule (encoder interface)
│   │   └── cnn.py                    # VoxelBox2DCNN, VoxelBox3DCNN, VoxelHierarchicalBox3DCNN; register_voxel_cnn_models()
│   ├── runner/                       # Execution backends (local and distributed)
│   │   ├── __init__.py
│   │   ├── models.py                 # LocalRunnerConfig, AnyscaleRunnerConfig (subclass RunnerConfig)
│   │   ├── base.py                   # Abstract Runner interface (submit, monitor, cancel)
│   │   ├── local.py                  # Local runner (single-process, dev/debug)
│   │   └── anyscale.py               # Anyscale distributed runner (Ray job submission)
│   ├── rewards/                      # Composable reward shaping strategies
│   │   ├── __init__.py
│   │   ├── models.py                 # RewardConfig, CompositeRewardConfig (subclass base)
│   │   └── base.py                   # Abstract RewardShaper interface
│   └── tune/                         # Hyperparameter optimization via Ray Tune
│       ├── __init__.py
│       ├── models.py                 # ASHAConfig, PBTConfig, BOHBConfig, … (subclass TuneConfig)
│       ├── base.py                   # BaseTuneConfig ABC: search_space(), scheduler(), search_alg(), metric(), mode()
│       ├── random.py                 # RandomSearch — FIFOScheduler, no early stopping (baseline)
│       ├── hyperband.py              # HyperbandSearch — synchronous Successive Halving
│       ├── bohb.py                   # BOHBSearch — HyperBandForBOHB + TuneBOHB (requires ConfigSpace)
│       ├── optuna.py                 # OptunaSearch — ASHAScheduler + OptunaSearch TPE (requires optuna)
│       ├── cmaes.py                  # CMAESSearch — FIFOScheduler + NevergradSearch CMA (requires nevergrad)
│       └── flaml.py                  # FLAMLSearch — FIFOScheduler + CFO cost-frugal (requires flaml)
├── core/                             # Rust source (was rust/)
│   ├── Cargo.toml                    # Workspace manifest
│   ├── Cargo.lock
│   ├── pyproject.toml                # Maturin build config for Python wheel (module: theseo_core)
│   ├── proto/
│   │   └── trajectory.proto          # Protobuf schema for TrajectoryCollection, Episode, Step
│   └── src/
│       ├── lib.rs                    # Library exports (for PyO3 wheel)
│       ├── main.rs                   # Binary entry point (interactive viewer)
│       ├── bridge/
│       │   ├── mod.rs
│       │   ├── dto.rs                # GeometrySubmission, EnvConfig, TrainConfig DTOs
│       │   └── py_bindings.rs        # PyO3 #[pyfunction] wrappers
│       ├── environments/
│       │   ├── mod.rs
│       │   ├── traits.rs             # Environment trait (reset, step, StepResult)
│       │   ├── voxel_env.rs          # Single-agent place/remove/noop environment
│       │   ├── surface_env.rs        # Multi-agent surface pathfinding environment
│       │   └── multi_voxel_env.rs    # MultiAgentVoxelEnv: N agents, shared grid, 26-action; exports OFFSETS_26, manhattan(), compute_surface_cells()
│       ├── world/
│       │   ├── mod.rs
│       │   ├── api.rs                # World trait, WorldError enum
│       │   ├── block.rs              # Block struct, BlockUpdate
│       │   ├── state.rs              # WorldState: HashMap<Coord, Block>, constants
│       │   └── ingest/
│       │       ├── mod.rs
│       │       ├── stl.rs            # ASCII STL parser -> mesh model
│       │       └── voxelize.rs       # Mesh -> voxel placement (vertex + solid fill)
│       ├── camera.rs                 # Camera math: orbit/pan/zoom, projection/view matrices
│       ├── renderer.rs               # Core software rasterizer → writes to RgbaBuffer
│       ├── app/                      # eframe interactive viewer (consumes RgbaBuffer)
│       │   ├── mod.rs
│       │   ├── main.rs               # eframe App setup, event loop
│       │   └── ui/
│       │       ├── mod.rs
│       │       └── panels.rs         # egui sidebar: stats, camera, voxel editor (planned)
│       └── bin/
│           ├── poc.rs                # PoC batch runner (smoke test)
│           ├── pathfinding_eframe.rs # Interactive pathfinding visualizer
│           └── voxel_replay.rs       # Trajectory replay viewer (opened by `anysearch replay`)
tests/                                # At repo root (alongside theseo_anysearch/)
├── conftest.py                       # Shared fixtures: settings, STL path, mock theseo_core
├── unit/                             # Fast tests; no Rust wheel required
│   ├── test_settings.py
│   ├── test_models.py
│   ├── test_environments.py
│   ├── test_rewards.py
│   ├── test_trainer.py
│   ├── test_experiments.py
│   └── test_cli.py
└── integration/                      # Slow tests; require theseo_core wheel
    ├── test_voxel_env.py
    ├── test_surface_env.py
    └── test_train.py
spec/
│   ├── project-structure.md          # This file
│   ├── naming.md                     # Naming philosophy: packages, classes, methods, flags
│   ├── experiments.md                # Experiment YAML schema, output layout, protobuf, MLflow, sweep
│   ├── python/
│   │   ├── cli.md                    # CLI commands: train, tune, experiment
│   │   ├── environments-python.md    # Gymnasium and PettingZoo wrappers
│   │   ├── rllib.md                  # RLlib trainer, algorithms, models, runner, rewards, tune
│   │   ├── settings.md               # YAML config schema, Pydantic models, loader
│   │   └── testing.md                # pytest strategy, unit/integration split, fixtures, CI
│   └── rust/
│       ├── bridge.md                 # DTOs, serialisation structs, PyO3 exported functions
│       ├── environment.md            # Environment trait, SurfaceEnv, VoxelEnv
│       ├── ingest.md                 # ASCII STL parser, voxelizer, solid-fill algorithm
│       ├── rendering.md              # Unified renderer, RgbaBuffer, camera, eframe app
│       ├── testing.md                # cargo test strategy, unit/integration split, CI
│       ├── voxel-spec.md             # Voxel world spec, interactive renderer milestones
│       └── world.md                  # WorldState, World trait, invariants
└── runtime/                          # Training artifacts (GIFs, JSON summaries)
```

---

## Module Responsibilities

### Rust (`core/src/`)

| Module | Responsibility |
|---|---|
| `bridge/` | DTOs, PyO3 `#[pyfunction]` wrappers; the only layer Python calls directly |
| `environments/` | `Environment` trait, `VoxelEnv`, `SurfaceEnv` |
| `world/` | Voxel state, block API, coordinate system, invariant enforcement, STL import, voxelization |
| `camera.rs` | Camera math: orbit/pan/zoom, projection/view matrices (shared by app and bridge) |
| `renderer.rs` | Single software rasterizer writing to `RgbaBuffer`; consumed by both the eframe app and the headless GIF encoder in `bridge/` |
| `app/` | eframe App lifecycle, input routing, egui panel display of the rendered buffer |
| `bin/poc.rs` | PoC batch runner: world API + STL + env rollout smoke test |
| `bin/pathfinding_eframe.rs` | Interactive pathfinding visualization binary |
| `bin/voxel_replay.rs` | Trajectory JSON replay viewer; launched by `anysearch replay` CLI command |

### Python (`theseo_anysearch/`)

| Module | Responsibility |
|---|---|
| `cli/commands/train.py` | `train` CLI command: selects runner (local/anyscale) via `--runner` flag, delegates to `rllib/` |
| `cli/commands/tune.py` | `tune` CLI command: launches Ray Tune search, delegates to `rllib/tune/` |
| `cli/commands/experiment.py` | `experiment` CLI command: run/resume/repeat/inspect/list |
| `cli/commands/replay.py` | `replay` CLI command: open trajectory JSON(s) in eframe viewer; subcommands `file`, `list` |
| `cli/commands/mlflow_ui.py` | `mlflow-ui` CLI command: launch MLflow UI pointed at experiment output dir |
| `experiments/runner.py` | `ExperimentRunner`: resolves config, opens MLflow run, drives trainer loop, writes artifacts |
| `experiments/sweep.py` | `SweepRunner`: expands sweep YAML, iterates `ExperimentRunner` per entry |
| `experiments/output.py` | `OutputStore`: fsspec-backed read/write for checkpoints, trajectories, renders |
| `experiments/tune.py` | `TuneRunner`: translates search space YAML to Ray Tune space, wraps trainer as trainable, drives trial loop |
| `experiments/trajectory.py` | `TrajectoryWriter`: accumulates episodes, serialises to protobuf per interval |
| `experiments/tracking.py` | `MLflowTracker`: log params, log metrics per step, log artifacts, manage nested runs |
| `environments/gymnasium/base.py` | Abstract `RustGymnasiumEnv`; all single-agent wrappers inherit from this |
| `environments/gymnasium/` | Concrete Gymnasium `Env` wrappers for single-agent Rust environments |
| `environments/pettingzoo/base.py` | Abstract `RustParallelEnv`; all multi-agent wrappers inherit from this |
| `environments/pettingzoo/` | Concrete PettingZoo `ParallelEnv` wrappers for multi-agent Rust environments |
| `rllib/trainer/base.py` | Abstract `Trainer`; constructs `Algorithm`, drives `train()` iterations |
| `rllib/trainer/ppo.py` | `PPOTrainer`; also `VoxelEnvPathHelper`, `_ensure_ray_runtime()` (shared by other trainers) |
| `rllib/trainer/sac.py` | `SACTrainer` — discrete off-policy; requires `MultiAgentPrioritizedReplayBuffer` |
| `rllib/trainer/dqn.py` | `DQNTrainer` — configurable replay buffer; `train_batch_size` is off-policy sample size |
| `rllib/trainer/rainbow.py` | `RainbowTrainer` — full Rainbow: distributional Q, noisy, dueling, double Q, n-step, PER |
| `rllib/trainer/multi_voxel_ppo.py` | `MultiAgentVoxelPPOTrainer` — PPO over `MultiVoxelEnv` via `ParallelPettingZooEnv`; shared policy |
| `rllib/trainer/ddpg.py` | `DDPGTrainer` stub — raises `NotImplementedError`; needs Box action space |
| `rllib/trainer/td3.py` | `TD3Trainer` stub — raises `NotImplementedError`; needs Box action space |
| `rllib/algorithms/base.py` | Abstract algorithm config and lifecycle hooks; all algorithms inherit from this |
| `rllib/algorithms/` | Concrete RLlib `AlgorithmConfig` subclasses (PPOConfig, SACConfig, DQNConfig, …) |
| `rllib/models/base.py` | Abstract `RLModule` encoder interface; all models inherit from this |
| `rllib/models/cnn.py` | `VoxelBox2DCNN`, `VoxelBox3DCNN`, `VoxelHierarchicalBox3DCNN`; `register_voxel_cnn_models()` |
| `rllib/runner/base.py` | Abstract `Runner` interface (submit, monitor, cancel) |
| `rllib/runner/local.py` | Local runner: single-process execution for dev and debug |
| `rllib/runner/anyscale.py` | Anyscale runner: Ray job submission and monitoring on Anyscale |
| `rllib/rewards/base.py` | Abstract `RewardShaper` interface for composable reward transforms |
| `rllib/rewards/` | Concrete reward shapers (distance-based, sparse, shaped, composite) |
| `rllib/tune/base.py` | `BaseTuneConfig` ABC: `search_space()`, `scheduler()`, `search_alg()`, `metric()`, `mode()` |
| `rllib/tune/random.py` | `RandomSearch` — FIFOScheduler, no early stopping (ablation baseline) |
| `rllib/tune/hyperband.py` | `HyperbandSearch` — synchronous Successive Halving |
| `rllib/tune/bohb.py` | `BOHBSearch` — HyperBandForBOHB + TuneBOHB TPE (requires `ConfigSpace`) |
| `rllib/tune/optuna.py` | `OptunaSearch` — ASHA + Optuna TPE (requires `optuna`) |
| `rllib/tune/cmaes.py` | `CMAESSearch` — FIFO + Nevergrad CMA-ES (requires `nevergrad`) |
| `rllib/tune/flaml.py` | `FLAMLSearch` — FIFO + FLAML CFO cost-frugal search (requires `flaml`) |
| `models.py` | Base Pydantic models: `EnvConfig`, `TrainingConfig`, `AnyscaleConfig`, `AlgorithmConfig`, `ModelConfig`, `Settings` |
| `settings.py` | YAML loader: reads config file, merges CLI overrides, resolves concrete `AlgorithmConfig` and `ModelConfig` subclasses |
| `tests/unit/` | Fast pytest tests; no Rust wheel required; cover settings, models, env wrappers, rewards, CLI |
| `tests/integration/` | Slow pytest tests; require `theseo_core` wheel; cover full env round-trips and training loop |

---

## Contract Boundaries

1. **Python → Rust:** Python passes immutable config/inputs to Rust via PyO3 DTOs (`bridge/dto.rs`)
2. **Rust → Python:** Rust returns deterministic outputs: JSON summaries, artifact file paths, step results
3. **CLI → Simulation:** CLI commands never mutate simulation state directly — all mutations go through `environments/` wrappers which call Rust bindings
4. **RL → Environments:** `rllib/` consumes the environment wrapper interface; it has no direct dependency on PyO3 or Rust internals
5. **Settings authority:** All configuration values originate from `settings.py`; CLI flags override settings but do not bypass them

---

## Build System

### Rust Binary (interactive viewer)

```bash
cd theseo_anysearch/core
cargo run                              # launches eframe interactive viewer
cargo run --bin pathfinding_eframe     # launches pathfinding visualizer
cargo run --bin poc                    # runs PoC batch smoke test
```

### Python Wheel (PyO3 bindings)

```bash
cd theseo_anysearch/core
maturin develop                        # build + install wheel into .venv for development
maturin build                          # produce .whl for distribution
```

### Python package

```bash
pip install -e .                       # install everything: cli, environments, rllib, settings
anysearch train --help                 # verify CLI
anysearch tune --help

# Run without installing (from repo root):
python -m theseo_anysearch.cli.main experiment run --config usage/experiments/train/ppo_baseline.yaml
```

---

## Missing Infrastructure

The following are not yet in place:

- No CI/CD pipeline (GitHub Actions or equivalent)
- No README at repository root
- `renderer.rs` / `bridge/py_bindings.rs` — headless GIF encoding path is a separate implementation inside `py_bindings.rs`; needs refactoring so both `app/` and the headless path consume the same `RgbaBuffer` pipeline
- `experiments/sweep.py` and `experiments/tune.py` — not yet present; `ExperimentRunner` covers single runs but sweep/tune orchestration is unimplemented
- `core/proto/trajectory.proto` — protobuf schema not yet present; `TrajectoryWriter` in `experiments/trajectory.py` currently writes JSON
- `usage/experiments/` — example YAML configs for `train/` and `tune/` subdirs not yet populated
- `runner/anyscale.py` — present as a file but Anyscale integration is a stub pending `anyscale` SDK wiring
