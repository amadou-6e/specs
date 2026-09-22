# Model-registry contract

This page defines the observable behavior implemented by the local registry. It does
not elevate the historical certification proposal into a current guarantee.

## Publication guarantees

Given a model with an extractable encoder and a validated `GardenConfig`,
`GardenStore.save(name, ..., tag)` writes the following files beneath the configured
store root:

| File | Implemented content |
|---|---|
| `model.pt` | Full model `state_dict` for reconstruction or inspection |
| `encoder.pt` | Extracted encoder `state_dict` used by downstream policies |
| `meta.json` | Name, tag, approach, architecture, encoder dimensions, training summary, augmentation, sources, and creation time |
| `loss_curve.json` | Epoch-level training records supplied to `save` |

With a tag, the package directory is `<root>/<name>/<tag>`; without one it is
`<root>/<name>`. Saving updates the machine-local YAML registry so the name and, when
present, `name:tag` resolve to the written location. The implementation overwrites
existing files at the same destination and provides no atomic transaction across the
four files and registry update.

## Discovery and resolution

Resolution first handles a Windows drive-letter path, then parses an optional tag,
then consults the global registry. An exact registry key wins. A family entry plus a
tag resolves only if the candidate tag directory contains `meta.json`. If no registry
entry exists, an existing filesystem path is accepted. Otherwise resolution raises
`KeyError`; it does not silently choose a different model.

Importing `theseo_anysearch.garden` scans the package's `garden/pretrained`
directories. A directory is registered only when it contains `encoder.pt`. Existing
registry entries whose targets still exist are retained, so a user registration can
take precedence over a bundled preset.

## Loading guarantees

`GardenStore.load_encoder_state` loads only `encoder.pt`, with
`torch.load(..., weights_only=True)` and caller-selected `map_location`. Missing
checkpoints and metadata raise `FileNotFoundError`. `meta` returns parsed JSON;
`loss_curve` uniquely treats a missing curve as an empty list.

The current RLlib consumer requires `box_radius`, `latent_dim`, and `conv_channels`
in `meta.json`, always reconstructs `VoxelEncoder3D`, and requires the state dictionary
to load strictly into that architecture. A frozen encoder has gradients disabled and
is put into evaluation mode. This loading path therefore does **not** implement a
generic architecture registry despite `GardenConfig` supporting multiple training
architectures.

## Identity and determinism

Names and tags are mutable aliases, not content identities. `created_at` makes
metadata time-dependent. No checksum binds metadata to either checkpoint, and no
schema version binds producer to consumer. Consequently, equal references do not
guarantee equal bytes across machines or across successive saves.

## Rejection and failure behavior

- Unknown references and unknown tags fail explicitly.
- Missing model metadata causes CLI inspection or policy construction to fail.
- Malformed YAML/JSON and invalid checkpoint contents propagate parser or PyTorch
  errors; there is no quarantine or recovery path.
- Concurrent writers are not coordinated. Partial files or lost registry updates are
  possible if publication is interrupted or processes race.
- Registry entries may point outside the store and are treated as trusted local input.

## Unsupported claims

The implementation does not currently guarantee certification, immutable release
history, provenance completeness, cryptographic integrity, safe untrusted loading,
atomic publication, remote distribution, architecture negotiation, or compatibility
across schema changes. Those claims require future contracts and tests; the
[certification plan](certification.md) by itself does not provide them.
