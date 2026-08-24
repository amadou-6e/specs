# Dependency — Medium

Used by two distinct services for two distinct purposes:

| Service | Purpose |
|---------|---------|
| **Connections** | OAuth 2.0 popup login — exchange auth code for access token, fetch username |
| **Articles** | Publish/push article body as a draft (via URL import strategy) |

---

## Callers

```
Connections router  ──────────────────────────────────►  Medium OAuth API
  GET  /api/connections/medium/oauth-start              https://medium.com/m/oauth/authorize
  GET  /api/connections/medium/oauth-callback           https://api.medium.com/v1/tokens
                                                        https://api.medium.com/v1/me

Articles push service  ─────────────────────────────►  Medium URL import
  POST /api/articles/{id}/push                          (render HTML → host → import URL)
```

---

## 1. OAuth 2.0 — Token Exchange

### Auth code → Access token

```
POST https://api.medium.com/v1/tokens
Content-Type: application/json

{
  "code":          "<auth_code from redirect>",
  "client_id":     "$MEDIUM_CLIENT_ID",
  "client_secret": "$MEDIUM_CLIENT_SECRET",
  "grant_type":    "authorization_code",
  "redirect_uri":  "$MEDIUM_REDIRECT_URI"
}
```

**Success response:**
```json
{
  "data": {
    "accessToken":  "<bearer token>",
    "tokenType":    "Bearer",
    "scope":        "basicProfile publicationsList",
    "expiresAt":    0
  }
}
```

> **Token extraction**: `token_data.get("access_token") or token_data.get("data", {}).get("accessToken")`  
> (Medium returns either top-level or nested depending on API version.)

**Error cases:**

| Condition | Behaviour |
|-----------|-----------|
| `code` missing or `error` in redirect params | Return popup HTML with `status=error` immediately — no HTTP call made |
| `MEDIUM_CLIENT_ID` not set | `GET /oauth-start` returns `{ available: false }` — OAuth disabled |
| Token exchange returns no `accessToken` | Return popup HTML with `status=error, error="No token in OAuth response"` |
| Network / timeout | Caught by outer `except Exception` → popup HTML with error text |

---

## 2. Profile Fetch — `/v1/me`

```
GET https://api.medium.com/v1/me
Authorization: Bearer <accessToken>
```

**Success response:**
```json
{
  "data": {
    "id":         "<medium user id>",
    "username":   "acisse",
    "name":       "A. Cisse",
    "url":        "https://medium.com/@acisse",
    "imageUrl":   "https://..."
  }
}
```

**Extracted fields**: `data.username` or `data.name` (whichever is present).  
Stored on the connection record as `username`.

---

## 3. OAuth Authorization Redirect

This is a browser-side redirect — backend only constructs the URL.

```
GET https://medium.com/m/oauth/authorize
  ?client_id=<MEDIUM_CLIENT_ID>
  &scope=basicProfile%20publicationsList
  &state=bloghub
  &response_type=code
  &redirect_uri=<MEDIUM_REDIRECT_URI>
```

**Default `MEDIUM_REDIRECT_URI`**: `http://localhost:8000/api/connections/medium/oauth-callback`

**postMessage payload** (sent from popup → opener on completion):
```json
{
  "type":     "oauth-complete",
  "platform": "medium",
  "status":   "connected",
  "username": "acisse"
}
```
Error variant adds `"error": "<message>"` and omits `username`.

---

## 4. Article Publishing (push)

### Approach: URL Import (confirmed from `article_publishing`)

Medium's direct-publish API (`POST /v1/users/{uid}/posts`) is restricted and unreliable.  
The confirmed approach from `article_publishing/publishing/` is **URL import**:

| Step | What happens |
|------|-------------|
| 1 | `render_medium_markdown()` converts article body to Medium-ready Markdown |
| 2 | `render_medium_import_html()` wraps it in a minimal public HTML page |
| 3 | HTML is hosted at a public URL (CDN / GitHub Pages / file server) |
| 4 | Medium imports the story via **Import a story** → URL |

> **@tbd**: How does the blog-hub backend host/serve the HTML artifact?  
> Options under consideration: (a) serve from `/api/articles/{id}/import-page`, (b) push to a known public URL, (c) manual step.

### Markdown rendering rules (from `medium_render.py`)

| Rule | Detail |
|------|--------|
| Strip planning tail | Lines starting with `PLANNING_MARKERS` and below are removed |
| Rewrite local images | `./path` or `../path` image refs rewritten to `$image_base_url/path` |
| Move leading image | If article opens with a bare image (no H1 first), it is moved below the title |
| Normalise spacing | Trim extra blank lines |

### HTML rendering rules (from `medium_import_html.py`)

| Rule | Detail |
|------|--------|
| `<p><img></p>` → `<img>` | Medium handles block images without wrapping `<p>` |
| `<pre><code>` → `<pre>` | Medium import chokes on nested code blocks |
| Title from first `# H1` | `<title>` + `<meta name="description">` populated |
| Description | First non-heading, non-image paragraph, truncated to 160 chars |

---

## 5. Environment Variables

| Variable | Required | Used by | Notes |
|----------|----------|---------|-------|
| `MEDIUM_CLIENT_ID` | OAuth only | `connections` router | Absence disables OAuth; falls back to API token form |
| `MEDIUM_CLIENT_SECRET` | OAuth only | `connections` router | Never forwarded to browser |
| `MEDIUM_REDIRECT_URI` | OAuth only | `connections` router | Default: `http://localhost:8000/api/connections/medium/oauth-callback` |

---

## 6. Stored Credential Shape

Stored in `_connections["medium"]` by `store.save_connection()`:

```python
{
  "token":        "<Medium access token>",
  "status":       "connected",
  "username":     "acisse",          # from /v1/me
  "connected_at": datetime(...),
  "error_message": None,
}
```

Survives `POST /api/dev/reset` — connections are not article state.

---

## 7. Error Mapping (publishing push)

> **@tbd** — not yet implemented in blog-hub backend. Reference from `article_publishing`:

| Condition | Action |
|-----------|--------|
| Import URL not yet hosted | Push job fails with `error: "Import URL not yet available"` |
| Medium import reports parse error | Job status = `error`; destination status = `error` + error text |
| Network timeout | Retry once; then fail with `error: "timeout"` |
