# Dependency — Secret & Credential Security

This file maps every secret in the system: where it originates, how it is stored, who reads it, how it travels, and what guards it. It is a cross-cutting dependency referenced by every service.

---

## 1. Secret Inventory

| Secret | Origin | Stored in | Who reads it | Never appears in |
|--------|--------|-----------|--------------|-----------------|
| `BLOGHUB_SECRET_KEY` | Env var (operator-generated) | OS process environment only | `backend/store/crypto.py` (Fernet key), `backend/middleware/auth.py` (session validation) | Responses, logs, DB, any subprocess env |
| Medium access token | OAuth code exchange (`/v1/tokens`) | `connections` table (Fernet-encrypted) | Articles push, Medium OAuth router | Responses, logs, URLs |
| Medium client secret | Env var `MEDIUM_CLIENT_SECRET` | OS process environment only | Connections router (token exchange) | Frontend, logs, any response body |
| Medium client ID | Env var `MEDIUM_CLIENT_ID` | OS process environment only | Connections router (auth URL) | Not a secret — appears in browser redirect |
| Hashnode PAT | User input (`PUT /api/connections/hashnode`) | `connections` table (Fernet-encrypted) | Articles push | Responses, logs |
| Dev.to API key | User input (`PUT /api/connections/devto`) | `connections` table (Fernet-encrypted) | Articles push | Responses, logs |
| Anthropic API key | User input or `ANTHROPIC_API_KEY` env | `connections` table (Fernet-encrypted) | Agent service (CLI env injection) | Responses, logs, CLI argv, disk |
| OpenAI API key | User input or `OPENAI_API_KEY` env | `connections` table (Fernet-encrypted) | Agent service (CLI env injection via request body) | Responses, logs, CLI argv, disk, cli-runner container filesystem |
| OAuth state nonce | `secrets.token_urlsafe(32)` | `_oauth_pending[state]` (TTL 10 min) | Connections router callback | Anywhere after single-use pop |
| CLI login state token | `secrets.token_urlsafe(16)` | `_cli_login_pending[conn_id]` (TTL 5 min) | Connections router poll | Any response beyond the internal poll |
| Session token | `secrets.token_urlsafe(32)` | `sessions` table in SQLite | Auth middleware (every request) | Response bodies, logs, URLs |
| User password | User input | Never stored — bcrypt hash only | Auth router (login verification) | Logs, responses, DB (only hash stored) |

---

## 2. Token Storage Tiers

### Current — SQLite with Fernet encryption

```
User input / OAuth response
        |
        v
encrypt_token(plaintext)          <- backend/store/crypto.py
        |                            uses BLOGHUB_SECRET_KEY env var
        v
"fernet:<ciphertext>"  ->  connections.token column in SQLite
        |
        v
decrypt_token(stored)             <- called by get_connection_token()
        |
        v
plaintext token (in memory only, for duration of request)
```

**Graceful migration:** values without the `fernet:` prefix are returned as-is (legacy plaintext passthrough). On next `save_connection()` call they are re-encrypted.

**Key absent:** tokens stored/read as plaintext with a logged warning. Acceptable for local dev only.

**Key must not be co-located with the SQLite file.** In production, inject via platform secrets manager.

### Future — external secrets manager

When horizontal scaling is needed, replace SQLite with Postgres and use AWS Secrets Manager, HashiCorp Vault, or equivalent for the encryption key. The `crypto.py` interface stays the same.

---

## 3. Credential Flow Diagrams

### Platform token (Hashnode / Dev.to example)

```
User          PUT /api/connections/hashnode
              body: { "token": "hnp_..." }
                |
                v
         connections router
              validate: not empty, no null bytes, no control chars 0x00-0x1F
                |
                v
         store.save_connection("hashnode", token, user_id)
              encrypt_token("hnp_...") -> "fernet:<blob>"
              stored in connections table
                |
                v
         push job
              token = store.get_connection_token("hashnode", user_id)
              decrypt_token("fernet:<blob>") -> "hnp_..." (in memory)
              HashnodeClient(personal_access_token=token)
              # token travels only as Authorization header, over TLS
              # token is never logged: verify via scrub() before any log.debug()
```

### Medium OAuth token flow

```
Browser popup -> medium.com/m/oauth/authorize?client_id=...&state=<nonce>
                              |
                              v
              User grants permission
                              |
                              v
medium.com -> GET /api/connections/medium/oauth-callback?code=...&state=<nonce>
                              |
              backend validates state nonce (pop -- single use, TTL check)
                              |
              POST https://api.medium.com/v1/tokens
                  { code, client_id, client_secret }    <- client_secret server-side only
                              |
              receives access_token
                              |
              store.save_connection("medium", token, user_id)
              encrypt_token(token) -> stored in SQLite
                              |
              responds with popup HTML -> postMessage({ status: "connected" }, APP_ORIGIN)
                              # token NEVER in postMessage payload
```

### OpenAI API key -> CLI subprocess injection

```
Backend (task dispatch)
    |
    +-- store.get_connection_token("openai", user_id)
    |       decrypt_token("fernet:<blob>") -> "sk-proj-..." (in memory)
    |
    +-- runner.run_task(provider="openai", ..., api_key="sk-proj-...")
    |       POST /tasks/run { ..., "api_key": "sk-proj-..." }
    |                                    ^
    |                            travels over localhost HTTP only
    |                            (cli-runner is on same host/network)
    |
cli-runner receives TaskRequest.api_key
    |
    +-- _build_env("openai", api_key="sk-proj-...")
    |       env["OPENAI_API_KEY"] = "sk-proj-..."
    |       # key is in env dict -- never as a CLI argument
    |       # env dict is not logged
    |
    +-- subprocess.Popen(cmd, env=env, ...)
            # key available to codex CLI via environment
            # key does NOT survive past subprocess exit
            # key is NEVER written to /root/.codex/api_key or any file
```

### Session authentication flow

```
Browser
    |
    +-- POST /api/auth/login { email, password, remember_me }
    |
backend/routers/auth.py
    |
    +-- store.get_user_by_email(email)
    +-- passlib.verify(password, user.password_hash)
    |       # password compared in memory, never stored raw
    |
    +-- token = secrets.token_urlsafe(32)
    +-- store.create_session(token, user_id, expires_at, remember_me)
    |
    +-- Set-Cookie: bloghub_session=<token>; HttpOnly; SameSite=Strict; [Secure]
    |       # max_age=2592000 (30d) if remember_me else max_age=3600 (1h)

Every subsequent /api/* request:
    |
    +-- middleware reads bloghub_session cookie
    +-- store.get_session(token) -- lookup in sessions table
    |       if not found or expired -> 401, clear cookie
    |
    +-- request.state.user_id = session.user_id
    +-- handler runs with user context
```

---

## 4. What Each Secret Guards — and What Must Not Happen

### `BLOGHUB_SECRET_KEY`

| Must | Must not |
|------|----------|
| Be injected via env var at startup | Be committed to the repo |
| Be used only by `crypto.py` and `auth.py` | Be passed to any subprocess |
| Be rotated out-of-band if compromised | Be stored in the same volume as the SQLite DB |

### Platform tokens (Medium, Hashnode, Dev.to)

| Must | Must not |
|------|----------|
| Be validated at input (non-empty, ASCII-safe) | Be returned by `GET /api/connections` |
| Be encrypted before writing to SQLite | Be included in error messages sent to client |
| Travel to external APIs only over TLS | Appear in `jobs` records or log output |

### AI provider keys (Anthropic, OpenAI)

| Must | Must not |
|------|----------|
| Be encrypted in SQLite | Appear as a CLI argument (`--api-key ...`) |
| Be injected via environment variable into subprocess only | Be written to any file inside the cli-runner |
| Be decrypted in memory only for the duration of the request | Be present in the subprocess `argv` list |
| Be passed in the `api_key` field of `POST /tasks/run` body | Flow through `jobs` result records |

### Session token

| Must | Must not |
|------|----------|
| Be generated with `secrets.token_urlsafe(32)` | Appear in response bodies or logs |
| Be stored only in the `sessions` table | Be accepted via URL query parameter |
| Be invalidated server-side on logout | Be used after `expires_at` |
| Travel only in `HttpOnly; SameSite=Strict` cookie | Appear in the `bloghub_session` cookie value decoded |

### User password

| Must | Must not |
|------|----------|
| Be hashed with bcrypt (passlib, 12 rounds) before any storage | Be stored in any form other than the hash |
| Be compared only via `passlib.verify()` | Be logged at any level |
| Return generic error on failure (no user enumeration) | Appear in error messages |

### OAuth state nonce

| Must | Must not |
|------|----------|
| Be generated with `secrets.token_urlsafe(32)` | Be reused (pop on first call) |
| Expire after 10 minutes | Be accepted after TTL |
| Be single-use | Be stored anywhere after validation |

---

## 5. Token Scrubbing

Applied before any `log.debug()`, `log.info()`, or error string construction:

```python
import re

_SCRUB_RE = re.compile(
    r'(Bearer\s+|token["\']?\s*[:=]\s*|api[_-]?key["\']?\s*[:=]\s*|Authorization:\s*)'
    r'[^\s"\'&]{8,}',
    re.IGNORECASE
)

def scrub(text: str) -> str:
    return _SCRUB_RE.sub(r'\1[REDACTED]', text)
```

**Applied at:**
- Any request/response log middleware
- All `except` blocks that format error messages with request context
- Before writing any CLI stdout/stderr excerpt to `job["error"]`

---

## 6. API Response Rules — What Is Never Returned

`GET /api/connections` (and all connection endpoints) return only:

```json
{
  "id":           "hashnode",
  "label":        "Hashnode",
  "type":         "blog",
  "auth_method":  "token",
  "status":       "connected",
  "username":     null,
  "connected_at": "2026-04-03T10:00:00Z",
  "error_message": null
}
```

The `token` field is **never serialised**. It does not appear in `ConnectionInfo`, `SaveTokenResponse`, or any error response.

`GET /api/auth/me` returns only `{ id, email, created_at }` — never the password hash or session token.

---

## 7. Input Validation at Token Entry Points

All `PUT /api/connections/{id}` calls validate the submitted token before storage:

| Check | Rule |
|-------|------|
| Non-empty | `len(token.strip()) > 0` |
| No null bytes | `'\x00' not in token` |
| No control characters | No characters in range `0x01-0x1F` (TAB `0x09` allowed) |
| Reasonable length | `4 <= len(token) <= 4096` |
| Not interpolated into shell | Token is stored as data; it never reaches `subprocess` argv |
| OpenAI key validation | Probed against `GET https://api.openai.com/v1/models` before saving |

---

## 8. Subprocess Credential Isolation

The subprocess environment is constructed as an explicit **allow-list** — `os.environ` is never copied wholesale. Only the named variables below are forwarded:

```python
def _build_env(provider: str, api_key: str | None = None) -> dict[str, str]:
    env: dict[str, str] = {
        "HOME": "/root",
        "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
        "CLAUDE_CONFIG_DIR": _PROVIDERS["anthropic"]["config_dir"],
        "CODEX_HOME": _PROVIDERS["openai"]["config_dir"],
    }
    if api_key:
        key_name = "ANTHROPIC_API_KEY" if provider == "anthropic" else "OPENAI_API_KEY"
        env[key_name] = api_key  # never logged
    return env
```

**Process independence guarantees:**
- `BLOGHUB_SECRET_KEY` is never forwarded to subprocesses
- `MEDIUM_CLIENT_SECRET` is never forwarded to subprocesses
- The subprocess cannot read the server's in-memory session store or connection tokens
- Each task runs in a fresh `tempfile.mkdtemp()` working directory, deleted in `finally`
- On timeout: SIGTERM -> 5s grace -> SIGKILL; work dir still cleaned in `finally`

---

## 9. Secret Lifetime Summary

| Secret | Created | Expires / Deleted |
|--------|---------|-------------------|
| Platform token (SQLite) | `PUT /api/connections/{id}` | `DELETE /api/connections/{id}` |
| Medium access token | OAuth callback | Same as above |
| `MEDIUM_CLIENT_SECRET` | Server start (env) | Process exit |
| `BLOGHUB_SECRET_KEY` | Server start (env) | Process exit |
| OAuth state nonce | `GET /oauth-start` | First use (pop) or 10 min TTL |
| CLI login state token | `GET /oauth-start` (CLI flow) | `whoami` success or 5 min TTL |
| AI key in subprocess env | Subprocess spawn | Subprocess exit |
| Temp working directory | Subprocess spawn | `finally` block after subprocess exits |
| Session token | `POST /api/auth/login` | `POST /api/auth/logout` or `expires_at` |
| User password (in memory) | `POST /api/auth/register` or `/login` | End of request handler |
