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
secret provisioning requiring explicit owner action/approval. Normal Laomedo sign-in is required for private access, as accepted by the owner.
The strict online-read policy remains proposed pending measured workflow review.

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
5. The native Windows app backend owns the private broker, vault adapter, reader
   and private registry/journal in-process. Its authenticated route constructs a
   non-serializable owner/session context and selects the connection. The broker
   resolves current generation and consent, then reads exact objects. Do not send
   private owner claims to the existing source/operation HTTP service. Those
   public-only services retain their public roots and have no private dispatcher.
   Test direct forged-owner requests there as refused, not as a trusted hop.
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
The owner accepted requiring normal Laomedo sign-in for private access on
2026-11-07. Final design review and actual session/persistence checks remain
necessary; no running preview configuration was changed.

## Pending requests, connections and navigation

The backend trusts its actual authentication dependency and local Windows host,
not a browser owner claim or a service token holder. Compromise of the same OS
user/backend process is excluded; remote authenticated requests still require
owner/session/generation admission. Private stores must not overlap any configured
public store, source allow-root or Agent mount. Unsupported Linux/container-hosted
backends refuse private access, rather than importing Windows credentials.

One Laomedo owner may connect several GitHub accounts. Each pending attempt has
its own request identity, expected replacement connection/generation and session.
Its authorizing/verifying/consent states are not connection-record states. A ready
connection is replaced only after successful verification and explicit consent.
Every failed/cancelled/expired attempt preserves its previous ready connection.

Draw.io cards use unique UI identifiers C01-C11 and error cards E01-E05. Pending
attempt transitions P01-P10, ready-connection transitions R01-R08 and navigation
N01-N17 are separately owned on their named pages. Story IDs GC01-GC10 below
reference these IDs; a story number is never a second identity for a UI card.
App registration, app installation and local read consent are separate actions.
The Install / manage app repositories control derives
`https://github.com/apps/APP-NAME/installations/new` from the trusted configured
app slug. Validate the slug and construct this exact HTTPS host/path; never accept
a browser-supplied target, query or redirect. GitHub owns account/repository
selection and installation permission checks. A private app is installable only
on the account that owns its registration; broader account support requires the
corresponding GitHub app visibility/installation policy.

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

Current evidence: source inventory, two bounded approach reviews and two canonical
specification/visual reviews. No implementation or real workflow is verified. First
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

## Story to editable-state coverage

| Story | Owning Draw.io states / transitions |
| --- | --- |
| GC01 browser connection | C01 no-app, C02 pending, C03 consent, C09 setup, C10 ready; P01/P03/P04/P05, N01/N02/N05 |
| GC02 explicit token | C06 secure token entry, E02 refusal; P02/P04/P05/P07 |
| GC03 cancellation/concurrency | C02/C03, E03 interrupted connection; P06/P07/P08/P09/P10 preserve previous ready |
| GC04 browser/app restart | C07 reauthorization, C08 crash recovery; P10, R05/R06, E05 unsupported auth |
| GC05 private discovery/files | C04 Skill selection, C05 locked Skill-files viewer; N03/N04, R01/R02 |
| GC06 revoke/rotate/disconnect | C10 ready, E04 incomplete vault removal; R03/R04/R05/R07/R08 |
| GC07 wrong identity/repository | E02 refused credentials, C11 empty installations/access, C05 locked view; P07, N05/N06 |
| GC08 exchange/refresh crash | C08, E03; P10, R06 |
| GC09 compatibility/errors | C04/C05 and E01-E05, no public/local fallback |
| GC10 takeover/profile/cleanup | E05 private auth refusal; owner/session guards on all transitions; unsupported profile use remains explicit |

Per-read online verification remains a proposed strict default with offline
refusal and measured latency. No asynchronous external revocation SLA is claimed.

## Corrected canonical review ledger

Full review at `c119de7`: Specification REVISE, Visual REVISE; all four original
images and the full substantive own-diff read. No implementation exists.

| Finding | Correction | Recheck status |
| --- | --- | --- |
| 251-S1 | Unique C01-C11/E01-E05 cards; story matrix derives links to state/transition IDs | Corrected, pending focused recheck |
| 251-S2 | Native Windows app backend owns private broker/vault/store in-process; public service cannot assert private owners | Corrected, pending focused recheck |
| 251-S3 | Separate pending-request, navigation and persisted/read transition authority P01-P10/N01-N17/R01-R08 | Corrected, pending focused recheck |
| 251-S4 | Registration vs installation vs read consent separated; manage-installation controls and verified-empty C11 | Corrected, pending focused recheck |
| 251-S5 | Shared-presenter E01-E05 for vault/token/ended-attempt/partial-removal/unsupported-owner failures | Corrected, pending focused recheck |
| 251-S6 | Pending request states are distinct from per-connection record states; multiple GitHub connections allowed for one app owner | Addressed clarification |
| 251-S7 | 32 combined refs, exact namespaces, bounded completeness and tag peeling, excess/truncation refusal | Addressed clarification |

Owner decisions now settled: local Windows first, separate specs worktree, no
existing app (prepare one-time setup), normal app sign-in for private access.
Actual app registration/secret entry and real browser acceptance remain undone.


## Deployment and recovery investigation

The maintained implementation guide, `docs/getting-started.md` (develop
`bb25013523e37fbb108b51638be171e879eb3883`, Terminal C), starts the Langflow app
with Windows `.venv/Scripts/python.exe` and Uvicorn's
`laomedo.integrations.langflow.viewer:create_app`. Docker hosts agent runners in
that recipe; the application itself is native. This establishes an existing
supported native deployment, not an observed running service. Its public preview
uses AUTO_LOGIN; private access requires a separately deliberate normal-sign-in
configuration. No current preview was reconfigured. Container-hosted application
private access is unsupported in this increment; no host credential bridge is
claimed.

GitHub documents first installation through the app's own Install App page and
its per-app installation URL, rather than the user's already-installed-app list:
[installing your own app](https://docs.github.com/en/apps/using-github-apps/installing-your-own-github-app)
and [sharing an app's installation URL](https://docs.github.com/en/apps/sharing-github-apps/sharing-your-github-app).
These references settle the proposed navigation target; actual first installation
and organisation permission behavior remain unverified until real acceptance.

All drawn buttons now carry an `actionRef` to their P/N/R transition authority.
The recovery review was expanded from individual missing labels to every control:
H01 provides distinct vault, incomplete-removal and normal-sign-in help; N09-N17
own help, replacement credential, new attempt, dismissal, retry removal, empty-list
cancellation, return and registration navigation. C11 Cancel discards only its
pending attempt. E04 retries local secret removal after generation fencing; it
never re-enables access. P07 distinguishes a declined GitHub callback from failed
credential verification. Static transition-reference coverage is supporting
evidence, not a runtime interaction test.

### Follow-up review scope

The recheck at `434a8c1` kept Specification and Visual at REVISE. S2/S5 were
verified in specification text only; S6/S7 were addressed. Surviving S1/S3 prompted
a whole-diagram identity/action audit instead of another isolated label patch.
S8 now has source-backed native deployment evidence above; S9 has official
first-install documentation. S10 has complete recovery targets and C11/E04 exits;
S11 has separate declined-callback handling. These corrections require a new
substantive design-readiness review; no approval is inferred from this ledger.
