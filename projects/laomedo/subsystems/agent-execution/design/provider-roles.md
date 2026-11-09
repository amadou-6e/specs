---
title: Equivalent provider roles and shared Docker ownership
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-11-08
applies_to: [laomedo]
supersedes: null
related: []
---

# Equivalent provider roles and shared Docker ownership

## Goal and ownership

Design target tracked by [Laomedo #277](https://github.com/amadou-6e/laomedo/issues/277), following [#275](https://github.com/amadou-6e/laomedo/issues/275) on existing `refactor/205`, PR #250; no competing branch or wholesale restart. Design baseline: implementation `a4661d4ce9508ac4f2fbd67f8425a031987c8f98`, specs `7cb8a89304d7681e5b87b1f58324a4c0434e82e9` (PR amadou-6e/specs#403). The owner selected this refactor and requires precise role definitions and reviewer approval before further implementation. No merge or issue closure is authorized here.

Equivalent objects must expose equivalent responsibilities through declared interfaces. Common Docker mechanics must actually be shared, rather than repeated in three implementations. Preserve the `Base<Role>` / `Codex<Role>` / `Claude<Role>` / `OpenCode<Role>` nomenclature. Reuse py-docker; do not build another Docker SDK.

## Target objects

| Role / defining module | Base and implementations | Assigned functionality | Excluded functionality / consumers |
| --- | --- | --- | --- |
| Application lifecycle, `base/agent.py` | Existing `BaseAgent`; three existing `{Provider}Agent` | Public start/resume/cancel/status, admission and locking, durable record ownership, interrupted-run recovery, freezing and publication dispatch. Shared `_execute` ultimately consumes the declared runner contract. | No concrete runtime fields or native RPC sequencing. Public interface adapters remain in `agents/interface`. |
| Invocation execution, `base/invocation.py` and provider `runner.py` | New `BaseAgentRunner`; `CodexAgentRunner`, `ClaudeAgentRunner`, `OpenCodeAgentRunner` | Execute one admitted attempt; native initialize/open/load/configure/prompt, correction sequencing, native result capture, post-close history, cleanup coordination. `run(request, journal, stop) -> InvocationResult`, synchronous host entry; native async loop remains on the creator thread. | run returns InvocationResult for every failure after the first journal reservation or lease acquisition, preserving settlement. Does not own application admission, mutate raw Agent records, freeze the workspace, select another model, or silently replace Resume with Fresh. Consumed polymorphically by Agent. |
| Docker resource lifetime, `base/runtime.py` | Retain `BaseAgentRuntime` as ABC plus shared concrete mechanisms; `{Provider}AgentRuntime` supply launch policy and topology | Shared exact-resource registration, launch and cleanup delegation to py-docker, creator-thread enforcement and cached fail-closed cleanup observations. Public `prepare(request: RuntimeLaunchRequest) -> RuntimeObservation`, `launch() -> RuntimeObservation`, `run_job(job: ContainerJob, *, cancelled=None, deadline=None, cleanup_seconds=None)`, `controller_stream() -> ControllerStream`, `close_controller(cause=None) -> CleanupObservation`, `shutdown(cause=None) -> RuntimeCleanupReport`. Base owns these mechanisms; provider hooks `_resource_plan(request)` and `_map_docker_failure(error, stage)` supply topology and stable error mapping. `prepare` starts dependencies but never the controller; `launch` starts the controller. Inputs are admitted configuration and collaborators, not prebuilt specifications dependent on as-yet unlaunched resources. | No ACP handshake/prompt/history/auth interpretation. Runner consumes this contract. close_controller returns uncertainty rather than raising; shutdown calls it if not already done. Do not force a single container per attempt. Provider specifics may configure mechanisms, not reimplement them. |
| Model discovery, existing `catalog.py` | `BaseModelCatalog` and three `{Provider}ModelCatalog` | Common `discover(refresh=False) -> ModelCatalogSnapshot`; zero model turns, exact advertised choices, native cache TTL and sharing. Inject discovery collaborator and admission gate rather than call Agent private methods. | Claude snapshot and OpenCode discovery/run exclusion remain explicit local collaborators unless a shared consumer emerges. Discovery does not call an attempt runner or consume a model turn. |
| Credential admission, existing `credentials.py` | `BaseCredentialProvider` and three `{Provider}CredentialProvider` | `admit(request) -> CredentialAdmission`: validated public binding plus explicitly excluded host-only launch material when needed. Dynamic lookup and native refresh ownership preserved. Native freshness/revocation probes remain provider-local runner collaborators. | Preserve native timing: Claude mirror-only pre-dispatch/resume admission differs from status checking; Codex volume mode persists `credential=None`; OpenCode receives its profile from typed composition. Remove success-only release stubs and universal token borrowing. Borrowed host login is never deleted/revoked. No secrets in representations, JSON, diagnostics or settings. |
| Command execution, provider `executor.py` | `BaseCommandExecutor`; `ClaudeCommandExecutor`, `OpenCodeCommandExecutor` | Typed `execute`, stop admission, signal owned jobs, `shutdown` with exact cleanup. HTTP/MCP only authenticate/translate. Shared consumers use declared methods and cleanup reports, never locks/flags. | Cancellation timing remains unchanged in this structural refactor. No fabricated native acknowledgement. |
| Codex persistent split service, `codex/split/executor.py` | Concrete `CodexExecServer` (rename current misleading role after callers migrate) | Typed registration value, persistent service health, assert_controller_isolated(identity: ContainerIdentity) from typed resource bindings, bounded preflight probe and closure. | Not a transient model-command executor; native model commands use ACP-registered exec-server. No fake sibling implementations or symmetry-only capability ABC. |
| Protocol and discovery collaborators | Shared concrete `AcpSession`; provider-local `CodexProtocolSession`; `ClaudeRuntimePolicy` | `AcpSession` takes `ControllerStream` and owns initialize/open/configure/prompt/named extension/disconnect, never process cleanup. `CodexProtocolSession` owns native handshake validation, registration, model paging and fixed probes, reused by runner, catalogue and Agent preflight. Claude policy remains Agent-lifetime spec/guard/lease/control-job policy owner. Claude discovery delegates control jobs through policy/shared mechanics; OpenCode discovery uses runtime prepare/run_job. | No new protocol ABC merely for symmetry. Preflight does not run an inference attempt. |
| Shared Docker delegation, `base/docker.py` | Concrete `AgentDockerMechanism(environment: Mapping[str, str])` pins its endpoint | Thread-neutral `recover(receipts)`, `run_job(job, *, cancelled=None, deadline=None, cleanup_seconds=None)` returning py-docker job CommandResult (distinct from Laomedo command result), and native session delegation. Own client per self-contained call; reuse py-docker jobs, sessions and receipt APIs. | No attempt state or provider policy. Shared by runtime scopes, worker executors, control jobs, history readers and startup recovery. |
| Lease / telemetry | Existing lease and telemetry objects | Runner acquires per-scope leases before prepare and passes grant bindings as request inputs. Leases are NOT resource-plan resources: the runner resolves them from RuntimeCleanupReport or transfers a surviving Codex lease to settlement. Runner owns publication registration; telemetry may be a plan resource. | Preserve provider-specific finish versus stop-heartbeat rules and publication host authority. |
| Activity, existing provider activity packages | `BaseActivityProjector` and three `{Provider}ActivityProjector` | `accepts`, `project -> ActivityProjection`; canonical read-time interpretation, native provenance and unknown usage/cost semantics. | Live execution capture remains inside runner: it establishes terminal truth and cannot be treated as optional read-time projection. |
| Registration | Existing `AgentProviderRegistry`, `AgentProviderDescriptor` | Trusted typed Agent/runner composition, declared capabilities, validated host configuration. | No graph-provided imports, executables or credential locations; no sibling provider imports. |

One runtime instance is one single-use resource scope; Claude's runner creates one per native turn. Session-scope prepare, launch, close_controller and shutdown execute on the creator thread. Self-contained jobs and `AgentDockerMechanism` are thread-neutral and own their clients per call. StopSignal is the cross-thread control input; worker results use typed reports. Runtime lifecycle is new -> prepared -> launched -> closed, with failed preparation/launch rolling back to closed. Remove `start`, `observe`, runtime `request_cancel` and `RuntimeLaunch` after migrating all consumers.

`ControllerStream` exposes only `write(data: bytes)` and `read_line() -> Line | None`, matching py-docker stream values. It has no close/remove method, container handle or credential access. Runtime returns this borrowed view only after launch, never an opaque runtime handle.

`ResourcePlan` is a trusted host-only ordered list of steps: id, depends_on, phase (prepare/launch), and builder receiving prior typed resource bindings. This allows specs to use live exec-server identities and broker ports without prematurely building them. Each resource supports close(cause); optional quiesce is a step field, present only for OpenCode workers in this refactor, preserving Claude cancellation timing. Optional stop_when callback belongs to the controller step: runtime enters stop_on at launch and exits it before close; monitor failure is retained in cleanup. Dependencies define closure order. Resource-plan policy remains provider-owned; generic allocation/registration/rollback and cleanup caching are shared. Builders/handles are never graph-selectable or serializable.

## Interface inspection checkpoint

Target ABCs are defined directly in base/ concern modules: invocation, runtime,
resources, credentials, commands, catalogue and Activity. The public base/__init__.py
exports those canonical contracts and BaseAgent for provider authors. Canonical
values remain in base/models/ concern modules. agent.py owns the shared lifecycle;
docker.py owns concrete AgentDockerMechanism. Internal concern/model imports use
defining modules to avoid cycles through the public initializer. The facade is an
explicit provider-authoring API, not a second set of class definitions.

Existing providers still inherit base/interim.py during inspection. These legacy
roles are internal and not exported over the new target roles; remove them only
when actual provider behavior and consumers migrate. This layout change does not
complete the [provider-authoring story](provider-authoring.md) or automatically register another provider.

Those declarations moved without changing behavior; remove this interim owner
when provider execution migrates to target interfaces. It is not a compatibility
promise or a completed behavioral migration.

Container-step builders return native `ContainerSession` specifications; shared
runtime code allocates the Docker session and produces its typed binding.
Non-Docker owned-resource builders may allocate brokers/telemetry under shared
rollback. Each plan declares exactly one launch-phase controller; stop monitors
are controller-only. This distinguishes launch policy from shared allocation.

Journal operations use separate typed values with native extensions confined to
non-shared keys. Settlement updates name their allowed fields; Agent retains
exclusive status/cancellation/snapshot demotion ownership. Attempt outcomes retain
completed, failed, cancelled, unknown, timeout and interrupted states and their
existing public error category, separately from allowlisted private diagnostics.
Deadline inputs remain optional where native policy has no whole-attempt deadline.
A missing controller observation means never allocated, not cleanup uncertainty.
All sensitive target values hide input data in validation-error text.

## Invocation nomenclature

The execution contract uses BaseAgentRunner.run(InvocationRequest, journal, stop)
returning InvocationResult. InvocationContext carries one admitted execution's
host context; BaseInvocationJournal / InvocationJournal names its durable write
port. Provider targets use CodexAgentRunner, ClaudeAgentRunner and OpenCodeAgentRunner
in runner.py. Provider authors import base contracts from laomedo.agents.agents.base.
Python definitions live directly in base/invocation.py, base/runtime.py and
other concern modules, with values in
base/models/invocation.py; there are no retired-name forwarding aliases.

One invocation can contain several native model/tool turns. It is distinct from
host run identity, saved conversation identity and persisted activity-attempt
records. Existing attempt_id fields, record shapes, open_activity_attempt record
construction, validation codes and cancellation semantics retain their spelling
and behavior. This terminology amendment does not migrate live providers or repair
the resource-builder abstraction. StopContext's combined request/observe contract
is not renamed to a read-only cancellation token. Historical review below covers
the earlier design; this nomenclature amendment is unreviewed until explicitly checked.

## Supporting contracts (not three mandatory provider implementations)

| Object | Required interface / guarantees |
| --- | --- |
| `BaseInvocationJournal` / Agent-owned `InvocationJournal` | `reserve_ownership`, `bind_native_session`, `reserve_dispatch`, `mark_dispatched`, `record_turn`, `record_lease`, `register_publication(lease)`, `bind_runtime_identity`, `record_correction_pending`, `record_scope_cleanup`, `record_evidence`; typed Pydantic values and atomic writes under the existing control lock. A successful durable write precedes its protected side effect. Preserve existing persisted field presence, extensions and codes. |
| Concrete `StopSignal` | Event-compatible `is_set`/`wait`, `request(reason)`, `source(reason) -> StopSource` with Event-style `set()`, and `subscribe(callback)` returning an unsubscribe handle. First private reason retained; subscriptions must handle already-set signals and concurrency without invoking callbacks under the state lock. Distinguish private user/deadline/lease/auth/executor/mediation reasons. Preserve current public projection exactly: `cancel_requested` still derives from is_set, status/cancel_confirmed unchanged. A semantic correction is separate work; acknowledgement remains a separate native fact. |
| `BasePostFreezeSettlement` / Codex settlement | `settle(view: SettlementView) -> SettlementResult`, `abort(view: SettlementView, failure: FailureObservation | None) -> SettlementResult`. Outcome carries settlement for ANY status with a surviving lease. Agent settles only completed frozen attempts and aborts all others, including failed/cancelled/freeze-failed paths. View is a deep copy; result returns verified cleanup, detail, stable code and typed declared record updates, never raw shared mutation. Exceptions mean verified=False. Preserve existing demotion on unverified settlement: failed/container_termination_unverified with snapshot_ready/post_run_hash/output_ref cleared. Lease finish versus stop_heartbeats remains provider policy. No no-op sibling settlement. |
| `RuntimeCleanupReport` | Per-controller observation and named resource observations, aggregate fail-closed confirmed, primary failure observation and stable code. Shutdown uncertainty is returned (not thrown); prepare/launch roll back all started resources on failure, raise the mapped RunnerError retaining primary observation, and cache a closed report. Exact-identity cleanup_exact fallback remains provider policy after ownership journaling: Codex when controller cleanup is unconfirmed or handle absent, Claude only when handle absent. Repeated cleanup cannot turn unknown into success or redo destructive work. |
| Provider activity-attempt construction | `BaseAgentRunner.open_activity_attempt(context) -> ActivityAttemptRecord` preserves each provider baseline and persisted shape. The Agent owns journal persistence. Transient provider-private record fields become runner state. |
| Pydantic boundary values, concern-owned `models.py` | `InvocationRequest`, `InvocationResult`, journal operation values, `RuntimeLaunchRequest`, admitted resource plan, `CredentialAdmission`, registration and cleanup reports. Reuse existing canonical bindings/observations rather than duplicate them. Secrets and live handles are host-only, excluded from serialization and repr. Explicit external adapters preserve public/persisted payloads. |

## Required lifecycle equivalence and native differences

| Path | Codex | Claude | OpenCode |
| --- | --- | --- | --- |
| Fresh | Admit; optional split service and controller; initialize; live model validation; journal native binding and turn reservation before prompt | Admit auth; per-turn controller and workers; initialize; journal native binding before prompt; correction may allocate another turn scope | Prepare environment without claiming launch; model/auth checks and history baseline; launch controller; bind before prompt |
| Resume | Load exact saved conversation, never Fresh fallback | Load exact saved conversation; exclude replay; corrections may use new container with same conversation | Validate runtime fingerprint; load saved conversation; baseline absence means partial evidence, not zero usage |
| Shutdown | Controller then unblock/disconnect ACP, executor and remaining resources; preserve supervised lease for settlement where required | Close controller on creator thread, disconnect ACP and drain workers; resolve each turn lease; preserve original failure | Close controller, disconnect ACP, drain workers and reconcile receipts; history after confirmed closure; history cleanup uncertainty is fatal |
| Freeze / settlement | Freeze only after exact owned-resource cleanup; then publication/evidence/lease settlement | Freeze after all turn scopes and workers settle | History completes before freeze; telemetry export remains best-effort after freeze |
| Cancellation / failure | Preserve native acknowledgement and cleanup as separate facts; lease loss is distinct from user cancel | Preserve existing worker cancellation timing pending separately authorized behavior change | Preserve existing dispatch/worker cancellation timing and receipt recovery guarantees |

Resource ordering is explicit: quiesce resources (including OpenCode worker signaling), close controller on creator thread while its event loop remains live, disconnect ACP, then shutdown/drain remaining workers and resources. Shared resource dependency order preserves native differences, not blind reverse-order deletion. ACP currently closes Docker too: remove this dual ownership only together with all consumers, including catalogue discovery, preflight and exception paths. Runtime is the single process-cleanup owner; runner orders disconnect after close_controller and before shutdown. The SDK Connection.close cancels tasks and returns; the actual constraint is the blocking asyncio.to_thread reader, whose thread must reach EOF before asyncio.run closes its default executor. Preserve constructor/partial-launch fallback and provider failure mappings, including ClaudeRuntimePolicy.

## Bounded implementation checkpoints

1. Document precise methods, models, source-to-target responsibility map and actual supported host composition and fail-closed missing-composition paths for each provider; amend canonical draft specification and READMEs before moving code. Preserve existing branch/PR ownership.
2. Implement shared runtime mechanisms and typed launch/cleanup ownership; migrate one coherent resource operation across all three providers with focused controls. Keep incomplete protocol extraction explicitly incomplete, not hidden behind aliases or checker exemptions.
3. Introduce Agent-owned journal and reasoned stop context; extract the three runners with explicit runtime/catalogue/credential/executor dependencies. Move public orchestration into shared Agent only after all three paths implement its contract.
4. Migrate catalogue/credential/command/private-state consumers and Codex settlement; remove obsolete role methods, factories and symmetry-only interfaces; update examples, diagrams, registration and packaging.
5. Final full-delta reviewer check, CI and owner real-workflow acceptance. Commit/push each coherent block promptly to the existing draft PR; no merge while any acceptance item remains open.

## Definition of complete

- [ ] Review-approved design records exact method signatures, ownership, error outcomes and the provider responsibility/callsite map; canonical specs agree with implementation and retain their actual maturity.
- [ ] All three Agents consume `BaseAgentRunner` equivalently. Shared callers never inspect concrete provider state, call undeclared methods, use duck-typed fallback factories, or reach through opaque handles. Explicit provider-local collaborators remain local and documented.
- [ ] One shared implementation owns generic Docker lifetime mechanisms through py-docker. All three runtime classes use it; provider differences are admitted specification/topology policy. Sessions, jobs and receipt recovery (workers, history and control jobs included) delegate through the shared mechanism; provider code supplies spec builders and stable failure mapping. No duplicated launch/removal algorithm remains in migrated scopes.
- [ ] Process cleanup has a single owner; ACP disconnect cannot secretly close Docker. Constructor failure, prompt failure, cancellation, normal completion, worker drain failure, cleanup uncertainty and repeated shutdown preserve exact scope and primary/cleanup failure evidence.
- [ ] Durable native binding and dispatch reservations precede their native side effects; interrupted-run recovery still works before concrete initialization. Existing public/persisted schemas, identity, graph IDs and failure codes remain supported.
- [ ] Codex post-freeze publication/lease settlement and abort are covered; Claude multi-scope correction and OpenCode post-close history preserve their required ordering.
- [ ] Provider authentication paths are wired in each currently supported composition; replace OpenCode untyped transport_factory with a typed host-supplied composition, preserving opencode_isolated_transport_required when absent. Adding production OpenCode wiring is separate work. Secret serialization/redaction, dynamic lookup, child environments, native refresh ownership and fail-closed admission remain intact.
- [ ] Zero-turn model discovery preserves native caches, shared refresh and OpenCode run exclusion. No automatic substitution, Fresh fallback, added inference or artificial unsupported/no-op capability.
- [ ] CI architecture checks cover declared public surface, signatures, typed consumer/factory boundaries, private-state leakage and dependency direction with positive/negative controls and documented static limits. Existing red guard reaches zero through correct ownership, not baselines/exemptions/renaming calls private. No hard-coded historical violation counts or retired-state tests.
- [ ] Concern-owned tests cover the current lifecycle invariants above for each provider; relevant source and installed-package checks, formatting and every configured CI check pass at exact final head. Deterministic doubles are labelled supporting evidence, never live acceptance.
- [ ] Actual composition and absence are traced: OpenCode currently has no default production wiring; this is a recorded real-acceptance blocker, not permission to add a new feature. Typed host-supplied composition remains supported. Actual supported Fresh, Resume, status, cancellation, discovery, Activity and failure/recovery stories receive the owner's required real-provider/graph acceptance; missing permission/environment is a recorded blocker. No new model probes are authorized merely by this issue.
- [ ] Exact final substantive implementation/spec diff is independently reviewed; confirmed blockers get the prescribed focused recheck. Final owner acceptance and specification merge dependencies remain separate from reviewer design approval.

## Scope boundaries and open evidence

This is a structural ownership refactor. Do not silently change correction policy, cancellation timing or the meaning of persisted `cancel_confirmed`. Existing suspected defects receive explicit evidence and a separately approved correction if required; they must not be disguised as moves. Keep open and unchanged the separate DESIGN-04 persisted cancellation correction, DESIGN-09 worker timing, DESIGN-10 Claude stream-JSON discovery spec ruling, and DESIGN-11 correction policy. Verify native provider contracts before migrating affected paths. ACP SDK close ordering and blocking-reader distinction were inspected by reviewer; validate shutdown behavior deterministically. OpenCode production composition is absent by current contract, not a missing feature to implement here. GitHub authorization remains host-owned. Preserve unrelated work, experimental archives and deferred campaigns. Do not change CI configuration/required checks, upgrade native dependencies, run live model probes, merge or close issues without applicable authorization.

## Review status

Claude focused design recheck: **APPROVE**, current Codex reviewer session62a1a754-1af6-477f-aa14-0b000a571381, low effort, 300-second bounded review; implementation baselinea4661d4c and specs7cb8a89. DESIGN-13..23 resolved; nonblocking DESIGN-24..30 corrections incorporated above. Safe to start checkpointed implementation. This is design approval only, not implementation/spec/PR acceptance. Earlier design verdict REVISE: DESIGN-01 durable journal, DESIGN-02 post-freeze settlement, DESIGN-03 dual cleanup ownership, DESIGN-04 stop-reason conflation and DESIGN-05..12 contract/consumer gaps. Owner explicitly requires shared Docker mechanics and retained role naming. Reviewer recommendations cannot override those decisions. Implementation begins only after this design has no unresolved blocking findings.
