# Import Article — Components Spec

---

## ModeHeader

Displays the screen title and, in platform mode, a step breadcrumb.

### Props
- `mode: 'platform' | 'upload'`
- `step: 1 | 2 | 3` (platform mode) or `1 | 2` (upload mode)

### Variants
- Platform mode: title + horizontal step breadcrumb (1. Choose platform > 2. Select draft > 3. Review)
- Upload mode: title only, no breadcrumb

Completed steps are dimmed. Active step is highlighted. Future steps are muted.

---

## PlatformPickerGrid

Step 1 of platform mode. Shows all platforms from `GET /api/connections`.

### Card anatomy
```
┌─────────────────────────────┐
│  [logo]  Medium             │
│          12 drafts          │
└─────────────────────────────┘
```

### Props per card
- `platform: string`
- `logo: string` (SVG or img src)
- `draftCount: number | null` (null = not yet fetched)
- `connected: boolean`

### States
- Default
- Hover: border brightens
- Selected: accent border, background tint, checkmark badge
- Disabled (disconnected): reduced opacity, "Connect in Settings" tooltip on hover

Empty state (no connected platforms): full-width message with link to `/screens/settings/v2.html?tab=platforms`.

---

## DraftList

Step 2 of platform mode. Paginated list of drafts for the selected platform.

### Row anatomy
```
┌─────────────────────────────────────────────────┐
│  Title of the draft                    1,200 w  │
│  Updated 3 days ago                             │
└─────────────────────────────────────────────────┘
```

### Props
- `drafts: Draft[]`
  - `id: string`
  - `title: string`
  - `wordCount: number`
  - `updatedAt: string` (relative)
- `selectedId: string | null`
- `hasMore: boolean`
- `loading: boolean`

### States
- Default row
- Hover: background lift
- Selected: left accent bar, background tint
- Loading: skeleton rows (3 placeholders)
- Empty: "No drafts found on this platform"

Load more: "Load more" button at bottom of list, hidden when `hasMore` is false.

---

## DraftReviewPane

Step 3 (platform) and Step 2 (upload). Shows a read-only preview of the content to be imported.

### Anatomy
```
┌─────────────────────────────────────────────────┐
│  [editable title input]                         │
│  1,200 words · Imported from Medium             │
│  ─────────────────────────────────────────────  │
│  [markdown preview — max 480px scrollable]      │
└─────────────────────────────────────────────────┘
```

### Props
- `title: string` (editable inline)
- `wordCount: number`
- `sourceLabel: string` (e.g. "Medium draft" or "Local file — article.md")
- `markdownBody: string`

### Notes
- Title field is a plain text input, not a heading element. It pre-fills from draft title or first `# heading` in uploaded file.
- Markdown preview renders basic formatting only (headings, bold, italic, lists, code blocks). No embeds.
- Preview is read-only.

---

## FileDropZone

Step 1 of upload mode. Accepts `.md` files via drag-and-drop or click-to-browse.

### States
- Idle: dashed border, centered icon + "Drop your .md file here or click to browse"
- Drag over: solid accent border, background tint, label changes to "Release to upload"
- Error: red border, inline error message (e.g. "Only .md files are accepted")
- Processed: success state collapses into a small file chip; screen advances to Review

### Props
- `onFile: (file: File) => void`
- `error: string | null`

### Notes
- File is parsed client-side (no upload at this step).
- `FileReader.readAsText` extracts content.
- Title is extracted from first `# ` line; word count is a simple split on whitespace.

---

## FooterActionBar

Fixed bottom bar with cancel, back, and primary action.

### Props
- `onCancel: () => void`
- `onBack: (() => void) | null` (null hides the Back button)
- `primaryLabel: string`
- `primaryDisabled: boolean`
- `onPrimary: () => void`
- `loading: boolean` (shows spinner on primary button, disables all)

### Layout
- Cancel: left-aligned text button
- Back + primary: right-aligned, Back is ghost, primary is solid accent fill

---

## ImportProgressOverlay

Shown while `POST /api/articles/import` is in-flight.

- Full-screen overlay with centered spinner and label "Importing article..."
- Not dismissable by the user.
- On success: overlay fades, navigation fires.
- On error: overlay replaced by inline error banner in the footer.

### Error banner
- Appears above the footer action bar.
- Text: "Import failed — [reason from API]. Try again."
- "Try again" re-enables the Import button and hides the banner.
