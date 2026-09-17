# Specification structure

This document is the Theseo AnySearch guide for placing, writing, reviewing, and
retiring specifications. The project may start with fewer categories, but it should
use these names and ownership boundaries as it grows.

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
must contain one canonical template. Use `template/` when an entry is a multi-file
folder and `template.md` when the category is top-structured or entries are individual
documents. The template is a realistic example, not an empty file or an abstract
directory tree. Do not add another example-name layer inside `template/`; multiple
templates are not expected unless the category explicitly defines distinct entry types.

Theseo provides one canonical reference template for each category:

- [architecture](architecture/template.md)
- [concerns](concerns/template/README.md)
- [experiments](experiments/template/README.md)
- [research](research/template.md)
- [decisions](decisions/template.md)
- [implementation](implementation/template.md)
- [operations](operations/template.md)
- [legacy](legacy/template.md)

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

Architecture is top-structured rather than a collection of independent entry folders.
Use `architecture/README.md` for the system map and add focused documents or diagrams
beside it when necessary. The
[architecture template](architecture/template.md) shows the
expected content of those documents.

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
[live concern example](concerns/template/README.md). Copy the
`template/` folder and rename the copy for the concern; do not nest it beneath another
template directory.

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
[live experiment example](experiments/template/README.md).
Copy the `template/` folder and rename the copy for the experiment.

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
[live research example](research/template.md). Research
entries are individual Markdown documents unless their evidence requires a dedicated
multi-file experiment.

## Decisions

Decision records explain why a durable choice was made. Each entry records status,
context, decision, alternatives, consequences, compatibility and migration effects,
and links to affected concerns and experiments. Superseded decisions remain available
and point to their replacement. See the
[live decision example](decisions/template.md). Copy it to a
numbered decision filename; do not create a folder for an ordinary decision record.

## Implementation

Implementation guidance defines contributor expectations for a language, framework,
or cross-cutting engineering domain. Typical entries include `shared`, `python`,
`rust`, `rllib`, `extensions`, `testing`, and `review`. They cover source organization,
dependency boundaries, error and compatibility policy, testing, performance hazards,
and integration conventions.

Implementation guidance may link to concern contracts but must not become a second
source of truth for product behavior. See the
[live implementation example](implementation/template.md).
Implementation is top-structured: create focused documents such as `python.md`,
`rust.md`, or `rllib.md` directly in the category.

## Operations

Operations contains end-to-end runbooks for running and maintaining the system:
installation, training, tuning, monitoring, artifacts, caches, recovery,
troubleshooting, and releases. Concern-specific operational facts stay with their
concern; operational entries compose those facts into complete workflows. See the
[live operations example](operations/template.md). Ordinary
runbooks are individual Markdown documents; use a folder only when a runbook owns
supporting artifacts.

## Legacy

Legacy preserves non-authoritative history with continuing evidential value. It is not
a dumping ground for active deprecations: user-actionable transitions remain in the
owning concern's `migrations.md`. Every legacy entry identifies why it was archived,
when it stopped being authoritative, and what replaced it. See the
[live legacy example](legacy/template.md). Ordinary archive
entries are individual Markdown documents and must link to their active replacement.

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
