# Upstream dependencies and extension boundaries

Status: findings for issue #118, 2026-09-28. This is a feasibility input, not
an implementation decision or an approved roadmap. It tests the proposal from
PR #113 ([component index](../components/agent-and-skill-components.md))
against the upstream tools it would depend on. The synthesis and
build-versus-adapt decision belong to #124.

## Evidence labels

- **Verified locally**: observed on this workstation in the installed version
  listed below. Commands were read-only; no configuration, profile, or flow
  was changed.
- **Documented**: stated in the upstream primary source linked in the row.
- **Inferred**: a conclusion drawn from the other two; needs an experiment.

## Versions inspected

| Component | Version or commit | License | Source |
| --- | --- | --- | --- |
| AGENTVIZ | `9f32319` (v1.2.0) | MIT | [jayparikh/agentviz](https://github.com/jayparikh/agentviz) |
| Langflow | 1.12.3, image `langflowai/langflow@sha256:34055a07d446…` (pulled as `latest`) | MIT | [langflow-ai/langflow](https://github.com/langflow-ai/langflow), [v1.12.3](https://github.com/langflow-ai/langflow/releases/tag/v1.12.3) |
| lfx (Langflow component runtime) | 1.12.3 | No license field in package metadata; repository is MIT (inferred) | Same repository, `src/lfx` |
| LangChain / langchain-core / LangGraph | 1.3.14 / 1.5.1 / 1.2.9, inside the Langflow image | MIT | Package metadata in the container |
| Codex Python SDK (`openai-codex`) | 0.157.1 | Apache-2.0 | [openai/codex](https://github.com/openai/codex), [SDK docs](https://github.com/openai/codex/tree/main/sdk/python/docs) |
| Codex CLI binary (`openai-codex-cli-bin`) | 0.157.1 | Apache-2.0 | Package metadata |
| Claude Agent SDK (`claude-agent-sdk`) | 0.2.160 on PyPI; not installed locally | MIT for the SDK; bundled Claude Code CLI is under Anthropic Commercial Terms | [PyPI](https://pypi.org/project/claude-agent-sdk/), [claude-code LICENSE](https://github.com/anthropics/claude-code/blob/main/LICENSE.md) |
| Deep Agents (`deepagents`) | 0.7.19 released upstream; not installed in Langflow | MIT | [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents), [skills docs](https://docs.langchain.com/oss/python/deepagents/skills) |

## Dependency and gap matrix

Classification: **adapt** (use as is), **extend** (use an upstream extension
point), **build** (new Laomedo code), **defer**, or **unknown** (needs the named
experiment).

| Laomedo need | Upstream capability | Evidence | Class | Gap or risk |
| --- | --- | --- | --- | --- |
| Flow canvas node for an agent step | Langflow custom components (`lfx` `Component`, typed inputs/outputs, async `_run`, `self.ctx` state), loaded from `LANGFLOW_COMPONENTS_PATH` in category folders | Documented ([custom components](https://docs.langflow.org/components-custom-components)); current flow uses the built-in APIRequest node (verified) | Extend | Loading a component requires mounting a directory and setting the variable. The local container sets neither, so adopting it changes the container configuration. |
| Skill selector node | None in Langflow. Upstream request [#11547](https://github.com/langflow-ai/langflow/issues/11547) is open with no comments; [#12656](https://github.com/langflow-ai/langflow/issues/12656) was closed as a duplicate. Langflow's own `.agents/skills/` holds contributor skills, not a product feature. | Documented (GitHub) | Build | A thin custom component that calls the Laomedo skill registry; the registry itself is new code. |
| Exact skill revision, hashes, rule/example items | No upstream tool versions skill bundles or exposes rule/example IDs | Verified absence in the Codex SDK types, Claude SDK docs and Deep Agents docs | Build | Owned by the Skill Revision spec; the manifest format is still open (#119). |
| Native skill delivery to Codex | Repo skills in `.agents/skills` (from cwd up to the repo root), user skills in `$HOME/.agents/skills`, admin in `/etc/codex/skills`, plus built-in system skills. The app-server protocol adds `skills/list`, `skills/extraRoots/set`, `skills/config/write` (enable/disable), and a `SkillInput(name, path)` turn input for explicit selection. | Documented ([build skills](https://learn.chatgpt.com/docs/build-skills)); protocol types verified in SDK 0.157.1 | Adapt | The high-level SDK exposes `SkillInput` but not `skills/list`, which needs a raw JSON-RPC request. User skills follow `$HOME`, not `CODEX_HOME`. |
| Native skill delivery to Claude | `.claude/skills` discovered through `setting_sources`; `skills=[names]` allowlist; `system/init` lists loaded skills; invocation appears as a `Skill` tool use | Documented ([SDK skills](https://code.claude.com/docs/en/agent-sdk/skills)) | Adapt, then verify in #121 | Unlisted skills stay readable through Read and Bash; the allowlist limits invocation, not file access. |
| Model and effort selection | Codex: per-turn `model` and `effort` (`none`–`ultra`); `models()` returns each model's `supportedReasoningEfforts` and default. Claude: a model option per query. | Codex verified in SDK types; Claude model option documented, effort control not checked | Adapt (Codex), unknown (Claude effort) | Pre-dispatch validation can use Codex `models()`. Claude effort selection and validation are unverified (#121). |
| Private persistent sessions (Codex) | `CodexConfig(env=…, config_overrides=…, codex_bin=…)` launches `codex app-server` over stdio. `thread_start`, `thread_resume`, `thread_fork`, `thread_list`, `ephemeral`. | Verified in SDK source | Extend | `env` is **merged** into `os.environ`, so the parent environment is inherited. The runner must build a clean environment (`HOME`, `CODEX_HOME`, `PATH`, credentials). |
| Private persistent sessions (Claude) | `CLAUDE_CONFIG_DIR`, `setting_sources`, `resume` by session ID | Documented ([Claude Code features](https://code.claude.com/docs/en/agent-sdk/claude-code-features), [sessions](https://code.claude.com/docs/en/agent-sdk/sessions)) | Extend | Managed policy and `~/.claude.json` are read regardless of `setting_sources`. Auto memory needs `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. Server-managed settings can't be disabled from the SDK when an organization credential is used. |
| Read-only and permission enforcement | Codex: `Sandbox.read_only`, approval policy, approval handler callback. Claude: permission modes, `can_use_tool`, hooks, command sandbox. | Codex verified in SDK; Claude documented | Adapt, and build the grant record | Provider sandboxes enforce inside the agent process. Laomedo's grant record, path validation and workspace snapshots are still new code. Symlink and traversal behavior is untested (#122). |
| Inner agent trace (Codex) | App-server notifications for items (agent message, reasoning, command execution, file change, MCP tool call, web search, sub-agent) and deltas; the rollout JSONL is also written under the profile's `sessions/` | Verified in SDK types and in a local rollout file | Adapt | No item type records a skill read. Codex skill use can only be inferred from command or file events. |
| Inner agent trace (Claude) | Streamed SDK messages: `system/init` (skills, commands), assistant tool uses, tool results, result with usage | Documented | Adapt, then verify in #121 | Skill invocation is observable as a `Skill` tool use; direct Read or Bash access to skill files is only inferable. |
| Outer flow trace | Langflow native tracing: flow traces and component spans in the `trace`/`span` tables, read through `/api/v1/monitor/traces`; OpenTelemetry, Arize and others as exporters | Documented ([traces](https://docs.langflow.org/traces)); API read verified locally | Adapt | For the fixture run, the trace reports `totalTokens: 0` although Codex used tokens. Langflow cannot see inner usage and shows unknown as zero, which the [run-traces spec](../monitoring/run-traces.md) forbids. The Laomedo run ID and thread ID appear only inside the output text. |
| Trace inspection UI | AGENTVIZ parses Codex rollout JSONL, Claude Code JSONL, Copilot formats and ATIF v1.6; includes live Codex/Claude normalizers and a skill extractor with lifecycle stages | Verified in `src/lib/parseSession.ts`, `codexParser.ts`, `skillExtractor.ts` | Adapt for inspection, extend for correlation | AGENTVIZ reads rollout files, not app-server event streams. A private runner's `CODEX_HOME/sessions` rollouts should import unchanged (inferred; #123). The skill extractor infers use from paths, so its output is `inferred` provenance. |
| Skill editing in a draft worktree | None upstream beyond agent write sandboxes | Verified absence | Build | Owned by the Skill Draft spec (#122). |
| Session and trace storage, multi-user | Langflow: SQLite in a Docker volume, `AUTO_LOGIN=true` locally | Verified locally | Build or defer | The local Langflow instance is single-user. It is not a store for runner sessions or credentials. |
| Alternative skill runtime | Deep Agents `SkillsMiddleware`: progressive disclosure, `scripts/`, `references/`, `assets/`, filesystem or store backends | Documented | Defer | Runs LangChain models, not the Codex or Claude Code runtimes. No per-run skill selection beyond which paths are configured. Useful as a reference design, not a substitute. |

## What the local fixture proves

The `.tools.local/laomedo-eval` fixture on the author's workstation (not
published) proves that the Langflow APIRequest node can call a host-side HTTP
bridge. The bridge runs one fixed read-only Codex task and returns a JSON
record. It does not prove isolation. Read-only inspection of one fixture run,
thread `01a0e6a6-…`, showed:

- **Personal history.** The thread was written to the personal
  `~/.codex/sessions/2026/09/28/` directory.
- **Personal skills leaked.** The run's context advertised a personal skill
  (`~/.codex/skills/deck-design-rulebook`) and plugin skills
  (`google-drive:google-docs`).
- **Inherited environment.** The session records `originator:
  "codex_vscode"`, which suggests the bridge inherited the VS Code terminal's
  environment.
- **Pasted skill, not native delivery.** The skill was pasted into the
  prompt; the bridge hashes only `SKILL.md`, and the response's
  `skill_applied` field is the model's own claim, not evidence.
- **Model and effort not controlled.** The model came from the personal
  default configuration.
- **Unsafe listener.** The bridge listens on `0.0.0.0:8765`, which is
  reachable from the local network, and is protected only by a token file.

These are the exact failure modes the
[runner isolation spec](../sandboxing/runner-isolation.md) guards against, so
the fixture is a useful negative control. It must not be treated as a
component.

## Proposed spec corrections

These follow from the evidence. They are proposals for review, not changes
made here.

1. **Codex isolation must set `HOME` as well as `CODEX_HOME`.** The documented
   user skill root is `$HOME/.agents/skills`. The personal
   `~/.codex/skills` leak shows the profile root also matters. The runner
   must launch Codex with a constructed environment, not the SDK's merged
   `os.environ`.
2. **Claude isolation needs more than `CLAUDE_CONFIG_DIR`.** It also needs
   `setting_sources` set to `[]` or `["project"]`,
   `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, and an explicit `skills` allowlist.
   It must record whether managed or server-managed settings applied.
3. **"Offered" must include everything reachable on disk.** A Claude skill
   allowlist does not hide skill files, and Codex scans several roots. The
   materialized directories therefore define what was offered, not the
   allowlist.
4. **Codex "used skill" is inferred at best; Claude invocation is observed.**
   The run-traces spec should record this per provider.
5. **Langflow token and cost fields must not be shown as agent usage.** The
   Laomedo component should put its run ID and native session ID into
   structured output or span metadata, not only into message text.

## Risks and questions for specialist review

- **Claude licensing.** Bundling the Claude Code CLI under Anthropic
  Commercial Terms may limit redistribution or hosted multi-user use. This
  needs a licensing review before a remote runner.
- **Credentials.** Neither SDK documents a supported path for per-tenant
  credentials in a shared runner. Codex reuses existing authentication by
  default; Claude server-managed settings follow organization credentials.
- **Version drift.** The Codex SDK marks `experimental_api=True`, and its
  protocol includes deprecated fields. Langflow is pulled as `latest`. Pin the
  image digest and SDK versions for every experiment.
- **Unreviewed parts of lfx.** lfx package metadata has no license field, and
  its component API docs changed recently (upstream PR
  [#15138](https://github.com/langflow-ai/langflow/pull/15138)).

## Recommended next experiments

| Question | Issue | Smallest test |
| --- | --- | --- |
| Which roots does Codex actually scan with `HOME` and `CODEX_HOME` both set to runner directories? | #119, #120 | Launch the SDK with a constructed environment. Call `skills/list` and diff the result against a planted personal skill. |
| Does `SkillInput` load a skill outside discovery roots, and does it produce any trace item? | #119 | A single turn with an explicit `SkillInput` pointing at a materialized bundle. |
| Does Claude load nothing personal with `setting_sources=[]`, a private `CLAUDE_CONFIG_DIR`, and auto memory off? | #121 | Plant a personal skill, `CLAUDE.md` and memory; check `system/init` and the transcript. |
| Can AGENTVIZ import a private-runner rollout without losing IDs? | #123 | Import one isolated rollout and compare the event count and IDs. |
| Can a Langflow custom component return structured run and session IDs and attach them to its span? | #118 follow-up, #123 | A disposable Langflow container with a mounted components path. |
