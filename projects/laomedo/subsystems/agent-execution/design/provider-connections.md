---
title: Provider connection settings workshop
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-11-16
applies_to: [laomedo]
supersedes: null
related: []
---

# Provider connection settings workshop

Draft for [specs #425](https://github.com/amadou-6e/specs/issues/425), awaiting owner
selection. No product implementation or provider eligibility approval is implied.
The [single-page editable workshop](provider-connections.drawio) is the authority
for UI geometry, screen IDs P01-P10, transition IDs T01-T16 and stories S01-S08.
Its state graph is above a column of screens: design left, story/behavior right.
Identifiers link states to screens; no edges run from the graph into the screens.
The [connection contract](../contract/provider-connections.md) owns persistent
identity, profile scoping, credential custody and dispatch invariants.

## Scope and terminology

A provider type is an integration, initially Codex, Claude or OpenCode. A saved
connection is a separate account/credential context and occupies one list row.
An upstream model service, account/workspace, native runtime and authentication
route are distinct: OpenCode in particular is not one universal account provider.
Graph/assistant bindings select compatible connection IDs, not a global host login.
GitHub repository connections, provider billing changes, hosted/multi-user release
and provider password collection are outside this increment.

## Source-backed capability research - checked 2026-11-16

These are documentation findings, not live support or legal approval for Laomedo.
Only routes validated for an installed adapter may become actionable in P03.

| Type | Candidate route and boundary | Primary evidence / outstanding gate |
| --- | --- | --- |
| Codex | App-owned Sign in with ChatGPT; API billing only if explicitly selected and supported. | [Token sharing to Codex app-server](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server) documents app-owned access-token delivery and renewal. Existing [authentication eligibility and lifecycle gates](../contract/authentication.md) remain; local account success is not universal access. Model listing is not entitlement verification. |
| Claude | Guided sign-in through an eligible, unmodified official Claude Code client in this connection's dedicated native profile; alternatively an explicitly supported Console/API credential route. | [Native authentication](https://code.claude.com/docs/en/authentication) and [authentication/product conditions](https://code.claude.com/docs/en/legal-and-compliance) distinguish users signing into official Claude Code from third parties offering their own Claude.ai login or collecting/intermediating session tokens. Do not implement an unofficial OAuth wrapper or infer product permission from a browser URL. Eligibility/distribution review is unresolved. |
| OpenCode | Installed adapter exposes a supported upstream provider and method, with its own identity/billing label. Current local Go credential borrowing is not a completed Settings login. | [Provider setup](https://opencode.ai/docs/providers/) describes /connect, route selection, optional Go API keys and supported ChatGPT methods. Documented OpenCode capabilities do not prove this Laomedo adapter supports them; version, native authentication orchestration and isolated refresh remain unverified. |

OpenAI references were checked after inspecting the local app-owned SIWC
connection implementation. No borrowed third-party client ID, credential file or
existing personal login is a proposed shortcut. Upstream documentation can change;
recheck the chosen route and installed version before implementation acceptance.

## Stories and workshop index

| Story | User outcome | Workshop |
| --- | --- | --- |
| S01 | See my provider connections and their current states in Settings. | P01 |
| S02 | Add a connection by choosing its provider type and supported sign-in method. | P02, P03, P09 |
| S03 | Complete provider-owned sign-in, return to Laomedo and cancel safely. | P04, P06 |
| S04 | Keep personal/work or multiple same-type accounts independent and select one explicitly for an agent. | P01, P05 |
| S05 | Repair an expired connection without changing other accounts or silently changing billing. | P05, P06 |
| S06 | Recover from a wrong-account reconnect or reuse an already connected identity. | P07 |
| S07 | Disconnect one connection while preserving other accounts and understanding active runs. | P08 |
| S08 | Use an explicitly supported API-key alternative, with billing visible and secrets protected. | P03, P10 |

## Owner-confirmed direction and remaining proposals

- D01: multiple accounts, including multiple connections per type, confirmed by
  the owner on 2026-11-16. Duplicate identity handling remains proposed and uses
  verified provider/route/workspace identity, not labels or assumed API-key identity.
- D02: selection between saved accounts confirmed by the owner on 2026-11-16.
  Local-profile scope and the exact consumer-binding realization remain proposed;
  existing graph or assistant sessions must not be silently retargeted.
- D03: disconnect follows the existing cancel/quarantine requirement for active
  controllers. Local removal waits for stop and credential cleanup; no unrelated
  host logout or unsupported claim of provider-wide revocation.
- D04: which methods are eligible and actually available for the first release.
  All three type choices may explain setup requirements, but no unavailable sign-in
  becomes an active button merely for visual symmetry.
- D05: existing development-only credential copying remains an isolated opt-in;
  it is not imported, enabled or retired automatically by adding this settings UI.

## Validation and handoff

Authoring checks: specs validator, XML parsing, stable ID/edge checks, and actual
Draw.io rendering at full-workshop and component scale. Independent Claude design
consultation and final substantive/visual review are recorded in the draft PR.
This page claims no real provider sign-in, model dispatch, refresh or revocation
acceptance. The future implementation issue must pin accepted specs, provider
routes and required live checks before code changes.

## Implementation gaps identified by Claude consultation

The current SIWC broker has a global active-account pointer; its access-token and
sign-out callers must become explicit per-connection operations before multiple
Codex rows are safe. The OpenCode adapter borrows the active Console account and
cannot yet independently own or remove a connection. Neither existing prototype
can be exposed as multiple isolated Settings rows merely by adding a list UI.
Claude-native authentication must stay in the official client, with no Laomedo
extraction/copy of its subscription credentials; eligibility remains gated.
These are future implementation requirements, not defects fixed by this draft.

Rename is deferred from this first workshop; connection labels may be derived
from verified account/type metadata. No rename/edit control is proposed yet.
T06 means the selected method fails a prerequisite/capability check when Continue
is pressed (for example the installed integration disappeared since rendering).
Known-unavailable routes are not selectable; a type with no enabled methods
explains that in its method screen without starting authentication.

## Visual reference selected by the owner - 2026-11-16

Use the existing GitHub connection visual language, rather than a new provider
settings component style. Reference implementation at Laomedo `be73ad9a`:
[ConnectionNavigation.tsx](https://github.com/amadou-6e/laomedo/blob/be73ad9acd99f53a6c21c6b8999bd775e351dc6e/frontend/langflow-skill-viewer/githubConnections/ConnectionNavigation.tsx),
[ConnectionForms.tsx](https://github.com/amadou-6e/laomedo/blob/be73ad9acd99f53a6c21c6b8999bd775e351dc6e/frontend/langflow-skill-viewer/githubConnections/ConnectionForms.tsx)
and [connections.css](https://github.com/amadou-6e/laomedo/blob/be73ad9acd99f53a6c21c6b8999bd775e351dc6e/frontend/langflow-skill-viewer/githubConnections/connections.css).
The sanitized [navigation crop](references/provider-github-navigation.png) and
[input crop](references/provider-github-input.png) come from the prior integrated
GitHub preview captures at `44fb7b10`; they contain no account or credential data.
They are visual references, not new runtime acceptance for provider settings.

In the workshop, left-hand screens use the existing dark preview theme while the
canvas and story column stay white/light for editing. The application must reuse
its existing theme tokens, not hard-code a separate provider-only palette. Back
is a 20 px left arrow; Refresh is the matching 20 px clockwise icon where a read
is meaningful, in a shared footer with a 12 px gap below the card. Accessible
names/tooltips and keyboard focus remain required even though text labels are not
shown. Confirmation Cancel buttons remain actions, not navigation replacements.
Refresh is illustrated on P01 (list), P04 (pending check), P05 (detail) and P06
(recovery); P08 cleanup variants may expose it only for a read, not as a retry
of cancellation or credential deletion. Back during P04 cancels the attempt first.
P10 has a placeholder-only masked API-key field, with no visible title above it;
its accessible name remains API key. Other future text fields follow the same rule.
