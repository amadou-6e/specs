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
are not imported. The provider-connections rollout retires development-only
host-login mirroring, its configuration and executable helpers. Standalone
runners may use explicitly authenticated dedicated native profiles; they must
not read or copy the ambient host login.

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
profile, with no host credential import or third-party token exchange. The official
client may provide an authorization URL and a one-use completion code instead of
a host callback. P12 relays that URL only to the initiating browser and accepts
the completion code in a masked, accessible field. The code is passed once to
the original client process, never exchanged by Laomedo or persisted. Refresh
only observes; Back fences the attempt and confirms native cleanup. Account and
workspace identity come from native auth status before publication. A failed
reconnect leaves the saved connection intact. Live acceptance remains required.
These selected requirements do not establish implemented or reviewed support.


## PC-09 - Subscription allowance observations (#300, specification #437)

P13/P14 and Q0-Q5 in the owning Draw.io define the Subscription agents allowance
surface. Graphs keep separate harness preferences; allowance belongs to each
current-profile saved connection, never to a run or its token/cost counters.

Opening the tab reads only cached observations. Each account has an explicitly
labelled Refresh limits icon. It invokes only the selected provider's bounded
read operation; no prompt, new thread, model probe, login, alternate account or
ambient host credential import is permitted. Codex admits only
`account/rateLimits/read`, with empty parameters, before creating a native
session. The existing connection-owned controller and exact cleanup receipts
remain authoritative; discovery/active-work conflicts report temporary
unavailability instead of weakening admission. OpenCode reports unavailable until a supported account-scoped zero-turn quota
operation is established. The selected Claude observation below supersedes the
earlier Claude-unavailable state and reuses the same P13-P16 surface.

Preserve primary/secondary windows and every returned metered bucket. Prefer
`rateLimitsByLimitId` when present; otherwise use the single `rateLimits` view.
Do not duplicate that fallback bucket. Preserve absent/null windows, duration,
reset, plan and credit details as unknown. Empty authoritative buckets mean no
reported limits. Used percentages must be finite and nonnegative; remaining is
max(0, 100 minus used), never inferred from tokens. Reset timestamps are Unix
seconds, displayed in local time with full date/time available. Window names are
derived from provider-reported minutes, never fixed hourly/weekly/monthly tiers.
Credits/balance/unlimited flags remain separate from percentage allowance.
Only explicit safe fields cross the browser boundary; no raw responses/errors,
credential paths, tokens or login metadata are returned or logged.

Cache in memory only, scoped to profile, connection, generation and browser
lease. Freshness lasts at most60seconds, and ends sooner if a reported reset
passes. Retain a stale same-binding snapshot after failed refresh with a concise
retry state; never claim a reset replenished allowance without a new read.
Retained cache is bounded and expires after10minutes. Native refresh is single-flight on (profile, connection, generation), independent
of browser lease. Cache visibility and publication remain lease-gated. Revoking
one waiter discards only its own result, not another valid waiter's read. Fresh
snapshots are reused even for explicit Refresh; failures have a10second retry
cooldown per native binding. Late responses cannot overwrite newer ones. Check
profile/connection/generation and the browser revocation fence both before and
after native reads. Disconnect, reconnect, logout, unavailable credentials or
controller closure prevent publication of an old observation. No account or
harness/graph change may show the previous selection's pending result. Native
cleanup failure remains a failure, and is not turned into a successful quota read.

Acceptance: observe real saved-Codex quota/reset data with zero submitted model
turns; cover null/multiple/malformed windows, over-limit percentages, credit
separation, foreign profiles, generation changes, disconnect/logout during reads,
failed refresh with stale retention and out-of-order browser responses. Inspect
narrow/wide rendered states; supporting fixtures are not real account acceptance.


PC-09 clarifications (Q1-Q9 review): P15 defines labelled buckets ordered by
opaque bucket ID, ascending; use the reported display name when present, otherwise
the ID. Do not impose a preferred bucket. A secondary-only bucket renders just its
secondary window. Each window has the same remaining-allowance bar; unknown
percentages have no bar. Empty windows/buckets say No limits reported. P16 defines
a320px view: headings/refresh remain aligned; window allowance is on its own line,
reset time wraps beneath it; no horizontal clipping.

A nonfinite/negative/nonnumeric percentage, nonpositive/noninteger duration or
noninteger/nonpositive/out-of-display-range reset becomes unknown for that field
only. Preserve other valid observations. Structurally invalid responses (wrong
bucket/window/map types or excessive records/strings/response size) fail the read
and keep the previous same-binding snapshot stale. Credits display Credit balance
with its provider-reported value; no currency is invented. Unlimited credits and
No credits are distinct from unknown credit details; no credit field implies no
credit line. Text fields are bounded safe fields, not unfiltered raw responses.

Explicit Refresh may start a temporary native app-server process in the existing
connection-owned isolation boundary. It sends only initialization and the named
rate-limit read, never session/new, thread/start or prompt. Reuse the admitted
zero-turn discovery lifecycle, with native request budget30seconds, initialization
budget45seconds, existing bounded image/startup budgets and exact native teardown.
The temporary controller is closed before publishing the observation. Startup,
protocol or cleanup failure becomes unavailable/stale, not a successful read;
client timeout/abort never authorizes replay or another account. No persistent
model task or credential-bearing process is created by mounting the panel.

Both parent PRs (#426 specification, Laomedo#285 implementation) are explicit
integration/merge gates. Their incomplete review or live acceptance is not waived
by this focused extension. If their ownership/lease contract changes, review this
extension against the resulting boundary again.


## Selected Codex connection - one native method (2026-11-20)

Owner direction: expose one Codex connection method which supports both Agent
execution and read-only subscription allowance. Replace the Settings token-sharing
method rather than offering native authentication as a second method. One saved
connection, identity generation and native credential profile govern both uses.
The older token-sharing credentials must never be reinterpreted as native tokens.

The pinned official Codex 0.159.2 app-server owns ChatGPT device-code sign-in
(`account/login/start`, type `chatgptDeviceCode`). Laomedo relays only the returned
one-use code and exact official verification URL to the initiating browser lease.
There is no password collection, API-billing fallback, host-login import or second
quota-only sign-in. Back cancels and fences the attempt; public progress reads do
not disclose the code. Refresh observes the existing attempt and never starts one.
Unavailable/disabled device authentication remains an explicit recoverable error.

Create custody before an authentication container starts: a dedicated labelled
volume, exact daemon and immutable managed image belong to one credential revision.
Saved-mode Agent startup verifies that admitted volume and must never create an
empty replacement or use the global/derived disposable credential volume. The
same profile is used by inference and quota discovery; model tool workers never
mount it and controller tool-policy denial of auth.json remains in force.

Use only native public observations: account/read with refreshToken false and
experimental workspaceRouting.chatgptAccountId, and account/rateLimits/read's
accountId. Cross-check both when present; missing or conflicting identity fails
closed. Reject unsupported account routing. Do not read credential-file contents,
decode token claims, or export tokens. Verify the official client's auth.json
exists only after the login process has stopped. Force file custody, the official
login issuer and the native OpenAI provider; never use an ambient keyring.
Email plus account/workspace ID is an observed binding, not an immutable user ID.
An email change cannot silently establish identity equivalence.

Native refresh stays client-owned. At most one live writer may use a credential
revision, including runs, validation and quota. Refuse overlapping use as connection
busy. Hold custody through confirmed teardown and reconcile exact owned session
receipts after a crash before admitting another writer. Cancelled or unpublished
attempts erase their entire staged revision, even after a late native completion.

Quota uses only the named bounded account/rateLimits/read operation before any
thread/prompt. It submits zero model turns and never grants inference entitlement.
Canonical browser lease renewal, profile/connection generation fences, stale/cache
rules, cancellation and Disconnect custody guarantees apply unchanged.

For an existing token-sharing account, Sign in again stages a fresh native login
and shows the newly verified account before explicit replacement confirmation.
Only confirmation publishes the revision using the same opaque connection ID,
keeping graph selections and incrementing generation. Never infer cross-method
identity equivalence from matching email. Back, failure, expiry or cancellation
preserves the committed login and erases the unpublished native revision. Retained
sessions from the old generation cannot resume with the replacement credentials.


## Selected Claude subscription observation (2026-11-24)

Owner direction extends the same saved-account quota panel to Claude Code.
Use the existing connection-owned native profile and the pinned official Claude
CLI2.1.310. Do not introduce a second sign-in, inspect token-file contents or
call a quota endpoint with exported OAuth credentials.

Explicit Refresh sends only native initialize and the structured `get_usage`
control request with `skip_behaviors: true`. The latter suppresses scans of local
transcripts and their behavioral summaries. No user message, model turn, tool,
resumed conversation or persisted model session is submitted. This is a pinned
experimental native surface, not a stable public SDK promise; unavailable or
changed structures fail closed and preserve only visibly stale prior evidence.

Validate the selected saved account before reading. Hold the existing controller
catalog admission fence through native job teardown and revalidate generation
before publishing. Cached panel reads remain metadata/memory-only. Existing
profile, browser-lease, reconnect, cancellation and Disconnect fences apply.
No raw CLI errors or unrelated session/behavior fields reach the browser.

Project native five_hour and seven_day utilization/reset observations as5hour
and7day windows. Additional OAuth-app, Opus, Sonnet or model-scoped weekly
windows are separate labelled buckets. Do not invent missing windows, remaining
quota or reset times. Invalid scalar observations remain unknown; invalid
structure fails the read. Extra-usage billing/credits are not subscription
allowance and are excluded. Reuse P15/P16's existing meter layout and narrow-view
rules in the Claude tab; no additional login or design screen is introduced.

Acceptance requires a real explicit read through an existing saved Claude
connection, including an exhausted allowance when that is what the provider
reports, and no model turns. Fixtures support protocol/isolation/error checks;
they do not establish real provider acceptance or independent visual review.

OpenCode feasibility: its current official Go documentation exposes read-only
GET https://opencode.ai/inference/go/v1/usage using the same Go key. It returns
rolling, weekly and monthly percentages and reset timestamps. This identifies a documented integration route, not implementation or live
acceptance here. Two read-only checks using the existing Go key returned HTTP403;
the cause is unestablished, so no working Go allowance read is claimed.
A later Go implementation must preserve all three reported windows; the current
two-window bucket contract must be deliberately extended or explicitly mapped.
Source: https://opencode.ai/docs/console/go/#usage


## Selected OpenCode Go allowance read (#445 / Laomedo #313)

Owner selected implementation on 2026-11-26. This supersedes the earlier
OpenCode-unavailable/feasibility-only projection for saved Go key connections.
P18/P19 and S12 in the workshop define its reuse of the existing allowance panel.

An explicit Refresh uses only the admitted saved Go key for GET
`https://opencode.ai/inference/go/v1/usage`. No second connection, browser login,
inference request, credential refresh/export, redirect, ambient login or billing
fallback is permitted. Validate private key custody before and after the bounded
read. Existing profile, generation, browser-lease, coalescing, stale-cache,
Disconnect and logout fences remain mandatory. Opening the subscription panel requests fresh limits automatically, then refreshes every 10 seconds while mounted. Do not overlap requests; stop the timer and cancel in-flight browser requests on unmount or account/generation change. Keep manual Refresh icon-only.
A stored Go key whose upstream authentication has not been checked may request
this explicit read; successful quota does not silently change its auth state.

Preserve all reported meters in provider order: rolling five-hour as primary,
weekly as secondary, and calendar monthly as monthly. Extend the shared window
kind with monthly and its per-bucket maximum from two to three on both wire
boundaries. Monthly has no fixed minute duration and is labelled Monthly window;
never infer thirty days or reset times. Each meter shows reported used percentage
as remaining allowance and its timezone-aware reported reset. Missing meters
remain absent, invalid scalar values remain unknown, invalid structural data
fails safely. No model/cost/credit values substitute for subscription allowance.

Use one bounded HTTPS GET (15-second total process deadline, at most 64 KiB) and no automatic
retry. HTTP401 means the key was not accepted; HTTP403 means this key cannot
access Go limits, without asserting which subscription/workspace cause applies;
HTTP429 asks the user to try later. Other HTTP/transport/protocol errors are a
failed refresh. Do not display raw upstream messages, keys or request headers.
These failures preserve the saved connection and any previous snapshot, explicitly
marked stale; they never imply zero allowance or successful authentication.

Acceptance: verify all three meters, unknown/missing fields, bounded reads,
redirect refusal, HTTP failure categories and key-change rejection in meaningful
deterministic tests. Verify the actual saved Go connection with zero inference;
if refused, report the safe HTTP category as the live blocker, not a fabricated
success. Inspect the implemented panel at wide and narrow widths using live
provider data when available, retaining source versus live evidence separately.
Source: https://opencode.ai/docs/console/go/#usage (checked 2026-11-26).

### Selected automatic quota refresh (owner decision, 2026-11-26)

For all supported connected providers, opening the subscription panel immediately requests fresh limits and repeats every 10 seconds while the panel remains mounted. This supersedes earlier explicit-only/cache-only mounting requirements in PC-09 and its provider amendments. Keep the manual Refresh icon without button text. Skip polling ticks while a check is in flight; clean up timers and browser requests when leaving the panel or changing account generation. Existing native admission, zero-inference, lifecycle, single-writer and stale-data protections remain mandatory. Failures remain visible and do not fabricate allowance or start authentication. Verify initial automatic loading, ten-second repetition, no overlapping checks and cleanup on leaving.
