---
title: Local-geometry encoder study
status: complete
kind: experiment
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related:
  - ../../legacy/python/perception-encoder-local-geometry.md
  - ../../legacy/python/perception-encoder-local-geometry-lg2.md
  - ../../legacy/python/perception-encoder-local-geometry-lg3.md
---

# Local-geometry encoder study

## Problem statement

The R0 topology study did not establish that its representation retained identifiable
topology. This separate program asked the narrower engineering question of whether a
small frozen encoder retained useful **local** occupancy, boundary, clearance, and
missing-cell recovery information. It then tested whether a joint objective could
preserve the two specialist objectives and whether that result transferred to
independently implemented synthetic generators.

## Research questions and hypotheses

1. **LG1:** do occupancy-only or ESDF-only objectives produce reusable local features
   under an equal small compute budget?
2. **LG2:** does joint occupancy-plus-distance pretraining preserve the useful local
   information found in the specialist objectives within frozen noninferiority margins?
3. **LG3:** do the frozen LG2 joint checkpoints support the same four tasks on fresh,
   independently implemented procedural generators?

LG2 hypothesized that the joint objective would preserve both specialists. LG3
hypothesized that every absolute, family, control, and integrity gate would pass.

## Scope and non-claims

This is synthetic, crop-local, radius-eight frozen-feature evidence. It does not
establish topology, connectivity, planning, navigation, global-embedding quality,
wide-context behavior, architecture superiority, real-world transfer, deployment
readiness, or advancement of the earlier P1-P8 program. LG3's fresh probes are
target-domain fits, not zero-shot transfer; its unchanged LG2 probes are diagnostic.

## Status and summarized outcome

Status: **complete**.

- LG1 completed, but neither specialist qualified under every frozen gate.
- LG2 validated the joint-preservation hypothesis and retained the joint recipe for
  an independent-generator screen, not for deployment.
- LG3 did not confirm broad transfer: distance tasks transferred, while boundary
  and oblique-sheet occupancy gates failed. The bounded final disposition is
  `not_confirmed`.

## Iteration model and historical authority

LG1, LG2, and LG3 are preserved as ordered iterations because the imported documents
present them as a continuation sequence. Each was prospectively registered under its
own immutable identity; the canonical experiment protocol now records their ordered
relationship and frozen differences. Preserved legacy documents remain provenance,
not the canonical navigation surface.

## Documents

- [Protocol](protocol.md)
- [Sources](sources.md)
- [Iterations](iterations/README.md)
