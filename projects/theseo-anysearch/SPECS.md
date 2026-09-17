# Specification structure

This document is the Theseo AnySearch guide for placing, writing, reviewing, and
retiring specifications. The project may start with fewer categories, but it should
use these names and ownership boundaries as it grows.

## Principles

1. Organize primary documentation by subsystem, not programming language.
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
├── subsystems/
├── experiments/
├── research/
├── decisions/
├── implementation/
├── ui-design/
├── bugs/
└── legacy/
```

This top-level category set is closed for the current specification version. Do not add,
rename, or repurpose a top-level category without updating this document and reviewing
the ownership effects. Categories have three structural types:

| Type | Expansion rule | Template rule | Categories |
| --- | --- | --- | --- |
| Fixed top-structured | The category has one system-wide structure. Focused documents or named partitions may be added only within that declared structure. | A `template.md` is optional. Fixed partitions do not use copyable templates. | `architecture`, `implementation` |
| Expandable folder collection | Each new entry is an independently owned multi-file folder following one stable entry schema. | One directly copyable `template/` folder. No example-name layer beneath it. | `subsystems`, `experiments`, `ui-design` |
| Expandable document collection | Each new entry is one independently owned Markdown document. | One directly copyable `template.md`. | `research`, `decisions`, `bugs`, `legacy` |

“Expandable” applies to entries, not to the top-level taxonomy or template variants.
Each expandable category has one canonical template unless this guide explicitly
introduces another entry type. A template is a realistic live example, not an empty
file or an abstract directory tree.

## Container and entry documentation

Every directory that organizes child specification elements is a **container** and
must contain a `README.md`. Its README must define:

- the type and purpose of the elements it contains;
- the permitted child shapes and filenames;
- the cardinality of required, optional, and repeatable elements;
- the authority and ownership boundary of the container; and
- how its template is used, when the category has one.

Use `1`, `0..1`, and `0..*` in a small tree or equivalent table to make those
relationships explicit. This rule applies recursively to category containers and
fixed partitions, including the project root.

An individual specification entry is a **leaf entry**, even when it needs a folder
for several documents. Leaf entries do not need to restate this structural contract.
Template folders are examples of leaf-entry structure and likewise do not need a
second recursive container specification. Evidence, captures, references, component
assets, and similar support directories are also exempt unless they become an
independently extensible collection with their own entry contract.

The category type does not determine authority. Authority is defined by purpose:

- architecture describes the current cross-subsystem system;
- subsystems normatively own observable behavior and contracts;
- experiments preserve protocols, execution evidence, and bounded conclusions;
- research is exploratory and non-normative;
- decisions normatively record accepted durable choices and their rationale;
- implementation normatively guides contributors without redefining product behavior;
- UI design normatively owns reviewed visual geometry, states, and interactions by tab or window;
- bugs preserve verified defect knowledge while GitHub owns work status; and
- legacy is explicitly non-authoritative historical evidence.

Theseo provides one canonical reference template for each category:

- [architecture](architecture/template.md)
- [subsystems](subsystems/template/README.md)
- [experiments](experiments/template/README.md)
- [research](research/template.md)
- [decisions](decisions/template.md)
- [implementation](implementation/README.md)
- [UI design](ui-design/template/README.md)
- [bugs](bugs/template.md)
- [legacy](legacy/template.md)

## Root project documents

`README.md` is the project landing page. It explains the project, maps its major
subsystems, and gives reading paths for users, experiment authors, implementers, and
extension authors. It must link to authoritative pages rather than restating them.

`glossary.md` owns project-specific terminology. Define a term once and link to that
definition. Do not let subsystem pages develop incompatible meanings for terms such as
world, geometry, task, route, episode, stage, or observation.

## Architecture

Architecture explains relationships spanning several subsystems: system context,
component responsibilities, cross-language ownership, important data flows,
execution lifecycles, and system-wide invariants. It describes the current system.
Arguments for individual choices belong in decisions.

Architecture is top-structured rather than a collection of independent entry folders.
Use `architecture/README.md` for the system map and add focused documents or diagrams
beside it when necessary. The
[architecture template](architecture/template.md) shows the
expected content of those documents.

## Subsystems

A subsystem is a functionally cohesive part of Theseo that owns a stable behavioral
and contractual boundary. It may span multiple languages and packages, but it has one
purpose, explicit interfaces and dependencies, and independently verifiable behavior.
Its entry folder uses the following structure as applicable:

```text
subsystems/<subsystem>/
├── README.md          # ownership, scope, consumers, maturity, reading map
├── behavior.md        # observable behavior, guarantees, lifecycle, limitations
├── interfaces.md      # public APIs, CLIs, ABIs, and serialized contracts
├── configuration.md   # schema, defaults, validation, path and identity effects
├── architecture.md    # internal components, state ownership, data flow
├── validation.md      # tests, parity checks, benchmarks, acceptance evidence
├── usage.md           # local user workflows specific to this subsystem
├── troubleshooting.md # symptoms, diagnostics, workarounds, recovery
├── python.md          # Python-specific implementation guidance
├── rust.md            # Rust-specific implementation guidance
├── extensions.md      # supported extension points and conformance rules
└── migrations.md      # actionable deprecations and compatibility transitions
```

`README.md`, `behavior.md`, and `validation.md` are expected for a mature subsystem.
Other files are conditional. Small subsystems may initially keep these as sections in
`README.md`, but must retain the same conceptual boundaries. Language pages never
redefine public behavior. See the
[live subsystem example](subsystems/template/README.md). Copy the
`template/` folder and rename the copy for the subsystem; do not nest it beneath another
template directory.

A subsystem is not a stakeholder concern, code module, class, package, individual UI
surface, research topic, or cross-cutting quality. Cross-cutting properties such as
determinism, security, performance, naming, and compatibility belong in architecture,
decisions, or implementation unless they genuinely have their own behavioral interface
and ownership boundary.

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
research -> experiment or decision -> subsystem specification
```

Research must not silently become normative behavior. See the
[live research example](research/template.md). Research
entries are individual Markdown documents unless their evidence requires a dedicated
multi-file experiment.

## Decisions

Decision records explain why a durable choice was made. Each entry records status,
context, decision, alternatives, consequences, compatibility and migration effects,
and links to affected subsystems and experiments. Superseded decisions remain available
and point to their replacement. See the
[live decision example](decisions/template.md). Copy it to a
numbered decision filename; do not create a folder for an ordinary decision record.

## Implementation

Implementation is a fixed top-structured category with exactly three technology
partitions:

```text
implementation/
├── README.md
├── python/
│   └── README.md
├── rust/
│   └── README.md
└── rllib/
    └── README.md
```

It defines contributor expectations, source organization, dependency boundaries,
error and compatibility policy, testing, performance hazards, integration conventions,
and local execution workflows. It does not use a template because contributors do not
create arbitrary implementation partitions. Adding a fourth partition requires an
explicit revision of this guide.

Local runbooks are folded into implementation: installation, training, tuning,
monitoring, artifacts, caches, recovery, troubleshooting, and releases. Put
technology-specific procedures in the owning partition and genuinely cross-stack
procedures directly under `implementation/`. Subsystem-specific usage and diagnostic
facts remain in the subsystem's `usage.md` and `troubleshooting.md`.

Implementation guidance may link to subsystem contracts but must not become a second
source of truth for product behavior. See the
[implementation index](implementation/README.md).

## UI design

UI design is an expandable folder collection split by independently navigable tab or
window. A tab is a primary destination within a shared application shell. A window is
a separately opened native or application surface with its own lifecycle. Each tab or
window owns one folder:

```text
ui-design/<tab-or-window>/
├── README.md        # purpose, entry/exit, states, interactions, ownership
├── design.drawio    # sole authority for visual geometry and transitions
├── references/      # source screenshots used for fidelity comparison
├── captures/        # reviewed renders or implementation comparisons
└── components/      # components owned only by this tab or window
```

Panels, dialogs, sidebars, and components do not become sibling top-level UI entries;
they stay under the tab or window that owns their lifecycle. Use `ui-design/shared/`
only for shell chrome, flows, or components with no single tab/window owner. A shared
artifact must link every consuming surface and must not become a substitute for each
surface's state and interaction specification.

The reviewed Draw.io file is authoritative for geometry, component states,
interaction identifiers, and transitions. `README.md` provides navigation and design
intent but cannot introduce behavior absent from Draw.io. References and captures are
evidence, not editable sources. See the
[UI-design template](ui-design/template/README.md). The existing combined replayer
workshop predates this structure and will be split in a separate migration.

## Bugs

Bugs is an expandable collection of individual records for defects with durable
diagnostic or design value: failures that are difficult to diagnose, platform-specific,
likely to recur, capable of silently invalidating results, or associated with an
important workaround. Ordinary defects do not need specification records.

GitHub issues remain authoritative for ownership, priority, implementation work, and
closure. A bug record preserves symptoms, expected behavior, affected conditions,
impact, verified root cause, workaround, resolution links, regression verification,
and lessons incorporated into subsystems or implementation guidance. See the
[bug template](bugs/template.md).

## Legacy

Legacy preserves non-authoritative history with continuing evidential value. It is not
a dumping ground for active deprecations: user-actionable transitions remain in the
owning subsystem's `migrations.md`. Every legacy entry identifies why it was archived,
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
kind: subsystem
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

Bug records use the more specific lifecycle `reported`, `confirmed`,
`fix-in-progress`, `resolved`, `not-reproducible`, or `superseded`. The GitHub issue,
not the bug record, remains authoritative for current work status.

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
