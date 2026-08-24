# Dependency — OpenAI CLI (`openai` / Codex)

The `openai` binary is OpenAI's command-line tool. Blog-hub uses it under the provider name `codex` in two roles:

| Role | Used by | When |
|------|---------|------|
| **Browser login** | Connections service | User saves an OpenAI connection via the CLI login flow |
| **Content generation** | Agent service | `POST /api/agent/generate`, `/regenerate`, `/generate-patch` with `provider: "codex"` |

> **Naming note**: The API field is `provider: "codex"` but the binary name is `openai`.  
> The `codex` label reflects the Codex model lineage in the generation context.

---

## 1. Binary Discovery

Resolved in order:

| Priority | Source |
|----------|--------|
| 1 | `OPENAI_CLI_PATH` env var (absolute path) |
| 2 | `shutil.which("openai")` — standard PATH lookup |
| 3 | Well-known fallback locations: `~/.local/bin`, `~/.npm-global/bin`, `/usr/local/bin` |

If not found: `GET /api/connections/openai/oauth-start` returns `{ available: false }`.

---

## 2. Login Flow

### Start login

```
openai login --print-url
```

| Channel | Content |
|---------|---------|
| stdout (first line) | `https://platform.openai.com/...` — URL to open in browser |
| Process state | Remains running; listens for OAuth callback |

> **@tbd**: Confirm the exact flag (`--print-url` vs `--print-login-url`) against installed OpenAI CLI version.

**Process tracking** stored in `_cli_login_pending[conn_id]`:

```python
{
  "pid":          <int>,
  "conn_id":      "openai",
  "state_token":  "<random nonce>",
  "started_at":   datetime(...),
}
```

### Poll for completion

```
openai whoami
```

| Exit code | stdout | Meaning |
|-----------|--------|---------|
| `0` | User info line | Authenticated — store `username`, mark `connected` |
| non-zero | error message | Still pending OR failed |

**Poll interval**: every 2 s, max 5 min client-side.  
**Backend action on exit 0**: `store.save_connection("openai", token="__cli_session__", username=...)`

### Credential file location

| Variable | Default |
|----------|---------|
| `OPENAI_CONFIG_DIR` | `~/.config/openai` |

Backend **never reads** this directory.

---

## 3. Content Generation

### Argv template

> **@tbd** — exact flags not yet confirmed from OpenAI CLI docs.

Known intent from `agent/service.md`:

```
openai api chat.completions.create -m gpt-4o -p "<prompt>"
```

or via Codex CLI (separate binary):

```
codex [--full-auto] -p "<prompt>"
```

> **Clarification needed**: The spec uses `provider: "codex"` but the connection ID is `"openai"`.  
> It's unclear whether generation uses the `openai` binary (chat completions) or a separate  
> `codex` binary. Confirm before implementing `cli_runner.py`.

**Inputs to the CLI:**

| Input | Source |
|-------|--------|
| Brief | `GenerateRequest.brief` |
| Skill system prompt | Loaded from skill library by name |
| Context text | `GenerateRequest.contextText` |
| Web search flag | **@tbd**: Codex CLI web search capability not confirmed |

**Assembled prompt structure** (same as Claude; see [cli-claude/service.md](../cli-claude/service.md)):

```
[system prompt from skill library]

USER BRIEF:
<brief>

CONTEXT:
<contextText if provided>

Write an article of approximately <wordCount> words.
```

### Outputs expected from stdout

| Operation | stdout content |
|-----------|---------------|
| `generate` | Full article body (Markdown) |
| `regenerate` | Revised article body (Markdown) |
| `generate-patch` | Diff / replaced text blocks — **@tbd** |

### Exit codes

| Code | Meaning | State |
|------|---------|-------|
| `0` | Success | Write stdout → article body; job `status=done` |
| non-zero | CLI error | stderr excerpt → job `status=error` |

---

## 4. Process Independence

Identical isolation model to the Claude CLI — see [cli-claude/service.md](../cli-claude/service.md#4-process-independence) for the full rationale. Differences for OpenAI:

### Explicit-allowlist environment

```python
env: dict[str, str] = {
    "HOME":              os.environ["HOME"],
    "PATH":              os.environ["PATH"],
    "OPENAI_CONFIG_DIR": os.environ.get("OPENAI_CONFIG_DIR", ""),
    "TEMP":              os.environ.get("TEMP", ""),
    "TMP":               os.environ.get("TMP",  ""),
    # Conditional — only when CLI session unavailable (priority 2/3):
    # "OPENAI_API_KEY": token   ← injected as data, never logged, never in argv
}
```

Variables that are **never forwarded**: `MEDIUM_CLIENT_SECRET`, `SECRET_KEY`, `ANTHROPIC_API_KEY`, `CLAUDE_CONFIG_DIR`, or any other BlogHub or Anthropic secret.

### Isolated working directory

```python
work_dir = tempfile.mkdtemp(prefix="bloghub_openai_")
try:
    proc = subprocess.run(
        [openai_path, "--flag", safe_value],  # list form — shell=False
        env=env,
        cwd=work_dir,
        shell=False,
        capture_output=True,
        timeout=int(os.environ.get("AGENT_TIMEOUT_SECONDS", 60)),
    )
finally:
    shutil.rmtree(work_dir, ignore_errors=True)
```

### API key transmission
- Key placed in `env["OPENAI_API_KEY"]` only — **never** as a CLI argument.
- Not visible in `ps aux`; not logged; env dict discarded after the call.

---

## 5. Process Limits

Same as Claude CLI — governed by the same env vars:

| Limit | Env var | Default |
|-------|---------|---------|
| Max wall-clock time | `AGENT_TIMEOUT_SECONDS` | `60` s |
| Max output read | `AGENT_MAX_OUTPUT_BYTES` | `524288` (512 KB) |
| Graceful shutdown | *(hardcoded)* | SIGTERM → 5 s → SIGKILL |

---

## 6. Credential Resolution Order

| Priority | Check | Auth method for subprocess |
|----------|-------|---------------------------|
| 1 | `openai whoami` exits 0 | CLI uses its own session |
| 2 | `_connections["openai"].token` non-empty | `OPENAI_API_KEY=<token>` injected in env |
| 3 | `OPENAI_API_KEY` env var set | Forwarded as-is |
| — | None | `400` — credential not configured |

---

## 7. Differences from Claude CLI

| Aspect | Claude CLI | OpenAI CLI |
|--------|-----------|------------|
| Login flag | `--print-login-url` | `--print-url` (**@tbd**) |
| Config dir env | `CLAUDE_CONFIG_DIR` | `OPENAI_CONFIG_DIR` |
| Web search support | Yes (flag known) | **@tbd** |
| Generation binary | `claude` | `openai` or `codex` (**@tbd**) |
| whoami output | `Logged in as <email>` | **@tbd** — format not confirmed |

---

## 8. Environment Variable Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| `OPENAI_CLI_PATH` | PATH lookup | Absolute path to `openai` binary |
| `OPENAI_CONFIG_DIR` | `~/.config/openai` | Override credential directory |
| `OPENAI_API_KEY` | *(not set)* | Fallback API key when CLI session unavailable |
| `AGENT_TIMEOUT_SECONDS` | `60` | Max seconds per subprocess |
| `AGENT_MAX_OUTPUT_BYTES` | `524288` | Output cap per subprocess |
