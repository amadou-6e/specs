---
title: Work Graph dispatch-binding sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [EXP-16 #46](https://github.com/amadou-6e/laomedo/issues/46): selected work/graph snapshots, freshness, blockers, grants, overrides and retained run/trace refs.
- [Work Graph contract](../../subsystems/work-graph/contract/work-graph.md): immutable records and binding semantics. Inspected specs baseline `ddb99c6d4aef61679df91229b668d0a87714e8bf`.
- [EXP-01 #50](../work-graph-source-integrity/README.md), merged specs #218 and Laomedo #74: synthetic source-integrity verification gate.
- [EXP-03 #33](../langflow-graph-freeze/README.md): native component-version freeze failed. Real adapter enforcement is tracked in [#77](https://github.com/amadou-6e/laomedo/issues/77).
- Laomedo `work_graph`, `workflow_run_store`, and EXP-05 evidence store at merged `develop` baseline `d3be94acf05b9720d55e4b9844067f073052846d` provide existing, separate components for the mock experiment.

The [EXP-16 response corpus and cases](https://github.com/amadou-6e/laomedo/tree/a776578a29b68de6ff0d55be7e3e048f89273a03/experiments/exp16) and hand-written oracle were committed before execution. The [probe revision](https://github.com/amadou-6e/laomedo/blob/6495714b0c9bce4a319dc74609b589f93e91c381/experiments/exp16/probe.py) was also committed before the first run. The experiment author wrote the oracle; it was separate from product tests but was not independently prepared by another party. No live source response, personal credential or private issue body was an input.
