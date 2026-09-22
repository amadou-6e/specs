---
title: Encoder-model Python responsibilities
status: draft
kind: subsystem-language-design
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [README.md]
---

# Encoder-model Python responsibilities

This page maps the encoder-model lifecycle to unambiguous Python source paths in the
Theseo Anysearch implementation.

## Configuration and construction

- `theseo_anysearch/garden/data_config.py` declares `EncoderConfig`,
  `AutoencoderConfig`, `MVMConfig`, `CustomEncoderConfig`, and the relevant fields of
  `GardenConfig`. It owns schema validation and dynamic custom-class instantiation.
- `theseo_anysearch/garden/encoder.py` selects the complete pretraining model and
  separates encoder parameters after training.

## Built-in architecture implementations

- `theseo_anysearch/garden/models/ae.py` implements the three built-in encoders,
  matching decoders, AE/VAE forward paths, and reconstruction losses.
- `theseo_anysearch/garden/models/mvm.py` implements random voxel masking, the shared
  built-in encoder, positional queries, transformer decoding, and masked-cell loss.

## Consumers outside the subsystem

- `theseo_anysearch/garden/trainer.py` owns optimization, scheduling, early stopping,
  and validation loss.
- `theseo_anysearch/garden/store.py` owns saved model layout, metadata, and state-dict
  persistence.
- `theseo_anysearch/cli/commands/garden.py` owns CLI selection and orchestration.
- `theseo_anysearch/rllib/models/cnn.py` reconstructs and consumes compatible garden
  encoders for policy training; that policy integration is not part of this contract.

There is no Rust component for encoder execution. Rust utilities may collect or show
data, but PyTorch owns model construction and inference.
