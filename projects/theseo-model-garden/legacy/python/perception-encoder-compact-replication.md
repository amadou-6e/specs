---
title: Fine729 compact encoder replication
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/compact-encoder-campaign/protocol.md
  - ../../experiments/compact-encoder-campaign/iterations/qualification/README.md
---

# Fine729 compact encoder replication

> This entry is historical and is not an authoritative specification. The original
> protocol and executed-evidence text below is preserved as identity-bearing evidence.

## Archived material

This record preserves the frozen `compact-replication-v1` protocol, its run identity,
recipe, gates, budget, and executed outcome. It was the authorized replication
successor to the compact structured-code study identified in the original text.

## Why it was archived

The replication now belongs to the structured
[compact perception-encoder campaign](../../experiments/compact-encoder-campaign/README.md),
where it is interpreted as part of the qualification sequence. This file remains in
place because its hashes, study and run identifiers, issue and PR references, and
original wording participate in historical provenance.

## Authority ended

This standalone record ceased to be the current navigational specification when the
compact encoder work was migrated into the structured campaign. The exact migration
commit and date are not established in this record; new work must not treat the
historical protocol below as current authorization.

## Current replacement

Use the campaign [protocol map](../../experiments/compact-encoder-campaign/protocol.md)
for protocol lineage and the [qualification
iteration](../../experiments/compact-encoder-campaign/iterations/qualification/README.md)
for the replication's current experimental context. Those records own current
interpretation; any new experiment requires a newly frozen protocol.

## Continuing evidential value

The record remains necessary to interpret the original compact-replication artifacts,
thresholds, reports, validation claims, and the identities embedded in later campaign
evidence. The historical content below is retained without normalizing its paths,
identifiers, commands, or claims to current repository conventions.

## Original historical record

Specs #74 / implementation #401. Authorized stacked successor to #399, not a
merge or promotion. Predecessor protocol `02ab2379655e8a76ae4a6a6f3dc4ff483a74145a`;
report `f4c46fe17c0c767e7e43e374ee940f70d83d760f472c18c1fd84a5ee02711b94`.
Preserve the selection winner ID8, not the development-passing runner-up.

## Fixed recipe and fresh identities

Study `compact-replication-v1`; run `compact-replication-v1-run1`. Freeze full
source/spec commits and array/initializer hashes before any fits. Input33,
central17 geometry targets, pretrained seed0 backbone fixed throughout. Retain
the fine9-cubed single-channel structured aggregation and native readout from
#399, flattened to729 numbers; no raw/local feature bypass into candidate heads.
Do not claim a generic semantic embedding or compatibility with arbitrary heads.

Fresh shared corpus: train6144 parents with two masks, probe1536 with four masks,
selection384 with one mask, development384 with one mask. Same central-density
four-family generator, parent49, 20% masks, fractions .08/.16/.28, truncation8.
IDs `compact-replication-v1-<split>-<index:04d>`; SHA-derived geometry/mask seeds.
Reject parent reuse across all new splits and against #389/#393/#395/#397/#399.
Verify support and full array hashes. Cache fixed float32 backbone features with
the existing hash, memory-map, disk-headroom and resume safeguards.

Three aggregation initialization seeds401/402/403; sampling seeds40100/40200/40300
respectively, reset at each fit. Directly instantiate StructuredModel after seed
initialization; do not use #399's factory that resets the seed to399. Independent
native heads use initialization seed+10000; the fitted null uses the identical
head initialization seed and sampling budget. Spatial reference uses seed+20000.
All three share the fresh corpus and the fixed backbone: this measures optimizer/
aggregation/head variability conditional on that corpus and backbone, not three
independent datasets or backbone replications.

## Training and assessment

Each seed: train aggregation/native decoder8192 updates, freeze aggregation,
extract vectors, fit independent native head8192 on probe only. LR .0003 for
aggregation training; .001 for independent, spatial and null heads. Preserve
batch64,256 uniform queries, AdamW weight decay .01, clip5,64-step warmup then
cosine to .1 of base LR, weighted hidden occupancy/boundary BCE and distance
10*SmoothL1. No mid-run edits, extra updates or early stopping. All fits8192;
checkpoint optimizer/RNG every1024. Twelve fits total: three each of training,
native probe, spatial reference and fitted null.

Per-channel probe-only normalization is unchanged (float64 population mean/std,
floor1e-5; float32 normalized vectors). Fit normalized-zero-code native controls.
Also evaluate candidate codes shuffled (permutation seed+30000) and zeroed with
the fixed fitted head and original thresholds. Persist predictions and hashes.

No candidate selection occurs in this study. All three seeds are frozen finalists
before execution. Binary thresholds use the unchanged pooled selection F1 search
.01..99, lower ties, separately per seed/control. Lock all calibrated thresholds
and all three seed IDs before development prediction access. Development uses
the frozen thresholds, never reselects a seed or learning rate. Store native,
shuffled, zeroed, spatial and fitted-null development predictions for each seed.
Common-head failure from #399 remains a declared limitation, not a rerun target.

Readiness assessment is conservative and directional: each of the three native
heads must meet IoU >= .60, boundary F1 >= .70, clearance/recovery NMAE <= .10
for every family on development. Additionally require per-family native F1 to
exceed both the shuffled and fitted-null F1 by at least .10 for every seed.
Report all values, per-seed failures, across-seed minima/maxima, and paired
spatial differences; do not average away failures. A reference miss is reported,
not used to lower the candidate target or to abort otherwise valid fits.

Passing means an experimental compact interface is ready for packaging checks,
not scientific certification, promotion or planning readiness. Three seeds on
one fresh corpus do not establish broad statistical confidence. If a valid run
misses, preserve its outcome and direct a new bounded refinement from the failing
family/task; do not tune or reinterpret this development set as selection.

## Budget and validity

Four-hour tranche inside the existing48 GPU-hour authorization, not additional
budget. Per-fit cap3600s; preparation cap5400s;900s overhead reserve. Charge
timed freeze preparation and conservative uncertain-phase resume caps. Exclusive
campaign ledger lock; no overlapping GPU trials. Deterministic float32 CUDA,
TF32/autotuning off, CPU threads4, unchanged batch admission from #399.

Validate seed isolation, unchanged recipe/schedule, normalization, frozen source,
fresh identities, threshold lock, per-seed/family assessment and budget/resume.
After execution replay hashed artifacts and original-device predictions at
rtol1e-5/atol1e-6, including cached backbone batches. Commit compact report and
assessment to implementation PR and evidence to this specs repository; no weights,
corpora or caches. No merges without review/explicit merge authorization.

## Executed evidence

Frozen spec `b77b6a20ffc7e88930b4e4110133a649afdb95c7`, source
`b3a28146fa2c2c8f890e9b0b9b531196032cb8a8`; issue401 / PR402.
Report `f7d65863a81c3c905d24649d78a4d2d55ce747ccc0c89d361feb796d4bfc7c10`:
all12 fits completed,109 hashed artifacts,6,876.375 accounted seconds.
All three fresh seeds pass every development family point target and both
per-family embedding-necessity comparisons. Experimental packaging readiness
is true; promotion remains false. Native development IoU .76333/.76398/.77122,
F1 .79149/.79435/.79458 for seeds401/402/403. Worst family/seed IoU .631216,
F1 .705934; maximum errors .059629/.059573. No seed was selected on development.

Proceed to a separately scoped frozen-interface export and round-trip validation.
Keep the native spatial-readout limitation, fixed-backbone/shared-corpus limits,
and narrow worst F1 margin explicit. This does not establish arbitrary-head,
topology, navigation, larger-field or broad statistical certification claims.
Assessment and diagram: `docs/perception-compact-replication-assessment.md`.
Validation:526 garden tests pass; original-CUDA replay verified109 artifacts,
three seed pipelines,30 predictions and eight backbone batches at unchanged
rtol1e-5/atol1e-6. Specs validator:zero errors, existing Draw.io warning only.
