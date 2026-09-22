---
title: Pretraining and qualification
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related:
  - ../encoder-models/README.md
  - ../model-registry/README.md
  - ../../experiments/README.md
---

# Pretraining and qualification

This subsystem turns collected voxel observations into trained encoder artifacts and
decides what evidence, if any, those artifacts support. It owns the training loop,
hyperparameter-search orchestration, training-result record, and the boundary between
ordinary validation-loss selection and research qualification. Dataset construction is
owned elsewhere; encoder architecture construction belongs to
[encoder models](../encoder-models/README.md), and artifact persistence and discovery
belong to the [model registry](../model-registry/README.md).

The implementation inspected here is Theseo AnySearch commit
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`. At that revision, training and Tune are
live, while the broader frozen-probe certification program exists only as historical
protocol and experiment evidence. Saving a checkpoint does not qualify it for a
navigation claim.

## Consumers

- `anysearch garden train` consumes a garden configuration, collected observations,
  and an encoder model, then writes the resulting artifact through `GardenStore`.
- `anysearch garden tune` runs Ray Tune trials and can retrain and save the
  validation-loss winner.
- experiment authors consume training histories and checkpoints when conducting
  explicit probe or robustness studies under [experiment protocols](../../experiments/README.md).
- downstream RL models consume published encoder weights, but qualification claims
  must come from recorded experiment evidence rather than checkpoint presence.

## Supported scope

The live path supports AE, VAE, and masked-voxel model losses, single- and
multi-radius batches, Adam optimization, constant or cosine learning rates,
validation-loss early stopping, checkpoint resume for direct training, and ASHA-based
Tune search. Exact behavior and limitations are in the [contract](contract/README.md).

The subsystem is `draft` because no implemented certification command maps a trained
checkpoint to the historical probe gates or emits a machine-readable qualification
decision. The historical program remains valuable evidence, but is not a live product
contract.

## Reading map

- [Contract and guarantees](contract/README.md)
- [Public interfaces](contract/interfaces.md)
- [Configuration](contract/configuration.md)
- [Internal design](design/README.md)
- [Python responsibility map](design/python.md)
- [Validation evidence and gaps](validation.md)
- [Training and tuning guide](guides/README.md)
