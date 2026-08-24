# Dependency — Dev.to (Forem)

Used by the **Articles** service to create and update article drafts on Dev.to (dev.to).

---

## Caller

```
Articles push service  ──────────────────────────────►  Dev.to REST API
  POST /api/articles/{id}/push                          https://dev.to/api
```

---

## 1. Endpoint

| Property | Value |
|----------|-------|
| Base URL | `https://dev.to/api` (overridable via `DEVTO_BASE_URL`) |
| Protocol | REST / JSON over HTTPS |
| Auth | `api-key: <key>` request header |
| Timeout | 30 s |
| Client | `requests.Session` (from `article_publishing/publishing/devto.py`) |

---

## 2. Request Headers

```http
api-key: <DEVTO_API_KEY>
Content-Type: application/json
Accept: application/json
```

---

## 3. Create Article

```
POST https://dev.to/api/articles
```

### Request body

```json
{
  "article": {
    "title":        "Building a Vector DB from Scratch",
    "body_markdown": "# Building a Vector DB...\n\nContent here...",
    "published":    false,
    "series":       null,
    "main_image":   "https://cdn.example.com/cover.png",
    "canonical_url": "https://medium.com/@acisse/...",
    "description":  "A short description under 160 chars.",
    "tags":         ["docker", "postgres", "database"]
  }
}
```

**Field notes:**

| Field | Required | Notes |
|-------|----------|-------|
| `title` | yes | Article headline |
| `body_markdown` | yes | Full article body in Markdown; Dev.to renders it |
| `published` | yes | `false` = draft (always false for initial push) |
| `tags` | optional | Array of strings, max 4. Dev.to tag slugs (lowercase, no spaces) |
| `main_image` | optional | Cover image URL shown at top of article |
| `canonical_url` | optional | Set when cross-posting to signal original source |
| `description` | optional | Meta description shown in feeds; max ~150 chars |
| `series` | optional | Groups articles into a series |

---

## 4. Update Article

```
PUT https://dev.to/api/articles/{article_id}
```

Same body structure as create. Uses `article_id` returned from the initial `POST`.

---

## 5. Success Response

```json
{
  "id":       123456,
  "url":      "https://dev.to/acisse/building-a-vector-db-from-scratch-1abc",
  "path":     "/acisse/building-a-vector-db-from-scratch-1abc",
  "title":    "Building a Vector DB from Scratch",
  "published": false,
  ...
}
```

**Extracted and persisted:**

| Response field | Stored as |
|----------------|-----------|
| `id` | `destination.draft_id` (as string) — used for update calls |
| `url` or `path` | `destination.url` |

> **Extraction logic**: `data.get("url") or data.get("path") or ""`

---

## 6. Error Handling

| Condition | HTTP status | Behaviour |
|-----------|-------------|-----------|
| Invalid API key | 401 | `raise DevToError("DEV API error 401: ...")` |
| Validation error (e.g. too many tags) | 422 | `raise DevToError("DEV API error 422: ...")` |
| Rate limited | 429 | `raise DevToError(...)` — **@tbd**: retry not yet implemented |
| Non-JSON response | any | `raise DevToError("DEV API returned non-JSON response: <status>")` |
| Network timeout | — | `requests.Timeout` propagates to job error handler |

**Error body format** (when JSON):
```json
{ "error": "human-readable message", "status": 422 }
```
or:
```json
{ "message": "..." }
```

Extraction: `data.get("error") or data.get("message") or data`

All errors map to: job `status=error`, destination `status=error`, `error_message=<str>`.

---

## 7. Content Preprocessing (from `article_publishing`)

| Step | What it does |
|------|-------------|
| No H1 stripping | Dev.to uses `title` field + renders the body `# H1`; no stripping needed |
| Tags normalised | Lowercase, spaces to hyphens before sending (done by caller, not the client) |
| Images | Local image refs must be absolute URLs — Dev.to fetches them at render time |

---

## 8. Environment / Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `DEVTO_API_KEY` | yes | Stored as `_connections["devto"]["token"]` after user saves via `PUT /api/connections/devto` |
| `DEVTO_BASE_URL` | no | Default: `https://dev.to/api` — override for local testing / staging |

---

## 9. Stored Credential Shape

```python
# _connections["devto"]
{
  "token":         "<Dev.to API Key>",
  "status":        "connected",
  "username":      None,            # no /me call at token save time
  "connected_at":  datetime(...),
  "error_message": None,
}
```

> **Note**: No server-side token verification at connection time — failures surface at push time.

---

## 10. Known Failure Modes (from `article_publishing` experience)

| Failure | Root cause | Workaround |
|---------|-----------|------------|
| "code block split" | Dev.to parser chokes on certain fenced code block sequences | Ensure single blank line before/after every code fence |
| Tags rejected | Sent as non-slug strings (spaces, uppercase) | Normalize tags before send |
| Image not rendered | Local path reference not rewritten to absolute URL | Always resolve image URLs before push |
