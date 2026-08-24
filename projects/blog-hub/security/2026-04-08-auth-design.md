# Multi-User Authentication Design

## Goal

Add email and password authentication to BlogHub with isolated per-user data. Each user registers independently, logs in, and sees only their own articles, connections, jobs, and related data.

## Architecture

Session-based auth using a `sessions` table in the existing SQLite database. A FastAPI middleware checks a signed HttpOnly cookie on every `/api/*` request and attaches `user_id` to `request.state`. All store methods are scoped by `user_id`.

## Data Model

Two new tables added to the existing SQLite schema:

```sql
CREATE TABLE users (
    id            TEXT PRIMARY KEY,       -- UUID
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,          -- bcrypt via passlib
    created_at    TEXT NOT NULL,
    is_active     INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE sessions (
    token       TEXT PRIMARY KEY,         -- secrets.token_urlsafe(32)
    user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at  TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    remember_me INTEGER NOT NULL DEFAULT 0
);
```

Every existing user-owned table gets a `user_id TEXT` column (nullable, no default):
- `articles`, `connections`, `jobs`, `comments`, `patches`, `assets`

Existing rows without a `user_id` become unreachable — effectively orphaned. Fresh registrations start a clean slate.

## API Endpoints

New router: `backend/routers/auth.py`, prefix `/api/auth`.

| Method | Path | Auth required | Description |
|--------|------|---------------|-------------|
| `POST` | `/api/auth/register` | No | Create account. Body: `{ email, password }`. Returns 201. |
| `POST` | `/api/auth/login` | No | Verify credentials, create session, set cookie. Body: `{ email, password, remember_me }`. |
| `POST` | `/api/auth/logout` | Yes | Delete session row, clear cookie. |
| `GET`  | `/api/auth/me` | Yes | Return `{ id, email, created_at }` for the current user. |

**Validation:**
- Email: valid format, unique (409 on duplicate)
- Password: minimum 8 characters
- Login failure: always return generic `"Invalid email or password"` — no user enumeration

**Session cookie:** name `bloghub_session`, HttpOnly, SameSite=Strict. Secure flag set when `BLOGHUB_HTTPS=true` env var is present.

**Session expiry:**
- `remember_me=true` → 30 days
- `remember_me=false` → 1 hour

## Middleware

`backend/middleware/auth.py` — checks every request to `/api/*`.

**Public paths (no auth check):**
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /health`
- `GET /screens/*`

**Flow for protected paths:**
1. Read `bloghub_session` cookie
2. No cookie → 401
3. Look up session in DB
4. Not found or `expires_at` in the past → delete stale row, return 401, clear cookie
5. Attach `user_id` to `request.state.user_id`
6. Pass to handler

**Startup cleanup:** on app startup, delete all expired sessions from the DB.

## Data Scoping

`ArticleStore` protocol (`backend/store/base.py`) gets `user_id: str` added to every method that reads or writes user-owned data:

- `list_articles`, `get_article`, `create_article`, `update_article_body`, `delete_article`
- `save_connection`, `get_connection_token`, `delete_connection`, `list_connections`
- `create_job`, `get_job`, `complete_job`
- `list_comments`, `save_comment`
- `list_patches`, `save_patch`
- `store_asset`, `get_asset`

The SQLite backend adds `WHERE user_id = ?` (or `AND user_id = ?`) to all affected queries.

Routers read `user_id` from `request.state.user_id` (set by middleware) and pass it to store calls. Routers have no knowledge of sessions.

**Not scoped (global):** platform metadata (`_CONNECTION_META`, `_PLATFORM_META`), health endpoint.

## Frontend

### New screen: `screens/auth/login.html`

Single page with two tabs: Login and Register.

**Login tab:**
- Email + password fields
- "Remember me" checkbox
- `POST /api/auth/login` on submit
- Success: redirect to `?next=` param or `/screens/overview/v3.html`
- 401: inline error "Invalid email or password"

**Register tab:**
- Email + password fields (password min 8 chars, strength hint shown)
- `POST /api/auth/register` on submit
- Success: auto-login then redirect to overview
- 409: inline error "An account with this email already exists"

### Auth guard (all existing screens)

Small inline script at the top of every existing screen:

```javascript
fetch('/api/auth/me')
  .then(r => { if (!r.ok) window.location.href = '/screens/auth/login.html?next=' + encodeURIComponent(location.pathname); })
```

### Logout

A logout button in the settings/nav area calls `POST /api/auth/logout` then redirects to login.

## New Dependency

- `passlib[bcrypt]` — add to `backend/requirements.txt`

## TODOs (out of scope)

- **Admin panel:** list users, delete accounts, revoke individual sessions
- **Email verification:** send confirmation email on registration (requires SMTP config)
- **Password reset:** "forgot password" flow via email link (requires SMTP config)
