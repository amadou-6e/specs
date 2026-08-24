# Settings / Platforms — Interactions

Source: `screens/settings/v2.html`

**Type key:**
- **Self** — stays on view, no navigation
- **Navigate** — moves to another view
- **Async** — fires API call; result reflected on same view
- **External** — opens new tab

---

## Global preconditions

The Settings view loads and immediately calls `GET /api/connections`. If the API is unreachable it falls back to a static disconnected state for all platforms. No authentication gate on the view itself — but connecting a platform requires the credentials for that platform.

---

## Navigation bar

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ST-01 | `a[href*="overview"]` | Click "Articles" nav link | — | → Overview | Navigate |
| ST-02 | `a[href="#"]:has-text("Queue")` | Click "Queue" nav link | — | → Publish Queue view | Navigate |
| ST-03 | `a[href*="settings"]` (active) | Click "Settings" nav link | — | Active (no-op, already on view) | Self |

---

## Section tabs

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ST-04 | `button[data-section="platforms"]` | Click "Platforms" tab | — | `#section-platforms` shown; `#section-ai` and `#section-account` hidden; tab gets `active` class | Self |
| ST-05 | `button[data-section="ai"]` | Click "AI Providers" tab | — | `#section-ai` shown; others hidden | Self |
| ST-06 | `button[data-section="account"]` | Click "Account" tab | — | `#section-account` shown; others hidden | Self |

---

## Platform cards (Medium, Hashnode, Dev.to)

### Not connected state

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ST-07 | `button[onclick*="expandKey"]` (inside `#plat-card-{id}`) | Click "Connect" button | Platform status = `disconnected` | Expands `#key-input-{id}` form within the card; focuses input | Self |
| ST-08 | `button[onclick*="doOAuth"]` | Click "Sign in with {Platform} →" OAuth button | Platform has `oauth: true` (Medium); form is shown | `GET /api/connections/{id}/oauth-start` → opens platform auth URL in new tab; throbber shown | External → Async |
| ST-09 | `#key-input-{id}` | Paste / type API key in expanded input | Form is expanded | Input receives value; "Save" becomes active | Self |
| ST-10 | `button[onclick*="saveKey"]` | Click "Save" button | `#key-input-{id}` is non-empty | `PUT /api/connections/:id {token}` → collapses form; reloads connections list; card re-renders as connected | Async |
| ST-11 | `#key-input-{id}` | Press Enter in API key input | Input is non-empty | Same as clicking "Save" (ST-10) | Async |
| ST-12 | `button[onclick*="collapseKey"]` | Click "Cancel" button | Form is expanded | Collapses form; clears input; card unchanged | Self |
| ST-13 | `a[href][target="_blank"]` (help link in card) | Click "Get your {token} →" help link | — | Opens platform's API token documentation in new tab | External |

### Connected state

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ST-14 | `#test-btn-{id}` | Click "Test" button | Platform status = `connected` | `POST /api/connections/:id/test` → spinner → ✓ OK (green) or ✗ Failed (red) | Async |
| ST-15 | `button[onclick*="expandKey"]` (connected card) | Click "Update" button | Platform status = `connected` | Expands `#key-input-{id}` for token replacement (same as ST-09 → ST-10) | Self |
| ST-16 | `button[onclick*="toggleConfirm"]` | Click "Disconnect" link | Platform status = `connected` | Opens inline confirmation popover anchored to link | Self |
| ST-17 | `button[onclick*="doDisconnect"]` | Click confirm "{Verb}" button in popover | Popover is open | `DELETE /api/connections/:id` → reloads list; card re-renders as disconnected | Async |
| ST-18 | `button[onclick*="closeConfirm"]` | Click "Cancel" in confirm popover | Popover is open | Closes popover; no change | Self |

### Expired state

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ST-19 | `button[onclick*="expandKey"]` (expired card) | Click "Reconnect" button | Platform status = `expired` | Expands inline API key input (same flow as ST-07 onwards) | Self |

---

## AI Provider cards (Anthropic / Claude, OpenAI / Codex)

### Not configured state

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ST-20 | `button[onclick*="doOAuth"]` (AI card) | Click "Login with browser" button | Provider has OAuth support; status = `disconnected` | `GET /api/connections/:id/oauth-start` → opens auth URL in new tab; login throbber shown | Async + External |
| ST-21 | `button[onclick*="expandKey"]` (AI card, not configured) | Click "Add API key" button | Provider status = `disconnected` | Expands `#key-input-{id}`; focuses input | Self |
| ST-22 | `button[onclick*="saveKey"]` (AI card) | Paste / type key; click "Save" | Input is non-empty | `PUT /api/connections/:id {token}` → card re-renders as connected | Async |
| ST-23 | `button[onclick*="collapseKey"]` (AI card) | Click "Cancel" in expanded form | Form is expanded | Collapses form; clears input | Self |
| ST-24 | `a[href][target="_blank"]` (AI help link) | Click "Get your {API key} →" help link | — | Opens provider's API key documentation in new tab | External |

### Browser login — Anthropic loopback OAuth (`flow: "cli_browser"`)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ST-25 | — (system event) | `oauth-start` returns `flow: "cli_browser"` | ST-20 completed | Throbber shown: instruction to copy address-bar URL + `#code-input-{id}` + Submit; polling starts (`GET …/cli-login-status` every 2 s) | Self |
| ST-26 | `button[onclick*="submitCode"]` | User pastes callback URL and clicks "Submit" | Loopback throbber shown; input non-empty | `POST /api/connections/anthropic/submit-code {code: "<full URL>"}` → on 200: throbber waits; on 409: error + retry | Async |
| ST-27 | — (poll event) | Poll returns `connected` | Polling active | Polling stops; throbber closes; list reloads; card re-renders as connected | Self |
| ST-28 | — (poll event) | Poll returns `error` | Polling active | Polling stops; error shown; "Try again" option offered | Self |

### Browser login — OpenAI device code (`flow: "device_code"`)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ST-29 | — (system event) | `oauth-start` returns `flow: "device_code"` | ST-20 completed | Throbber shown: instruction + URL link (new tab) + device code in bold monospace; polling starts | Self + External |
| ST-30 | — (poll event) | Poll returns `connected` | Polling active | Same as ST-27 | Self |
| ST-31 | — (poll event) | Poll returns `error` | Polling active | Same as ST-28 | Self |

### Configured state

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ST-32 | `#test-btn-{id}` (AI card) | Click "Test" button | Provider status = `connected` | `POST /api/connections/:id/test` → spinner → ✓ OK (green) or ✗ Failed (red) | Async |
| ST-33 | `button[onclick*="expandKey"]` (AI card, configured) | Click "Update key" button | Provider status = `connected` | Expands `#key-input-{id}` for replacement | Self |
| ST-34 | `button[onclick*="toggleConfirm"]` (AI card) | Click "Remove" link | Provider status = `connected` | Opens inline confirmation popover | Self |
| ST-35 | `button[onclick*="doDisconnect"]` (AI card) | Click "Remove" confirm | Popover is open | `DELETE /api/connections/:id` → card re-renders as not configured | Async |
| ST-36 | `button[onclick*="closeConfirm"]` (AI card) | Click "Cancel" in popover | Popover is open | Closes popover; no change | Self |

---

## Multiple cards open guard

Only one API key input form and one confirmation popover can be open at a time. Opening a second one collapses any currently open form/popover.

---

## Precondition summary for connection operations

| Operation | Platform credential required |
|---|---|
| Medium — OAuth | Active Medium account; OAuth app approved |
| Medium — token | Medium integration token (Settings → Security → Integration tokens) |
| Hashnode — token | Hashnode personal access token (Account → Developer) |
| Dev.to — token | Dev.to API key (Settings → Extensions) |
| Anthropic (Claude) — browser login | Active Claude account; CLI runner running with `claude` binary available |
| Anthropic (Claude) — key | Anthropic Console API key |
| OpenAI (Codex) — browser login | Active OpenAI account; CLI runner running with `codex` binary available; subject to device code rate limits (~15 min cooldown on 429) |
| OpenAI (Codex) — key | OpenAI platform API key |
