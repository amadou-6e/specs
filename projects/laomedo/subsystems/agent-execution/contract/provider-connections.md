---
title: Provider connections in Settings
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-11-16
applies_to: [laomedo]
supersedes: null
related: []
---

# Provider connections in Settings

Owning proposal: [specs #425](https://github.com/amadou-6e/specs/issues/425).
This is a draft for owner review, not implementation authorization. The owner
requested a login flow in Settings, a list of provider connections and a provider
type choice when connecting. On 2026-11-16 the owner confirmed multiple account
connections and explicit selection between them. Detailed lifecycle and provider
enablement below remain draft proposals unless already governed by the
authentication contract. Existing authentication isolation and revocation
requirements continue to apply.

The [editable workshop](../design/provider-connections.drawio) owns screen states,
control labels, interaction identifiers and transitions. Its story rows are the
canonical UI proposal. [Design notes](../design/provider-connections.md) index that
workshop and record provider research and unresolved enablement decisions. This
contract owns connection identity, custody and dispatch semantics; it does not
replace the broader [authentication contract](authentication.md).

## PC-01 - List saved connections, not provider types

Settings > Providers lists connections owned by the active local profile.
Provider type identifies the integration (Codex, Claude or OpenCode); a connection
identifies one explicitly established credential context for that integration.
Multiple connections of the same type may coexist (owner-confirmed 2026-11-16). Display a label, type,
authentication method, verified account/workspace when supplied by the provider,
and current observed connection status. A user label never proves identity;
API-key methods need not supply an account name. Never invent identity or
entitlements from a filename, label, model catalogue or successful login alone.
Loading, empty and failed reads are distinct; failed reads must not imply deletion.

## PC-02 - Explicit connection establishment

Add provider opens provider-type selection before any login process starts.
A type exposes only authentication routes supported by the installed adapter,
pinned provider version and deployment. An unavailable route explains the missing
prerequisite without reading ambient credentials or silently selecting another
method, account, provider or billing source. Type selection is not credential
consent. Continue starts the selected route exactly once per admitted attempt.
Native sign-in remains provider-owned; Laomedo must not imitate a provider login
page or collect provider passwords. Supported API-key entry is explicitly labelled
with its separate billing basis and uses a masked field, not a fake browser login.

An attempt is bound to local profile, connection candidate, provider type,
authentication route, private runtime/profile and lifetime. Only matching native
completion or a validated one-use callback may stage credentials. A callback is not
proof of success: verify the selected route's authenticated state, then commit
connection metadata and private credential reference together. Cancellation, expiry,
logout and an invalidated lease fence late completion. No duplicate launch on polling or
page refresh. An interrupted attempt is reconciled or reported as expired; restarting
Laomedo never blindly replays login. An uncertain local save must be reconciled against
the committed admission index before retrying; never report an unchanged connection
without confirmation. Routine token rotation does not advance the saved connection
identity generation. Superseded and crash-left unadmitted credential copies are fenced
and scrubbed by the owning runtime, without remotely revoking a grant shared with a
committed revision. Provider-side revocation of superseded grants remains unconfirmed unless separately observed through a supported revoke-and-recover operation; local scrubbing never claims remote logout.

## PC-03 - Credential ownership and isolation

Store secrets only in host/native custody outside repositories and tool mounts,
scoped to the local profile and opaque connection ID. Native-provider profiles
are dedicated per connection where the official client owns authentication; do
not extract or copy its login into a different client. Host IDE/CLI credentials
are not imported automatically. Existing explicitly authorized development-only
mirroring remains separately scoped and is not evidence of this Settings feature.

Local graph and assistant bindings select an opaque compatible connection ID,
separate from the host-only credential_ref. Export omits the private local binding;
import requires explicit rebinding. Neither export nor prompts carry credential_ref,
secrets, login paths or executable login commands. Dispatch
checks profile ownership, provider compatibility and connection generation before
borrowing a credential. No fallback to another connection or global active
account. An unavailable selected connection yields a recoverable connection error.
A retained native conversation remains pinned to its connection and identity;
account replacement cannot silently resume it under a different principal.
Native controller credentials must not become available to model tool processes;
existing isolation and release gates remain required.

Use distinct generations: `connection_generation` advances only on reconnect, key
replacement or disconnect and pins saved-connection dispatch and retained identity.
The broker advances `credential_generation` on token rotation; record it for the
admitted controller/turn and incident review. Routine renewal preserves the
connection pin. Authentication lifecycle step 4 still governs controller-token
replacement between completed turns.

## PC-04 - Status and readiness

Reuse the canonical auth_state values from authentication.md: ready, refreshing,
reauthorization_required, expired, revoked and unavailable. The UI maps them to
Connected, Checking, Sign in again (native/browser), Update key (API) or Unavailable; it does not invent another
credential state machine. Disconnecting, Cleanup required and Removed describe
local removal progress. Connecting/verifying belongs to a bounded attempt;
read/check activity does not create another connection. Connected means successful
route-specific authentication verification, not a successful inference or universal
model eligibility. Runner availability is a separate observation: a valid account
with an offline runner is not signed out. Catalogue loading uses the selected
connection, performs no model turn and never bills a hidden test request. If the
provider cannot verify credentials without inference, disclose that limitation;
do not claim a completed credential check.

Refresh belongs to the credential-owning broker/native client, serialized per
connection generation. Retryable transport failure does not discard a valid
credential or start sign-in automatically. An expired/revoked credential requires
explicit sign-in again and blocks new dispatch; no billing fallback.

## PC-05 - Reconnect, account changes and duplicates

Sign in again targets the selected connection. Preserve an existing working
credential until replacement is validated and committed atomically. Failure or
cancellation preserves the previous committed state. If the provider supplies a
stable principal and the staged account differs, refuse the reconnect with a safe
account-mismatch result and offer Add as new connection. Do not overwrite the
selected row or provide an account-replacement shortcut in this first increment.
Discard the refused attempt's staged credential through its native owner or host
custody; it must never become a reusable connection. Add as new connection starts
a fresh attempt. Existing sessions remain bound to their original identity.

When the same verified identity, provider type, route and workspace is already
connected, refuse a duplicate save and offer that existing connection; do not merge records
or replace its credential.
Where identity cannot be established (for example some API keys), do not pretend
to deduplicate; keep explicitly labelled independent connections. Equal email
addresses or user labels across types are not a canonical identity match.

For an API-key update, verify the provider workspace/account when that route
supplies it. A verified identity mismatch follows the wrong-account rule above.
If the route cannot establish identity, require explicit replacement confirmation
before committing: the account or API billing may change. Advance the connection
generation and refuse reuse of retained native sessions; new dispatch starts a
fresh session. Never swap a credential under a running controller. Cancel or failed
verification preserves the old committed key. The P10 update variant owns this
confirmation; it is not implied by pressing Connect for a new connection.

## PC-06 - Disconnect and removal

Follow the existing authentication contract's revoke/recover rule: disconnect
immediately fences new dispatch and refresh borrows, then cancels or quarantines
active controllers using this connection. Confirmation names the affected run
count before commit. Preserve partial trace/workspace evidence; cancellation is
not a successful run. The row stays Disconnecting until stop/quarantine and local
credential cleanup are confirmed. Unknown stop or cleanup leaves recovery visible,
not a false success. No alternate drain policy is selected by this proposal.

Remove only credentials owned by this connection, not the user's ordinary host
CLI login, another local profile, another provider connection or the external
account. Failed cleanup leaves a non-selectable Cleanup required row with Retry
cleanup. Confirm removal only after cleanup; an old callback cannot recreate it.
External/provider-wide logout or token revocation is a separate action/guarantee
and is not implied by Disconnect. A supplied API key may still exist upstream.
Profile logout blocks new use of its private records and pending callbacks without
implicitly deleting its saved connections or logging out unrelated native clients.

## PC-07 - Observable acceptance

- S01/P01: list current-profile connections; loading, empty and read error differ.
- S02/P02/P03: Add chooses type before auth; only supported methods are actionable.
- S03/P04: explicit native sign-in completes in the intended connection context;
  cancellation, expiry and duplicate/late callbacks never save unintended accounts.
- S04/P01/P05: two same-type accounts coexist; independent private runtimes and
  selected connection IDs route two real provider runs to the correct identities.
- S05/P05/P06: reauthentication preserves the committed account on failure;
  runner outage and model entitlement failures do not become incorrect login states.
- S06/P07: different-account reconnect is refused with Add as new connection;
  verified duplicate recovery opens the existing connection without overwriting it.
- S07/P08: disconnect fences dispatch and preserves other connections/host login;
  active controllers and failed cleanup follow the existing revoke/recover rule.
- S08/P03/P09/P10: unavailable native methods do not fall back to host credentials
  or API billing; explicit key entry is masked and never serialized into graphs.
- Keyboard focus, labelled controls, status announcements, safe errors, narrow
  layouts and back/cancel actions follow the workshop. Preserve unfinished safe
  choices; never restore a submitted secret into a field.

Document validation and fixture tests cannot establish provider-native login,
refresh, revocation, account selection or isolation acceptance. Future integration
acceptance records exact provider/runtime versions and sanitized evidence, with
live model use only under explicit authorization; no credentials or login URLs.

## PC-08 - Existing GitHub connection visual language

Owner direction, 2026-11-16: reuse the GitHub connection screens' visual language.
Back and read-only Refresh are the same small icon controls below the main card,
with consistent placement, spacing, accessible names, tooltips and busy states.
Do not introduce boxed Back buttons or a mixture of text and icon navigation.
Refresh rereads the current connection/attempt; it never launches sign-in,
replays a callback, rotates credentials or sends a model request. Back from a
pending sign-in first cancels/fences that exact attempt and then returns to the
unchanged list or selected connection. If cancellation cannot be confirmed,
retain a safe recovery state rather than claiming the attempt was cancelled.
Text-entry fields use an in-field placeholder and a persistent accessible name;
there is no separate visible title above the field. Screen headings remain.
API-key input remains masked. Placeholder text is not the accessible label.


## Selected extension - Claude Code and OpenCode Go (2026-11-18)

The owner selected implementation of the remaining harness connections and
explicitly selected OpenCode Go, using its supported Go key connection first.
A Go key belongs to the Go subscription route; it is not a Console login or an
automatic switch to another billing source. P11 owns its entry and disclosure.
When the installed adapter cannot verify a Go key without inference, record only
local custody and display Key saved, with verification unavailable. Do not submit
a hidden test turn or claim authenticated account identity. Such an explicitly
supplied key may be selected for a user-requested run; upstream refusal remains
a run diagnostic. Missing or altered local key material blocks selection/dispatch.
Exact repeated keys may be detected; different keys are not evidence of different
accounts. Key replacement is not offered in the initial Go increment.

Graph preferences select one compatible connection independently for Codex,
Claude Code and OpenCode, scoped to the authenticated owner and graph. An explicit
node selector overrides only its harness preference. A retained run stays with
its original connection and generation. Cross-harness selectors are refused.

Claude native sign-in remains an official-client operation inside its own private
profile, with no host credential import or third-party token exchange. Its
container callback and user handoff still need implementation and live acceptance.
These selected requirements do not establish implemented or reviewed support.
