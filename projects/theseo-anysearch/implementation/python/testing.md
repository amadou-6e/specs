---
title: Python testing
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Python testing

This page owns Python test placement by concern, selection, prerequisites, and
evidence limits. [Rust testing](../rust/testing.md) owns native test placement.

Status: source-pinned contributor guide, not a claim that every test passes. Inspected against AnySearch revision [`fd94554c`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec) on 2026-09-28. Tests were read, **not run** at that revision.

## Layout and selection

### Placement rules

Choose the production concern that owns the behavior first, then the test tier.
Add a case to an existing module for the same behavior before creating another
module. Create a new concern directory only for a distinct, stable production
owner with enough tests to justify it—not for one flag, bug, or technique. Name
modules for the behavior or boundary they prove.

- Use `test_unit/` for isolated logic with controlled inputs and doubles. Use
  `test_integration/` when the claim depends on real components working across
  a native, process, RLlib, Ray, or service boundary. A temporary file alone
  does not make a test integration-level; mocked Ray is not a real-Ray test.
- Put genuinely cross-concern fixtures in root `tests/conftest.py`, local
  fixtures in the nearest concern/tier `conftest.py`, and narrow helpers beside
  their consumers. Record optional dependencies, skip behavior, and the CI or
  local selection that exercises each real boundary. Mark real-Ray tests `ray`.
- For a cross-concern scenario, choose the owner of the contract under test,
  name its dependencies, and add a second boundary test only when it proves a
  distinct contract. Keep a Python/native boundary test here and a small
  native invariant test near its Rust owner when both are needed.

### Annotated target tree

This is the existing placement target at the pinned revision, **not** a
reorganization. Every displayed path exists; nonlisted sibling files stay put.
Comments identify the concern and boundary used to place new tests. Flat
concerns do not yet have invented tier directories.

```text
tests/
├── conftest.py                            # cross-concern fixtures; integration auto-mark
├── test_cli/                              # command parsing, validation, output
│   ├── test_unit/
│   │   ├── test_cli.py                    # dispatch and arguments
│   │   └── test_tune_validation.py        # CLI-side validation
│   └── test_integration/test_cli_commands.py  # actual CLI process boundary
├── test_environments/                     # actions, lifecycle, observations, exports
│   ├── test_unit/
│   │   ├── test_action_spaces.py           # action-space logic
│   │   └── test_shape_collision.py         # collision behavior
│   └── test_integration/
│       ├── conftest.py                     # environment-integration fixtures
│       └── test_voxel_env_core.py          # native environment boundary
├── test_experiments/                      # run orchestration and artifacts
│   ├── test_unit/
│   │   ├── conftest.py                     # experiment-unit fixtures
│   │   ├── _support.py                     # local helper, not a test
│   │   ├── test_experiment_runner_run.py   # run lifecycle
│   │   └── test_trajectory_storage.py      # trajectory storage
│   └── test_integration/
│       ├── test_execution_train_ray.py     # real Ray run
│       └── test_native_extensions.py       # compiled extension in a run
├── test_garden/test_unit/                 # model-garden data and store
│   ├── test_garden_dataset.py
│   └── test_garden_store.py
├── test_heuristic/                        # flat: factory and voxel strategies
│   ├── test_factory.py
│   └── test_voxel_strategies.py
├── test_imitation/                        # flat: demonstrations and pretraining
│   ├── test_cache.py
│   └── test_imitation_preflight.py
├── test_rllib/                            # algorithms, models, trainer, explain
│   ├── test_unit/
│   │   ├── _tune_runner_support.py         # local helper, not a test
│   │   ├── test_dqn_runtime.py             # adapter-specific logic
│   │   ├── test_tune_runner_resources.py   # existing placement; review owner
│   │   └── test_explain/test_policy_scorer.py  # nested explain concern
│   └── test_integration/
│       ├── test_algorithm_coverage.py      # declared algorithm trials
│       └── test_ppo_trainer_ray.py         # real-Ray trainer
├── test_settings/test_unit/              # configuration models
│   ├── test_heterogeneous_agents.py
│   └── test_scenarios.py
├── test_world_providers/                 # flat: acquisition, cache, service
│   ├── test_aerialgym_provider.py
│   └── test_source_cache.py
└── test_worlds/                          # compile, residency, route feasibility
    ├── test_unit/
    │   ├── test_compiler.py
    │   └── test_residency.py
    └── test_integration/
        ├── test_obstacle_waypoint_preflight.py  # feasibility boundary
        └── test_seeded_gate_catalog.py          # cross-concern world scenario
```

The pinned [test tree](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests)
contains 152 Python test modules across these ten concerns. Use this map when
filing a test:

| Concern | Keep together | Representative evidence |
| --- | --- | --- |
| CLI | Dispatch, command validation and real invocation. | [unit](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_cli/test_unit/test_cli.py), [integration](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_cli/test_integration/test_cli_commands.py) |
| Environments | Actions, task lifecycle, shapes, rewards, observations and export conversion. | [actions](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_environments/test_unit/test_action_spaces.py), [native boundary](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_environments/test_integration/test_voxel_env_core.py) |
| Experiments | Loading/preflight, run/resume, recipes, output/tracking, trajectories, native execution. | [runner](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_experiments/test_unit/test_experiment_runner_run.py), [trajectory](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_experiments/test_unit/test_trajectory_storage.py) |
| Garden | Augmentation, dataset configuration/data, store. | [dataset](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_garden/test_unit/test_garden_dataset.py) |
| Heuristic | Factory and voxel strategies. | [strategies](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_heuristic/test_voxel_strategies.py) |
| Imitation | Cache, providers, collection, preflight, models and pretraining. | [cache](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_imitation/test_cache.py), [preflight](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_imitation/test_imitation_preflight.py) |
| RLlib | Algorithm/model adapters, trainer/evaluation/curriculum, Tune resources, explain and real training. | [DQN](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_dqn_runtime.py), [explain](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_explain/test_policy_scorer.py) |
| Settings | Field declarations, heterogeneous/scenario/evaluation settings. | [fields](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_settings/test_unit/test_configuration_field_declarations.py) |
| World providers | Source adapters, cache, service and optional extras. | [provider](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_world_providers/test_aerialgym_provider.py), [cache](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_world_providers/test_source_cache.py) |
| Worlds | Artifacts, candidates, compilation, manifests, overview, residency and route feasibility. | [compiler](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_worlds/test_unit/test_compiler.py), [route feasibility](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_worlds/test_integration/test_obstacle_waypoint_preflight.py) |

Existing locations that deserve an ownership review—not automatic moves—include
[`test_experiment_cli.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_experiments/test_unit/test_experiment_cli.py)
under experiments, the `test_tune_runner_*` modules under RLlib that test
`experiments/tune_runner.py`, and environment export tests versus provider
acquisition tests. Decide from the principal assertion. If moving a test,
preserve marks, fixtures, CI selectors and assertion coverage; do not rearrange
all existing tests merely for symmetry.

Pytest discovers `tests/`, grouped by domains including `test_cli`, `test_environments`, `test_experiments`, `test_rllib`, `test_worlds`, `test_garden`, `test_settings`, `test_heuristic`, `test_imitation`, and `test_world_providers`. Some groups contain nested `test_unit` and `test_integration` directories; there are no root `tests/unit/` or `tests/integration/` trees. Root [`tests/conftest.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/conftest.py) auto-marks tests below a `test_integration` directory. [`pyproject.toml`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/pyproject.toml) defines `integration` for multiple components or external processes and `ray` for a real Ray runtime excluded from fast CI.

The product [`README.md`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/README.md) recommends this lightweight selection:

```powershell
python -m pytest -m "not ray and not integration" -q
```

The expression selects tests; it does **not** promise dependency-free collection. For focused work, select a domain path or node ID and inspect its marks and imports. `-m ray` selects Ray-marked tests, not all integration tests. A full `python -m pytest` may involve a native build and real Ray tests, depending on installation and selection.

## Prerequisites and fixtures

The [`README.md`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/README.md) setup installs the editable package with `dev` and `torch-cpu` extras plus Maturin, then builds `theseo_core` using `python -m maturin develop --release --manifest-path theseo_anysearch/core/Cargo.toml`. The core dependency is `ray[default,rllib]`; Torch is optional ([`pyproject.toml`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/pyproject.toml)). Some unmarked tests import optional libraries, so resolve prerequisites for each selected test.

Root [`tests/conftest.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/conftest.py) provides temporary paths and per-test `.anysearch` registry isolation. When the installed native wheel is stale, collection can attempt `[sys.executable, "-m", "maturin", "develop"]`; a failed build warns rather than aborting immediately, so a skipped native test is not a pass. Its session-scoped `ray_session` fixture starts Ray with four CPUs and shuts it down afterward. These are fixture implementations, not proof that every test exercises them successfully.

## Evidence boundary

[`local-tests.yml`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/.github/workflows/local-tests.yml) builds a Rust wheel, installs it for Python jobs, and runs selected groups with exclusions, not every Python test. [`ray-cli-tests.yml`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/.github/workflows/ray-cli-tests.yml) separately runs Ray-marked CLI integration tests. A marker or job defines intended selection, not current passing status. Inspect exact assertions and a recorded run before claiming behavior is verified.

See [Rust testing](../rust/testing.md) for Cargo and native-binding checks, [RLlib compatibility and testing](../rllib/compatibility-and-testing.md) for algorithm and checkpoint compatibility, and [Ray implementation](../ray/README.md) for distributed execution evidence. Subsystem contracts own user-visible acceptance criteria.
