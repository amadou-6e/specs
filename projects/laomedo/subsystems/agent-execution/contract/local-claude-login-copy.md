---
title: Local Claude login reuse
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-25
applies_to: [laomedo]
---

# Local Claude login reuse

The owner authorises login-only duplication for the single-user local Docker
prototype. This follows the local Claude subscription decision; it does not
permit copying sessions, memories, settings, an entire profile or API-billing
credentials. No login material enters graphs, model tools, logs or repository
history. Host and runner sign-in are distinct observations.

The trusted host runner-service configuration opts in with
`mirror_host_claude_login: true`; it is disabled by default and valid only for
Claude. Startup only enables a fixed opt-in environment flag; it does not copy login
material while holding the startup lock or delay its cancellable startup identity.
For asynchronous Start/Fresh, reserve the request identity and send the acknowledgement
before copying in the worker, before model dispatch. A slow copy must not delay that
acknowledgement. Copy failure is retained against that run. Synchronous Fresh and
Resume copy before dispatch; they do not promise an early acknowledgement. Status, Cancel and publication do not mirror credentials.
Browser/model inputs choose neither source paths, commands nor destinations.

The host remains the refresh owner. Copy only the current access credential,
expiry and native subscription/scope metadata to the labelled dedicated local
profile. Do not duplicate its rotating refresh credential. The runner cannot
refresh the host's duplicate independently. Normal host Claude usage refreshes
its own login; later graph requests pick up that current credential automatically.
If the host access credential has expired, report that fact before dispatch;
this is not evidence that the host subscription is unavailable, and does not
justify copying an entire profile or blindly repeating an uncertain execution.

Validate the effective Docker endpoint before reading the host credential.
Respect Docker context precedence, pin the validated endpoint explicitly for all
subsequent Docker calls, and remove context/host overrides from their environment.
Refuse TCP endpoints including loopback tunnels, SSH endpoints and remote named
pipes. Only a local named pipe or local Unix socket is permitted. Each Docker
copy step has a20-second deadline. Startup cancellation never waits for copying;
a prepared task cancelled during copying must not dispatch a model afterwards. Write only to the trusted labelled Claude volume, through a
network-disabled helper with stdin transfer, private file permissions and atomic
replacement. Never place credential values in command arguments or environment.
The renderer/catalogue explain missing host login, expiry or copy failures with
safe codes. Existing uncertain outcomes must still be checked before new work.

Verification separates actual host/runner sign-in checks, actual no-skill Agent
execution and internal tests of opt-in, redaction, refresh ownership, endpoint
selection and dispatch ordering. CLI sign-in status alone is not inference proof.
