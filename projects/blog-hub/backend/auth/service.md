# Auth Service Spec — User and Session Management

> Covers registration, login, logout, session lifecycle, and the auth middleware.
> Security constraints (token scrubbing, cookie flags, etc.) are in `.spec/backend/security.md`.
> Data model (users/sessions tables) is in `.spec/storage/sql.md`.

---

## Scope

- Multi-user: each user has their own isolated data (articles, connections, jobs)
- Self-registration: open signup, no invite required
- Session-based auth: stateful server-side sessions, HttpOnly cookie
- No email sending yet: verification and password reset are future TODOs

**Out of scope (TODOs):**
- Admin panel (list users, delete accounts, revoke sessions)
- Email verification on registration
- Password reset via email

---

## Files

| File | Purpose |
|------|---------|
| `backend/routers/auth.py` | API endpoints: register, login, logout, me |
| `backend/middleware/auth.py` | Request middleware: enforces session on every `/api/*` |
| `backend/store/backends/sqlite.py` | Auth store methods: create_user, get_user_by_email, create/get/delete session |

---

## API Endpoints

Router prefix: `/api/auth`

### POST /api/auth/register

Create a new user account.

**Request body:**
```json
{ "email": "user@example.com", "password": "mypassword123" }
```

**Validation:**
- `email`: valid format, max 254 chars, unique in `users` table
- `password`: minimum 8 characters

**Flow:**
1. Validate email format and length
2. Check email uniqueness — return 409 if taken
3. Hash password with bcrypt (`passlib.hash.bcrypt.hash(password)`, 12 rounds)
4. Insert into `users` table with a new UUID
5. Auto-login: create a session (same as login flow, `remember_me=false`)
6. Return 201 with session cookie set

**Responses:**
- `201 Created`: `{ "id": "...", "email": "..." }` + `Set-Cookie: bloghub_session=...`
- `409 Conflict`: `{ "detail": "An account with this email already exists" }`
- `422 Unprocessable`: validation errors

**Error messages must not reveal whether an email exists** during registration. The 409 is acceptable here since the user just submitted that email themselves.

---

### POST /api/auth/login

Verify credentials and issue a session.

**Request body:**
```json
{ "email": "user@example.com", "password": "mypassword123", "remember_me": false }
```

**Flow:**
1. Look up user by email
2. If not found or `is_active=false`: return 401 (same message as wrong password)
3. Verify password: `passlib.hash.bcrypt.verify(password, user.password_hash)`
4. If mismatch: return 401
5. Generate `token = secrets.token_urlsafe(32)`
6. Compute expiry: `+30 days` if `remember_me` else `+1 hour`
7. Insert into `sessions` table
8. Set `bloghub_session` cookie with appropriate `max_age`
9. Return 200

**Session cookie attributes:**
```
Set-Cookie: bloghub_session=<token>; HttpOnly; SameSite=Strict; Path=/
Max-Age: 2592000   # 30 days if remember_me
Max-Age: 3600      # 1 hour if not remember_me
Secure             # only when BLOGHUB_HTTPS=true
```

**Responses:**
- `200 OK`: `{ "id": "...", "email": "..." }` + cookie
- `401 Unauthorized`: `{ "detail": "Invalid email or password" }` — same message for both wrong email and wrong password (no user enumeration)

---

### POST /api/auth/logout

Invalidate the current session.

**Flow:**
1. Read `bloghub_session` cookie
2. Delete session row from `sessions` table (no-op if already gone)
3. Clear the cookie (`max_age=0`)
4. Return 200

**Responses:**
- `200 OK`: `{ "status": "logged_out" }`
- No 401 on missing cookie — logout is always safe to call

---

### GET /api/auth/me

Return the current user's profile. Used by frontend screens to check auth state on load.

**Response:**
```json
{ "id": "uuid", "email": "user@example.com", "created_at": "2026-04-08T..." }
```

**Responses:**
- `200 OK`: user profile
- `401 Unauthorized`: no valid session (triggers frontend redirect to login)

---

## Middleware

`backend/middleware/auth.py` — applied to every request.

**Public paths (bypass auth check):**
```
POST /api/auth/register
POST /api/auth/login
GET  /health
GET  /screens/*    (static files — login page must be reachable)
```

**All other `/api/*` paths are protected.**

**Enforcement flow:**
```
Request arrives
    |
    +-- path in public list? -> pass through
    |
    +-- read Cookie: bloghub_session
    |       missing? -> 401 { "detail": "Authentication required" }
    |
    +-- store.get_session(token)
    |       None or expires_at < now?
    |           -> delete stale row
    |           -> clear cookie in response
    |           -> 401
    |
    +-- request.state.user_id = session["user_id"]
    +-- pass to handler
```

**Startup cleanup:** `delete_expired_sessions()` is called once on app startup to purge stale rows from the `sessions` table.

---

## User data scoping

Every router reads `request.state.user_id` (set by middleware) and passes it to all store calls. No router has any knowledge of sessions or auth — that boundary is maintained strictly.

Example pattern in a router:
```python
@router.get("/api/articles")
def list_articles(request: Request, ...):
    user_id = request.state.user_id      # set by middleware
    articles, total = store.list_articles(user_id=user_id, ...)
    ...
```

---

## Password handling

- Library: `passlib[bcrypt]` (`passlib.hash.bcrypt`)
- Work factor: 12 rounds (bcrypt default)
- Salt: auto-generated per hash by passlib (unique per password even if same input)
- Verification: `passlib.hash.bcrypt.verify(plaintext, stored_hash)` — constant-time comparison
- The plaintext password exists only in memory for the duration of the request handler
- It is never logged, stored, or forwarded anywhere

---

## Frontend integration

### Login screen: `screens/auth/login.html`

Single page, two tabs (Login / Register).

**Login tab flow:**
1. User submits email + password + remember_me checkbox
2. `POST /api/auth/login`
3. Success: redirect to `?next=` param or `/screens/overview/v3.html`
4. 401: show inline error "Invalid email or password"

**Register tab flow:**
1. User submits email + password
2. `POST /api/auth/register`
3. Success (201): auto-login happens server-side, redirect to overview
4. 409: show inline error "An account with this email already exists"
5. 422: show field-level validation errors

### Auth guard on all other screens

Every existing screen includes this snippet near the top of its `<script>` block:

```javascript
fetch('/api/auth/me').then(r => {
  if (!r.ok) {
    window.location.href = '/screens/auth/login.html?next='
      + encodeURIComponent(location.pathname);
  }
});
```

### Logout button

Present in the settings/nav area. On click:
```javascript
await fetch('/api/auth/logout', { method: 'POST' });
window.location.href = '/screens/auth/login.html';
```

---

## Session lifetime summary

| Event | Action |
|-------|--------|
| `POST /api/auth/login` | Create session row, set cookie |
| `POST /api/auth/logout` | Delete session row, clear cookie |
| Session `expires_at` reached | Deleted on next lookup, cookie cleared in response |
| App startup | All expired sessions deleted from DB |
| User account deleted (future admin) | All sessions cascade-deleted via FK |
