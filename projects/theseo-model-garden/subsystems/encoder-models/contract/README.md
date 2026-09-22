---
title: Encoder-model contract
status: draft
kind: subsystem-contract
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [../README.md]
---

# Encoder-model contract

This page defines the observable construction and tensor behavior of Model Garden
encoders. It describes the implementation at Theseo Anysearch revision
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`; it does not promote experimental model
quality into a runtime guarantee.

## Construction guarantees

- `build_encoder()` accepts only `voxel_box_3dcnn`, `voxel_box_2dcnn`, and
  `voxel_triplanar_2dcnn`; any other value raises `ValueError`.
- `build_model()` selects `VoxelAE`, `VoxelVAE`, or `VoxelMVMEncoder` from the
  top-level approach. The effective side length is `2 * max(radius) + 1`, using
  `encoder.box_radii` when present and otherwise `encoder.box_radius`.
- `architecture: custom` requires `custom_encoder`; omission raises `ValueError`.
  When present, the imported object is returned as the complete model before the
  approach-specific assembly path is entered.
- Configuration models reject unknown keys through Pydantic `extra="forbid"`.

## Built-in tensor contracts

- `VoxelEncoder3D` accepts `(B,N,N,N)` by inserting a channel dimension, or an
  already channelized 5-D tensor, and returns `(B, latent_dim)`.
- `VoxelEncoder2D` interprets a 4-D voxel tensor as `(B,x,y,z)`, permutes it to
  `(B,z,x,y)`, and returns `(B, latent_dim)`. Its first convolution is constructed
  for the configured side length, so the input depth must match that length.
- `VoxelEncoderTriplanar` takes the three center planes from a 4-D voxel tensor,
  stacks them as channels, and returns `(B, latent_dim)`.
- Built-in encoders end in adaptive average pooling and a linear projection. This
  yields a fixed latent width, but does not make every architecture compatible with
  arbitrary input side lengths.

## Pretraining-model behavior

- `VoxelAE.forward()` returns `(reconstruction, latent)`. Reconstruction targets
  differ by architecture: the full volume for 3D, three center planes for
  tri-planar, and the permuted full volume for depth-as-channel 2D.
- `VoxelVAE.forward()` returns `(reconstruction, mu, log_var)` and samples through
  reparameterization. Its loss is binary cross entropy plus beta-weighted KL loss.
- `VoxelMVMEncoder` randomly masks `int(N^3 * mask_ratio)` cells, predicts all cell
  values with a transformer decoder, and computes binary cross entropy only at the
  masked positions.
- VAE and MVM stochastic behavior depends on PyTorch random state; the modules do not
  establish or preserve a seed themselves.

## Encoder extraction

`extract_encoder()` returns `.encoder` when present, then `._base_enc` for the VAE,
and otherwise returns the supplied module unchanged. A VAE extraction therefore
produces the base encoder whose output width is twice the configured latent width;
consumers must not assume the extracted VAE module emits a sampled latent vector.

## Rejection and failure behavior

Architecture incompatibilities, invalid tensor ranks, channel mismatches, invalid
decoder dimensions, and incompatible custom outputs are allowed to fail through
PyTorch or Python exceptions. The factory performs no forward-pass conformance probe.
Model quality, checkpoint compatibility, device placement, and checkpoint identity
are validated by other subsystems or remain caller responsibilities.

## Unsupported or unresolved cases

- The historical monolithic design says custom encoders are automatically wrapped by
  an AE or MVM decoder. Current code returns the custom instance directly; automatic
  wrapping is unsupported.
- No stable protocol type formally represents an encoder interface.
- Multi-radius compatibility is architecture-dependent and is not validated during
  construction.
