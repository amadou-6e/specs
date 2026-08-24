# Third-Party Plugin System

This document describes how external developers can write their own BlogHub blog adapters
and distribute them as installable Python packages.

---

## Overview

A BlogHub plugin is any Python package that:

1. Implements the [integration contract](./contract.md) (`BlogAdapter` protocol + `MANIFEST` dict)
2. Declares a `bloghub.adapter` entry point in its `pyproject.toml`
3. Is installed into the same Python environment as BlogHub

BlogHub discovers plugins automatically at startup via `importlib.metadata` — no config file
edits or code changes are required.

---

## Entry point declaration

In your plugin's `pyproject.toml`:

```toml
[project]
name = "bloghub-ghost"
version = "0.1.0"
dependencies = ["requests>=2.31"]

[project.entry-points."bloghub.adapter"]
ghost = "bloghub_ghost:MANIFEST"
```

The key (`ghost`) must match `MANIFEST["id"]`. The value is the import path to the `MANIFEST`
dict in your package.

---

## Minimal plugin layout

```
bloghub-ghost/
  pyproject.toml
  bloghub_ghost/
    __init__.py          # exports MANIFEST and GhostAdapter
    client.py            # thin Ghost Admin API wrapper
    service.py           # maps BlogHub types ↔ Ghost types
```

`__init__.py` minimum:

```python
from bloghub_ghost.service import GhostAdapter

MANIFEST = {
    "id":                 "ghost",
    "label":              "Ghost",
    "kind":               "api",
    "auth":               "pat",
    "can_list_drafts":    True,
    "can_create_draft":   True,
    "can_update_draft":   True,
    "can_publish":        True,
    "can_list_published": True,
    "can_import":         True,
    "can_schedule":       True,
    "bg":                 "#212121",
    "color":              "#ffffff",
    "initials":           "G",
    "adapter_class":      GhostAdapter,   # must satisfy BlogAdapter protocol
}
```

---

## Plugin discovery (how BlogHub loads plugins)

At startup, `backend/plugins.py` (to be built) runs:

```python
import importlib.metadata

def discover_adapters() -> dict[str, dict]:
    adapters = {}
    for ep in importlib.metadata.entry_points(group="bloghub.adapter"):
        try:
            manifest = ep.load()          # loads MANIFEST dict
            _validate_manifest(manifest)
            adapters[manifest["id"]] = manifest
        except Exception as exc:
            logger.warning("Skipping plugin %s: %s", ep.name, exc)
    return adapters
```

Built-in adapters (Hashnode, Dev.to, Medium) are registered the same way as plugins —
they declare the same entry point in the main `pyproject.toml`. There is no privileged
"built-in" path.

---

## Adapter validation

`_validate_manifest` checks:

- Required keys present: `id`, `label`, `kind`, `auth`, `adapter_class`
- `kind` in `{"api", "automation"}`
- `auth` in `{"pat", "oauth2", "cookie", "wallet"}`
- `adapter_class` satisfies `isinstance(cls, type)` and `issubclass(cls, BlogAdapter)` (runtime check)
- `id` is unique (no two plugins share the same id — first one wins, warning emitted for duplicates)

---

## OAuth 2 plugins

Plugins that declare `"auth": "oauth2"` must additionally provide:

```python
MANIFEST = {
    ...
    "oauth2": {
        "authorize_url":  "https://example.com/oauth/authorize",
        "token_url":      "https://example.com/oauth/token",
        "scopes":         ["posts:write", "posts:read"],
        "client_id_env":  "GHOST_CLIENT_ID",       # env var BlogHub reads
        "client_secret_env": "GHOST_CLIENT_SECRET",
    },
}
```

BlogHub's OAuth controller reads these values and handles the redirect/callback flow
generically — the plugin does not need to implement any auth endpoints.

---

## Automation (browser) plugins

Plugins that declare `"kind": "automation"` are allowed to use Playwright internally.
BlogHub will warn users during connection setup that automation adapters are less stable
than API adapters.

Automation plugins must declare:

```python
MANIFEST = {
    ...
    "kind":         "automation",
    "auth":         "cookie",
    "login_url":    "https://substack.com/sign-in",   # opened by BlogHub setup wizard
}
```

BlogHub will surface a one-time "connect" flow in Settings that opens the login URL in a
headless browser, captures the session cookie, and stores it encrypted.

---

## Credential storage

BlogHub never stores credentials in plain text. All tokens and cookies are encrypted at rest
using the key in `BLOGHUB_SECRET_KEY` (AES-GCM via `backend/store/crypto.py`).

Plugins receive a plain `credentials: dict` on instantiation — decryption is handled by
BlogHub before calling the adapter. Plugins must not re-encrypt or re-store credentials.

---

## Versioning and compatibility

| BlogHub version | Contract version | Breaking changes |
|----------------|-----------------|-----------------|
| 0.x | 1 | Initial draft — subject to change |
| 1.0 | 1 | Stable — no breaking changes without major version bump |

Plugins may declare a minimum BlogHub version in their `pyproject.toml`:

```toml
[project]
dependencies = ["bloghub-sdk>=1.0"]
```

`bloghub-sdk` (to be published) will re-export the contract types (`RemoteArticle`,
`DraftResult`, `PublishResult`, `BlogAdapter`, all `AdapterError` subclasses) so plugin
authors have a stable import target independent of BlogHub internals.

---

## Publishing a plugin

1. Implement the contract and write tests (see [contract.md](./contract.md))
2. Publish to PyPI: `pip publish` / `twine upload`
3. Name your package `bloghub-<platform>` by convention (not enforced)
4. Users install it: `pip install bloghub-ghost`
5. Restart BlogHub — the adapter appears automatically in Settings → Connections

---

## Security considerations

- Plugins run in the same process as BlogHub — only install trusted packages
- BlogHub validates manifests but cannot sandbox plugin code
- Future: a `--plugins-dir` flag will support loading plugins from a local directory
  without PyPI, for development and air-gapped deployments
