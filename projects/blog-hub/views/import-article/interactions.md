# Import Article — Interactions

Source: `screens/import-article/v1.html`

**Type key:**
- **Self** — stays on view, no navigation
- **Navigate** — moves to another view
- **Async** — fires API call; result reflected on same view
- **External** — opens new tab

---

## Global preconditions

The import view is reached from the Overview split-button dropdown with a `?mode=` query param (`platform` or `upload`). The URL also carries an optional `?returnTo=overview` for post-import back-navigation.

The wizard has two step slots:
1. **Select source** — pick a platform + article (platform mode) OR upload a `.md` file (upload mode)
2. **Review & confirm** — preview the article; edit title; click "Import ✦" to create it in blog-hub

`#primary-btn` is disabled until a valid selection is made in each step.

---

## Navigation bar

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| IM-01 | `a[href*="overview"]` | Click "Articles" nav link | — | → Overview | Navigate |
| IM-02 | `a[href="#"]:has-text("Queue")` | Click "Queue" nav link | — | → Publish Queue view | Navigate |
| IM-03 | `a[href*="settings"]` (nav bar) | Click "Settings" nav link | — | → Settings view | Navigate |

---

## Step indicator (read-only)

The `#step-bar` / `#step-indicator` dots are visual-only and not interactive.

---

## Step 1 — Platform mode (`#view-platform-pick`)

Visible when `?mode=platform` OR after user navigates back from review.

### No connected platforms state

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| IM-04 | `a[href*="settings"]:has-text("Open Settings")` | Click "Open Settings" link | `#no-platforms` is visible (no connected platforms) | → Settings / Platforms tab | Navigate |

### Platform grid

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| IM-05 | `.platform-card:not(.disconnected)` | Click a connected platform card | Platform status = `connected` | Card gets `.selected` class; `#view-draft-list` slides in; `GET /api/connections/:id/articles` (or equivalent) fetches drafts; `#primary-btn` stays disabled until an article is selected | Self → Async |
| IM-06 | `.platform-card.disconnected` | Click a disconnected platform card | Platform status = `disconnected` | No-op (cursor `not-allowed`; interaction blocked) | Self |

---

## Step 1 — Draft list (`#view-draft-list`, after platform selected)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| IM-07 | `#draft-search` | Type in article search box | `#view-draft-list` is visible | `setDraftSearch(value)`: filters `.draft-row` list live | Self |
| IM-08 | `#pill-all` | Click "All" filter pill | — | Shows both `draft` and `published` rows; `#pill-all` gets `active` class | Self |
| IM-09 | `#pill-draft` | Click "Draft" filter pill | — | Shows only rows with `.draft-badge.draft`; `#pill-draft` gets `active` | Self |
| IM-10 | `#pill-published` | Click "Published" filter pill | — | Shows only rows with `.draft-badge.published` | Self |
| IM-11 | `.draft-row` | Click an article row | `#view-draft-list` visible; row is not already selected | Row gets `.selected` class; `#primary-btn` becomes enabled | Self |
| IM-12 | `.draft-row.selected` | Click selected article row | Row is already `.selected` | Row remains selected (no deselect on re-click) | Self |
| IM-13 | `#load-more-wrap button` ("Load more") | Click "Load more" | `#load-more-wrap` is visible (more articles available) | `loadMore()`: fetches next page; new rows appended to `#draft-rows` | Async |

---

## Step 1 — Upload mode (`#view-upload`)

Visible when `?mode=upload` OR when user navigates back from review after an upload.

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| IM-14 | `#drop-zone` (click) | Click drop zone | `#dz-idle` is shown | `triggerFilePicker()` → `#file-input` click → OS file picker (`.md` only) | Self |
| IM-15 | `#file-input` (programmatic) | Drop `.md` file onto `#drop-zone` | `#dz-idle` is shown | `dragover` + `drop` events handled; file loaded; `#dz-hover` shown during drag; on drop: file parsed; `#view-review` shown; `#primary-btn` enabled | Self |
| IM-16 | `#drop-zone` | Drag `.md` over drop zone | Any drag state | `#drop-zone` gets `.drag-over` class (indigo border) while pointer is over zone | Self |
| IM-17 | `button[onclick*="resetDropZone"]` ("Try again") | Click "Try again" in error state | `#dz-error` is shown | `resetDropZone()`: clears error; resets to `#dz-idle` state; `#primary-btn` disabled again | Self |

---

## Step 2 — Review panel (`#view-review`)

Reached after selecting an article (platform mode) or loading a file (upload mode).

### Single-article review (`#review-single`)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| IM-18 | `#title-input` | Edit article title | `#review-single` is visible | `syncTitle(value)`: updates internal state; affects the title used on import | Self |
| IM-19 | `#markdown-preview a[target="_blank"]` | Click a link inside the markdown preview | Preview has rendered links | Opens link URL in new tab | External |

### Multi-article review (`#review-multi`)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| IM-20 | `#review-article-list .draft-row` | Click an article row in multi-article review | `#review-multi` is visible | Selects/deselects article for import; updates `#primary-btn` state | Self |

---

## Error banner (`#error-banner`)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| IM-21 | `button[onclick*="retryImport"]` ("Try again") | Click "Try again" in error banner | `#error-banner` is visible (import API call failed) | `retryImport()`: re-fires import request; banner hides; overlay shown | Async |

---

## Action bar (`#action-bar`) — persistent footer

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| IM-22 | `#back-btn` | Click "← Back" | Any step | `goBack()`: returns to previous step (step 2 → step 1; step 1 → Overview) | Self / Navigate |
| IM-23 | `#startover-btn` | Click "↺ Start over" | `#startover-btn` is visible (step 2) | `doStartOver()`: resets to step 1 initial state; clears selection; `#startover-btn` hides | Self |
| IM-24 | `#primary-btn` ("Next →" / "Import ✦") | Click "Next →" (step 1) | `#primary-btn` is enabled (article selected or file loaded) | `advance()`: advances to step 2; label changes to "Import ✦"; `#startover-btn` shown | Self |
| IM-25 | `#primary-btn` ("Import ✦") | Click "Import ✦" (step 2) | `#primary-btn` is enabled; article is confirmed | `advance()`: `POST /api/articles/import` with selected article data → 202; `#import-overlay` shown; on success → Editor with `?id={article.id}` | Async → Navigate |

---

## Import overlay (`#import-overlay`)

The overlay is displayed during the import API call. It has no interactive elements — it is purely a loading indicator that resolves automatically when the `POST` completes.

---

## Step indicator dot semantics

| Dot state | Visual | Meaning |
|---|---|---|
| `inactive` | Small grey rounded rect | Step not yet reached |
| `active` | Wider indigo rounded rect | Current step |
| `done` | Small indigo rounded rect | Step completed |
