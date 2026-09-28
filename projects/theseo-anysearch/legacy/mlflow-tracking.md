---
title: Historical MLflow tracking
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

> Historical source; not an authoritative current specification.

# MLflow Tracking

Every training run and tuning run logs hyperparameters, per-iteration metrics,
and artifacts to MLflow so that results are searchable, comparable, and
reproducible from the UI.

The high-level shape is specified in `spec/experiments.md` (MLflow Integration
section). This document adds the implementation-level detail: class design, exact
param/metric names, artifact conventions, and error handling.

---

## Configuration

`MLflowConfig` is an optional section in the experiment YAML:

```yaml
mlflow:
  tracking_uri: null      # null → defaults to sqlite:///experiments/mlflow.db (see below)
  experiment_name: null   # null → uses experiment.name from YAML
  artifact_store: null    # null → MLflow default artifact root
```

### Tracking URI resolution

`ExperimentRunner` resolves the effective tracking URI before constructing
`MLflowTracker`, via `_resolve_mlflow_config()`:

| YAML | Effective URI |
|---|---|
| `mlflow:` key absent | Tracking disabled (no-op) |
| `tracking_uri: "http://..."` | Used as-is |
| `tracking_uri: null` (or `mlflow: {}`) | `sqlite:///experiments/mlflow.db` relative to CWD |

The SQLite default is pinned to `experiments/mlflow.db` in the current working
directory (wherever `anysearch experiment run` is invoked). This avoids
interference from system-level `MLFLOW_TRACKING_URI` environment variables.

Launch the UI against this DB:

```bash
mlflow ui --backend-store-uri sqlite:///experiments/mlflow.db
```

Pydantic model (already declared in `experiments/models.py`):

```python
class MLflowConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tracking_uri: str | None = None
    experiment_name: str | None = None   # override; defaults to experiment.name
    artifact_store: str | None = None
```

If the `mlflow:` key is absent from the YAML, tracking is **disabled** and
`MLflowTracker` operates in no-op mode — no import of `mlflow` occurs, so
the dependency is optional at runtime.

---

## `MLflowTracker` Class

Module: `theseo_anysearch/experiments/tracking.py`

```python
class MLflowTracker:
    """
    Thin, stateful wrapper around the mlflow client.

    All public methods are no-ops when tracking is disabled (mlflow_config is None).
    Nesting (parent/child runs for tuning) is managed internally.
    """

    def __init__(
        self,
        mlflow_config: MLflowConfig | None,
        experiment_name: str,
    ) -> None:
        self._enabled = mlflow_config is not None
        if not self._enabled:
            return
        import mlflow
        if mlflow_config.tracking_uri:
            mlflow.set_tracking_uri(mlflow_config.tracking_uri)
        self._experiment_name = mlflow_config.experiment_name or experiment_name
        mlflow.set_experiment(self._experiment_name)
        self._run_id: str | None = None

    # ------------------------------------------------------------------
    # Run lifecycle
    # ------------------------------------------------------------------

    def start_run(self, run_name: str, tags: dict | None = None) -> str | None:
        """Open a new MLflow run. Returns the mlflow run_id or None if disabled."""

    def start_child_run(self, run_name: str, tags: dict | None = None) -> str | None:
        """Open a nested child run (for tuning trials). Returns run_id or None."""

    def end_run(self, status: str = "FINISHED") -> None:
        """End the active run (or child run). status: FINISHED | FAILED | KILLED."""

    def end_child_run(self, status: str = "FINISHED") -> None:
        """End the innermost nested run without ending the parent."""

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def log_params(self, params: dict[str, Any]) -> None:
        """Log a flat dict of hyperparameters. Called once at run start."""

    def log_metrics(self, metrics: dict[str, float], step: int) -> None:
        """Log one dict of metrics at the given step (iteration number)."""

    def log_artifact(self, local_path: str | Path) -> None:
        """Upload a local file or directory to the active run's artifact store."""

    def set_tag(self, key: str, value: str) -> None:
        """Set a string tag on the active run."""

    @property
    def run_url(self) -> str | None:
        """
        Return the tracking URL for the active run, or None if disabled.
        Format: {tracking_uri}/#/experiments/{exp_id}/runs/{run_id}
        """
```

### No-op contract

Every method checks `if not self._enabled: return` before any mlflow import.
This ensures that:

- Projects without `mlflow` installed can still run experiments; they just will not
  have tracking.
- Unit tests never need a live MLflow server.
- The `MLflowTracker` can be constructed unconditionally in `ExperimentRunner` —
  callers do not need to guard against `None`.

---

## Training Run

### Params logged at run start

All params are logged as a flat dict. Nested config keys use dot notation:
`algorithm_config.lr`, `env.agent_count`, etc.

| Param key | Source |
|---|---|
| `algorithm` | `training.algorithm` |
| `runner` | `training.runner` |
| `iterations` | `training.iterations` |
| `checkpoint_interval` | `training.checkpoint_interval` |
| `trajectory_every` | `training.trajectory_every` |
| `best_trajectory` | `training.best_trajectory` |
| `env.stl_path` | `env.stl_path` |
| `env.agent_count` | `env.agent_count` |
| `env.max_steps` | `env.max_steps` |
| `env.seed` | `env.seed` |
| `env.obs_mode` | `env.obs_mode` |
| `env.box_radius` | `env.box_radius` (if obs_mode == "box") |
| `algorithm_config.*` | All fields from the resolved AlgorithmConfig |
| `model_config.custom_model` | If set |
| `model_config.hidden_sizes` | If no custom_model |
| `model_config.activation` | If no custom_model |
| `experiment_name` | `experiment.name` |
| `run_id` | Project run_id (8-char hex) |

### Metrics logged per iteration

Logged via `log_metrics(metrics, step=iteration)` after each training step:

| Metric key | Source |
|---|---|
| `episode_reward_mean` | `TrainResult.episode_reward_mean` |
| `episode_len_mean` | `TrainResult.episode_len_mean` |
| `episodes_total` | `TrainResult.episodes_total` |
| `elapsed_s` | `TrainResult.elapsed_s` |

### Artifacts logged

| Trigger | What is logged |
|---|---|
| Run start | `experiment.yaml` (config snapshot) |
| Each checkpoint | The `checkpoints/iter_XXXXXX/` directory |
| Each trajectory file | `trajectories/iter_XXXXXX.pb` and `trajectories/best.pb` when updated |

Artifact logging is best-effort: failures are caught and printed as warnings
rather than aborting the training run.

### Integration with `ExperimentRunner`

```python
# In ExperimentRunner.run():
tracker = MLflowTracker(self._config.mlflow, self._config.experiment.name)
run_mlflow_id = tracker.start_run(run_name=run_id, tags={"project_run_id": run_id})
run_info.mlflow_run_url = tracker.run_url

tracker.log_params(_flatten_config(self._config))
tracker.log_artifact(run_dir / "experiment.yaml")

# Wire metrics into trainer hook:
def _hook(result: TrainResult) -> None:
    tracker.log_metrics({
        "episode_reward_mean": result.episode_reward_mean,
        "episode_len_mean": result.episode_len_mean,
        "episodes_total": result.episodes_total,
        "elapsed_s": result.elapsed_s,
    }, step=result.iteration)

trainer.on_iteration_end = _compose(trainer.on_iteration_end, _hook)

try:
    trainer.train()
    tracker.end_run("FINISHED")
except Exception:
    tracker.end_run("FAILED")
    raise
```

`_flatten_config(config)` recursively traverses the Pydantic model hierarchy
and returns a flat `dict[str, str]` with dotted keys. MLflow requires param
values to be strings or numbers; complex types (lists, dicts) are JSON-encoded.

---

## Tuning Run

A tuning run uses MLflow nested runs: one **parent run** for the sweep and one
**child run** per trial.

### Parent run

Opened before any trial starts. Params logged:

| Param key | Source |
|---|---|
| All base config params | Same as training run (see above) |
| `tune.scheduler` | `tune_config.scheduler` |
| `tune.num_samples` | `tune_config.num_samples` |
| `tune.metric` | `tune_config.metric` |
| `tune.mode` | `tune_config.mode` |
| `tune.search_space` | JSON-encoded search space dict |

### Child run (per trial)

Opened at trial start, closed at trial end.

Params logged at trial start:

| Param key | Value |
|---|---|
| `trial_id` | Ray Tune trial id |
| `algorithm_config.*` | Sampled hyperparameter values for this trial |

Metrics logged per trial iteration: same set as training run.

At parent run end, the following summary metrics are logged on the parent run:

| Metric key | Value |
|---|---|
| `best_trial_metric` | Best metric value across all completed trials |
| `num_trials_completed` | Count of COMPLETED trials |
| `num_trials_failed` | Count of FAILED trials |

And the best trial's id is set as a tag: `best_trial_id`.

### Integration with `TuneRunner`

```python
# In TuneRunner.run():
tracker = MLflowTracker(config.mlflow, config.experiment.name)
tracker.start_run(run_name=f"{config.experiment.name}-tune", tags={"kind": "tune"})
tracker.log_params(_flatten_tune_config(config))

def _trainable(trial_config: dict) -> None:
    child_run_id = tracker.start_child_run(run_name=trial_config["trial_id"])
    tracker.log_params({f"algorithm_config.{k}": v
                        for k, v in trial_config.items()})
    try:
        # ... run trial ...
        for result in trial_results:
            tracker.log_metrics({...}, step=result.iteration)
        tracker.end_child_run("FINISHED")
    except Exception:
        tracker.end_child_run("FAILED")
        raise

# After tune finishes:
tracker.log_metrics({
    "best_trial_metric": best_metric,
    "num_trials_completed": n_completed,
    "num_trials_failed": n_failed,
}, step=0)
tracker.set_tag("best_trial_id", best_trial_id)
tracker.end_run("FINISHED")
```

---

## `_flatten_config` Helper

```python
def _flatten_config(config: ExperimentConfig) -> dict[str, Any]:
    """
    Recursively flatten a Pydantic model to a dict with dotted keys.
    Complex values (list, dict) are JSON-encoded.
    Excludes fields not relevant to ML tracking (e.g. output_dir, mlflow itself).

    Example:
        {"env": {"agent_count": 4, "max_steps": 200}}
        → {"env.agent_count": 4, "env.max_steps": 200}
    """
```

Excluded top-level keys: `anyscale`, `renders`, `mlflow`, `experiment.output_dir`.

---

## Error Handling

All mlflow calls are wrapped in try/except to prevent tracking failures from
aborting training:

```python
def log_metrics(self, metrics, step):
    if not self._enabled:
        return
    try:
        import mlflow
        mlflow.log_metrics(metrics, step=step)
    except Exception as exc:
        warnings.warn(f"MLflow log_metrics failed: {exc}", stacklevel=2)
```

The pattern is consistent across all logging methods.

---

## Testing

### Unit tests (`tests/unit/test_tracking.py`)

| Test | What it covers |
|---|---|
| `test_noop_when_disabled` | `MLflowTracker(None, ...)` — all methods return without error |
| `test_run_url_none_when_disabled` | `tracker.run_url is None` |
| `test_flatten_config_dotted_keys` | `_flatten_config` produces expected flat dict |
| `test_flatten_config_excludes_mlflow` | `mlflow` key absent from result |
| `test_flatten_config_list_json_encoded` | `hidden_sizes` → JSON string |
| `test_log_params_called_with_flat_dict` | `mlflow.log_params` receives flat dict (mock) |
| `test_log_metrics_called_with_step` | `mlflow.log_metrics` receives correct step arg (mock) |
| `test_end_run_called_on_failure` | Exception in trainer → `end_run("FAILED")` called (mock) |
| `test_child_run_lifecycle` | `start_child_run` / `end_child_run` maintains correct nesting (mock) |

Tests mock `mlflow` at the module level (`unittest.mock.patch("mlflow.start_run", ...)`).
No live MLflow server is required.

### Integration test note

A live-MLflow integration test is out of scope for the unit tier. End-to-end
validation is done manually against a local `mlflow server` instance.

---

## Implementation Order

1. Add `MLflowConfig` fields `experiment_name` to Pydantic model (already partially exists)
2. Add `best_trajectory: bool = True` to `TrainingConfig` (also needed by trajectory spec)
3. Implement `_flatten_config` in `experiments/tracking.py`
4. Implement `MLflowTracker` with no-op fallback
5. Wire `MLflowTracker` into `ExperimentRunner.run()`
6. Wire child runs into `TuneRunner.run()`
7. Write unit tests (mock mlflow throughout)
8. Update `spec/experiments.md` to reference this document for implementation detail
