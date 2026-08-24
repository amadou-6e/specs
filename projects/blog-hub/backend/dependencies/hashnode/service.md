# Dependency — Hashnode

Used by the **Articles** service to push article drafts to Hashnode.

---

## Caller

```
Articles push service  ──────────────────────────────►  Hashnode GraphQL API
  POST /api/articles/{id}/push                          https://gql.hashnode.com
```

---

## 1. Endpoint

| Property | Value |
|----------|-------|
| URL | `https://gql.hashnode.com` |
| Protocol | GraphQL over HTTPS (`POST` with JSON body) |
| Auth | `Authorization: <token>` header — **no "Bearer" prefix** |
| Timeout | 30 s |
| Client | `requests.Session` (from `article_publishing/publishing/hashnode.py`) |

---

## 2. Request Headers

```http
Content-Type: application/json
Authorization: <personal_access_token>
```

> The token has no prefix — sending `"Bearer <token>"` will fail.

---

## 3. Create Draft Mutation

### GraphQL

```graphql
mutation CreateDraft($input: CreateDraftInput!) {
  createDraft(input: $input) {
    draft {
      id
      title
      canonicalUrl
      coverImage {
        url
      }
    }
  }
}
```

### Variables payload

```json
{
  "query": "<mutation above>",
  "variables": {
    "input": {
      "title":           "<article title>",
      "publicationId":   "<hashnode publication id>",
      "contentMarkdown": "<article body — no leading H1>",
      "tags": [
        { "name": "Docker",    "slug": "docker" },
        { "name": "Postgres",  "slug": "postgres" }
      ],
      "subtitle":              "<optional subtitle>",
      "originalArticleURL":    "<canonical URL if cross-posting>",
      "coverImageOptions": {
        "coverImageURL": "<https://... cover image>"
      }
    }
  }
}
```

**Field notes:**

| Field | Key | Notes |
|-------|-----|-------|
| `contentMarkdown` | required | Leading `# H1` must be stripped (`HashnodeClient.strip_leading_h1()`) — Hashnode renders `title` separately |
| `publicationId` | required | Hashnode publication (blog) identifier — stored in connection settings |
| `tags[].slug` | derived | Slugified from tag name: lowercase, `[^a-z0-9]+` → `-`, trimmed |
| `originalArticleURL` | optional | Set when cross-posting; tells Hashnode the canonical source |
| `coverImageOptions` | optional | Omitted when no cover image available |
| `subtitle` | optional | Second headline shown below title |

> **@tbd**: Where does `publicationId` come from in blog-hub?  
> Options: (a) stored with the Hashnode connection credential, (b) per-article destination config.

---

## 4. Success Response

```json
{
  "data": {
    "createDraft": {
      "draft": {
        "id":           "<draft_id>",
        "title":        "Building a Vector DB from Scratch",
        "canonicalUrl": null,
        "coverImage":   { "url": "https://cdn.hashnode.com/..." }
      }
    }
  }
}
```

**Extracted and persisted:**

| Field | Stored as |
|-------|-----------|
| `draft.id` | `destination.draft_id` — used to link to draft URL |
| `draft.canonicalUrl` | logged |
| `draft.coverImage.url` | logged |

---

## 5. Error Handling

GraphQL errors appear in a top-level `"errors"` array, not as HTTP 4xx:

```json
{
  "errors": [
    { "message": "Publication not found", "locations": [...] }
  ]
}
```

| Condition | Behaviour |
|-----------|-----------|
| `response.errors` present | Raise `HashnodeError(str(errors))` |
| HTTP non-2xx | `response.raise_for_status()` → `requests.HTTPError` |
| Network timeout (>30 s) | `requests.Timeout` propagates to job error handler |

All errors map to: job `status=error`, destination `status=error`, `error_message=<str>`.

---

## 6. Content Preprocessing (from `article_publishing`)

Applied **before** sending to Hashnode:

| Step | Function | What it does |
|------|----------|-------------|
| Strip leading H1 | `HashnodeClient.strip_leading_h1()` | Removes first `# Title` line; Hashnode renders it separately from `title` field |
| Slugify tags | `HashnodeClient.slugify_tag()` | `re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")` |

---

## 7. Environment / Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| Hashnode PAT | yes | Stored as `_connections["hashnode"]["token"]` after user saves it via `PUT /api/connections/hashnode` |
| Publication ID | yes — **@tbd** | Not yet specified where this is stored in blog-hub |

---

## 8. Stored Credential Shape

```python
# _connections["hashnode"]
{
  "token":         "<Hashnode Personal Access Token>",
  "status":        "connected",
  "username":      None,            # Hashnode token has no /me endpoint to fetch username
  "connected_at":  datetime(...),
  "error_message": None,
}
```

> **Note**: Unlike Medium, there is no server-side "verify token" step at connection time.  
> The token is accepted and stored immediately; failures surface at push time.
