---
title: Compact classification controls diagnostic
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/compact-encoder-campaign/protocol.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md
  - perception-encoder-compact-controls-evidence.md
---

> This entry is historical and is not an authoritative specification. The original
> diagnostic design is preserved below without normalizing its identity-bearing
> revisions, hashes, run names, limits, or claims.

## Archived material

This record froze the `compact-controls-v1` classification-control diagnostic for
the compact smoke checkpoints. It specified the development-only data, frozen
representations and controls, probe recipes, threshold selection, metrics, execution
budget, and bounded interpretation rules for `compact-controls-v1-run1`.

## Why it was archived

The diagnostic became one source in the structured compact perception-encoder
campaign. The campaign now owns navigation, chronology, and current interpretation
across the sequential engineering screens; this file remains provenance for the
original control design and exact frozen identities.

## Authority ended

By the 2026-09-22 structured migration, current interpretation moved to the
`compact-encoder-campaign` experiment. This archived protocol does not authorize a
rerun, HPO selection, encoder update, promotion, or continuation beyond its original
bounded diagnostic.

## Current replacement

- [Compact encoder campaign](../../experiments/compact-encoder-campaign/README.md)
- [Campaign protocol map](../../experiments/compact-encoder-campaign/protocol.md)
- [Engineering-screen iteration](../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md)
- [Engineering-screen execution](../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md)
- [Engineering-screen results](../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md)

## Continuing evidential value

Keep this record to interpret reports, manifests, probes, and predictions that cite
specs issue 56, Theseo AnySearch issue 381, parent campaign plan
`4df18c69ee81c2c2ebd383b7eab615ae7583a6b3`, governing smoke specification
`04673aba3906a50c9a51e4631ef910f8a3e767e7`, study `compact-controls-v1`, or run
`compact-controls-v1-run1`. The recorded run outcome remains in
[the compact-controls evidence](perception-encoder-compact-controls-evidence.md).

---

## Preserved historical diagnostic design

# Compact classification controls diagnostic

Status: frozen diagnostic design, not HPO or certification
Issues specs#56 / theseo-anysearch#381. Authorized unmerged stack on #379.
Parent campaign plan4df18c69ee81c2c2ebd383b7eab615ae7583a6b3;
smoke evidence source7e31294, governing smoke spec04673aba3906a50c9a51e4631ef910f8a3e767e7.

## Question and identities

Did short probes, class imbalance or fixed thresholds hide useful classification
signal in the compact smoke checkpoints? Compare controls without training any
encoder. This cannot establish the best compact architecture or replace the full
C0-C4 foundations. No final assessment set, distance recipe, HPO selection, budget
expansion, topology, navigation, promotion or integration merge is authorized.

Study/run compact-controls-v1 / compact-controls-v1-run1. New development-only
probe48 / selection24 / development48 parents, IDs
compact-controls-v1-<split>-<index:03d>. Same49 parent/33 input/central17 query
geometry and target rules as compact smoke v2; SHA seed per parent, independent20%
mask, random-field/oblique-sheet families and .08/.16/.28 density fractions. Fixed
256 queries/task/parent, query RNG38100+split index, replacement only for nonempty
undersized pools. Parent targets truncation8; binary tasks only scored here.
All queried binary cells are hidden. Reject duplicate parents and fewer than20
positive or negative labels in any family/split pool. Freeze and verify hashes;
new parents must not overlap source smoke or preceding context datasets.

## Frozen representations and controls

Six128-dimensional compact smoke v2 checkpoints (grid/strided/attention times
frozen/joint), each with fresh fixed probes. Additional controls:

- Random backbone+grid aggregation128, initialization seed381, no training.
- Validated pretrained spatial encoder seed0: per-query8 spatial features.
- Raw3-cubed neighborhood:27 visible-occupancy flags and27 hidden flags.
  Unknown occupancy is zeroed before neighborhood extraction; no ground truth
  completion enters features. This is a local raw-input control, not full-grid.
- Coordinates only. Every other representation also receives the same three
  coordinates normalized[-1,1]. No other query-conditioned compact inputs.

Encoder files/state hashes verified, all encoder parameters frozen throughout.
Cache extracted features once for each representation/split for probe comparisons.
The controls differ in input dimension and parameter count:131/11/57/3 features
for compact/spatial/raw/coordinates. All heads have32 hidden units, SiLU and one
logit. Report actual parameter counts, not a capacity-matching claim. Random grid
is a single control, not an architecture-matched control for every aggregation.

## Probe and calibration comparison

For each representation and binary task, run plain128, plain1024 and balanced1024
update recipes. AdamW lr.001/wd.01, batch1024 sampled queries, initialization seed
41000 and sample RNG42000, train-only standardization floor1e-5. Balanced uses
positive BCE weight = training negatives/positives; no evaluation reweighting.
All fits restart from initialization; save losses at128/512/1024 where applicable.
Record training and held-out-development metrics to expose probe overfitting.

Pick operating threshold on selection F1 over .01..99, ties lowest, unchanged
across families. Use F1 for threshold selection for both tasks as in prior helper.
Report fixed.5 and selected-threshold scores (occupied IoU / boundary F1), AUPRC
(stepwise average precision), AUROC, log loss in nats, Brier score, prevalence,
positive prediction rates and probability quantiles. Report family breakdowns.
Weighted BCE outputs need not be calibrated probabilities; log loss and Brier
expose that limitation. No temperature fitting or development-threshold selection.

60 independent probe fits total:10 representations x2 tasks x3 recipes. Preserve
probe states, train normalization and train/selection/development predictions for
replay, but not in Git. Hash artifacts; commit compact reports and manifests.

## Execution and interpretation

One CUDA process, CPU threads4, deterministic float32, TF32/cuDNN autotuning off.
Overall30-minute cap including registration preparation; checks per feature batch
and optimizer update. Measure feature extraction and fit/evaluation wall time.
No concurrency or isolated throughput claim. Freeze source/spec/data/checkpoint
identities before fitting. This small diagnostic does not spend the proposed
48 GPU-hour search budget.

If ranking is useful but fixed.5 scores fail, route to threshold/probability
calibration. If longer fits improve training only, investigate overfitting. If
spatial/raw controls substantially outperform compact representations after probe
adjustments, investigate compact training or compression rather than more context.
If coordinate/random controls match compact features, do not claim pretraining
benefit. These are descriptive development comparisons without multi-seed or
confidence-interval certification. Do not select an HPO winner from this run.
