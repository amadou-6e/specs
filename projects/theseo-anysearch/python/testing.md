# Python Testing Specification

## Test Tiers

| Tier | Location | Ray | torch | theseo_core | Speed |
|---|---|---|---|---|---|
| Unit | `tests/unit/` | No | No | No | Fast (~5 s) |
| Integration | `tests/integration/` | Yes | Yes | Yes (auto-built) | Medium (~3 min) |

`theseo_core` is built automatically by `tests/integration/conftest.py::pytest_configure`
via `maturin develop` before collection begins. All integration tests depend on both Ray
and the Rust wheel.

```bash
# Dev loop (no Ray, no Rust)
pytest tests/unit/

# Full stack
pytest tests/unit/ tests/integration/ -m ray

# Integration only (requires Ray + theseo_core)
pytest tests/integration/ -m ray
```

---

## Layout

```
tests/
├── conftest.py                          # shared fixtures + FakeAlgorithm
├── unit/
│   ├── test_models.py                   # Pydantic base models
│   ├── test_settings.py                 # YAML loader + registry resolution
│   ├── test_environments.py             # VoxelEnv + SurfaceEnv (stub, no Rust)
│   ├── test_rewards.py                  # RewardShaper ABC + configs
│   ├── test_trainer.py                  # Trainer ABC + TrainResult.from_rllib() parsing
│   ├── test_experiments.py              # full experiments layer
│   └── test_cli.py                      # CLI help + experiment subcommand smoke tests
└── integration/
    ├── conftest.py                      # pytest_configure (maturin develop) + ray_session fixture
    ├── test_voxel_env.py                # VoxelEnv + PyVoxelEnv reset/step/API     [integration]
    ├── test_surface_env.py              # SurfaceEnv + PySurfaceEnv reset/step/API  [integration]
    ├── test_ppo_trainer_ray.py          # PPOTrainer with real RLlib + VoxelEnv     [ray]
    ├── test_sac_trainer_ray.py          # SACTrainer: build/train/checkpoint/resume [ray]
    ├── test_dqn_trainer_ray.py          # DQNTrainer + RainbowTrainer: train/ckpt   [ray]
    ├── test_experiment_runner_ray.py    # ExperimentRunner end-to-end with Ray      [ray]
    ├── test_cli_ray.py                  # CLI subprocess: run/resume/repeat/tune    [ray]
    ├── test_ray_ppo_real.py             # Standalone PPO smoke test                 [ray]
    └── test_train.py                    # CLI subprocess: experiment run via YAML   [ray, integration]
```

Markers:
- `@pytest.mark.ray` — requires `ray[rllib]`, `torch`, and `theseo_core`
- `@pytest.mark.integration` — used on individual test classes/functions within env test files;
  same requirements as `ray`

All imports use the `theseo_anysearch.*` namespace:
```python
from theseo_anysearch.models import Settings
from theseo_anysearch.rllib.trainer.base import Trainer, TrainResult
from theseo_anysearch.experiments.runner import ExperimentRunner
```

---

## Shared Fixtures (`tests/conftest.py`)

| Fixture | Returns | Purpose |
|---|---|---|
| `minimal_yaml` | `Path` | Minimal valid experiment YAML written to tmp_path |
| `trainer_settings` | `Settings` | PPOConfig + VoxelEncoderConfig; output_dir -> tmp_path |
| `fake_ppo_trainer` | `PPOTrainer` | PPOTrainer whose `_build_algorithm()` returns FakeAlgorithm |

`FakeAlgorithm` (in conftest): duck-typed Algorithm stub visible directly in test source.
- `train() -> dict` with `episode_reward_mean`
- `save(path) -> str` writes sentinel file
- `restore(path) -> None` reads sentinel; raises `FileNotFoundError` if absent

### Integration fixtures (`tests/integration/conftest.py`)

| Fixture | Scope | Purpose |
|---|---|---|
| `ray_session` | session | Initializes Ray once (`num_cpus=1`, no dashboard); shuts down on teardown |

`pytest_configure` hook: runs `maturin develop` from `theseo_anysearch/core/` before
collection if `theseo_core` is not already importable. Uses `sys.executable` (the venv
Python) to avoid picking up system Python.

---

## Unit Tests

### `test_models.py`

| Class | Key tests |
|---|---|
| `TestEnvConfig` | defaults; requires stl_path; rejects extra fields |
| `TestTrainingConfig` | defaults; algorithm required; invalid runner literal rejected |
| `TestAnyscaleConfig` | round-trip; rejects extra |
| `TestAlgorithmConfig` | defaults: lr=3e-4, gamma=0.99, train_batch_size=4096; rejects extra |
| `TestPPOConfig` | inherits AlgorithmConfig; clip_param=0.2, num_sgd_iter=10, lambda_=0.95, kl_coeff=0.2; rejects extra |
| `TestSACConfig` | inherits AlgorithmConfig; tau=0.005, target_entropy="auto", n_step=1 |
| `TestModelConfig` | hidden_sizes=[256,256], activation="relu"; invalid activation rejected |
| `TestVoxelEncoderConfig` | inherits ModelConfig; use_position_encoding=True, encoder_depth=3 |
| `TestSettings` | constructs from all sub-configs; model_cfg alias; round-trip via model_dump(by_alias=True) |

### `test_settings.py`

| Class | Key tests |
|---|---|
| `TestDeepMerge` | shallow override; nested key preserved; nested key overridden |
| `TestLoadSettings` | loads minimal YAML; resolves PPOConfig; resolves VoxelEncoderConfig; unknown algo base fallback; override applied; nested override preserves siblings |

### `test_environments.py`

No Rust required — `_rust_env = None`.

| Class | Key tests |
|---|---|
| `TestVoxelEnv` | obs space keys/shapes; action space Discrete(26); reset() returns (obs, {}); obs values are numpy; reset() twice consistent |
| `TestVoxelEnvStep` | step() raises NotImplementedError when Rust not initialised |
| `TestSurfaceEnv` | agent IDs match count; possible_agents populated; obs space per agent; action space; reset() returns per-agent obs dict |

### `test_rewards.py`

| Class | Key tests |
|---|---|
| `TestRewardShaper` | passthrough; negative reward; scaled multiply; done flag forwarded |
| `TestRewardConfig` | default weight=1.0; custom weight |
| `TestCompositeRewardConfig` | empty shapers list |

### `test_trainer.py`

| Class | Key tests |
|---|---|
| `TestTrainResult` | `from_rllib()` new-API-stack path (env_runners.episode_return_mean); legacy path (episode_reward_mean); missing keys -> 0.0; iteration set; elapsed_s set; extra dict populated |
| `TestExecution` | one TrainResult per iteration; instances are TrainResult; sequential numbers; reward from algo; on_iteration_end each step |
| `TestConfigValidity` | output_dir from settings; iteration count; checkpoint_interval triggers at correct steps |
| `TestOutputSanity` | state.json; iteration in state; episodes_total; latest.json written; latest.json path; weights sentinel; checkpoint dirs created |
| `TestRestore` | restores iteration; restores episodes_total; builds algo if None; calls algo.restore() |
| `TestResume` | False/True by checkpoint presence; restores iteration; remaining iters only; start from restored point |

### `test_experiments.py`

Isolation: `runner_mod._build_trainer` monkey-patched per test using `FakeAlgorithm`; always
restored in `finally`. Mock is explicit in test source — no env var routing.

| Class | Key tests |
|---|---|
| `TestExperimentModels` | single YAML -> ExperimentConfig; PPOConfig typed; VoxelEncoderConfig typed; run_output_dir; sweep YAML -> SweepConfig; expand_sweep; sweep overrides; to_settings() returns Settings |
| `TestOutputStore` | write/read JSON; parent dirs created; exists(); list(); list_dirs(); write_bytes/read_bytes; write_yaml copies source |
| `TestExperimentRunner` | run() -> COMPLETED; 8-char hex run_id; output dir; experiment.yaml; checkpoints at interval |
| `TestExperimentRunnerFailure` | RuntimeError -> FAILED; end_time set |
| `TestExperimentRunnerResume` | resume -> COMPLETED; preserves run_id; unknown run raises; no checkpoint raises |
| `TestExperimentRunnerRepeat` | new run_id; COMPLETED; preserves experiment_name; unknown run raises |
| `TestInspect` | InspectResult; status; checkpoint_iterations; unknown raises |
| `TestListRuns` | empty dir -> []; finds runs |
| `TestSweepConfigExtra` | empty list -> []; base gamma per entry; base env per entry; experiment_name set |

### `test_cli.py`

Uses `typer.testing.CliRunner`. No subprocesses, no Ray.

| Class | Key tests |
|---|---|
| `TestCliHelp` | root help exits 0; mentions train/tune/experiment; train/tune help options present; train missing --stl exits non-zero |
| `TestCliExperimentHelp` | `experiment --help` exits 0; `run/resume/repeat/inspect/list --help` all exit 0 with expected options |

---

## Integration Tests

All integration test files:
```python
ray = pytest.importorskip("ray", reason="ray not installed")
pytestmark = pytest.mark.ray
```

No mock environments, no env var bypasses. All tests run real Ray RLlib with real
`VoxelEnv` backed by `theseo_core.PyVoxelEnv`.

Minimal config used throughout: `train_batch_size=200, iterations=2,
checkpoint_interval=1, max_steps=10, hidden_sizes=[32]`.

Module-scoped fixtures in `test_ppo_trainer_ray.py`, `test_sac_trainer_ray.py`,
`test_dqn_trainer_ray.py`, and `test_experiment_runner_ray.py` limit algorithm builds
to 2–3 per file.

### `test_voxel_env.py`

Tests the Python `VoxelEnv` wrapper and the underlying `theseo_core.PyVoxelEnv` directly.

| Class | Key tests |
|---|---|
| `TestVoxelEnvIntegration` | `_rust_env` is `PyVoxelEnv`; obs space keys/shapes/dtypes; reset returns (dict, {}); steps_remaining normalised; step returns 5-tuple; noop reward < 0.3; episode terminates within max_steps; encode_action returns int |
| _(direct Rust)_ | `PyVoxelEnv.reset()` observation attributes; step decrements steps_remaining; done at max_steps; Place increases fill count; repeated Place on same coord fails |

### `test_surface_env.py`

Tests the Python `SurfaceEnv` wrapper and `theseo_core.PySurfaceEnv` directly.

| Class | Key tests |
|---|---|
| `TestSurfaceEnvIntegration` | `_rust_env` is `PySurfaceEnv`; possible_agents count; reset returns per-agent obs; obs keys/dtypes; steps_remaining normalised; step returns per-agent dicts; agents list clears on done; episode terminates |
| _(direct Rust)_ | `from_surface_coords` builds env; agent state attributes (current, target, reached); step decrements steps_remaining; done at max_steps; agent eventually reaches goal; deterministic reset with same seed |

### `test_ppo_trainer_ray.py`

Module-scoped `trained` fixture runs 2 training iterations once for the whole file.

| Class | Key tests |
|---|---|
| `TestPPOTrainerRayBuild` | algo has `.train()`, `.save()`, `.restore()` |
| `TestPPOTrainerRayTrain` | returns `list[TrainResult]`; count matches iterations; `episode_reward_mean` is finite float; `episodes_total >= 0`; `elapsed_s > 0` |
| `TestPPOTrainerRayCheckpoint` | checkpoint dir created and populated; `state.json` valid JSON with `iteration`; `latest.json` path exists |
| `TestPPOTrainerRayResume` | `_iteration > 0` after restore; matches trained count; `train()` after resume returns list |

### `test_experiment_runner_ray.py`

Module-scoped `run_info`, `resumed_info`, `repeated_info` fixtures limit to 3 algorithm builds.

| Class | Key tests |
|---|---|
| `TestExperimentRunnerRay` | `status == "COMPLETED"`; 8-char hex run_id; `experiment.yaml` in run dir; `checkpoints/` populated; `run.json` has correct experiment name |
| `TestExperimentRunnerRayResume` | resume status COMPLETED; run_id preserved |
| `TestExperimentRunnerRayRepeat` | new run_id; status COMPLETED; separate run dir |

### `test_cli_ray.py`

CLI via subprocess. No `ANYSEARCH_*` env vars. Default timeout 180 s.

| Class | Key tests |
|---|---|
| `TestCliExperimentRun` | exits 0; last JSON `status=COMPLETED`; run dir created; bad config exits non-zero |
| `TestCliExperimentResume` | run then resume exits 0; `status=COMPLETED` |
| `TestCliExperimentRepeat` | run then repeat exits 0; new run_id in JSON |
| `TestCliExperimentInspect` | run then inspect exits 0; `checkpoint_iterations` in JSON |
| `TestCliExperimentList` | run twice then list exits 0; JSON array length >= 2 |
| `TestCliTune` | `tune --num-samples 1 --max-iterations 2` exits 0; JSON has `best_config` and `best_result`; 300 s timeout |

### `test_sac_trainer_ray.py`

Module-scoped `trained` fixture runs 2 SAC iterations; uses `train_batch_size=32`,
`warmup_steps=0`, `replay_buffer_config=MultiAgentPrioritizedReplayBuffer`.

| Class | Key tests |
|---|---|
| `TestSACTrainerRayBuild` | algo has `.train()`, `.save()`, `.restore()` |
| `TestSACTrainerRayTrain` | returns `list[TrainResult]`; count matches iterations; `episode_reward_mean` is finite; `episodes_total >= 0`; `elapsed_s > 0` |
| `TestSACTrainerRayCheckpoint` | checkpoint dir created; `state.json` valid; `latest.json` path exists |
| `TestSACTrainerRayResume` | `_iteration > 0` after restore; matches count; train after resume returns list |

### `test_dqn_trainer_ray.py`

Module-scoped `dqn_trained` and `rainbow_trained` fixtures. DQN: `train_batch_size=32`,
`replay_buffer_capacity=1000`, `warmup_steps=0`. Rainbow: minimal config (`num_atoms=5`,
`n_step=1`, `noisy=false`) for speed.

| Class | Key tests |
|---|---|
| `TestDQNTrainerRayBuild` | algo has `.train()`, `.save()`, `.restore()` |
| `TestDQNTrainerRayTrain` | returns `list[TrainResult]`; count; `episode_reward_mean` finite; `episodes_total >= 0`; `elapsed_s > 0` |
| `TestDQNTrainerRayCheckpoint` | checkpoint dir created; `state.json` valid; `latest.json` path exists |
| `TestRainbowTrainerRayTrain` | returns `list[TrainResult]`; count; `episode_reward_mean` finite; checkpoint dir created |

### `test_ray_ppo_real.py`

Single standalone test (no class). 60 s timeout.

| Test | Assertion |
|---|---|
| `test_ppo_trainer_runs_real_ray_with_real_env` | `PPOTrainer(settings).train()` returns non-empty `list[TrainResult]` |

### `test_train.py`

CLI via subprocess using an inline minimal YAML (2 iterations, batch=200). Marked both
`ray` and `integration`.

| Class | Key tests |
|---|---|
| `TestTrainIntegration` | module-path invocation (`python -m theseo_anysearch.cli.main`) exits 0; `status=COMPLETED`; correct experiment name; user-style invocation from package dir exits 0; no stray `runtime/` dir left in package dir |

---

## What Is Not Tested

| Area | Reason |
|---|---|
| Anyscale runner | Requires live account and cluster |
| Ray Tune BOHB, Optuna, CMA-ES, FLAML | Phase 2/3; not yet implemented |
| GIF pixel content | Brittle; assert file exists with valid header |
| RLlib algorithm internals | Upstream Ray test suite |
| MLflow tracking | Not yet implemented |
| Trajectory protobuf recording | Not yet implemented |
| TD3, DDPG | Require continuous (Box) action space; VoxelEnv/SurfaceEnv are Discrete |

---

## Pytest Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "ray: requires ray[rllib], torch, and theseo_core",
    "integration: used on individual test classes within env test files; same requirements as ray",
]
```
