---
title: Reference-training refinement
status: superseded
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/encoder-continuation-and-context/README.md
  - ../../experiments/encoder-continuation-and-context/protocol.md
  - ../../experiments/encoder-continuation-and-context/iterations/003-reference-refinement/README.md
  - perception-reference-refinement-evidence.md
---

# Reference-training refinement

> This entry is a historical, frozen protocol and is not an authoritative
> specification for new work.

## Archive context

This record preserves the preregistered reference-training refinement protocol for
`voxel-reference-refinement-v1`, including its recipe order, data identities,
random streams, decision rule, budgets, and integrity requirements. Its authority
ended when the study was completed and migrated into the structured
[encoder continuation and context experiment](../../experiments/encoder-continuation-and-context/README.md).
The exact migration date is not recorded here.

Current navigation and interpretation belong to the experiment's
[retrospective protocol map](../../experiments/encoder-continuation-and-context/protocol.md)
and [reference-refinement iteration](../../experiments/encoder-continuation-and-context/iterations/003-reference-refinement/README.md).
This frozen record remains valuable for interpreting the registered procedure,
historical identities, and the associated
[evidence record](perception-reference-refinement-evidence.md). The original protocol
follows unchanged.

Issues specs#39 and theseo-anysearch#364. User authorizes the unmerged experiment
stack, without integration merges. Separate study; preserve prior verdicts.
Prior protocol: specs commit df765d0d4eed2f74a1d6e85f358e435e126d4b08,
`projects/theseo-anysearch/python/perception-encoder-checkpoint-diagnostic.md`.

## Frozen screen

Six recipes, in tie-break order, one screening seed (0). All use the same reference
architecture, unweighted BCE, 2048 AdamW updates and batch eight from the prior
checkpoint diagnostic. Select checkpoints at 16/32/64/128/256/512/1024/1536/2048
by selection log loss, ties earliest. Then select recipe by its best selection
loss, ties recipe order. No assessment data in the screen.

| Recipe | Training geometries | Masks/queries | Learning rate | Weight decay |
| --- | --- | --- | --- | --- |
| baseline | 48 | fixed | 0.001 | 0.01 |
| dynamic | 48 | freshly sampled each update | 0.001 | 0.01 |
| coverage | 192 | dynamic | 0.001 | 0.01 |
| lower_lr | 192 | dynamic | 0.0003 | 0.01 |
| higher_decay | 192 | dynamic | 0.001 | 0.1 |
| higher_lr | 192 | dynamic | 0.003 | 0.01 |

Dynamic masks are label-independent Bernoulli(0.20); draw 256 uniformly sampled
hidden query cells per volume via independent random priorities. Fewer than 256
eligible cells invalidates, never redraws. Clean boundaries are loss targets only.
Keep the reference and encoder input channel construction unchanged. The 48-grid
subset is the first 48 entries in the shared 192-grid training pool.

## Fresh confirmation

Study `voxel-reference-refinement-v1`, phase dataset identities
`voxel-reference-refinement-v1-screen-development-1` and
`voxel-reference-refinement-v1-confirmation-development-1`. Screen: 192 training
pool /48 selection, no assessment. Confirmation: fresh 192 training pool /48
selection /48 assessment, same four procedural families and three density strata.
Every geometry hash must be disjoint across phases/splits and from both earlier
diagnostic registrations. Mask streams screen 36401/36402, confirmation
36411/36412/36413; dynamic training stream 36420+seed. Model initialization and
minibatch streams match the previous reference diagnostic.

Persist the selected recipe before confirmation fits. On seeds 0/1/2 compare
baseline and selected recipe, each checkpoint-selected from the full matched update
budget. Fit the unchanged linear/32/128 probe ladder on the first 48 confirmation
training geometries, selection loss choosing capacity. Encoder weights frozen.
The chosen reference may therefore consume more training geometries than the probe;
do not interpret that contrast as a controlled architecture-only comparison.
Each model calibrates F1 on selection thresholds 0.01..0.99, ties lowest.

Primary direction follows paired assessment log loss: whole-geometry bootstrap,
2000 draws, within family/density strata, seed 362, average three seeds. Reuse the
checkpoint diagnostic's three-way comparison rule, interpreting its `best` as
chosen recipe and `final` as baseline. If chosen does not clearly beat baseline,
report unresolved training benefit. If it improves but stays below probe, refine
reference; if it clearly beats probe, investigate encoder training/representation;
overlapping intervals remain uncertain. F1 and per-family scores are diagnostic.
No promotion follows, even from success. The single-seed screen may misrank recipes;
fresh three-seed assessment tests the chosen recipe, not all possible rankings.

## Bounds and integrity

Two-hour campaign limit, at most 600 seconds per reference or probe-ladder fit;
D0 sanity reruns within 300 seconds. No automatic retry or sweep expansion.
Timeout is inconclusive; leakage, identity mismatch and changed frozen states
invalidate. Freeze source/spec commits, all corpus/query/target hashes, prior
registration hashes, LG2 checkpoint file/state hashes and resolved plan before
fitting. Report compact evidence and artifact hashes; never commit weights/corpora.
