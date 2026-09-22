---
title: Reference refinement evidence
status: superseded
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-reference-refinement.md
  - ../../experiments/encoder-continuation-and-context/README.md
  - ../../experiments/encoder-continuation-and-context/protocol.md
  - ../../experiments/encoder-continuation-and-context/iterations/003-reference-refinement/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/003-reference-refinement/results.md
  - ../../experiments/encoder-continuation-and-context/iterations/003-reference-refinement/evidence/README.md
---

# Reference refinement evidence

> This entry is historical evidence and is not an authoritative specification for
> new work.

## Archived material

This record preserves the outcome summary and artifact identities produced by the
completed `voxel-reference-refinement-v1` study. It accompanies the archived
[frozen protocol](perception-reference-refinement.md).

## Why it was archived

The study was completed and its navigational and interpretive ownership moved to
the structured
[encoder continuation and context experiment](../../experiments/encoder-continuation-and-context/README.md).
This archive remains unchanged as the compact historical evidence record; it does
not define a current training recommendation or promotion decision.

## Authority ended

Authority ended when the completed study was migrated to the structured experiment.
The exact migration date is not recorded in this evidence.

## Current replacement

Use the experiment's
[retrospective protocol map](../../experiments/encoder-continuation-and-context/protocol.md),
[reference-refinement iteration](../../experiments/encoder-continuation-and-context/iterations/003-reference-refinement/README.md),
[results](../../experiments/encoder-continuation-and-context/iterations/003-reference-refinement/results.md),
and [evidence manifest](../../experiments/encoder-continuation-and-context/iterations/003-reference-refinement/evidence/README.md)
for current navigation and interpretation.

## Continuing evidential value

The record retains the frozen protocol and executable revisions, measured outcomes,
runtime, absence of committed weights, and report-payload identity needed to
interpret the historical study and verify its migrated summary.

## Historical evidence

Issues specs#39 / theseo-anysearch#364. Frozen protocol
`44b089b58db3b9af45820cb358033c6a4acbc99f`, executable `7f3727c`.

Six fixed single-seed screening recipes selected dynamic masks, 192 geometries,
learning rate 0.003 and weight decay 0.01. Fresh three-seed assessment:
refined boundary F1 0.7628/0.7805/0.7468; baseline 0.4897/0.4879/0.4697;
frozen probe 0.6275/0.6182/0.6376. Paired loss improvement over baseline
0.1187 (95% CI [0.1023,0.1318]), over probe 0.0531 ([0.0296,0.0740]).

Outcome `reference_exceeds_probe`. Training refinement is a supported direction
with architecture fixed. No promotion: oblique-sheet F1 remains below 0.70 in two
seeds, and the reference has 192 training geometries versus the probe's 48.
Next proposed study equalizes probe exposure and tests broader-data/dynamic-mask
encoder pretraining at fixed architecture. This is a proposal, not a protocol
amendment or executed encoder study. No topology/scaling claims follow.

Completed in 256.16 recorded seconds, zero encoder updates. No weights committed.
Full implementation assessment: `docs/perception-reference-refinement-assessment.md`
on exp/364; report payload
`0baf857fccb0bc18ecb8c4aa917a2028d20d4625941a69f0de1460be94801043`.
