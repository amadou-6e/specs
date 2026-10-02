---
title: Agent handoffs and bounded controllers
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
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
provider, completed source, native thread, run, snapshot, model, effort and exact
ordered pinned skill set; runner
bindings remain authoritative. Failed resume never becomes a fresh run.

The Langflow Handoff node accepts a completed structured Run Reference and exposes
selected Task plus separate provenance. Connect Task to the next agent's Task and
connect pinned Skill nodes independently. Failed origins reject downstream work.
The visual node supports fresh answer/task handoffs. Connect its provenance output
to the target's Handoff Provenance input; the runner persists execution ID, step,
source provider/run and independent workspace policy with the target run. Sources
are declared provenance, not a cryptographic proof of a foreign provider's result.

## Workspace and artifacts

Fresh agents use independent runner-created workspaces. An explicit artifact
selection contains source provider/run UUID, complete snapshot hash, relative source
path, content hash and relative destination beneath `handoff/`. The runner resolves
only its own completed immutable post-run snapshots. Verify the entire source tree
before and after import, validate content hashes and persist the selected manifest
with the downstream run before dispatch. Maximum 32 files, 1 MiB each, 8 MiB total.
Reject absolute/traversal/alternate-stream paths, dot profile paths, credential/key
filenames, symlinks, reparse points, hard links, existing destinations and ambiguous
case-insensitive destination collisions. Copy only regular selected files, never
credentials or sessions implicitly. Arbitrary user-selected text/files are not
content-scanned for secrets; callers remain responsible for choosing task content.
Cross-provider file transfer fails closed without an explicitly audited shared
artifact store. Sequential shared workspaces remain unsupported and are rejected.

## Execution limits and stopping

The controller requires positive maximum iterations, aggregate submitted-turn
budget and deadline of at most 24 hours. One conservative reservation occurs
before each adapter call, including uncertain sends. A definite HTTP rejection
without a run ID from an explicit validation or authorization 4xx releases that
reservation; timeout, 5xx or transport failure retains
it because submission may have occurred. The deadline bounds dispatch attempts,
not remote execution: a timed-out fresh POST may leave a model turn running.
Every dispatch uses remaining deadline and shared cancellation signal. Stop on
explicit success predicate, chain end,
iteration/turn/deadline limit, cancellation, agent failure, repeated output, empty
output or predicate exception. Retain transitions and partial results. No retries.

Controller scheduling is separate from visual cycles: the delivered example is
an acyclic graph of two real custom Codex nodes. No runnable cyclic Langflow graph
is claimed. The native Bounded Agent Controller node provides bounded chains/loops
through the same adapter without requiring cyclic visual edges. It accepts task,
pinned skills, target provider/model/effort list, local endpoint map, exact success
answer, iteration/turn/deadline limits and private execution-state directory. Both
outputs share one dispatch per build; invalid targets fail before dispatch. Its
runtime package must be available to Langflow. A separate-volume deployment
configuration is a draft, not an automatic change to shared services.
The deployment draft disables Langflow auto-login and mounts a read-only runner
API capability file. Clients send that capability as a bearer header. It is
separate from the model login and never enters a flow or execution record.

Duplicate dispatch is rejected within one controller instance. Private records
persist each conservative turn reservation before send, selected input/provenance,
native run outcomes and partial cancellation evidence via atomic file replacement.
Concurrent cancel and run updates serialize their record writes.
Restart inspection labels interrupted/uncertain state and never replays dispatch.
Durable exactly-once dispatch and automatic restart continuation are not claimed.
Rerunning means creating a new explicit execution. Fresh HTTP POST lacks an early
run ID, so immediate remote cancellation cannot be guaranteed. Report unavailable
acknowledgment, retain evidence, and do not interpret client timeout as agent stop.

## Acceptance and current limits

- Credential-free pinned Langflow graph: agent B receives A's selected answer once;
  failed A never dispatches B; handles match generated port types.
- Controller tests: independent iteration, turn and deadline stops; success,
  repetition, cancellation, uncertain-send accounting and provider-bound resume.
- Native-controller graph tests establish success, iteration, turn, deadline,
  repetition, uncertain-send and cancellation stopping with persisted evidence.
  Runner tests establish selected-file boundaries and restart provenance.
- Shared workspaces remain intentionally unavailable, with conflicts rejected.
  Installed UI acceptance and real loops remain separate from synthetic checks.
- The user authorized four additional submitted turns across #27/#28, failures and
  timeouts included; #28 is allocated two for one real chain. Prior ledgers remain
  intact. Real loop calls are outside this allocation.
- Cross-provider live acceptance depends on Laomedo #27. Remote cancellation depends
  on #22 and outstanding native command finalization depends on #24.

This is partial implementation evidence for #28, not issue completion or accepted
production guarantees. Existing Docker permissions and prior ledgers are unchanged.
