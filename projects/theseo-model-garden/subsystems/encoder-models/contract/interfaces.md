---
title: Encoder-model interfaces
status: draft
kind: subsystem-interface
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [README.md]
---

# Encoder-model interfaces

This page lists the Python call surfaces through which trainers, stores, and custom
extensions construct or separate encoder models.

## Factory functions

In `theseo_anysearch/garden/models/ae.py`:

- `build_encoder(architecture, n, channels, latent_dim) -> nn.Module` constructs one
  built-in encoder and rejects unknown architecture names.

In `theseo_anysearch/garden/encoder.py`:

- `build_model(cfg: GardenConfig) -> nn.Module` constructs the full trainable model;
- `extract_encoder(model: nn.Module) -> nn.Module` selects the stored encoder portion;
  and
- `load_encoder_from_store(garden_dir, name, device="cpu")` reads `encoder.pt` with
  `weights_only=True`, despite its annotated `nn.Module` return type actually being a
  state dictionary. New callers should use the model-registry loading path rather
  than rely on that inaccurate annotation.

## Built-in modules

`theseo_anysearch/garden/models/ae.py` exposes `VoxelEncoder3D`, `VoxelEncoder2D`,
`VoxelEncoderTriplanar`, `VoxelAE`, and `VoxelVAE`. The masked-voxel full model is
`VoxelMVMEncoder` in `theseo_anysearch/garden/models/mvm.py`.

These are Python implementation surfaces, not a separately versioned public package
API. Serialized checkpoints depend on the selected class and constructor dimensions.
