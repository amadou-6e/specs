# Import Article — API Contract

All requests use `Authorization: Bearer <token>`.
Base URL: `http://localhost:8000/api/v1` (development).

---

## GET /connections

Fetches the list of all platforms and their connection status. Used to populate the PlatformPickerGrid.

Already defined in the Settings contract. Referenced here, not duplicated.

### Response 200 (relevant fields)
```json
{
  "platforms": [
    {
      "id": "medium",
      "name": "Medium",
      "connected": true,
      "expires_at": null
    },
    {
      "id": "hashnode",
      "name": "Hashnode",
      "connected": false,
      "expires_at": null
    }
  ]
}
```

Only `connected: true` platforms are selectable in the platform picker. Others are shown as disabled.

---

## GET /connections/:platform/drafts

Fetches a paginated list of drafts for a connected platform.

### Path params
| Param | Type | Description |
|-------|------|-------------|
| platform | string | `medium`, `hashnode`, or `devto` |

### Query params
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| page | int | no | Page number, default 1 |
| per_page | int | no | Results per page, default 20 |

### Response 200
```json
{
  "platform": "medium",
  "drafts": [
    {
      "id": "draft-abc123",
      "title": "How I built a distributed cache",
      "word_count": 1840,
      "updated_at": "2026-03-28T10:00:00Z"
    }
  ],
  "total": 47,
  "page": 1,
  "per_page": 20,
  "has_more": true
}
```

### Response 401
```json
{ "error": "unauthenticated" }
```

### Response 404
```json
{ "error": "platform_not_connected", "platform": "medium" }
```

The frontend must treat 404 as a disconnected-platform error and return to the platform picker step.

---

## GET /connections/:platform/drafts/:draft_id

Fetches the full content of a single draft. Called when the user advances to the Review step in platform mode.

### Response 200
```json
{
  "id": "draft-abc123",
  "title": "How I built a distributed cache",
  "word_count": 1840,
  "updated_at": "2026-03-28T10:00:00Z",
  "body": "# How I built a distributed cache\n\nThis is the full markdown body..."
}
```

### Response 404
```json
{ "error": "draft_not_found" }
```

---

## POST /articles/import

Creates a new article workspace from imported content and returns the article ID for navigation to the editor. On success, the frontend navigates to `/screens/editor/v2.html?id=<id>&title=<encoded-title>`.

### Request body — platform source
```json
{
  "source": "platform",
  "platform": "medium",
  "draft_id": "draft-abc123",
  "title": "How I built a distributed cache"
}
```

`title` is the (possibly user-edited) title from the Review step. The backend stores this as the article title, not the original draft title.

### Request body — upload source
```json
{
  "source": "upload",
  "filename": "my-article.md",
  "title": "How I built a distributed cache",
  "content": "# How I built a distributed cache\n\nFull markdown content..."
}
```

### Response 201
```json
{
  "id": "uuid",
  "title": "How I built a distributed cache"
}
```

The backend must:
1. Create the article record in the store (title, body from content, word count).
2. Set `source: "platform"` or `source: "uploaded"` in the article metadata.
3. Add a timeline event: "Imported from &lt;platform&gt;" or "Uploaded from &lt;filename&gt;".
4. Return 201 before any AI processing begins.

### Response 409
```json
{ "error": "duplicate_draft", "existing_article_id": "uuid" }
```

Returned when the same `platform` + `draft_id` pair already exists as an article. The frontend shows an inline warning: "This draft was already imported. Open it instead?" with a link to the existing article in the editor.

### Response 422
```json
{ "error": "parse_failed", "reason": "string" }
```

Returned for upload source when the content cannot be parsed as valid Markdown.

### Response 500
```json
{ "error": "internal_error" }
```

---

## Frontend error handling rules

| HTTP status | Behaviour |
|-------------|-----------|
| 401 | Redirect to Settings with "Session expired" banner |
| 404 (draft fetch) | Return to draft list step with inline "Draft not found" error |
| 404 (platform) | Return to platform picker with inline "Platform disconnected" error |
| 409 | Show warning banner on Review step with link to existing article |
| 422 | Show inline error on Review step: "File could not be parsed as Markdown" |
| 500 | Show error banner in footer with "Try again" action |
| Network | Show toast: "Connection lost" with retry button |
