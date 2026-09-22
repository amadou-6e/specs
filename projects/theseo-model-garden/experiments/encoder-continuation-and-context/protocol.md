# Retrospective protocol map

This experiment-level document is a retrospective umbrella reconstructed after the
decision-bearing results existed. It is **not** a frozen shared protocol. Each ordered
iteration was governed by its own pre-result protocol, identified below and summarized
in that iteration's local records. No threshold is transferred between iterations
unless the later registered protocol explicitly says so.

## Ordered registered studies

| Iteration | Frozen specification revision | Study or run identity | Decision boundary |
| --- | --- | --- | --- |
| `001-diagnostics` | `66279ceab743af9c350107fe26fca730d2b245fe` | `voxel-encoder-diagnostics-v1` | Distinguish reference/readout failure from representation failure |
| `002-checkpoint-selection` | `df765d0d4eed2f74a1d6e85f358e435e126d4b08` | `voxel-encoder-checkpoint-diagnostic-v1` | Test selection-best versus final reference checkpoints |
| `003-reference-refinement` | `44b089b58db3b9af45820cb358033c6a4acbc99f` | `voxel-reference-refinement-v1` | Screen then freshly confirm one reference-training recipe |
| `004-encoder-continuation` | `4349ad2ac47cbad912a7a984407f97bbd9042628` | `voxel-encoder-continuation-v1` | Compare old and newly pretrained encoders at matched probe exposure |
| `005-distance-retention` | `762262d657b4320dbce39d3b53bc028105a2896b` | `voxel-distance-retention-v1` | Require registered non-inferiority on clearance and recovery |
| `006-family-transfer` | `bc3a092d07309eb8f22390bd2878f371713badad` | `voxel-family-transfer-v1` | Test shells and trig-labyrinths without new-family adaptation |
| `007-context-17-to-33` | `b950249860b3e33640e9faadc3fe0a7ecabc92fc` | `voxel-context-scale-v1` | Compare central queries with 17- and 33-cubed context |
| `008-context-33-to-65` | `2f9fa46f3c26f96b9f0e1c05f9fa101a09923ad3` | `voxel-context-65-v1-run1` | Test 65 context under memory-first execution |
| `009-tiled-context` | `76bb3c403fb36b30ebf5335dcbc8f77005cf2db4` | `voxel-context-tiles-v1-run1` | Compare tiled 33 coverage with dense 65 coverage |

## Shared invariants

- Assessment data could not select models, recipes, thresholds, or interventions
  unless an iteration explicitly registered that selection split.
- Geometry, query, checkpoint, source, and specification identities were frozen before
  fitting or assessment; identity or leakage failures invalidated affected evidence.
- Missing or timed-out evidence was inconclusive, never a pass.
- Encoder state remained frozen during probe and context assessments except in the
  explicitly registered continuation pretraining arms.
- Every result was non-promotional and retained the earlier studies' verdicts.

Exact data generation, metrics, thresholds, budgets, permitted adaptations, and
forbidden changes are recorded in each iteration's local records. Preserved legacy
documents remain provenance and are indexed in `sources.md`; they are not the only
navigational home of the canonical experiment.
