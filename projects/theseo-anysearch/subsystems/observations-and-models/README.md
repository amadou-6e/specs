---
title: Observations and policy models
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
related: []
---

# Observations and policy models

This subsystem defines how environment state becomes policy input and how custom
RLlib models turn that input into action scores and value predictions. It owns schema,
normalization, model compatibility, auxiliary features, and masking at the model
boundary—not environment transitions or training protocols.

The specification was audited at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`. It is draft because inspected tests were
not run and a stale cursor dependency remains open in policy explainability.

`VoxelEnv` supports scalar, box, radial, and hierarchical-box observation modes.
Multi-agent environments have a separate local-grid/neighbor/ray schema. Custom CNNs
consume `local_grid` spatially and other non-mask keys as auxiliary features. The
optional action mask changes output logits, not encoder input.

[Theseo Model Garden](../../../theseo-model-garden/README.md) is a separately owned,
optional product that publishes pretrained representation packages. Anysearch owns
only the compatibility and loading boundary; Model Garden is not an internal
extension or part of the base observation guarantee.

## Important limitations

- Scalar mode without goal fields is empty and unsuitable for a feed-forward policy.
- Removed cursor/time fields, unit-vector goal direction, and kind-preserving box
  encoding break compatibility with older checkpoints; no silent adaptation exists.
- Single-agent and multi-agent schemas are intentionally different.

## Reading map

- [Contract](contract/README.md)
- [Interfaces](contract/interfaces.md)
- [Extension contract](contract/extensions.md)
- [Design](design/README.md)
- [Validation](validation.md)
- [Schema migration](migrations.md)
