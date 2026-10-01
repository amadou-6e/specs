# Local Langflow skill-agent pilot

Status: implemented prototype, verified 2026-10-01. This is the bounded
single-user Codex route. The component specifications remain target product
contracts; the pilot does not implement all of them.

Implementation: Laomedo [runner PR #13](https://github.com/amadou-6e/laomedo/pull/13),
[Langflow PR #14](https://github.com/amadou-6e/laomedo/pull/14), and
[evidence PR #15](https://github.com/amadou-6e/laomedo/pull/15), stacked on
[Skill Draft core PR #5](https://github.com/amadou-6e/laomedo/pull/5).
The tested implementation is commit `5e14c7a`; sanitized evidence was added
in `8bfd0af`. These identify branch work, not a claim of merge to `main`.

## Execution and ownership

The saved Langflow flow connects Chat Input, Laomedo Skill Agent, and Chat
Output. The component sends a task, model and effort, and exact whole-skill
ref to `http://host.docker.internal:8765/v1/runs`. The host runner listens on
`127.0.0.1` only; the observed host uses Docker Desktop on Windows.

Each fresh run gets an independent workspace copied from the source. The
runner resolves a content-addressed bundle and validates its file hashes,
then materializes it under `.agents/skills/<skill_id>` before calculating the
effective workspace hash. Source, effective, and post-run hashes are distinct.
Successful runs retain post-run snapshots. Failed and cancelled runs preserve
received raw events and identity without claiming completed output.

The runner owns records, snapshots, raw events, and a cumulative turn ledger
outside every Git working tree. Execution starts and closes Docker app-server
processes; native sessions persist in the existing private volume. The pilot
reuses the explicitly authorized single-user ChatGPT login in that volume,
with no new credential copy. Production credential lifecycle remains with
[specs #129](https://github.com/amadou-6e/specs/issues/129).

## Frozen runtime and permissions

| Item | Tested value |
| --- | --- |
| Codex CLI | `0.159.2` |
| Codex image | `laomedo-codex-boundary:0.159.2` |
| Codex image ID | `sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239` |
| Permission file SHA-256 | `a14cd7e8abb4216b16d29e55809c2c3c9a9c33cc0196fd459fc033aaaa1ea4c4` |
| Langflow | `1.12.3` |
| Langflow image digest | `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0` |
| Requested and effective model/effort | `gpt-6-luna`, `low` |
| Whole-skill revision | `sha256:a12c212a57a9bc8fa3f0ecd834c09f9576a37ee89e21c62a096b1213fcc2bef8` |

The pilot retains the grant and mounts from the
[Docker feasibility study](../feasibility/docker-skill-draft.md). Its private
workspace is writable; canonical and sibling-store mounts are protected.
This is not a selectable general read-only grant. Permission redesign and
broader network-isolation work are deferred. Hosted and multi-user deployment
are outside this iteration.

## Adapter contract

`POST /v1/runs` accepts the following narrower request. The runner resolves
the bundle's file hashes from the registry and validates model/effort support
before reserving a turn.

```json
{
  "task": "Read the fixture with a shell tool.",
  "model": "gpt-6-luna",
  "effort": "low",
  "skill_ref": {
    "skill_id": "laomedo-pilot",
    "revision_id": "sha256:a12c212a57a9bc8fa3f0ecd834c09f9576a37ee89e21c62a096b1213fcc2bef8",
    "tree_hash": "sha256:a12c212a57a9bc8fa3f0ecd834c09f9576a37ee89e21c62a096b1213fcc2bef8"
  }
}
```

The Langflow result contains `answer`, `run_id`, native `thread_id`, `status`,
`skill_revision`, `skill_use_evidence`, `trace_ref`, and `usage`. Chat Output
renders this object as JSON text. The component returns inner `usage: unknown`
and conservative `skill_use_evidence: offered`; the acceptance report can
separately identify observed native reads. A skill read does not prove
compliance with every rule.

Langflow's run endpoint requires its own server API key, even with auto-login
enabled. That key authenticates to Langflow, not to the model provider.
Credentials, raw skill content, and private runner paths do not belong in the
saved flow or this specs repository.

## Resume, errors, and limits

`GET /v1/runs/{run_id}` returns the persisted record.
`POST /v1/runs/{run_id}/resume` requires `task`, `model`, `effort`,
`expected_thread_id`, and `expected_post_run_hash`. Resume verifies the native
thread, profile, runtime pins, workspace and snapshot hashes, and protected
mounts before reopening the same thread. The saved Langflow node starts fresh
runs; the observed resume used the runner API.

Missing snapshots return HTTP 400 with `post_run_snapshot_mismatch` before
reserving a turn. `POST /v1/runs/{run_id}/cancel` returns HTTP 202 when accepted.
The original runner invocation then returns HTTP 502 with terminal status,
identity, and partial events. The Langflow component raises an error with
the run ID and category, falling back to terminal status when needed.

The runner defaults to a zero-turn cap. Reservations persist before dispatch;
submitted timeouts and cancellations count. The observed cap was exhausted at
**4/4**. A subsequent request returned `model_turn_cap_reached` without a native
thread or ledger change. Restart does not reset this ledger. Additional model
tests require a newly authorized bounded budget.

## Observed acceptance

| Check | Observation |
| --- | --- |
| Saved-flow execution | Real answer `amber`, count `3`, run/thread IDs, pinned revision, and trace ref returned |
| Native skill read and tools | Skill-read and fixture/marker commands matched start/completion IDs and exited 0 |
| Output file | Host inspection confirmed `pilot-marker.txt` contained `FIRST-RUN` |
| Restart/resume | Same native thread read the marker after host-runner restart and a new app-server; snapshot hash unchanged |
| Fresh-run independence | Second Langflow run used a different thread; command output and host inspection confirmed no prior marker |
| Missing snapshot | HTTP 400, `post_run_snapshot_mismatch`, ledger unchanged; held snapshot restored |
| Cancellation | Cancel followed a native command start; status `cancelled`, 39 events retained; Langflow HTTP 500 named the run and cancellation |
| Cap enforcement | Exhausted request rejected before native thread creation; ledger remained 4/4 |

The [sanitized acceptance report](https://github.com/amadou-6e/laomedo/blob/8bfd0af/examples/skill-agent-pilot/e2e-results.json)
was checked against private Langflow responses, native events, records, and
actual snapshots. The
[reproduction guide](https://github.com/amadou-6e/laomedo/blob/8bfd0af/examples/skill-agent-pilot/README.md)
records setup and the four test steps. Raw transcripts are not committed.

## Remaining target-contract work

| Capability | Current limit |
| --- | --- |
| Skill Revision node and isolated rules/examples | Whole-bundle materializer exists; flow embeds a frozen ref rather than a separate skill node |
| Langflow resume control | Resume verified through runner API only |
| Complete shared contracts | Narrower adapter implemented; generalized refs and definition-version correlation remain target work |
| Monitoring | Native IDs/results retained; automated skill-read projection, inner usage extraction, and full normalized subsystem incomplete |
| UI acceptance | Browser interaction untested; no new UI behavior is defined here |
| AGENTVIZ | Deferred at the user's request; earlier feasibility evidence remains historical |
| Crash interruption | Explicit cancellation tested; process-crash interruption not tested in this pilot |
| Claude parity | No equivalent model-backed result demonstrated |
| Production auth and tenancy | Deferred; existing private single-user login remains the prototype route |

This is a go for the tested local Langflow-to-Codex path. It does not satisfy
every original check in [Laomedo #11](https://github.com/amadou-6e/laomedo/issues/11)
or establish the full component contracts.
