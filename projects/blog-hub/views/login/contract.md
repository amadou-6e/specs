# Login View — API Contract

> Scope: this file defines service requests and payloads. UI geometry, visible states,
> interaction IDs, and transitions are governed by [login.drawio](login.drawio).

Backend lives at the same origin (no CORS needed in production).
Dev backend: `http://localhost:8082`.

---

## Session check on page load

**Request:**
```
GET /api/auth/me
```

**Usage:** Called immediately on page load. If 200, redirect to overview.

**Responses:**
- `200 OK`: `{ "id": "...", "email": "...", "created_at": "..." }` — user is logged in, redirect
- `401 Unauthorized`: stay on login page

---

## Login

**Request:**
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "mypassword123",
  "remember_me": false
}
```

**Responses:**
- `200 OK`: `{ "id": "...", "email": "..." }` + `Set-Cookie: bloghub_session=...; HttpOnly; SameSite=Strict`
- `401 Unauthorized`: `{ "detail": "Invalid email or password" }` — show in ErrorBanner
- `422 Unprocessable Entity`: validation error — show field errors

**Loading state:** Show spinner on button from click until response resolves.

---

## Register

**Request:**
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "mypassword123"
}
```

**Responses:**
- `201 Created`: `{ "id": "...", "email": "..." }` + `Set-Cookie: bloghub_session=...; HttpOnly; SameSite=Strict`
- `409 Conflict`: `{ "detail": "An account with this email already exists" }` — show in ErrorBanner
- `422 Unprocessable Entity`: `{ "detail": [{ "loc": [...], "msg": "...", "type": "..." }] }` — map to field errors

---

## 422 error mapping

FastAPI returns structured validation errors. Map as follows:

| `loc` value    | Field to mark | Message to show                          |
|----------------|---------------|------------------------------------------|
| `["body", "email"]`    | email  | Use `msg` from the response              |
| `["body", "password"]` | password | Use `msg` from the response             |
| Other / unknown | ErrorBanner  | "Validation error. Check your input."   |

---

## Post-auth redirect

On any successful auth response (200 or 201), navigate to:
```
/screens/overview/v3.html
```

No token storage needed in JS — the server sets an HttpOnly cookie automatically.
