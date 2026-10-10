---
title: Resume lifecycle and synthetic feedback acceptance audit
status: draft
kind: implementation-record
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Resume lifecycle and synthetic feedback acceptance audit

Inspected base: Laomedo develop at
`8204056c21e388b975909377cf552fcf6d81e822`. Implementation/test revision:
[99da4d4f8493ef410b5a4dad75b5c1ef323dd87c](https://github.com/amadou-6e/laomedo/tree/99da4d4f8493ef410b5a4dad75b5c1ef323dd87c).
The changes are review candidates until merged; this record does not change
issue state, maturity, permissions, deployment or model-turn authorization.

## #20 resume and lifecycle

Governing [node contract](../subsystems/agent-execution/contract/langflow-node.md).
Credential-free verification: 320 host tests passed, six skipped; 30 component
tests passed in cached Langflow/lfx 1.12.3 image
`sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`,
network disabled and source mounted read-only. No model turn or personal login
was used. These are deterministic checks, not fresh live acceptance.

| Issue criterion | Check and boundary |
| --- | --- |
| Structured identity and exact snapshot | Node accepts Data or manual JSON with completed state, native thread, model/effort and SHA-256 snapshot; missing/invalid/noncompleted references fail before HTTP |
| Profile/thread/snapshot consistency | Runner checks persisted bindings, workspace, canonical mount and snapshot. New profile/thread/hash tamper test observes zero additional transports and unchanged synthetic turn ledger; existing missing/modified snapshot tests remain |
| No fresh fallback | Response run mismatches and changed completed native thread fail explicitly; one resume POST only |
| Prior output wiring without private paths | Pinned Graph.from_payload/arun connects a fresh node's Run Reference Data output to the next node's Prior Run port; exactly one fresh and one resume dispatch |
| Partial evidence after failure | Failed/timeout/cancelled resume errors retain public run/thread/trace projection through RunnerResultError.run_reference; profile/workspace canaries excluded; artifact absent in failure fixtures |
| Transport ambiguity | Resume timeout retains known run/trace with unknown current outcome; no retry, no fabricated completion or confirmed cancellation |
| Cancellation propagation | Existing pinned component and recorded UI Stop evidence establish fresh/start cancellation attribution; explicit status/cancel use the known run and reject another run's response. A client Stop during synchronous resume does not automatically cancel it. #22 owns that remaining lifecycle/race guarantee; retain the run reference and use explicit status/cancel rather than claiming remote cancellation |
| Saved example and instructions | flow.json embeds the updated source; components/README.md documents exception recovery. No installed flow or existing server was activated |

Reproduce from the implementation checkout:

```powershell
uv run --no-project --python 3.12 --with 'PyJWT[crypto]==2.15.1' --with truststore==0.10.4 python -m unittest discover -s tests
```

Run `python tests/langflow/test_codex_component.py` inside the exact pinned
image with this checkout at `/workspace`, `PYTHONPATH=/workspace`, network off
and read-only source. The initial default host Python lacked PyJWT and failed
test imports; the isolated uv run with declared dependencies resolved that
environment failure. It is not a product failure or a model attempt.

Independent review found a pre-dispatch error-path bug: a refusal body with
`status: failed` and no run ID was attached to the prior run as failed. The
correction overrides that request-only outcome to unknown; its regression uses
the actual runner error shape. The structured exception reference is available
to code callers. A failed UI node emits no Data output; use its known run ID
with status/cancel for recovery.

The older file-backed runner has a synthetic restart/resume check. App-owned
ChatGPT connections intentionally refuse resume across runner-instance restart
and changed account identity. This audit does not remove that restriction or
claim universal restart/resume across authentication modes. Historical live
checks remain in [native node implementation](native-langflow-node.md).

## #123 synthetic experiment acceptance

The [S1 record](../experiments/pr-check-feedback/iterations/s1/results.md)
was merged in specs #300 at `15b147bd13ffdd244ddcc0480864ab163b61d21a`.
[Implementation audit](https://github.com/amadou-6e/laomedo/blob/c76ee650dbddbf72cc8a2b7544798443ace56821/experiments/exp123/ACCEPTANCE-AUDIT.md)
maps each issue acceptance item to the frozen protocol, seven captured cases,
identity journal, bounded branch routing and independent reviews.

Read-only replay passed all three probe/evidence tests, verified all 15 captured
file hashes and reconstructed the recorded outcomes. Negative controls catch
extra invocations, wrong graph, stale head and fabricated terminal results.
There was no new graph dispatch or modification to S1 captures. Replay is not
an independent fresh runtime replication.

The experiment acceptance is met at its amended synthetic scope: one live
Graph.arun, custom polling waits and an unrolled two-invocation correction cap.
Graph completion with Result2 failed is not successful task completion. Stop
is explicit controller cancellation, not UI Stop; backend restart does not
resume the old graph. Existing egress, telemetry and deadline limits remain.

The broader objective remains unfinished. #104/#105 owns active-run grants,
trusted staging and literal Git/gh delivery. Production PR-check components,
authenticated ingress, real provider delivery and ownership checks, real-agent
head changes and disposable-repository acceptance are not proven by S1. #123
remains their tracking context; no closure or broader acceptance is implied.
Live testing needs a prospectively reviewed protocol, explicit write scope and
a new model-turn budget. This audit uses zero model turns and provider writes.
