---
title: Fixed-architecture encoder continuation protocol
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/encoder-continuation-and-context/README.md
  - ../../experiments/encoder-continuation-and-context/iterations/004-encoder-continuation/README.md
  - perception-encoder-continuation-evidence.md
---

> This entry is a historical, identity-bearing protocol and is not an
> authoritative specification for new Model Garden experiments.

## Archive context

### Archived material

This record preserves the frozen protocol for the fixed-architecture encoder
continuation study, including its registered comparisons, training bounds,
identities, streams, assessment rule, and decision gate. Those details remain in
their original form below so historical reports and artifacts can still be
interpreted against the protocol that governed them.

### Why it was archived

The protocol has been incorporated into the structured
[encoder continuation and context experiment](../../experiments/encoder-continuation-and-context/README.md).
The structured experiment now owns the active experiment organization; this file
remains the provenance source and must not be rewritten as current guidance.

### Authority ended

Authority ended when the continuation work was migrated into the structured
experiment entry. The original text identifies specs#41, theseo-anysearch#366,
and its frozen specification commits; no more precise migration date is asserted
by the available record.

### Current replacement

The canonical owner is iteration
[004 — Fixed-architecture encoder continuation](../../experiments/encoder-continuation-and-context/iterations/004-encoder-continuation/README.md).
Its execution, results, and evidence pages provide the current structured view of
this completed iteration.

### Continuing evidential value

Retain this record to interpret the `voxel-encoder-continuation-v1` study and
`voxel-encoder-continuation-v1-development-1` dataset, reproduce the registered
comparison bounds, and verify historical stream, checkpoint, timeout, and
bootstrap identities. The related
[continuation evidence](perception-encoder-continuation-evidence.md) records the
reported outcome.

## Preserved historical protocol

# Fixed-architecture encoder continuation

Issues specs#41 / theseo-anysearch#366. User authorizes continued execution and
stacking on unmerged exp/364; no integration merges. Separate experiment from
reference refinement at specs commit 44b089b58db3b9af45820cb358033c6a4acbc99f.
Do not alter previous verdicts or reopen the topology program.

## Comparisons

Three seeds, same fresh probe selection/assessment sets for all arms:

- Existing LG2 encoder, probe fit on 48 geometries.
- Same existing encoder, probe fit on 192 geometries at the same update budget.
- Newly pretrained encoder of the exact same architecture, probe fit on 192.
- Strong supervised reference using the previously selected dynamic/192/lr0.003
  recipe, checkpoint selection as in reference refinement.

New encoders start from fresh seed initializations, not LG2 checkpoints. Pretrain
on 192 separate geometries for 2048 updates, batch eight, AdamW lr0.003/wd0.01.
Use fresh label-independent Bernoulli(0.20) masks each update. Objective is the
existing LG2 joint loss: hidden occupancy BCE plus 10 times SmoothL1 on normalized
ESDF (truncation eight, divide by eight). Attach a two-channel 1x1x1 training head
to eight local feature channels. Global projection remains untrained/out of scope.
Freeze final encoder weights after pretraining; no boundary-assessment selection
of encoder checkpoints. Probe heads alone train afterward.

Keep the linear/32/128 probe ladder and 1024 updates per capacity, AdamW
lr0.001/wd0.01, batch1024. Train-only normalization. Choose capacity by selection
log loss, then calibrate F1 threshold using selection only as in prior protocols.
The new-192 versus old-192 comparison has matched probe exposure. It evaluates a
pretraining bundle, not an isolated effect of learning rate or dataset composition.

## Identities and bounds

Study `voxel-encoder-continuation-v1`; dataset
`voxel-encoder-continuation-v1-development-1`. Pretrain192 /probe-train192 /
selection48 /assessment48 geometries, same four procedural families and density
strata. All splits disjoint by content hash; reject overlap with the prior reference
refinement campaign. CPU mask/query streams 36600/36601/36602/36603; encoder
training random stream 36610+seed. Fixed observation/query support rules unchanged.

Freeze source/spec commits, corpus/query/target hashes, prior-registration hash,
old encoder file/state hashes and resolved configuration before fitting. Verify
loaded and post-probe encoder states. Save new checkpoints untracked with report
hashes. D0 reruns. Maximum900 seconds per reference, encoder or probe-ladder fit;
overall7200 seconds including preparation, no automatic retries or expansions.
Validity failures stop affected evidence; timeout retains inconclusive results.

## Assessment

Paired per-geometry boundary log loss, averaged across all three seeds; 2000
cluster-bootstrap draws within family/density strata, seed362. Report old192 versus
old48 gain, new192 versus old192 gain, and new192 versus reference gain, positive
favoring the first named model. If the new versus old192 lower95% bound exceeds
zero, proceed toward distance-retention and new-family validation. Otherwise retain
the old encoder and investigate objective/readout limitations. Exposure results
inform interpretation but never permit changing completed thresholds.

Report F1 and per-family scores as diagnostics. This surface-only experiment does
not validate distance retention, general encoder quality, unseen-family transfer,
topology, planning or radius scaling. No promotion follows from any outcome.
