---
title: Community distribution and maintainer proposal for Langflow components
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Community component package

Investigation and proposal brief for [release package one](../../../architecture/release-packages.md).
No current upstream distribution policy or maintainer preference has been
researched for this brief. It does not claim that upstream will accept the nodes.
Existing node behavior remains owned by the
[Codex node contract](../../agent-execution/contract/langflow-node.md),
[OpenCode contract](../../agent-execution/contract/opencode.md) and
[Skill node contract](../../skill-registry/contract/langflow-node.md).

## Requirement owners and design scope

[Community distribution](../contract/community-distribution.md) owns the confirmed
independent release, Codex/Windows-first scope and automatic setup experience.
[Decision 0006](../../../decisions/0006-release-packages.md) preserves the owner's
answers. The [Output Contract](../../agent-execution/contract/output-contract.md)
owns its new node/precheck behavior. This page owns the proposed investigation
and maintainer approach, not a competing set of install or output rules.

The existing node contracts above retain their narrower implemented/pilot
boundaries. Artifact format, managed runner lifecycle and loading mechanism
need design after compatibility/license research. The internal component/runner
split must meet the contract's automatic setup experience. No current installer
or Output Contract implementation is claimed.

## Research questions and deliverables

The table below is a proposed research handoff, pending an owned entry in
Laomedo's `research/` collection. Before executing the investigation, create
that entry from the [research template](../../../research/template/README.md).
It will own the method, sources, findings and synthesis. This original review
page remains an index/outreach proposal and must not become the source ledger.

Use the shared [research skill](../../../../../shared/skills/research/SKILL.md)
for the source investigation and independent writing handoff. Inspect current
primary Langflow contribution documentation, custom-component loading APIs,
distribution mechanisms and relevant accepted/rejected integration proposals.
Pin source revisions and access dates. Record these outcomes:

| Question | Required deliverable |
| --- | --- |
| How can users install/version custom components? | Reproducible distribution options, update/uninstall behavior and clean install test plan |
| Where does upstream want external-runner integrations? | Evidence-backed comparison of core inclusion, maintained extension collection and independent package; maintainer preference remains unknown until response |
| Which versions are supportable? | Test matrix for the pinned baseline and a separately selected current upstream version; no latest-version compatibility assumption |
| Can the complete artifact be distributed? | License inventory for our code, Langflow integration, provider clients/binaries and bundled assets; unresolved distribution questions explicitly tracked |
| What is the sustainable maintenance cost? | Owners, release cadence, API-change policy, issue routing and unsupported-platform statement |

Produce a source/finding handoff before a final recommendation. A historical
license note or successful local component test is not distribution clearance.

## Maintainer approach, proposed sequence

1. Prepare a short reproducible demo using synthetic/nonpersonal data, an
   architecture diagram, installation instructions and test/compatibility results.
2. Identify the contribution channel from current upstream guidance. Draft one
   proposal explaining the user need, nodes, external-service boundary,
   credentials, maintenance commitment and alternatives.
3. Ask maintainers where this integration belongs and which tests, interfaces
   and support expectations would make it useful. Offer a minimal representative
   component rather than presenting the entire Laomedo application as required.
4. Obtain explicit user authorization before sending the proposal or opening
   an upstream issue/discussion/PR. Record the actual URL, date and response.
5. Classify acceptance, requested redesign, deferment, rejection or no response
   without interpreting silence as approval. If redirected, update the route
   and retain the original response as evidence.

Draft outreach opening: "We have custom Langflow components that run pinned-skill
Codex agents through an automatically configured local runner, with OpenCode
planned as a follow-up. We would like your
feedback on whether these fit core, an integration collection or an independently
maintained package. We can provide a minimal demo, versioned interfaces and
compatibility tests. Which route and review requirements would you recommend?"
This text is unsent and will need evidence links and a verified contribution channel.

## Handoff and open questions

Use [the distribution contract's acceptance](../contract/community-distribution.md#acceptance-and-open-engineering)
for clean-install gates. This research must produce the source/finding handoff
before a final packaging recommendation. Still open: package format/name,
runner installation/lifecycle, Langflow matrix, optional manifest entries,
visibility/license, maintenance commitment and publication channel.

Windows/Codex first and independent distribution are owner choices, not open
votes. No upstream contact, installer test or community release occurred here.
Outreach and distribution implementation are parked while the owner prioritizes
the integrated Langflow demonstration.
