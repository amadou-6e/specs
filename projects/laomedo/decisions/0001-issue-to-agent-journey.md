---
title: Issue-to-agent journey decisions
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue-to-agent journey decisions

## Status and sources

This is a **reconstructed discussion record**, not a verbatim chat log. It
captures the user's choices while developing the
[user-traversal graph](../architecture/user-traversal.drawio) and its
[narrative](../architecture/user-traversal.md), through 2026-10-02. The
[Mermaid input](../architecture/user-traversal.mmd) and
[card metadata](../architecture/user-traversal.cards.json) provide diagram
provenance, not a transcript. Exact message timestamps, rejected wording and
unrecorded alternatives are unavailable in the repository. The record remains
draft until the user reviews this reconstruction. It describes desired product
behavior, not a working Laomedo feature.
The inspected graph history is pinned to specs commit
`0e4ebd5f533e49d8c7975bf054b50dec4f31abad` (last change to the journey
diagram before this record).

## Entry and configuration

1. The initial issue-centered path was: select an issue, then choose a single
   agent or a Langflow graph. The user later also allowed direct prompt and
   scheduled/event launches; those are recorded in the
   [handoff decisions](0002-subsystem-handoffs.md#launch-and-version-resolution).
2. The first implementation emphasis is the single-agent path: a form for agent,
   prompt, model/effort, files and recommended skills, with editable templates.
   The user may curate a native or GitHub-backed prompt/skill library. Both
   users and agents may edit and publish there; GitHub publication defaults to
   a PR, with an explicit direct-edit option.
3. The graph option uses Langflow for structured agent stages, handoffs, review
   loops, limits and assigned skills. A chat assistant can navigate the same
   configuration API, help set it up, launch runs and highlight stable UI
   elements. It is assistance over the same operations, not a second execution
   model. Later clarification made even the single-agent path a one-node
   Langflow workflow; see [D02](0002-subsystem-handoffs.md#workflow-setup-and-definitions).

## Live run and visual language

1. The user asked for a GitHub Actions-like execution view: multiple configured
   stages appear as stages, while a single agent appears as one card. Clicking
   a running card opens that agent's telemetry. This is an overview of execution,
   not the Langflow editor graph; the later handoff interview refined it to
   separate invocations and timings, with waterfall only a candidate layout.
2. After completion, a digestible action graph/summary expands to tool calls,
   web searches, edits, commands and artifacts. Findings are stored only if the
   user selects them. The UI should make saved versus unsaved and published
   versus unpublished results understandable.
3. The first Draw.io pass was generated from text, then refined in discussion:
   four card categories (User, Agent, Laomedo, External service) are marked by
   header, icon and color; action, decision, artifact and continuation use
   different shapes. Cards use left-aligned `IN:`, `OUT:` and `DETAIL:` fields;
   decision diamonds retain short questions and were normalized to one size.
   Adjacent operations were grouped into subgraphs. These are diagram editorial
   choices, not runtime API fields.
4. Two user-added red annotations prompted a clarification: a run record holds
   configuration, trace, status, summary and references, while output files may
   remain in a workspace, PR or other store. Their destination policy still
   needs an experiment; no storage system was selected.

## Outcome, review and continuation

1. A successful run normally ends with a PR on the user's GitHub repository.
   The user reviews it and can start a linked follow-up run. The user selects
   which existing or new agent session to use; the agent is only prompted that
   PR comments exist and should retrieve and address them itself.
2. An unsuccessful run produces an editable semi-structured report. The user
   reviews it and may convert it into a new issue for another agent. That issue
   has the same execution capability as any other issue; no special failure-
   issue class was chosen.
3. The user may select whether to store findings. Publishing to a GitHub-backed
   library is a separate, reviewable action unless direct editing was explicitly
   enabled.

## Alternatives, limits and consequences

- The journey does not require every run to start from an issue, despite the
  initial issue-centered sketch. Direct and scheduled launches were added
  later; the graph should not be read as an exhaustive trigger API.
- The user chose a separate execution overview over using the Langflow editor
  graph as live telemetry. AgentViz reuse was discussed only as a possibility.
- Exact UI layout, summary schema, telemetry retention, permissions, artifact
  placement and implementation feasibility remain open. The
  [subsystem handoff record](0002-subsystem-handoffs.md) narrows several of these
  topics without claiming they are implemented.
