---
title: Ray trials and process boundaries
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray trials and process boundaries

Source baseline: [`theseo-anysearch` fd94554c](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected 2026-09-28. Tests at this revision were read, not run; source wiring is not proof of remote portability.

The module-level Tune trainable is designed to cross Ray's cloudpickle boundary. It reconstructs configuration and paths, materializes the Python extension and native binary in the trial process before creating a trainer, then stops its algorithm on normal exception unwinding. A locally importable extension is therefore not evidence that a remote trial can load it. See [`tune_runner.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L286-L593).

The trainable applies `with_resources` to the base function **before** `with_parameters`; a source comment reports that reversing this order silently drops the placement group in the Ray version used there. Trials also set `reuse_actors=False` to avoid stale bundle references. These are implementation choices, not live placement evidence. See [resource setup](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1335-L1400) and [trial setup](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1483-L1507).

On Windows, Tune patches Ray's internal `_atomic_save` to normalize mixed separators and report `MAX_PATH` errors. This private-API patch is upgrade-sensitive. See [`tune_runner.py`](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L601-L665).

Real-Ray [Tune integration tests](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_tune_runner_ray.py) are declared but were not run for this page. Verify remote extension loading, cancellation cleanup, and trial isolation before claiming portability. Process ownership is in [runtime lifecycle](runtime-lifecycle.md); requested bundles are in [resources and placement](resources-and-placement.md).
