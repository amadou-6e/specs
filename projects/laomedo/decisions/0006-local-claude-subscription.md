---
title: Local Claude Code subscription prototype
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-26
applies_to: [laomedo]
---

# Local Claude Code subscription prototype

The owner chose Claude Code subscription authentication and explicitly approved
mirroring only the current access credential into a dedicated local Docker profile.
The 2026-10-26 workspace opt-in keeps refresh ownership exclusively on the host;
the rotating refresh credential must never be copied.
For this single-user prototype, drive the official pinned CLI stream protocol
rather than describe it as the Agent SDK transport. The SDK remains the broader
target; no shared/hosted authentication or distribution acceptance is implied.

The controller image owns a dedicated profile and resumable sessions. Do not copy
personal sessions, settings, memories, or an entire profile. Do not print login
material, put it in graphs, or substitute API billing. Refresh only on the host.
The mirrored access credential must cover the execution deadline; refuse an expired or insufficiently long-lived credential. Do not
overwrite a profile holding an independently established refresh-capable login. An operator may instead sign into the dedicated profile with mirroring disabled.

Model-callable native controller file/shell tools are disabled. Draft file work
and commands execute in separate containers without credentials or network.
Selected immutable skills may use the native Skill tool, but controller-side
preprocessing and permission/session/model overrides are refused. External effects
require an explicit host-mediated grant. Independent supervision must survive an
API exit; completed-session Resume must not imply crash-safe replay (D17).

Requested configuration and observed native evidence stay distinct. Missing
native effort or usage stays unknown. Historical verification allowances are
retained as evidence only, never gates in normal services. Full source review,
real graph/error/cancellation evidence and the owner's graph approval remain
release gates. Initial live successes alone do not establish full acceptance.
