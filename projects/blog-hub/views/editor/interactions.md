# Editor — Interactions

Source: `screens/editor/v2.html`

**Type key:**
- **Self** — stays on view, no navigation
- **Navigate** — moves to another view
- **Async** — fires API call; result reflected on same view
- **External** — opens new tab

---

## Global preconditions

The editor loads an article by `?id=` URL parameter. All interactions below assume the article is loaded. Write mode is the default on load.

---

## Navigation bar

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-01 | `button[onclick*="location.href"][onclick*="overview"]` | Click "←" back-to-overview icon button | — | → Overview (`screens/overview/v3.html`) | Navigate |
| ED-02 | `#article-title` (contenteditable) | Edit article title inline | — | Title updates; `#save-indicator` shows amber dot; autosave fires `PATCH /api/articles/:id` after 2 s inactivity | Async |
| ED-03 | `.nav-btn.accent` ("Review") | Click "Review" button (top bar) | — | `showReview()`: switches to Review mode; `#gen-overlay` shown | Self |
| ED-04 | `.nav-btn:not(.accent)` ("Inspect") | Click "Inspect" button (top bar) | — | `triggerInspect()` → Inspection view for current article | Navigate |
| ED-05 | `button:has-text("Publish")` | Click "Publish" button (top bar) | — | Opens publish flow (platform confirmation); `POST /api/articles/:id/publish` | Async |

---

## AI strip (toolbar row 1 — always visible)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-06 | `.ai-btn.hl` ("Regenerate") | Click "Regenerate" in AI strip | — | `showReview()`: `#gen-overlay` shown with regeneration progress | Self |
| ED-07 | `.ai-btn[onclick*="patches"]` ("View Diff") | Click "View Diff" in AI strip | — | `openSection('patches')`: Patches accordion expands in left panel | Self |
| ED-08 | `.ai-btn:not([onclick])` ("Revert") | Click "Revert" in AI strip | — | Reverts article content to last saved version | Self |
| ED-09 | `.ai-btn[onclick*="chat"]` ("Chat") | Click "Chat" in AI strip | — | `openSection('chat')`: Chat accordion expands in left panel | Self |
| ED-10 | `.ai-btn[onclick*="rules"]` ("Rules") | Click "Rules" in AI strip | — | `openSection('rules')`: Rules accordion expands in left panel | Self |

---

## Format toolbar (toolbar row 2)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-11 | `.icon-btn[title="Bold"]` | Click Bold button | Text selected in `#raw-editor` | Wraps selection with `**…**` markdown | Self |
| ED-12 | `.icon-btn[title="Italic"]` | Click Italic button | Text selected | Wraps selection with `*…*` | Self |
| ED-13 | `.icon-btn[title="Code"]` | Click Code button | Text selected | Wraps selection with `` `…` `` | Self |
| ED-14 | `.icon-btn[title="H2"]` | Click H2 button | Cursor in editor | Prefixes current line with `## ` | Self |
| ED-15 | `.icon-btn[title="H3"]` | Click H3 button | Cursor in editor | Prefixes current line with `### ` | Self |
| ED-16 | `.icon-btn[title="Blockquote"]` | Click Blockquote button | Cursor in editor | Prefixes current line with `> ` | Self |
| ED-17 | `.icon-btn[title="Link"]` | Click Link button | Text selected | Wraps selection with `[…](url)` template | Self |
| ED-18 | `.icon-btn[title="Image"]` | Click Image button | Cursor in editor | Inserts `![alt](url)` template at cursor | Self |
| ED-19 | `.ai-btn.warn[onclick*="insertCommentCmd"]` | Click "+ Comment" in toolbar | — | `insertCommentCmd()`: inserts `/comment ` at cursor; opens comment thread in left panel | Self |

---

## Selection popover (appears when text is selected)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-20 | `#sel-popover .sp-btn[onclick*="selFormat('**')"]` | Click B (Bold) in popover | Text selected; `#sel-popover` visible | Wraps selection with `**…**` | Self |
| ED-21 | `#sel-popover .sp-btn[onclick*="selFormat('*')"]` | Click I (Italic) in popover | Text selected; `#sel-popover` visible | Wraps selection with `*…*` | Self |
| ED-22 | `#sel-popover .sp-btn[onclick*="selFormat('\`')"]` | Click `code` in popover | Text selected; `#sel-popover` visible | Wraps selection with `` `…` `` | Self |
| ED-23 | `#sel-popover .sp-btn.sp-accent` ("Add comment") | Click "Add comment" in popover | Text selected; `#sel-popover` visible | `addCommentFromSel()`: underlines selection amber; new comment thread in left panel | Self |

---

## Editor body

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-24 | `#raw-editor` | Type in editor textarea | — | `onInput()`: `#save-indicator` amber dot; autosave `PATCH /api/articles/:id` after 2 s inactivity; dot clears on success | Async |
| ED-25 | `#raw-editor` | Type `/comment your_note` on new line | — | `insertCommentCmd()` at cursor; comment thread opens | Self |

---

## Generation overlay (shown after showReview / Regenerate)

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-26 | `#gen-overlay button[onclick*="finishReview"]` | Click "Done — view patches" | `#gen-overlay` is visible | `finishReview()`: overlay closes; Patches accordion opens in left panel | Self |
| ED-27 | `#gen-overlay button[onclick*="gen-overlay"]` | Click "Dismiss" | `#gen-overlay` is visible | Hides overlay; stays in Review mode | Self |

---

## Left panel — general

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-28 | `#panel-strip` | Click collapse strip (left edge) | — | `toggleLeft()`: left panel collapses; strip arrow reverses | Self |
| ED-29 | `.acc-hdr[onclick*="comments"]` | Click "Comments" accordion header | — | `toggleSection('comments')`: expands / collapses Comments section | Self |
| ED-30 | `.acc-hdr[onclick*="patches"]` | Click "Patches" accordion header | — | `toggleSection('patches')`: expands / collapses Patches section | Self |
| ED-31 | `.acc-hdr[onclick*="destinations"]` | Click "Destinations" accordion header | — | `toggleSection('destinations')`: expands / collapses Destinations section | Self |
| ED-32 | `.acc-hdr[onclick*="chat"]` | Click "Chat" accordion header | — | `toggleSection('chat')`: expands / collapses AI Chat section | Self |
| ED-33 | `.acc-hdr[onclick*="rules"]` | Click "Rules" accordion header | — | `toggleSection('rules')`: expands / collapses Style Rules section | Self |

---

## Left panel — Comments section

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-34 | `button[onclick*="generate-patch"]` ("Fix with AI") | Click "Fix with AI" on a comment | `hasPatch = false`; AI provider configured | `POST /api/agent/generate-patch/:articleId/comments/:cid` → 202 → patch in Patches section; button replaced by patch indicator | Async |
| ED-35 | `button[onclick*="resolveComment"]` ("Resolve") | Click "Resolve" on a comment | Comment is open | `POST /api/articles/:id/comments/:cid/resolve` → comment removed from list; collapses with "Resolved" label | Async |

### Precondition detail for ED-34 (Fix with AI)

- An AI provider (Claude or Codex) must be connected in Settings / AI Providers.
- The comment must not already have an associated patch (`hasPatch = false`).

---

## Left panel — Patches section

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-36 | `button[onclick*="acceptPatch"]` | Click "Accept" on a patch | Patch is in `pending` state | `POST /api/patches/:patchId/accept` → replaces editor content at patch range; patch removed from list | Async |
| ED-37 | `button[onclick*="rejectPatch"]` | Click "Reject" on a patch | Patch is in `pending` state | `POST /api/patches/:patchId/reject` → patch removed from list; associated comment stays open | Async |

---

## Left panel — Destinations section

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-38 | `a[href][target="_blank"]` (destination URL) | Click destination URL link (↗) | Destination has a URL | Opens URL in new tab | External |
| ED-39 | `button[style*="f87171"]` ("Retry") | Click "Retry" on a failed destination | Push job failed for platform | Retries `POST /api/articles/:id/push` for that platform only | Async |
| ED-40 | `button[onclick*="triggerInspect"]` (inside destinations) | Click "Inspect" button in Destinations footer | — | `triggerInspect()` → Inspection view | Navigate |

---

## Left panel — Chat section

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-41 | `#chat-input` | Type in chat input | Chat accordion is expanded | Input receives text | Self |
| ED-42 | `button[onclick*="sendChat"]` (↵) | Click send button (↵) or press Enter | `#chat-input` is non-empty | `sendChat()`: `POST /api/agent/chat` with message; response streamed into chat | Async |

---

## Preview pane

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-43 | `#preview-strip` | Click preview strip (right edge) | — | `togglePreview()`: shows / hides markdown preview pane | Self |
| ED-44 | `#preview-sel` | Select platform in preview dropdown | Preview pane is visible | `renderPreview()`: re-renders preview with selected platform's styles | Self |
| ED-45 | `#ext-link` ("visit ↗") | Click "visit ↗" link | Preview pane visible; destination has live URL | Opens published URL in new tab | External |
| ED-46 | `button[onclick*="renderPreview"]` | Click "Reload draft" button | Preview pane is visible | Re-renders markdown from current `#raw-editor` content | Self |

---

## Autosave error states

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| ED-47 | `#save-indicator` | `PATCH /api/articles/:id` fails | Autosave fired | Amber dot stays; tooltip "Save failed — retrying"; next keystroke re-arms debounce | Self |

---

## Future operations (not yet in screen)

| ID | Endpoint | Notes |
|---|---|---|
| ED-48 `@future` | `POST /api/agent/regenerate/:articleId` | Re-run generation on the full article with optional provider override; endpoint exists but no UI trigger in `v2.html` yet |
