---
title: Encoder models
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../architecture/model-garden-monolith.md
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/local-geometry-encoder/README.md
---

# Encoder models

This subsystem owns construction and tensor behavior for the voxel encoders and
pretraining model families shipped by the Model Garden. It turns a validated model
configuration into a PyTorch module and defines how an encoder is separated from its
training-only decoder. Dataset production, optimization, qualification, artifact
storage, and RL policy integration belong to neighboring subsystems.

## Problem and ownership

The Model Garden needs a stable boundary between local voxel observations and latent
vectors that can later be consumed by policies or diagnostic readouts. This subsystem
owns the built-in 3D, depth-as-channel 2D, and tri-planar architectures; AE, VAE, and
masked-voxel pretraining model assembly; and dynamic construction of custom modules.

It does not claim that an architecture is useful for navigation. Experimental results
and qualification gates remain evidence owned by the experiment and qualification
records, not runtime guarantees of this subsystem.

## Consumers

- the garden trainer and Tune trainable construct full pretraining models;
- the garden store extracts encoder parameters from trained models;
- CLI training and tuning commands select architectures through `GardenConfig`;
- Anysearch policy models reconstruct compatible encoder modules before loading
  garden checkpoints; and
- encoder experiments use these implementations as experimental treatments.

## Supported scope

The current implementation provides three built-in encoder architectures and three
pretraining approaches. A custom architecture may be imported from a Python class
path, but the factory returns that module as the complete model; automatic decoder
wrapping for custom encoders is not implemented. The subsystem is Python/PyTorch
only and exposes no Rust implementation.

## Maturity and limitations

The implementation is live, but this specification remains `draft` because direct
unit coverage of the encoder tensor contracts and several configuration combinations
is absent. Historical documents describe stronger custom-encoder wrapping behavior
than the current factory implements; the current behavior is authoritative and the
conflict is recorded in the contract.

## Reading map

- [Contract, behavior, and guarantees](contract/README.md)
- [Python interfaces](contract/interfaces.md)
- [Configuration](contract/configuration.md)
- [Custom encoder extension point](contract/extensions.md)
- [Internal design](design/README.md)
- [Python responsibility map](design/python.md)
- [Validation evidence and gaps](validation.md)
