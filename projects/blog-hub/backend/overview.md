# Backend Spec — Overview screen

> Scope: everything the Overview screen needs to be **fully functional as a standalone view**.
> Explicitly excluded: functionalities that only make sense after navigating to another screen
> (editor save, article-detail stats, publish-queue scheduling).

---

## 1. Article list

### `GET /api/articles`

Returns the paginated list of article summaries that populate the table.

**Query parameters**

| Param      | Type                                               | Default  | Notes                                          |
|------------|----------------------------------------------------|----------|------------------------------------------------|
| `q`        | string                                             | —        | Full-text match on title. Substring is fine.   |
| `gate`     | `pass \| warn \| fail \| pending`                  | —        | Filter rows by gate result                     |
| `status`   | `none \| draft \| review \| ready \| pending \| error \| published` | — | Match any platform with this status |
| `platform` | `medium \| hashnode \| devto`                      | —        | Combined with `status` to narrow per-platform  |
| `page`     | integer ≥ 1                                        | 1        |                                                |
| `pageSize` | integer 1–100                                      | 20       |                                                |
| `sortBy`   | `updatedAt \| createdAt \| title`                  | `updatedAt` |                                             |
| `sortDir`  | `asc \| desc`                                      | `desc`   |                                                |

**Response shape** — see `contracts/overview.ts → ArticleListResponse`

Each item carries:
- `id`, `title`, `updatedAt`, `wordCount`
- `gate: GateStatus`
- `destinations: Record<Platform, PlatformSummary>` — status + label + url + error for each of the 3 platforms
- `recentTimeline: TimelineEvent[]` — last 5 events, newest first

**Behaviour rules**
- `updatedAt` reflects the latest of: content edit, destination push, gate check.
- An article with no destination configured still appears; all three `PlatformSummary.status` values are `'none'`.
- Timeline events must be stored server-side (not derived). The overview only shows the tail; full history is for article-detail.

---

## 2. Article creation

### `POST /api/articles`

Triggered by the "+ New article" button. Creates a blank article and returns the new id so the UI can navigate to the editor.

**Request body**

```json
{ "title": "Untitled" }
```

- `title` is pre-filled to `"Untitled"` client-side; the user can rename in the editor.
- No content, no destinations — those are editor concerns.

**Response** — `201 Created`

```json
{
  "id": "art_xxxxxxxx",
  "title": "Untitled",
  "createdAt": "2026-04-02T10:00:00Z"
}
```

**Side effects**
- A `TimelineEvent` `"Article created"` is appended by the server.
- The new article immediately appears in subsequent `GET /api/articles` calls with `gate: 'pending'` and all destinations `'none'`.

---

## 3. Article deletion (bulk)

### `DELETE /api/articles`

Triggered by the bulk-select checkbox + delete action. The UI sends a list of ids.

**Request body**

```json
{ "ids": ["art_abc", "art_def"] }
```

**Response** — `204 No Content`

**Constraints**
- Published articles: the server should reject deletion (return `409`) unless the client explicitly passes `"force": true`. The UI must surface the error and ask for confirmation — this is an overview-level action, not editor-specific.
- Partial success is not supported; the entire batch succeeds or fails atomically.

---

## 4. Gate / inspection — trigger

### `POST /api/articles/:id/inspect`

Triggered by the "Inspect" button in the side panel. Runs the automated gate check against the stored article content and updates `gate` + destination statuses.

**Request body** — empty `{}`

**Response** — `202 Accepted`

```json
{
  "jobId": "job_xxxxxxxx",
  "status": "running"
}
```

**Why async?**
Inspection may call external validators (readability score, word count, code-block checks). The response is immediate; the result lands via polling (see §5).

**Side effects**
- `gate` is set to `'pending'` immediately on the server.
- A `TimelineEvent` `"Inspection started"` is appended.
- On completion the server sets `gate` to `pass | warn | fail` and appends `"Inspection passed (gate: …)"` or `"Inspection failed: …"`.

---

## 5. Polling — job status

### `GET /api/jobs/:jobId`

The overview uses this to update the gate badge and destination pills after triggering an inspect or push.

**Response**

```json
{
  "jobId": "job_xxxxxxxx",
  "type": "inspect | push",
  "status": "running | done | error",
  "articleId": "art_xxxxxxxx",
  "result": { ... } | null,
  "error": "string | null"
}
```

- When `status === 'done'`, the UI re-fetches `GET /api/articles?page=…` to refresh the row.
- Poll interval: 2 s. Stop polling after `done | error` or after 60 s (timeout).
- The overview does **not** need to display job detail; it only uses `status` and `error`.

![diagram-1](https://mermaid.ink/img/c2VxdWVuY2VEaWFncmFtCiAgICBwYXJ0aWNpcGFudCBVIGFzIFVzZXIKICAgIHBhcnRpY2lwYW50IFVJIGFzIE92ZXJ2aWV3IFVJCiAgICBwYXJ0aWNpcGFudCBCIGFzIEJhY2tlbmQKCiAgICBVLT4-VUk6IGNsaWNrICJJbnNwZWN0IgogICAgVUktPj5COiBQT1NUIC9hcGkvYXJ0aWNsZXMve2lkfS9pbnNwZWN0CiAgICBCLT4-QjogZ2F0ZSA9ICdwZW5kaW5nJzsgYXBwZW5kIFRpbWVsaW5lRXZlbnQKICAgIEItLT4-VUk6IDIwMiB7IGpvYklkLCBzdGF0dXM6ICJydW5uaW5nIiB9CgogICAgbG9vcCBldmVyeSAyIHMgKG1heCA2MCBzKQogICAgICAgIFVJLT4-QjogR0VUIC9hcGkvam9icy97am9iSWR9CiAgICAgICAgQi0tPj5VSTogeyBzdGF0dXM6ICJydW5uaW5nIiB9CiAgICBlbmQKCiAgICBOb3RlIG92ZXIgQjogaW5zcGVjdGlvbiBjb21wbGV0ZXMKICAgIEItPj5COiBnYXRlID0gcGFzcyB8IHdhcm4gfCBmYWlsOyBhcHBlbmQgVGltZWxpbmVFdmVudAogICAgVUktPj5COiBHRVQgL2FwaS9qb2JzL3tqb2JJZH0KICAgIEItLT4-VUk6IHsgc3RhdHVzOiAiZG9uZSIsIHJlc3VsdCB9CiAgICBVSS0-PkI6IEdFVCAvYXBpL2FydGljbGVzP3BhZ2U94oCmCiAgICBCLS0-PlVJOiB1cGRhdGVkIGFydGljbGUgbGlzdCB3aXRoIG5ldyBnYXRlIGJhZGdl)

---

## 6. Destination draft push

### `POST /api/articles/:id/push`

Triggered by the "Push drafts" button in the side panel. Sends the current article content to all configured platforms as drafts.

**Request body**

```json
{ "platforms": ["medium", "hashnode", "devto"] }
```

- If `platforms` is omitted, the server pushes to all configured destinations.
- The UI sends only the platforms the user has connected (derived from `destinations` status ≠ `'none'`).

**Response** — `202 Accepted`

```json
{ "jobId": "job_xxxxxxxx", "status": "running" }
```

**Side effects**
- Each targeted platform's `status` is immediately set to `'pending'` by the server.
- On per-platform result: status updated to `'draft'` or `'error'`; a `TimelineEvent` is appended for each outcome.

---

## 7. Platform connection status

### `GET /api/platforms`

Populates the "N platforms connected" indicator in the nav bar.

**Response**

```json
{
  "platforms": [
    { "id": "medium",   "connected": true,  "label": "Medium",   "username": "@acisse" },
    { "id": "hashnode", "connected": true,  "label": "Hashnode", "username": "acisse.hashnode.dev" },
    { "id": "devto",    "connected": false, "label": "Dev.to",   "username": null }
  ]
}
```

- The overview only reads this; connecting / disconnecting is a Settings concern.
- The count badge (`3 platforms connected`) is derived client-side: `platforms.filter(p => p.connected).length`.

---

## 8. What is explicitly out of scope

| Feature                        | Reason excluded                                      |
|--------------------------------|------------------------------------------------------|
| Article content read/write     | Editor screen only                                   |
| Comment CRUD                   | Editor screen only                                   |
| Patch accept / reject          | Editor screen only                                   |
| Full timeline history          | Article-detail screen only                           |
| Platform live-URL / view stats | Article-detail screen only (needs published article) |
| Scheduling a publish time      | Publish-queue screen only                            |
| AI generation                  | Editor screen only                                   |
| Platform OAuth connect flow    | Settings screen only                                 |

---

## 9. Error handling expectations

| Scenario                        | Expected HTTP status | UI behaviour                              |
|---------------------------------|----------------------|-------------------------------------------|
| Article not found               | 404                  | Remove stale row, show toast              |
| Push/inspect while job running  | 409                  | Disable button while `status === 'pending'` |
| Platform auth expired           | 403 (from platform)  | Set destination `status: 'error'`, surface label |
| Delete published article        | 409                  | Show confirmation dialog with force option |
| Network / server error          | 500                  | Show inline error toast, keep existing data |

---

## 10. Data freshness strategy

The overview is read-heavy. Suggested approach (no real-time infrastructure required):

1. **On mount**: fetch `GET /api/articles` + `GET /api/platforms`.
2. **Search / filter change**: debounce 300 ms, re-fetch with updated query params.
3. **After user action** (create, delete, push, inspect): re-fetch the affected article row.
4. **Polling**: only active during in-flight jobs (inspect / push). Stop immediately on `done | error`.
5. **No websockets required** for the overview to be functional.
