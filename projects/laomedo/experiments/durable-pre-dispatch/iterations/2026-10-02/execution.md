---
title: Durable pre-dispatch execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

On Windows with Python 3.12, run python experiments/exp04/probe.py on Laomedo feat/34. Each child uses an independent temporary SQLite database, synchronous FULL and WAL, then exits at its selected crash phase. Parent reopens the database and performs startup sweep. The callback only inserts a synthetic monotonic counter row. No Langflow server, model, agent, personal credential or network call was used in this probe. Python unit tests cover invalid config/source, dispatch without reservation, one-attempt enforcement and idempotent startup sweep.

An initial probe failed temporary-directory cleanup on Windows because SQLite connections were committed but not closed. The store was corrected to close each connection, then the six-phase probe and tests passed. The earlier cleanup failure is retained here as recovered setup evidence. The protocol does not establish that the live Langflow adapter uses this store or that an OS/filesystem power loss cannot defeat SQLite durability.
