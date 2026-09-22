---
title: Context-scale pilot evidence
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-context-scale.md
  - ../../experiments/encoder-continuation-and-context/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/007-context-17-to-33/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/007-context-17-to-33/execution.md
  - ../../experiments/encoder-continuation-and-context/iterations/007-context-17-to-33/results.md
  - ../../experiments/encoder-continuation-and-context/iterations/007-context-17-to-33/evidence/README.md
  - ../../subsystems/encoder-models/README.md
---

# Context-scale pilot evidence

> This entry is historical, identity-bearing evidence and is not an
> authoritative specification for new work.

## Archived material

This record preserves the compact outcome and integrity evidence for the
fixed-resolution 17-to-33 context pilot. It identifies the governing issue and
specification revision, executable revision, measured task and resource outcomes,
bounded interpretation, and report payload identity.

## Why it was archived

The pilot is now represented by the structured
[encoder continuation and context experiment](../../experiments/encoder-continuation-and-context/README.md),
specifically [iteration 007](../../experiments/encoder-continuation-and-context/iterations/007-context-17-to-33/README.md).
This page remains in place because its historical hashes, issue references, summary
measurements, and artifact path are evidence used to interpret that completed run.

## Authority ended

This page ceased to be the active account when the pilot was migrated into the
structured experiment record. The exact migration date is not recorded in the
preserved evidence. New work must use the current experiment and applicable
[encoder-model contracts](../../subsystems/encoder-models/README.md).

## Current replacement

The canonical structured account is
[iteration 007 — Fixed-resolution 17-to-33 context pilot](../../experiments/encoder-continuation-and-context/iterations/007-context-17-to-33/README.md).
Its [execution](../../experiments/encoder-continuation-and-context/iterations/007-context-17-to-33/execution.md),
[results](../../experiments/encoder-continuation-and-context/iterations/007-context-17-to-33/results.md),
and [evidence manifest](../../experiments/encoder-continuation-and-context/iterations/007-context-17-to-33/evidence/README.md)
own the current structured description. The matching
[frozen protocol](perception-context-scale.md) remains archived alongside this
evidence.

## Continuing evidential value

The preserved text below records the exact protocol and executable revisions,
reported score ranges, resource observations, report payload identity, and limits
on promotion claims. These details support audit of the migrated experiment and old
artifacts; they do not authorize another run or establish current model behavior.

## Preserved evidence

Issues specs#47 / theseo-anysearch#372. Frozen protocol
`b950249860b3e33640e9faadc3fe0a7ecabc92fc`; executable `6dea43e`.

Completed17/33 fixed-resolution paired pilot, three seeds, frozen and retrained
arms. Shared frozen encoder at33 improved all four central-query tasks with
positive paired intervals. Boundary F1 rose from0.696-0.722 to0.739-0.756;
IoU from0.660-0.679 to0.687-0.717. Distances also improved.

Short512-update retraining did not beat the established frozen33 encoder on
surface tasks. Retain shared weights as the working direction. A separately
registered65-cubed frozen/resource check is next, not automatic execution or a
claim about radius512. Probes were scale-adapted; full-volume accuracy untested.

Batch4 incremental inference allocation rose from9.93 to72.91 MiB. Short timing
measurements are noisy and not production scaling guarantees. Recorded whole
run duration247.15s; no out-of-memory error.

Report payload `e66dfdecf165ee75bbf6255741968d3acb3457a696f9b851a385c444af062bfe`.
Implementation assessment: docs/perception-context-scale-assessment.md.
All weights/corpora remain untracked; no promotion or integration merges.
