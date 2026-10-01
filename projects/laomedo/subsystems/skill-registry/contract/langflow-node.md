---
title: Langflow Skill reference node
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow Skill reference node

Tracking: [Laomedo #25](https://github.com/amadou-6e/laomedo/issues/25), explicitly
selected after the Codex node pilot. Expose LaomedoSkill in the same operator-installed
category as LaomedoCodexAgent. Existing four-node pilot exports remain historical
evidence and are not silently rewritten.

Inputs: existing Skill ID and exact immutable SHA-256 revision. Validate the ID
against the registry's supported identifier grammar and reject latest/malformed
revisions. Output Data containing skill_id, revision_id and tree_hash; tree_hash
equals the revision identity used by the existing whole-bundle store.

The node selects a reference, not prompt text or credential-bearing filesystem
content. It makes no model call and does not claim a referenced revision exists.
The runner remains authoritative for existence, exact bytes, hash checks and
materialization before a model turn. Discovery, creation/editing, draft promotion,
rule/example subsets and registry browsing are separate capabilities.

The agent's Skill Reference Data input accepts the node output for fresh runs.
Advanced inline fields preserve existing flows. If both are present, matching
values are allowed and conflicting identities fail before dispatch. Empty/unwired
Data inputs must preserve the inline fallback. Resume continues its bound existing
skill/workspace snapshot, rather than silently replacing it from a connected node.

The saved example wires Chat Input and Skill to the agent, with both answer/run
ports connected. No credentials, host profile paths or raw skill content appear
in the reference. Publishing a flow reveals its skill identity/revision, not the
private store contents. Permissions and private login boundaries remain unchanged.

Acceptance: validate descriptor and conflicts without a turn; execute the real
five-node graph with one dispatch; verify installed catalog and imported flow;
verify a bounded model-backed run carries the selected revision and observed
native file result. Link evidence from registry validation; distinguish this
follow-up from the historical six-turn agent-node evidence.
