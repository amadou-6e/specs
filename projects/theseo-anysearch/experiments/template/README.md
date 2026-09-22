---
title: Compact encoder study
status: template
kind: experiment
owners: [theseo-team]
last_reviewed: YYYY-MM-DD
applies_to: [theseo-anysearch]
supersedes: null
related: []
---

# Compact encoder study

This example separates the research question from the frozen protocol, actual
execution, evidence, results, and replication record.

## Contained elements and relationships

```text
<experiment>/
├── 1 README.md
├── 1 protocol.md
├── 1 sources.md
└── 0..1 iterations/
    ├── 1 README.md
    └── 1..* <iteration>/
        ├── 1 README.md
        ├── 1 execution.md
        ├── 0..1 results.md
        ├── 0..1 replication.md
        └── 1 evidence/
            ├── 1 README.md
            └── 0..* evidence artifacts or artifact references
```

The experiment entry is the aggregate root for all of these elements. Their
relationships are:

- one experiment defines one frozen protocol;
- one protocol defines `1..*` research questions, `0..*` hypotheses, `1..*` stop or
  decision gates, `0..*` sub-experiments, and `0..*` planned iterations;
- one experiment has one consolidated source list, shared by all of its protocol,
  execution, result, and replication claims;
- one experiment may have `0..*` iterations governed by that protocol;
- each iteration has one execution record and one evidence manifest containing
  `0..*` evidence artifacts or stable artifact references;
- each concluded iteration has one result record synthesizing that iteration's
  execution and evidence without replacing either source; and
- an iteration that tests reproducibility or replication has one replication record
  distinguishing an identical-input rerun from a fresh-seed, fresh-data, or
  independent replication attempt.

A planned experiment requires `README.md`, `protocol.md`, and `sources.md`. The
`iterations/` container is created when the first iteration starts. Every started
iteration requires its own `README.md`, `execution.md`, and `evidence/README.md`; a
concluded iteration requires `results.md`; and `replication.md` is required only for
an iteration that performs a reproducibility or replication check. The sample
`iteration-001/` demonstrates the complete iteration shape.

## Problem statement

State the decision-relevant problem and why existing evidence is insufficient.

## Research questions and hypotheses

List bounded questions and falsifiable hypotheses.

## Scope and non-claims

State what the study can and cannot establish.

## Status and summarized outcome

Use `planned`, `running`, `complete`, `replicated`, or `superseded`. When complete,
summarize the outcome and disposition without replacing iteration-level results.

## Documents

- [Frozen protocol](protocol.md)
- [Consolidated sources](sources.md)
- [Iterations](iterations/README.md)
