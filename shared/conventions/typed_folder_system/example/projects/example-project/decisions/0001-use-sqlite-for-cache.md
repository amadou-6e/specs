---
title: Use SQLite for Widget Store persistence
status: active
kind: decision
owners:
  - example-team
last_reviewed: 2026-01-01
applies_to:
  - example-project
supersedes: null
related:
  - subsystems/widget-store
---

# Use SQLite for Widget Store persistence

A named entry copied from [`template.md`](template.md) and filled in.

## Status

Active.

## Context

Widget Store needs durable persistence with no separate database service to operate
in this example.

## Decision

Widget Store persists to a single local SQLite file.

## Alternatives considered

- In-memory only: rejected, does not survive a restart.
- A separate database service: rejected, adds operational surface this example does
  not need.

## Consequences

Single-writer throughput is bounded by SQLite's single-connection-mutex design; this
is acceptable for the example's expected load.

## Compatibility and migration

None; this is the initial storage choice.

## Links

- [Widget Store subsystem](../subsystems/widget-store/README.md)
