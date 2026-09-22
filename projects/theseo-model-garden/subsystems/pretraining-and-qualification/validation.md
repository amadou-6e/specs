---
title: Pretraining and qualification validation
status: draft
kind: subsystem-validation
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [README.md, contract/README.md]
---

# Pretraining and qualification validation

This record maps live guarantees to checks present in the inspected repository and
separates those checks from historical experiment evidence. No test command was run
during this documentation pass; entries below describe tests present at commit
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`.

## Implemented checks

| Guarantee or boundary | Check | What it proves |
|---|---|---|
| Training defaults and strict config keys | `tests/test_garden/test_unit/test_garden_data_config.py::TestGardenTrainingConfig` and `TestGardenConfig` | Defaults parse, accepted literals are bounded, and extra top-level fields fail. |
| Tune defaults | `tests/test_garden/test_unit/test_garden_data_config.py::TestGardenTuneConfig` | Default sample count, concurrency, grace period, and empty search space. |
| Supported YAML forms | `tests/test_garden/test_unit/test_garden_data_config.py::TestLoadGardenConfig` | Inline, wrapped, and external-data configurations validate. |
| Final artifact set | `tests/test_garden/test_unit/test_garden_store.py::TestGardenStoreSave` | Save produces states, metadata, history, tags, and returned path. |
| Registry resolution | `tests/test_garden/test_unit/test_garden_store.py::TestGardenStoreResolveRef` | Saved names and tags resolve and missing references fail. |

These tests validate configuration and persistence edges, not training or Tune itself.

## Historical experiment evidence

- [Perception encoder R0](../../experiments/perception-encoder-r0/README.md) preserves
  a registered protocol and bounded result; it is not a regression suite.
- [Compact encoder campaign](../../experiments/compact-encoder-campaign/README.md)
  preserves engineering, collision-readout, optimization, and qualification evidence.
- [Local geometry encoder](../../experiments/local-geometry-encoder/README.md) and
  [continuation/context](../../experiments/encoder-continuation-and-context/README.md)
  preserve later investigations without creating a universal runtime status.

## Missing coverage

- no test directly exercises `trainer.train`, early stopping, callback ordering,
  resume, best-weight restoration, multi-radius batches, or scheduler state;
- no tests directly exercise Tune parsing, resource allocation, ASHA reporting,
  winner selection, or save-best retraining;
- no deterministic reproduction check exists because training and loader seeds are
  not part of the interface;
- no test proves saved metadata can reconstruct a training run;
- no implemented check converts frozen-probe evidence into a registry qualification
  decision; and
- no CI evidence was inspected during this documentation pass.

The reliable automated claim is therefore limited to the named configuration and
registry-artifact behaviors. Training correctness and qualification remain only
partially verified.
