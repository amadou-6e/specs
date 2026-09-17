---
title: Voxel rendering landscape
status: template
kind: research
owners: [theseo-team]
last_reviewed: YYYY-MM-DD
applies_to: [theseo-anysearch]
supersedes: null
related: []
---

# Voxel rendering landscape

This example shows how a research topic separates method, source characterization,
individual findings, and synthesis.

## Contained elements and relationships

```text
<research-topic>/
├── 1 README.md
├── 1 method.md
├── 1 findings/
│   ├── 1 README.md
│   └── 1..* <finding>.md
└── 1 sources/
    ├── 1 README.md
    └── 1..* <source>.md
```

One research topic owns `1..*` questions, `1..*` sources, and `1..*` findings. Every
finding cites `1..*` source records. One source may support, qualify, or contradict
`0..*` findings. Findings distinguish externally reported claims, directly verified
facts, synthesis, project-specific inference, and recommendations. This README
synthesizes the finding records but must not introduce claims that they do not support.

## Question and relevance

Define the exploratory question and why it matters to the project.

## Method and search date

Summarize the search boundary and link to the full [method](method.md).

## Evaluation criteria

State how sources and candidate approaches are compared. Keep eligibility criteria
separate from conclusions.

## Synthesized findings

Summarize the registered [findings](findings/README.md), preserving their identifiers,
classification, confidence, and disagreements.

## Comparison

Use a matrix when several findings compare the same candidates or dimensions. Every
cell containing a substantive claim must resolve to a finding or source record.

## Applicability and limitations

Explain what transfers to the project, what does not, and why.

## Recommendation and open questions

Recommend experiments or decisions without turning the recommendation into a contract.

## Sources

Use the [source registry](sources/README.md). Do not replace characterized source
records with an unexplained list of links.
