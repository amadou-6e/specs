---
title: Compact popup card presentation
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-25
applies_to: [laomedo]
supersedes: null
related: []
---

# Compact popup card presentation

The user-approved **A** card in the [editable recovery design](../design/local-runner-recovery.drawio)
owns the visual reference. The **Popup placement and dismissal** page shows that
same card in viewport context. Preserve its compact reading order, inline
title/context where space allows, light coral accent and separate action group.
The other comparison cards are alternatives, not selected standards.

This shared presentation baseline is being implemented for runner connection
failures in [Laomedo #182](https://github.com/amadou-6e/laomedo/issues/182) /
[PR #183](https://github.com/amadou-6e/laomedo/pull/183). Other surfaces are
tracked below; the document does not claim they already conform.

## Visual and content rules

- Use the application's sans-serif stack consistently. Primary copy, context
  and action labels use 14 px; the diagnostic disclosure uses 12 px, matching A.
  Use weight and grouping rather than extra typefaces or oversized headings.
- Use a neutral card with the light coral `#F87171` error rail. Keep ordinary
  recovery actions outlined and neutral. Semantic success/information colours
  must remain distinguishable; a restart must not appear destructive.
- Keep the title and affected node/operation together; wrap context on narrow
  screens rather than overlap, clip or remove it. Use compact related spacing
  and separate explanatory text, technical details and action buttons.
- Provide one concise explanation and useful recovery instruction. Avoid
  repeating a generic failure heading, a second "What to do" heading and the
  same advice in several paragraphs. Preserve uncertainty about remote work.
- Keep safe machine codes and allowlisted identifiers in collapsed Technical
  details. Copy diagnostics copies only those fields, confirms actual clipboard
  success, and offers a manual-copy fallback. See [node errors](node-errors.md).

## Position, overflow and dismissal

Anchor floating notification cards at the bottom-right of the **visible**
viewport, 16 px inside its edges plus device safe areas. A 384 px preferred
width must shrink to the available width. Height is bounded by the visible
viewport; resizing, zoom, visual-viewport movement and the on-screen keyboard
must recompute the bounds. Canvas transforms, clipping ancestors or graph
coordinates must not determine a notification's position.

Scroll long copy and expanded diagnostics inside the body. Keep the header
and action group visible. Actions wrap on narrow screens rather than overflow.
The selected A uses an explicit **Dismiss** button; close icons elsewhere need
an accessible name and an adequate target. Keyboard activation and Escape from
inside the card dismiss it. Restore prior focus, or the canvas when unavailable.
Closing the UI never cancels execution or interrupts a requested API restart.
Errors requiring recovery or with unconfirmed outcomes remain until dismissed.

The shared toast host follow-up must stack notifications upward inside one
bounded scrollable region and coordinate with the persistent recovery card.
No stack item or action may be pushed outside the viewport. This cross-surface
stack is a tracked implementation gap, not established by the single recovery
popup. Informational expiry needs an explicit policy before its migration.

## Surface inventory and migration issues

| Surface | Current owner in pinned Langflow | Work |
| --- | --- | --- |
| Runner connection failure | `components/laomedoRecovery/RecoveryPopup.tsx`, flow-building integration | [#182 / PR #183](https://github.com/amadou-6e/laomedo/pull/183), current implementation slice |
| Error notifications and shared toast host | `alerts/error/index.tsx`, `alerts/displayArea/index.tsx` | [#186](https://github.com/amadou-6e/laomedo/issues/186) |
| Notice and success notifications | `alerts/notice/index.tsx`, `alerts/success/index.tsx` | [#187](https://github.com/amadou-6e/laomedo/issues/187), reuse #186's host |
| Remaining running/completed/failed flow cards | `pages/FlowPage/components/flowBuildingComponent/index.tsx` | [#188](https://github.com/amadou-6e/laomedo/issues/188) |

Inventory inspected against upstream Langflow
`fec71dca901949c09ed4d63315804337cd2eb13d` and the Laomedo overlay. Node-anchored
error popovers and modal dialogs are different interaction surfaces: do not
silently move them into the notification stack as part of these issues.

## Verification requirements

For each migrated surface, check real app-triggered messages at desktop,
narrow and short viewport sizes, long copy, expanded details, resize/zoom,
keyboard dismissal and focus restoration. Confirm all actions remain visible
and no automatic graph/model request is triggered. Runner recovery additionally
requires the real offline-to-ready path without model dispatch, bounded by a
separate verification harness. Preserve historical evidence; do not turn
experiment-only turn ceilings into normal-runner authorization.
Internal unit tests may use fixtures; they do not establish live acceptance.
Record exact revisions, screenshots, remaining gaps and independent visual
review. No merge is authorized by the existence of these requirements.

Current implementation evidence and the installed-CLI startup blocker are
recorded in [the dated validation entry](../validation.md#approved-a-popup-implementation-2026-10-25).
