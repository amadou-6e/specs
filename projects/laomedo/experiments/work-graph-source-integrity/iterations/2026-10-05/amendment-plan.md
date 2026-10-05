---
title: EXP-01 filtering amendment plan
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Filtering amendment before rerun

The first eight-case run compared filtered item and edge membership but did not compare each projected item's readiness. Its hidden prerequisite was closed, so it could not distinguish full-graph readiness from a faulty projection-local calculation. This is an evidence gap against the existing [protocol](../../protocol.md) and [Work Graph contract](../../../../subsystems/work-graph/contract/work-graph.md), not an observed implementation failure.

The amended [corpus and oracle](https://github.com/amadou-6e/laomedo/tree/de32cc8/experiments/exp01) were committed at `de32cc8` before rerun. The new `hidden_open_blocker` case has an open, unlabeled prerequisite and an open, `focus`-labeled dependent. The full graph must classify the dependent `blocked`; filtering to open `focus` items must retain the dependent as `blocked` and carry the hidden prerequisite in `context_dependencies`. The probe now compares per-item projected readiness for this case and the earlier closed-blocker case. A projected `ready` result is a no-go even if edge membership matches.

Run the amended nine-case corpus against a fresh installed wheel from the frozen source revision in a disposable environment outside Git. Retain the original eight-case result unchanged. Publish the rerun as a separate artifact with a source revision, local wheel hash, corpus/oracle hashes, case matrix and limits. The wheel hash identifies only the local artifact; source revision and input commits are the reproducible pins because separate wheel builds may differ byte-for-byte. The corpus was prepared by the same author as the implementation, independently of its development fixtures, not by an independent second party.
