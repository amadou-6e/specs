---
title: Trusted output-validation publication handoff
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Trusted output-validation publication handoff

Engineering mechanism for [decision 0007](../../../decisions/0007-trusted-output-publication-handoff.md), tracked by [Laomedo #138](https://github.com/amadou-6e/laomedo/issues/138) and [specs #345](https://github.com/amadou-6e/specs/issues/345). This is host-side opt-in composition, not an activated deployment or live-publication pass.

## Ownership and admission

The trusted host constructs `PublicationController` with its mediator store, a finite positive lifetime, a private artifact resolver, a description builder, an injected provider transport and a provider readback. There is no default lifetime and no ambient GitHub login fallback. The host must explicitly run the startup recovery sweep after the old controller is known dead; it revokes unfinished handoffs and never replays a publication.

Before agent dispatch, the controller registers the existing supervised grant and freezes the Output Contract reference, wall-clock deadline and monotonic deadline in `publication_handoffs`. An opt-in GitHub-scoped launch without a valid Output Contract refuses dispatch. Renewal clamps to those deadlines. Neither agent completion nor graph waiting resets them. The independent lease service continues supervising the same lease; there is no separate publisher grant, grant resurrection or extra sign-in. This remains run scoping, not authorization against another process with the same user's host access.

After verified executor removal, the controller freezes the host-observed answer and resolves the existing private `VerifiedStage`. The artifact's run, repository and branch must match the existing grant, its bundle bytes must match their digest, and its exact stage digest must have a confirmed push receipt under that grant. The controller fixes PR head/base, title/body, a stable handoff marker, `draft: true` and an effect identity. A graph never selects a host path, repository, branch, grant, deadline or publication payload.

The transition to `validation_pending` serializes with mediator intent reservations. All operations through the old agent bearer, including bundle capture/status, are refused after this transition. Any unresolved effect intent makes the handoff `unknown` and revokes it; waiting for a possibly in-flight agent write is not evidence of safe completion.

## Graph and publisher boundary

The Draft PR Publisher node follows the accepted-success route. It sends only an empty POST body to the authenticated local runner's `/v1/runs/{run_id}/publish`. Its convenience checks reject contract rejection, reported failure, interrupted execution and incomplete/unknown evidence before dispatch. These checks are not authority: the host reevaluates the dispatch-pinned contract against its frozen envelope. A forged graph verdict cannot replace that data.

Only contract acceptance with explicit task success, completed executor status and independently established `evidence_complete: true` admits `publication_pending`. The current real runner still lacks that completeness closure, so it remains unknown and cannot pass this gate. An already-pushed, verified artifact is required; this publisher does not push an agent checkout or create a new bundle.

The publisher uses the existing mediation journal: the fixed effect identity is persisted as unknown before provider dispatch. A complete rejection is failed; a lost response, inconclusive readback or process loss stays unknown and never causes an automatic resend. Successful readback must identify the exact draft PR number, repository, head branch and commit, base, title, body and marker. Completion is publication acceptance at that scope, not proof that the code is correct.

A local mediation exception is classified from the durable effect row, not its exception type: no intent or a recorded complete rejection may be failed; an unknown intent or confirmed write followed by an error remains unknown. Early or concurrent duplicate publish requests observe the current phase without ending the agent lease or interrupting the first publication. The controller admits only one publication call per run at a time.

## Termination and recovery

Completion, contract rejection, failure, uncertainty, cancellation and expiry revoke the same grant and finish its lease. Cancellation or expiry racing a remote write cannot undo that effect: preserve its journal receipt and never relabel the cancelled/expired handoff as successful. The publisher node also treats a lost HTTP response as unknown, does not follow redirects and exposes only sanitized phase and publication state.

The controller keeps the lease heartbeat through validation. Runner/controller death stops that heartbeat; the existing independent service revokes before exact owned-container cleanup. Its startup sweep and hard grant TTL retain the 60-second orphan bound. No new service configuration is activated by this design. Host shutdown/startup composition must explicitly cancel/recover controller-owned handoffs.

## Verification boundary

Credential-free checks must cover accepted draft publication and exact readback, non-success refusal, forged graph operations, foreign or unconfirmed artifacts, changed requirements, in-flight effects, deadline-preserving renewal, clock rollback, cancellation/expiry during publication, no resend after uncertainty, explicit startup recovery and lease loss while another run remains usable. Pinned Langflow checks cover the real custom node against a fake local response, without a live provider.

The bounded [#100](https://github.com/amadou-6e/laomedo/issues/100) and [#104](https://github.com/amadou-6e/laomedo/issues/104) prerequisite acceptance is recorded; #100's live-provider result is in [specs #344](https://github.com/amadou-6e/specs/pull/344). Live publication still requires [#139](https://github.com/amadou-6e/laomedo/issues/139)'s separate model-turn cap and scoped identity. Native precheck acceptance, independently verified real-run completeness and a deployed graph-to-publisher demonstration are not established by fake transports.
