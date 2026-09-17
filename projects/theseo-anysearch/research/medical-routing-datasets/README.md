---
title: Medical geometry and centerline datasets
status: draft
kind: research
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
supersedes: null
related:
  - ../../dataset_research.md
---

# Medical geometry and centerline datasets

## Question and relevance

Which public datasets pair or can derive 3D surface geometry and path-like centerlines
for routing research, and what evidential or access limits apply?

## Status

This is an initial structural migration from `dataset_research.md`. The original
German-language survey remains the historical synthesis until all findings and source
details receive substantive review.

## Evaluation criteria

Sources are compared by surface format, centerline/path availability, coordinate
evidence, modality, size, access, rights, and whether a route is supplied or must be
derived.

## Synthesized findings

- [F-001 — Centerline presence does not always establish coordinate semantics](findings/F-001-coordinate-semantics.md)

## Existing synthesis

- [Public datasets for 3D routing with STL scenes and paths](../../dataset_research.md)

## Recommendation and open questions

Treat centerlines as reference paths only when their coordinate relationship to the
surface is verified. Derived centerlines and format conversions require new identities
and independent geometry checks.

## Sources

See the [source registry](sources/README.md).
