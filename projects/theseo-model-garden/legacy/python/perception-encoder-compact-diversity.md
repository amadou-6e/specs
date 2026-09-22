---
title: Compact feature diversity and detail training
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/compact-encoder-campaign/iterations/optimization/README.md
  - ../../experiments/compact-encoder-campaign/iterations/optimization/execution.md
  - ../../experiments/compact-encoder-campaign/iterations/optimization/results.md
  - ../../experiments/compact-encoder-campaign/iterations/optimization/evidence/README.md
---

# Compact feature diversity and detail training

> This entry is a historical, identity-bearing protocol and evidence record. It is
> retained for provenance and is not an authoritative specification for new work.

## Archive context

This record preserves the frozen `compact-diversity-v1` protocol and its completed
evidence, including study and run identities, hashes, recipes, gates, budget, and
reported disposition. Its authority ended when the compact-encoder work was
organized under the structured
[optimization sequence](../../experiments/compact-encoder-campaign/iterations/optimization/README.md).
The date of that transition is not stated in this historical record.

The current experiment owner preserves the protocol lineage in
[execution](../../experiments/compact-encoder-campaign/iterations/optimization/execution.md),
the bounded conclusions in
[results](../../experiments/compact-encoder-campaign/iterations/optimization/results.md),
and the original records and artifact identities in the
[evidence manifest](../../experiments/compact-encoder-campaign/iterations/optimization/evidence/README.md).
Use those pages for current navigation and interpretation; retain the text below
unchanged when resolving old checkpoints, reports, cache identities, or campaign
budget records.

## Preserved historical record

Issues specs#66 / implementation#393. Authorized unmerged stack on #391; no merges.
Fixed33 input, central17 predictions,64-number output. This is a fresh developmental
comparison prompted by report49f6cfd3cab1b0ff1c2542cdc709731c89cd6d798af4d4987fbf0999023e2e6d,
not an amendment of the completed compact-search-v1 experiment.

## Identity, data and cache

Study compact-diversity-v1; run compact-diversity-v1-run1. Full clean source/spec
SHAs and source spatial-encoder hashes frozen before training. Counts: train768,
probe768, selection192, development192, balanced over the same four field families
and fractions.08/.16/.28. IDs compact-diversity-v1-<split>-<index:04d>, SHA256
first8 little-endian bytes seed NumPy. Generate the same underlying49-cubed scalar
fields as compact-search-v1 (random Gaussian sigma1.5 reflect, oblique sine sheets,
two sphere surfaces, two box surfaces), but compute the occupancy quantile from
the central17 scalar field and apply that threshold once to the entire parent.
This deliberately balances target-region density; no real-world-distribution claim.
It changes the data distribution, so include contemporaneous unregularized controls
and do not attribute cross-study improvement solely to regularization.

Hash parents and all input/mask/target arrays; reject duplicates across new splits
and against compact-search-v1 parent hashes. Targets remain parent occupancy,
boundary and positive signed EDT truncated/divided by8, cropped to17. Support:
at least20 positives/negatives per binary task/family/split, nonempty free pools.
Probe/selection/development use one fixed20% independent mask per geometry. Train
uses eight fixed20% masks per geometry, SHA ID plus -mask-<bank-index> seeds. This
is an explicit finite augmentation bank, not fresh unseen masks every update.
Held-out scenes and their masks test transfer beyond the training bank.

Freeze the pretrained spatial seed0 backbone and cache ordered5-cubed and9-cubed
pooled features for every exact training input/mask pair. Extraction batches16;
compare direct and cached values on fixtures. Cache key includes source backbone,
data identity and bank definition; hash the artifact before any fitting, retain
it outside Git. No hidden truth may enter encoder channels. Do not cache a different
mask or claim independent exposure when the same bank entry repeats. Evaluation
features use the exact registered mask and frozen source too. Defer development
feature extraction/metrics until selection lock; freeze its identity only beforehand.

## Six recipes

All recipes: ordered pooling, flatten -> Linear(8*side^3,128) -> SiLU -> Linear(128,64).
Training decoder Linear(64,3*4913). Backbone stays frozen. Recipe IDs:

| ID | Pool side | LR | Schedule | Regularizer multiplier |
| --- | ---: | ---: | --- | ---: |
| 0 | 5 | .003 | constant | 0 |
| 1 | 5 | .0003 | warmup/cosine | 0 |
| 2 | 5 | .0003 | warmup/cosine | .1 |
| 3 | 5 | .0003 | warmup/cosine | 1 |
| 4 | 9 | .0003 | warmup/cosine | .1 |
| 5 | 9 | .0003 | warmup/cosine | 1 |

AdamW weight decay.01, feature batch128, global parameter-gradient clip5. Initialize
aggregation/decoder with seed393 and sample indices with CUDA generator39300 for
every recipe. Uniform draws from the768*8 bank, same draws across recipes. Train
1024 updates, evaluate/save256/512/1024; no early pruning. Warmup scales linearly
over32 updates, then cosine from base LR to.1*base at update1024. Record examples,
unique bank entries, time and memory; larger batch/cache changes are shared by all
recipes. Side9 has more parameters, so this is not a parameter-matched pooling test.

Reconstruction: train-prevalence weighted hidden-cell occupancy and boundary BCE,
plus10*SmoothL1 distance over all free central cells. Regularizer is
lambda*(25*mean(relu(1-sqrt(var(z)+1e-4))) + sum(offdiag(cov(z))^2)/64), with
unbiased batch variance/covariance. This adapts variance/covariance terms from
[VICReg](https://arxiv.org/abs/2105.04906); no invariance term or claim of replicating
that method. Batch128 supports estimation for64 features. Increasing entropy rank
alone is not evidence of retained task information. No hidden-label inputs or skip.

## Readout, selection and evidence

At each checkpoint, discard the training head for ranking. Fit the same independent
float64 ridge alpha1 readout on all768 probe scenes, train-only vector normalization
and bias unpenalized, output clamp[0,1]. Threshold classification by pooled selection
F1 on.01..99, lower ties. Report pooled and family task metrics, probe entropy rank,
fixed-threshold shuffled-vector scores and trained-head diagnostics (its thresholds
selected separately on selection). Report a probe spatial-mean prior once. These
are controls, not proof of superiority over a matched nonlinear raw/spatial model.

Use family macro scores for the four tasks. Fixed developmental targets remain
IoU.60, boundary F1.70, clearance/recovery error.10. Rank by number of macro targets
met, minimum directed target ratio over all task/family cells, mean macro directed
ratio capped2, fewer aggregation parameters, fewer updates, lower recipe ID.
Keep every checkpoint in the ledger. Select one best checkpoint per recipe, then
the top two recipes using selection alone. Lock this choice before development;
evaluate those exact checkpoints once without selecting again. No silent final-
checkpoint replacement. Single-seed development, not certification. Family failures
and dependence on readout capacity remain explicit even if macro targets pass.

## Budget, validity and continuation

At most4 charged hours inside the authorized48-hour campaign; no new approval is
needed within that total. Each recipe has a30-minute cap including its evaluations.
Reserve300 seconds for source/tests/report preparation overhead and charge measured
freeze preparation. Exclusive ledger lock; no overlapping GPU experiment. Cached
features/readout/optimizer/checkpoints remain outside Git with hashes. CPU threads4,
deterministic float32, TF32/cuDNN autotuning off. Numerical failures invalidate the
affected evidence, not permission to change frozen hyperparameters.

Checkpoint each recipe/rung, RNG and optimizer. On interruption, charge the full
1800s uncertain recipe allowance before resuming a saved rung; reuse completed
artifacts after verifying their hashes. Keep an explicit elapsed/inflight progress
record and protect the4h total. Completed runs must not retrain silently.

Before training test regularizer gradients and correlation response, schedule,
mask isolation, cache/direct agreement, density support, ranking, resume/identity
and budget bounds. Verify frozen backbone hashes before/after caching/inference.
If rank improves without task metrics, do not declare success: next test nonlinear
decoding or representation detail. If quality improves, confirm on fresh seeds and
controls before packaging. Continue in-scope evidence-directed work within budget;
never merge/promote or enlarge the field without the corresponding authorization.

## Completed evidence

Implementation#393 / PR394, sourceb09313a, manifest0f042ca, evidenceefb5c5d.
Six recipes and18 stages completed. Report payload
02701cbde1957a598460a86b0a4321f3ff39344a3a468c0f54dd3b943787fbe0.
473 garden tests passed. All21 artifact hashes,18 selection metric/threshold
replays,18 cached-feature-to-prediction CUDA replays and two development assessments
verified. Strict CPU replay differed by up to4.055e-6; tolerance was not relaxed,
and CPU portability at that tolerance is not certified.

Fine pooling/strong penalties raised entropy rank to21.62, but selection boundary
F1 remained.3301. Rank alone did not fix task information. Family-aware selection
chose recipe0/512. Development IoU.24850, boundary F1.33044, clearance.09825,
recovery.09837: classification targets fail. Neither finalist is usable or
promotion-eligible. The density-balanced corpus removes the previous filled-crop
advantage; cross-study pooled numbers are not directly comparable.

Cached1024-update recipes plus evaluations took about9.3-9.7s each; repeated bank
entries are not independent scenes. Ledger charge484.922s includes300s overhead
reserve and freeze preparation. Continue a fresh nonlinear frozen-readout study,
not stronger penalties or field scaling. No integration merges performed.
