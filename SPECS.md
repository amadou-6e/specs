# Specification structure

This document is the repository-wide guide for placing, writing, reviewing, and
retiring specifications. A project may start with fewer categories, but it should use
these names and ownership boundaries as it grows.

## Principles

1. Organize primary documentation by concern, not programming language.
2. Give every behavior or contract one canonical owner; other pages link to it.
3. Keep normative specifications, implementation guidance, research evidence, and
   historical records distinguishable.
4. Separate an experiment's frozen protocol, execution record, evidence, and result.
5. Preserve negative results and superseded decisions without presenting them as
   current behavior.
6. A merged experiment result records knowledge; it does not promote a model or
   implementation unless a separate decision says so.
7. Update specifications with behavior changes and identify unresolved decisions
   explicitly.

## Project layout

```text
projects/<project>/
├── README.md
├── glossary.md
├── architecture/
├── concerns/
├── experiments/
├── research/
├── decisions/
├── implementation/
├── operations/
└── legacy/
```

Only create a category when the project has material for it. Every created category
must contain a `template/` subfolder. The template contains a realistic example entry
folder, not merely an empty file or an abstract directory tree.

The Theseo AnySearch project provides the reference templates:

- [architecture](projects/theseo-anysearch/architecture/template/streaming-world-system/README.md)
- [concerns](projects/theseo-anysearch/concerns/template/world-storage/README.md)
- [experiments](projects/theseo-anysearch/experiments/template/compact-encoder-study/README.md)
- [research](projects/theseo-anysearch/research/template/voxel-rendering-landscape/README.md)
- [decisions](projects/theseo-anysearch/decisions/template/000-separate-worlds-and-tasks/README.md)
- [implementation](projects/theseo-anysearch/implementation/template/python/README.md)
- [operations](projects/theseo-anysearch/operations/template/training-runbook/README.md)
- [legacy](projects/theseo-anysearch/legacy/template/superseded-world-format/README.md)

## Root project documents

`README.md` is the project landing page. It explains the project, maps its major
concerns, and gives reading paths for users, experiment authors, implementers, and
extension authors. It must link to authoritative pages rather than restating them.

`glossary.md` owns project-specific terminology. Define a term once and link to that
definition. Do not let concern pages develop incompatible meanings for terms such as
world, geometry, task, route, episode, stage, or observation.

## Architecture

Architecture explains relationships spanning several concerns: system context,
component responsibilities, cross-language ownership, important data flows,
execution lifecycles, and system-wide invariants. It describes the current system.
Arguments for individual choices belong in decisions.

An architecture entry normally contains a `README.md` and may add focused diagrams or
pages when the subject is too large for one document. See the
[live architecture example](projects/theseo-anysearch/architecture/template/streaming-world-system/README.md).

## Concerns

A concern owns one coherent product or platform capability. Its entry folder uses the
following structure as applicable:

```text
concerns/<concern>/
├── README.md          # ownership, scope, consumers, maturity, reading map
├── behavior.md        # observable behavior, guarantees, lifecycle, limitations
├── interfaces.md      # public APIs, CLIs, ABIs, and serialized contracts
├── configuration.md   # schema, defaults, validation, path and identity effects
├── architecture.md    # internal components, state ownership, data flow
├── validation.md      # tests, parity checks, benchmarks, acceptance evidence
├── operations.md      # diagnostics, metrics, sizing, troubleshooting
├── python.md          # Python-specific implementation guidance
├── rust.md            # Rust-specific implementation guidance
├── extensions.md      # supported extension points and conformance rules
└── migrations.md      # actionable deprecations and compatibility transitions
```

`README.md`, `behavior.md`, and `validation.md` are expected for a mature concern.
Other files are conditional. Small concerns may initially keep these as sections in
`README.md`, but must retain the same conceptual boundaries. Language pages never
redefine public behavior. See the
[live concern example](projects/theseo-anysearch/concerns/template/world-storage/README.md).

## Experiments

Experiments answer bounded research questions under explicit decision rules:

```text
experiments/<experiment>/
├── README.md       # question, hypothesis, status, summary, non-claims
├── protocol.md     # frozen design, metrics, gates, permitted adaptations
├── execution.md    # revisions, commands, hardware, deviations, produced artifacts
├── results.md      # outcomes, uncertainty, failed gates, interpretation, disposition
├── replication.md  # reproducibility and fresh-data/fresh-seed replication status
├── sources.md      # code, specs, data, artifacts, literature, related experiments
└── evidence/       # machine-readable reports or a manifest linking large artifacts
```

Freeze `protocol.md` before observing decision-bearing results. Record deviations in
`execution.md`; never silently rewrite the protocol to match what happened. Keep raw
evidence machine-readable and summarize it in `results.md`. See the
[live experiment example](projects/theseo-anysearch/experiments/template/compact-encoder-study/README.md).

## Research

Research contains exploratory knowledge that is useful but not yet a product contract:
literature reviews, technology surveys, feasibility assessments, benchmark surveys,
and open questions. Each entry states its question, relevance, sources and search date,
findings, limitations, recommendation, and unresolved questions.

The normal promotion path is:

```text
research -> experiment or decision -> concern specification
```

Research must not silently become normative behavior. See the
[live research example](projects/theseo-anysearch/research/template/voxel-rendering-landscape/README.md).

## Decisions

Decision records explain why a durable choice was made. Each entry records status,
context, decision, alternatives, consequences, compatibility and migration effects,
and links to affected concerns and experiments. Superseded decisions remain available
and point to their replacement. See the
[live decision example](projects/theseo-anysearch/decisions/template/000-separate-worlds-and-tasks/README.md).

## Implementation

Implementation guidance defines contributor expectations for a language, framework,
or cross-cutting engineering domain. Typical entries include `shared`, `python`,
`rust`, `rllib`, `extensions`, `testing`, and `review`. They cover source organization,
dependency boundaries, error and compatibility policy, testing, performance hazards,
and integration conventions.

Implementation guidance may link to concern contracts but must not become a second
source of truth for product behavior. See the
[live implementation example](projects/theseo-anysearch/implementation/template/python/README.md).

## Operations

Operations contains end-to-end runbooks for running and maintaining the system:
installation, training, tuning, monitoring, artifacts, caches, recovery,
troubleshooting, and releases. Concern-specific operational facts stay with their
concern; operational entries compose those facts into complete workflows. See the
[live operations example](projects/theseo-anysearch/operations/template/training-runbook/README.md).

## Legacy

Legacy preserves non-authoritative history with continuing evidential value. It is not
a dumping ground for active deprecations: user-actionable transitions remain in the
owning concern's `migrations.md`. Every legacy entry identifies why it was archived,
when it stopped being authoritative, and what replaced it. See the
[live legacy example](projects/theseo-anysearch/legacy/template/superseded-world-format/README.md).

## Metadata

Every new entry begins with a short metadata block. Use only fields that the document
can maintain accurately:

```yaml
---
title: Example title
status: draft
kind: concern
owners:
  - project-team
last_reviewed: YYYY-MM-DD
applies_to:
  - project
supersedes: null
related: []
---
```

Allowed lifecycle values are `draft`, `active`, `complete`, `deprecated`, and
`superseded`. Templates use `status: template` so they cannot be mistaken for active
specifications. Experiments additionally record governing protocol, implementation,
data, and result identities in `execution.md` once known.

## Review checklist

Before opening a specification pull request, confirm that:

- the document is in the category that owns its purpose;
- links point to canonical contracts instead of duplicating them;
- normative statements are distinguishable from evidence and recommendations;
- configuration examples do not masquerade as the authoritative schema;
- behavior, limitations, validation, compatibility, and migration effects are explicit;
- unresolved decisions are recorded rather than invented;
- superseded material points to its replacement;
- the project landing page is updated when navigation changes; and
- `python tools/validate_specs.py` passes.
