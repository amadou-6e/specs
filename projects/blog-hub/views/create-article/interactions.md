# Create Article — Interactions

Source: `screens/create-article/v1.html`

**Type key:**
- **Self** — stays on view, no navigation
- **Navigate** — moves to another view
- **Async** — fires API call + job polling; navigates after completion
- **External** — opens new tab

---

## Global preconditions

The wizard is a 3-step linear flow. The "Next" / "Generate" button is the only forward action; "Back" is always available from steps 2 and 3. The view requires at least one AI provider (Claude or Codex) to be configured in Settings to reach step 3 and generate.

---

## Navigation bar

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| CA-01 | `a[href*="overview"]` | Click "Articles" nav link | — | → Overview | Navigate |
| CA-02 | `a[href="#"]:has-text("Queue")` | Click "Queue" nav link | — | → Publish Queue view | Navigate |
| CA-03 | `a[href*="settings"]` (nav bar) | Click "Settings" nav link | — | → Settings view | Navigate |
| CA-04 | `button[onclick*="doResetWizard"]` | Click "↺ Reset" button | Any step | Resets wizard to Step 1 initial state; clears brief, file, skill, provider, destinations | Self |

---

## Step 1 — Prompt & Context

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| CA-05 | `#prompt-text` | Type in brief textarea | — | Char count updates; `#next-btn` becomes enabled when length > 10 | Self |
| CA-06 | `button[onclick*="loadTemplate('tutorial')"]` | Click "+ Tutorial" template button | — | Fills `#prompt-text` with tutorial brief; overwrites existing content | Self |
| CA-07 | `button[onclick*="loadTemplate('comparison')"]` | Click "+ Comparison" template button | — | Fills `#prompt-text` with comparison brief; overwrites existing content | Self |
| CA-08 | `button[onclick*="saveAsTemplate"]` | Click "Save as template" | `#prompt-text` is non-empty | Saves current textarea content as a named template (local storage) | Self |
| CA-09 | Drop zone div (click) → `#file-input` | Click file drop zone / "browse" link | — | Opens OS file picker filtered to `.md`; triggers `#file-input` click | Self |
| CA-10 | `#file-input` | Drop `.md` file onto drop zone | — | Loads file; shows filename + "×" remove button; brief no longer required to be non-empty | Self |
| CA-11 | `button[onclick*="clearFile"]` | Click "×" on uploaded filename | A context file is loaded | Clears file; drop zone reverts to empty state | Self |
| CA-12 | `#next-btn` | Click "Next" (Step 1) | `#prompt-text` > 10 chars OR a context file is loaded | Advances to Step 2; `#step-2` becomes active | Self |

---

## Step 2 — Configure

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| CA-13 | `.skill-row` (any) | Click a skill row | — | Clicked row gets `.selected`; summary panel updates | Self |
| CA-14 | `#provider-claude` | Click "Claude" provider button | — | Activates Claude; `#provider-codex` deactivates; summary updates | Self |
| CA-15 | `#provider-codex` | Click "Codex" provider button | — | Activates Codex; `#provider-claude` deactivates; summary updates | Self |
| CA-16 | `a[href*="settings?tab=ai"]` (no provider warning) | Click "Add in Settings →" (no provider) | No AI provider configured | → Settings / AI Providers tab | Navigate |
| CA-17 | `input[type="range"]` | Drag word-count slider | — | Word count label updates (500–4000 step 100); summary updates | Self |
| CA-18 | `#back-btn` (Step 2) | Click "Back" | On Step 2 | Returns to Step 1; step indicator updates | Self |
| CA-19 | `#next-btn` (Step 2) | Click "Next" | — | Advances to Step 3; `#step-3` becomes active | Self |

---

## Step 3 — Destinations

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| CA-20 | `#toggle-medium` | Toggle Medium destination on | Medium status = `connected` | Enables Medium as target; track background becomes indigo (`#6366f1`) | Self |
| CA-21 | `#toggle-medium` | Toggle Medium destination off | Medium is currently on | Disables Medium; track background becomes grey | Self |
| CA-22 | `#toggle-hashnode` | Toggle Hashnode destination | Hashnode status = `connected` | Same toggle pattern as CA-20/21 | Self |
| CA-23 | `#toggle-devto` | Toggle Dev.to destination | Dev.to status = `connected` | Same toggle pattern as CA-20/21 | Self |
| CA-24 | `a[href*="settings"]:has-text("Reconnect")` | Click "Reconnect" on an expired platform | Platform status = `expired` | → Settings / Platforms tab | Navigate |
| CA-25 | `a[href*="settings"]:has-text("Add in Settings")` (Step 3) | Click "Add in Settings" on a disconnected platform | Platform status = `disconnected` | → Settings / Platforms tab | Navigate |
| CA-26 | `#back-btn` (Step 3) | Click "Back" | On Step 3 | Returns to Step 2 | Self |
| CA-27 | `#next-btn` (Step 3 — "Generate ✦") | Click "Generate ✦" | ≥1 destination toggled on; ≥1 AI provider configured; brief has content or context file loaded | `POST /api/agent/generate {brief, skill, provider, wordCount, destinations[]}` → 202 + `jobId`; spinner shown; button + back disabled; polls `GET /api/jobs/:jobId`; on `done` → Editor with `?id={article.id}` | Async → Navigate |
| CA-28 | `button[onclick*="startGeneration"]` ("Retry") | Click "Retry" in generation-error state | Generation job has failed | Re-fires `POST /api/agent/generate` with same parameters | Async |

### Precondition detail for CA-27 (Generate)

- **AI provider**: the selected provider must have a valid API key or OAuth token in Settings / AI Providers. The UI disables Generate and shows a warning if none is configured.
- **Destinations**: at least one destination must be toggled on. Disconnected platform cards are shown locked and cannot be toggled.
- **Brief**: the prompt textarea must contain more than 10 characters OR a `.md` context file must be loaded.

---

## Summary panel (right rail, visible from Step 2 onwards)

The summary panel is read-only and updates reactively as the user changes selections. It has no interactive elements of its own.
