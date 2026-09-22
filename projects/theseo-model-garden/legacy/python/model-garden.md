---
title: Imported Model Garden monolithic specification
status: superseded
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../architecture/model-garden-monolith.md
  - ../../architecture/README.md
  - ../../subsystems/README.md
  - ../../experiments/README.md
  - ../../research/README.md
---

# Imported Model Garden monolithic specification

> This entry is historical and is not an authoritative specification.

## Archived material

This record identifies the former monolithic Model Garden specification at
`projects/theseo-anysearch/python/model-garden.md`. That source combined proposed
dataset collection, encoder training, artifact storage, command-line workflows,
Anysearch integration, and implementation sequencing in one document.

The imported source first appeared in commit
`0bfcdd1f0233320338351252680a7e69f1726241` and was subsequently revised through
commit `dfc52232373415b61f7dc060d2ef57f320f2d47d`. These identifiers and the original
path are retained verbatim because they participate in the provenance of historical
protocols and experiment records.

The preserved document body is available as
[Model Garden monolithic design record](../../architecture/model-garden-monolith.md).
That record keeps the proposal intact while clearly separating it from current
architecture authority.

## Why it was archived

Model Garden became a peer project rather than a Python topic owned by Theseo
Anysearch. Its former monolithic document also mixed architecture, subsystem
contracts, experiments, research claims, and implementation plans that now have
separate canonical owners.

## Authority ended

By the 2026-09-22 specification restructure, new work was required to use the
Model Garden project taxonomy and its canonical owners instead of the imported
Anysearch Python document. The historical commits remain valid evidence of what was
proposed at the time; they do not establish current behavior.

## Current replacement

- The [architecture map](../../architecture/README.md) defines current system
  boundaries and links to the preserved monolithic design record.
- [Subsystem specifications](../../subsystems/README.md) own current contracts and
  implementation designs for datasets, encoder models, qualification, and registry
  behavior.
- [Experiments](../../experiments/README.md) own protocols, iterations, executions,
  and empirical results.
- [Research](../../research/README.md) owns source characterization and findings that
  are not normative runtime contracts.

## Continuing evidential value

Keep this record when interpreting old links, checkpoints, reports, configuration
examples, and experiment evidence that name the former
`projects/theseo-anysearch/python/model-garden.md` path or rely on its proposal. Any
schema, command, path, performance estimate, or implementation sequence in the
preserved document must be checked against the current canonical owner before use.
