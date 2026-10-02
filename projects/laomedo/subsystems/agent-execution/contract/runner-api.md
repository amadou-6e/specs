---
title: Local runner API boundary
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Local runner API boundary

This page owns the tested single-user local HTTP control plane used by the
[Codex pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md).
It is narrower than production authentication, which remains with
[specs #129](https://github.com/amadou-6e/specs/issues/129). The runner binds
only to host loopback. Docker Desktop can still route a bridged container to
that listener through `host.docker.internal`, so loopback binding alone is not
an access boundary.

On startup, the runner creates or reuses a random 64-hex API capability at
`<private-runner-state>/api-token`. Every `GET` and `POST` under `/v1/runs`
requires `Authorization: Bearer <api-token>`. Missing or incorrect capability
returns HTTP 401 before reading a run or reserving a turn. This covers fresh
start, status, resume, cancel, and artifact selection where supported. The
capability is separate from the model login, never belongs in flow JSON or
agent command containers, and may be mounted read-only into a trusted
Langflow server. Every custom component and other code running in that server
can then read it. On Windows, the private state directory ACL provides the
file boundary; Unix `0o600` does not establish a Windows ACL.

Fresh `POST /v1/runs` accepts task, model, effort, and exact pinned skill
reference. `GET /v1/runs/{run_id}` returns a persisted run record.
`POST /v1/runs/{run_id}/resume` requires task, model, effort, native thread ID,
and post-run snapshot hash. `POST /v1/runs/{run_id}/cancel` requests stop and
returns HTTP 202 when accepted. Invalid inputs fail before model dispatch where
possible. A failed or timed-out accepted run retains its run ID, category, and
partial events; client timeout is not evidence that remote work stopped.

For active Codex turns, the runner addresses a uniquely named container,
sends native `turn/interrupt`, force-removes the owned container, and verifies
removal on cancel or timeout. If removal cannot be verified, it records
`container_termination_unverified` instead of reporting a clean stop. A no-model
Docker canary established this teardown path after the 2026-10-01 pilot; that
pilot itself observed cancellation status and 39 retained events but did not
verify immediate container termination. A cancel before `turn/start` can still
reserve a turn before interruption. No atomic cancel/dispatch guarantee is
claimed. The permission file content did not change; the runner accepts only
its reviewed CRLF and LF byte hashes for Windows and Linux checkouts.

Acceptance for this local boundary requires an unauthenticated bridged worker
request to return 401, an authorized request to succeed, a private token file
absent from the agent mounts, and a no-model cancel/timeout probe to observe
owned-container removal. These checks do not establish hosted or multi-user
tenancy, complete network isolation, or production credential lifecycle.
