---
title: Separate exact-container absence from grant revocation
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-11
applies_to: [laomedo]
supersedes: null
related: []
---

# Separate exact-container absence from grant revocation

## Status and source

Owner-confirmed prospectively on2026-10-11. Verbatim answer:
"Accept exact-container absence, with separate revocation proof".
Recorded on [#22](https://github.com/amadou-6e/laomedo/issues/22#issuecomment-6108964723).
This decision does not turn earlier incomplete evidence into a pass.

## Context and question

S2's independent controller saw the actual agent container before runner loss,
but the service's later watcher returned never_observed. The separate
[D1 fixture](https://github.com/amadou-6e/laomedo/blob/227e3d2/experiments/exp93/ATTACHED-CLIENT-D1-RESULTS.md)
was auto-removing before one second after attached-client loss, without a service.
D1 does not establish S2's cause or native app-server behavior.

## Discussion trail

The frozen test required service-attributed removal. The owner was asked whether
future tests should accept independent exact-container absence instead, keeping
grant revocation separate. The owner selected absence. These are different claims:
container gone, credential unusable, and who removed the container.

## Decision and scope

Future bounded orphan acceptance may establish stopped-container containment by
independently verified absence of its pre-loss label-verified exact container ID
within60seconds, together with an empty reserved name. Verify authorization
revocation separately within the same bound; container death is not revocation.
Keep removal attribution and the service's own cleanup result distinct.

The independent supervisor/startup-sweep architecture is unchanged. This selects
an acceptance criterion, not a new recovery mechanism or permission. Existing
[S1/S2 results](../experiments/orphan-lease/iterations/README.md) remain incomplete.
The current shared model ledger stays14/16; two turns remain. No new turn is
authorized beyond that budget and no consumed identity is reused.

## Consequences and verification

The [authentication contract](../subsystems/agent-execution/contract/authentication.md#prospective-orphan-absence-and-revocation-acceptance)
owns checks and failure semantics. A trusted independent controller can witness
the live exact ID before loss; a service-owned pre-loss record is not mandatory
for that particular experiment. Production service observability may improve
separately; do not forge its cleanup result to satisfy this criterion.

Unknown Docker responses, wrong labels, replacement IDs, missing pre-loss witness,
late absence, wrong grant or a refusal that dispatches a provider write fail the
check. Freeze prospective protocol/source and obtain independent pre-run review.

## Open questions and supersession

No real-agent acceptance is established by this record. #93/#22/Q11 remain open;
power loss, double failure, hostile code and production observability are not
accepted by this bounded choice. A new passing capture and post-run review are
required before promotion.
