# Cloud Storage Backends — Spec

**Status:** Future implementation (after SQLite is in place)
**Depends on:** `sql.md` — SQLite must be the local store before cloud sync is added
**Goal:** Let users sync their BlogHub data to a cloud storage provider they already own, with no hosting costs for us.

---

## Supported providers (priority order)

| Provider | Free storage | API quality | User base |
|----------|-------------|-------------|-----------|
| Google Drive | 15 GB | Excellent | Largest |
| OneDrive | 5 GB (Microsoft 365: 1 TB) | Good | Strong on Windows |
| Dropbox | 2 GB free | Excellent | Developer-friendly |

iCloud Drive has no public web API for third-party apps. It is not supported.

---

## Mental model

Cloud storage is a **sync target**, not the primary database. SQLite remains the source of truth for the running server. Cloud sync is a background operation that mirrors article content to a folder in the user's chosen provider.

```
BlogHub writes to SQLite
    → sync job reads from SQLite
    → writes to /BlogHub/ folder in cloud provider
```

This means:
- BlogHub works offline and after auth token expiry
- Sync failures surface as warnings, not blocking errors
- Users can open their cloud folder and see readable files

---

## Folder structure (same for all providers)

```
/BlogHub/
  articles/
    <article-id>/
      article.md        ← full markdown body
      meta.json         ← title, gate, source, destinations, updated_at
      images/
        <filename>      ← extracted from data: URIs (stored as real files)
  bloghub-index.json    ← lightweight index of all articles (id, title, updated_at)
```

Images embedded as `data:` URIs in the markdown body are extracted and saved as real files in `images/`. The stored `article.md` has the refs rewritten to relative paths (`images/chart.png`). This keeps the cloud copy human-readable.

---

## Sync triggers

| Trigger | Action |
|---------|--------|
| Article created | Upload `article.md` + `meta.json` |
| Article body updated | Upload `article.md` |
| Article deleted | Move to `BlogHub/.trash/<id>/` (not hard delete) |
| Platform push result | Update `meta.json` |
| Manual "Sync now" | Full reconcile: upload any local article missing from cloud |

Sync is one-directional for v1: BlogHub writes to cloud. Import-from-cloud (reading back into BlogHub) is a separate future feature.

---

## OAuth flows

Each provider uses OAuth 2.0 with an offline refresh token so the user only authenticates once.

### Google Drive

- Scopes: `https://www.googleapis.com/auth/drive.file` (access only to files BlogHub created — no access to the user's other Drive content)
- Flow: standard authorization code flow, redirect to BlogHub callback
- Token storage: `connections` table, `platform = 'google_drive'`
- API: Google Drive REST v3 (`files.create`, `files.update`, `files.get`)

### OneDrive

- Scopes: `Files.ReadWrite.AppFolder` (sandboxed to a single `/Apps/BlogHub/` folder — user cannot accidentally expose other files)
- Flow: Microsoft identity platform authorization code flow (PKCE)
- Token storage: `connections` table, `platform = 'onedrive'`
- API: Microsoft Graph v1.0 (`/me/drive/special/approot`)

### Dropbox

- Scopes: `files.content.write`, `files.content.read`
- Flow: Dropbox OAuth2 with PKCE
- Token storage: `connections` table, `platform = 'dropbox'`
- API: Dropbox API v2 (`files/upload`, `files/upload_session`)

---

## Backend design

### New modules

```
backend/services/cloud_sync.py      ← orchestrator: decides what to sync and when
backend/services/providers/
    google_drive.py                 ← Google Drive API client
    onedrive.py                     ← Microsoft Graph client
    dropbox.py                      ← Dropbox API client
```

All three provider modules expose the same interface:

```python
class CloudProvider(Protocol):
    def upload_file(self, path: str, content: bytes, mime: str) -> str: ...
    def update_file(self, file_id: str, content: bytes) -> None: ...
    def move_file(self, file_id: str, new_path: str) -> None: ...
    def file_exists(self, path: str) -> str | None: ...  # returns file_id or None
```

`cloud_sync.py` calls these through the protocol — swapping providers requires no changes to the orchestrator.

### New DB columns

```sql
ALTER TABLE articles ADD COLUMN cloud_file_id TEXT;
ALTER TABLE articles ADD COLUMN cloud_synced_at TEXT;
```

`cloud_file_id` is the provider's opaque file ID for `article.md`. Used for updates (avoids re-lookup by path on every sync).

### Sync job

Sync runs as a FastAPI background task (`BackgroundTasks`) triggered on write operations. It is not a cron job — no scheduler dependency needed.

Token refresh is handled per-request inside each provider module. If refresh fails (revoked token), the sync job records the error and sets `cloud_synced_at = NULL`. The UI surfaces this as a warning badge on the settings screen.

---

## Settings UI additions

The existing settings screen (`screens/settings/v2.html`) gains a "Cloud Storage" section with:
- A provider picker (Google Drive / OneDrive / Dropbox, styled as platform cards)
- Connect / Disconnect buttons (same OAuth flow pattern as AI providers)
- Last synced timestamp
- "Sync now" button that triggers a full reconcile
- Error state if last sync failed (token expired, quota exceeded, network error)

Only one provider can be active at a time (no multi-cloud for v1).

---

## Pricing / hosting cost

None. All storage is in the user's account. BlogHub only needs OAuth app credentials (free) registered with each provider's developer console.

Developer console registrations needed:
- Google Cloud Console: OAuth 2.0 client ID for web app
- Microsoft Azure: App registration with delegated Files.ReadWrite.AppFolder
- Dropbox App Console: app with scoped permissions

---

## Error handling

| Error | Behaviour |
|-------|-----------|
| Token expired | Auto-refresh. If refresh fails, mark sync error. |
| Quota exceeded | Mark sync error, show warning in settings. |
| Network timeout | Retry up to 3 times with exponential backoff. |
| File conflict | BlogHub wins: overwrite cloud copy. |
| Provider API 5xx | Log error, retry on next write. |

---

## What is explicitly out of scope for v1

- Import from cloud (reading back into BlogHub)
- Multi-cloud (more than one active provider)
- Real-time collaboration
- Conflict resolution beyond "BlogHub wins"
- iCloud
