---
title: RL training diversity study
status: planned
kind: experiment
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
related:
  - imported-protocol.md
---

# RL training diversity study

## Problem statement

Determine how geometry, route, task, and sampling diversity should be controlled and
measured in RL training without leaking evaluation families or confusing new seeds
with genuinely new environments.

The surviving design proposes geometry-pool sampling, scale variation, and
training-time obstacle augmentation as mechanisms for reducing memorization of one
fixed map. The repository now implements those mechanisms to different degrees and
with different single- and multi-agent validation boundaries, but implementation is
not evidence that the proposed comparative study ran.

## Research questions and hypotheses

The imported design motivates, but does not formally preregister, these questions:

1. Does sampling distinct geometry identities improve held-out routing performance
   relative to training on one fixed geometry?
2. Does scale variation improve transfer across voxel resolutions without changing
   the observation-space contract?
3. Does reset-time obstacle augmentation improve robustness to novel obstruction
   layouts without causing unacceptable task infeasibility?
4. Can those effects be attributed separately rather than only to their combined
   configuration?

The imported material does not state falsifiable hypotheses, controls, effect-size
thresholds, or statistical acceptance rules. Those remain protocol gaps.

## Scope and non-claims

The intended scope is RL navigation under varied geometry, scale, and obstacle
conditions. It does not establish that any one mechanism improves generalization,
that the mechanisms preserve task difficulty, or that the example PPO configuration
is preferred. It also does not cover encoder-pretraining studies, which belong to the
peer Theseo Model Garden project.

## Status and summarized outcome

Status: `planned`.

The historical document is preserved as an imported design source. No frozen
protocol, registered iteration, execution manifest, evidence manifest, result, or
replication is present, so this entry has no scientific outcome. Repository inspection
confirms that several proposed mechanisms were later implemented; that is engineering
traceability only and must not be reported as an experiment result.

## Documents

- [Protocol](protocol.md)
- [Sources](sources.md)
- [Unmodified imported design](imported-protocol.md)

`iterations/` is intentionally absent. Create it only when an attempt is actually
authorized and begins under a pinned protocol.
