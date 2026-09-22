---
title: Compact decoder learnability and tiny-corpus overfit
status: superseded
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-encoder-compact-learnability-evidence.md
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/evidence/README.md
---

# Compact decoder learnability and tiny-corpus overfit

> This entry preserves a historical, identity-bearing protocol and is not an
> authoritative specification for new work. The original protocol text and all
> identity-bearing values are retained verbatim below.

## Archived material

This record preserves the frozen protocol for study `compact-learnability-v1`, run
`compact-learnability-v1-run1`. It defined a six-arm tiny-corpus overfit diagnostic
that separated query-decoder limitations from the voxel encoder's ability to learn
geometry codes.

## Why it was archived

The diagnostic is complete and its evidence is now interpreted within the structured
[compact encoder campaign](../../experiments/compact-encoder-campaign/README.md),
under the [engineering-screens
iteration](../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md).
That iteration owns the current chronology, results, and disposition. This page
remains at its historical path so recorded protocol references continue to resolve.

## Authority ended

Authority at this path ended when the completed diagnostic was reconstructed under
`experiments/compact-encoder-campaign/iterations/engineering-screens/`. The exact
migration commit is not recorded here. The parent diagnostic specification
`97e205793e6e443199f118b528c0c3fc9181e76c`, study and run identifiers, scene IDs,
seeds, thresholds, and other frozen protocol values below remain historical
identifiers and must not be normalized to the current tree.

## Current replacement

- The [engineering-screens execution record](../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md)
  records the run identity and protocol/source revisions.
- The [engineering-screens results](../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md)
  own the current interpretation and disposition.
- The [evidence registry](../../experiments/compact-encoder-campaign/iterations/engineering-screens/evidence/README.md)
  connects this frozen protocol with its preserved run evidence.

## Continuing evidential value

The original protocol is retained to interpret the associated model states,
predictions, reports, and run evidence without changing the meaning of their frozen
identities. It also documents that the six fits were development-only learnability
diagnostics and did not establish generalization, select an HPO winner, or qualify a
deployment checkpoint.

## Preserved original protocol

Issues specs#58 / theseo-anysearch#385. Authorized unmerged stack on #381.
Parent diagnostic spec97e205793e6e443199f118b528c0c3fc9181e76c. No merge/promotion.
Development learnability only; no HPO winner, useful-checkpoint or generalization
claim. The aim is to distinguish query-decoder limitations from learning geometry
codes out of voxel inputs before committing substantial search compute.

## Data and controls

Study compact-learnability-v1, run compact-learnability-v1-run1. Four fresh sheets
with IDs compact-learnability-v1-scene-0..3. NumPy RNG first8 little-endian SHA256
bytes of ID. Random unit normal from standard-normal3; frequency uniform[4,8],
phase uniform[-pi,pi].49-cubed coordinates -24..24 divided by8. Field is absolute
sine of frequency times projected coordinate plus phase. Occupancy below parent
quantile at fractions .08/.16/.28/.16, using midpoint quantile to avoid a threshold
on a voxel sample. Independent fixed20% mask, SHA ID plus -mask.33 input crop;
all4913 central17 voxel occupancies are overfit targets, including visible cells.
This intentionally differs from hidden-only certification: labels never become
encoder inputs and there is no held-out accuracy claim.

The exact known geometry code is six numbers: normal3, frequency/8, phase/pi,
threshold. A deterministic analytic decoder is a correctness reference; its
predictions must agree with generated targets before any fit. This code has access
to generator parameters unavailable at deployment and is never a gating model.

Three input paths: fixed oracle6; learned per-scene128-dimensional embedding table
(no voxel encoder); actual33-input grid-aggregation128 compact encoder initialized
from validated spatial checkpoint seed0, jointly trained. Never pass scene IDs or
generator code to the actual encoder. Old global projection remains excluded.

## Fit design

Each input path receives both decoder bundles: raw coordinates with one32-hidden
SiLU layer, or raw+Fourier coordinates with two128-hidden SiLU layers. Fourier
features are sin/cos(pi*f*x) for each coordinate and f in[1,2,4,8]. This changes
both positional features and decoder capacity; it is not a causal isolation of
either change. Six fits, identical seed385,2048 updates each, AdamW.001/wd.01.
Every step uses all four scenes and256 uniformly drawn central queries per scene;
shared query RNG38500. BCE positive weight is full training-corpus negatives divided
by positives. Oracle code fixed; lookup table or encoder and decoder trained jointly.

Evaluate on the same four scenes over all4913 cells at steps128/512/1024/2048,
chunk queries in256. Fixed.5 threshold, no selection. Report IoU, F1, AUPRC, BCE,
probability range, positive rate and per-scene values. Record final full-grid
predictions and model states outside Git with hashes, source/spec/data identities.
Target for learnability diagnosis: pooled IoU>=.95 AND F1>=.97 at2048. These are
overfit targets, not deployment acceptance criteria or retroactive gates.

## Execution and next-action rules

Deterministic float32, CPU threads4, TF32/cuDNN autotuning off; one CUDA process.
Whole-run cap1800s including manifest preparation, per-fit cap600s, checked every
update and at evaluation checkpoints. Preserve completed artifacts and classify
an incomplete run honestly. Measure CUDA allocated training peaks, wall time and
loss curves; no production throughput/exhaustive hardware-utilization claim.

If analytic reference fails, repair data validity before training. If even oracle
and learned table cannot overfit, examine decoder/optimization before blaming
encoder capacity. If table succeeds but encoder fails, direct work to encoder
optimization/aggregation. If stronger bundled decoder succeeds while small fails,
carry a suitable training decoder into a fresh protocol, with independent frozen
readout validation afterward. Memorization alone is never an encoder qualification.
No48 GPU-hour search begins under this short diagnostic contract.
