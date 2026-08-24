# Blob Storage — Spec

**Status:** Approved for implementation (development mode)
**Depends on:** `sql.md` — SQLite holds all metadata and path references
**Goal:** Store article content and binary assets as files on disk. The DB stays lean: metadata, indexes, and paths only. No raw content or binary data in SQL rows.

---

## Rationale

Markdown is UTF-8 text and could fit in a `TEXT` column, but it conflates two concerns — the DB becomes both a metadata index and a file store. As binary assets enter the picture (images dropped during import: `.png`, `.jpg`, `.jpeg`, `.svg`) this becomes untenable:

- SQLite BLOBs fragment the B-tree and degrade read performance for all other queries
- No HTTP range requests, content-type headers, or CDN path
- Impossible to serve assets directly without reading them through SQLite

The clean split:
- **DB** holds metadata: title, word count, gate, destinations, timeline, and *paths* to content files
- **Filesystem** holds content: one `.md` per article, binary assets in a per-article subdirectory

---

## Directory layout (development)

```
blog-hub/
  data/                          ← gitignored
    bloghub.db                   ← SQLite (metadata + paths)
    blobs/                       ← BLOGHUB_BLOBS_DIR default
      articles/
        {article_id}/
          body.md                ← article markdown content
          assets/
            chart.png
            diagram.svg
            banner.jpg
```

`data/blobs/` is created automatically at startup if absent. It is gitignored.

---

## Configuration

| Env var            | Default       | Notes                                                    |
|--------------------|---------------|----------------------------------------------------------|
| `BLOGHUB_DB_PATH`  | `data/bloghub.db` | Path to SQLite database                              |
| `BLOGHUB_BLOBS_DIR`| `data/blobs`  | Root blob directory; relative to process CWD             |

---

## Schema changes to `articles` table

`body TEXT NOT NULL DEFAULT ''` is **kept** as a backward-compat fallback column.
`body_path TEXT` is **added** — a path relative to `BLOGHUB_BLOBS_DIR`, e.g. `articles/art_001/body.md`.

Read logic: if `body_path IS NOT NULL` → read file from disk. If `body_path IS NULL` → fall back to the `body` column (existing rows in a pre-migration DB, or seed data before first write).

`word_count` stays in the DB — computed on every write, avoids reading all files for a listing query.

**Migration applied at startup (idempotent):**
```sql
ALTER TABLE articles ADD COLUMN body_path TEXT;
```

---

## New table: `article_assets`

```sql
CREATE TABLE IF NOT EXISTS article_assets (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id  TEXT    NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    filename    TEXT    NOT NULL,
    asset_path  TEXT    NOT NULL,
    mime_type   TEXT,
    created_at  TEXT    NOT NULL,
    UNIQUE(article_id, filename)
);
```

`asset_path` is relative to `BLOGHUB_BLOBS_DIR`, e.g. `articles/art_001/assets/chart.png`.

---

## Store interface additions

```python
def store_asset(
    self,
    article_id: str,
    filename: str,
    data: bytes,
    mime_type: str | None = None,
) -> str:
    """
    Write binary data to disk at blobs/articles/{article_id}/assets/{filename}.
    Record the asset in article_assets.
    Return the asset_path (relative to BLOGHUB_BLOBS_DIR).
    """
```

---

## Lifecycle

| Event                 | Blob action                                                    |
|-----------------------|----------------------------------------------------------------|
| `create_article`      | `mkdir data/blobs/articles/{id}/assets/`; write initial `body.md` |
| `update_article_body` | Overwrite `body.md`; update `body_path` and `word_count` in DB |
| `store_asset`         | Write binary to `assets/{filename}`; upsert `article_assets` row |
| `delete_articles`     | `shutil.rmtree(data/blobs/articles/{id}/)` after DB row deleted |
| `store.reset()`       | Remove entire `data/blobs/articles/` tree, recreate, re-seed   |

---

## Backward compatibility

Callers (routers) still pass `content: str` to `update_article_body`. The store handles the disk write transparently — no router changes needed. The `get_article` dict still includes `body: str` (read from disk). Routers are unaware of the file system layout.

---

## Production path

In production, `BLOGHUB_BLOBS_DIR` can point to a mounted cloud storage volume or an S3-compatible bucket via a FUSE mount. The store interface is unchanged — only the path root changes. A future `store/backends/s3.py` can implement the same `store_asset` contract using boto3 directly (no filesystem involvement), satisfying the same Protocol.
