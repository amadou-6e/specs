---
title: Native Langflow node implementation and acceptance status
status: draft
kind: implementation-record
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Native Langflow node implementation and acceptance status

Governing proposed contract: [Langflow node](../subsystems/agent-execution/contract/langflow-node.md).
Implementation work follows Laomedo #18 through #21, on branch `feat/18-21`,
stacked on `feat/11-pilot`. Specification work is `docs/18`, stacked on `feat/11`.
Both remain proposals pending review; no issue is closed by this record.

## Credential-free observations, 2026-10-01

- Pinned Langflow 1.12.3, image digest
  `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`.
- DirectoryReader recognizes the category/module; custom schema compilation and
  Graph.from_payload build a four-vertex, three-edge graph.
- Eight component/graph tests pass in that runtime: concurrent answer/run output
  methods share one invocation, actual connected graph branches dispatch once,
  a serialized resume reference preserves bindings, invalid inputs do not call
  HTTP, and failures/status/cancel preserve their documented semantics.
- Thirty-four host tests pass using `python -m unittest discover -s tests`,
  including the exported flow's whole-skill pin and source identity.
- These synthetic observations do not prove installed-server palette display,
  a real Codex turn, restart/resume through the new node, or native cancellation.

The tests are retrospective evidence; no model turn was submitted in this phase.
The separate prospective #21 real-run plan lives beside the exported example and
must pin actual implementation/spec commits before execution.

## Recovered failures

The initial test loader omitted registering the component module in `sys.modules`,
preventing Langflow source inspection. Registering it fixed that test-only failure.
An initial test tried to persist a Data handle's value inline; the pinned graph
builder drops that value. The node now offers an explicit advanced Prior Run JSON
alternative while retaining its Data port, with an actual graph regression.
Regenerating a Docker-copied temporary fixture first failed because the copied
file was root-owned; regeneration used root only for that temporary fixture,
then the component tests ran as the normal container user. Runner permissions
and mounts were unchanged. No credentials entered the test paths or repository.

## Definitive limitation and follow-up

[Laomedo #22](https://github.com/amadou-6e/laomedo/issues/22) owns asynchronous start
and automatic Langflow cancellation propagation. Synchronous runner start returns
its new run ID after completion, so UI Stop cannot reliably cancel that new turn.
Explicit cancel with a known ID is implemented and synthetically tested; real
native cancellation remains an acceptance gap. This issue does not waive #21.

## Pending acceptance

Separate server startup/configuration and a fresh bounded model-turn ledger await
explicit authorization at the original implementation revision. The user subsequently
approved the proposed server and four new turns; those are now recorded in the
[canonical experiment](../experiments/native-codex-node/README.md). The new ledger
was 4/4 with cancellation inconclusive. The user then authorized two more turns;
the [retry](../experiments/native-codex-node/iterations/2026-10-01-retry/results.md)
passed explicit cancellation and a successful independent fresh task. The ledger
is now 6/6; bounded #21 acceptance is complete and ready for review. No native
interrupt acknowledgement or UI Stop support is claimed. The historical pilot's
4/4 ledger remains exhausted and
unchanged. No new credential copy is required: use the existing approved private
Docker volume only. The intended real sequence is fresh edit/read, restart/resume
through the node, independent fresh run, and bounded cancellation if approved.

No hosted, multi-user, built-in Agent tool-interface, AGENTVIZ, network-boundary or
production authentication claim is introduced. All private raw events stay outside Git.
