# Inspection — API Contract

> Scope: this file describes service requests and payloads only. No Inspection UI
> behavior is authoritative until `inspection.drawio` exists and is reviewed.

---

## GET /articles/:id/inspection

Returns the latest inspection report for all destinations.

### Response 200
```json
{
  "article_id": "uuid",
  "inspected_at": "2026-04-02T14:00:00Z",
  "overall": "warn",
  "platforms": {
    "medium": {
      "result": "pass",
      "checks": [
        {
          "id": "code_blocks",
          "label": "Code blocks preserved",
          "result": "pass",
          "detail": "4 / 4 blocks intact",
          "artifact_url": "/artifacts/uuid/medium/code_blocks"
        },
        {
          "id": "tail",
          "label": "Article tail present",
          "result": "pass",
          "detail": "Content complete",
          "artifact_url": "/artifacts/uuid/medium/tail"
        }
      ]
    },
    "hashnode": {
      "result": "warn",
      "checks": [
        {
          "id": "images",
          "label": "Image count",
          "result": "warn",
          "detail": "3 / 4 images — 1 missing",
          "artifact_url": "/artifacts/uuid/hashnode/images"
        }
      ]
    }
  }
}
```

### Response 404
No inspection has been run yet.
```json
{ "error": "no_inspection_found" }
```

Frontend redirects to editor with a "Run inspection first" prompt.

---

## POST /articles/:id/inspection

Triggers a fresh inspection run.

### Response 202
```json
{
  "job_id": "uuid",
  "poll_url": "/jobs/uuid"
}
```

Frontend polls until job is done, then re-fetches GET /articles/:id/inspection.

---

## GET /artifacts/:inspection_id/:platform/:check_id

Returns raw artifact data for a specific check.

### Response 200 (code_blocks)
```json
{
  "type": "code_blocks",
  "expected_count": 4,
  "found_count": 4,
  "blocks": [
    { "index": 1, "language": "python", "content": "...", "status": "ok" },
    { "index": 2, "language": "bash",   "content": "...", "status": "ok" }
  ]
}
```

### Response 200 (images)
```json
{
  "type": "images",
  "expected": ["https://...", "https://..."],
  "found":    ["https://..."],
  "missing":  ["https://..."]
}
```

### Response 200 (sections)
```json
{
  "type": "sections",
  "expected": ["Introduction", "Setup", "Results", "Conclusion"],
  "found":    ["Introduction", "Setup", "Results"],
  "missing":  ["Conclusion"]
}
```

### Response 200 (tail)
```json
{
  "type": "tail",
  "result": "fail",
  "last_500_chars": "string",
  "truncation_offset": 412
}
```

---

## Frontend error handling rules

| HTTP status | Behaviour                                                    |
|-------------|--------------------------------------------------------------|
| 404 (report)| Redirect to editor with "No inspection yet" toast            |
| 404 (artifact)| Show "Artifact not available" in the panel              |
| 500         | Show error in the relevant panel section with retry link     |
