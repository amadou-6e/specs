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

The protected service must also own the launch capability. A caller that can
invoke Docker or pass a fabricated `grant_authority` callable directly to the
stage can bypass an otherwise protected issuer. In the production route, the
agent and ordinary same-user client must not have direct access to the Docker
Engine, the issuer ledger, or a launch entry point that accepts caller-supplied
authorization. The service accepts only the reviewed request and grant
reference, performs the final source and stage checks, consumes the grant, and
dispatches the stage itself. The existing injectable local launcher remains a
test fixture until that route and OS access boundary are exercised.

The registered public key and issuer code are trust anchors. The ledger's
mutable one-use state also needs integrity protection: rechecking a valid
signature cannot detect a reset `redeemed_at` value or a duplicate grant row
carrying the same approved assertion. The service must own challenge creation,
approval state, grant creation, and atomic one-use redemption. A same-user
process must be unable to edit or roll back those records. An independently
protected monotonic consumption record could replace a protected ledger, but
an unprotected ledger alone cannot enforce one use.

The protected service must display the canonical request itself before it
starts the authenticator ceremony: work URL and body digest, prerequisite
content digest, exact task digest, graph identity, runner identity, workspace
scope, expiry, timeout, and turn limit. The protected launch route recomputes
the task digest from the submitted prompt and refuses a mismatch, even though
this may consume the one-use grant before dispatch. The Windows Hello or
security-key prompt does not
display these fields. A ceremony started by an ordinary caller, or one whose
displayed request differs from the signed request, cannot authorize a grant.
The service binds a fresh challenge and nonce to that exact request digest.
It verifies a registered WebAuthn assertion, including signature, credential
ID, relying-party ID hash, exact origin, user presence and user verification,
challenge, expiry, and applicable signature counter checks. Redemption must
reverify the stored assertion against the protected registered key and the
stored canonical request. Challenge consumption and grant creation are atomic.
Changing any reviewed field requires a new ceremony.

The initial implementation accepts ES256 only. A zero signature counter is
permitted only when both the stored and new counters are zero; otherwise the
new counter must be strictly greater. A real Windows ceremony must pin the
service's RP ID, exact `clientDataJSON.origin`, credential ID, algorithm and
user-verification policy before this design is activated. The native
[`WEBAUTHN_CLIENT_DATA`](https://learn.microsoft.com/en-us/windows/win32/api/webauthn/ns-webauthn-webauthn_client_data)
structure receives client-provided JSON, so this proposal cannot infer a
platform-generated origin. A fixture value is not a production pin. The
service must verify the exact chosen values in both approval and redemption.

On Windows, an SCM service cannot directly show an operator window from session
0. The local implementation must therefore either run a persistent interactive
broker under the dedicated protected account or use a service-controlled helper
in the operator's session. A helper cannot return a bare `approved` flag; the
service must supply the exact request to display, initiate the challenge, and
verify the resulting assertion. The interactive route, its process identity,
and its ability to resist a same-user caller starting an unreviewed ceremony
remain an acceptance gate, not an assumed property of a Windows service.
See [Microsoft's interactive-services guidance](https://learn.microsoft.com/en-us/windows/desktop/Services/interactive-services).

Denial, expiry, service crash, lost response, and inconclusive lookup do not
authorize dispatch. Replays fail without consuming a fresh approval. A caller
cannot obtain approval by editing a local confirmation string or copying a
grant file. The authority records request and grant IDs and a redacted outcome;
private credentials and assertions do not enter agent-visible files or PRs.

Credential-free tests should first demonstrate the existing same-user bypass,
then exercise request binding, ledger tampering and rollback, replay, expiry,
denial, and crash windows using fixture keys. A later test needs an actual
Windows service identity, ACL audit, protected operator display and real
authenticator ceremony. Until those tests pass, #95 remains open and the
existing issuer stays labeled as a fixture. Administrator or service
compromise and a human approving misleading content actually shown by the
protected display are outside this local boundary.

The proposed ceremony follows the [Windows WebAuthn API](https://learn.microsoft.com/en-us/windows/win32/api/webauthn/),
[Windows service security guidance](https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights),
and [WebAuthn assertion verification requirements](https://www.w3.org/TR/webauthn-3/#sctn-verifying-assertion).
