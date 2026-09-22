---
title: Pretraining and qualification design
status: draft
kind: subsystem-design
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [../README.md, python.md]
---

# Pretraining and qualification design

This design explains how CLI orchestration, the Torch training loop, Ray Tune, and the
registry boundary realize the current subsystem contract.

## Direct-training flow

```text
config reference
  -> validated GardenConfig
  -> collect observations per requested radius
  -> build train/validation datasets
  -> build encoder model
  -> train and record epoch losses
  -> GardenStore.save(model, encoder, metadata, loss curve)
```

The CLI owns orchestration and progress reporting. The trainer owns optimization and
early stopping but knows nothing about registry naming or qualification. Dataset and
model factories are injected as built objects, which keeps the loop reusable but
leaves orchestration responsible for compatible shapes and objectives.

## Tune flow

Ray Tune flattens sampled values into dotted configuration keys. Each worker rebuilds
the configuration, collects data through the collection layer, builds a fresh model,
and reports per-epoch loss. ASHA and Ray select the minimum-loss trial. Optional
publication starts a separate fresh training run from the winning configuration.

This avoids depending on transient Ray checkpoints for publication, but publication
is consequently a reproduction attempt rather than promotion of the measured winner.
No seed or equivalence gate links the two.

## State and persistence boundaries

- Optimizer, scheduler, patience counter, and in-memory weights belong to one process.
  The optional resume checkpoint omits scheduler and patience state.
- Ray owns trial state and scheduling under the Tune output directory.
- `GardenStore` owns final artifact files and registry entries. It does not assign
  qualification status.
- Experiment folders own frozen protocols, evidence, and conclusions. The trainer
  does not interpret them.

## Trust and failure boundaries

Garden YAML is structurally validated with Pydantic, then custom encoder imports,
filesystem sources, Torch execution, and Ray execution cross into less constrained
boundaries. Custom model code is trusted Python code. Dataset caches and checkpoints
are local artifacts rather than cryptographically verified inputs.

The most consequential design debt is the missing handoff between experimental
qualification and registry metadata. Another is the divergence between best observed
loss and final saved weights. Both are contract gaps, not merely documentation gaps.

## Trade-offs

- Validation-loss early stopping is cheap and objective-aligned, but cannot establish
  representation usefulness for routing.
- Zero-worker loading avoids multiprocessing complexity and platform variance, but
  can constrain throughput.
- Equal fractional GPU allocation enables parallel Tune trials, but assumes trials
  fit that fraction and ignores model-dependent memory.
- Self-contained Tune workers simplify scheduling; content-addressed caching is needed
  to prevent duplicated collection cost.
