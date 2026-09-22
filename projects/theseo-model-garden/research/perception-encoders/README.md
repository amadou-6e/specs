---
title: Scalable 3D voxel perception encoders
status: discovery
kind: research
owners: [amadou-6e]
last_reviewed: 2026-09-01
applies_to: [theseo-model-garden]
supersedes: research/perception-encoders.md
related:
  - https://github.com/amadou-6e/specs/issues/5
  - https://github.com/amadou-6e/specs/issues/9
  - https://github.com/amadou-6e/specs/issues/11
---

# Scalable 3D voxel perception encoders

This topic preserves and structures the project's historical investigation of a
reusable perception encoder for 3D voxel observations. The migration did not repeat
the literature review. Consequently, the records below characterize the predecessor
document as the inspected source and distinguish its project proposals from verified
external evidence.

## Question and relevance

Which perception architecture could be pretrained on 3D voxel observations, stored
in the Model Garden, frozen during path-finding training, and reused with a small
task-specific head across observation radii from 2 through 512?

The question matters because dense voxel inputs scale cubically, while reusable
checkpoints require stable observation semantics and a clearly defined frozen
boundary.

## Non-questions

This topic does not certify an encoder, authorize a dependency, establish a production
checkpoint contract, or show that frozen transfer improves navigation. Those outcomes
require the experiments and decisions identified below.

## Method and search date

The available material is a historical synthesis last reviewed on 2026-09-01. Its
original search process and per-source inspection depth were not recorded. See the
[method](method.md) for the migration boundary and limitations.

## Evaluation criteria

The predecessor compared candidates by memory scaling, preservation of occupancy
semantics, spatial detail, implementation complexity, portability, checkpoint
compatibility, and suitability for frozen transfer. It proposed evaluating geometric
probes, downstream navigation, latency, memory, radius generalization, and controlled
ablations. These are recorded criteria, not completed measurements.

## Synthesized findings

- [F-001](findings/F-001-dense-input-scaling.md) records the cubic scaling constraint
  that motivated alternatives to a dense radius-512 cube.
- [F-002](findings/F-002-explicit-occupancy-semantics.md) records the requirement to
  preserve occupied, known-free, unknown, and invalid-space distinctions.
- [F-003](findings/F-003-goal-independent-boundary.md) records the proposed reusable,
  goal-independent encoder boundary.
- [F-004](findings/F-004-sparse-hierarchical-candidates.md) records that sparse and
  hierarchical families were plausible but unvalidated candidates.
- [F-005](findings/F-005-fixed-grid-pyramid-pilot.md) records the predecessor's
  recommendation to pilot a fixed-grid multiresolution residual encoder first.
- [F-006](findings/F-006-geometry-aware-pretraining.md) records the proposed geometric
  and planning-aware pretraining objectives.
- [F-007](findings/F-007-frozen-transfer-controls.md) records that frozen transfer was
  a hypothesis requiring matched controls.
- [F-008](findings/F-008-promotion-evidence.md) records the proposed separation between
  standalone certification and downstream planner evidence.

All eight findings are reconstructions from one historical project source. Their
support therefore establishes what was proposed, not whether the underlying external
claims or the proposed design are correct.

## Comparison

The predecessor considered dense voxel CNNs, sparse CNNs, octree encoders, point
encoders, tri-plane representations, implicit fields, and a fixed-grid
multiresolution residual encoder. It treated the dense CNN as a bounded-radius
baseline, sparse and octree approaches as higher-complexity candidates, tri-plane
processing as a lower-cost topology-risk baseline, and the fixed-grid pyramid as the
first scalable engineering hypothesis. No independently verified comparison matrix
can be produced from the surviving inspection record.

## Applicability and limitations

The constraints and proposed evaluation dimensions apply directly to Model Garden
encoder work. Reported results from adjacent 2D, 3D, robotics, and mapping literature
do not automatically transfer to Theseo's observation semantics, radii, hardware, or
navigation tasks. A future literature refresh must characterize each cited source
individually before treating its claims as evidence.

## Recommendation and open questions

The historical recommendation was to implement only the data contract, raw-grid
control, dense radius-32 residual baseline, and a Tiny fixed-grid pyramid before
scaling radius or capacity. That remains a research recommendation, not an accepted
architecture.

Open questions include whether conservative multiscale aggregation retains useful
topology, whether shared weights work across physical scales, whether a global latent
is sufficient, whether frozen transfer beats matched controls, and whether specialized
sparse backends meet portability requirements.

## Sources

The [source registry](sources/README.md) currently contains only the inspected
historical synthesis. Its embedded bibliography is preserved for later
source-by-source characterization.
