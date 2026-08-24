# SQLite Storage — Spec

**Status:** Implemented
**Backend:** `backend/store/backends/sqlite.py`
**Goal:** Durable storage that survives server restarts, with no external dependencies.

---

## Why SQLite

- Zero infra: one file, ships with Python (`sqlite3` stdlib)
- Survives restarts
- Supports concurrent reads (WAL mode)
- Trivially portable: copy `bloghub.db` to move all data
- Later: can be replaced by Postgres without changing the store interface

---

## Database file location

```
blog-hub/data/bloghub.db
```

Configurable via env var `BLOGHUB_DB_PATH`. The `data/` directory is gitignored.
Tests use an in-memory database: `BLOGHUB_DB_PATH=:memory:`.

---

## Schema

All timestamps are ISO-8601 strings (`2026-04-07T14:32:00Z`).

### Users and sessions (auth)

```sql
CREATE TABLE IF NOT EXISTS users (
    id            TEXT PRIMARY KEY,       -- UUID
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,          -- bcrypt via passlib
    created_at    TEXT NOT NULL,
    is_active     INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS sessions (
    token       TEXT PRIMARY KEY,         -- secrets.token_urlsafe(32)
    user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at  TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    remember_me INTEGER NOT NULL DEFAULT 0
);
```

### Articles

```sql
CREATE TABLE IF NOT EXISTS articles (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    body            TEXT NOT NULL DEFAULT '',
    body_path       TEXT,                 -- path to blob file for large bodies
    word_count      INTEGER NOT NULL DEFAULT 0,
    gate            TEXT NOT NULL DEFAULT 'pending',  -- pending | pass | warn | fail
    source          TEXT NOT NULL DEFAULT 'native',   -- native | imported
    source_platform TEXT,
    canonical_url   TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    user_id         TEXT REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS article_destinations (
    article_id  TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    platform    TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'none',  -- none | pending | published | error
    label       TEXT,
    url         TEXT,
    draft_id    TEXT,
    error       TEXT,
    PRIMARY KEY (article_id, platform)
);

CREATE TABLE IF NOT EXISTS article_timeline (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id  TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    timestamp   TEXT NOT NULL,
    event       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS article_assets (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id  TEXT    NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    filename    TEXT    NOT NULL,
    asset_path  TEXT    NOT NULL,
    mime_type   TEXT,
    created_at  TEXT    NOT NULL,
    UNIQUE(article_id, filename)
);

CREATE TABLE IF NOT EXISTS article_comments (
    id          TEXT PRIMARY KEY,
    article_id  TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    author      TEXT NOT NULL,
    text        TEXT NOT NULL,
    anchor      TEXT,                     -- JSON: { start, end } char offsets
    resolved    INTEGER NOT NULL DEFAULT 0,
    has_patch   INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS article_patches (
    id          TEXT PRIMARY KEY,
    article_id  TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    comment_id  TEXT REFERENCES article_comments(id) ON DELETE SET NULL,
    label       TEXT NOT NULL,
    removed     TEXT NOT NULL,
    added       TEXT NOT NULL,
    state       TEXT NOT NULL DEFAULT 'pending',  -- pending | accepted | rejected
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS article_chat_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id  TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    role        TEXT NOT NULL,
    text        TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
```

### Connections (AI + blog platforms)

```sql
CREATE TABLE IF NOT EXISTS connections (
    platform      TEXT PRIMARY KEY,
    token         TEXT NOT NULL,          -- Fernet-encrypted (see Token Encryption below)
    status        TEXT NOT NULL DEFAULT 'connected',  -- connected | disconnected | error
    username      TEXT,
    connected_at  TEXT NOT NULL,
    error_message TEXT,
    user_id       TEXT REFERENCES users(id) ON DELETE CASCADE
);
```

### Jobs

```sql
CREATE TABLE IF NOT EXISTS jobs (
    job_id       TEXT PRIMARY KEY,
    kind         TEXT NOT NULL,
    article_id   TEXT,
    status       TEXT NOT NULL DEFAULT 'pending',  -- pending | done | error
    result       TEXT,                    -- JSON-encoded
    error        TEXT,
    created_at   TEXT NOT NULL,
    completed_at TEXT,
    user_id      TEXT REFERENCES users(id) ON DELETE CASCADE
);
```

---

## Token Encryption

Connection tokens are encrypted at rest using Fernet (AES-128-CBC + HMAC-SHA256) via `backend/store/crypto.py`.

**Key:** `BLOGHUB_SECRET_KEY` env var (URL-safe base64, 32 bytes).

**Format:** encrypted values are prefixed `fernet:<ciphertext>`. Values without this prefix are treated as legacy plaintext and returned as-is (graceful migration — no backfill required).

**Key absent:** tokens stored and read as plaintext with a logged warning. Only acceptable for local dev.

See `.spec/backend/dependencies/security/service.md` for the full security contract.

---

## Store interface — Repository pattern

The public functions in `backend/store/` keep the same signatures across backends. Routers import from `store` only — never from a backend directly.

```
routers/articles.py
    | import store
store/__init__.py          <- selects backend, re-exports as flat functions
    | delegates to
store/backends/sqlite.py   <- current
store/backends/postgres.py <- future (same Protocol, different impl)
```

**Protocol:** `backend/store/base.py` defines `ArticleStore` (a `typing.Protocol`). All methods that read or write user-owned data accept `user_id: str`. Switching backends requires changing one line in `store/__init__.py`.

### User-scoped methods (require `user_id`)

```python
# Articles
list_articles(user_id, q, gate, status, platform, page, page_size, sort_by, sort_dir)
get_article(user_id, article_id)
create_article(user_id, title, source, source_platform, canonical_url)
update_article_body(user_id, article_id, body, event)
delete_article(user_id, article_id)

# Connections
save_connection(user_id, conn_id, token, status, username, error)
get_connection_token(user_id, conn_id)
delete_connection(user_id, conn_id)
list_connections(user_id)

# Jobs
create_job(user_id, kind, article_id)
get_job(user_id, job_id)
complete_job(user_id, job_id, result, error)

# Comments and patches
list_comments(user_id, article_id)
save_comment(user_id, article_id, ...)
list_patches(user_id, article_id)
save_patch(user_id, article_id, ...)

# Assets
store_asset(user_id, article_id, filename, data, mime_type)
get_asset(user_id, article_id, filename)
```

### Auth methods (no `user_id` — operate on users/sessions directly)

```python
create_user(email, password_hash) -> dict
get_user_by_email(email) -> dict | None
get_user_by_id(user_id) -> dict | None

create_session(token, user_id, expires_at, remember_me) -> None
get_session(token) -> dict | None         # returns None if expired
delete_session(token) -> None
delete_expired_sessions() -> int          # returns count deleted
```

### Global methods (no `user_id` — shared data or test utilities)

```python
reset() -> None           # test isolation: drops and recreates tables, re-inserts seeds
count_connected(user_id)  # scoped — counts connected platforms for one user
```

---

## Connection management

`SQLiteStore.__init__` opens a single `sqlite3.Connection` and holds it for the process lifetime. WAL mode is enabled on open:

```python
con = sqlite3.connect(DB_PATH, check_same_thread=False)
con.execute("PRAGMA journal_mode=WAL")
con.execute("PRAGMA foreign_keys=ON")
```

`check_same_thread=False` is safe because FastAPI runs handlers in a thread pool and SQLite WAL supports concurrent readers with one writer.

---

## Seed data

Six seed articles are inserted at startup if the `articles` table is empty. Seed insertion uses `INSERT OR IGNORE` (idempotent). In production (when real articles exist) seeds are skipped.

Seed articles have no `user_id` and are effectively invisible once users exist. They serve as fixtures for local dev and tests only.

---

## Test isolation

Tests set `BLOGHUB_DB_PATH=:memory:` via `conftest.py` before importing the store.
`POST /api/dev/reset` drops and recreates all tables, then re-inserts seeds.
The `reset_store` pytest fixture continues to work without modification.

---

## Migration path

No migration tooling for v1. Schema is created fresh on first run via `CREATE TABLE IF NOT EXISTS`.

When adding `user_id` to existing tables, the column is added as nullable with no default. Existing rows (if any) become unreachable to authenticated users — they are effectively orphaned. This is acceptable for a dev tool where existing data predates multi-user support.

For production migrations with real user data, `alembic` is the preferred tool — do not add it until there is data to protect.

---

## Files

| File | Purpose |
|------|---------|
| `backend/store/base.py` | `ArticleStore` Protocol — contract all backends must satisfy |
| `backend/store/backends/sqlite.py` | `SQLiteStore` — full implementation over `sqlite3` |
| `backend/store/crypto.py` | `encrypt_token` / `decrypt_token` — Fernet wrapper |
| `backend/store/__init__.py` | Instantiates backend, re-exports all public functions |
| `data/bloghub.db` | Runtime database file (gitignored) |
