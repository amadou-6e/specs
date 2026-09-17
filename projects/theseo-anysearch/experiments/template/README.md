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
├── 0..1 execution.md
├── 0..1 results.md
├── 0..1 replication.md
└── 0..1 evidence/
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
- one protocol may have `0..*` executions or reruns, all consolidated in the single
  `execution.md` rather than represented as sibling experiment entries;
- each recorded execution may produce `0..*` evidence artifacts, indexed by the one
  evidence manifest;
- one result record synthesizes the applicable executions and evidence without
  replacing either source; and
- one replication record may describe `0..*` replication attempts against the same
  frozen protocol and distinguishes them from ordinary reruns.

A planned experiment requires `README.md`, `protocol.md`, and `sources.md`. Once an
execution starts, `execution.md` and `evidence/README.md` become required. A concluded
experiment requires `results.md`. `replication.md` becomes required only when a
replication is attempted. Files remain present in this template to demonstrate the
complete lifecycle even when their logical cardinality is `0..1`.

## Problem statement

State the decision-relevant problem and why existing evidence is insufficient.

## Research questions and hypotheses

List bounded questions and falsifiable hypotheses.

## Scope and non-claims

State what the study can and cannot establish.

## Status and summarized outcome

Use `planned`, `running`, `complete`, `replicated`, or `superseded`. When complete,
summarize the outcome and disposition without replacing [results](results.md).

## Documents

- [Frozen protocol](protocol.md)
- [Execution record](execution.md)
- [Results](results.md)
- [Reproducibility and replication](replication.md)
- [Consolidated sources](sources.md)
- [Evidence manifest](evidence/README.md)
