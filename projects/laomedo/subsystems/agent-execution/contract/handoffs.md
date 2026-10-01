---
title: Agent handoffs and bounded controllers
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent handoffs and bounded controllers

## Envelope and identity

An explicit envelope contains schema version, workflow execution UUID, zero-based
step, originating provider/run, allowlisted target provider/agent/model/effort,
selected task, pinned skill references, selected artifacts, operation and workspace
policy. Source records are not copied wholesale. Credentials, profiles and raw
native sessions are never implicit transfer payloads. User-selected task text is
not automatically redacted; callers must not select secrets as task text.

Fresh handoff carries no native thread or prior snapshot. Resume requires matching
provider, completed source, native thread, run, snapshot, model and effort; runner
bindings remain authoritative. Failed resume never becomes a fresh run.

The Langflow Handoff node accepts a completed structured Run Reference and exposes
selected Task plus separate provenance. Connect Task to the next agent's Task and
connect pinned Skill nodes independently. Failed origins reject downstream work.
The current visual node supports fresh answer/task handoffs only. Its provenance
output is inspectable but is not yet durably attached to the downstream run record.

## Workspace and artifacts

Fresh agents use independent runner-created workspaces. The first implementation
passes text and skill descriptors only. Nonempty artifact selections fail before
dispatch with `artifact_transfer_not_supported`; this is an explicit incomplete
criterion, not a claim of implemented safe file transfer. Sequential shared
workspaces remain unsupported. A future importer must validate source snapshot,
relative paths, content hashes, destination collisions, symlinks/reparse points and
credential exclusions before copying selected bytes, then bind its output manifest.

## Execution limits and stopping

The controller requires positive maximum iterations, aggregate submitted-turn
budget and deadline of at most 24 hours. One budget reservation occurs before each
adapter call, including uncertain sends. Every dispatch uses remaining deadline
and shared cancellation signal. Stop on explicit success predicate, chain end,
iteration/turn/deadline limit, cancellation, agent failure, repeated output, empty
output or predicate exception. Retain transitions and partial results. No retries.

Controller scheduling is separate from visual cycles: the delivered example is
an acyclic graph of two real custom Codex nodes. No runnable cyclic Langflow graph
is claimed. The standalone controller provides bounded loops through an adapter;
a native loop/controller node remains outside this initial partial delivery.

Duplicate dispatch is rejected within one controller instance. State is in memory;
restart/reconnect recovery and durable exactly-once semantics are not implemented.
Rerunning means creating a new explicit execution. Fresh HTTP POST lacks an early
run ID, so immediate remote cancellation cannot be guaranteed. Report unavailable
acknowledgment, retain evidence, and do not interpret client timeout as agent stop.

## Acceptance and current limits

- Credential-free pinned Langflow graph: agent B receives A's selected answer once;
  failed A never dispatches B; handles match generated port types.
- Controller tests: independent iteration, turn and deadline stops; success,
  repetition, cancellation, uncertain-send accounting and provider-bound resume.
- Artifact transfer, shared workspace conflicts, durable downstream provenance,
  installed UI acceptance and real chain/loop acceptance remain unverified or
  unimplemented. A new explicit aggregate turn/spend authorization is required.
- Cross-provider live acceptance depends on Laomedo #27. Remote cancellation depends
  on #22 and outstanding native command finalization depends on #24.

This is partial implementation evidence for #28, not issue completion or accepted
production guarantees. Existing Docker permissions and prior ledgers are unchanged.
