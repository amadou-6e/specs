---
title: Encoder-model design
status: draft
kind: subsystem-design
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [../contract/README.md]
---

# Encoder-model design

This page explains how configuration, encoder architecture, training objective, and
encoder extraction compose to realize the encoder-model contract.

## Component flow

```text
GardenConfig
  -> build_model()
      -> custom class instance, or
      -> built-in encoder + AE/VAE/MVM training-only decoder
  -> trainer optimizes full model
  -> extract_encoder()
  -> model registry serializes encoder state
```

`GardenConfig` is the validated selection boundary. `build_model()` derives one
construction side length from the configured radii, then either crosses the trusted
custom-import boundary or assembles a built-in model. Training owns optimization;
the registry owns persistence. This subsystem holds no global mutable state and does
not cache model instances.

## Architecture trade-offs

- The 3D encoder preserves volumetric convolution but has the highest spatial compute.
- The depth-as-channel 2D encoder processes the full volume with cheaper 2D kernels,
  while binding its first convolution to a specific depth.
- The tri-planar encoder is smaller and interpretable but observes only three center
  planes and can omit off-plane geometry.
- Adaptive pooling yields a fixed output width and reduces parameter dependence on
  spatial dimensions, but also removes explicit output-position structure.
- AE and VAE decoders provide reconstruction objectives and are discarded for later
  encoder use. MVM uses a transformer decoder over all voxel positions, making its
  decoder cost scale with volume.

## State and failure boundaries

Module parameters and BatchNorm state live in ordinary PyTorch modules. Random VAE
sampling and MVM masking use ambient PyTorch RNG state. Device selection is performed
by callers. Configuration parsing prevents unknown names, while shape compatibility
and most numeric validity remain deferred to construction or forward execution.

The dynamic custom class boundary is trusted executable code. Artifact serialization,
checkpoint metadata, compatibility checks, and qualification status are outside this
subsystem and must not be inferred from successful construction.
