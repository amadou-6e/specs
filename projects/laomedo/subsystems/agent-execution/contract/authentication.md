---
title: Runner authentication and credential lifecycle
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-07
applies_to: [laomedo]
supersedes: null
related: []
---

# Runner authentication and credential lifecycle

This remains the target contract for issue #129, not a hosted release
authorization. A bounded single-user local Codex prototype is implemented at
[Laomedo `b76b6f3`](https://github.com/amadou-6e/laomedo/blob/b76b6f3a3e51c345a4cc49a3a141527317a255d9/experiments/feasibility/107/README.md)
in draft PR #109. Its two live turns do not establish refresh rotation,
sign-out with OpenAI, multi-user custody or hosted isolation.
It consumes the [skill-discovery](../../../research/runner-feasibility/sources/119.md),
[Codex runner](../../../research/runner-feasibility/sources/120.md),
[Claude runner](../../../research/runner-feasibility/sources/121.md),
and [feasibility synthesis](../../../research/runner-feasibility/sources/124.md) results. The original feasibility report changed no credential,
account, or provider configuration; the later #107 prototype is recorded below.
Time-sensitive provider claims were checked on **2026-10-02** against the linked
OpenAI token/app-server and Anthropic authentication/federation documentation;
the provider's broader eligibility and lifecycle claims remain unverified.
The contract was re-reviewed on **2026-10-07** against the selected orphan
policy and the merged local OpenCode adapter. The local-project eligibility
statement below was checked on **2026-10-07** against OpenAI's linked cookbook
and quickstart; the other external provider claims were not refreshed, and no
new credentialed turn was run during that document review. The later #107
bounded check connected one app-owned ChatGPT account and completed two
`gpt-6-luna` turns on the pinned split runner before and after process restart;
see the separately pinned [validation evidence](../validation.md).

## Decision and deployment gates

Laomedo needs a persistent **credential broker** owned by the runner, separate
from disposable workspaces, agent tool processes, skill bundles, snapshots, and
traces. A run selects a provider credential reference and records its mode and
identity provenance, never the secret. The broker refreshes or rotates the
credential and launches a provider controller with a constructed environment.
The controller's tool executor must receive a separate environment with no
credential, token file, refresh state, or secret-store access. Merely setting
`CODEX_HOME` or `CLAUDE_CONFIG_DIR` does not prove that boundary.

The selected agent provider's account connection is the only sign-in required
to run that agent. Laomedo does not add a Windows Hello or FIDO2 ceremony, a
second operator login, or a Docker credential prompt for stage approval. Run
grants and mediated GitHub capabilities still scope actions, but the current
same-user local Work Graph grant does not authenticate human approval; see the
[Work Graph contract](../../work-graph/contract/work-graph.md).

For a **single-user local Codex pilot**, the preferred design candidate is an
app-owned [Sign in with ChatGPT](https://developers.openai.com/siwc/quickstart)
connection and the documented [Codex app-server token
path](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server).
The opt-in local prototype uses its own broker store and no copied IDE login.
Actual refresh rotation remains untested. OpenAI's
[local-project guide](https://developers.openai.com/cookbook/articles/sign-in-with-chatgpt)
explicitly includes personal projects that run locally, alongside open-source
projects and selected private apps. The
[quickstart](https://developers.openai.com/siwc/quickstart) summarizes the
program more narrowly as open-source partners and selected private clients.
The cookbook says plan usage includes "personal projects that run locally";
the quickstart says it is available to "selected private clients". The
local-project route supports trying Laomedo privately. The bounded #107 check
established consent and one account's ability to run two eligible model
requests, but it does not establish other accounts' or hosted eligibility.
Only a validated OAuth grant with `chatgpt.tokens.use.direct` followed by a
successful model request establishes local plan access for that account and
request. Hosted eligibility remains a separate decision. The broker
must test whether app-server tool
subprocesses can see its access-token environment; until an observed denial
exists, this mode is **not approved for untrusted tool execution**. These are
design gates, not claims demonstrated by the #119-#122 probes.

A later #107 credential-free negative control on pinned Codex CLI 0.159.2
showed an unselected `apply_patch` call writing into the credential
controller's private profile, although shell commands used the executor.
The local runner therefore refuses app-owned split preflight and dispatch
before any model turn until a reviewed configuration and a probe prove that
every offered file and command tool stays in the executor. The earlier two
successful live turns establish this account's local access and reuse across
runner processes, not the protected tool boundary. The four additionally
authorized model turns remain unused while this gate is closed.
The tested disposable `PreToolUse` deny-hook and explicit profile-path deny
did not stop this code-mode patch on 0.159.2, even though the temporary
configuration file was loaded. Neither control is active in the runner.

If that route is unavailable, a dedicated OpenAI Platform project API key is
the local fallback **only after the owner chooses its separate billing
path**. For a managed hosted Codex workload, evaluate
[Codex workload identity federation](https://developers.openai.com/api/docs/guides/workload-identity-federation)
with a managed ChatGPT workspace principal; it is beta and requires workspace
enablement. A Platform service account key or Platform federation instead
authenticates an OpenAI API project, not the ChatGPT plan. Do not silently
substitute one identity or billing source for another.

For Claude, use a dedicated Claude Console service-account API key for a
shared runner, or [Claude workload identity
federation](https://platform.claude.com/docs/en/manage-claude/authentication)
when a suitable workload identity exists. A personal API key can serve
single-user development, but is not a shared-service identity. Do not use a
copied claude.ai or Claude Code personal login for Laomedo. #121 did not run a
credentialed turn, so Claude Agent SDK isolation and trace behavior remain
unverified. A separate licensing review must decide whether the intended
distribution and hosting of its bundled CLI are permitted.

For OpenCode, the [local adapter](opencode.md#authentication-and-isolation-gate)
reads the active Console account from the user's database without copying its
refresh token or full profile. It selects only the Go credential and routing
context for private runner state. The runner rejects a near-expiry Console
token before reserving a turn; the official client remains responsible for
refresh. This is local adapter behavior, not a hosted credential lifecycle or
proof that every controller-to-tool access route is closed.

Hosted or multi-user release is **no-go** until the credential mode is
eligible, per-user or per-tenant authorization and isolation are tested, tool
subprocesses cannot read broker credentials, refresh and revocation pass, and
the #124 trace and confinement gates pass. The #146 Docker result permits only
a bounded single-user local prototype.

## Credential-mode matrix

| Mode | Principal and billing | Local use | Hosted use and lifecycle |
| --- | --- | --- | --- |
| Temporary copied Codex ChatGPT login | One personal ChatGPT session and plan | Already used only for bounded spikes | Reject. A copied refresh chain can conflict with the original; no app-owned provisioning or tenant identity. |
| App-owned Sign in with ChatGPT | Consenting eligible user and ChatGPT plan or available credits | One local account connected and completed two bounded Codex turns in #107; repeatability after token rotation remains untested | Hosted use needs explicit eligibility, per-user ownership, and tool-env proof. Broker owns rotating refresh token. |
| OpenAI Platform project API key | Project or service-account identity; Platform billing | Opt-in fallback with separate billing | Secret-store rotation and scoped project access; never label it ChatGPT plan access. |
| Codex workload identity federation | Managed ChatGPT workspace user or service account; workspace Codex access | Optional when managed workspace is available | Beta and enablement-dependent. Exchange short-lived external identity for Codex access; no copied login file. |
| OpenCode Go `console_token` | Active user's OpenCode Console account and selected Go routing; billing provenance needs verification | Local adapter selects the active Console token without copying refresh state | Official client owns refresh; hosted identity and controller/tool isolation remain unverified. |
| OpenCode Go `provider_key` | Active user's OpenCode Console account and provider key selected from its Go configuration; billing provenance needs verification | Local adapter selects the key without copying the complete profile | Hosted provisioning, key rotation, and controller/tool isolation remain unverified. |
| Claude personal API key | Personal Claude Console identity and API billing | Single-user development only | Reject for shared automation. |
| Claude service-account API key | Claude Console service account/workspace and API billing | Supported candidate after #121 runtime is available | Secret-store rotation, expiry, revocation, and licensing review. |
| Claude workload identity federation | Claude Console service account/workspace and API billing | Optional when IdP exists | Preferred hosted candidate where supported; short-lived exchanged token and scoped federation rule. |
| Provider-managed Claude route | Bedrock, Vertex, or another documented provider identity and billing | Separate adapter investigation | Requires provider-specific authorization, provenance, terms, and a #121 parity test. |

OpenAI [service-account keys](https://developers.openai.com/api/reference/cli/resources/admin/subresources/organization/subresources/projects/subresources/service_accounts/subresources/api_keys/methods/create)
can have scopes and expiration. OpenAI federation maps API workloads to
Platform service accounts and Codex workloads to managed ChatGPT principals,
which are distinct namespaces. Anthropic documents personal and service
account key types, expiration, disable/delete behavior, and federation
against a service account. Its [federation
reference](https://platform.claude.com/docs/en/manage-claude/wif-reference)
says Claude Code and the Claude Agent SDK honor that credential resolution
order. Provider support does not establish that Laomedo's pinned SDK or
sandbox has passed the proposed boundary tests.

## Contract between flow, broker, and provider

The flow stores an opaque `credential_ref`, not a key, login path, environment
variable value, or auth file. The runner resolves it only after checking run
owner, tenant, provider, environment, approved credential mode, and requested
capability. A run record carries:

| Field | Meaning |
| --- | --- |
| `credential_ref` | Opaque broker reference; absent from exported flows and agent prompts. |
| `credential_mode` | Exact mode from the matrix, never inferred from a token prefix. |
| `principal_ref` | Internal, pseudonymous user or service-account reference. |
| `provider_account_ref` | Provider organization, workspace, or project reference, protected by access control. |
| `billing_context` | ChatGPT plan, OpenAI Platform project, OpenCode Console/Go account with billing provenance to verify, Claude Console workspace, or named cloud provider. |
| `credential_generation` | Monotonic broker version used for rotation and incident review, not secret bytes or a token hash. |
| `auth_state` | `ready`, `refreshing`, `reauthorization_required`, `expired`, `revoked`, or `unavailable`. |
| `provenance` | How identity was established: verified OAuth identity, selected official-client account, admin-created service account, or federated rule. |

GitHub authorization is a separate grant, not an agent-provider credential.
The selected user-facing [GitHub account connection](github-account-connection.md)
uses browser sign-in by default or an explicit token; it does not import local
host `gh` or Git Credential Manager credentials. Its concrete broker and
connection lifecycle remain proposed, not implemented.
For a run that may push or open/update a PR, the runner must resolve a
run-scoped `github_grant_ref` for that repository and actor. Its allowed
operations must be explicit: repository contents write for branch pushes,
[pull-request write](https://docs.github.com/en/rest/pulls/pulls) for
creation/update, and [Actions read](https://docs.github.com/en/rest/actions/workflow-jobs)
for job logs when requested. Checks may require a distinct read permission;
the exact grant set must be verified against the chosen GitHub API operations
before dispatch. A run that only reads issues or reviews gets
read grants, not implicit write grants. The grant must not include workflow-file
write permission merely because the runner may inspect failing Actions runs;
workflow modification requires a separately approved capability. A missing or
insufficient GitHub grant fails the affected operation without falling back to
the host's `gh` session or a mounted Git credential helper. The exact GitHub
grant broker and API handoff with [issue integration](../../issue-integration/contract/README.md)
remain a first-slice design decision, not an implemented guarantee.
This is the **first-slice grant**, not the full capability target in
[decision 0004](../../../decisions/0004-mediated-git-gh.md) and the
[mediation contract](github-write-mediation.md): parity with authorized
`git`/`gh` operations never widens a run's selected grant. General `gh api`
or GraphQL access must enforce the same repository, operation and separate
workflow-file approval rules. Agent-created follow-up issues remain subject
to the user's reviewed-publication decision in
[IF-12](../../issue-integration/contract/interfaces.md#if-12--reviewed-follow-up-issue-publication),
not an implicit issue-write grant. The
[merged Q16 contract](https://github.com/amadou-6e/specs/commit/56192486b2dad9158a0bbd435b781cb211237dd3)
addresses uncertain mediated writes, but does not establish exactly-once
remote effects or prove the proposed connection modes.

The broker keeps refresh credentials and service keys in OS-protected local
storage for one user or a managed secret store for a remote service. It persists
across runner restarts but is not mounted into a run workspace. Store the
minimum metadata needed to resume auth, and bind it to the provider account
and Laomedo owner. Restrict reads and writes to the broker identity. Keep
separate keys for development and production, and separate tenants or users.
Backups must preserve protection and support revocation; deleting a workspace
must not delete the account connection.

At dispatch, the broker creates a clean provider-controller environment,
allowlisting only required paths, settings, and the selected credential
channel. It clears inherited `HOME`, profile/config paths, `OPENAI_API_KEY`,
`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `OPENCODE_CONSOLE_TOKEN`,
cloud credential variables,
proxy secrets, and other competing auth sources before adding the selected
mode. Claude's documented precedence means even an **empty** API-key variable
can shadow federation, so unused variables must be unset. A tool-command
environment is built independently and receives no credential channel.
Bundled scripts use that same tool environment. Agent-controlled processes
must not be able to read the broker store, app-server process environment,
token file, IPC endpoint with reusable credentials, or host secret manager.

The official Codex app-server recipe places the OAuth access token in the
app-server child's `ACCESS_TOKEN` environment and requires an app-server
restart with a replacement token before `thread/resume`. This describes a
provider-controller token swap between completed turns in a still-live run,
not recovery of a crashed backend or interrupted turn. It is a
**controller exposure** which Laomedo must audit: if Codex tool execution
inherits the value or can inspect the controller process, the current
architecture fails the secret boundary. Use a separate OS/container identity
for tool execution or a brokered inference channel only after testing its
actual access paths. A prompt instruction or sanitizer alone cannot fix a
readable secret.

For Claude federation, prefer a projected identity-token file accessible to
the controller alone. Anthropic documents credential precedence and says
`ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` overrides federation; the
broker must reject ambiguous configurations. Claude's
`CLAUDE_CONFIG_DIR` isolation from #121 remains required independently of
authentication. A provider SDK's default profile must not be a fallback when
the selected credential is missing.

## Provisioning, renewal, and retirement

1. **Provision.** A user explicitly connects a local ChatGPT account through
   app-owned OAuth, or an administrator registers a service identity, key, or
   federation rule. Record the verified identity and granted scopes or rule
   identifier. Never import the IDE's `auth.json` as a production shortcut.
2. **Dispatch.** Lock one credential generation to a run. Verify its owner,
   provider, workspace, allowed purpose, and readiness. Preserve the requested
   credential mode in trace metadata even when dispatch fails.
3. **Renew.** A single broker writer performs refresh under a per-profile lock
   and atomically replaces persisted state. Other runs wait for the result
   rather than using parallel copies of a rotating refresh token. OpenAI's
   [token reference](https://developers.openai.com/siwc/token-sharing-open-source/token-reference)
   documents one-hour access tokens and replacement refresh tokens with
   30-day validity for this flow. Never replay an old refresh token after an
   ambiguous exchange outcome without the provider's recovery procedure.
4. **Replace a controller token between completed turns.** If the Langflow
   backend and run remain live, a broker may replace the Codex app-server
   process with a new access token and use the documented `thread/resume`
   transport operation for the saved native thread. Before another turn, verify
   the exact post-turn workspace snapshot under [runner isolation](isolation.md).
   This is **not** recovery from a Langflow/backend restart or a mid-turn
   container crash. Either event ends the affected run or invocation with
   partial/unknown evidence under [D16/D17](../../../decisions/0002-subsystem-handoffs.md#execution-recovery-and-inspection);
   no same-run or same-turn continuation is implied. Broker state may reload
   after backend restart, but the terminated run does not resume.
5. **Rotate.** For static keys, provision a new generation, verify it in a
   credential-only check, switch new dispatches, drain or stop old processes,
   then disable/delete the old key. For federation, rotate the issuer or rule
   under provider guidance and verify claim matching. Keep only non-secret
   generation IDs in run history.
6. **Revoke and recover.** Stop new dispatches immediately, cancel or
   quarantine active controllers with that credential, and mark affected
   sessions `reauthorization_required` or `revoked`. Preserve workspace and
   trace evidence without exposing credentials. Reconnect or rotate, then
   require an explicit decision before another turn; never switch accounts
   silently. A still-live run may continue **between completed turns** only
   under step 4's checks. After a backend crash or terminal state, any later
   execution is a user-requested **new run**, not native session recovery.

Run-scoped GitHub grants expire or are revoked when their invocation ends.
Backend death must not leave a push-capable orphan usable throughout an
unbounded outage: issuer-enforced expiry or an independent lease/supervisor
must bound grant use **while the backend is down**. A restart sweep is only a
second line of cleanup. [Q01/Q25](../design/decision-readiness.md) select an
independent lease supervisor for outage-time revocation and stop, plus a
backend startup sweep for durable reconciliation, with a 60-second maximum
exposure bound. The synthetic [E01 result](../design/decision-readiness.md)
does not prove real push-credential revocation or production integration;
writable dispatch with that grant remains blocked until those checks pass.
The broker reconciles active grants against durable run identities after
restart, revokes unmatched grants before dispatch, and records only
non-secret grant IDs and revocation outcomes. A provider account connection
may persist for future consented runs, but its per-run derived grant must not.

The temporary #119-#122 ChatGPT handoff remains outside Git until its owner
retires it. Migration means establish a new app-owned or dedicated identity,
validate it separately, switch the runner to the new `credential_ref`,
confirm no test depends on the copied profile, and securely remove only the
identified temporary copies. Do not copy that profile into another location
or run it concurrently during migration. Keep a non-secret audit of which
profile was retired and when. This document does not authorize deleting the
existing private profile.

## Errors, traces, and validation

Authentication failures are their own terminal or recoverable category:
`auth_missing`, `auth_consent_missing`, `auth_expired`,
`auth_refresh_failed`, `auth_revoked`, `auth_scope_denied`,
`auth_account_mismatch`, and `auth_mode_unavailable`. Keep provider HTTP
status, stable code when supplied, and request ID in restricted diagnostics,
with secret-bearing body fields redacted. Do not mislabel a 401 as a model
failure, a 403 scope denial as a filesystem denial, a usage limit as expiry,
or a missing session snapshot as authentication failure. OpenAI's
[error guidance](https://developers.openai.com/siwc/token-sharing-open-source/errors-and-recovery)
also distinguishes consent, eligibility, admission, and usage availability.
Trace projection may expose the sanitized category and credential mode, while
raw provider events remain under [trace access controls](../../run-traces/contract/README.md).

The design is accepted only after tests on the pinned runner version:

| Scenario | Required observation |
| --- | --- |
| Disposable workspace deletion | Broker credential and private native session data survive independently; deleted workspace files and tool process retain no credential. Survival of session data does not authorize automatic run recovery. |
| Between-turn Codex app-server token replacement | With the Langflow backend and run still live, replacement controller uses the new token; any next turn uses the saved thread ID only after hash-verified post-turn files. No mid-turn recovery is claimed. |
| Backend restart | Broker state reloads, but the previous run is terminal `crashed`; no agent turn is resumed or redispatched. Partial/unknown effects remain visible. |
| Refresh race and ambiguous response | At most one refresh writer; no two active copies of one rotating refresh chain; ambiguous failure requires safe recovery. |
| Expiry, revoked consent/key, wrong scope/account | Typed auth error with no model turn and no silent fallback to another credential or billing mode. |
| Static-key rotation or federation rule change | New dispatch uses the new generation; old generation is rejected after retirement. |
| Personal-profile leak | Before/after path and hash checks show no personal profile writes; only selected project skills are available. |
| Tool and script secret access | Agent-originated shell and bundled script attempts to read env, mounted files, process data, and broker IPC are denied with observed tool events. |
| Trace and export leak | Synthetic canary credentials do not appear in raw or projected trace, crash logs, Langflow output, AGENTVIZ import, or flow export. |
| Multi-user cross-access | User B cannot select, read, refresh, resume, or inspect user A's credential or session; revocation affects only its owner. |
| GitHub grant scope and orphan cleanup | A run can push, create/update a PR, and read only its approved checks/logs; it cannot edit workflow files without a separate grant. An interrupted or lost run's grant expires or is revoked within the selected bound even while the backend is down, with no fallback to host credentials. |

Tests use synthetic canary secrets first, then a dedicated credential only
under a separately approved bounded run. No model call or provider account
change is needed to validate this document.

## Open product and legal decisions

- Confirm whether this local Laomedo installation obtains app-owned ChatGPT
  plan usage, which users and workspaces are eligible, and whether its preview
  limits fit Codex's required tools. A
  [self-hosted VM transfer](https://developers.openai.com/siwc/token-sharing-open-source/self-hosted-vms)
  is documented, but host-specific attribution and revocation of transferred
  sessions are not yet available; this does not solve hosted tenancy.
- Choose local OS secret storage and the future hosted secret manager, account
  owner model, billing display, retention and deletion periods, and whether a
  remote runner is part of the first product. None is selected here.
- Confirm whether Claude's service-account or federation path works with the
  pinned Agent SDK and whether the bundled Claude Code CLI's Commercial Terms
  permit the planned packaging and hosted model. Obtain specialist review
  before redistribution or multi-user deployment.
- Audit the controller-to-tool credential boundary for Codex and Claude. A
  token in a controller environment is not automatically hidden from agent
  subprocesses. Failure to prove the boundary keeps untrusted tool execution
  and hosted release blocked.
