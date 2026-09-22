---
title: Compact search post-hoc diagnosis
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/compact-encoder-campaign/protocol.md
  - ../../experiments/compact-encoder-campaign/iterations/optimization/README.md
  - ../../experiments/compact-encoder-campaign/iterations/optimization/execution.md
  - ../../experiments/compact-encoder-campaign/iterations/optimization/results.md
  - ../../subsystems/encoder-models/README.md
  - ../../subsystems/pretraining-and-qualification/README.md
---

# Compact search post-hoc diagnosis

> This entry is a preserved historical diagnostic protocol and completion record.
> It is not an authoritative specification for new Model Garden work, and its
> frozen identities, budget, measurements, and recorded outcomes must not be
> revised retrospectively.

## Archival context

This page preserves the original post-hoc diagnosis authorized through specs #64
and implementation #391 for the already completed compact search. Its authority as
an executable analysis ended when the registered diagnosis completed and its
evidence was recorded below. The exact analysis identity, report hashes, checkpoint
selection, resource accounting, tolerances, measurements, and conclusions remain
identity-bearing historical evidence.

Use the [compact encoder campaign](../../experiments/compact-encoder-campaign/README.md)
for the current bounded interpretation of the program, its
[protocol lineage](../../experiments/compact-encoder-campaign/protocol.md), and the
[optimization iteration](../../experiments/compact-encoder-campaign/iterations/optimization/README.md)
for the current execution and result map. Current reusable representation contracts
belong to [encoder models](../../subsystems/encoder-models/README.md); current
training, evidence, and promotion rules belong to
[pretraining and qualification](../../subsystems/pretraining-and-qualification/README.md).
This archive remains necessary to interpret `compact-search-diagnosis-v1-run1`, the
six analyzed checkpoints, the spectrum and ablation evidence, the charged campaign
budget, and why the findings motivated a fresh successor comparison without changing
the original compact-search result.

## Preserved historical record

Issues specs#64 / implementation#391. Authorized unmerged stack on #389, not merge
authorization. This is explanatory analysis of an already completed search, not
a revised search, new training comparison, independent validation or certification.

## Frozen inputs and budget

Analysis identity compact-search-diagnosis-v1-run1. Pin a full specs SHA, clean
implementation source SHA, original registration identity and report payload
572e8910c6d1934f59662a9b79312f0a08e482fb91dfe2d832f08a6bca8048a6 before execution.
Select the two original final-stage trial IDs and their512/2048/8192 checkpoints.
Verify each original artifact hash. Use only the original probe/selection arrays
under their original identities and hashes. Reuse is intentional for post-hoc
explanation; do not assign these arrays a misleading new independent dataset ID.
No development data access, winner reselection or changes to the original report.

Cap900 seconds within the user's existing48 GPU-hour authorization and exclusive
campaign ledger lock. Reserve120 of those seconds conservatively for preceding
post-search verification/report overhead; at most780 seconds for this analysis.
Charge the reservation before execution and retain it on failure/interruption.
A started, incomplete analysis may not silently restart or obtain free time.
No overlapping GPU experiment. CPU threads4, deterministic float32 inference,
float64 spectra, TF32/autotuning disabled. Preserve weights outside Git.

## Measurements

For each of the six saved checkpoints, extract frozen probe/selection vectors.
Verify encoder state remains unchanged. Recompute the saved ridge predictions and
require agreement with the original saved selection predictions (rtol1e-5,
atol1e-6); differences outside tolerance are a validity failure, not new evidence.

Probe-vector diagnostics: per-coordinate standard deviation, entropy effective
rank of the centered covariance spectrum, leading eigenvalue fraction and
mean vector norm. Report dimension and numeric spectrum. No arbitrary pass/fail
rank gate is introduced after observing scores.

Compare, on the original eligible selection cells:

- Original independent ridge head and frozen original thresholds.
- Original jointly trained dense decoder, class sigmoid and distance clamp[0,1].
- Ridge with vectors replaced by the probe mean, by zeros, or permuted across
  selection scenes with fixed CPU-generator seed391. Do not retune thresholds for
  these ablations. Zero vectors may be out of distribution; mean/permutation are
  the more informative companions.
- A no-input spatial prior: probe-target mean at each output cell, broadcast to
  selection scenes. This diagnoses position/family-mixture priors, not raw geometry.

For trained-decoder/prior diagnostics only, select F1 thresholds over.01..99 on
selection, lower ties, and explicitly label these post-hoc calibrated diagnostics.
No model weights are optimized. Report all four task scores and all families;
these comparisons do not establish nonlinear control superiority or pretraining
benefit. A shuffled vector can legitimately perform poorly because scenes differ;
the magnitude diagnoses necessity but is not an independent usefulness certificate.

## Evidence-directed continuation

If a trained head is stronger than the fresh ridge head, investigate readout
adaptation under a new protocol. If both are weak and feature rank falls or the
head is insensitive to permutation, investigate representation/optimization.
If prior performance is close, identify the shortcut rather than celebrate pooled
scores. Multiple mechanisms may coexist; avoid a causal claim from this analysis.
The next actual training comparison requires fresh identities/data, frozen changes
and budget, not revised thresholds on this search. Favor small-field training or
decoder/aggregation changes over increasing field size. Keep original failures.

Commit registration, compact diagnostic report, hashes and assessment. Do not stop
at the diagnostic when an in-scope next training experiment is justified and budget
remains. No automatic integration merge or promotion.

## Completed evidence

Source91de70a / evidencebaee828 on implementation#391. All six input checkpoint
hashes and encoder states verified; regenerated ridge predictions matched original
saved predictions. Full garden suite462 passed. Report payload
49f6cfd3cab1b0ff1c2542cdc709731c89cd6d798af4d4987fbf0999023e2e6d.
29.297s analysis plus120s conservative overhead charged within the campaign.

Probe covariance entropy rank ranges1.33-2.07 for grid64 and falls to1.000001 for
grid192 at8192 updates (leading variance fraction .99999993). At that checkpoint,
ridge boundary F1 .1985 and shuffled-vector F1 .1938 are near the spatial prior
.1902. Grid64 still uses scene information (.2815 real versus .1613 shuffled),
but its trained decoder (.2811) is also weak. This motivates a fresh small-field
anti-collapse/detail training comparison. Entropy rank is variance concentration,
not literal matrix rank or information capacity. No independent qualification or
change to the original search result follows from this analysis.
