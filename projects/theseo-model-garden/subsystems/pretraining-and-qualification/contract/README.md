---
title: Pretraining and qualification contract
status: draft
kind: subsystem-contract
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [../README.md, interfaces.md, configuration.md]
---

# Pretraining and qualification contract

This contract describes observable training, selection, and qualification behavior.
It deliberately separates guarantees implemented by the current trainer from claims
proposed or evaluated in historical perception-encoder campaigns.

## Training lifecycle

Given a constructed model, train dataset, validation dataset, and validated training
configuration, the trainer creates loaders, optimizes with Adam, optionally advances a
cosine scheduler once per epoch, computes mean training and validation losses, and
records both values in epoch order. A strictly lower validation loss counts as an
improvement. Training stops after the configured number of consecutive non-improving
epochs or after the configured maximum epoch.

For AE-style objectives, occupied-voxel class weighting is fixed by configuration or
estimated from at most the first 512 training samples. VAE and masked-voxel objectives
delegate loss computation to the model without that weighting. These branches are
implemented in
[`trainer.py`](../../../../../../theseo_anysearch/garden/trainer.py). The trainer does
not seed PyTorch or loader shuffling, so identical configuration does not guarantee
identical weights.

## Result and checkpoint semantics

`TrainResult.final_val_loss` is the best validation loss observed, not necessarily the
loss from the final in-memory model state. When checkpointing is enabled, each new best
epoch overwrites `_checkpoint.pt` with model state, optimizer state, epoch, best loss,
and loss history. Resume restores those fields and continues at the following epoch.

The direct CLI does **not** reload the best checkpoint before publishing. It saves the
model object as it exists when training stops. Therefore `final_val_loss` can describe
an earlier epoch than the weights written to `model.pt` and `encoder.pt`. Consumers
must not infer that published weights are the best-validation weights until this gap is
resolved. Scheduler and patience state are also not restored on resume.

If resume is disabled, no intermediate training checkpoint is written. If enabled,
the checkpoint path is scoped to the model family and not the tag, so tagged runs of
the same family can share a checkpoint unintentionally.

## Tune selection

Tune accepts a validated garden configuration containing a `tune` block. Search-space
entries are flattened as `<section>.<field>`, converted to supported Ray Tune sampler
functions, and applied to a copy of the base configuration. Trials report epoch,
training loss, and validation loss. ASHA prunes against validation loss, and the final
winner is the result with minimum reported validation loss.

When `--save-best` is enabled, the winner's sampled configuration is retrained from
scratch and that new run is saved. The saved weights are not the winning trial's
weights, and the retraining outcome is not required to reproduce the winning metric.
Multi-radius dataset construction is supported by direct training, but the current
Tune trial and retraining paths collect only `encoder.box_radius`; configurations that
depend on `encoder.box_radii` are not equivalent across the two commands.

## Qualification boundary

The live subsystem has no certification or qualification evaluator. Reconstruction
validation loss, Tune rank, successful serialization, or registry presence are not
evidence that an encoder improves navigation, preserves topology, resists corruption,
or passes frozen probes.

Historical documents define proposed gates and record bounded outcomes, including the
[compact encoder campaign](../../../experiments/compact-encoder-campaign/README.md)
and [R0 experiment](../../../experiments/perception-encoder-r0/README.md). Those
records remain evidence under their frozen protocols; they do not create a general
runtime status field or automated promotion rule.

## Resource and failure behavior

- Training uses data-loader workers `0`; memory limits depend on the dataset, radius,
  batch size, model, and device rather than an enforced budget.
- Device `auto` chooses CUDA when available. Tune divides one GPU equally among
  `max_concurrent` trials and otherwise requests no GPU.
- Configuration parsing forbids unknown fields, but most numeric ranges and
  cross-field constraints are not validated before execution.
- Data, model, device, Ray, and persistence errors propagate as command failures; the
  trainer does not convert them into qualification results.
