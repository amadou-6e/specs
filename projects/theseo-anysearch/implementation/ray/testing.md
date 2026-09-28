---
title: Ray testing
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray testing

This page owns test placement and evidence for Ray runtime/process behavior.
[RLlib testing](../rllib/testing.md) owns framework API adaptation, and
[Python testing](../python/testing.md) owns common pytest organization. The
inventory is pinned to product revision
[`fd94554c`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec).
Tests were read, not run at that revision.

## Distributed placement map

There is no top-level `tests/test_ray/` at the pinned revision. Ray crosses
several production concerns, so place each test with the contract it proves.
The tree records existing files, not a proposed reorganization. A file with
`ray` in its name is not sufficient evidence of live execution; inspect its
fixture, marks, and assertions.

```text
tests/
├── conftest.py                                      # shared ray_session fixture
├── test_rllib/
│   ├── test_unit/
│   │   ├── test_ray_runtime_options.py             # init/address/shutdown choices
│   │   ├── test_ppo_rollout_config.py              # requested runner/vectorization settings
│   │   ├── test_parallel_evaluation.py             # evaluation dispatch with doubles
│   │   ├── test_tune_runner_resources.py           # placement requests with doubles
│   │   └── test_tune_lifecycle.py                  # trial lifecycle with doubles
│   └── test_integration/
│       ├── test_tune_runner_ray.py                 # real trials and placement
│       ├── test_ppo_trainer_ray.py                 # real PPO runner/evaluation path
│       ├── test_dqn_trainer_ray.py                 # real DQN/Rainbow path
│       ├── test_sac_trainer_ray.py                 # real SAC path
│       ├── test_cnn_models_ray.py                  # real model training/restore
│       ├── test_ray_ppo_real.py                    # real environment and evaluation
│       └── test_algorithm_coverage.py             # real algorithm trial declarations
├── test_experiments/test_integration/
│   ├── test_execution_train_ray.py                 # run-to-Ray execution boundary
│   ├── test_experiment_runner_ray.py               # run/resume/repeat and output
│   └── test_train.py                               # end-to-end train execution
└── test_cli/test_integration/
    └── test_cli_commands.py                        # Ray-marked run/inspect/resume/repeat cases
```

For runtime lifecycle, assert owned versus external `ray.init` reuse and
shutdown without terminating a caller-owned cluster. For trial/process
boundaries, assert that serialized configuration, extensions, and artifacts
are available inside the trial process, not only on the driver. For resources
and placement, separate requested bundles from actual scheduled actors and
their CPU/GPU assignment. For environment execution, count live EnvRunners
and environment instances and check seed/path behavior. For evaluation,
distinguish dedicated remote runners from local fallback. For measurement,
verify observed throughput and telemetry attribution rather than interpreting
high utilization as training success. These categories correspond to this
folder's runtime, trial, resource, environment, evaluation, and measurement
pages; they are coverage targets, **not claims that existing tests already
prove all of them**.

## Marks, fixtures, and evidence

The root `tests/conftest.py` provides a session-scoped `ray_session` that
initializes local Ray and shuts it down afterward. The CNN integration module
also defines a narrower local fixture. `pyproject.toml` defines `ray` for
tests that start or require a real runtime; root `conftest.py` marks tests
under `test_integration/` as integration. A unit test using a fake worker or
patched Ray call must not acquire the `ray` marker merely because it refers
to Ray settings.

```powershell
python -m pytest -m ray -q
python -m pytest tests/test_rllib/test_integration -m ray -q
```

The first command selects Ray-marked tests across concerns, not every
integration test. Record exact versions, source SHA, test IDs, pass/fail/skip
counts, live actor or process observations when claimed, and cleanup state.
Marking a case or using `ray_session` is not evidence that actor placement,
vectorization, remote evaluation, or multi-node file access occurred. A
single-node local-Ray result does not establish multi-node portability.
