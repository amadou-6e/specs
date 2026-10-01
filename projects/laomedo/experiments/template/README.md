---
title: Snapshot-rejection experiment example
status: template
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Snapshot-rejection experiment example

Illustrative unexecuted question: does holding a synthetic post-run snapshot make resume
fail before native dispatch and reservation? Tests execution semantics, not answer quality.
Use deterministic fixture checks first; real model-backed turns need separate authorization.

| Element | Cardinality |
| --- | --- |
| README.md, protocol.md, sources.md, iterations/README.md | 1 each |
| iterations/<attempt>/ | 0..* |
| attempt overview, execution.md, results.md, evidence/manifest.md | 1 each |
| replication.md | 0..1 when actually repeated |

Copy directly, rename, replace all example facts/lifecycle/links. Keep initial attempt as
an honest draft plan or remove until execution; never register its results as observed.
Read [protocol](protocol.md), [sources](sources.md), [attempt](iterations/initial/README.md).
