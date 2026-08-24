# Overview — Interactions

Source: `screens/overview/v3.html`

**Type key:**
- **Self** — stays on view, no navigation
- **Navigate** — moves to another view
- **Async** — fires API call + polls job on same view; spinner/status shown in panel
- **External** — opens new tab

---

## Global precondition

The overview view loads with no authentication gate. All filter and search operations are available immediately. Operations that require a selected article are disabled (buttons absent or inert) when no article is selected.

The nav bar is present on every screen. OV-01 through OV-05 cover all nav bar elements; the same elements appear verbatim on Create-article, Editor, Settings, and Import-article screens.

---

## Navigation bar

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| OV-01 | `#nav-articles` | Click "Articles" nav button | — | Active tab (no-op, already on view); `#nav-articles` border-bottom becomes indigo | Self |
| OV-02 | `#nav-queue` | Click "Queue" nav button | — | → Publish Queue view | Navigate |
| OV-03 | `#nav-settings` | Click "Settings" nav button | — | → Settings view | Navigate |
| OV-04 | `.split-left` (New Article button) | Click "New Article" | — | → Create Article wizard (`screens/create-article/v1.html`) | Navigate |
| OV-05 | `#create-menu-btn` | Click split-button chevron (▾) | — | Toggles `#import-menu` dropdown open/closed | Self |
| OV-06 | `#import-menu button:nth-child(1)` | Click "Import from platform" (inside dropdown) | `#import-menu` is open | → Import Article view with `?mode=platform` | Navigate |
| OV-07 | `#import-menu button:nth-child(2)` | Click "Upload .md file" (inside dropdown) | `#import-menu` is open | → Import Article view with `?mode=upload` | Navigate |

---

## Filter bar

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| OV-08 | `#search-input` | Type in search box | — | `applyFilters()` on each input; article list re-renders to matches | Self |
| OV-09 | `#sf-all` | Click "All" status filter | — | Removes status filter; all articles shown; pill gets `active` class | Self |
| OV-10 | `#sf-drafting` | Click "Drafting" status filter | — | Shows only drafting articles; pill gets `active` class | Self |
| OV-11 | `#sf-ready` | Click "Ready" status filter | — | Shows only ready articles | Self |
| OV-12 | `#sf-error` | Click "Error" status filter | — | Shows only articles with errors | Self |
| OV-13 | `#sf-published` | Click "Published" status filter | — | Shows only published articles | Self |
| OV-14 | `#pf-medium` | Click "Medium" platform filter | — | Toggles Medium platform filter on/off; pill border toggles indigo | Self |
| OV-15 | `#pf-hashnode` | Click "Hashnode" platform filter | — | Toggles Hashnode filter | Self |
| OV-16 | `#pf-devto` | Click "Dev.to" platform filter | — | Toggles Dev.to filter | Self |

---

## Article table

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| OV-17 | `.article-card` | Click article row | — | Row gets `.selected` class (indigo border/bg); Side Panel opens with article detail | Self |
| OV-18 | `.article-card` (other) | Click a different row | A row is already `.selected` | Previous `.selected` removed; new row selected; Panel updates | Self |
| OV-19 | `.plat-tab` inside card | Click platform destination pill | Destination has a URL | Opens destination URL in new tab | External |
| OV-20 | `.gate-badge` inside card | Click gate badge (Pass/Warn/Fail) | Article has a gate result (not `pending`) | → Inspection view for this article | Navigate |
| OV-21 | `.ctx-trigger` button | Click ⋯ context menu button | — | Context menu appears with Edit / Duplicate / Archive / Delete options | Self |
| OV-22 | `.ctx-item:nth-child(1)` ("Edit") | Click "Edit" in context menu | Context menu is open | → Editor view with `?id={article.id}` | Navigate |
| OV-23 | `.ctx-item:nth-child(2)` ("Duplicate") | Click "Duplicate" in context menu | Context menu is open | Duplicates article; article list reloads | Async |
| OV-24 | `.ctx-item:nth-child(3)` ("Archive") | Click "Archive" in context menu | Context menu is open | Archives article; article removed from active list | Async |
| OV-25 | `.ctx-item.danger` ("Delete") | Click "Delete" in context menu | Context menu is open | Deletes article; article removed from list | Async |

---

## Empty-state actions (shown only when no articles match)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| OV-26 | `button[onclick*="clearFilters"]` | Click "Clear filters" | Empty-state row is shown | Resets `q`, status (`all`), platform (`null`); `applyFilters()` reruns | Self |
| OV-27 | `button[onclick*="create-article"]` (empty state) | Click "+ New article" in empty state | Empty-state row is shown | → Create Article wizard | Navigate |

---

## Side strip

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| OV-28 | `#side-strip` | Click collapse/expand strip | — | Toggles details panel open/closed; strip arrow flips | Self |

---

## Side panel (opens when an article is selected)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| OV-29 | `button[onclick*="deselectCard"], .panel-close` | Click "×" close button | Panel is open | Calls `deselectCard()`; deselects article; hides panel | Self |
| OV-30 | `#panel-primary-btn` | Click primary action button ("Push drafts" / "Resume" etc.) | Article is selected; at least one destination must be connected | `POST /api/articles/:id/push` → 202 → polls job; on completion reloads list and refreshes panel | Async |
| OV-31 | `button[onclick*="runArticleAction"]` ("Inspect") | Click "Inspect" button in panel | Article is selected | `POST /api/articles/:id/inspect` → 202 → polls job; on completion reloads article list | Async |
| OV-32 | `button[onclick*="Edit"]` (in panel) | Click "Edit" button in panel | Article is selected | → Editor view with `?id={article.id}` | Navigate |
| OV-33 | `button:has-text("Schedule")` (in panel) | Click "Schedule" button in panel | Article is selected | → Publish Queue view with article pre-selected | Navigate |
| OV-34 | `#panel-inspect-btn` | Click "Inspect" icon button in panel footer | Article is selected | Same as OV-31 | Async |

### Precondition detail for OV-16 (Push drafts)

- Medium: user must have connected their Medium account (OAuth or integration token) in Settings / Platforms.
- Hashnode: valid Hashnode personal access token saved in Settings / Platforms.
- Dev.to: valid Dev.to API key saved in Settings / Platforms.
- If none of the selected article's destinations have a connected platform, the push completes but produces no published output (server-side behaviour, not blocked by the UI).

---

## Job polling (after OV-16 or OV-17)

| ID | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|
| OV-18 | Job status becomes `done` | Polling interval active | Clears interval; reloads article list; refreshes panel if article still selected | Self |
| OV-19 | Job status becomes `error` | Polling interval active | Clears interval; reloads article list; panel shows error state | Self |
