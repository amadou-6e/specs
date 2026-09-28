---
title: Test organization by concern
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Test organization by concern

This is a proposed placement guide for contributors, grounded in the product tree at [`fd94554c9620096f94aaed95ffda6a1bbd4711ec`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected on 2026-09-28. The inventory describes files read, **not tests run**. The placement rules below are guidance to review and adopt; the current tree and CI do not enforce every rule. The [Python](python/testing.md) and [Rust](rust/testing.md) testing pages own commands, prerequisites, and evidence limits. Subsystem specifications own behavioral acceptance criteria.

## Placement rule

Choose the **production concern that owns the behavior** first, then the test tier. Add a case to an existing module for the same behavior before creating another module. Create a new concern directory only when there is a distinct, stable production owner and enough tests to justify it; do not create a new directory for one feature flag, bug, or test technique. Name modules for the behavior or boundary they prove, not for a contributor, ticket, or arbitrary batch.

1. Identify the module or contract whose regression the test would diagnose. Put the test under its existing concern root. If several components participate, choose the owner of the boundary under test and name its dependencies explicitly.
2. Use `test_unit/` for isolated logic with controlled inputs and doubles. Use `test_integration/` when the claim depends on components working together across a real boundary, such as a native wheel, process, RLlib trainer, Ray runtime, or service. A temporary file alone does not make a test integration-level; a test using a mock Ray actor does not become a real-Ray integration test.
3. Put broadly reusable, genuinely cross-concern fixtures in root `tests/conftest.py`. Keep concern-specific fixtures in the nearest local `conftest.py`, and narrow helpers beside their callers. Avoid a global fixture merely because two unrelated tests happen to need similar setup.
4. Record optional dependencies and the intended selection gate. A skip, collection success, or a registered algorithm is not evidence that the tested behavior ran. When a real Ray runtime is required, use the `ray` marker in addition to the appropriate concern and tier.
5. For cross-language behavior, keep a small native test near the Rust implementation and a Python integration test at the exposed binding or workflow boundary. Link the two in a review or test plan; do not copy every assertion into both languages.

At the pinned revision, [`tests/conftest.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/conftest.py) marks paths containing `test_integration`, while [`pyproject.toml`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/pyproject.toml) defines `integration` and `ray` markers. This is a selection mechanism, not a comprehensive architecture check. Some existing concerns have flat test layouts; the guidance does not require moving them merely to make the tree symmetrical.

## Python concern map

The [`tests/` tree](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests) has 152 Python test modules across these ten roots. The examples indicate *where a new case should be considered*, not that every case presently passes.

### Annotated existing target tree

This is the **existing placement target** at the pinned revision, not a proposed
reorganization. Each displayed path exists; omitted sibling files remain where
they are. Comments explain the concern, tier, and boundary for choosing a home
for a new test. A flat concern has no invented `test_unit/` or `test_integration/`
directory. See the linked concern table below for exact source links.

```text
tests/
├── conftest.py                            # cross-concern fixtures; auto-mark integration paths
├── test_cli/                              # CLI command contract
│   ├── test_unit/
│   │   ├── test_cli.py                    # dispatch/arguments without real command boundary
│   │   └── test_tune_validation.py        # CLI-side validation
│   └── test_integration/
│       └── test_cli_commands.py           # actual CLI invocation
├── test_environments/                     # environment actions, observations, lifecycle, exports
│   ├── test_unit/
│   │   ├── test_action_spaces.py           # action-space logic
│   │   └── test_shape_collision.py         # collision behavior
│   └── test_integration/
│       ├── conftest.py                     # environment-integration fixtures only
│       └── test_voxel_env_core.py          # native environment boundary
├── test_experiments/                      # experiment/run orchestration and artifacts
│   ├── test_unit/
│   │   ├── conftest.py                     # experiment-unit fixtures only
│   │   ├── _support.py                     # adjacent helper, not a test module
│   │   ├── test_experiment_runner_run.py   # run orchestration
│   │   └── test_trajectory_storage.py      # trajectory format/storage
│   └── test_integration/
│       ├── test_execution_train_ray.py     # real Ray execution boundary
│       └── test_native_extensions.py       # compiled extension in a run
├── test_garden/test_unit/                 # model-garden data and store
│   ├── test_garden_dataset.py
│   └── test_garden_store.py
├── test_heuristic/                        # flat: heuristic factory and strategies
│   ├── test_factory.py
│   └── test_voxel_strategies.py
├── test_imitation/                        # flat: demonstration/pretraining concern
│   ├── test_cache.py
│   └── test_imitation_preflight.py
├── test_rllib/                            # RLlib adapters, models, trainers, explain
│   ├── test_unit/
│   │   ├── _tune_runner_support.py         # adjacent helper, not a test module
│   │   ├── test_dqn_runtime.py             # adapter-specific logic
│   │   ├── test_tune_runner_resources.py   # current RLlib-root placement; review boundary
│   │   └── test_explain/
│   │       └── test_policy_scorer.py       # nested explain concern
│   └── test_integration/
│       ├── test_algorithm_coverage.py      # declared algorithm train trials
│       └── test_ppo_trainer_ray.py         # real-Ray trainer boundary
├── test_settings/test_unit/              # settings/configuration models
│   ├── test_heterogeneous_agents.py
│   └── test_scenarios.py
├── test_world_providers/                 # flat: source adapters and provider cache
│   ├── test_aerialgym_provider.py
│   └── test_source_cache.py
└── test_worlds/                          # world compilation, residency, route feasibility
    ├── test_unit/
    │   ├── test_compiler.py
    │   └── test_residency.py
    └── test_integration/
        ├── test_obstacle_waypoint_preflight.py  # feasibility boundary
        └── test_seeded_gate_catalog.py          # cross-concern world scenario
```

| Concern root | Behavior and boundaries to keep together | Existing shape or representative evidence |
| --- | --- | --- |
| `test_cli/` | Command parsing, dispatch, user-facing validation, output, and actual CLI invocation. | Six modules; [dispatch](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_cli/test_unit/test_cli.py), [Tune validation](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_cli/test_unit/test_tune_validation.py), [real CLI commands](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_cli/test_integration/test_cli_commands.py). |
| `test_environments/` | Environment lifecycle, actions, tasks, shape/reward behavior, observation and export boundaries; native environment integration. | 32 modules, local integration `conftest.py`; [actions](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_environments/test_unit/test_action_spaces.py), [shape collision](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_environments/test_unit/test_shape_collision.py), [native voxel environment](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_environments/test_integration/test_voxel_env_core.py). |
| `test_experiments/` | Run configuration and preflight, orchestration, resume/stages, evaluation recipes, outputs, trajectories, Tune runner integration, and native extension execution during a run. | 36 modules, local unit fixtures and helpers; [runner/resume](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_experiments/test_unit/test_experiment_runner_resume_repeat.py), [trajectory storage](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_experiments/test_unit/test_trajectory_storage.py), [native extensions](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_experiments/test_integration/test_native_extensions.py). |
| `test_garden/` | Model-garden augmentation, dataset configuration, dataset and store behavior. | Four unit modules; [augmentation](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_garden/test_unit/test_garden_augment.py), [dataset](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_garden/test_unit/test_garden_dataset.py), [store](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_garden/test_unit/test_garden_store.py). |
| `test_heuristic/` | Heuristic factory and voxel strategy behavior. | Flat, two modules: [factory](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_heuristic/test_factory.py), [voxel strategies](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_heuristic/test_voxel_strategies.py). |
| `test_imitation/` | Demonstration cache/providers, collection, preflight, YAML configuration, pretraining, and imitation model behavior. | Flat, nine modules; [cache](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_imitation/test_cache.py), [generation providers](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_imitation/test_generation_providers.py), [preflight](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_imitation/test_imitation_preflight.py). |
| `test_rllib/` | Algorithm adapters, RLlib model/config surfaces, trainer/evaluation/curriculum/reporting, Tune scheduler/resources, explain integration, and real algorithm training where explicitly tested. | 41 modules; [DQN runtime](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_dqn_runtime.py), [explain scorer](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_explain/test_policy_scorer.py), [algorithm coverage](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_algorithm_coverage.py). Registration-only tests must not be described as trainability proof. |
| `test_settings/` | Settings parsing, heterogeneous/scenario/evaluation configuration, and package configuration. | Five unit modules; [field declarations](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_settings/test_unit/test_configuration_field_declarations.py), [heterogeneous agents](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_settings/test_unit/test_heterogeneous_agents.py), [scenarios](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_settings/test_unit/test_scenarios.py). |
| `test_world_providers/` | Provider-specific acquisition, cache and shared-service behavior, optional provider extras. | Flat, seven modules; [AerialGym](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_world_providers/test_aerialgym_provider.py), [source cache](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_world_providers/test_source_cache.py), [optional CaveDrone extra](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_world_providers/test_cavedrone_install_extra.py). |
| `test_worlds/` | World artifacts, candidates, compilation, extents, manifests, overviews, residency, obstacles, waypoint feasibility, and seeded gate catalog scenarios. | Ten modules; [compiler](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_worlds/test_unit/test_compiler.py), [obstacle waypoint preflight](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_worlds/test_integration/test_obstacle_waypoint_preflight.py), [seeded gate catalog](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_worlds/test_integration/test_seeded_gate_catalog.py). |

Some boundaries remain ambiguous in the current layout. For example, [`tests/test_experiments/test_unit/test_experiment_cli.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_experiments/test_unit/test_experiment_cli.py) is under the run owner rather than `test_cli/`; the RLlib-root [Tune continuation](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_tune_runner_continuation.py), [miscellaneous](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_tune_runner_misc.py), and [resource](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_tune_runner_resources.py) modules test production `experiments/tune_runner.py`; and environment export tests can overlap provider acquisition. Treat these as review prompts, **not automatic relocation instructions**. Decide from the principal assertion: CLI contract versus run orchestration, RLlib adapter versus Tune process orchestration, environment serialization versus provider retrieval. Keep related assertions in one owning module and cross-link a second boundary test only when it proves a genuinely different contract.

## Rust concern map

The native core keeps many focused `#[cfg(test)]` modules beside production code under [`theseo_anysearch/core/src/`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/core/src). Keep local invariants beside their owning module: replay/viewer and camera/render; bridge and Python-exposed conversions; environment/action/reward/scenario; world ingest/residency; geometry/predicates; and verification. Larger sibling test files such as `multi_heterogeneous_tests.rs`, `single/tests.rs`, and `regional_tests.rs` are existing patterns for a module with a substantial focused test body, not a reason to aggregate unrelated tests.

The native **existing target tree** has a different shape: most unit tests are
inline in the owning `.rs` module, not in a parallel `tests/unit/` tree. The
shown module paths and three `core/tests` targets exist at the pinned revision;
other inline test-bearing modules are omitted. `#[cfg(test)]` is confirmed in
the representative inline files below and in `extension_sdk/src/lib.rs`.

```text
theseo_anysearch/
├── core/
│   ├── src/                                  # native unit tests live with owners
│   │   ├── bin/voxel_replay.rs                # replay binary behavior; inline tests
│   │   ├── camera.rs                          # camera logic; inline tests
│   │   ├── replay/storage.rs                  # replay storage; inline tests
│   │   ├── bridge/python/environments/voxel/environment.rs  # PyO3-facing env; inline tests
│   │   ├── voxel/actions/pipeline.rs          # action pipeline; inline tests
│   │   ├── voxel/predicates/native.rs          # native predicate; inline tests
│   │   ├── voxel/world/ingest/voxelize.rs      # ingest logic; inline tests
│   │   ├── voxel/world/disk_backed.rs          # world residency; inline tests
│   │   ├── voxel/environment/multi_heterogeneous_tests.rs  # focused sibling tests
│   │   ├── voxel/environment/single/tests.rs  # focused submodule tests
│   │   ├── voxel/world/regional_tests.rs       # focused sibling tests
│   │   └── verification/tests.rs               # backend parity/fault checks
│   └── tests/                                # black-box crate/boundary targets
│       ├── ingest_to_world.rs                 # ingest -> world
│       ├── ingest_to_env.rs                   # ingest -> environment
│       └── scenario_v2_extension.rs          # compiled extension scenario
└── extension_sdk/src/lib.rs                  # separate crate; embedded SDK tests
```

Use [`core/tests/`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/core/tests) for black-box crate boundaries: `ingest_to_world.rs`, `ingest_to_env.rs`, and `scenario_v2_extension.rs` currently exercise that tier. The [extension SDK](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/extension_sdk) has its own crate-local tests. A benchmark smoke test may guard that a path executes but does not prove throughput, latency, or performance regression limits; those claims need separately designed measurement.

## Review and migration

For each new test, the review should be able to answer: **which behavior owns it; why this tier; which dependencies are real versus doubled; which CI or local selection runs it; and what a skip would leave unverified?** Prefer a nearby addition over a new test bucket. If a test is misplaced, move it in a focused change while preserving its marks, fixtures, node selection used by CI, and assertion coverage. Do not reorganize all existing tests solely to conform to this proposed map. Changes to test placement rules should update this guide and the relevant language-specific testing page together.
