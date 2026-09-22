---
title: Perception encoder R0 topology-identifiability audit
status: complete
kind: experiment
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related:
  - ../../legacy/python/perception-encoder-r0-execution.md
  - ../../legacy/python/perception-encoder-r0-result.md
---

# Perception encoder R0 topology-identifiability audit

## Problem statement

Before comparing perception encoders, the program needed to establish that completed
connectivity was identifiable from visible voxel context under its registered
empirical completion model. Without that evidence, a downstream score could reflect
an ill-posed target rather than encoder quality.

## Research question and hypothesis

Could a visible-context predictor improve on a frozen geometric-summary prior while
satisfying conditional-entropy, forbidden-feature, and spatial-transfer bounds in
every supported optimistic-path stratum? The operational hypothesis was that all four
gates would pass and authorize P0C.

## Scope and non-claims

This was a topology-identifiability audit, not encoder training or architecture
ranking. It cannot establish a native-world posterior, universal topology
learnability, input leakage, or the quality of any encoder.

## Status and summarized outcome

Status: **complete**. The registered outcome was **defer**, with stop reason
`no_topology_identifiable`. Two transfer strata lacked negative-label support, and
the supported `6+` stratum failed all four conservative gates. P0C, P0D, and P1 did
not start. No architecture was ranked or rejected.

## Documents

- [Frozen protocol](protocol.md)
- [Consolidated sources](sources.md)
- [Iterations](iterations/README.md)
