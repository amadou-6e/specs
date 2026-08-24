# Dependency — In-Memory Store (`backend/store/memory.py`)

The shared store is a **module-level dict** used by multiple services. Because it is shared global state, all callers that write to it are implicitly coupled. This file documents the function-level interface so that each service knows exactly what it can call.

---

## 1. Store Layout

```python
_articles:    dict[str, dict]    # keyed by article_id
_jobs:        dict[str, dict]    # keyed by job_id
_platforms:   list[dict]         # seed-only; not mutated at runtime
_connections: dict[str, dict]    # keyed by conn_id; survives reset()
```

> **`_connections` is NOT reset** by `POST /api/dev/reset`. All other stores are.

---

## 2. Callers per Store

| Store | Service / Router | Access |
|-------|-----------------|--------|
| `_articles` | Articles router | R/W — all CRUD + push + inspect |
| `_articles` | Agent service | R/W — create blank, write body + wordCount |
| `_articles` | Comments-Patches service | R — validate article_id; W — write body on patch accept |
| `_jobs` | Articles router | W — create + update job records |
| `_jobs` | Agent service | W — create + update job records |
| `_jobs` | Jobs router | R — read-only poll |
| `_connections` | Connections router | R/W — save, delete, list |
| `_connections` | Articles push service | R — `get_connection_token()` to verify platform cred |
| `_connections` | Agent service | R — `get_connection_token()` to verify AI provider cred |
| `_connections` | Platforms router | R — `list_connections()` to derive connected state |

---

## 3. Articles Interface

### `list_articles(...) → tuple[list[dict], int]`

```python
def list_articles(
    q: str | None = None,          # substring match on title (case-insensitive)
    gate: str | None = None,       # "pass" | "warn" | "fail" | "pending"
    status: str | None = None,     # platform status filter
    platform: str | None = None,   # "medium" | "hashnode" | "devto"
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "updatedAt",    # "updatedAt" | "createdAt" | "title"
    sort_dir: str = "desc",        # "asc" | "desc"
) -> tuple[list[dict], int]:       # (page items, total count)
```

**Filter combinations:**
- `status + platform` → articles where `destinations[platform].status == status`
- `status` only → articles where any destination has that status
- `platform` only → articles where that destination status != `"none"`

### `get_article(article_id: str) → dict | None`

Returns the full article dict or `None` if not found.

### `create_article(title: str) → dict`

Creates a new article with:
- `id`: `"art_<8 hex chars>"`
- `word_count`: `0`
- `gate`: `"pending"`
- All three destinations at `status="none"`, `label="—"`
- `recent_timeline`: one entry `"Article created"`

Returns the full article dict.

### `delete_articles(ids: list[str], force: bool = False) → list[str]`

Deletes articles by id. Returns list of ids that **could not** be deleted (published + `force=False`).  
Published = any destination has `status == "published"`.

### `set_destinations_pending(article_id: str, platforms: list[str]) → None`

Sets `destinations[p]["status"] = "pending"` for each platform in the list. Updates `updated_at`.

### `apply_push_result(article_id, platform, success, url=None, error=None) → None`

```python
# On success:
dest["status"] = "draft"
dest["label"]  = "Draft"
dest["url"]    = url
dest["error"]  = None
# Prepends timeline event "Draft pushed to <Platform>"

# On failure:
dest["status"] = "error"
dest["label"]  = "Error"
dest["error"]  = error
# Prepends timeline event "<Platform> push failed — <error>"
```

Timeline is trimmed to the 5 most recent entries. `updated_at` is refreshed.

### `apply_inspect_result(article_id: str, gate: str) → None`

Sets `article["gate"] = gate`.  
Prepends timeline event `"Inspection completed (gate: <gate>)"`.  
Trims timeline to 5. Updates `updated_at`.

---

## 4. Jobs Interface

### `create_job(job_type: str, article_id: str) → dict`

```python
{
  "job_id":     "job_<8 hex chars>",
  "type":       <"push" | "inspect" | "generate">,
  "status":     "running",
  "article_id": article_id,
  "result":     None,
  "error":      None,
}
```

### `get_job(job_id: str) → dict | None`

Read-only. Used exclusively by the Jobs router.

### `complete_job(job_id: str, result: dict | None = None, error: str | None = None) → None`

```python
job["status"] = "error" if error else "done"
job["result"] = result
job["error"]  = error
```

**Result shapes by job type:**

| `type` | `result` when done |
|--------|--------------------|
| `push` | `{ "platforms": ["medium", "hashnode"] }` |
| `inspect` | `{ "gate": "pass" \| "warn" \| "fail" }` |
| `generate` | `{ "article_id": "art_..." }` |

---

## 5. Connections Interface

### `list_connections() → list[dict]`

Returns all 5 known connections (medium, hashnode, devto, anthropic, openai) whether connected or not.  
Each dict:

```python
{
  "id":           "medium",
  "label":        "Medium",
  "type":         "blog",           # "blog" | "ai"
  "auth_method":  "oauth_or_token", # "oauth_or_token" | "token"
  "status":       "connected",      # "connected" | "disconnected"
  "username":     "acisse",         # None if not connected
  "connected_at": datetime(...),    # None if not connected
  "error_message": None,
}
```

### `save_connection(conn_id, token, status="connected", username=None, error=None) → dict`

Raises `KeyError` if `conn_id` not in `_CONNECTION_META`.  
Stores `token` in `_connections[conn_id]`. Returns the full merged dict (same shape as list item).

### `delete_connection(conn_id: str) → None`

Removes the entry from `_connections` (no-op if not present).

### `get_connection_token(conn_id: str) → str | None`

Returns the raw stored token or `None`.  
Used by Articles push service and Agent service to verify presence before side-effectful operations.

---

## 6. Reset

```python
def reset() -> None:
    global _articles, _jobs, _platforms
    _articles  = {a["id"]: deepcopy(a) for a in _SEED_ARTICLES}
    _jobs      = {}
    _platforms = deepcopy(_SEED_PLATFORMS)
    # _connections is NOT reset
```

Called from:
- `POST /api/dev/reset` (dev router)
- Test fixtures (`conftest.py`)

---

## 7. Article Dict Shape

The raw dict stored in `_articles` (before schema conversion):

```python
{
  "id":        "art_001",
  "title":     "Building a Vector DB from Scratch",
  "updated_at": datetime(2026, 4, 2, 12, 0, tzinfo=UTC),
  "word_count": 1820,
  "gate":       "pass",           # "pass" | "warn" | "fail" | "pending"
  "destinations": {
    "medium":   { "status": "draft",    "label": "Draft v2",  "url": None, "error": None },
    "hashnode": { "status": "pending",  "label": "Pending",   "url": None, "error": None },
    "devto":    { "status": "draft",    "label": "Draft v1",  "url": None, "error": None },
  },
  "recent_timeline": [
    { "timestamp": datetime(...), "event": "Draft pushed to Medium" },
    ...
  ],
  # Extended fields (not in seed — added by agent service):
  # "body":       "<full markdown body>",
  # "content":    "<full markdown body>",   ← @tbd: confirm field name
}
```

> **@tbd** — The article dict in the seed data has no `body` / `content` field.  
> Agent service needs to write the generated body somewhere. The field name and  
> whether it lives in the same dict or a separate store needs to be confirmed  
> when `agent_service.py` is implemented.

---

## 8. Concurrency Note

The in-memory store has **no locking**. In the current single-worker `uvicorn` setup this is safe.  
For production (multi-worker / task queue), the store must be replaced with a database or  
distributed cache, and all write operations need transactions.
