# Blog Integration Contract

Every platform adapter — whether built into BlogHub or provided as a third-party plugin —
must implement this contract. Adapters that cannot support an operation should raise
`NotImplementedError`; optional capabilities are declared in the adapter's manifest.

---

## Directory layout

Each adapter lives in `blogs/<platform-id>/`:

```
blogs/
  hashnode/
    __init__.py          # exports: adapter class, MANIFEST
    client.py            # thin API wrapper (pure HTTP, no BlogHub imports)
    service.py           # maps BlogHub types ↔ platform types; calls client
    render.py            # Markdown → platform-specific HTML/JSON (if needed)
    test_<name>/         # unit + integration tests
      conftest.py
      test_client.py
      test_service.py
      test_render.py
      test_integration_<name>.py
```

`client.py` must have **zero** imports from `backend.*`. It is a reusable library.
`service.py` bridges the client with BlogHub's internal types.

---

## Manifest

Every `__init__.py` must expose a module-level `MANIFEST` dict:

```python
MANIFEST = {
    # Required
    "id":          "hashnode",          # unique slug, lowercase, no spaces
    "label":       "Hashnode",          # human-readable display name
    "kind":        "api",               # "api" | "automation"
    "auth":        "pat",               # see Auth schemes below

    # Capabilities — set False if unsupported
    "can_list_drafts":      True,
    "can_create_draft":     True,
    "can_update_draft":     True,
    "can_publish":          True,
    "can_list_published":   True,
    "can_import":           True,       # can fetch a remote article as Markdown
    "can_schedule":         False,      # scheduled publishing

    # UI hints
    "bg":       "#2c6ef7",              # card background colour
    "color":    "#ffffff",              # card text colour
    "initials": "H",                    # 1-2 character abbreviation
}
```

### Auth schemes

| Value | Meaning |
|-------|---------|
| `pat` | Personal Access Token — stored encrypted in BlogHub DB |
| `oauth2` | OAuth 2 Authorization Code flow — BlogHub handles redirect |
| `cookie` | Browser session cookie — automation adapter, set via Playwright |
| `wallet` | Cryptographic wallet signature (e.g. EIP-712 for Mirror.xyz) |

---

## Python adapter interface

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class RemoteArticle:
    """Normalized article fetched from a remote platform."""
    article_id:    str
    title:         str
    body_markdown: str
    url:           str | None
    canonical_url: str | None
    cover_image:   str | None
    published:     bool
    updated_at:    str | None   # ISO-8601 or None
    raw:           dict         # original API payload, unmodified


@dataclass(frozen=True)
class DraftResult:
    """Result returned after creating or updating a draft."""
    draft_id:   str
    url:        str | None
    raw:        dict


@dataclass(frozen=True)
class PublishResult:
    """Result returned after publishing an article."""
    article_id: str
    url:        str
    raw:        dict


@runtime_checkable
class BlogAdapter(Protocol):
    """
    Contract every blog adapter must satisfy.

    Instantiated with the user's credentials dict.
    The shape of `credentials` depends on MANIFEST["auth"]:
      - pat:     {"token": "<pat>"}
      - oauth2:  {"access_token": "...", "refresh_token": "...", "expires_at": "..."}
      - cookie:  {"cookie": "<session-cookie-string>"}
      - wallet:  {"address": "0x...", "private_key": "..."}  (never persisted in plain text)
    """

    def __init__(self, credentials: dict) -> None: ...

    # ── Core operations ──────────────────────────────────────────

    def list_drafts(self) -> list[RemoteArticle]:
        """Return all unpublished drafts accessible with these credentials."""
        ...

    def create_draft(
        self,
        title: str,
        body_markdown: str,
        *,
        cover_image: str | None = None,
        canonical_url: str | None = None,
        tags: tuple[str, ...] = (),
    ) -> DraftResult:
        """Create a new draft. Return its remote ID and preview URL."""
        ...

    def update_draft(
        self,
        draft_id: str,
        title: str,
        body_markdown: str,
        *,
        cover_image: str | None = None,
        canonical_url: str | None = None,
        tags: tuple[str, ...] = (),
    ) -> DraftResult:
        """Overwrite an existing draft."""
        ...

    def publish(self, draft_id: str) -> PublishResult:
        """Publish a draft. Return the canonical live URL."""
        ...

    def list_published(self) -> list[RemoteArticle]:
        """Return published articles owned by these credentials."""
        ...

    def fetch_article(self, article_id: str) -> RemoteArticle:
        """Fetch a single article (draft or published) by its platform ID."""
        ...

    # ── Optional operations ──────────────────────────────────────
    # Raise NotImplementedError if MANIFEST["can_schedule"] is False.

    def schedule(self, draft_id: str, publish_at: str) -> DraftResult:
        """Schedule a draft to publish at an ISO-8601 UTC timestamp."""
        ...
```

---

## Error contract

All adapter methods must raise only these exceptions (never raw `requests.HTTPError`):

| Exception | When |
|-----------|------|
| `AdapterAuthError` | Credentials invalid or expired |
| `AdapterRateLimitError` | Platform rate limit hit — include `retry_after` seconds if known |
| `AdapterNotFoundError` | Requested article/draft does not exist |
| `AdapterError` | Any other platform-side error — include message and status code |

All exceptions live in `blogs/_contract.py` so adapters can import without circular deps.

---

## Testing requirements

Every adapter must provide:

| Test file | What it covers |
|-----------|----------------|
| `test_client.py` | HTTP calls, request shape, response parsing — all mocked |
| `test_service.py` | Type mapping BlogHub ↔ platform, field normalization |
| `test_render.py` | Markdown → platform format conversion (if `render.py` exists) |
| `test_integration_<name>.py` | Live API call, marked `@pytest.mark.integration`, skipped if no credentials |

Integration tests must be skippable via missing env vars and must **not** publish publicly
(use draft-only operations or a dedicated test publication).

---

## Backend registration

Adapters are registered in `backend/routers/connections.py` via the `ADAPTERS` registry:

```python
from blogs.hashnode import MANIFEST as hashnode_manifest
from blogs.devto    import MANIFEST as devto_manifest

ADAPTERS: dict[str, dict] = {
    m["id"]: m
    for m in [hashnode_manifest, devto_manifest]
}
```

`GET /api/connections` reads `ADAPTERS` to build the platform list returned to the frontend.
The adapter class is loaded lazily when a connection is used, keyed by `MANIFEST["id"]`.
