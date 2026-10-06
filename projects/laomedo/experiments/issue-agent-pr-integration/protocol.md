---
title: EXP-19 credential-free integration protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Phase zero: credential-free composition

Question: can the current Laomedo Work Graph snapshot, EXP-04 durable run store and EXP-05 raw-event store retain one coherent selected-issue identity through a fake-agent result and a local Git PR candidate, while refusing stale or blocked input and preserving partial failure evidence?

Freeze the existing `examples/work-graph/github-pages.json` fixture, the local Laomedo implementation revision, a two-node synthetic flow definition, fake provider/model/effort, synthetic skill-byte digest, a local-only grant, and a zero-turn budget. Use issue `example/work#2`, whose prerequisite #1 is closed in the fixture. Bind the immutable graph snapshot ID, work key/source update marker, input digest, run ID, trace ID, component revision and local commit ref. A discovered PR is contextual only and must not become a target PR without explicit selection.

Run five conditions in disposable state: (1) source-ready success with a fake agent, a retained raw event and a local Git commit on a unique branch; (2) source body/update-marker change before dispatch; (3) an opened prerequisite; (4) incomplete source/blocker evidence; (5) fake-agent failure after one retained raw event. Require zero dispatch in conditions 2-4, no PR candidate in conditions 2-5, a durable failed run and partial trace in condition 5, and a complete binding only in condition 1. Compare exact snapshot and commit hashes; do not infer a GitHub PR from a local branch.

This phase may use local temporary directories and Git CLI only. It must not start Langflow, Codex, OpenCode or Claude; call a model; read a personal profile; post to GitHub; or change a real issue. The local grant authorizes only writing the disposable checkout. Retain a sanitized observation and test assertions with zero model turns and zero external writes. A pass establishes deterministic composition of these libraries, not Langflow graph execution, native agent events, production grant isolation, Work Graph source correctness, or a real PR. The deferred EXP-18 agent-originated check was a limit of phase zero and remains unproven; the scoped local attempt below uses a host publisher instead of a push-capable agent stage.

## Local authenticated end-to-end attempt

The next attempt asks whether a real selected GitHub issue can pass through a frozen Langflow one-agent flow and the existing single-user Docker Codex runner, produce an observed native command result and bounded output artifact, and have a trusted host publisher turn only that verified artifact into a reviewable PR with a Work Graph run binding. It uses the runner's existing private subscription-backed login. It does not create a browser login flow or expose a GitHub credential to the agent command container. [Specs #129](https://github.com/amadou-6e/specs/issues/129) owns the later browser-managed authentication contract.

Before any model submission, freeze: the exact selected issue URL, stable work key, update marker and body digest; source-complete Work Graph snapshot and readiness; governing specs and component revision; Langflow version and imported/exported flow digest; runner code, image ID, CLI version, permission config, skill revision and source-workspace digest; model and effort; output artifact allowlist; destination repository, unique branch and PR base; time and submitted-turn cap. Timeouts count as submitted turns. The runner ledger starts at zero for this attempt and is never reset to retry a failed call. A refreshed issue or blocker snapshot that differs from the frozen input refuses dispatch.

Run credential-free preflight first: source/graph consistency, Langflow import and round trip, runner authentication and model/effort availability without submitting a turn, exact output path validation, host publisher dry run, and failure injection for stale issue input. Use a disposable source workspace and a private run/evidence directory outside Git. Record a durable run and trace identity before Langflow dispatch. The native command worker must not receive the runner's login file, Langflow key, GitHub token, or host-side publisher path. Preserve raw native events privately, publish only sanitized event identities/counts and hashes, and report skill use as offered unless an event proves more.

The positive model path requires an observed agent-originated command result and an output artifact whose exact bytes match the selected, hashed run artifact. Before publishing, the trusted host validates the artifact path, content, size, source run, target repository and branch, and frozen issue marker. Only the host may push and create a draft PR; it must bind the returned PR URL and commit SHA to the same work key, graph snapshot, input digest, run ID, trace ID and native thread reference. A local branch or attempted POST is not evidence that a PR exists. Lost or uncertain GitHub acknowledgement remains unknown and must not be silently retried.

Test a refusal or partial path as well: a changed issue or blocker source must stop before a model turn; an agent error after raw events must retain a partial trace and create no PR. Record every submitted turn and external write. A success proves only a bounded single-user local path using the current runner permissions and host-side publication. It does not prove the deferred EXP-18 agent-originated push-capable stage boundary, hosted or multi-user isolation, or the production browser-auth lifecycle. If implementation would require GitHub credentials or direct push rights inside the agent stage, stop before dispatch and return to EXP-18.

No model turn is authorized by this protocol alone. Before the first turn, record an explicit cap and approved login mode. Before a GitHub issue or PR write, record the exact repository, branch/base, and permitted write. The [dated local attempt](iterations/2026-10-05-local-e2e/README.md) must pin those grants and actual evidence or remain pending.

## Artifact retry after the first live attempt

The first local attempt ended with a completed native turn but no output file and an exhausted 6/6 ledger. [Issue #69](https://github.com/amadou-6e/laomedo/issues/69) owns a distinct retry. The user added four submitted turns, including timeouts, so the same private runner ledger has a cumulative cap of 10; its first six entries must not be reset or discarded. The earlier exact `test/49` to `develop` draft-PR grant remains unused and applies only to that destination and one verified artifact.

Before a new Langflow dispatch, require the source workspace to contain the selected artifact's parent directory, require the artifact itself to be absent, and compare the whole source tree hash with the newly frozen plan. A changed source refuses dispatch before reserving a workflow run or model turn. Freeze the current issue/graph, code/spec revisions, skill and imported flow again. A no-model nested-write probe or a simpler direct agent canary establishes only filesystem capability, not successful issue-report authoring. The [artifact retry attempt](iterations/2026-10-05-artifact-retry/README.md) records the separate grant, evidence and result; no positive PR claim is inherited from the first attempt.
