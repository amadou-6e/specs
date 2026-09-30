---
title: Imported RLlib module specification
status: superseded
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
supersedes: null
related: []
---

> Historical source. This document is not current implementation guidance.
> Its original wording is retained below for traceability.

## Migration disposition

The abstract-trainer, algorithm, runner, and tuner catalog predates the current
RLlib package layout and cannot be assumed to describe implemented interfaces.
Current investigation ownership is in [RLlib integration](../implementation/rllib/integration.md)
and [training-and-tuning design](../subsystems/training-and-tuning/design/README.md). Claims
must be checked against product source and tests before promotion. Its original
authority ended no later than classification under specs issue #110; an earlier
supersession date has not been established.

## Archived material

# RLlib Module Specification

## Purpose

Orchestrate reinforcement learning training over Rust-backed environments using Ray RLlib.
All classes in this module are abstract bases; concrete implementations live alongside them.

---

## Dependency Stack

```
Ray Tune          (hyperparameter search)
    └── Ray RLlib (training loop, algorithm, model)
            └── environments/ (Gymnasium / PettingZoo wrappers over Rust)
                    └── rust/ (PyO3 bindings: simulation, rendering)
```

---

## `trainer/base.py` — Abstract Trainer

Owns the top-level training lifecycle: builds the algorithm, runs iterations,
checkpoints, and triggers artifact export (GIF rendering) at epoch boundaries.

```python
class Trainer(ABC):
    def __init__(self, config: TrainerConfig): ...

    @abstractmethod
    def build_algorithm(self) -> Algorithm: ...

    def train(self, num_iterations: int) -> list[TrainResult]: ...
        # calls algorithm.train() in a loop
        # calls on_epoch_end() at each checkpoint interval

    @abstractmethod
    def on_epoch_end(self, iteration: int, result: TrainResult): ...
        # hook for GIF export, logging, checkpointing

    def stop(self): ...
```

`TrainerConfig` fields (sourced from `settings.py`):

| Field | Type | Description |
|---|---|---|
| `algorithm_cls` | `type[Algorithm]` | RLlib Algorithm class to instantiate |
| `env_cls` | `type[Env \| ParallelEnv]` | Environment class to register with RLlib |
| `runner_cls` | `type[Runner]` | Runner backend (local or anyscale) |
| `reward_shapers` | `list[RewardShaper]` | Applied in order before RLlib sees rewards |
| `checkpoint_interval` | `int` | Epochs between checkpoints and artifact export |
| `output_dir` | `Path` | Where GIFs and JSON summaries are written |

---

## `algorithms/base.py` — Abstract Algorithm Config

RLlib algorithms are configured via `AlgorithmConfig` objects, not subclassed directly.
`base.py` defines the project's standard config scaffold.

```python
class BaseAlgorithmConfig(ABC):
    @abstractmethod
    def build(self) -> AlgorithmConfig: ...
        # returns a fully configured ray.rllib.algorithms.AlgorithmConfig

    @abstractmethod
    def env_config(self) -> dict: ...
        # env kwargs passed through to the registered environment
```

Concrete implementations (e.g. `ppo.py`, `sac.py`) call `PPOConfig()` / `SACConfig()`
and apply project-specific defaults (rollout length, batch size, multi-agent policies).

---

### Concrete trainer implementations (`trainer/`)

Each concrete trainer class inherits from `Trainer`, sets `algorithm_name`, and implements `_build_algorithm()` (or the class-level `build_algorithm_from_settings()`).

| File | Class | Algorithm | Action space | Notes |
|---|---|---|---|---|
| `ppo.py` | `PPOTrainer` | `ray.rllib.algorithms.ppo.PPO` | Discrete / Continuous | Default baseline; `VoxelEnv` registration via `register_with_ray()`; also exports `VoxelEnvPathHelper` and `_ensure_ray_runtime()` shared by other trainers |
| `sac.py` | `SACTrainer` | `ray.rllib.algorithms.sac.SAC` | Discrete (VoxelEnv) | Uses `MultiAgentPrioritizedReplayBuffer` (required for legacy stack) |
| `dqn.py` | `DQNTrainer` | `ray.rllib.algorithms.dqn.DQN` | Discrete | Configurable replay buffer via `DQNConfig`; `train_batch_size` is off-policy sample size |
| `rainbow.py` | `RainbowTrainer` | `ray.rllib.algorithms.dqn.DQN` | Discrete | Full Rainbow: distributional Q (`num_atoms`), noisy nets, dueling, double Q, n-step, PER |
| `multi_voxel_ppo.py` | `MultiAgentVoxelPPOTrainer` | `ray.rllib.algorithms.ppo.PPO` | Discrete (26) | Multi-agent PPO; wraps `MultiVoxelEnv` via `ParallelPettingZooEnv`; all agents share `"shared_policy"` |
| `ddpg.py` | `DDPGTrainer` | — | Continuous | **Stub** — raises `NotImplementedError`; requires Box action space env |
| `td3.py` | `TD3Trainer` | — | Continuous | **Stub** — raises `NotImplementedError`; requires Box action space env |

`_ensure_ray_runtime(output_dir)` in `ppo.py` initialises Ray (if not already running) with `num_cpus=1`, no dashboard, and writes `ray_runtime.json` to the output dir. `VoxelEnvPathHelper.ray_root()` redirects Ray's session dir to the system temp dir when `output_dir` is deeply nested (Windows MAX_PATH guard).

---

## `models/base.py` — Abstract RLModule

Custom neural network architectures for policy and value heads.

```python
class BaseRLModule(RLModule, ABC):
    @abstractmethod
    def encode_observation(self, obs: dict) -> Tensor: ...
        # maps raw observation dict to a latent embedding

    # policy_head and value_head defined in concrete subclasses
```

### Concrete CNN models (`models/cnn.py`)

All models conform to the RLlib **legacy `TorchModelV2`** interface and are registered via `register_voxel_cnn_models()`.

| Class | YAML key | Input | Architecture |
|---|---|---|---|
| `VoxelBox2DCNN` | `voxel_box_2d_cnn` | `local_grid: Box(N³,)` + scalars | Reshape → `(B, z, x, y)` Conv2d stack → global-avg-pool → FC + policy/value heads |
| `VoxelBox3DCNN` | `voxel_box_3d_cnn` | `local_grid: Box(N³,)` + scalars | Reshape → `(B, 1, N, N, N)` Conv3d stack → global-avg-pool → FC heads |
| `VoxelHierarchicalBox3DCNN` | `voxel_hierarchical_box_3d_cnn` | `local_grid: Box(sum_i n_i³,)` + scalars | Split by radius, centre-pad to `N_max`, stack as channels → Conv3d → FC heads |

Scalars concatenated before FC head: `steps_remaining (1)`, `voxel_count (1)`, `cursor_pos (3)` = 5 total.

#### Common config keys (`custom_model_config`)

| Key | Default | Applies to |
|---|---|---|
| `box_radius` | `2` | `VoxelBox2DCNN`, `VoxelBox3DCNN` |
| `box_radii` | `[1, 4]` | `VoxelHierarchicalBox3DCNN` |
| `conv_channels` | `[32, 64, 64]` | all |
| `fc_hiddens` | `[256]` | all |
| `pool_type` | `"avg"` | all (`"avg"` or `"max"`) |

`_build_rllib_model_dict(model_cfg)` (exported from `cnn.py`) returns the correct RLlib `model=` dict — either a `custom_model` block (triggers `register_voxel_cnn_models()` on first call) or a plain `fcnet_hiddens` block.

---

Observation input format (from `SurfaceEnv`):

| Key | Shape | Description |
|---|---|---|
| `steps_remaining` | `(1,)` | Normalised steps left in episode |
| `agent_positions` | `(N, 3)` | Current position of each agent |
| `agent_targets` | `(N, 3)` | Target position of each agent |
| `reached_mask` | `(N,)` | Binary: agent has reached its goal |

---

## `runner/base.py` — Abstract Runner

Decouples the training orchestration from where it executes.

```python
class Runner(ABC):
    @abstractmethod
    def submit(self, trainer: Trainer) -> RunHandle: ...

    @abstractmethod
    def status(self, handle: RunHandle) -> RunStatus: ...

    @abstractmethod
    def cancel(self, handle: RunHandle): ...
```

### `runner/local.py`

Runs `trainer.train()` directly in the current process.
Used for development, debugging, and CI smoke tests.
No Ray cluster required.

### `runner/anyscale.py`

Submits a Ray job to Anyscale using the Anyscale SDK.
Reads cluster config from `settings.anyscale`.
Streams logs and polls job status via `anyscale.job.status()`.

---

## `rewards/base.py` — Abstract RewardShaper

Reward shapers intercept step results from the Rust environment before RLlib
processes them. They are applied in sequence (pipeline pattern).

```python
class RewardShaper(ABC):
    @abstractmethod
    def shape(self, agent_id: str, reward: float, obs: dict, done: bool) -> float: ...
```

Concrete shapers (examples):

| File | Strategy |
|---|---|
| `distance.py` | Dense shaping: additional reward proportional to distance reduction |
| `sparse.py` | Pass-through: no shaping, raw Rust rewards only |
| `composite.py` | Chains multiple shapers, returns summed result |

---

## `tune/base.py` — Abstract Tune Config

Defines the search space and scheduler for a Ray Tune experiment.

```python
class TuneConfig(ABC):
    @abstractmethod
    def search_space(self) -> dict: ...
        # ray.tune param_space dict (tune.uniform, tune.choice, etc.)

    @abstractmethod
    def scheduler(self) -> TrialScheduler: ...
        # e.g. ASHAScheduler, PopulationBasedTraining

    @abstractmethod
    def metric(self) -> str: ...
        # RLlib result key to optimise (e.g. "env_runners/episode_reward_mean")

    @abstractmethod
    def mode(self) -> Literal["min", "max"]: ...
```

Concrete configs (examples): `asha.py` (ASHA scheduler), `pbt.py` (Population Based Training).

---

## Wiring: How the pieces connect

```
cli/commands/train.py
    → reads Settings
    → instantiates AlgorithmConfig (algorithms/)
    → instantiates Trainer (trainer/)  ← wires env, algorithm, reward shapers
    → instantiates Runner (runner/)
    → runner.submit(trainer)

cli/commands/tune.py
    → reads Settings
    → instantiates TuneConfig (tune/)
    → calls ray.tune.Tuner(trainable=Trainer, param_space=..., tune_config=...)
    → .fit()
```

---

## RLlib Registration

Environments must be registered with RLlib before `AlgorithmConfig.environment()` can reference them:

```python
from ray.tune.registry import register_env

register_env("surface_env", lambda cfg: SurfaceEnv(cfg))
register_env("voxel_env",   lambda cfg: VoxelEnv(cfg))
```

Registration happens in `environments/__init__.py` so it runs on import.

---

## Multi-Agent Policy Mapping

`SurfaceEnv` is multi-agent (PettingZoo parallel API).
RLlib maps agent IDs to policies via a `policy_mapping_fn`:

```python
# Shared policy across all agents (parameter sharing)
def policy_mapping_fn(agent_id, episode, **kwargs):
    return "shared_policy"
```

Shared policy is the default. Independent policies per agent are supported
by mapping `agent_id` → `f"policy_{agent_id}"`.

---

## Algorithm Roadmap

### Phase 1 — Implemented

| Algorithm | File | Type | Action space | Notes |
|---|---|---|---|---|
| PPO | `trainer/ppo.py` | On-policy | Discrete / Continuous | Default baseline; stable on sparse rewards |
| SAC | `trainer/sac.py` | Off-policy | Discrete (VoxelEnv) | Sample-efficient; `MultiAgentPrioritizedReplayBuffer` required for legacy stack |
| DQN | `trainer/dqn.py` | Off-policy | Discrete | Simplest discrete baseline; configurable replay buffer |
| Rainbow DQN | `trainer/rainbow.py` | Off-policy | Discrete | DQN + PER + dueling + n-step + distributional Q + noisy nets |

### Phase 2 — Stub (requires Box action space env)

| Algorithm | File | Type | Action space | Notes |
|---|---|---|---|---|
| TD3 | `trainer/td3.py` | Off-policy | Continuous | Raises `NotImplementedError`; VoxelEnv/SurfaceEnv are Discrete |
| DDPG | `trainer/ddpg.py` | Off-policy | Continuous | Raises `NotImplementedError`; VoxelEnv/SurfaceEnv are Discrete |

### Phase 3 — Distributed / large-scale

| Algorithm | File | Type | Action space | Priority | Notes |
|---|---|---|---|---|---|
| IMPALA | `algorithms/impala.py` | On-policy (async) | Discrete / Continuous | Medium | Scales to many workers on Anyscale; V-trace correction |
| APPO | `algorithms/appo.py` | On-policy (async) | Discrete / Continuous | Medium | Async PPO; Anyscale-native distributed training |
| MADDPG | `algorithms/maddpg.py` | Off-policy (multi-agent) | Continuous | Low | Centralised critic for cooperative `SurfaceEnv` agents |

### Algorithm selection guide

```
Discrete routing actions (VoxelEnv):
  fast iteration  → DQN
  best result     → Rainbow DQN
  distributed     → APPO

Continuous control (SurfaceEnv):
  baseline        → PPO
  sample efficient → SAC
  deterministic   → TD3
  distributed     → IMPALA

Multi-agent cooperative:
  shared policy   → PPO or SAC with parameter sharing (default)
  independent     → MADDPG (Phase 3)
```

---

## Tuner Roadmap

Tuners live in `rllib/tune/` and implement the `TuneConfig` ABC.
They are referenced by name in `tune_config.scheduler` in the experiment YAML.

All tuner classes implement `BaseTuneConfig` with `search_space()`, `scheduler()`, `search_alg()`, `metric()`, `mode()`.

### Implemented tuners

| Name | File | YAML key | Scheduler | Search alg | Notes |
|---|---|---|---|---|---|
| ASHA | `tune/asha.py` | `scheduler: asha` | `ASHAScheduler` | random | Async Successive Halving; stops bad trials early; default choice |
| PBT | `tune/pbt.py` | `scheduler: pbt` | `PopulationBasedTraining` | mutation | Exploits best configs and explores mutations |
| Random Search | `tune/random.py` | `scheduler: random` | `FIFOScheduler` | random | Baseline; no early stopping; every trial runs to `max_t` |
| Hyperband | `tune/hyperband.py` | `scheduler: hyperband` | `HyperBandScheduler` | random | Synchronous Successive Halving; all trials in a rung evaluated together before promotion |
| BOHB | `tune/bohb.py` | `scheduler: bohb` | `HyperBandForBOHB` | `TuneBOHB` (TPE) | Bayesian + Hyperband; requires `ConfigSpace`; state-of-the-art on small budgets |
| Optuna | `tune/optuna.py` | `scheduler: optuna` | `ASHAScheduler` | `OptunaSearch` (TPE) | Best for rich continuous search spaces; requires `optuna` |
| CMA-ES | `tune/cmaes.py` | `scheduler: cmaes` | `FIFOScheduler` | `NevergradSearch` (CMA) | Strong on low-dimensional (≤20) continuous spaces; requires `nevergrad` |
| FLAML | `tune/flaml.py` | `scheduler: flaml` | `FIFOScheduler` | `CFO` | Cost-frugal optimiser; best when trial runtimes vary; requires `flaml` |

### Tuner selection guide

```
Tight compute budget, unknown landscape → ASHA (default)
Long-running trials, want evolution     → PBT
Bayesian + budget control               → BOHB
Rich continuous search space            → Optuna
Ablation / baseline                     → Random Search
```

### ASHA config fields (`ASHAConfig`)

| Field | Default | Description |
|---|---|---|
| `max_t` | `training.iterations` | Max resource (iterations) per trial |
| `grace_period` | `max_t // 10` | Minimum iterations before a trial can be stopped |
| `reduction_factor` | `3` | Ratio of trials eliminated at each rung |
| `brackets` | `1` | Number of ASHA brackets |

### PBT config fields (`PBTConfig`)

| Field | Default | Description |
|---|---|---|
| `perturbation_interval` | `20` | Iterations between perturbations |
| `hyperparam_mutations` | (from YAML) | Fields and samplers to mutate; same syntax as `search_space` |
| `resample_probability` | `0.25` | Probability of resampling from distribution instead of perturbing |
