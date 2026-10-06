---
title: Host approval authority proposal
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-06
applies_to: [laomedo]
supersedes: null
related: []
---

# Host approval authority proposal for #95

`LocalGrantAuthority.issue()` is a zero-turn fixture, not a human approval
boundary. A process running as the same Windows user can call it directly and
skip the CLI's typed confirmation. The user's SID identifies the process owner;
it does not prove that the user reviewed a particular grant.

For the local Windows pilot, put the issuer and one-use grant ledger in a
service running under a dedicated non-administrator identity. Its executable,
configuration, credential public keys, and ledger must be writable only by that
identity and administrators. An ordinary process may submit a pending request,
but cannot mint a grant or alter its approval record.

The operator must review the canonical request before approval: work URL and
body digest, prerequisite content digest, graph identity, runner identity,
workspace scope, expiry, timeout, and turn limit. The service binds a fresh
challenge and nonce to that exact request digest. It verifies a registered
WebAuthn assertion, including signature, credential ID, relying-party ID hash,
origin, user presence and user verification, challenge, expiry, and applicable
signature counter checks. Challenge consumption and grant creation are atomic.
Changing any reviewed field requires a new ceremony.

Denial, expiry, service crash, lost response, and inconclusive lookup do not
authorize dispatch. Replays fail without consuming a fresh approval. A caller
cannot obtain approval by editing a local confirmation string or copying a
grant file. The authority records request and grant IDs and a redacted outcome;
private credentials and assertions do not enter agent-visible files or PRs.

Credential-free tests should first demonstrate the existing same-user bypass,
then exercise request binding, replay, expiry, denial, and crash windows using
fixture keys and a separately owned issuer process. A later test needs an actual
Windows service identity, ACL audit, and operator authenticator ceremony. Until
those tests pass, #95 remains open and the existing issuer stays labeled as a
fixture. Administrator or service compromise and a human approving misleading
request content are outside this local boundary.

The proposed ceremony follows the [Windows WebAuthn API](https://learn.microsoft.com/en-us/windows/win32/api/webauthn/),
[Windows service security guidance](https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights),
and [WebAuthn assertion verification requirements](https://www.w3.org/TR/webauthn-3/#sctn-verifying-assertion).
