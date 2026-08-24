# Backend Spec Audit

**Scope:** All 5 swagger specs in `.spec/backend/` cross-referenced against:
- `.spec/views/*/interactions.md` (4 views, 96 operations total)
- `contracts/overview.ts` (handwritten TS contract)
- `contracts/generated/*.ts` (openapi-typescript output)
- `backend/schemas/generated/*.py` (datamodel-codegen output)

**Date:** 2026-04-03  
**Auditor:** automated cross-reference

---

## A1 — CRITICAL: `POST /api/connections/{conn_id}/test` is missing from the spec

**File:** `connections/swagger.yaml`  
**Called by:** ST-13 (Test platform connection), ST-24 (Test AI provider connection)

The settings screen defines a `testConn(id)` function that calls this endpoint and shows
"OK" / "Failed" feedback. No path, schema, or response code for it exists anywhere in
`connections/swagger.yaml`.

**Fix:** Add to `connections/swagger.yaml`:

```yaml
/api/connections/{conn_id}/test:
  post:
    operationId: testConnection
    tags: [connections]
    summary: Test a saved connection
    description: |
      Verifies the stored credential is still valid by making a lightweight
      authenticated request to the platform or AI provider.
      Returns the new status — `connected` if the credential works, `error` if not.
    parameters:
      - name: conn_id
        in: path
        required: true
        schema: { $ref: "#/components/schemas/ConnectionId" }
    responses:
      "200":
        description: Test complete.
        content:
          application/json:
            schema:
              type: object
              required: [status]
              properties:
                status: { type: string, enum: [connected, error] }
                error_message: { type: string, nullable: true }
      "404":
        description: Unknown connection ID.
      "422":
        description: No token stored — nothing to test.
```

---

## A2 — HIGH: `GenerateRequest` fields use snake_case, violating the camelCase convention

**File:** `agent/swagger.yaml` → `components/schemas/GenerateRequest`  
**Fields:** `word_count`, `context_text`  
**Called by:** CA-23 — screen sends `wordCount`, `contextText`

Every other schema in the project uses camelCase for JSON field names (e.g., `wordCount`,
`createdAt`, `jobId`). The `GenerateRequest` schema is the only exception.

The generated Pydantic (`backend/schemas/generated/agent.py`) will emit snake_case
fields with camelCase aliases only if the spec field names already use camelCase.
Because the spec has `word_count`, the alias would be absent.

**Fix in `agent/swagger.yaml`:**

| Current | Correct |
|---------|---------|
| `word_count` | `wordCount` |
| `context_text` | `contextText` |

Also update `required: [brief, skill, provider, word_count, destinations]`
→ `required: [brief, skill, provider, wordCount, destinations]`.

---

## A3 — HIGH: `GenerateAccepted.article_id` is snake_case while `jobId` is camelCase

**File:** `agent/swagger.yaml` → `components/schemas/GenerateAccepted`

```yaml
# Current (inconsistent)
GenerateAccepted:
  required: [jobId, status, article_id]
  properties:
    jobId:      { type: string }   # camelCase
    status:     { type: string }   # camelCase
    article_id: { type: string }   # snake_case ← WRONG
```

The `contracts/generated/agent.ts` will produce both `jobId` and `article_id` as typed
fields, making the contract a mix of two conventions.

**Fix:** Rename `article_id` → `articleId` in both `properties` and `required`.

---

## A4 — HIGH: `ConnectionInfo` has 3 snake_case fields without camelCase counterparts

**File:** `connections/swagger.yaml` → `components/schemas/ConnectionInfo`

| Field current | Should be |
|---------------|-----------|
| `auth_method` | `authMethod` |
| `connected_at` | `connectedAt` |
| `error_message` | `errorMessage` |

`SaveTokenResponse` also uses `error_message` — same fix needed there.

These appear in the list example too:
```yaml
- id: medium
  auth_method: oauth_or_token     # ← snake_case in example
  connected_at: "2026-04-03…"    # ← snake_case in example
  error_message: null             # ← snake_case in example
```

Because these are the only property names the client reads from `GET /api/connections`,
any TypeScript or Pydantic consumer will receive `auth_method` etc. — inconsistent with
every other model in the codebase.

**Fix:** Rename all three in both schema definitions and all inline examples.

---

## A5 — MEDIUM: `Comment` schema is defined differently in two separate specs

**Files:** `articles/swagger.yaml` and `comments-patches/swagger.yaml`

| Field | `articles` | `comments-patches` |
|-------|------------|-------------------|
| `id` | ✓ | ✓ |
| `author` | ✓ | ✓ |
| `text` | ✓ | ✓ |
| `createdAt` | ✓ | ✓ |
| `resolved` | ✓ | ✓ |
| `hasPatch` | ✓ | ✓ |
| `anchor` | optional | optional |
| `article_id` | ✗ absent | ✓ present (snake_case) |

The `articles` spec omits `article_id` — reasonable since it is implicit from the URL
context. The `comments-patches` spec includes it but names it snake_case.

**Fix:**
1. Rename `article_id` → `articleId` in `comments-patches/swagger.yaml`.
2. Document which spec is authoritative (comments-patches is the CRUD home;
   articles borrows the schema for embedding in `ArticleDetail`).

---

## A6 — MEDIUM: `Patch` schema duplicated with different fields across two specs

**Files:** `articles/swagger.yaml` and `comments-patches/swagger.yaml`

| Field | `articles` | `comments-patches` |
|-------|------------|-------------------|
| `id` | ✓ | ✓ |
| `label` | ✓ | ✓ |
| `removed` | ✓ | ✓ |
| `added` | ✓ | ✓ |
| `state` | ✓ | ✓ |
| `article_id` | ✗ absent | ✓ present (snake_case) |
| `comment_id` | ✗ absent | ✓ present (snake_case) |

Both `article_id` and `comment_id` in `comments-patches` are snake_case.

**Fix:** Rename both to `articleId`, `commentId`. Resolve which spec owns the schema.

---

## A7 — MEDIUM: `JobType` enum is missing `generate`

**File:** `jobs/swagger.yaml` → `components/schemas/JobType`  
**Current:** `enum: [inspect, push]`

`POST /api/agent/generate` also creates a job and returns a `jobId` (see `GenerateAccepted`).
The description even says "jobs are created by push and inspect" — excluding agent generate
entirely. Polling `GET /api/jobs/{jobId}` for a generate job would return a `JobResponse`
with an unrecognized type.

**Fix:**
1. Add `generate` to `JobType` enum: `enum: [inspect, push, generate]`.
2. Update the spec description to include agent generate.

---

## A8 — MEDIUM: `ArticleListQuery.platform` missing from `contracts/overview.ts`

**File:** `contracts/overview.ts` → `ArticleListQuery`  
**Spec:** `articles/swagger.yaml` → `GET /api/articles` parameters

The swagger defines a `platform` query parameter for filtering by platform.
The `ArticleListQuery` interface in `contracts/overview.ts` does not include it.

The overview screen's filter bar (OV-03: platform filter dropdown) will pass `platform`
as a query param — but the contract doesn't type it, so TypeScript callers have no
guidance.

**Fix in `contracts/overview.ts`:**
```ts
export interface ArticleListQuery {
    q?: string;
    gate?: GateStatus;
    status?: PlatformStatus;
    platform?: Platform;   // ← ADD THIS
    page?: number;
    pageSize?: number;
    sortBy?: 'updatedAt' | 'createdAt' | 'title';
    sortDir?: 'asc' | 'desc';
}
```

---

## A9 — MEDIUM: `AsyncAccepted.status` Pydantic default breaks `required`

**File:** `articles/swagger.yaml` → `components/schemas/AsyncAccepted`  
**Also in:** `agent/swagger.yaml` (same schema, separate definition)

The spec marks `status` as `required`. But the Pydantic model (both handwritten and generated)
assigns `status: JobStatus = JobStatus.running` as a default, which means Pydantic v2 does
**not** include `status` in `model_json_schema()["required"]`. The existing compat test
**fails** on this field.

This is a Pydantic-side issue, not a spec error — but it surfaces as a spec/implementation
gap. Two options:

1. **Remove the default** in Pydantic → `status: JobStatus` (no default). Spec is correct.
2. **Acknowledge divergence** in the compat test skip list and document why.

Recommended: option 1 (remove the default; `status` is always `running` on `202` returns,
so defaulting it is unnecessary).

---

## A10 — LOW: `AsyncAccepted` defined in two specs independently

**Files:** `articles/swagger.yaml` and `agent/swagger.yaml`

Identical schema defined twice. No shared components across specs. Low risk now but
will drift if one spec changes.

**Fix (optional):** Extract to a shared `common.yaml` and `$ref` from both, or just
accept duplication given current project scope.

---

## A11 — LOW: `POST /api/agent/regenerate/{article_id}` has no caller in interactions

**File:** `agent/swagger.yaml`  
**Spec:** `POST /api/agent/regenerate/{article_id}` exists, documented, with a `provider`
override body.

None of the 4 interactions files (OV, CA, ED, ST) reference this endpoint.
The editor interactions file (ED-01 to ED-26) has no "Regenerate" operation.

Either:
- The screen has no Regenerate button yet (planned feature) → document as `@future` in
  the interactions file.
- The button exists but was missed → add ED-27 for it.

---

## A12 — LOW: `platforms/swagger.yaml` legacy status vs. current v4 overview usage

**File:** `platforms/swagger.yaml`

Marked "legacy, prefer `/api/connections`". The current `overview/v4.html` screen should
call `/api/connections` for the nav-bar "N platforms connected" count. If `v4` still calls
`/api/platforms`, the legacy service is still required infrastructure, not truly optional.

**Action:** Confirm in `overview/v4.html` which endpoint the nav-bar count uses.
If `/api/connections` — mark `platforms/swagger.yaml` as `deprecated: true` on the path.
If `/api/platforms` — remove the "prefer connections" warning until v4 is updated.

---

## Summary Table

| ID | Severity | File | Issue |
|----|----------|------|-------|
| A1 | **Critical** | connections/swagger.yaml | `POST /api/connections/{conn_id}/test` — endpoint missing entirely |
| A2 | **High** | agent/swagger.yaml | `GenerateRequest.word_count` + `.context_text` snake_case vs camelCase convention |
| A3 | **High** | agent/swagger.yaml | `GenerateAccepted.article_id` snake_case mixed with camelCase `jobId` |
| A4 | **High** | connections/swagger.yaml | `ConnectionInfo.auth_method`, `.connected_at`, `.error_message` + `SaveTokenResponse.error_message` all snake_case |
| A5 | **Medium** | comments-patches/swagger.yaml | `Comment.article_id` snake_case; schema diverges from articles spec |
| A6 | **Medium** | comments-patches/swagger.yaml | `Patch.article_id`, `.comment_id` snake_case; schema diverges from articles spec |
| A7 | **Medium** | jobs/swagger.yaml | `JobType` enum missing `generate`; description incomplete |
| A8 | **Medium** | contracts/overview.ts | `ArticleListQuery` missing `platform` filter field |
| A9 | **Medium** | articles/swagger.yaml, agent | `AsyncAccepted.status` Pydantic default omits field from `required` — compat test fails |
| A10 | **Low** | articles, agent swagger | `AsyncAccepted` schema duplicated across two independent specs |
| A11 | **Low** | agent/swagger.yaml | `POST /api/agent/regenerate/{article_id}` has no caller in any interactions file |
| A12 | **Low** | platforms/swagger.yaml | Legacy status unclear — verify if v4 overview still calls `/api/platforms` |

---

## Endpoint Coverage Map

Every **Async** and **Navigate** operation in the interactions files, checked against the swagger:

| Interaction op | Method + Path | Status |
|---------------|---------------|--------|
| OV-01 | `GET /api/articles` | ✓ |
| OV-05 | `POST /api/articles` | ✓ |
| OV-09 | `DELETE /api/articles` | ✓ |
| OV-15 | `GET /api/articles/{id}` | ✓ |
| OV-16 | `POST /api/articles/{id}/push` | ✓ |
| OV-17 | `GET /api/jobs/{jobId}` (poll) | ✓ |
| OV-18 | `POST /api/articles/{id}/inspect` | ✓ |
| CA-23 | `POST /api/agent/generate` | ✓ |
| CA-23 | `GET /api/jobs/{jobId}` (poll) | ✓ |
| ED-04 | `PATCH /api/articles/{id}` | ✓ |
| ED-12 | `GET /api/articles/{id}/comments` | ✓ |
| ED-13 | `POST /api/articles/{id}/comments` | ✓ |
| ED-14 | `GET /api/articles/{id}/patches` | ✓ |
| ED-16 | `POST /api/agent/generate-patch/{articleId}/comments/{commentId}` | ✓ |
| ED-17 | `POST /api/articles/{id}/comments/{cid}/resolve` | ✓ |
| ED-18 | `POST /api/patches/{patchId}/accept` | ✓ |
| ED-19 | `POST /api/patches/{patchId}/reject` | ✓ |
| ST-01 | `GET /api/connections` | ✓ |
| ST-07 | `GET /api/connections/medium/oauth-start` | ✓ |
| ST-09 | `PUT /api/connections/{id}` | ✓ |
| ST-13 | `POST /api/connections/{id}/test` | **✗ MISSING** |
| ST-16 | `DELETE /api/connections/{id}` | ✓ |
| ST-24 | `POST /api/connections/{id}/test` | **✗ MISSING** |

21 of 23 mapped interaction calls have a corresponding spec endpoint.  
2 are missing: both map to the same unspecified `test` endpoint (A1 above).
