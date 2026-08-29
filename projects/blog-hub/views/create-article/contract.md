# Create Article — API Contract

> Scope: this file defines service requests and payloads. UI geometry, visible states,
> interaction IDs, and transitions are governed by [create-article.drawio](create-article.drawio).

---

## GET /platforms

Returns all configured platforms and their session health. Used to populate the DestinationChecklist.

### Response 200
```json
{
  "platforms": [
    {
      "id": "medium",
      "label": "Medium",
      "status": "connected",
      "session_expires_at": "2026-04-05T00:00:00Z"
    },
    {
      "id": "hashnode",
      "label": "Hashnode",
      "status": "expired",
      "session_expires_at": "2026-03-30T00:00:00Z"
    },
    {
      "id": "devto",
      "label": "Dev.to",
      "status": "not_configured",
      "session_expires_at": null
    }
  ]
}
```

Platform status values: `connected`, `expired`, `not_configured`.

---

## GET /providers

Returns configured AI providers. Used to render the ProviderToggle with correct warning states.

### Response 200
```json
{
  "providers": [
    { "id": "claude", "label": "Claude", "configured": true },
    { "id": "codex",  "label": "Codex",  "configured": false }
  ]
}
```

---

## POST /articles/generate

Creates an article and starts the AI generation job.

### Request body
```json
{
  "title": "string | null",
  "prompt": "string (required, min 10 chars)",
  "skill": "technical | tutorial | comparison | opinion | tip",
  "provider": "claude | codex",
  "tone": "technical | conversational | tutorial",
  "target_word_count": 1500,
  "destinations": ["medium", "hashnode"]
}
```

### Response 202
```json
{
  "article_id": "uuid",
  "job_id": "uuid",
  "poll_url": "/jobs/uuid"
}
```

Frontend navigates to `/article/:article_id` immediately and polls `/jobs/:job_id` to show generation progress in the editor.

### Response 400
```json
{
  "error": "validation_error",
  "fields": {
    "prompt": "required",
    "destinations": "at_least_one_required"
  }
}
```

### Response 422
```json
{
  "error": "provider_not_configured",
  "provider": "codex"
}
```

---

## GET /skills

Returns available writing skills with metadata. Used to populate the SkillCard grid.

### Response 200
```json
{
  "skills": [
    {
      "id": "technical",
      "name": "Technical deep-dive",
      "description": "In-depth exploration of a technical concept with code examples.",
      "available": true
    },
    {
      "id": "comparison",
      "name": "Comparison / benchmark",
      "description": "Side-by-side evaluation of tools, approaches, or results.",
      "available": true
    }
  ]
}
```

`available: false` means the skill is visible but locked (future plan feature).

---

## Frontend error handling rules

| HTTP status | Behaviour                                                       |
|-------------|-----------------------------------------------------------------|
| 400         | Highlight invalid fields inline, do not navigate away           |
| 422         | Show provider error banner with link to /settings               |
| 500         | Show error banner above action bar with retry                   |
| Network     | Show error banner with "Check your connection" and retry        |
