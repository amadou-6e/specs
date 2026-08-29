# Publish / Schedule — API Contract

> Scope: this file defines service requests and payloads. UI geometry, visible states,
> interaction IDs, and transitions are governed by
> [publish-schedule.drawio](publish-schedule.drawio).

---

## GET /articles/:id/publish-state

Returns the current draft state per destination, used to populate destination rows.

### Response 200
```json
{
  "article_id": "uuid",
  "gate": "pass",
  "destinations": {
    "medium": {
      "draft_status": "ready",
      "draft_label": "Draft v2",
      "draft_url": "https://...",
      "error": null
    },
    "hashnode": {
      "draft_status": "ready",
      "draft_label": "Draft v1",
      "draft_url": "https://...",
      "error": null
    },
    "devto": {
      "draft_status": "error",
      "draft_label": "Error",
      "draft_url": null,
      "error": "code_block_split"
    }
  }
}
```

---

## POST /articles/:id/publish

Triggers publish or schedule for one or more destinations.

### Request body
```json
{
  "actions": [
    { "platform": "medium",   "mode": "now" },
    { "platform": "hashnode", "mode": "scheduled", "scheduled_at": "2026-04-04T09:00:00Z" }
  ]
}
```

`mode` values: `now`, `scheduled`.
`scheduled_at` is required when mode is `scheduled`. Must be in the future.

### Response 202
```json
{
  "job_id": "uuid",
  "poll_url": "/jobs/uuid"
}
```

Frontend polls until done, then renders the OutcomeScreen using the job result.

### Response 400
```json
{
  "error": "validation_error",
  "fields": {
    "actions[1].scheduled_at": "must_be_in_future"
  }
}
```

### Response 409
```json
{
  "error": "already_published",
  "platform": "medium",
  "published_url": "https://..."
}
```

Frontend shows inline conflict: "Already published on Medium. [View post]"

---

## GET /jobs/:job_id (publish result)

Polls async publish job. Same endpoint as used elsewhere.

### Response 200 (done)
```json
{
  "job_id": "uuid",
  "status": "done",
  "result": {
    "medium": {
      "outcome": "published",
      "url": "https://medium.com/...",
      "published_at": "2026-04-02T15:00:00Z"
    },
    "hashnode": {
      "outcome": "scheduled",
      "scheduled_at": "2026-04-04T09:00:00Z"
    }
  }
}
```

Outcome values: `published`, `scheduled`, `failed`.
Failed items include a `reason` field.

---

## Frontend error handling rules

| HTTP status | Behaviour                                                        |
|-------------|------------------------------------------------------------------|
| 400         | Highlight the invalid destination row inline                     |
| 409         | Show "Already published" inline on the row with view link        |
| 500         | Show error above action bar with retry                           |
| Network     | Show "Connection lost" banner; do not auto-retry publish         |
