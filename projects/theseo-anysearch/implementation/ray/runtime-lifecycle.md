---
title: Ray runtime lifecycle
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray runtime lifecycle

Source baseline: [`theseo-anysearch` fd94554c](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected 2026-09-28. Ray integration tests at this revision were read, not run. This page concerns runtime ownership, not RLlib configuration or training guarantees.

## Entry points and ownership

The lifecycle is entry-point-specific; there is no single repository-wide Ray owner:

| Entry point | Initialization and reuse in source | Normal cleanup in source |
| --- | --- | --- |
| Standalone algorithm builders | The shared `_ensure_ray_runtime` first sets RLlib's default storage under the output directory. It reuses an already initialized Ray runtime; otherwise it starts local Ray with an output-derived `_temp_dir`, no dashboard, and `max(num_env_runners + 1, 1)` CPUs. This CPU value is an initialization request, not measured actor capacity. [PPO helper](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L68-L115) | The helper does not itself call `ray.shutdown()`. Its caller's lifetime must be assessed separately. [PPO helper](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/algorithms/ppo.py#L78-L115) |
| Experiment `TuneRunner` | It records whether Ray was initialized and calls `ray.init` with either the configured external address or a local `_temp_dir`, never both. The local temp directory can be configured independently of Tune's persistent `storage_path`. [options and ownership predicate](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L963-L990), [storage and initialization](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1240-L1252) ([temp/init](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1298-L1310)) | Its `finally` calls `ray.shutdown()` when the explicit `shutdown_ray_on_complete` override says so, or by default only when this invocation initialized a local runtime. A preinitialized or external runtime is therefore not shut down by default. [ownership predicate](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L976-L990), [cleanup](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1550-L1557) |
| Legacy CLI Tune command | It uses the resolved output directory for Tune storage and a short process-specific system-temp path for local Ray, to reduce Windows path length. [CLI setup](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/cli/commands/tune.py#L955-L985) | It calls `ray.shutdown()` in `finally` after its Tune execution; unlike `TuneRunner`, this path has no preexisting-runtime ownership predicate. [CLI cleanup](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/cli/commands/tune.py#L1033-L1102) |
| Garden Tune | It initializes Ray only if not already initialized, without the experiment runner's explicit external-address/temp-directory policy. [Garden runner](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/garden/tune_runner.py#L138-L160) | No shutdown appears in this runner's `run` method; do not assume this method owns the runtime. [Garden runner](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/garden/tune_runner.py#L138-L202) |

`TuneRunner` initializes Ray **before** entering the `try/finally` that contains shutdown. A failure in `ray.init` or the intervening setup therefore bypasses that cleanup block; the effect on any partially started Ray processes is unverified. A process crash or forced termination likewise is not covered by the source-level `finally` guarantee. Neither a `ray.shutdown()` call nor this source inspection proves temporary files are deleted. [Initialization](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1304-L1310), [later setup and cleanup](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1311-L1557).

## Verification boundary

These are source-path findings, not observed lifecycle guarantees. The pinned-revision Ray tests were read, not run for this investigation. Verify fresh and preinitialized local runtimes, external-address mode, successful and failed Tune execution, and `ray.init` failure; inspect process state and persistent artifacts separately. Keep Tune trial-local `Algorithm.stop()` behavior in [trial boundaries](trials-and-process-boundaries.md), and reservations versus live actor placement in [resources](resources-and-placement.md).
