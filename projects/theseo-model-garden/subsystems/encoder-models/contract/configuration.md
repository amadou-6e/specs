---
title: Encoder-model configuration
status: draft
kind: subsystem-configuration
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [README.md]
---

# Encoder-model configuration

This page describes the model-building fields validated in
`theseo_anysearch/garden/data_config.py`. Dataset, augmentation, optimizer, and Tune
settings are owned by their respective subsystems even though they share
`GardenConfig`.

## Architecture selection

| Field | Default | Effect |
|---|---:|---|
| `architecture` | `voxel_box_3dcnn` | Selects 3D, depth-as-channel 2D, tri-planar 2D, or `custom`. |
| `approach` | `autoencoder` | Selects AE, VAE, or masked-voxel full-model assembly. |
| `encoder.box_radius` | `2` | Supplies the side length when `box_radii` is absent. |
| `encoder.box_radii` | `null` | When set, its maximum determines construction side length. |
| `encoder.conv_channels` | `[32, 64, 64]` | Sets built-in convolution widths. |
| `encoder.latent_dim` | `128` | Sets built-in projected latent width. |

The schema accepts approaches `autoencoder`, `vae`, and `mvmencoder`. The separate
`autoencoder.variant` field defaults to `ae`, but the factory selects VAE behavior
from top-level `approach`; changing `variant` alone does not select a VAE.

## Objective-specific settings

- `autoencoder.beta` defaults to `1.0` and weights VAE KL loss.
- `mvmencoder.mask_ratio` defaults to `0.75`.
- `mvmencoder.decoder_layers`, `decoder_dim`, and `decoder_heads` default to `2`,
  `64`, and `4` respectively.

Pydantic validates literal choices and rejects extra keys, but the shown numeric and
list fields do not declare positivity or cross-field constraints. Invalid channel
lists, radii, head divisibility, or mask ratios may therefore fail only during model
construction or execution.

## Identity effects

Architecture, approach, radii, channel widths, latent width, objective-specific
settings, and custom class/kwargs can change module structure or behavior and must be
part of any artifact identity that promises checkpoint compatibility. Identity and
metadata persistence are owned by the model-registry subsystem.
