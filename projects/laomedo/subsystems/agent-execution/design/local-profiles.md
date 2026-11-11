---
title: Local setup profiles
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-11-07
applies_to: [laomedo]
supersedes: null
related: []
---

# Local setup profiles

Owner clarification: one Windows user selects different local setups. These are
not hosted web accounts or independent Windows identities. The owner requires a
PIN when entering/switching profiles; no separate administrator setup is exposed.
[Editable states and transitions](local-profiles.drawio) own the proposed UI.
All new behavior is PROPOSED / NOT IMPLEMENTED.

## Profile identity and entry

Reuse ordinary upstream user records, password hashing, rate limiting and session
cookies as internal profile identity. Create profile uses a name and PIN with
confirmation, no email or approval step. Proposed initial policy is six ASCII
digits, preserved as text (including leading zeroes), and a trimmed nonempty
name of at most 40 characters. Compare names case-insensitively for both
reserved names and duplicates; preserve the display spelling. The PIN is a convenience lock under one OS-user
trust boundary, not a remote-safe account credential. Never log/serialize PINs
or return submitted values in error details. Unknown/malformed names and PINs
receive safe catalogue-backed errors, never raw validation payloads.

Creation makes an active ordinary user and a default project. It authenticates
through the existing upstream login before displaying the workspace; creation
success alone is not session success. If creation succeeds but login cannot be
confirmed, retain that profile and offer PIN entry, never re-create it on retry.
The picker shows ordinary active profile names/identities only. Registration and
listing cannot expose or accept role flags, hashes, API keys or system identities.
Do not expose the upstream administrator user-list endpoint.

## Startup and internal privilege

Normal upstream startup still provisions a superuser. Proposed minimal adaptation
uses one reserved internal system identity solely for upstream initialization and
controlled profile creation through existing user-service behavior. It is never
selectable, never used as the browser principal and has no human setup step.
Set the cryptographically random startup value directly on the in-process
upstream auth settings immediately before startup, never in an environment
variable or command argument. Upstream may persist its password hash for a new
internal record; never persist the plaintext. Upstream clears the settings value
after setup. No child environment, response, log or settings serialization may
contain the value. Existing profiles
remain ordinary users. Refuse reserved-name registration, an existing reserved
record with wrong role/activity/legacy password, other unexpected superusers,
and a missing internal identity in an otherwise populated profile database.
Before any migration, classify the explicitly owned database read-only:

- Absent database or a valid SQLite database with no application schema: fresh
  only if the owned runtime marker authorizes initialization and no unrelated
  tables/data are present. A zero-byte newly prepared database counts as fresh.
- Recognized migrated schema with the internal identity: verify role/activity,
  password format, absence of legacy credentials and absence of internal API keys;
  ordinary profiles remain unchanged.
- Populated user table without the internal identity, unexpected superusers,
  missing required tables/columns, partial schema, corruption, unreadable state or
  an unknown migration revision: refuse startup with a descriptive error. Do not
  repair, reset or reinterpret such state as fresh.

Only admitted fresh state may create the internal identity through startup.
No account reset, user promotion or global auth bypass is a recovery action.

The generic upstream anonymous registration endpoint stays closed. A dedicated
same-origin local profile-creation boundary validates name/PIN and delegates the
existing user creation with the verified internal actor; it accepts no arbitrary
privileged operation. This is a proposed backend compatibility measure, not an
accepted claim of completed account provisioning. The pinned upstream call is
`add_user(user: UserCreate, session: DbSession, current_user: User | None)` at
Langflow commit `fec71dca901949c09ed4d63315804337cd2eb13d`. Its transaction,
identity-mutation lock, hashing, default project and audit remain upstream-owned.
The audit's technical `created_by: admin` denotes this internal actor, not a
human administrator. A compatibility regression must detect signature changes.

After the upstream lifespan finishes initialization, but before accepting any
request, install a narrow `LocalProfileAuthService` subclass through the upstream
service manager. Registration before initialization is insufficient: upstream
`register_all_service_factories` replaces it. Verify the effective instance before
yielding the application's lifespan. Refuse internal identity at password login,
JWT authentication and token creation (including refresh); preserve the upstream
implementation for ordinary profiles. No API key may belong to the internal
identity: admission checks for existing keys, authenticated creation is refused,
and environment-key/external-identity authentication is disabled in profile mode.
Direct upstream API-key callers bypass the auth service, so subclassing only the
API-key method is not a complete guard. Verify those routes fail closed too.

The upstream self-update route permits username changes by ordinary users. In
profile mode refuse direct username, password, role and activity updates there;
this first slice does not offer profile renaming or PIN changes. This prevents
reserved-name and casefold uniqueness bypass. No global settings toggles or
module monkeypatches may temporarily enable privileged public registration.
Effective startup, restart, reserved-name/role races and upgrade compatibility
need real verification.

## Switching, persistence and limits

Successful profile creation and normal entry persist with the app login lifetime
selected by the owner, including valid refresh and browser/app restart. Every
explicit switch requires the target PIN. Switching first confirms upstream
logout and clears local authentication and query state before selecting another
context. Plain logout uses the same local-session boundary and the shared
`app_signout_unconfirmed` error as switching. Private GitHub access revocation
and pending OAuth invalidation are deferred to the separate private-connection
feature; they are not implemented or promised by this local-profile slice.
A failed switch never claims success or
silently chooses credentials. In-flight results cannot repopulate the new profile. Tabs within one browser
context share its cookie session; a confirmed profile change replaces other
tabs' documents before their old requests can fill new profile state. Independent
simultaneous profiles require separate browser contexts. Returning from the
back-forward cache must not restore a stale profile document.
Profile switching does not rerun a graph or cancel an unrelated model task.

Keep loopback-only serving, exact origin/host checks and appropriate CSRF guards
on new mutations. Picker reads also validate the exact configured Host. For
browser same-origin GETs with no Origin header, require the configured host and
same-origin Fetch Metadata; reject cross-site metadata or a present mismatching
Origin. Mutations require exact Origin and the agreed CSRF protection; never use
substring matching or accept arbitrary localhost ports. One browser session cannot silently use a graph-supplied profile
ID to select credentials. Public Skill registry and existing activity storage are
installation-shared; no tenant-isolation claim. Private data still belongs to the
actual authenticated profile plus repository consent/generation. The earlier
private-session logout/replay design remains a separate proposal tracked by
[Laomedo #259](https://github.com/amadou-6e/laomedo/issues/259).
GitHub connection sharing and PIN reset/deletion are not claimed
as implemented. Forgotten-PIN recovery must preserve data; no destructive reset
is offered as a shortcut. Define/validate recovery before claiming that story.

## Entry availability

LP-C11/C12/C13 and LP-T17 define loading, unavailable setup and unsupported
browser states. Gate the profile UI on the explicit backend capability; ordinary
preview mode retains the native page. Shared catalogue text owns explanations.
No error advice is shown while checking, and retries only repeat safe reads.
The error panel Close action dismisses presentation without claiming to cancel
a submitted sign-out.

## Acceptance

Real browser stories: empty first run, create/confirm PIN, duplicate/reserved name,
leading zeroes, wrong PIN and rate limit, session restoration, expired session,
explicit switch and logout failure, concurrent tabs/profiles, browser/app crash
and restart, and unchanged existing preview. Verify no secret-bearing API/user
list or stale result appears. Tests/renders/reviewer advice are supporting only.
The requesting owner must inspect and validate the final workflow before merge.

## Accepted initial recovery constraint

On 2026-11-07 the owner explicitly selected: defer recovery; a forgotten PIN
blocks entry to that profile. Preserve its data. PIN recovery is unsupported in
this first slice, not a tested capability or a destructive delete/recreate flow.
This owner decision resolves LP-R8 without claiming a recovery implementation.

## Entry presentation

Each profile picker row includes a decorative initials avatar beside the left-aligned stored profile name. The name remains the accessible label. Invalid creation details use concise field-specific messages, as defined in Account-picker refinement below. Editing an invalid field clears that validation notice, and moving between picker, create and entry screens clears previous-screen errors. These changes do not dismiss uncertain save or sign-out outcomes automatically.

Owner decision, 2026-11-11: local profiles now; private revocation later. No private-connection capability or specification maturity change is implied.

Errors inside the profile picker, creation, PIN-entry and save-reconciliation forms show only the shared title, explanation and recovery advice, without a technical-details expander. The separate LP-C12 service-availability screen retains its safe technical details. The owner confirmed that valid matching input does not show the validation error; validation rules are unchanged.

## Account-picker refinement

Owner selected the researched contained-list design: fixed 36px decorative initials avatars, left-aligned names, 64px minimum rows, subtle separators and a trailing chevron. The whole row selects the profile. A divider separates the secondary sentence-case Create profile action with a plus icon. Preserve keyboard focus and long-name wrapping. Local submit errors appear beside their fields: Enter a profile name; Use a six-digit PIN; Confirm your PIN; PINs don't match. Associate errors with fields, preserving input for correction; authentication and uncertain-outcome recovery are unchanged.
