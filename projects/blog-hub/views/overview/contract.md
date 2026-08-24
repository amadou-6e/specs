# Overview — API Contract

All requests are authenticated via session token in the `Authorization: Bearer <token>` header.
Base URL: `http://localhost:8000/api/v1` (development).

---

## GET /articles

Fetches the article list for the overview grid.

### Query params
| Param      | Type   | Required | Description                                      |
|------------|--------|----------|--------------------------------------------------|
| status     | string | no       | Filter by status: draft, ready, error, published |
| platform   | string | no       | Filter by platform: medium, hashnode, devto       |
| q          | string | no       | Full-text search on title                        |
| page       | int    | no       | Page number, default 1                           |
| per_page   | int    | no       | Results per page, default 20, max 100            |

### Response 200
```json
{
  "articles": [
    {
      "id": "uuid",
      "title": "string",
      "word_count": 1800,
      "updated_at": "2026-04-02T14:00:00Z",
      "destinations": {
        "medium":   { "status": "draft",     "label": "Draft v2", "url": "https://..." },
        "hashnode": { "status": "pending",   "label": "Pending",  "url": null },
        "devto":    { "status": "none",      "label": "—",        "url": null }
      },
      "gate": {
        "result": "pass",
        "inspected_at": "2026-04-02T13:55:00Z",
        "report_url": "/inspect/uuid"
      }
    }
  ],
  "total": 42,
  "page": 1,
  "per_page": 20
}
```

### Response 401
```json
{ "error": "unauthenticated" }
```

---

## DELETE /articles/:id

Deletes an article and all associated draft records.

### Response 204
No body.

### Response 404
```json
{ "error": "not_found" }
```

### Response 409
```json
{ "error": "has_published_destinations", "message": "Cannot delete an article with live published posts." }
```

The frontend must surface the 409 as an inline error on the card, not a toast.

---

## POST /articles/:id/push

Triggers draft creation on one or more platforms.

### Request body
```json
{
  "platforms": ["medium", "hashnode", "devto"]
}
```

### Response 202
Returns immediately. Job runs async.
```json
{
  "job_id": "uuid",
  "status": "queued",
  "poll_url": "/jobs/uuid"
}
```

The frontend polls `/jobs/:job_id` until status is `done` or `failed`, then refreshes the article card.

---

## GET /jobs/:job_id

Polls async job status.

### Response 200
```json
{
  "job_id": "uuid",
  "status": "queued | running | done | failed",
  "result": {
    "medium":   { "status": "draft", "url": "https://..." },
    "hashnode": { "status": "error", "reason": "auth_expired" }
  },
  "finished_at": "2026-04-02T14:05:00Z"
}
```

Poll interval: 2s. Stop polling after `done`, `failed`, or 60s timeout.

---

## Frontend error handling rules

| HTTP status | Behaviour                                                  |
|-------------|------------------------------------------------------------|
| 401         | Redirect to /settings with "Session expired" banner        |
| 404         | Show inline error on the relevant card                     |
| 409         | Show inline conflict message, do not dismiss automatically |
| 500         | Show toast: "Something went wrong, try again"             |
| Network     | Show toast: "Connection lost" with retry button            |
