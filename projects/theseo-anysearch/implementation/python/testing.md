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

Status: source-pinned contributor guide, not a claim that every test passes. Inspected against AnySearch revision [`fd94554c`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec) on 2026-09-28. Tests were read, **not run** at that revision.

## Layout and selection

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
