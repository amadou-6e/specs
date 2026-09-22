# Model Garden specification structure

This guide defines where Model Garden specifications belong, which categories may
expand, and how their local templates and skills are used. Model Garden follows the
Theseo family taxonomy while owning its own examples, evidence, and authoring rules.

## Principles

1. Organize current behavior by subsystem rather than by source-language package.
2. Keep architecture, normative contracts, experiments, research, implementation
   guidance, and historical evidence distinguishable.
3. Preserve frozen protocols, actual execution, raw evidence, and bounded results as
   separate experiment authorities.
4. Treat an accepted encoder artifact as a registry and qualification outcome, not as
   an implication of a promising research or experiment result.
5. Preserve identity-bearing historical paths and records without presenting them as
   current guidance.
6. Keep AnySearch consumer integration and World Providers acquisition behavior with
   those peer projects.

## Project layout

```text
theseo-model-garden/
|-- 1 README.md
|-- 1 SPECS.md
|-- 1 spec.json
|-- 1 architecture/
|-- 1 subsystems/
|-- 1 experiments/
|-- 1 research/
|-- 1 implementation/
`-- 1 legacy/
```

The top-level category set is closed. Do not add, rename, or repurpose a category
without revising this guide and reviewing ownership effects.

| Structural type | Expansion rule | Template rule | Categories |
| --- | --- | --- | --- |
| Fixed top-structured | One project-wide structure; focused documents or declared partitions may be added within it. | Architecture provides `template.md`; implementation deliberately has no copyable template. | `architecture`, `implementation` |
| Expandable folder collection | Each entry is an independently owned multi-file folder with one stable schema. | One directly copyable `template/` folder. | `subsystems`, `experiments`, `research` |
| Expandable document collection | Each ordinary entry is one independently owned Markdown document. | One directly copyable `template.md`. | `legacy` |

Every container directory has a `README.md` defining its children, cardinalities,
authority, and template use. A multi-file template's README defines the internal shape
of one entry. Concrete entries need not repeat that structural contract.

## Category authority and authoring resources

### Architecture

`architecture/README.md` is the current project-wide system and relationship map.
Focused cross-subsystem pages sit beside it. Use
[architecture/template.md](architecture/template.md) and
[architecture/SKILL.md](architecture/SKILL.md). The imported monolith is evidence to
reconcile, not a template or current contract.

### Subsystems

Each subsystem owns one observable behavioral boundary and its implementation design.
A mature entry contains `README.md`, `contract/README.md`, `design/README.md`, and
`validation.md`; interface, configuration, guide, extension, and migration pages are
conditional. Copy [subsystems/template/](subsystems/template/README.md) and use its
[SKILL.md](subsystems/template/SKILL.md).

### Experiments

Each experiment owns one overview, one frozen `protocol.md`, one consolidated
`sources.md`, and zero or more ordered iterations. A started iteration records actual
execution and an evidence manifest; a concluded iteration adds results; replication is
present only when performed. Copy
[experiments/template/](experiments/template/README.md) and use
[experiments/SKILL.md](experiments/SKILL.md).

### Research

Each research topic owns a reproducible method, one or more individually characterized
sources, one or more bounded findings, and a synthesis that introduces no unsupported
claim. Copy [research/template/](research/template/README.md) and use
[research/SKILL.md](research/SKILL.md). Existing flat research pages are migration
inputs until substantively reviewed.

### Implementation

Implementation is fixed and currently contains the Python partition plus optional
cross-stack contributor documents. It owns engineering conventions and local workflows,
not product behavior. It intentionally has no template because contributors do not
create arbitrary implementation partitions. See
[implementation/README.md](implementation/README.md).

### Legacy

Legacy preserves non-authoritative records with continuing evidential or identity
value. Ordinary entries are Markdown files created from
[legacy/template.md](legacy/template.md) using [legacy/SKILL.md](legacy/SKILL.md).
The imported `legacy/python/` tree is a preservation area, not an alternative entry
schema. Active protocol and migration guidance belong to their current owners.

## Metadata

New entries use only metadata that can be maintained accurately:

```yaml
---
title: Example title
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: YYYY-MM-DD
applies_to: [theseo-model-garden]
supersedes: null
related: []
---
```

Generic lifecycle values are `draft`, `active`, `complete`, `deprecated`, and
`superseded`; templates use `template`. Experiments use `planned`, `running`,
`complete`, `replicated`, or `superseded` in their experiment status narrative.

## Validation

Before review, confirm that the canonical category owns the document, template content
was replaced rather than copied as false evidence, links resolve, normative statements
are distinguishable from evidence, historical records identify current replacements,
and `python tools/validate_specs.py` passes.

Experiment evidence may cite historical paths in immutable reports. Those fields are
provenance and are not rewritten merely because the containing file moved.
