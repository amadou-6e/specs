---
title: Policy explainability
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../rllib/explain/README.md
---

# Policy explainability

## Problem and ownership

Own restoration and attribution of trained-policy decisions on identified episode
states, feature grouping, action comparison, explanation artifacts, and their CLI/API
surface. It explains deployed policy behavior rather than an isolated network.

## Consumers

Training diagnostics, collision investigations, trajectory replay, DQN/PPO analysis,
and researchers consume explanation artifacts.

## Maturity and migration status

The imported RLlib explainability folder is the principal source. This entry provides
its subsystem placement without rewriting that specification in this migration.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Guides](guides/README.md)
- [Validation](validation.md)
