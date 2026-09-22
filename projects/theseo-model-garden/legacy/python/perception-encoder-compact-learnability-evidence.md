---
title: Compact learnability evidence
status: superseded
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-encoder-compact-learnability.md
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/evidence/README.md
---

# Compact learnability evidence

> This entry preserves historical run evidence and is not an authoritative
> specification for new work. The original evidence text and all identity-bearing
> values are retained verbatim below.

## Archived material

This page records the outcome and disposition of study `compact-learnability-v1`, run
`compact-learnability-v1-run1`, under the frozen
[compact learnability protocol](perception-encoder-compact-learnability.md). It
preserves the reported measurements, limitations, test result, protocol and source
identities, and machine-payload identity.

## Why it was archived

The evidence is now interpreted within the structured
[compact perception-encoder campaign](../../experiments/compact-encoder-campaign/README.md).
The campaign's engineering-screens iteration owns the current chronology,
interpretation, and disposition. This page remains at its historical path so old
reports and identities continue to resolve.

## Authority ended

Authority at this path ended when the compact campaign was reconstructed under
`experiments/compact-encoder-campaign/`. The exact migration commit is not recorded
here. Protocol identity `1bf1359b55b7c9aef2de1fe23a831e2e850009e0`, source
revision `91d50ad`, run identity `compact-learnability-v1-run1`, and machine-payload
identity `00e7511e6dd9ba360140428fc249689b9f7c5db0dab62b28bd226f58123ea256`
remain historical identifiers and must not be normalized to the current tree.

## Current replacement

- [Campaign overview](../../experiments/compact-encoder-campaign/README.md)
- [Engineering-screens iteration](../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md)
- [Execution ledger](../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md)
- [Consolidated results](../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md)
- [Evidence index](../../experiments/compact-encoder-campaign/iterations/engineering-screens/evidence/README.md)

## Continuing evidential value

This record supports audits of the tiny-corpus query-decoder overfit screen and
interpretation of the named run and machine payload. It preserves evidence that all
six learned readout arms missed the declared overfit targets while the analytic
generator-code reference recovered the targets exactly. It does not establish
insufficient 128-dimensional capacity, generalization, certification, or promotion.

## Preserved historical evidence

# Compact learnability evidence

Specs#58 / implementation#385. Protocol1bf1359b55b7c9aef2de1fe23a831e2e850009e0,
source91d50ad. Run compact-learnability-v1-run1,303.141 seconds, six2048-step fits.
All failed overfit IoU.95/F1.97 targets. Plain32 IoU about.20 for oracle/table/encoder;
Fourier128 IoU.242 oracle/.374 table/.334 encoder. Analytic oracle exactly recovers
all targets: code information sufficiency does not guarantee learned readout success.

Next action already prepared: specs#60 / implementation#386 direct dense-output
positive control, fresh data, no coordinate-query decoder. These results cannot
establish insufficient128-dimensional capacity or generalization. Four scenes,
one seed, visible+hidden training labels; Fourier/capacity bundled change.
447 garden tests passed; final states/predictions hashed outside Git. Disposition
retain diagnostic. No merge, HPO winner or certification. Full report:
docs/perception-compact-learnability-assessment.md in implementation repository.
Machine payload00e7511e6dd9ba360140428fc249689b9f7c5db0dab62b28bd226f58123ea256.
