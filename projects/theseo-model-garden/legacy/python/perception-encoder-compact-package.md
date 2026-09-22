---
title: Experimental fine729 package
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
  - ../../subsystems/model-registry/README.md
---

# Experimental fine729 package

> This entry is historical and is not an authoritative specification. The original
> package contract and executed-evidence text below is preserved as identity-bearing
> evidence.

## Archived material

This record preserves the frozen `compact-package-v1-run1` package interface,
manifest and verification requirements, resource accounting, source and spec
identities, and executed packaging outcome. It describes an experimental local
artifact produced from the replicated fine729 encoder; it is not a current package
format or promotion contract.

## Why it was archived

The package work now belongs to the structured
[compact perception-encoder campaign](../../experiments/compact-encoder-campaign/README.md),
where packaging is interpreted as implementation equivalence within the
[qualification sequence](../../experiments/compact-encoder-campaign/iterations/qualification/README.md).
The active [model-registry subsystem](../../subsystems/model-registry/README.md) owns
the current publication and discovery boundary. This record remains in place because
its hashes, frozen identities, issue and PR references, runtime path, and exact
interface wording participate in historical provenance.

## Authority ended

This standalone package record ceased to be the current navigational specification
when the compact encoder work was migrated into the structured campaign. The exact
migration commit and date are not established here. Its explicit original
non-promotion status remains in force: new work must not treat this historical
package as a certified or generally supported model artifact.

## Current replacement

Use the campaign [protocol map](../../experiments/compact-encoder-campaign/protocol.md)
and [qualification
iteration](../../experiments/compact-encoder-campaign/iterations/qualification/README.md)
to interpret the experiment and its package-equivalence result. Use the
[model-registry subsystem](../../subsystems/model-registry/README.md) for current
artifact publication and loading behavior. Any new qualification or promotion claim
requires a newly frozen protocol and must not be inferred from this archive.

## Continuing evidential value

The record remains necessary to interpret `compact-package-v1-run1`, its manifest
and verification-report hashes, the three seed artifacts, compatibility limits,
equivalence replay, GPU measurements, and budget accounting. The historical content
below is retained without normalizing its paths, identifiers, numeric values, or
claims to current repository conventions.

## Original historical record

# Experimental fine729 package

Specs #76 / implementation #403. Authorized unmerged successor to replication
#401, source b3a28146fa2c2c8f890e9b0b9b531196032cb8a8, spec
b77b6a20ffc7e88930b4e4110133a649afdb95c7, verified report
f7d65863a81c3c905d24649d78a4d2d55ce747ccc0c89d361feb796d4bfc7c10.
All three seeds passed the directional packaging assessment. No new training,
model selection, threshold calibration or scientific quality claim occurs here.

## Interface

Expose a frozen encoder taking binary occupancy (B,33,33,33) and a boolean
unknown mask of the same shape (or B,1,33,33,33). All cells are valid, stride1;
other geometry/validity regimes are unsupported. Mask semantic occupancy/free
channels using VoxelLevel.from_occupancy before the fixed backbone. Never expose
the unused backbone projection or raw feature volume to the caller's head.

Output is a detached float32 tensor (B,729), normalized by the frozen probe-only
float64 population statistics. Layout is channel-major1x9x9x9, centers8..24
at stride2 in the input. It is a spatial code, not a generic global embedding.
Backbone and aggregation remain eval/frozen even if the parent calls train().
Use no_grad, not inference_mode, so a separately trainable head can consume it.

Provide the separately loaded native head; it accepts only code and integer
central17 flattened query indices and produces three raw-logit/value channels:
hidden occupancy, boundary, and normalized clearance/recovery distance. Query
indices use the existing tensor flatten order. Apply sigmoid to binary channels
and clamp distance to[0,1] for evaluation; return raw values for head training.
Default seed401 is the lowest numeric ID, not a development-selected winner.
Export all401/402/403. No fine-tuning the encoder or transferring arbitrary-head
quality is claimed.

## Artifact and verification contract

Versioned manifest pins this full spec SHA, source commit, replication report
hash, input/output layout, normalization, all three seed/checkpoint/state hashes,
calibrated thresholds, and experimental/non-promotion status. Atomic local weight
files plus SHA256 hashes; loader checks manifest digest, safe basenames, format,
fixed contract, file hashes and restored module state hashes before returning.
Statistics must be finite,729-long, shared across positions and scale>=1e-5.
Weights/corpora remain runtime-only; commit compact manifest/verification report.

Export is conditional on the verified replication report hash and recomputed
packaging-readiness assessment. Recheck source report/artifact/backbone hashes.
Replay direct occupancy/mask inputs for the first32 and last32 development rows
for every seed, at rtol1e-5/atol1e-6 against saved independent-head predictions.
This is implementation equivalence, not a new holdout claim. Test forward sizes,
invalid inputs, manifest/weight tampering, state round trip and mask isolation.
On disposable copies, take a head-only optimizer step and require finite nonzero
head gradients, changed head state, unchanged encoder state and no encoder grads.
Do not save the modified head. Report CUDA peak memory and warm median/p95
encoder latency at batch1 (ten warmups,50 timed repetitions, synchronized).

Use deterministic float32 CUDA without TF32/autotuning. No new corpus beyond
regenerating the known development rows for equivalence. Freeze package identity
`compact-package-v1-run1` and governing/source SHAs before validation. Reserve
1800 seconds inside the existing48 GPU-hour ledger, including300s test overhead.
No overlapping GPU run; charge actual successful elapsed time plus reserve, or
the full tranche on failure. No failed-run overwrite or uncharged resume.

Success delivers a directly loadable experimental local-geometry artifact and
usage example with the explicit limits. It does not promote to develop, merge
PRs, establish planning/topology transfer, or certify out-of-distribution quality.

## Executed evidence

Frozen spec1eedc6ca419b4f62f9bb320d1e983d65cb8999ca; source
65e6f8f3480d3caca5046d5b03391f14cf343dd7; issue403 / PR404.
All three seed artifacts exported and verified:64 direct-input development rows
per seed reproduce native-head predictions at unchanged tolerances; each
disposable head-only optimizer step changes the head without encoder gradients
or state changes. 537 garden tests pass. Manifest payload:
`2ddf188ecedff4699dba434fec05a851c5649119c07dcf30c9d9afd1292d4ed1`.
Verification report:
`786c803a8c648b283c5136d6332c95ba7a88b7a6179a51847fa4850ede8bf8d1`.

Observed RTX3060Ti warm batch1 encoder latency13.98ms median/14.77ms p95;
peak CUDA allocation54,901,248 bytes. Accounted331.453s includes300s overhead,
within1800s tranche. Runtime artifact directory `runtime/compact-package-v1-run1`;
usage and limits in `docs/perception-compact-package.md`. No weights committed,
no merge/promotion. The bounded experimental frozen-encoder/native-head package
is available; broader transfer and certification remain outside this result.
