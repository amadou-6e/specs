# Backend Spec — CLI Runner Service

> The CLI runner is a separate Docker-based HTTP service that wraps the `claude` and `openai`
> CLIs. The BlogHub backend never spawns CLI subprocesses directly. It communicates with the
> runner over HTTP. This replaces the subprocess model described in `agent-environment.md`.

---

## 1. Why a separate service

| Concern | Subprocess model (old) | CLI runner (new) |
|---------|----------------------|-----------------|
| CLI isolation | Per-invocation `tempfile.mkdtemp()` | Docker container boundary |
| Credential storage | Host filesystem, path-resolved | Named Docker volume, container-owned |
| What the AI sees | Controlled by env allow-list | Only what the runner mounts in the task dir |
| Login callback | Host must expose random port | Container port mapped once in docker-compose |
| Restart persistence | In-memory (lost on restart) | Volume-backed CLI credential dirs |

The container is the trust boundary. The BlogHub backend is a client; it never touches
CLI binaries, credential files, or article temp directories directly.

---

## 2. Container layout

```
cli-runner/
  Dockerfile
  main.py          ← FastAPI app exposing the runner REST API
  requirements.txt
```

**Docker image contents:**
- Python 3.12 + FastAPI + uvicorn
- `claude` CLI (Anthropic) — installed via `npm install -g @anthropic-ai/claude-code`
  or official binary release
- `openai` CLI — installed via `pip install openai` (CLI entry point: `openai`)

**Named volumes (docker-compose):**
| Volume | Mount path in container | Purpose |
|--------|------------------------|---------|
| `claude-config` | `/root/.claude` | Claude credential store |
| `openai-config` | `/root/.config/openai` | OpenAI credential store |

**Exposed ports:**
| Port | Purpose |
|------|---------|
| `8001` | Runner REST API |
| `54322` | OAuth loopback callback for `claude login` |
| `54323` | OAuth loopback callback for `openai login` |

The loopback ports must also be mapped on the host (`54322:54322`, `54323:54323`) so the
browser's redirect from the provider reaches the CLI's temporary callback server inside the
container.

---

## 3. REST API

Base URL: `http://localhost:8001` (configured in BlogHub backend via `CLI_RUNNER_URL` env var).

### Health

```
GET /health
Response 200: { "status": "ok", "providers": { "anthropic": "available", "openai": "available" } }
```

`available` means the binary is present; it says nothing about authentication.

---

### Auth — start browser login

```
POST /auth/{provider}/login
Provider values: "anthropic" | "openai"
```

Spawns `claude login` (or `openai login`) in the background. The CLI opens a temporary HTTP
server on the loopback port and returns the authorization URL via stdout.

**Response 200:**
```json
{
  "url": "https://claude.ai/oauth/authorize?...",
  "poll_url": "/auth/anthropic/status"
}
```

**Response 503** — CLI binary not found:
```json
{ "available": false, "reason": "claude binary not found" }
```

The runner stores `{ pid, started_at }` in memory for the active login session.
Only one active login session per provider at a time; a new call cancels the previous.

---

### Auth — poll login status

```
GET /auth/{provider}/status
Provider values: "anthropic" | "openai"
```

Runs `claude whoami` (or `openai whoami`) — a cheap, non-destructive probe.

**Response 200:**
```json
{ "status": "connected", "username": "user@example.com" }
{ "status": "pending" }
{ "status": "error", "reason": "whoami exited 1" }
```

`pending` means the login process is still running but `whoami` has not returned exit 0 yet.
`error` means the login process exited non-zero or timed out (> 5 min since `POST /login`).

---

### Auth — logout

```
POST /auth/{provider}/logout
```

Runs `claude logout` / `openai logout` to clear stored credentials from the volume.

**Response 200:** `{ "status": "disconnected" }`

---

### Tasks — run

```
POST /tasks/run
```

Executes a CLI task against a single article. Article content travels in the request body —
no shared filesystem between backend and runner.

**Request body:**
```json
{
  "provider":    "anthropic",
  "task":        "inspect",
  "article_md":  "# Title\n\nBody text…",
  "context_md":  "Optional uploaded context file contents.",
  "args":        []
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `provider` | yes | `"anthropic"` or `"openai"` |
| `task` | yes | Slug identifying what to run — see task registry below |
| `article_md` | yes | Full article markdown. Written to `article.md` in the task dir. |
| `context_md` | no | Uploaded `.md` context file contents. Written to `context.md` if present. |
| `args` | no | Extra flags forwarded to the CLI invocation. Allow-listed — see §6. |

**Task directory (ephemeral):**
```
/tmp/bloghub_task_{uuid}/
  article.md       ← article content
  context.md       ← uploaded context (if provided)
```

The CLI is invoked with `cwd` set to this directory. Nothing else is accessible.
The directory is deleted in a `finally` block after the CLI exits or times out.

**Response 200:**
```json
{
  "exit_code": 0,
  "stdout":    "Gate result: pass\n…",
  "stderr":    "",
  "truncated": false
}
```

**Response 422** — unknown task slug or disallowed args.
**Response 503** — provider not authenticated (`whoami` exits non-zero before invocation).
**Response 504** — task timed out.

---

## 4. Login flow — end to end

The loopback redirect pattern (RFC 8252 §7.3, used by GitHub CLI, VS Code, Heroku CLI):

```
BlogHub UI      BlogHub backend      CLI runner (container)      Browser        Provider
    │                  │                       │                     │               │
    │ click Login      │                       │                     │               │
    │─────────────────►│                       │                     │               │
    │                  │ POST /auth/anthropic/login                  │               │
    │                  │──────────────────────►│                     │               │
    │                  │                       │ spawn `claude login`│               │
    │                  │                       │ CLI opens server    │               │
    │                  │                       │ on port 54322       │               │
    │                  │◄──────────────────────│                     │               │
    │                  │ { url: "https://claude.ai/authorize         │               │
    │◄─────────────────│         ?redirect_uri=http://localhost:54322/callback" }    │
    │ open new tab ───────────────────────────────────────────────►│               │
    │                  │                       │                     │ GET /authorize│
    │                  │                       │                     │──────────────►│
    │                  │                       │                     │ user logs in  │
    │                  │                       │                     │◄──────────────│
    │                  │                       │◄────────────────────│               │
    │                  │                       │ GET :54322/callback?code=…          │
    │                  │                       │ CLI exchanges code  │               │
    │                  │                       │ writes to volume    │               │
    │                  │                       │ port 54322 closes   │               │
    │ poll every 2s    │                       │                     │               │
    │─────────────────►│                       │                     │               │
    │                  │ GET /auth/anthropic/status                  │               │
    │                  │──────────────────────►│                     │               │
    │                  │                       │ `claude whoami`     │               │
    │                  │◄──────────────────────│                     │               │
    │                  │ { status: "connected", username: "…" }      │               │
    │◄─────────────────│                       │                     │               │
    │ card updates     │                       │                     │               │
```

**Why the user does not need to do anything after the browser step:**
The tab opens, the user authenticates on the provider's website, the provider redirects to
`localhost:54322`, the CLI's temporary server receives the callback and closes the tab
automatically (or shows "You can close this window"), and the UI detects completion via polling.
No manual copy-paste, no token handling.

**Port mapping requirement:**
The docker-compose host port mapping (`54322:54322`, `54323:54323`) must exist for the
browser's redirect to reach the container. Without it the callback returns
"connection refused" and the CLI login hangs.

---

## 5. Task isolation

The CLI subprocess inside the runner sees only:

| Path | Contents |
|------|----------|
| `/tmp/bloghub_task_{uuid}/article.md` | Article markdown |
| `/tmp/bloghub_task_{uuid}/context.md` | Uploaded context (optional) |

It does not see:

- Other articles
- The runner's own credential volumes (mounted at `/root/.claude`, not the task dir)
- The BlogHub backend source code or data
- Any environment variable containing secrets (env is allow-listed — see §6)

---

## 6. Subprocess environment inside runner

The CLI subprocess receives only:

```python
env = {
    "HOME":             "/root",
    "PATH":             "/usr/local/bin:/usr/bin:/bin",
    "CLAUDE_CONFIG_DIR": "/root/.claude",      # credential volume
    "OPENAI_CONFIG_DIR": "/root/.config/openai",
    # ANTHROPIC_API_KEY injected only if CLI session unavailable (fallback)
    # never logged — see security.md §1
}
```

`BLOGHUB_*`, `MEDIUM_*`, `DATABASE_*`, `SECRET_KEY`, and all other host secrets are
never forwarded.

---

## 7. Process limits

| Limit | Env var | Default |
|-------|---------|---------|
| Task wall-clock timeout | `RUNNER_TASK_TIMEOUT` | `60` s |
| Login wait timeout | `RUNNER_LOGIN_TIMEOUT` | `300` s (5 min) |
| Max stdout + stderr | `RUNNER_MAX_OUTPUT_BYTES` | `524288` (512 KB) |

On timeout: SIGTERM → 5 s grace → SIGKILL. Task dir cleaned up in `finally`.

---

## 8. BlogHub backend integration

The backend delegates to the runner via a thin client in `backend/services/cli_runner.py`.

**Environment variable:**

| Var | Default | Notes |
|-----|---------|-------|
| `CLI_RUNNER_URL` | `http://localhost:8001` | Set in `.env`; backend reads on startup |

**When `CLI_RUNNER_URL` is not set or runner is unreachable:**
- `GET /api/connections/{id}/oauth-start` → returns `{ available: false }`
- `POST /api/articles/{id}/inspect` → returns `503` with `{ detail: "AI runner not available" }`
- UI surfaces "AI runner not connected" inline — no crash

**Connections router changes:**

| Old behaviour | New behaviour |
|---------------|--------------|
| Spawn `claude login` subprocess directly | `POST {CLI_RUNNER_URL}/auth/anthropic/login` |
| Run `claude whoami` in process | `GET {CLI_RUNNER_URL}/auth/anthropic/status` |
| Run `claude logout` | `POST {CLI_RUNNER_URL}/auth/anthropic/logout` |
| Spawn task subprocess | `POST {CLI_RUNNER_URL}/tasks/run` |

The `_cli_login_pending` dict in `memory.py` is removed. Session state lives in the runner.

---

## 9. docker-compose excerpt

```yaml
services:
  cli-runner:
    build: ./cli-runner
    ports:
      - "8001:8001"    # runner REST API
      - "54322:54322"  # claude login loopback callback
      - "54323:54323"  # openai login loopback callback
    volumes:
      - claude-config:/root/.claude
      - openai-config:/root/.config/openai
    environment:
      - RUNNER_TASK_TIMEOUT=60
    restart: unless-stopped

volumes:
  claude-config:
  openai-config:
```

The BlogHub backend process runs on the host (not in the compose file). It reaches the
runner at `http://localhost:8001`.

---

## 10. What is explicitly out of scope for the runner

| Feature | Reason excluded |
|---------|----------------|
| Medium OAuth | Handled by BlogHub backend directly (server-side code exchange) |
| Hashnode / Dev.to token storage | API key only; stored in BlogHub backend memory store |
| Article persistence | Runner is stateless per-task; no database |
| Multiple simultaneous tasks per provider | Single active task per provider in v0.x |
