# BlogHub Data Model

Source: extracted from `.planning/core_feature_functioning_and_ui_samples.md` Section 6 and 4.6.

---

## Article

| Field            | Type     | Notes                                      |
|------------------|----------|--------------------------------------------|
| article_id       | uuid     | Primary key                                |
| workspace_id     | uuid     | Owner workspace                            |
| title            | string   | Editable inline in editor                  |
| canonical_content| text     | Markdown source of truth                   |
| version          | int      | Increments on each accepted patch or save  |
| status_global    | enum     | Derived from destination states (see below)|
| word_count       | int      | Computed from canonical_content            |
| created_at       | datetime |                                            |
| updated_at       | datetime |                                            |

---

## Comment

| Field      | Type   | Notes                                            |
|------------|--------|--------------------------------------------------|
| comment_id | uuid   |                                                  |
| article_id | uuid   |                                                  |
| anchor     | object | `{ start: int, end: int }` — char offsets        |
| text       | string |                                                  |
| author     | string |                                                  |
| state      | enum   | `open`, `resolved`                               |
| patch_id   | uuid?  | Set when an AI patch has been generated for this |
| created_at | datetime |                                                |

---

## AgentPatch

| Field              | Type     | Notes                                    |
|--------------------|----------|------------------------------------------|
| patch_id           | uuid     |                                          |
| article_id         | uuid     |                                          |
| source_comment_ids | uuid[]   | Comments that prompted this patch        |
| diff               | object   | `{ original: string, replacement: string, anchor: object }` |
| status             | enum     | `pending`, `accepted`, `rejected`        |
| accepted_by        | string?  |                                          |
| accepted_at        | datetime?|                                          |

Rules:
- Patches are always diff-based. Never a silent full overwrite.
- Every patch is logged. Users can revert to any prior version.

---

## DestinationDraft

| Field               | Type     | Notes                                        |
|---------------------|----------|----------------------------------------------|
| destination_draft_id| uuid     |                                              |
| article_id          | uuid     |                                              |
| platform            | enum     | `medium`, `hashnode`, `devto`                |
| status              | enum     | See state machine below                      |
| remote_draft_url    | string?  | URL to the draft on the platform             |
| remote_revision     | string?  | Platform's internal revision ID if available |
| last_sync_at        | datetime?|                                              |
| error_payload       | object?  | Structured error from the last failed action |

---

## Destination State Machine

Each DestinationDraft moves through these states:

```
not_connected
    ↓ (platform session established)
connected
    ↓ (push draft triggered)
draft_pending
    ↓ (push completed)
draft_created
    ↓ (inspection run, issues found)
review_required
    ↓ (issues resolved or accepted)
ready_to_publish
    ↓ (schedule set)
scheduled
    ↓ (publish time reached and executed)
published

At any point: → sync_error (recoverable via retry)
```

State descriptions:

| State              | Meaning                                                   |
|--------------------|-----------------------------------------------------------|
| not_connected      | Platform not linked, no session                           |
| connected          | Platform linked, no draft pushed yet                      |
| draft_pending      | Push job queued or running                                |
| draft_created      | Draft exists on platform, not yet inspected               |
| review_required    | Inspection ran and found warn/fail issues                 |
| ready_to_publish   | Inspection passed, ready for scheduling or immediate pub  |
| scheduled          | Publish time set, waiting for execution                   |
| published          | Live on the platform                                      |
| sync_error         | Last operation failed; error_payload has the reason       |

---

## InspectionReport

| Field         | Type     | Notes                               |
|---------------|----------|-------------------------------------|
| report_id     | uuid     |                                     |
| article_id    | uuid     |                                     |
| platform      | enum     |                                     |
| overall       | enum     | `pass`, `warn`, `fail`              |
| checks        | object[] | See check shape below               |
| inspected_at  | datetime |                                     |

### Check shape

```json
{
  "id": "code_blocks | images | sections | tail",
  "label": "string",
  "result": "pass | warn | fail",
  "detail": "string",
  "artifact_url": "string"
}
```

---

## Platform

| Field              | Type     | Notes                                            |
|--------------------|----------|--------------------------------------------------|
| platform_id        | enum     | `medium`, `hashnode`, `devto`                    |
| label              | string   |                                                  |
| status             | enum     | `connected`, `expired`, `not_configured`         |
| session_token      | string?  | Encrypted at rest                                |
| api_key            | string?  | Encrypted at rest                                |
| connected_at       | datetime?|                                                  |
| expires_at         | datetime?| Null for API-key platforms                       |

---

## Provider

| Field        | Type   | Notes                              |
|--------------|--------|------------------------------------|
| provider_id  | enum   | `claude`, `codex`                  |
| label        | string |                                    |
| configured   | bool   |                                    |
| api_key      | string?| Encrypted at rest, never returned  |
| masked_key   | string?| e.g. `sk-ant-...abc`               |
