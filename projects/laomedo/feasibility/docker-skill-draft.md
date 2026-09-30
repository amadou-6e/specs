# Docker Skill Draft feasibility, issue #146

Status: **go for a bounded single-user local prototype; no-go for hosted or
multi-user use on this evidence**, 2026-09-30. This is a feasibility finding,
not an approval to promote a skill or deploy a runner. It compares the Docker
route with the [OS-sandbox Skill Draft study](122.md) under the same pinned
synthetic edit policy.

The source experiment is
`amadou-6e/laomedo/experiments/feasibility/docker-skill-draft/`, on local
branch `feat/146`. Its JSON observation files are sanitized; raw event streams,
session state, and the ChatGPT login remain outside Git. The older source
branch is reviewed in [Laomedo PR #4](https://github.com/amadou-6e/laomedo/pull/4),
but its Docker additions and the new `feat/146` branch are local pending
publication approval. The exact local spike commit is `d2525cd`; it is not
yet reachable remotely. Link the published commit and PR here before treating
the report as a complete remote deliverable.

## Predeclared checks and observations

The [#146 issue](https://github.com/amadou-6e/specs/issues/146) declared the
pass conditions before its two new model turns. The original #122 ledger
remains at 7/7. The separate Docker ledger retained its first two attempts and
is now **4/6**. Turns 3 and 4 used `gpt-6-luna` at low effort with the existing
isolated ChatGPT handoff; they have no direct OpenAI Platform API bill.

| Condition | Result and evidence |
| --- | --- |
| Allowed edit, pinned policy and base, distinct draft, patch and fixed case | **Verified.** Turn 3 edited `SKILL.md`. The policy hash is `sha256:0d0c67179033c5948276b3fe32f8e3e222f9995f3b5fb59b62f4a4ae0d6c4c14`. The pinned base and candidate tree hashes differ; the candidate has one changed path, a patch, no structural violations, and a passing deterministic fixed case. Raw workspace artifacts are handled separately below. |
| Agent-originated forbidden write | **Verified for the synthetic store.** Turn 3's completed `commandExecution` item invoked a pinned validation script, reported `/store/sentinel.txt`, exited 2 with an OS denial, and the host sentinel was unchanged. The store was mounted writable in Docker and an unsandboxed positive control wrote to it, isolating Codex's inner Linux restriction. This corrects the earlier Docker turns, where the agent merely claimed a denial without a command event. |
| Canonical, path traversal, escaping symlink and file type | **Verified on the tested paths.** The canonical mount was read-only. Direct Codex commands were denied writes to the writable sibling store, traversal through `/draft/../store`, and a symlink from the draft to the store. The inventory rejected the symlink; policy validation rejected an extra script even though the OS allowed writing it inside the draft. The canonical source stayed unchanged. |
| Partial failure, timeout, missing or corrupt snapshot, concurrent base change | **Verified with synthetic commands and deterministic guards.** Partials remained observable but ineligible; missing or corrupt snapshots did not replace the draft; a changed canonical hash and revision blocked promotion eligibility. No promotion was attempted. |
| Persistent resume from the last post-run files | **Verified.** Turn 4 restarted the app-server, resumed turn 3's native thread, mounted a fresh draft restored from the pinned post-run candidate hash, and made an observed read command whose result contained the added example line. The restored draft and canonical/store files remained unchanged. |
| Credential and personal-profile boundary | **Verified for the tested exact path and mounts.** The personal Codex profile and Docker socket were not mounted. The persistent Docker volume held one earlier copy of the isolated #120 login; app-server `command/exec` was denied reading its `auth.json`. The source and Docker copies were still byte-identical after turn 4. This does not prove refresh, rotation, revocation, or multi-user isolation. |
| Network boundary | **Verified for the tested loopback and external calls.** Direct connections from a credential-free Docker container succeeded. The same calls under the named Codex sandbox reached the test process but failed with `EPERM` for loopback and `EAI_AGAIN` for external DNS. A no-model app-server command under the real runner profile also started and failed external DNS with `EAI_AGAIN`. Other protocols and hosting arrangements were not tested. |

The raw turn 3 workspace contained empty `.agents`, `.codex`, and `.git`
directories created during Codex execution. A no-model diagnostic placed
`.codex` and `.git` at `thread/start`. The raw inventory correctly rejected
the tree. Candidate materialization preserves that raw evidence, checks that
only those three exact runtime directories exist and are empty, and copies
only approved `SKILL.md` content into a separate candidate. It fails closed
for nonempty runtime directories or any extra path. A Docker-created symlink
also exposed a Windows host-path case where `Path.is_dir()` raised an OS error;
the inventory now converts that into a deterministic rejection instead of
following or silently omitting the entry.

Turn 3's native thread and turn IDs, per-turn event counts, and token usage
are in `model-observations.json`. Its final cumulative usage was 62,849 total
tokens, including 56,320 cached input tokens. After turn 4, the same native
thread reported 95,813 cumulative total tokens, including 87,552 cached
input tokens. These are provider-reported thread totals, not independent
request lengths or a billed USD amount. The raw streams remain private and
can be matched by the recorded native IDs.

## Minimum boundary and decision

Use a non-root container with only a disposable draft mounted writable, the
canonical skill mounted read-only or omitted, no Docker socket or personal
profile mount, and a persistent runner-owned `CODEX_HOME` separate from
disposable drafts. The named [Codex permission profile](https://learn.chatgpt.com/docs/permissions)
must deny the credential path, constrain writes to the draft, and disable
agent-command network access when the controller still needs model traffic.
The [Linux sandbox](https://github.com/openai/codex/blob/main/codex-rs/linux-sandbox/README.md)
applies those command restrictions; the [Docker mount configuration](https://docs.docker.com/engine/storage/bind-mounts/)
provides an independent read-only canonical boundary. Record actual mounts,
effective policy, command events, host sentinel checks, and both source and
candidate hashes. Validate and freeze a separate candidate before review;
never promote directly from the raw agent workspace.

This is a **go** for the tested local, single-user Skill Draft prototype.
It avoids repeated native Windows sandbox provisioning prompts and satisfies
#146's filesystem and resume conditions with observed agent events. It is a
**no-go for claiming production confinement or hosted/multi-user readiness**:
the ChatGPT login handoff remains a copied single-user token, exact-path denial
has not been audited against every credential access route, and the network
test covers only selected paths. The production credential lifecycle is
owned by [#129](https://github.com/amadou-6e/specs/issues/129); the broader
build-versus-adapt and risk synthesis belongs to
[#124](https://github.com/amadou-6e/specs/issues/124).
