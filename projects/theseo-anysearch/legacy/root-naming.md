---
title: Historical naming philosophy
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: [../implementation/python/code-conventions.md, ../implementation/rust/code-conventions.md]
---

# Historical naming philosophy

> These imported examples are candidate conventions, not enforced current
> rules. Verify Python and Rust patterns against pinned source, formatter,
> lint, and contributor evidence before promoting them to the respective
> [Python](../implementation/python/code-conventions.md) or
> [Rust](../implementation/rust/code-conventions.md) guidance.

## Original imported text

# Naming Philosophy

## Guiding Principle

Names should state what a thing *is* or *does* at the level of abstraction it lives in.
No redundant suffixes, no encoding of layer in the name, no Hungarian notation.
When reading a name in isolation, its role should be unambiguous.

---

## Package and Module Names

| Thing | Name | Notes |
|---|---|---|
| Python package | `theseo` | Short, matches project; importable root |
| Rust wheel (PyO3) | `theseo_core` | Replaces current `voxel_renderer`; signals it is the compiled core |
| CLI entry point | `anysearch` | The command users type (`anysearch train`) |

Current `voxel_renderer` is a working name from the PoC. It is renamed to `theseo_core`
when the package is restructured.

---

## File Names

All Python files: `snake_case.py`.
No `-` in file names. No `Abstract`, `Base`, `I` prefixes in file names.

| Pattern | Example | Notes |
|---|---|---|
| Abstract base | `base.py` | One per directory; always named `base.py` |
| Config models | `models.py` | One per directory; always named `models.py` |
| Concrete impl | `{noun}.py` | Named after the thing, not the pattern: `ppo.py`, `local.py` |
| CLI command | `{verb}.py` | Named after the action: `train.py`, `tune.py` |

---

## Class Names

`PascalCase` throughout.

### Abstract bases

Named after the concept, not the abstraction mechanism.
Do **not** prefix with `Base`, `Abstract`, or `I`.

```python
# Correct
class Trainer(ABC): ...
class Runner(ABC): ...
class RewardShaper(ABC): ...

# Wrong
class BaseTrainer(ABC): ...
class AbstractRunner(ABC): ...
class IRewardShaper(ABC): ...
```

### Concrete implementations

Named after their specific behaviour or algorithm.
Do **not** repeat the base class name.

```python
# Correct
class LocalRunner(Runner): ...
class AnyscaleRunner(Runner): ...
class PPO(Algorithm): ...

# Wrong
class LocalRunnerImpl(Runner): ...
class PPOAlgorithm(Algorithm): ...
```

### Config models (Pydantic)

Always suffixed with `Config`. The suffix signals "this is a validated data bag, not a live object."

```python
class EnvConfig(BaseModel): ...
class PPOConfig(AlgorithmConfig): ...
class VoxelEncoderConfig(ModelConfig): ...
class AnyscaleRunnerConfig(RunnerConfig): ...
```

### Environment wrappers

Named after the environment's behaviour, not its implementation detail.
Drop redundant words (`Basic`, `Env` suffix is enough from the library base class).

```python
# Correct
class VoxelEnv(RustGymnasiumEnv): ...
class SurfaceEnv(RustParallelEnv): ...

# Wrong
class BasicVoxelEnv(RustGymnasiumEnv): ...
class SurfacePathFindingEnv(RustParallelEnv): ...
```

`Surface` is unambiguous in context — every surface environment is a pathfinding environment.
`Path` is redundant and is dropped everywhere (Python and Rust).

---

## Method Names

Verb-first. Use domain verbs, not generic ones (`run`, `execute`, `do`).

| Class | Method | Not |
|---|---|---|
| `Trainer` | `train()`, `checkpoint()`, `stop()` | `run()`, `execute()` |
| `Runner` | `submit()`, `status()`, `cancel()` | `run()`, `start()` |
| `RewardShaper` | `shape(reward)` | `apply()`, `run()` |
| `TuneConfig` | `search_space()`, `scheduler()` | `get_space()`, `build()` |
| `AlgorithmConfig` | `build()` | `make()`, `create()` |
| Settings loader | `load_settings(path)` | `get_settings()`, `parse()` |
| Env registration | `register_envs()` | `setup()`, `init()` |

CLI command entry points keep `run(args)` — it is the established pattern and
these are procedural dispatch functions, not domain objects.

---

## Variable and Argument Names

`snake_case`. Spell out words fully; no abbreviations except established domain terms.

| Established abbreviation | Full form avoided |
|---|---|
| `obs` | `observation` (Gymnasium convention) |
| `cfg` | never — always `config` |
| `env` | acceptable when referring to a live environment instance |
| `lr` | acceptable in ML config context (`lr: float`) |
| `stl` | acceptable as domain term (file format) |

---

## CLI Flag Names

`kebab-case`. Match the Python attribute name with `_` → `-` substitution.
The flag name should be the noun or adjective, not the implementation detail.

```
--runner         not --backend
--iterations     not --episodes (episodes implies one env step; iterations = RLlib train calls)
--checkpoint-interval  not --save-every
--output-dir     keep (already established)
--video-every    keep (already established)
```

**Resolved inconsistency:** current code uses `--backend`. The spec name is `--runner`.
`runner` is preferred because it names the role (something that runs a job), not the technology layer.

---

## JSON Output Keys

`snake_case`. Match Python attribute names exactly.
No camelCase, no abbreviations.

```json
{
  "iteration": 42,
  "episode_reward_mean": 12.4,
  "success_rate": 0.73,
  "checkpoint_path": "runtime/checkpoints/iter_0042"
}
```

---

## Rust Naming

Rust follows its own idioms. These rules apply to the `rust/src/` codebase.

### General conventions

| Category | Convention | Example |
|---|---|---|
| Types, traits, enums | `PascalCase` | `WorldState`, `StepResult`, `WorldError` |
| Functions, methods, variables | `snake_case` | `reset()`, `set_block()`, `agent_count` |
| Constants | `UPPER_SNAKE_CASE` | `WORLD_SIZE`, `WORLD_CENTER` |
| Modules (files) | `snake_case` | `surface_env.rs`, `voxel_env.rs` |
| PyO3 exported functions | `py_` prefix | `py_submit_geometry`, `py_render_stl` |

---

### Traits

Traits name the *capability*, not the implementor. No `Interface` or `Trait` suffix.

| Current | Renamed | Reason |
|---|---|---|
| `WorldInterface` | `World` | `Interface` suffix is Java idiom; the trait is the concept |
| `RlEnvironment` | `Environment` | `Rl` prefix is redundant — all environments here are RL environments |

`WorldState` remains the concrete implementation of the `World` trait.

---

### Environment types

Aligned with Python: drop `PathFinding`, drop `Basic`.

| Current | Renamed | File |
|---|---|---|
| `SurfacePathFindingEnv` | `SurfaceEnv` | `environments/surface_env.rs` |
| `BasicVoxelEnv` | `VoxelEnv` | `environments/voxel_env.rs` |
| `SurfacePathAction` | `SurfaceAction` | (in `surface_env.rs`) |
| `BasicVoxelAction` | `VoxelAction` | (in `voxel_env.rs`) |
| `SurfacePathObservation` | `SurfaceObservation` | (in `surface_env.rs`) |

---

### Rendering and projection internals

| Current | Renamed | Reason |
|---|---|---|
| `ProjVertex` | `Vertex` | In rendering context, all vertices are projected; the prefix is noise |
| `project_iso_f32_with_depth` | `project_with_depth` | Type is implicit; `iso` is an implementation detail |
| `project_iso` | `project` | Same reasoning |
| `CameraAngles` | keep | Clear and accurate |
| `RgbaBuffer` | keep | Accurate and explicit |

---

### Data / serialisation structs

| Current | Renamed | Reason |
|---|---|---|
| `RustVideoRunSummary` | `TrainingSummary` | `Rust` is an implementation detail; the struct is a training outcome |
| `EpisodeTrace` | keep | Accurate |
| `EpisodeStep` | keep | Accurate |
| `EpochSummary` | keep | Accurate |
| `PaintVoxel` | keep | Clear in context |
| `GeometrySubmission` | keep | DTO name, describes the payload |

---

### PyO3 exported functions (`bridge/py_bindings.rs`)

The `py_` prefix is kept on all exported functions — it marks the Python-facing boundary
clearly when reading Rust code.

Function names are simplified to remove implementation detail (`pathfinding`, `rust`, `poc`, `test`).

| Current | Renamed |
|---|---|
| `py_submit_geometry` | keep |
| `py_world_interface_poc` | `py_world_smoke_test` (temporary; retire with test suite) |
| `py_surface_pathfinding_from_stl` | `py_surface_env_from_stl` |
| `py_surface_pathfinding_trace_from_stl` | `py_surface_env_trace` |
| `py_train_pathfinding_rust_videos` | `py_train_videos` |
| `py_render_stl_test` | `py_render_stl` |
| `py_render_cube_test` | `py_render_cube` |

---

### Module (pymodule) name

| Current | Target |
|---|---|
| `voxel_renderer` | `theseo_core` |

This is the importable Python name of the compiled Rust wheel.
`voxel_renderer` is the PoC name and does not describe the module's full scope.
