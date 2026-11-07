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
name of at most 40 characters. The PIN is a convenience lock under one OS-user
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
Its startup-only value is cryptographically random, held in memory and never
stored as a login secret, exported to processes or disclosed. Existing profiles
remain ordinary users. Refuse reserved-name registration, an existing reserved
record with wrong role/activity/legacy password, other unexpected superusers,
and a missing internal identity in an otherwise populated profile database.
New empty owned state may create the internal identity through normal startup.
No account reset, user promotion or global auth bypass is a recovery action.

The generic upstream anonymous registration endpoint stays closed. A dedicated
same-origin local profile-creation boundary validates name/PIN and delegates the
existing user creation with the verified internal actor; it accepts no arbitrary
privileged operation. This is a proposed backend compatibility measure, not an
accepted claim of completed account provisioning. Effective startup, restart,
reserved-name/role races and upgrade compatibility need real verification.

## Switching, persistence and limits

Successful profile creation and normal entry persist with the app login lifetime
selected by the owner, including valid refresh and browser/app restart. Every
explicit switch requires the target PIN. Switching first confirms upstream
logout, clears user/query/private buffers and invalidates pending profile-bound
OAuth before selecting another context. A failed switch never claims success or
silently chooses credentials. In-flight results cannot repopulate the new profile.
Profile switching does not rerun a graph or cancel an unrelated model task.

Keep loopback-only serving, exact origin/host checks and appropriate CSRF guards
on new mutations. One browser session cannot silently use a graph-supplied profile
ID to select credentials. Public Skill registry and existing activity storage are
installation-shared; no tenant-isolation claim. Private data still belongs to the
actual authenticated profile plus repository consent/generation. The earlier
private-session logout/replay guarantees in SC01/#259 are not weakened by this
profile proposal. GitHub connection sharing and PIN reset/deletion are not claimed
as implemented. Forgotten-PIN recovery must preserve data; no destructive reset
is offered as a shortcut. Define/validate recovery before claiming that story.

## Acceptance

Real browser stories: empty first run, create/confirm PIN, duplicate/reserved name,
leading zeroes, wrong PIN and rate limit, session restoration, expired session,
explicit switch and logout failure, concurrent tabs/profiles, browser/app crash
and restart, and unchanged existing preview. Verify no secret-bearing API/user
list or stale result appears. Tests/renders/reviewer advice are supporting only.
The requesting owner must inspect and validate the final workflow before merge.
