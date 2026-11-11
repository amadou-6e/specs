---
title: GitHub account connections and scoped repository access
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-11-07
applies_to: [laomedo]
supersedes: null
related: []
---

# GitHub account connections and scoped repository access

This proposed contract records the user's choice in [specs #253](https://github.com/amadou-6e/specs/issues/253): browser-based GitHub sign-in is the default connection path, and explicit token connection is an alternative. Laomedo does **not** reuse, import, mount, or fall back to credentials from the host's `gh` session, Git Credential Manager, shell environment, or Git configuration. The connection is distinct from [Codex/Claude provider authentication](authentication.md) and from the [per-run mediated grant](github-write-mediation.md). No production browser or token connection has been implemented or exercised; [#108's draft synthetic probe](https://github.com/amadou-6e/laomedo/pull/110) is not a live GitHub login.

## Connection modes and user control

| Mode | User-visible behavior | Credential handling |
| --- | --- | --- |
| Browser sign-in (default) | Laomedo opens GitHub's authorization flow; the user chooses an account and approves the requested access. Laomedo shows the verified account, available repositories, connection state, and how to disconnect or reconnect. | The broker completes and verifies the authorization exchange and retains its reusable credential outside disposable workspaces. A GitHub App user-access-token web flow is a candidate, not yet the selected implementation. |
| Explicit token | The user deliberately supplies a supported GitHub token to Laomedo, chooses its intended repository scope, and sees the verified account, permissions, expiry when available, and removal/rotation controls. Laomedo must reject unsupported, expired, wrong-account, wrong-repository, or insufficiently scoped tokens before a writable run. Broad-scope classic tokens are refused by default; any exception needs a separately reviewed justification and explicit user approval. | The broker stores the token as a secret. It must not infer refresh capability for a user-supplied static token. Supported token classes, verification APIs, secure entry and custody require research before implementation. |

Neither mode authorizes a run merely by being connected. The user selects a connection and approves a repository-and-operation-specific run grant. The broker resolves that connection for the chosen owner, records a non-secret reference and credential generation, then gives the stage only a revocable capability to ask the [mediator](github-write-mediation.md) to perform permitted operations. GitHub permission is an upper bound; the narrower run grant, reviewed-issue publication rule, and separate workflow-file approval remain in force.

The trusted run approval and durable mediator grant both carry that selected
`connection_id` and credential generation. The approval owner checks that the
connection belongs to the user and covers the repository; the mediator checks
that the generation is still current before a **new** effect. The
credential-owning transport resolves only that same connection/generation,
never an ambient or unrelated token. Rotation or disconnect makes old grants
unusable for new effects. A remote effect already dispatched before revocation
may remain uncertain under Q16; generation checks do not undo it.

## Boundary and failure behavior

- A connection record identifies `connection_id`, Laomedo owner, mode, verified GitHub principal, verified repository access, credential reference/generation, expiry if known, and state (`ready`, `reauthorization_required`, `expired`, `revoked`, or `unavailable`). It contains no token, refresh secret, authorization code, or host credential path. Exact storage and callback schemas are still open.
- Browser authorization must bind the callback to the initiating Laomedo user and connection request, verify the resulting GitHub identity and access, and reject a mismatch. UI closure, broker restart, declined consent and revoked consent must have explicit recovery behavior; none silently selects another identity.
- Token entry must not echo into prompts, commands, traces, logs, issue bodies, PRs, flow exports, or agent-visible files. Verification must be read-only and scoped to the selected identity/repository before a write grant is issued. A removed or revoked token stops new grants and causes affected requests to fail closed; an already dispatched remote effect remains subject to the [Q16 uncertain-write rules](github-write-mediation.md#q16-effect-identity-and-uncertain-writes-proposed).
- Disconnect or credential replacement must make the mediator refuse new effects under the old connection generation, including effects requested by still-running stages. If denial cannot be verified, the connection reports incomplete revocation rather than success. The broker separately records whether the provider token itself was revoked; removing a Laomedo record is not proof of provider revocation. Other users' connections and unrelated runs remain unaffected.
- An unavailable broker, absent selected connection, failed verification, or insufficient permission is an authentication/authorization error, not a reason to use local `gh`, Git Credential Manager, `GH_TOKEN`, or any ambient Git credential helper. No opt-in host-credential flag is part of this design.

For the wider mediated/hosted target, the browser mechanism, supported token
classes, secret stores, callback transport and renewal policy remain open design
work. The SC01-SC10 draft below proposes a narrower local source-read increment;
it does not establish production implementation or resolve hosted deployment. Whether GitHub's
device authorization flow satisfies the browser-default experience on a
remote or headless host is explicitly **undecided**; no device-flow fallback
is selected here. [GitHub documents a GitHub App web application flow](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app) and [fine-grained token permissions](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens); these are research inputs, not evidence that Laomedo implements either mode. This contract must not be read as approval to connect a personal account for an experiment.

## Validation path

The separate [account-connection exercise #108](https://github.com/amadou-6e/laomedo/issues/108) first freezes a protocol and tests both modes with synthetic credentials and a fake GitHub-compatible endpoint. It must check identity/callback binding, wrong account/repository/scope, token expiry and revocation, broker restart, disconnect, cross-user access, secret absence from agent/tool environments and traces, and an ambient-credential negative control. A later bounded disposable-repository connection may test the chosen real flow only after its credential custody and protocol are reviewed. Passing this exercise would not by itself prove [#104's](https://github.com/amadou-6e/laomedo/issues/104) live runner-loss write denial or full `git`/`gh` parity under [#100](https://github.com/amadou-6e/laomedo/issues/100).

## Private Skill source increment (SC01-SC10)

Tracking: [Laomedo #251](https://github.com/amadou-6e/laomedo/issues/251),
[specs #410](https://github.com/amadou-6e/specs/issues/410). Owner selected
single-user local Windows on 2026-11-07, then corrected the registration answer:
no GitHub App exists yet. Include one-time registration setup; do not create or
change an app without explicit approval. The following
is a draft concrete increment, not an implemented or accepted connection flow.
Its [mechanism and acceptance matrix](../design/github-account-connections.md)
and [editable UI states](../design/github-account-connections.drawio) are reviewed
before implementation. Existing mediated-run restrictions above remain in force.

### SC01: Supported owner and deployment

A private connection belongs to the actual authenticated local profile on a
single-OS-user Windows installation. Profiles select setups, not separate Windows
users or hosted tenants. The owner requires a PIN for profile entry/switching and
no separate administrator workflow; see the proposed [local profile design](../design/local-profiles.md).
One profile may have multiple separately selected GitHub
connections; each has its own principal, generation, consent and private store. Every private route resolves the actual authenticated app
principal, never an owner supplied in JSON or a shared service bearer token.
The private broker, vault adapter, object reader and private store are owned by
the native Windows Langflow backend process. Its authenticated route dependency
constructs an in-process owner/session context; no private request is sent to the
existing public source or operation service, and no shared bearer token can mint
that context. Direct calls to those public services never reach private stores.
A malicious process running as the same Windows user remains outside this trust
boundary. The owner-selected supported setup requires AUTO_LOGIN disabled and an active ordinary local
profile resolved by upstream authentication; private routes refuse unknown, auto-login, API-key-only
or mismatched owner/session contexts. Public/local features remain unchanged.
Do not change a running app's login configuration automatically. The owner accepted normal Laomedo sign-in for private access on 2026-11-07;
a different local-owner session design requires explicit review. Hosted, remote and multi-user isolation are unsupported.

Private browser access additionally uses a server-revocable session bound to the
upstream-authenticated owner. Reuse normal Laomedo login; do not create another
account/password system. The owner selected following the normal app login
lifetime, including valid refresh and restart, on 2026-11-07. Refresh must not
create or resurrect a revoked/missing/expired private session. Logout revokes the
current browser's private session before completing; it does not silently revoke
unrelated profiles or disconnect the GitHub connection. A surviving upstream JWT
alone cannot restore private access. A missing/inconsistent private session under
an otherwise valid app login offers explicit Sign in again recovery: sign out,
then open the existing login page. If sign-out is unconfirmed, keep private data
locked and offer retry; never claim completion. See C13/C14 and N18/N19 in the
editable design. Actual behavior remains subject to the real browser story gate.

### SC02: Browser-default and deliberate token entry

Use an explicitly operator-configured GitHub App's web authorization flow with
S256 PKCE, unpredictable one-use state and an exact registered loopback callback.
No device-flow fallback or embedded shared app secret. Bind the pending request
to the initiating owner, browser session, request identity and generation. Verify
the returned principal and show it before committing repository consent. Declined,
cancelled, expired, wrong-session, duplicate or replayed callbacks cannot replace
a connection. The callback never reports success from merely receiving a code. Authorizing,
verifying and awaiting-consent are states of a separate pending request, not a
ready connection record. Cancelling or failing that request discards provisional
credentials while preserving any previous ready connection unchanged.
A pending request is invalidated on broker restart; the existing ready connection
survives a new failed/cancelled connection attempt.

The alternative accepts deliberately entered fine-grained personal access tokens;
classic tokens and unverified token classes are refused. Verify the principal and
selected repository reads. Report only scope/expiry facts actually established by
GitHub, not assumed from a prefix or successful public read. A fine-grained token
may have upstream rights beyond this feature; Laomedo grants source reads only.
A static token is replaced explicitly and is never treated as refreshable.

### SC03: Host-only credential custody

Store app secret, access credential and refresh credential in an explicitly chosen
Windows OS keyring backend. Null/plaintext/fallback backends fail closed. Public
records contain only opaque connection identity, principal, mode, generation,
selected repository identities, state and verified expiry when available. Keep
secrets out of settings serialization, graphs, URLs, argv, ordinary child-process
environments, logs, traces, agent files, browser storage and exports. Secure
same-origin token entry clears the DOM after submit/cancel; never echo it in
errors. The host vault is not a sandbox against other code running as the same
Windows user. Do not import host gh/GCM/environment/Git credentials.

### SC04: Repository read consent is distinct authority

App registration and installation are distinct. Provide an explicit Install /
manage app repositories action opening the trusted configured app slug's
`https://github.com/apps/APP-NAME/installations/new` page. Validate the slug and
construct the exact HTTPS host/path; no browser-supplied target is accepted. A
verified empty accessible-repository list shows a distinct empty state, no granted
consent, and that recovery action; a failed permission check is not an empty list.
After principal verification, show accessible repositories and let the owner
consent to explicit repository content reads. GitHub App access is the
intersection of user and app installation/repository access; authorization alone
is not installation consent. Bind every source read to owner/session,
connection/current generation and the consented repository identity. Browser or
node data carries a non-secret connection reference, never credentials or an
asserted owner. Read consent authorizes discovery, exact revision resolution and
private file/history viewing; it grants no Agent run, repository write, Issue/PR
operation or Git publishing permission.

Owner decision (2026-11-11): consent binds both the numeric repository identity
and its confirmed owner/name location. A rename or transfer stops private access,
including retained history, until the owner deliberately reconnects and confirms
the repository again. Do not follow redirects or silently update stored consent.
A matching old name with a different numeric identity remains refused. If renewal
cannot revalidate any consented repository at its confirmed location, require
reauthorization of the connection rather than partially restoring its authority.

### SC05: Private store access, not cache-only separation

Private imported bytes, provenance, index and journal live outside all existing
public/shared registry roots and runner mounts, in an owner-and-connection-owned
namespace. Raw repository object caches are additionally generation scoped.
Bundle hashes and exact revision identities retain their meaning; identity is not
read permission. Every viewer, binary/image, history/diff/compare and applicable
editor/operation route authorizes the stored private provenance before reading
and again before releasing a response. Never publish private-origin content into
the shared registry as a side effect of browsing or editing.

A public-only CLI or runner cannot open the private store through a graph field.
An unavailable public pin does not reveal whether a private copy exists.
Independently authorized public bytes remain readable even when their hash equals
a private bundle. Future private materialization must have its own explicit
admission and preserve provenance; source consent alone does not authorize it.
Do not claim private Agent execution from private browsing acceptance.

### SC06: Revalidation, offline behavior and disconnect

Before each private user read, including warm-cache history/view, verify the
current GitHub principal and repository access within a bounded deadline.
Offline/unavailable verification refuses private content; it does not serve stale
permission from cache. This incurs network latency and API rate cost, which must
be measured and disclosed. This is the proposed fail-closed implementation policy; its measured latency
and final workflow remain subject to requesting-owner acceptance before merge.

Disconnect fences new requests before secret deletion, advances generation and
invalidates open private-view queries; late responses recheck generation and
cannot repopulate them. Already delivered browser bytes and lawfully materialized
run files cannot be recalled. Retained private audit bytes are not continuing
access authority. Rotation permits retained history only after current-generation
repository reauthorization; old in-flight requests remain refused. External
revocation is checked at the next requested private read, not a claimed background
SLA. Measure elapsed check/denial time. Local deletion does not prove GitHub token
revocation; distinguish those facts and report incomplete vault deletion.

### SC07: Refresh and crash outcomes

One broker owns refresh per connection. Serialize attempts and commit credential
replacement with a durable in-progress marker and generation fencing. A crash or
lost response after refresh may have consumed the old refresh token: mark
reauthorization required rather than replaying it. Pending sign-in and refresh
recovery cannot silently use another account. Broker/app restart restores ready
metadata only with the matching vault material and supported session ownership.
Cancellation stops local waiting and invalidates pending state; it does not claim
to revoke consent already granted at GitHub.

### SC08: Bounded nonexecuting private repository reads

For private GitHub sources, the proposed reader uses in-process authenticated
GitHub refs/commits/trees/blobs GETs, keeping secrets out of Git subprocesses.
Public Git and admitted local readers retain their existing guards. Enumerate
only heads/tags, bind exact commits and peel annotated tags with a finite bound.
Refuse truncated inventories, unsupported object modes, links, submodules,
unsafe paths, oversized blobs/bundles or exhausted total deadline. Preserve the
existing source/file/cache limits and immutable bundle hashing. At most 32 combined
heads/tags are admitted; bounded enumeration must establish completeness and
refuse excess, truncation or unfinished pagination instead of hiding choices.
List only the exact heads/ and tags/ namespaces, and peel annotated tags with a
finite depth/visited-identity bound before accepting a commit. Do not follow
provider redirects or forwarded download URLs with credentials. No checkout,
hook, script, executable or submodule operation is needed for source reads.
This is an explicit private transport extension, not arbitrary Git history support.

### SC09: Descriptive failure and recovery

Use the shared presenter and producer catalogue coverage for missing connection,
reauthorization, unavailable broker, refused repository and bounded/network read
failure. Preserve source text and exact selected pins. Ambiguous GitHub 404 means
access could not be confirmed, never that the repository exists or is private.
Recovery opens the implemented connection manager, reconnect or repository
selection control. Never retry a write or start an Agent as recovery. Private
connection failure never falls back to anonymous, local or another account.

### SC10: Acceptance boundary

Both real connection modes, real private HTTPS discovery/files, browser profile
restoration, app/broker restart, logout/expired session, human takeover, cancelled/
declined/expired/crashed/concurrent connection attempts, expiry/rotation/revocation,
wrong identity/org/installation/repository, cold/warm-cache isolation and all
private read surfaces require actual browser/resource evidence. Mark unsupported
profile concurrency or hosted behavior as constraints. Record revision, timing,
cleanup, safe diagnostics and unknowns; do not use fixtures as real acceptance.
No model turn or repository write is needed to prove these browsing stories.
Requesting-owner final workflow inspection gates implementation merge.
