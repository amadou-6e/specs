---
title: Model registry
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related:
  - ../../architecture/README.md
  - contract/certification.md
  - ../../legacy/python/perception-encoder-compact-package.md
---

# Model registry

The model registry is the local publication and discovery boundary for pretrained
voxel encoders. It turns a trained Python model into a directory containing weights
and descriptive metadata, maps a short reference such as `r2:v1` to that directory,
and supplies the encoder state used by Anysearch's RLlib model. This specification
describes implementation revision
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`.

## Ownership and boundary

The subsystem owns:

- writing `model.pt`, `encoder.pt`, `meta.json`, and `loss_curve.json` after garden
  training;
- the local model-reference registry and package-bundled preset registration;
- resolving a registered reference or explicit directory; and
- exposing stored metadata and encoder state to local consumers.

Dataset collection and training belong to the dataset-pipeline and
pretraining-and-qualification subsystems. Anysearch owns construction of the policy
model around the loaded encoder. Research protocols decide whether an artifact is
useful; they are evidence, not behavior implemented by this registry.

## Consumers

The `anysearch garden list` and `inspect` commands read registry metadata. Garden
training and tuning publish artifacts through `GardenStore.save`. The legacy
`PretrainedVoxelModel` resolves a reference, reconstructs `VoxelEncoder3D` from three
metadata fields, loads `encoder.pt`, and optionally freezes it. See the exact
[interfaces](contract/interfaces.md).

## Supported scope

The implemented registry is local and filesystem-backed. It supports untagged names,
`name:tag` references, explicit paths, package-bundled preset directories, and a
separate registry of reusable garden YAML files. The persisted checkpoint is a
PyTorch state dictionary; no network service or remote artifact catalog is involved.

## Maturity and limitations

Status is **draft** because the current store is usable but does not satisfy the
strong package contract described by historical Model Garden proposals. In
particular, publication is not atomic or immutable, names may be overwritten,
metadata and checkpoints are not content-hashed, registry writes are not locked, and
consumer compatibility is inferred from a small metadata subset rather than a
versioned schema. A `final_val_loss` is descriptive and is not certification.

The extensive [certification plan](contract/certification.md) remains a proposed
promotion protocol. Current `GardenStore.save` neither runs it nor records its gates.

## Reading map

- [Contract](contract/README.md): implemented guarantees and unsupported claims.
- [Interfaces](contract/interfaces.md): files, references, Python calls, CLI, and
  consumer loading.
- [Certification](contract/certification.md): proposed qualification protocol, kept
  separate from the implemented storage contract.
- [Design](design/README.md): local data flow, state, and failure boundaries.
- [Python responsibilities](design/python.md): module-by-module ownership.
- [Validation](validation.md): checks present, checks run for this review, and gaps.
