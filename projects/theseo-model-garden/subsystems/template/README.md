---
title: Model registry
status: template
kind: subsystem
owners: [theseo-team]
last_reviewed: YYYY-MM-DD
applies_to: [theseo-model-garden]
supersedes: null
related: []
---

# Model registry

This example demonstrates a mature subsystem entry. The overview, contract, design,
and validation record are required; guides and migrations are included when
applicable.

## Contained elements and relationships

```text
<subsystem>/
â”œâ”€â”€ 1 README.md
â”œâ”€â”€ 1 contract/
â”‚   â”œâ”€â”€ 1 README.md
â”‚   â”œâ”€â”€ 0..1 interfaces.md
â”‚   â”œâ”€â”€ 0..1 configuration.md
â”‚   â””â”€â”€ 0..1 extensions.md
â”œâ”€â”€ 1 design/
â”‚   â”œâ”€â”€ 1 README.md
â”‚   â”œâ”€â”€ 0..1 python.md
â”‚   â””â”€â”€ 0..1 rust.md
â”œâ”€â”€ 0..1 guides/
â”‚   â”œâ”€â”€ 1 README.md
â”‚   â””â”€â”€ 0..1 troubleshooting.md
â”œâ”€â”€ 0..1 extensions/
â”‚   â”œâ”€â”€ 1 README.md
â”‚   â””â”€â”€ 0..* <extension>/
â”œâ”€â”€ 1 validation.md
â””â”€â”€ 0..1 migrations.md
```

The subsystem entry is the aggregate root for one behavioral and contractual
boundary. Its internal relationships are:

- one subsystem owns `1..*` observable guarantees, invariants, lifecycle rules, or
  limitations, consolidated in `contract/README.md`;
- one subsystem may expose `0..*` public APIs, CLIs, ABIs, events, or serialized
  contracts, consolidated in `contract/interfaces.md`;
- one subsystem may expose `0..*` configuration fields or configuration groups,
  consolidated in `contract/configuration.md`;
- `contract/extensions.md` may define `0..*` extension points and their conformance
  rules;
- `design/README.md` explains how `1..*` internal components realize the owned
  contract, but cannot redefine that contract;
- `validation.md` maps each decision-relevant guarantee to `0..*` checks, proofs,
  benchmarks, or other acceptance evidence and explicitly identifies any guarantee
  that still has no verification;
- `guides/README.md` and `guides/troubleshooting.md` describe workflows and diagnostics
  for the same subsystem rather than creating additional behavioral owners;
- `design/python.md` and `design/rust.md` map the contract onto language-specific
  implementation responsibilities without becoming separate subsystem
  specifications; and
- `extensions/` contains `0..*` concrete optional implementations of extension points
  declared by `contract/extensions.md`; each extension depends on the host contract
  and cannot redefine it; and
- `migrations.md` may define `0..*` active compatibility transitions from an older
  contract to the current one.

A mature subsystem requires `README.md`, `contract/README.md`, `design/README.md`, and
`validation.md`. Add optional pages, `guides/`, and `extensions/` only when their
subject exists; do not create empty elements merely to match the complete template.
The template includes documentation for the extension relationship but need not ship
a concrete example extension.

## Problem and ownership

State the capability this subsystem owns and the boundary beyond which another subsystem
takes responsibility.

## Consumers

List dataset builders, trainers, qualification workflows, registry clients, extensions,
and external consumers that depend on it.

## Guarantees

Summarize the most important observable guarantees and link to the
[contract](contract/README.md).

## Maturity and limitations

State lifecycle status, supported use cases, exclusions, and known limitations.

## Reading map

- [Contract, behavior, and guarantees](contract/README.md)
- [Interfaces](contract/interfaces.md)
- [Configuration](contract/configuration.md)
- [Extension points](contract/extensions.md)
- [Internal design and architecture](design/README.md)
- [Python implementation](design/python.md)
- [Rust implementation](design/rust.md)
- [Validation](validation.md)
- [Usage](guides/README.md)
- [Troubleshooting](guides/troubleshooting.md)
- [Concrete extensions](extensions/README.md)
- [Migrations](migrations.md)
