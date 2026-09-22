---
title: Perception encoder program state review
status: complete
kind: research
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: ../perception-encoder-state-review.md
related:
  - ../../legacy/python/perception-encoder-r0-result.md
  - ../../legacy/python/perception-encoder-compact-validation-assessment.md
  - ../../legacy/python/perception-encoder-collision-readout-assessment.md
---

# Perception encoder program state review

This topic reconstructs the recorded state of the perception-encoder program from
retained Model Garden specifications and assessments. It answers what the completed
audits and frozen-code studies established, which continuation gates remained closed,
and what they did not establish. It is a documentation synthesis, not a new experiment
or an artifact-promotion decision.

## Question and relevance

- What outcomes were recorded for the v2r1 calibration, v2r2 R0 audit, frozen compact
  encoder robustness study, and frozen collision-readout follow-up?
- Which conclusions are supported across those records?
- Which follow-up work remained unauthorized or unstarted?

The answer matters because a high absolute metric can coexist with a failed comparative
gate, and because retaining useful evidence is not equivalent to promoting an encoder.

## Non-questions

This review does not determine the best encoder architecture, validate navigation
performance, approve a Model Garden artifact, or replace the frozen protocols and
assessments. It does not independently reproduce their runs or inspect runtime-only
weights and arrays.

## Method and search date

The review was reconstructed on 2026-09-22 from four retained local records. The full
[method](method.md) distinguishes their reported experimental evidence from facts
verified by inspecting this repository's documentation structure.

## Evaluation criteria

Records were compared on protocol state, gate outcome, evaluated distribution,
baseline or control relationship, explicit disposition, and stated limitations.
Conclusions are included only where a characterized source states the underlying
result or where the synthesis follows directly from multiple such dispositions.

## Synthesized findings

- [F-001](findings/F-001-r0-deferred.md) records that v2r2 R0 ended in `defer` because
  class-support and conservative audit gates failed; it was not an architecture test.
- [F-002](findings/F-002-robustness-limited.md) records substantial failures under
  distribution shifts, so the frozen compact encoder did not demonstrate broad
  robustness.
- [F-003](findings/F-003-collision-heads-not-competitive.md) records repeatable
  improvements from revised collision heads without competitiveness against raw-grid
  and spatial controls.
- [F-004](findings/F-004-no-promotion.md) synthesizes the consistent program-level
  disposition: retain the evidence, but do not infer promotion or authorize further
  encoder training from these records.

The historical v2r1 calibration values were:

| Component | Floor | Reference | Recorded outcome |
| --- | ---: | ---: | --- |
| Occupied IoU | 0.5974 | 0.9551 | Passed |
| Boundary F1 | 0.5913 | 0.9864 | Passed |
| Clearance NMAE (lower is better) | 0.2231 | 0.0913 | Passed |
| Reachability AUPRC | 0.9309 | 0.9971 | Failed the 0.10 headroom requirement |
| Geodesic NMAE | unavailable | unavailable | Deferred |

The reachability gate was comparative: the coordinates-only reference was too strong
for the required headroom even though its absolute AUPRC was high. The retained record
does not establish linear decodability of connectivity from raw occupancy.

## Program-state comparison

| Work | Recorded result | Supported interpretation | Unsupported interpretation |
| --- | --- | --- | --- |
| v2r1 P0C | Reachability headroom failed | The candidate did not clear the registered comparative gate | Reachability was generally poor |
| v2r2 R0 | `defer`; `no_topology_identifiable` | Evidence was insufficient under the audited prior, controls, and budget | Hidden topology is universally unidentifiable |
| Frozen robustness | Many shifted conditions missed retained targets | Broad distributional robustness was not demonstrated | The encoder is useless in every regime |
| Collision readout | Revised heads improved but did not beat controls | Head design recovered some signal but did not establish compact-code competitiveness | Encoder retraining or promotion was justified |

## Applicability and limitations

These findings apply to the specific frozen encoders, synthetic generators, masks,
controls, budgets, and readouts named by the source records. The studies did not test
RL navigation, global reachability, continuous swept volumes, sensor noise beyond the
declared corruptions, or arbitrary real-world distributions. This review inspected
retained Markdown records; it did not rerun experiments or validate runtime-only data.

## Recommendation and open questions

Preserve these outcomes as evidence and require any successor to state which failed
gate or limitation it addresses. A future comparative experiment would need a frozen
contract, eligible baselines, and explicit continuation gates. This review itself does
not authorize that experiment or select an architecture.

Open questions include whether a later representation and readout can outperform
spatial controls under an accepted contract, and which data distribution is relevant
to downstream navigation.

## Sources

See the [source registry](sources/README.md). The records characterize retained local
specifications and assessments; none is presented as independent external research.
