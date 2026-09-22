---
title: Checkpoint diagnostic evidence
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/encoder-continuation-and-context/iterations/002-checkpoint-selection/README.md
  - perception-encoder-checkpoint-diagnostic.md
---

# Checkpoint diagnostic evidence

> This entry is historical evidence and is not an authoritative experiment
> specification. The structured experiment iteration is the current owner.

## Archived material

Issues specs#37 / theseo-anysearch#362. Protocol frozen at
`df765d0d4eed2f74a1d6e85f358e435e126d4b08`, executable `d7b8e7a`.

Completed all three trajectories and the frozen probe ladder. Every seed selected
update 256 from the same 2048-update trajectory. Recorded elapsed time 71.39s.
Zero encoder updates. No promotion or changes to previous verdicts.

Selected reference F1: 0.3829/0.3990/0.4017; final: 0.3676/0.3736/0.3865;
frozen probe: 0.6006/0.5847/0.5699. Selected loss improves over final by 0.2529
(paired 95% CI [0.2339,0.2725]), but exceeds probe loss by 0.1495
(paired improvement interval [-0.1639,-0.1353]).

Outcome `reference_improves_below_probe`: refine the reference before attributing
encoder failure. Earlier checkpoints and regularization/data coverage are possible
new interventions, not tested conclusions or adopted protocol modifications.

Implementation report: `docs/perception-encoder-checkpoint-assessment.md` on exp/362.
Machine-readable payload SHA256:
`72f39596cef5d24bf12ab2469c9950c1e7bab6411ea93436e97be58f9cee7f42`.
Only compact evidence is committed; model/prediction artifacts remain untracked.

## Why it was archived

This compact evidence record was imported from the former Python-oriented
perception-encoder documentation. Its results are now organized as iteration
`002-checkpoint-selection` of the structured encoder-continuation experiment, so
this imported path no longer owns the active experiment narrative.

## Authority ended

The exact historical date on which this standalone record ceased to be
authoritative is not recorded. New work must use the structured experiment entry
rather than infer a current protocol from this archived evidence.

## Current replacement

- [Checkpoint-selection iteration](../../experiments/encoder-continuation-and-context/iterations/002-checkpoint-selection/README.md)
- [Evidence manifest](../../experiments/encoder-continuation-and-context/iterations/002-checkpoint-selection/evidence/README.md)

The identity-bearing frozen protocol remains archived at
[perception-encoder-checkpoint-diagnostic.md](perception-encoder-checkpoint-diagnostic.md)
and is referenced by the current evidence manifest.

## Continuing evidential value

This record preserves the original issue references, frozen specification and
executable revisions, measured outcomes, historical implementation-report path,
and payload digest. Those identities are needed to interpret the checkpoint
selection result and verify that later summaries refer to the same evidence.
