---
title: Environment runtime
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-17
applies_to: [theseo-anysearch]
related:
  - ../../rust/environment.md
  - ../../rust/bridge.md
  - ../../python/environments-python.md
---

# Environment runtime

## Problem and ownership

Own reset/step semantics, actions, rewards, termination and truncation, agent state,
multi-agent coordination, action masks, and Gymnasium/PettingZoo exposure. World
storage and observation representation remain separate subsystems.

## Consumers

Heuristics, RLlib, Tune, trajectory collection, world providers, and evaluation tools
consume the environment contract.

## Maturity and migration status

This entry maps imported native, bridge, and Python-wrapper specs. Exact action counts,
observation keys, and lifecycle hooks require reconciliation against current code.

## Reading map

- [Contract](contract/README.md)
- [Design](design/README.md)
- [Validation](validation.md)
