# Dependency — Claude CLI (`claude`)

The `claude` binary is Anthropic's command-line tool. Blog-hub uses it in two distinct roles:

| Role | Used by | When |
|------|---------|------|
| **Browser login** | Connections service | User saves an Anthropic connection via the CLI login flow |
| **Content generation** | Agent service | `POST /api/agent/generate`, `/regenerate`, `/generate-patch` |

---

## 1. Binary Discovery

Resolved in order:

| Priority | Source |
|----------|--------|
| 1 | `ANTHROPIC_CLI_PATH` env var (absolute path) |
| 2 | `shutil.which("claude")` — standard PATH lookup |
| 3 | Well-known fallback locations: `~/.local/bin`, `~/.npm-global/bin`, `/usr/local/bin` |

If not found: `GET /api/connections/anthropic/oauth-start` returns `{ available: false }`.  
Generation falls back based on credential resolution order; if no credential → `400`.

---

## 2. Login Flow

### Start login

```
claude login --print-login-url
```

| Channel | Content |
|---------|---------|
| stdout (first line) | `https://console.anthropic.com/oauth/authorize?...` — the URL to open in browser |
| Process state | Remains running; listens for the OAuth callback from the opened browser |

**Process tracking** stored in `_cli_login_pending[conn_id]`:

```python
{
  "pid":          <int>,
  "conn_id":      "anthropic",
  "state_token":  "<random nonce>",
  "started_at":   datetime(...),
}
```

### Poll for completion

```
claude whoami
```

| Exit code | stdout | Meaning |
|-----------|--------|---------|
| `0` | `Logged in as acisse@example.com` | Authenticated — store `username`, mark `connected` |
| non-zero | error message | Still pending OR failed |

**Poll interval**: every 2 s, max 5 min client-side.  
**Backend action on exit 0**: `store.save_connection("anthropic", token="__cli_session__", username=...)` — the literal token is a sentinel; actual key lives in CLI config dir.

### Credential file location

| Variable | Default |
|----------|---------|
| `CLAUDE_CONFIG_DIR` | `~/.claude` |

Backend **never reads** this directory — only `claude whoami` is used to probe auth state.

---

## 3. Content Generation

### Argv template

> **@tbd** — exact flags not yet confirmed from Claude CLI docs.

Known intent from `agent/service.md`:

```
claude [--web-search] -p "<assembled prompt>"
```

or prompt delivered via stdin on a non-interactive invocation:

```
echo "<prompt>" | claude [--no-input-file] [--model claude-3-5-sonnet]
```

**Inputs to the CLI:**

| Input | Source |
|-------|--------|
| Brief | `GenerateRequest.brief` |
| Skill system prompt | Loaded from skill library by name (`GenerateRequest.skill`) |
| Context text | `GenerateRequest.contextText` (uploaded `.md` file contents) |
| Web search flag | Enabled when `_connections["anthropic"].web_search == true` and credential allows it |

**Assembled prompt structure** (from `agent/service.md`):

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
| `generate` | Full article body (Markdown) — captured entirely after exit 0 |
| `regenerate` | Revised article body (Markdown) — replaces current `Article.body` |
| `generate-patch` | Diff in unified format OR `removed` / `added` text blocks — **@tbd**: exact format |

### Exit codes

| Code | Meaning | Article/job state |
|------|---------|------------------|
| `0` | Success | Write stdout → article body; job `status=done` |
| non-zero | CLI error | stderr excerpt → job `status=error`, `error=<stderr[:500]>` |

---

## 4. Process Independence

The `claude` subprocess runs in a **fully isolated process** — it shares no memory, file handles, or environment variables with the FastAPI server process. Independence is enforced at every level:

### Separate process memory
- The subprocess cannot access `_connections`, `_articles`, `_jobs`, or any module-level dict.
- Results are captured exclusively via **stdout**. The agent service reads stdout after exit and writes results back to the store itself.
- stderr is captured separately for error reporting only — never written to the store as-is.

### Explicit-allowlist environment (never `os.environ` wholesale)

```python
import os, subprocess, tempfile, shutil

# ONLY these variables are forwarded — nothing else
env: dict[str, str] = {
    "HOME":               os.environ["HOME"],
    "PATH":               os.environ["PATH"],
    "CLAUDE_CONFIG_DIR":  os.environ.get("CLAUDE_CONFIG_DIR", ""),
    "TEMP":               os.environ.get("TEMP", ""),
    "TMP":                os.environ.get("TMP",  ""),
    # Conditional — only when CLI session unavailable (priority 2/3):
    # "ANTHROPIC_API_KEY": token   ← injected as data, never logged, never in argv
}
```

Variables that are **never forwarded**: `MEDIUM_CLIENT_SECRET`, `SECRET_KEY`, `DATABASE_URL`, `HASHNODE_TOKEN`, `DEVTO_API_KEY`, or any other BlogHub-internal secret.

### Isolated working directory

```python
work_dir = tempfile.mkdtemp(prefix="bloghub_claude_")
try:
    proc = subprocess.run(
        [claude_path, "--flag", safe_value],  # list form — no shell interpretation
        env=env,
        cwd=work_dir,          # fresh dir, not the server's working dir
        shell=False,           # NEVER shell=True
        capture_output=True,
        timeout=int(os.environ.get("AGENT_TIMEOUT_SECONDS", 60)),
    )
finally:
    shutil.rmtree(work_dir, ignore_errors=True)  # always cleaned up, even on timeout
```

### No shared file handles
- `capture_output=True` gives the subprocess its own stdin/stdout/stderr pipes.
- The server's log file handlers, socket connections, and open files are not inherited.
- On POSIX: `close_fds=True` is the default for `subprocess.run` — explicitly set it.

### API key transmission
- When credential priority 2 or 3 applies, the key is placed in `env["ANTHROPIC_API_KEY"]` — **never** as a CLI argument.
- Positional: `["claude", "--flag"]` — the key is not visible in `ps aux` output.
- The env dict is constructed in memory and discarded after the call; it is not logged.

---

## 5. Process Limits

| Limit | Env var | Default |
|-------|---------|---------|
| Max wall-clock time | `AGENT_TIMEOUT_SECONDS` | `60` s |
| Max output read | `AGENT_MAX_OUTPUT_BYTES` | `524288` (512 KB) |
| Graceful shutdown | *(hardcoded)* | SIGTERM → 5 s → SIGKILL |

Output exceeding the cap: append `[output truncated]` marker; process continues but further bytes are discarded.

---

## 6. Credential Resolution Order

Evaluated before any generation subprocess is spawned:

| Priority | Check | Auth method for subprocess |
|----------|-------|---------------------------|
| 1 | `claude whoami` exits 0 | CLI uses its own session — no key injected |
| 2 | `_connections["anthropic"].token` non-empty | `ANTHROPIC_API_KEY=<token>` injected in env |
| 3 | `ANTHROPIC_API_KEY` env var set | Forwarded as-is into subprocess env |
| — | None of the above | `400` — credential not configured |

---

## 7. Environment Variable Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| `ANTHROPIC_CLI_PATH` | PATH lookup | Absolute path to `claude` binary |
| `CLAUDE_CONFIG_DIR` | `~/.claude` | Override credential directory |
| `ANTHROPIC_API_KEY` | *(not set)* | Fallback API key when CLI session unavailable |
| `AGENT_TIMEOUT_SECONDS` | `60` | Max seconds per subprocess |
| `AGENT_MAX_OUTPUT_BYTES` | `524288` | Output cap per subprocess |
