# Editor — API Contract

> Scope: this file defines service requests and payloads. UI geometry, visible states,
> interaction IDs, and transitions are governed by [editor.drawio](editor.drawio).

---

## GET /articles/:id

Fetches article content and metadata for the editor.

### Response 200
```json
{
  "id": "uuid",
  "title": "string",
  "content": "string (markdown)",
  "word_count": 1800,
  "updated_at": "2026-04-02T14:00:00Z",
  "destinations": {
    "medium":   { "status": "draft", "url": "https://..." },
    "hashnode": { "status": "none",  "url": null },
    "devto":    { "status": "none",  "url": null }
  },
  "gate": { "result": "pass", "inspected_at": "..." }
}
```

---

## PATCH /articles/:id

Saves article title and/or content. Called on autosave (debounced 2s).

### Request body
```json
{
  "title": "string | null",
  "content": "string | null"
}
```

### Response 200
```json
{
  "updated_at": "2026-04-02T14:05:00Z",
  "word_count": 1850
}
```

### Response 409
Conflict: article was modified by another session.
```json
{ "error": "conflict", "server_updated_at": "2026-04-02T14:04:55Z" }
```

Frontend must show a conflict banner with "Keep mine" and "Discard and reload" options.

---

## GET /articles/:id/comments

Returns all comments for the article.

### Response 200
```json
{
  "comments": [
    {
      "id": "uuid",
      "author": "string",
      "text": "string",
      "resolved": false,
      "anchor": { "start": 120, "end": 245 },
      "replies": [],
      "patch_id": null
    }
  ]
}
```

---

## POST /articles/:id/comments

Creates a new comment.

### Request body
```json
{
  "text": "string",
  "anchor": { "start": 120, "end": 245 }
}
```

### Response 201
```json
{ "id": "uuid", "created_at": "..." }
```

---

## PATCH /articles/:id/comments/:comment_id

Resolves a comment.

### Request body
```json
{ "resolved": true }
```

### Response 200
```json
{ "resolved": true, "resolved_at": "..." }
```

---

## POST /articles/:id/comments/:comment_id/fix

Requests an AI-generated patch for a comment.

### Request body
```json
{
  "instruction": "string (the comment text)",
  "context": "string (the anchored article content)"
}
```

### Response 202
```json
{
  "patch_id": "uuid",
  "poll_url": "/patches/uuid"
}
```

---

## GET /patches/:patch_id

Polls for patch generation status.

### Response 200
```json
{
  "id": "uuid",
  "status": "pending | ready | failed",
  "diff": {
    "original": "string",
    "replacement": "string",
    "anchor": { "start": 120, "end": 245 }
  }
}
```

---

## POST /patches/:patch_id/accept

Accepts a patch and saves the updated content in one operation.

### Response 200
```json
{ "content": "string (full updated markdown)", "updated_at": "..." }
```

---

## DELETE /patches/:patch_id

Rejects and discards a patch.

### Response 204
No body.

---

## Frontend error handling rules

| HTTP status | Behaviour                                                        |
|-------------|------------------------------------------------------------------|
| 409         | Show conflict banner with Keep/Discard options                   |
| 404         | Redirect to / with "Article not found" toast                     |
| 500         | Show save failure indicator, retry silently up to 3 times        |
| Network     | Show "Offline" banner; queue saves and flush when reconnected    |
