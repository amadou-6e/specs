# Known Bugs and Production Incidents

This document records non-obvious bugs that have been observed in production,
explains their root cause, and describes the fixes applied.  Some are
environment-specific (Windows path limits, GPU driver behaviour) and cannot
be caught by the standard unit-test suite without real hardware or OS.

---

## 1. Windows MAX_PATH — Ray cannot write internal state files

### Symptom

`anysearch experiment run --config ...` (or `TuneRunner.run()`) raises:

```
FileNotFoundError: [Errno 2] No such file or directory:
  'C:\...\long\path\driver_artifacts\.uuid-tmp-basic-variant-state-YYYY-MM-DD.json'
```

The error appears during the sweep (after trials have started) inside Ray Tune's
internal checkpoint logic, not inside training code.

### Root cause

Ray Tune writes its own internal bookkeeping under two roots:

| Root | Purpose |
|---|---|
| `ray.init(_temp_dir=...)` | Session temp: actor logs, object store sockets |
| `RunConfig(storage_path=...)` + `name=...` | `{storage_path}/{name}/driver_artifacts/` — search algorithm state, basic-variant-state.json |

Under each root Ray appends several path segments:
- `session_YYYY-MM-DD_HH-MM-SS_MICROSECONDS_PID/` (~40 chars)
- `artifacts/YYYY-MM-DD_HH-MM-SS/` (~30 chars)
- `{experiment_name}/driver_artifacts/` (~30 chars)
- `.{uuid4}-tmp-basic-variant-state-YYYY-MM-DD_HH-MM-SS.json` (~80 chars)

When these roots are inside a deep workspace directory (e.g.
`C:\Users\username\Documents\CodeWorkspace\theseo-anysearch\`) the combined
path length exceeds Windows' default MAX_PATH limit of **260 characters**.

Windows cannot create the file, `open()` raises `FileNotFoundError`, and
Ray Tune propagates the exception — killing the entire sweep.

A secondary issue: Ray joins the storage_path (often using forward slashes from
YAML) with internal suffixes using `os.path.join` (backslashes on Windows).
The resulting mixed-separator path is also rejected by `open()`.

### Fix applied

**`TuneRunner.run()`** now routes Ray's internal files to the system temp dir
instead of the user's `output_dir`:

```python
# Ray internal bookkeeping → short system temp path
storage_path = os.path.normpath(os.path.join(tempfile.gettempdir(), "anysearch_tune"))

# Ray session temp → short system temp path
ray_temp_dir = os.path.join(tempfile.gettempdir(), f"anysearch_tune_{os.getpid()}")
```

Training artifacts (model checkpoints, trajectories, videos, MLflow data) are
**not** affected — `_experiment_trainable` writes those directly to
`output_dir/run_tag/trial_id/`, which is fully under our control.

The `apply_win_atomic_save_patch()` function in `tune_runner.py` additionally
normalises mixed separators via `os.path.normpath` and emits an actionable
error message if a `FileNotFoundError` still occurs.

### User override

If the default temp location is undesirable (e.g. network temp dir, temp
partition too small), set either or both in your YAML:

```yaml
tune_config:
  ray_storage_dir: C:/ray_tmp   # where Ray Tune writes driver_artifacts & search state
  ray_temp_dir: C:/ray_tmp      # where Ray writes session temp files (actor logs, etc.)
```

Both fields default to the system temp dir.  Only override if you see this error
or need Ray's internal state to survive across runs (e.g. for sweep resume).

### Trade-off

Ray's internal trial-checkpoint state (used by `Tuner.restore()` to resume an
interrupted sweep) now lives in system temp and may be cleaned up on reboot.
Training outputs and MLflow data are unaffected.

---

## 2. Placement group bundle index invalid — `ValueError: bundle index N is invalid`

### Symptom

During a Ray Tune sweep, one or more trials crash with:

```
ValueError: placement group bundle index 1 is invalid.
            Valid placement group indexes: 0-1
```

The error format `0-{bundle_count}` means `bundle_count=1` — the trial actor's
placement group has only 1 bundle, but RLlib tried to schedule an env-runner
worker at bundle index 1+.

Observed in production at trial ~6 of a 30-trial ASHA sweep
(`multi_agent_ppo_asha.yaml`, tag `v10`).

### Root cause (two distinct mechanisms)

#### 2a. SIGSEGV in theseo_core corrupts the raylet

`theseo_core` (Rust via PyO3) runs inside raylet-managed remote actor processes
when `num_env_runners > 0`.  If the Rust code SIGSEGV-crashes, the raylet
process itself is killed.

When the raylet restarts, the GCS (Global Control Store) loses its accurate
bundle cache for existing placement groups.  The next time a trial asks for
its placement group's `bundle_count`, the GCS returns 1 (a stale/empty cache
entry) instead of the real count (e.g. 13 for 12 env runners + 1 driver).

When RLlib's `EnvRunnerGroup._make_worker()` tries to schedule worker 1 at
`pg_bundle_idx = pg_offset + worker_index = 0 + 1 = 1`, Ray raises
`ValueError` because `bundle_count=1` means only bundle 0 exists.

#### 2b. Stale placement group refs from `reuse_actors=True`

With `reuse_actors=True`, Ray Tune reuses the same trial actor across
consecutive trials.  After ~14 trials the actor's internal PG bundle
references become stale: the old placement group is released but the actor
still holds indices into it.  New trials scheduled on the reused actor inherit
these stale refs, causing `bundle index N is invalid` at trial ~14.

### Fixes applied

**Fix for 2a — `num_env_runners: 0` in YAML:**

```yaml
training:
  num_env_runners: 0   # run rollouts in the trial actor, not raylet workers
```

With `num_env_runners=0`, RLlib runs the env (including the Rust code) inside
the trial actor process.  A SIGSEGV kills the trial actor but **not the
raylet**.  The raylet stays healthy, subsequent trials allocate PGs correctly,
and `bundle_count` is always accurate.

This is the current default in `usage/experiments/tune/multi_agent_ppo_asha.yaml`.

**Fix for 2b — `reuse_actors=False` in `TuneRunner`:**

```python
tune_config=ray_tune.TuneConfig(
    reuse_actors=False,   # each trial gets a fresh actor with a fresh PG
    ...
)
```

Applied unconditionally in `TuneRunner.run()`.  Running 16 consecutive trials
with `reuse_actors=False` passes without errors; with `reuse_actors=True` the
same test fails around trial 14.

### Placement group sizing

`TuneRunner` declares a `PlacementGroupFactory` with `1 + num_env_runners`
bundles:

- Bundle 0 → trial actor (driver)
- Bundles 1..N → env runner workers

**Critical ordering:** `with_resources` must wrap the base function **before**
`with_parameters`.  Applying `with_resources` after `with_parameters` silently
drops the `PlacementGroupFactory` in the current Ray version, reverting to a
1-bundle PG and triggering the error for any `num_env_runners > 0`.

```python
# Correct
trainable = ray_tune.with_parameters(
    ray_tune.with_resources(fn, pgf),   # pgf applied first
    **kwargs,
)

# Wrong — pgf is silently dropped
trainable = ray_tune.with_resources(
    ray_tune.with_parameters(fn, **kwargs),
    pgf,
)
```

### Regression tests

- `tests/integration/test_tune_runner_ray.py::TestBundleIndexWithRealRay` —
  three tests using a real Ray cluster (no theseo_core required) that verify
  bundle_count, actor spawning at bundle 1, and consecutive trial freshness.
- `tests/integration/test_tune_runner_ray.py::TestStalePGRefsRegression` —
  16 consecutive trials to verify `reuse_actors=False` holds above the failure
  threshold (requires theseo_core).
