---
title: Compact dense-output learnability evidence
status: superseded
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-encoder-compact-dense.md
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/evidence/README.md
---

# Compact dense-output learnability evidence

> This entry preserves historical run evidence and is not an authoritative
> specification for new work. The original evidence text and all identity-bearing
> values are retained verbatim below.

## Archived material

This page records the outcome and disposition of study `compact-dense-v1`, run
`compact-dense-v1-run1`, under the frozen
[dense-output protocol](perception-encoder-compact-dense.md). It preserves the
reported measurements, resource use, test result, protocol and source identities,
and machine-payload identity.

## Why it was archived

The evidence is now interpreted within the structured
[compact perception-encoder campaign](../../experiments/compact-encoder-campaign/README.md).
The campaign's engineering-screens iteration owns the current chronology,
interpretation, and disposition. This page remains at its historical path so old
reports and identities continue to resolve.

## Authority ended

Authority at this path ended when the compact campaign was reconstructed under
`experiments/compact-encoder-campaign/`. The exact migration commit is not recorded
here. Protocol identity `fd8eba978a6100b997cc762dbea6078d3b0f5686`, source
revision `2afe8f0`, run identity `compact-dense-v1-run1`, and machine-payload identity
`ab01e6a66c5c83969149f8ba9bbfdd2df3eff28f7b2b25f4573b7b5f19939e96` remain
historical identifiers and must not be normalized to the current tree.

## Current replacement

- [Campaign overview](../../experiments/compact-encoder-campaign/README.md)
- [Engineering-screens iteration](../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md)
- [Execution ledger](../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md)
- [Consolidated results](../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md)
- [Evidence index](../../experiments/compact-encoder-campaign/iterations/engineering-screens/evidence/README.md)

## Continuing evidential value

This record supports audits of the dense-output positive control, interpretation of
the named run and machine payload, and comparison with the preceding query-decoder
learnability screens. It supports the bounded conclusion that the compact training
path memorized four scenes; it does not establish generalization, certification,
deployment-head quality, or promotion.

## Preserved historical evidence

# Dense compact learnability evidence

Specs#60 / implementation#386; protocolfd8eba978a6100b997cc762dbea6078d3b0f5686,
source2afe8f0. Run compact-dense-v1-run1,76.765s.1024 full-grid updates per arm.
Learned table128 and actual voxel encoder128 reach IoU/F1=1 already at128 updates.
Oracle6 reaches.9223/.9596, below frozen .95/.97 targets. Preserve all outcomes.

The actual compact training path can memorize four scenes; no generalization,
hidden-only quality, efficient deployment-head or HPO-winner claim follows.
Different head structure/LR/exposure prevent an isolated causal comparison to
query decoder fits. Proceed to fresh multi-scene training and independent frozen
readouts. User approved up to48 GPU-hours for the campaign on2026-09-12; no merges.
449 garden tests passed. Full report docs/perception-compact-dense-assessment.md
in implementation repository; machine payload
ab01e6a66c5c83969149f8ba9bbfdd2df3eff28f7b2b25f4573b7b5f19939e96.
Disposition retain engineering direction; no certification or promotion.
