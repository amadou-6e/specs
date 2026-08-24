# Settings — API Contract

---

## GET /platforms

Returns all platform configurations and session health.
(Shared with create-article — see that contract for full response shape.)

---

## POST /platforms/:id/connect

Initiates a platform connection. Behaviour varies by platform.

### For API-key platforms (Hashnode, Dev.to)

#### Request body
```json
{ "api_key": "string" }
```

#### Response 200
```json
{
  "platform": "hashnode",
  "status": "connected",
  "connected_at": "2026-04-02T14:00:00Z"
}
```

#### Response 401
```json
{ "error": "invalid_api_key" }
```

### For session-based platforms (Medium)

#### Request body
```json
{ "session_token": "string" }
```

#### Response 200
Same shape as above, includes `expires_at`.

---

## DELETE /platforms/:id/connect

Disconnects a platform (removes stored credentials).

### Response 204
No body.

---

## POST /platforms/:id/test

Tests whether the current stored session/key is valid.

### Response 200
```json
{
  "status": "ok",
  "detail": "Connected as @username"
}
```

### Response 401
```json
{
  "status": "error",
  "reason": "session_expired"
}
```

---

## GET /providers

Returns AI provider configurations.
(Shared with create-article — see that contract.)

---

## POST /providers/:id/key

Saves an API key for a provider.

### Request body
```json
{ "api_key": "string" }
```

### Response 200
```json
{
  "provider": "claude",
  "configured": true,
  "masked_key": "sk-ant-...abc"
}
```

### Response 422
```json
{ "error": "invalid_api_key", "reason": "string" }
```

---

## DELETE /providers/:id/key

Removes a provider API key.

### Response 204
No body.

---

## POST /providers/:id/test

Tests the stored API key.

### Response 200
```json
{
  "status": "ok",
  "model": "claude-opus-4-6"
}
```

### Response 401
```json
{
  "status": "error",
  "reason": "invalid_api_key"
}
```

---

## PATCH /account

Updates account display name.

### Request body
```json
{ "display_name": "string" }
```

### Response 200
```json
{ "display_name": "string" }
```

---

## POST /auth/signout

Signs the user out and clears the session.

### Response 204
Frontend redirects to login screen.

---

## Frontend error handling rules

| HTTP status | Behaviour                                                     |
|-------------|---------------------------------------------------------------|
| 401 (connect)| Show inline error on the platform card: "Invalid credentials"|
| 422 (key)   | Show inline error on the provider card with reason           |
| 500         | Toast: "Something went wrong. Try again."                    |
