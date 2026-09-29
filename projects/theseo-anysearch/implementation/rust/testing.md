---
title: Rust testing investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Rust testing

This page owns native test placement by production concern, commands,
prerequisites, and evidence limits. [Python testing](../python/testing.md)
owns the Python-facing boundary tests.

This page inventories native verification and its current limits. It is a draft
source-and-test audit, not a claim that the commands below were run or that every
test passes. The inspected product baseline is
[`theseo-anysearch` `fd94554c9620096f94aaed95ffda6a1bbd4711ec`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec),
read on 2026-09-28. Refresh the inventory against a new pinned revision before
using it as a release gate.

## Test boundaries

### Placement rules and annotated target tree

Keep local invariants in `#[cfg(test)]` beside their owning Rust module. A
larger focused body may live in a sibling `tests.rs` or `*_tests.rs` module;
do not accumulate unrelated behavior there. Put black-box crate and extension
boundaries under `core/tests/`. The SDK is a separate crate with its own tests.

This is the existing target at the pinned revision; displayed paths exist and
omitted inline test-bearing modules stay in place:

```text
theseo_anysearch/
├── core/
│   ├── src/                                  # native unit tests beside owners
│   │   ├── bin/voxel_replay.rs                # replay binary
│   │   ├── camera.rs                          # camera logic
│   │   ├── replay/storage.rs                  # replay storage
│   │   ├── bridge/python/environments/voxel/environment.rs  # PyO3 boundary
│   │   ├── voxel/actions/pipeline.rs          # action pipeline
│   │   ├── voxel/predicates/native.rs          # native predicates
│   │   ├── voxel/world/ingest/voxelize.rs      # world ingest
│   │   ├── voxel/world/disk_backed.rs          # world residency
│   │   ├── voxel/environment/multi_heterogeneous_tests.rs  # focused sibling tests
│   │   ├── voxel/environment/single/tests.rs  # focused submodule tests
│   │   ├── voxel/world/regional_tests.rs       # focused sibling tests
│   │   └── verification/tests.rs               # backend parity/fault checks
│   └── tests/                                # black-box crate boundaries
│       ├── ingest_to_world.rs                 # ingest -> world
│       ├── ingest_to_env.rs                   # ingest -> environment
│       └── scenario_v2_extension.rs          # compiled extension scenario
└── extension_sdk/src/lib.rs                  # separate crate; embedded SDK tests
```

For Python/native behavior, test the native invariant here and the exposed
binding or workflow from [Python integration](../python/testing.md); link the
pair in the change review instead of duplicating every assertion. Benchmarks
are separate measurements, not correctness tests. The tree records placement,
not passing results.

| Boundary | Current evidence at the pinned revision | What it does not establish |
| --- | --- | --- |
| Native unit tests | `#[cfg(test)]` tests are embedded throughout [`theseo_anysearch/core/src/`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/core/src), including verification, replay, and bridge modules. | Their presence alone does not prove that all native behavior or the Python boundary is covered. |
| Native integration tests | [`theseo_anysearch/core/tests/`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/core/tests) contains `ingest_to_world.rs`, `ingest_to_env.rs`, and `scenario_v2_extension.rs`. The extension scenario builds a release extension in a temporary location, so it has additional build cost. | They do not exercise every Python wrapper or a packaged wheel. |
| Backend comparison | [`theseo_anysearch/core/src/verification/tests.rs`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/core/src/verification/tests.rs) contains world-backend parity, fault, and residency checks, as well as a benchmark smoke test. | The benchmark smoke test is not a complete performance characterization or a subsystem acceptance result. |
| Python/native boundary | [`tests/test_environments/test_integration/test_voxel_env_core.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_environments/test_integration/test_voxel_env_core.py) imports `PyVoxelEnv` with `importorskip`; [`tests/test_experiments/test_integration/test_native_extensions.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_experiments/test_integration/test_native_extensions.py) compiles, loads, and executes a native extension. [`tests/conftest.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/conftest.py) attempts a `maturin develop` when the wheel is not current and warns if it fails. | An `importorskip` or build warning can leave a boundary unverified; collection without a skip audit is not proof. These integration tests are excluded from the default local CI selection. |

The native core has its own [`theseo_anysearch/core/Cargo.toml`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/core/Cargo.toml) (`cdylib` and `rlib`), and the extension SDK has a separate [`theseo_anysearch/extension_sdk/Cargo.toml`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/extension_sdk/Cargo.toml); neither should be assumed to be covered by a root Cargo workspace command. The wheel build uses [`theseo_anysearch/core/pyproject.toml`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/core/pyproject.toml) and maturin/PyO3.

## Reproducible checks to run

From the product repository root, with a stable Rust toolchain and the Python
environment required by the relevant Python tests:

```powershell
cargo check --manifest-path theseo_anysearch/core/Cargo.toml --all-targets
cargo test --manifest-path theseo_anysearch/core/Cargo.toml --lib
cargo test --manifest-path theseo_anysearch/core/Cargo.toml --test ingest_to_world
cargo test --manifest-path theseo_anysearch/core/Cargo.toml --test ingest_to_env
cargo test --manifest-path theseo_anysearch/core/Cargo.toml --test scenario_v2_extension
cargo test --manifest-path theseo_anysearch/extension_sdk/Cargo.toml
```

These are proposed full-scope checks inferred from the manifests and test targets,
**not execution evidence** for this audit. The extension scenario may compile a
release artifact and take substantially longer than a unit test. To verify the
installed Python/native boundary, follow the [native build workflow](native-workflow.md)
and run the relevant Python integration tests with an explicit report of passes,
failures, and skips. A wheel build alone proves packaging succeeds, not that the
wrapper's behavior is correct.

## What CI presently requires

At the pinned revision, [local-tests.yml](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/.github/workflows/local-tests.yml)
configures Windows, Python 3.12, and stable Rust. Its native portion runs
`cargo check --all-targets` for `core`, one named verification benchmark-smoke
test (`verification::tests::benchmark_smoke_matrix_is_ci_safe_and_separates_future_memory_metrics`),
and a release maturin wheel build. The Python job excludes Ray and integration
tests. No full `cargo test`, `cargo clippy`, or `cargo fmt --check` gate was found
in that workflow. Other workflows were not established by this audit; absence
from this workflow is not a global absence claim.

The [archived Rust testing plan](../../legacy/rust-testing.md) describes old
`rust/tests/` paths and a full test/clippy/fmt CI gate. Those claims are
historical, not a current CI guarantee. When changing native behavior, record
which test tier actually ran, the target and toolchain, and any skipped Python
boundary tests; do not translate a passing smoke check into full coverage.

Subsystem-specific behavioral acceptance belongs in each owning subsystem's
validation specification. Build commands, diagnostic procedure, release artifacts,
and performance methodology belong in [native-workflow.md](native-workflow.md),
not this test inventory.
