---
title: World providers
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../world-provider-cli.md
  - ../../ifc-bench-mep-provider.md
  - ../../terrain-geometry-generator.md
---

# World providers

## Problem and ownership

Own provider discovery, source acquisition boundaries, deterministic generation or
conversion, routing-bundle production, independent verification, previews, local
registration, and explicit attachment to experiments. It does not own core world
storage or training split policy.

## Consumers

The worlds CLI, experiment configuration, benchmark adapters, geometry generators,
and local artifact workflows consume this subsystem.

## Maturity and migration status

The imported specs include proposed and implemented provider generations. Commands,
manifest versions, and provider capabilities must be checked against current code
before this entry becomes active.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Guides](guides/README.md)
- [Validation](validation.md)
