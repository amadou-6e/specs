---
title: EXP-19 credential-free integration protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Credential-free phase zero

Question: can the current Laomedo Work Graph snapshot, EXP-04 durable run store and EXP-05 raw-event store retain one coherent selected-issue identity through a fake-agent result and a local Git PR candidate, while refusing stale or blocked input and preserving partial failure evidence?

Freeze the existing `examples/work-graph/github-pages.json` fixture, the local Laomedo implementation revision, a two-node synthetic flow definition, fake provider/model/effort, synthetic skill-byte digest, a local-only grant, and a zero-turn budget. Use issue `example/work#2`, whose prerequisite #1 is closed in the fixture. Bind the immutable graph snapshot ID, work key/source update marker, input digest, run ID, trace ID, component revision and local commit ref. A discovered PR is contextual only and must not become a target PR without explicit selection.

Run five conditions in disposable state: (1) source-ready success with a fake agent, a retained raw event and a local Git commit on a unique branch; (2) source body/update-marker change before dispatch; (3) an opened prerequisite; (4) incomplete source/blocker evidence; (5) fake-agent failure after one retained raw event. Require zero dispatch in conditions 2-4, no PR candidate in conditions 2-5, a durable failed run and partial trace in condition 5, and a complete binding only in condition 1. Compare exact snapshot and commit hashes; do not infer a GitHub PR from a local branch.

This phase may use local temporary directories and Git CLI only. It must not start Langflow, Codex, OpenCode or Claude; call a model; read a personal profile; post to GitHub; or change a real issue. The local grant authorizes only writing the disposable checkout. Retain a sanitized observation and test assertions with zero model turns and zero external writes. A pass establishes deterministic composition of these libraries, not Langflow graph execution, native agent events, production grant isolation, Work Graph source correctness, or a real PR. Full EXP-19 acceptance remains gated by its [listed prerequisites](https://github.com/amadou-6e/laomedo/issues/49), including deferred EXP-18 step 5.
