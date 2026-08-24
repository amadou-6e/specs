# Backend Spec — Security Considerations

> Cross-cutting security requirements for tokens, sessions, OAuth flows, and agent execution.
> These apply across all routers and the CLI agent subsystem.
> Reference: OWASP Top 10 (2021).

---

## 1. Token Storage

### SQLite backend (`sqlite.py`) — current implementation

Tokens are persisted in the `connections` table, encrypted at rest using Fernet (AES-128-CBC + HMAC-SHA256) via `backend/store/crypto.py`.

**Encryption key:** `BLOGHUB_SECRET_KEY` env var (URL-safe base64, 32 bytes). Generate with:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Storage format:** encrypted tokens are prefixed with `fernet:` to distinguish from legacy plaintext values. `decrypt_token()` handles both transparently — no migration step required for existing rows.

**Behaviour when key is absent:** tokens stored and read as plaintext with a warning logged. Acceptable for local dev, not for production.

**OpenAI key — no file persistence:** the OpenAI API key is stored only in SQLite (encrypted). It is never written to `/root/.codex/api_key` or any file inside the cli-runner container. It is fetched from the store at task dispatch time, passed in the `POST /tasks/run` request body as `api_key`, and injected into the subprocess env as `OPENAI_API_KEY`. It does not survive past subprocess exit.

**Key co-location rule:** `BLOGHUB_SECRET_KEY` must never be stored in the same location as the SQLite file. In production, inject via the platform secrets manager (AWS SSM, Fly.io secrets, Docker secrets, etc.) — never commit to the repo.

### What must never appear in:

| Location | Examples to block |
|----------|-------------------|
| Log lines (any level) | `token=`, `Authorization:`, `api_key`, `client_secret`, `access_token` |
| HTTP response bodies | Only `status`, `username`, `connected_at` — never the raw token value |
| Error messages surfaced to the client | No credential values, no internal stack traces |
| CLI subprocess stdout captured for logging | May contain tokens; scrub before storing |
| URL query strings | Tokens must never appear as query parameters (`?token=...`) |

### Token scrubbing helper

Apply before any log write or error-message construction:

```python
import re

_SCRUB_RE = re.compile(
    r'(Bearer\s+|token["\']?\s*[:=]\s*|api[_-]?key["\']?\s*[:=]\s*|Authorization:\s*)'
    r'[^\s"\'&]{8,}',
    re.IGNORECASE
)

def scrub(text: str) -> str:
    """Replace credential-like values with [REDACTED] before logging."""
    return _SCRUB_RE.sub(r'\1[REDACTED]', text)
```

---

## 2. OAuth Flow Security

### State nonce — CSRF prevention

Every OAuth initiation must generate a cryptographically random state parameter:

```python
import secrets

# oauth-start
state = secrets.token_urlsafe(32)          # 256 bits of entropy
_oauth_pending[state] = {
    "conn_id":  conn_id,
    "expires":  time.time() + 600,         # 10-minute TTL
}
# state is included in the authorization URL returned to the frontend

# oauth-callback  (?code=...&state=...)
entry = _oauth_pending.pop(state, None)    # single-use -- pop removes it
if entry is None:
    raise HTTPException(400, "Invalid or expired OAuth state")
if entry["conn_id"] != conn_id:
    raise HTTPException(400, "State/connection mismatch")
if time.time() > entry["expires"]:
    raise HTTPException(400, "OAuth state expired")
```

Rules:
- State tokens are **single-use** — `pop()` on first use.
- TTL: 10 minutes. Stale entries purged lazily on access or via a 15-minute background sweep.
- Missing, empty, or unrecognised `state` → `400 Bad Request`; log the event (scrubbed), never redirect.
- A new `oauth-start` call always generates a fresh state; previous states for the same `conn_id` are invalidated.

### Client secret

- `MEDIUM_CLIENT_SECRET` (and any future provider secrets) live in **environment variables only**.
- Never returned in any HTTP response, never logged, never embedded in frontend code.
- The authorization-code → access-token exchange happens entirely server-side (backend → provider).

### postMessage origin validation

The OAuth callback HTML page must send `postMessage` only to the same origin:

```js
// In the callback HTML page served by /api/connections/{id}/oauth-callback:
if (window.opener) {
    window.opener.postMessage(
        { type: 'oauth-complete', platform: '{conn_id}' },
        '{APP_ORIGIN}'          // injected server-side; never '*'
    );
}

// In the parent (Settings screen):
window.addEventListener('message', (e) => {
    if (e.origin !== window.location.origin) return;   // mandatory check
    if (e.data?.type !== 'oauth-complete') return;
    // safe to reload connection list
});
```

- The `targetOrigin` in `postMessage` must be the app's exact origin — **never `'*'`**.
- The parent listener must validate `e.origin` before acting on any message.

### CLI browser login state token

For CLI-based login (Anthropic, OpenAI), a lightweight state token tracks the pending login:

```python
state_token = secrets.token_urlsafe(16)
_cli_login_pending[conn_id] = {
    "pid":         proc.pid,
    "state_token": state_token,
    "started_at":  time.time(),
}
```

- `cli-login-status` returns `{ status: "pending" }` until `whoami` succeeds or TTL expires.
- Abandoned sessions (CLI process terminated without success) auto-expire after 5 minutes.

---

## 3. CLI Credential Isolation

- The backend **never reads raw token bytes** from CLI credential files — it only calls
  `claude auth status` / `codex login status` to verify auth state.
- The subprocess environment is an explicit allow-list (see `agent-environment.md § 5`).
  Passing `os.environ` wholesale to a subprocess risks leaking `SECRET_KEY`, database
  connection strings, and other process-level secrets.
- Each CLI invocation runs in a fresh `tempfile.mkdtemp()` working directory, deleted in a
  `finally` block after completion.
- API keys injected into the subprocess environment (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`)
  come from the store's `get_connection_token()` (decrypted in memory) — they are **not logged**
  at any point and are passed via the `api_key` field in the `POST /tasks/run` request body,
  not as CLI arguments.
- The OpenAI key is **never written to disk** inside the cli-runner container. The `/auth/openai/key`
  endpoint and file-based key storage (`/root/.codex/api_key`) have been removed.
- On Windows: verify `TEMP`/`TMP` point to a user-writable directory without world-read
  access before writing any task artefacts.

---

## 4. CORS Policy

CORS is configured in `backend/main.py` and restricts which browser origins can make cross-origin requests to the API.

**Local/dev (default — no env var set):**
```python
allow_origin_regex = r"https?://(localhost|127\.0\.0\.1)(:\d+)?"
```
Covers any localhost port, including the dynamic port selected by `start.sh`.

**Production:**
Set `BLOGHUB_ALLOWED_ORIGINS` to a comma-separated list of exact origins:
```
BLOGHUB_ALLOWED_ORIGINS=https://bloghub.example.com
```
When this env var is set, the regex is disabled and only the listed origins are allowed.

**Allowed methods and headers** are restricted to what the app actually uses:
- Methods: `GET, POST, PUT, DELETE, OPTIONS`
- Headers: `Content-Type, Authorization`

`allow_origins=["*"]` is never acceptable — it disables SameSite CSRF protection and allows any website to make authenticated requests on behalf of a logged-in user.

---

## 5. Session Management

Multi-user session-based authentication is implemented via a `sessions` table in SQLite.

**Design:**
- Session token: `secrets.token_urlsafe(32)` (256 bits of entropy)
- Cookie name: `bloghub_session`, `HttpOnly`, `SameSite=Strict`
- `Secure` flag: set when `BLOGHUB_HTTPS=true` env var is present
- Cookie contains only the opaque session token — no user data
- Session row contains: `token`, `user_id`, `expires_at`, `created_at`, `remember_me`

**Expiry:**
- `remember_me=true` → 30 days
- `remember_me=false` → 1 hour

**Invalidation:**
- Logout deletes the session row server-side (client cookie removal alone is insufficient)
- Expired sessions are deleted on lookup and purged at app startup
- `SameSite=Strict` prevents CSRF for all mutation endpoints without a separate CSRF token

**Enforcement:** `backend/middleware/auth.py` checks every `/api/*` request except:
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /health`
- `GET /screens/*`

Do not accept session tokens in URL query parameters.

**TODOs:** admin session revocation, session listing per user.

---

## 6. HTTP Security Headers

All responses from the FastAPI app must include the following headers via middleware:

| Header | Required value |
|--------|---------------|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` (except OAuth popup callback page — omit there) |
| `Referrer-Policy` | `no-referrer` |
| `Content-Security-Policy` | `default-src 'self'` (tighten per-route; see note) |

```python
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    # CSP is set per-route where needed; default middleware sets the baseline
    return response
```

CSP notes:
- The OAuth callback HTML page needs `script-src 'unsafe-inline'` (for the postMessage script)
  and `frame-ancestors 'none'` — set as a response header on that route only.
- API JSON routes need no `script-src` at all; set `default-src 'none'` on those.

---

## 7. Input Validation

| Input | Validation rules |
|-------|-----------------|
| `token` (all PUT /api/connections/{id}) | Strip leading/trailing whitespace; reject empty; reject strings containing null bytes (`\x00`) or control characters (0x00-0x1F except TAB) |
| `conn_id` path parameter | Validated against the `ConnectionId` enum before any use; never interpolated into shell commands or log format strings |
| OAuth `state` parameter | Only characters from `[A-Za-z0-9_\-]`; length 20-200 chars |
| CLI subprocess arguments | Built from an allow-list of known flags; `conn_id` is never passed as a shell argument |
| `email` (auth endpoints) | Valid email format; max 254 chars |
| `password` (auth endpoints) | Minimum 8 characters; never logged |
| Query parameters | Standard Pydantic validation; no raw SQL construction |

Never construct shell commands via string formatting with user-supplied data. Use
`subprocess.run([cli_path, "--flag", safe_value], ...)` — the list form, not shell=True.

---

## 8. Scope / Least-Privilege Checklist

Request the minimum OAuth scopes needed:

| Provider | Minimum scopes |
|----------|---------------|
| Medium OAuth | `basicProfile`, `publishPost` |
| Anthropic CLI | Workspace-scoped session; do not request organisation admin |
| OpenAI CLI | Project-scoped API key when possible; no billing or org admin access |

Platform tokens stored via manual key entry should be documented (in the UI help link) with
the exact minimum permissions required so users do not paste organisation-level keys.

---

## 9. Dependency Supply Chain

- Pin all dependencies with exact versions in `requirements.txt` / `pyproject.toml`.
- Run `pip audit` (or `safety check`) in CI on every PR; block merges on HIGH+ CVEs.
- The server-side OAuth code exchange must use `httpx` with `verify=True` (default).
  Never set `verify=False` in any HTTP client used for credential exchange.
- Do not use `eval()` or `exec()` anywhere in the backend; prefer safe alternatives.
