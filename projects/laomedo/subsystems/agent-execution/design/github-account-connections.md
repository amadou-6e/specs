---
title: Local GitHub connections and private Skill reads
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-11-07
applies_to: [laomedo]
supersedes: null
related: []
---

# Local GitHub connections and private Skill reads

[SC01-SC10](../contract/github-account-connection.md#private-skill-source-increment-sc01-sc10)
own observable requirements. [Editable interaction states](github-account-connections.drawio)
own new connection controls and transitions. [Skill source selection](../../skill-registry/design/skill-source-selection.md)
retains existing public/local controls. All new states are PROPOSED / NOT IMPLEMENTED.

Owner decisions: single-user local Windows first; use a dedicated specs worktree
to preserve unrelated edits. The owner corrected the earlier registration answer:
no GitHub App exists. Prepare one-time app setup, with actual registration and
secret provisioning requiring explicit owner action/approval. AUTO_LOGIN/setup
and strict online-read policy are proposed, not owner-accepted defaults.

## Boundaries and object vocabulary

| Boundary | Responsibility | Vocabulary |
| --- | --- | --- |
| App session to broker | Derive actual owner/session and protect same-origin mutations | ConnectionOwner, ConnectionSession |
| Broker lifecycle | Verify principal, retain consent, serialize generation/refresh/disconnect | GitHubConnectionService; connect, confirm, authorize_read, reconnect, disconnect |
| OAuth integration | Maintained OAuth client, PKCE/state, fixed callback | GitHubOAuthClient; begin, complete, refresh |
| Host vault | Explicit Windows keyring, no fallback or public serialization | WindowsCredentialVault; store, load, remove |
| Repository permission | Current principal/repository verification with no write surface | GitHubRepositoryAccess; verify |
| Private object reader | Exact refs/commit/tree/blob reads with existing source limits | GitHubRepositoryReader; refs, entries, read_blob |
| Private registry/journal | Provenance and owner/connection namespace, never shared public root | PrivateSkillAccess; inspect, history, compare |

These names specify proposed responsibility, not delivered objects. A public
ConnectionReference is not an authorization token. Canonical Pydantic records
belong to module models.py; no duplicated user/run model or secret-bearing
settings projection. Use existing source and inspection validators after explicit
private admission. No general plugin registry or cross-domain utilities.

## Flow and persistence

1. Connection manager rejects unsupported deployment/authentication before opening
   GitHub. Existing public browsing is unaffected; no app setting is changed.
2. Begin records an expiring pending request plus session binding; state and PKCE
   verifier stay server-side. Callback is exact and one-use, with no request logging.
3. Verify GitHub principal and show account plus accessible repository choices.
   Confirm records repository-specific read consent; never auto-select all access.
4. Commit secrets to vault and non-secret metadata to the broker journal through
   recoverable prepare/commit markers. Do not leave an apparently ready row after
   a partial write. New attempts cannot destroy an existing ready connection.
5. Discovery receives authenticated owner context from the app and an opaque
   connection ID. The broker resolves current generation and validates requested
   repository against consent, then reads exact objects with no child credentials.
6. Private bundles and provenance remain in the private namespace. UI inspection,
   history and operation paths route there explicitly; shared readers cannot
   discover it by ID/hash alone. No automatic export to an Agent registry.
7. Each private response has a bounded admission lease. Recheck owner/session and
   generation before returning bytes; disconnect/refresh cannot resurrect a late
   response. The browser clears scoped private query data on disconnect/logout.
8. Refresh/disconnect use one per-connection serialization boundary and durable
   intent. Uncertain refresh requires reconnect. Restart invalidates pending login
   and recovers ready metadata only if its vault transaction is consistent.

Store namespace is owner/connection, not solely URL or hash. Generation-scoped
raw caches cannot authorize access. Old immutable private revisions can be viewed
under a new generation only after current repository consent/access verification;
never silently rewrite their hash, commit identity or provenance.

## Alternatives and unresolved facts

Host gh/GCM/env reuse violates the selected contract. Token-only omits the browser
mode. A custom Git credential bridge is unnecessary unless a concrete object-read
gap is demonstrated. GitHub object APIs cover the current shallow head/tag source
shape; recursive truncation, annotated tags, binary bytes and limits still need
regression and real verification. This is not proof of arbitrary Git equivalence.

Assess maintained OAuth/HTTP and OS-keyring libraries before selecting versions;
do not hand-roll protocol or credential encryption. GitHub web flow needs a local
operator-provisioned app secret, never a package-embedded shared secret. Device
flow/hosted broker are not implicit alternatives. No registration exists; prepare a concrete read-only registration configuration
for owner approval rather than assuming an app or borrowing another client ID.
Exact callback matching and its read-only app permissions still require inspection.

A private-only authentication gate preserves auto-login public previews but refuses
private connection until a supported owner session is deliberately configured.
It does not by itself solve the usability decision of requiring another app login.
Owner confirmation and final design review remain necessary.

## Required story matrix

| ID | Observable story | Evidence needed before delivery claim |
| --- | --- | --- |
| GC01 | Connect browser, verify account, select repositories | Real GitHub authorization/return, ready account, no secrets in responses |
| GC02 | Add explicit supported token and select read scope | Real token via secure UI, verified principal/repository; classic/expired refusal |
| GC03 | Cancel/decline/expire/concurrent sign-in | Ready connection preserved; obsolete callback rejected, no wrong account selected |
| GC04 | Restart browser/profile and app/broker | Actual session/profile restoration and authenticated state, expired-session recovery |
| GC05 | Discover private URL and view selected immutable files | Exact real refs/bytes/hash; no Agent request or write |
| GC06 | Disconnect/rotate/revoke during cold/warm reads | No late content release; view/history/binary/editor/runner boundaries denied, measured latency |
| GC07 | Wrong account/repository/owner/session | No cross-owner cache or ID-based disclosure; source text preserved |
| GC08 | Crash during callback/refresh/vault update | Explicit expired/reauthorization state, no replay or lost existing ready connection |
| GC09 | Public/local compatibility and diagnostics | Existing paths usable, missing access distinct from empty source, copy/redaction verified |
| GC10 | Human takeover, concurrent profile and cleanup limits | Supported paths actually tested; unsupported use refused/documented; unrelated accounts untouched |

Current evidence: source inventory and two bounded approach reviews only. First
review skipped required instructions; recheck read them and confirmed corrected
mechanisms but left design/owner gates open. No real connection, browser state or
private repository read has been performed. Prototype #108 remains historical.

## Upstream references

- [GitHub App web flow, PKCE and access intersection](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app).
- [Callback registration](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/about-the-user-authorization-callback-url).
- [Refresh semantics](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens).
- [Git refs](https://docs.github.com/en/rest/git/refs), [trees](https://docs.github.com/en/rest/git/trees), [blobs](https://docs.github.com/en/rest/git/blobs).
- [Windows OS-keyring support](https://keyring.readthedocs.io/en/latest/).

Checked 2026-11-07. Upstream documentation establishes API intent, not this
implementation's acceptance or permission to copy existing credentials.
