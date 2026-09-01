# Overview — API Contract

> Scope: this file defines service requests and payloads. UI geometry, visible states,
> interaction IDs, and transitions are governed by [overview.drawio](overview.drawio).

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

`gate.result` is `pass`, `warn`, `fail`, or `pending`. `report_url` is null for
Pending and whenever a completed inspection report is unavailable.

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

## POST /articles/:id/duplicate

Creates one independent draft copy. The request requires an `Idempotency-Key` header;
repeating the same key returns the same copy and does not create another article.

### Response 201
```json
{ "article": { "id": "new-uuid", "title": "Copy of original title" } }
```

### Response 404
```json
{ "error": "not_found" }
```

---

## POST /articles/:id/archive

Removes an article from the active collection while retaining revisions, remote
identities, job history, and audit history.

### Response 200
```json
{ "id": "uuid", "archived": true }
```

### Response 404
```json
{ "error": "not_found" }
```

---

## POST /articles/:id/push

Triggers draft creation on one or more platforms.

Requires an `Idempotency-Key` header stable for the article and visible operation until
the request settles. A repeated key returns the existing job.

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

The frontend polls `/jobs/:job_id` through the durable lifecycle described below, then
refreshes the card and selected detail after a terminal result.

The same durable submission and response envelope applies to
`POST /articles/:id/inspect`.

---

## GET /jobs?article_id=:id&active=true

Discovers durable work after Overview reload. Returns queued, running, or retrying jobs
for the article, newest first. Terminal jobs may be requested with `active=false`.

### Response 200
```json
{
  "jobs": [
    {
      "job_id": "uuid",
      "article_id": "uuid",
      "operation": "push | inspect",
      "status": "queued | running | retrying",
      "retryable": false
    }
  ]
}
```

---

## GET /jobs/:job_id

Polls async job status.

### Response 200
```json
{
  "job_id": "uuid",
  "status": "queued | running | retrying | done | failed | canceled",
  "operation": "push | inspect",
  "retryable": true,
  "result": {
    "medium":   { "status": "draft", "url": "https://..." },
    "hashnode": { "status": "error", "reason": "auth_expired" }
  },
  "finished_at": "2026-04-02T14:05:00Z"
}
```

Poll interval: 2s. Stop polling only after `done`, `failed`, or `canceled`, or when the
backend returns its durable terminal timeout. The browser does not infer failure from a
short local timeout.

---

## POST /jobs/:job_id/retry

Retries a retryable failed or canceled job. Requires an `Idempotency-Key`; repeating the
same retry returns the same queued/running job.

### Response 202
```json
{ "job_id": "uuid", "status": "queued", "poll_url": "/jobs/uuid" }
```

### Response 409
```json
{ "error": "not_retryable", "message": "This job cannot be retried." }
```

---

## Frontend error handling rules

| HTTP status | Behaviour                                                  |
|-------------|------------------------------------------------------------|
| 401         | Redirect to /settings with "Session expired" banner        |
| 404         | Show inline error on the relevant card or selected panel   |
| 409         | Show inline conflict message, do not dismiss automatically |
| 500         | Keep article mutations inline; use a toast for collection-level failures |
| Network     | Keep active mutation/job context inline; use a toast for collection loss |
