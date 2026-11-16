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
type choice when connecting. Multiple accounts and the detailed list/lifecycle behavior below are proposals,
not previously accepted product decisions. Existing authentication isolation and
revocation requirements continue to apply.

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
Multiple connections of the same type may coexist. Display a label, type,
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
completion or a validated one-use callback may stage credentials. A callback is
not proof of success: verify the selected route's authenticated state, then commit
connection metadata and private credential reference together. Cancellation,
expiry, logout and an invalidated lease fence late completion. No duplicate launch
on polling or page refresh. An interrupted attempt is reconciled or reported as
expired; restarting Laomedo never blindly replays login.

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
Existing sessions remain bound to their original identity.

When the same verified identity, provider type, route and workspace is already
connected, refuse a duplicate save and offer that existing connection; do not merge records
or replace its credential.
Where identity cannot be established (for example some API keys), do not pretend
to deduplicate; keep explicitly labelled independent connections. Equal email
addresses or user labels across types are not a canonical identity match.

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
