---
title: Work Graph source integrity sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [EXP-01 #50](https://github.com/amadou-6e/laomedo/issues/50) defines the independent verification question and zero-model/no-write scope.
- [Work Graph contract](../../subsystems/work-graph/contract/work-graph.md) defines stable identity, native blocker provenance, complete-source readiness, immutable refresh and projection behavior. Inspected specs baseline: `7f6760e22cbdd0128e608a6591a1c94bdfd685bf`.
- [Laomedo Work Graph package](https://github.com/amadou-6e/laomedo/tree/0ead228a0adea44afd0467dea4acec93177af0b9/laomedo/work_graph) is the initial implementation baseline. Its development fixtures/tests are context only, not the EXP-01 oracle.

The dedicated [fixture response corpus](https://github.com/amadou-6e/laomedo/blob/7597c89d4dd2b305522f011240223079fd547ac9/experiments/exp01/corpus.json) and [hand-checked oracle](https://github.com/amadou-6e/laomedo/blob/7597c89d4dd2b305522f011240223079fd547ac9/experiments/exp01/oracle.json) were committed before execution. No live GitHub response, account token, or private issue body is a source for this attempt.

The [amended corpus and oracle](https://github.com/amadou-6e/laomedo/tree/de32cc8/experiments/exp01) were committed before the nine-case rerun. Both sets were prepared by the same author as the implementation without copying development fixtures; neither is a second-party oracle.
