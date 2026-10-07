---
title: GitHub account connection for mediated agent runs
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-07
applies_to: [laomedo]
supersedes: null
related: []
---

# GitHub account connection for mediated agent runs

This proposed contract records the user's choice in [specs #253](https://github.com/amadou-6e/specs/issues/253): browser-based GitHub sign-in is the default connection path, and explicit token connection is an alternative. Laomedo does **not** reuse, import, mount, or fall back to credentials from the host's `gh` session, Git Credential Manager, shell environment, or Git configuration. The connection is distinct from [Codex/Claude provider authentication](authentication.md) and from the [per-run mediated grant](github-write-mediation.md). No browser or token connection has been implemented or exercised yet.

## Connection modes and user control

| Mode | User-visible behavior | Credential handling |
| --- | --- | --- |
| Browser sign-in (default) | Laomedo opens GitHub's authorization flow; the user chooses an account and approves the requested access. Laomedo shows the verified account, available repositories, connection state, and how to disconnect or reconnect. | The broker completes and verifies the authorization exchange and retains its reusable credential outside disposable workspaces. A GitHub App user-access-token web flow is a candidate, not yet the selected implementation. |
| Explicit token | The user deliberately supplies a supported GitHub token to Laomedo, chooses its intended repository scope, and sees the verified account, permissions, expiry when available, and removal/rotation controls. Laomedo must reject unsupported, expired, wrong-account, wrong-repository, or insufficiently scoped tokens before a writable run. | The broker stores the token as a secret. It must not infer refresh capability for a user-supplied static token. Supported token classes, verification APIs, secure entry and custody require research before implementation. |

Neither mode authorizes a run merely by being connected. The user selects a connection and approves a repository-and-operation-specific run grant. The broker resolves that connection for the chosen owner, records a non-secret reference and credential generation, then gives the stage only a revocable capability to ask the [mediator](github-write-mediation.md) to perform permitted operations. GitHub permission is an upper bound; the narrower run grant, reviewed-issue publication rule, and separate workflow-file approval remain in force.

## Boundary and failure behavior

- A connection record identifies `connection_id`, Laomedo owner, mode, verified GitHub principal, verified repository access, credential reference/generation, expiry if known, and state (`ready`, `reauthorization_required`, `expired`, `revoked`, or `unavailable`). It contains no token, refresh secret, authorization code, or host credential path. Exact storage and callback schemas are still open.
- Browser authorization must bind the callback to the initiating Laomedo user and connection request, verify the resulting GitHub identity and access, and reject a mismatch. UI closure, broker restart, declined consent and revoked consent must have explicit recovery behavior; none silently selects another identity.
- Token entry must not echo into prompts, commands, traces, logs, issue bodies, PRs, flow exports, or agent-visible files. Verification must be read-only and scoped to the selected identity/repository before a write grant is issued. A removed or revoked token stops new grants and causes affected requests to fail closed; an already dispatched remote effect remains subject to the [Q16 uncertain-write rules](github-write-mediation.md#q16-effect-identity-and-uncertain-writes-proposed).
- Disconnect or credential replacement must make the mediator refuse new effects under the old connection generation, including effects requested by still-running stages. If denial cannot be verified, the connection reports incomplete revocation rather than success. The broker separately records whether the provider token itself was revoked; removing a Laomedo record is not proof of provider revocation. Other users' connections and unrelated runs remain unaffected.
- An unavailable broker, absent selected connection, failed verification, or insufficient permission is an authentication/authorization error, not a reason to use local `gh`, Git Credential Manager, `GH_TOKEN`, or any ambient Git credential helper. No opt-in host-credential flag is part of this design.

The exact GitHub browser authorization mechanism, token classes, local and hosted secret stores, callback transport, renewal policy, and permission-verification method remain open design work. [GitHub documents a GitHub App web application flow](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app) and [fine-grained token permissions](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens); these are research inputs, not evidence that Laomedo implements either mode. This contract must not be read as approval to connect a personal account for an experiment.

## Validation path

The separate [account-connection exercise #108](https://github.com/amadou-6e/laomedo/issues/108) first freezes a protocol and tests both modes with synthetic credentials and a fake GitHub-compatible endpoint. It must check identity/callback binding, wrong account/repository/scope, token expiry and revocation, broker restart, disconnect, cross-user access, secret absence from agent/tool environments and traces, and an ambient-credential negative control. A later bounded disposable-repository connection may test the chosen real flow only after its credential custody and protocol are reviewed. Passing this exercise would not by itself prove [#104's](https://github.com/amadou-6e/laomedo/issues/104) live runner-loss write denial or full `git`/`gh` parity under [#100](https://github.com/amadou-6e/laomedo/issues/100).
