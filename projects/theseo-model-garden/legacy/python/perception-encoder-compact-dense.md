---
title: Compact dense-output learnability positive control
status: superseded
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md
  - perception-encoder-compact-dense-evidence.md
---

# Compact dense-output learnability positive control

> This entry preserves a historical frozen protocol and is not an authoritative
> specification for new work. Its protocol text and identity-bearing values are
> retained verbatim below.

## Archived material

This page is the original protocol for study `compact-dense-v1`, run
`compact-dense-v1-run1`. It specified a direct dense-output positive control after
the earlier coordinate-query decoder arms failed their tiny-corpus learnability
targets.

## Why it was archived

The protocol and its resulting evidence are now interpreted as one screen in the
structured [compact perception-encoder campaign](../../experiments/compact-encoder-campaign/README.md).
That experiment entry owns the campaign chronology, scope, and present disposition;
this page remains at its historical path for provenance.

## Authority ended

Authority at this path ended when the compact campaign was reconstructed under
`experiments/compact-encoder-campaign/`. The exact migration commit is not recorded
here. The frozen protocol identity
`fd8eba978a6100b997cc762dbea6078d3b0f5686` and source revision `2afe8f0` remain
historical identifiers and must not be normalized to the current tree.

## Current replacement

- [Campaign overview](../../experiments/compact-encoder-campaign/README.md)
- [Engineering-screens iteration](../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md)
- [Execution ledger](../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md)
- [Consolidated results](../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md)

## Continuing evidential value

The record preserves the exact prospective constraints, gates, identities, resource
limits, and interpretation rules needed to audit `compact-dense-v1-run1`. Its
[retained evidence](perception-encoder-compact-dense-evidence.md) records the run
outcome. Neither record establishes generalization, certification, or promotion.

## Preserved historical protocol

Issues specs#60 / implementation#386. Authorized unmerged follow-up to #385.
Prior protocol1bf1359b55b7c9aef2de1fe23a831e2e850009e0. Oracle/table query-decoder
arms failed tiny-corpus targets despite exact analytic oracle reconstruction.
This control removes the coordinate-conditioned readout difficulty; it does not
establish generalization, a deployable decoder, an HPO winner or certification.

Study compact-dense-v1, run compact-dense-v1-run1. Use #385 generator and validity
checks with fresh IDs compact-dense-v1-scene-0..3. Four sheets, parent49/input33,
fixed20% hidden mask, all4913 central17 labels including visible cells. All labels
are training targets, never encoder inputs. Hash parent/input/mask/target/code;
analytic generator-code decoder must reproduce the target exactly.

Three independently initialized fits: oracle6 code fixed; learned per-scene128
table; actual128 grid-aggregation encoder jointly trained from spatial checkpoint
seed0. A single linear layer maps each code directly to4913 logits. No queries,
local feature skips or generator parameters enter the actual encoder decoder.
All three trainable decoders receive the whole code; no global average substitution.
Seed386 before model creation, AdamW.003/wd.01,1024 full-batch updates (four scenes,
all central voxels), positive BCE weight training negatives/positives. Old backbone
global projection excluded. This changes head structure, query exposure and LR;
interpret as a positive control, not an isolated causal attribution or matched
compute comparison against #385. Report actual parameter and resource costs.

Evaluate complete training grids at128/256/512/1024, fixed.5 threshold. Report
IoU/F1/AUPRC/BCE and per-scene scores. Learnability target pooled IoU>=.95 and
F1>=.97. No early stopping, threshold changes or architecture selection. Save
provider/decoder states and full predictions outside Git, with hashes and replay.

One deterministic float32 CUDA process, CPU threads4, no TF32/autotuning. Overall
1200s including preparation, per-fit600s, checked every update. Record train wall
time and CUDA allocated peak. Do not execute concurrently with another GPU fit;
finish and assess the #385 run first. Source/spec/checkpoint identities frozen.

If oracle/table succeeds, coordinate-query readout was not a necessary route to
fitting these grids. If the real encoder also succeeds, proceed to a fresh
train/probe/selection/development study using the dense training decoder and
independent frozen readouts; memorization alone is not sufficient. If only table
succeeds, diagnose the encoder path. If all fail, debug optimization/normalization
before HPO. Maintain all earlier failed outcomes unchanged; no merge or promotion.
