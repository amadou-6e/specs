# Contract — Dev Service

**Prefixes:** `/api/dev`, `/health`
**Swagger:** [swagger-dev.yaml](../backend/swagger-dev.yaml)
**Purpose:** Test isolation and server health probe. Not exposed in production.

> Gate in production with `APP_ENV=dev` or equivalent env flag.
> Connection credentials intentionally survive `POST /api/dev/reset`
> (they outlive article state in real usage too).

---

## Endpoint inventory

| Method | Path | Action | Used by |
|--------|------|--------|---------|
| `POST` | `/api/dev/reset` | Restore `_articles` + `_jobs` to seed | Playwright `beforeEach` |
| `GET` | `/health` | Confirm server is up | Playwright `webServer`, CI |

---

## 1. Test reset — `beforeEach` hook

Restores articles and jobs to seeded defaults (6 articles, no pending jobs).
Connections are **not** reset — they hold user secrets.

![diagram-1](assets/dev-service/diagram-1.png)

---

## 2. Health check — readiness probe

Used by `playwright.config.js → webServer.url` to wait for the server before running tests.

![diagram-2](https://mermaid.ink/img/c2VxdWVuY2VEaWFncmFtCiAgICBwYXJ0aWNpcGFudCBQVyBhcyBQbGF5d3JpZ2h0IC8gQ0kKICAgIHBhcnRpY2lwYW50IEIgYXMgRGV2IFNlcnZpY2UKCiAgICBsb29wIHVudGlsIDIwMCBvciB0aW1lb3V0CiAgICAgICAgUFctPj5COiBHRVQgL2hlYWx0aAogICAgICAgIGFsdCBzZXJ2ZXIgbm90IHlldCByZWFkeQogICAgICAgICAgICBCLS14UFc6IGNvbm5lY3Rpb24gcmVmdXNlZCAvIDV4eAogICAgICAgICAgICBOb3RlIG92ZXIgUFc6IHdhaXQgMjAwIG1zOyByZXRyeQogICAgICAgIGVsc2Ugc2VydmVyIHJlYWR5CiAgICAgICAgICAgIEItLT4-UFc6IDIwMCB7IHN0YXR1czogIm9rIiB9CiAgICAgICAgICAgIE5vdGUgb3ZlciBQVzogcHJvY2VlZCB3aXRoIHRlc3Qgc3VpdGUKICAgICAgICBlbmQKICAgIGVuZA==)
