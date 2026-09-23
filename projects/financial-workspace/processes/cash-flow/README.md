---
title: Cash-flow process
status: draft
kind: process
owners:
  - amadou-6e
last_reviewed: 2026-09-23
applies_to:
  - financial-workspace
supersedes: null
related:
  - model/mappings/cross-system
  - migrations/0001-existing-system
---

# Cash-flow process

This entry specifies portable acquisition, analysis, reconciliation, replay, review, and approved Notion publication for cash-flow data.

```text
cash-flow/
|-- README.md    1
|-- workflow.md  1
`-- examples/   0..1
```

[workflow.md](workflow.md) is the current design. Generated manifests, cached evidence, reconciliation outputs, and publication audits belong in `workspaces/cash-flow/runs/<run-id>/` in the financial repository.
