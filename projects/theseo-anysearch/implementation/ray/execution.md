---
title: Ray actors workers and vectorization investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray execution: investigation plan

Inspect `theseo-anysearch` at pinned `origin/develop`
`fd94554c9620096f94aaed95ffda6a1bbd4711ec` or record a newer exact
revision before changing this plan into contributor guidance.

## Purpose and boundary

Map how AnySearch uses Ray processes, actors, workers, scheduling, resources,
and vectorized environment execution. RLlib's `EnvRunner` configuration API is
documented under [RLlib](../rllib/README.md); this page owns its runtime and
resource consequences, not the evaluation or training contract.

## Evidence to inspect

Inspect `theseo_anysearch/experiments/tune_runner.py`,
`theseo_anysearch/garden/tune_runner.py`, CLI tune/train entry points,
`rllib/algorithms/`, `rllib/trainer/evaluation/parallel.py`, trainer lifecycle
and evaluation coordinator, training/evaluation settings, and tests that use
multiple workers or vectorized environments. Verify actual `ray.init`/shutdown,
remote tasks, actor creation, placement groups, resource declarations, and
environment count propagation; do not infer behavior from setting names alone.

An initial focused test run on `exp/296`
`ed8982e218d39e064965661696f8b6da34bf2bb5` returned **18 passed** for
`test_ppo_rollout_config.py`, `test_parallel_evaluation.py`, and
`test_dqn_runtime.py`. These are unit checks of configuration and helper paths,
not evidence of live multi-actor scheduling or measured vectorization.

## Questions to resolve

- Where is Ray initialized and stopped, and who owns cleanup on failure?
- Which tasks or actors are actually remote, and which loops remain local?
- How are RLlib EnvRunner counts and per-runner vectorization translated into
  processes, environment instances, seeds, and CPU/GPU budgets?
- How do trial concurrency and parallel evaluation interact with training
  resources and worker state? What is serialized or reconstructed remotely?
- Which failures, timeouts, cache paths, and platform constraints have tests?

## Initial source observations

At the pinned revision, `cli/commands/tune.py`, `experiments/tune_runner.py`,
and `rllib/algorithms/ppo.py` contain `ray.init` call sites;
`rllib/trainer/evaluation/parallel.py` configures RLlib evaluation EnvRunners
and contains vectorized collection paths. These observations locate code to
audit; they do **not** establish effective concurrency or resource consumption.

## Deliverable and acceptance

Produce an execution and resource map, failure/cleanup checklist, and test
commands for single-worker, multi-worker, vectorized, and parallel-evaluation
cases. Classify findings **current**, **obsolete**, or **unverified**, with exact
source revision and test evidence. Link behavior to subsystem contracts.
