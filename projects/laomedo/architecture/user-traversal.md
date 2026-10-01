---
title: Issue-to-agent user traversal
status: draft
kind: user-journey
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue-to-agent user traversal

The [editable user-traversal graph](user-traversal.drawio) records the product
journey defined with the user on 2026-10-01. It is a draft cross-subsystem journey,
not implemented behavior or a reviewed screen-layout specification. Future
view-specific geometry and interactions belong to their owning Draw.io workshops.

The [Mermaid input](user-traversal.mmd) is retained as generation provenance.
Draw.io is the editable design authority: do not regenerate over user edits without
reconciling them. The files were moved from runtime with identical SHA-256 hashes:

- Draw.io: `872d3d566908455ad64745e6ae1676d376bf97169e3689d20aa2c0251c7e027f`.
- Mermaid: `e32eccc7cc55e498c6242202ebed41cf4bd2b4ace91005e59dbfcbe377dfb654`.

These are the initial import hashes, not the current file hashes. Subsequent
user-requested layout refinement groups setup, live inspection, results, PR review,
failure recovery and library management into six editable subgraphs. All four
decision diamonds are 220 x 220, centered on their laid-out positions, with adjusted
connectors and containing group bounds. After regenerating from Mermaid, normalize
diamond geometry only after layout; another layout pass can override those sizes.
The grouped single-page render was visually inspected after those corrections.

## Diagram vocabulary

Card category identifies responsibility and is not an actor/owner field in the
card body: **User**, **Agent**, **Laomedo**, or **External service**. Category is
shown in the header, icon and color. Shared editing/publication paths name their
alternate actors in details; this diagram grouping does not freeze implementation
ownership or permissions. The category legend is separate from the node-type legend.

Card text is left-aligned with a consistent inset. Field markers are `IN:`, `OUT:`
and `DETAIL:`; decision questions remain centered within their diamonds.

| Node type | Shape | Meaning |
| --- | --- | --- |
| Action | Rectangle | Selection, configuration, inspection, processing or publication |
| Decision | Diamond | A branching choice or outcome; four journey diamonds and the legend diamond are 220 x 220 |
| Artifact | Document with wavy lower edge | An issue, PR, library, trace, graph, summary or finding record |
| Continuation | Capsule with return-arrow marker | Re-entry, handoff or end of this traversal |

Cards show a category/type header, title, purpose where it adds information, named
inputs and outputs, and a type-specific detail line. Actions describe choices,
completion, permissions or execution limits; artifacts describe storage, contents
or retention; continuations describe carried context and destination. Unknown
values stay unspecified. Diamonds retain a short question/category and branch
labels rather than becoming crowded field tables.

[Card authoring metadata](user-traversal.cards.json) stores category, inputs, outputs
and details for the 39 journey nodes. It is draft diagram metadata, not a runtime
API schema. Title/purpose and branch text remain in the diagram and generation input.

Mixed operations are separated where useful: creating a PR leads to its PR
artifact; converting a failure report leads to an issue draft. These arrows express
the user journey, not a frozen implementation event ordering. Icons are UTF-8 text;
labels and colors convey card category; shapes convey node type independently.
Document shapes and uniform diamonds are applied after text-to-Draw.io generation;
regeneration must preserve those refinements or explicitly reapply and inspect them.

## Confirmed journey

Select an issue, then configure direct-agent execution or a Langflow workflow.
The first scope is direct-agent execution, with recommended prompts/skills and
a user-curated library. Langflow defines stage-specific agents/skills, structured
handoffs, reviews and loop limits. UI and chat-assisted API configuration share
the execution model; the chat agent can configure/launch and highlight UI elements.

Choose an existing local checkout or a prepared isolated workspace. A run is
distinct from an agent session. Stages appear in a GitHub Actions-style graph;
a single agent has one Langflow-style card. Inspect telemetry by clicking a card.
Completed runs expose an expandable action digest and retained semi-structured
summary. Users optionally promote selected findings into project knowledge with
source/run links; publishing them to GitHub is a separate action.

Delivery creates a GitHub PR. Review feedback starts a new linked run updating
that same PR; the user selects an existing session or a new one. The agent is
hinted that PR comments exist and should be addressed, and retrieves them itself.
An unsuccessful run supplies a semi-structured report convertible into an issue
draft that the user reviews/edits before publishing. The new issue uses the same
normal agent-execution path as every other issue.

Users and agents can edit a native or GitHub-backed prompt/skill library. GitHub
publication uses PRs by default; the user can disable review and allow auto-editing
on the configured branch.

## Boundaries and open choices

Summary fields, API authorization details, execution budgets, workspace defaults,
PR merge behavior, exact screen geometry, retention policy and implementation
reuse remain unspecified. AgentViz reuse is an option, not an accepted design.
No new model-backed validation or product implementation accompanies this graph.
Some diagram wording organizes the journey for readability; future contracts
must resolve precise semantics through review rather than treating it as an API.
