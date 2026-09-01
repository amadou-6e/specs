# Import Article — UI Tests

> Test authority: [import-article.drawio](import-article.drawio). Tests project its
> represented states and `IM-*` transitions; they must not create new UI requirements.

---

## Platform mode

### IA-P-01 — Navigate to platform mode from Overview dropdown
1. From Overview, open the "New Article" split button dropdown.
2. Click "Import from platform".
3. Expect: navigation to `/screens/import-article/v1.html?mode=platform&returnTo=overview`.
4. Expect: ModeHeader shows "Import Article" with step breadcrumb at step 1.
5. Expect: PlatformPickerGrid shows all connected platforms.

### IA-P-02 — Disabled state for disconnected platform
1. Arrive at platform mode with one platform disconnected.
2. Hover over the disconnected platform card.
3. Expect: card is visually reduced (opacity), hover shows "Connect in Settings" tooltip.
4. Click the disconnected card.
5. Expect: no selection happens, no state change.

### IA-P-03 — Select platform and advance to draft list
1. Click a connected platform card.
2. Expect: card gains accent border and checkmark.
3. Expect: footer "Next" button activates.
4. Click "Next".
5. Expect: step breadcrumb advances to step 2.
6. Expect: DraftList shows drafts for the selected platform (or skeleton while loading).

### IA-P-04 — Empty draft list
1. Select a platform that returns 0 drafts.
2. Expect: DraftList shows "No drafts found on this platform" empty state.
3. Expect: footer "Next" remains disabled.

### IA-P-05 — Load more drafts
1. Platform returns more than the initial page of drafts.
2. Expect: "Load more" button visible at bottom of list.
3. Click "Load more".
4. Expect: additional drafts append to the list without replacing existing rows.
5. When no more drafts remain: "Load more" button disappears.

### IA-P-06 — Select draft and advance to review
1. Click a draft row.
2. Expect: row gains accent left bar and background tint.
3. Expect: footer "Next" activates.
4. Click "Next".
5. Expect: step breadcrumb advances to step 3.
6. Expect: DraftReviewPane shows title (pre-filled from draft title), word count, source label, markdown preview.

### IA-P-07 — Edit title before importing
1. On the Review step, click the title field.
2. Clear the text and type a new title.
3. Click "Import".
4. Expect: the article is created with the edited title (not the original draft title).

### IA-P-08 — Import success, navigate to editor
1. On the Review step, click "Import".
2. Expect: ImportProgressOverlay appears.
3. API responds 201 with `{ id, title }`.
4. Expect: navigation fires to `/screens/editor/v1.html?id=<id>`.

### IA-P-09 — Import failure, retry
1. On the Review step, click "Import".
2. API responds 500.
3. Expect: overlay replaced by error banner above footer.
4. Click "Try again".
5. Expect: error banner hides, Import button re-enables.

### IA-P-10 — Back navigation between steps
1. On step 2 (draft list), click "Back".
2. Expect: returns to step 1 (platform picker). Previously selected platform is still highlighted.
3. On step 3 (review), click "Back".
4. Expect: returns to step 2. Previously selected draft is still highlighted.

### IA-P-11 — Cancel from platform mode, returnTo=overview
1. Arrive via `?mode=platform&returnTo=overview`.
2. Click "Cancel" in the footer (or Zone A Cancel button).
3. Expect: navigation to `/screens/overview/v3.html`.

### IA-P-12 — Cancel from platform mode, returnTo=create-article
1. Arrive via `?mode=platform&returnTo=create-article`.
2. Click "Cancel".
3. Expect: navigation to `/screens/create-article/v1.html`.

---

## Upload mode

### IA-U-01 — Navigate to upload mode from Overview dropdown
1. From Overview, open the split button dropdown.
2. Click "Upload .md".
3. Expect: navigation to `/screens/import-article/v1.html?mode=upload&returnTo=overview`.
4. Expect: ModeHeader shows "Import Article" with no step breadcrumb.
5. Expect: FileDropZone is shown in idle state.

### IA-U-02 — Upload valid .md file via click
1. Click the FileDropZone.
2. Select a `.md` file in the file picker.
3. Expect: file parses client-side, screen advances to Review.
4. Expect: title pre-filled from first `# heading`. Word count computed.

### IA-U-03 — Upload valid .md file via drag-and-drop
1. Drag a `.md` file over the FileDropZone.
2. Expect: drop zone border changes to solid accent, label changes to "Release to upload".
3. Drop the file.
4. Expect: same outcome as IA-U-02.

### IA-U-04 — Reject non-.md file
1. Drop a `.pdf` or `.txt` file on the FileDropZone.
2. Expect: drop zone shows red border and inline error "Only .md files are accepted".
3. Expect: no navigation to Review step.

### IA-U-05 — File without a heading
1. Upload a `.md` file that has no `# heading` on the first line.
2. Expect: title field is pre-filled with the filename (without extension).
3. Expect: word count is still computed from the full content.

### IA-U-06 — Edit title before importing (upload mode)
Same as IA-P-07 but for upload mode.

### IA-U-07 — Import success (upload mode)
Same flow as IA-P-08 but `POST /api/articles/import` body uses `source: "upload"`.

### IA-U-08 — Cancel from upload mode, returnTo=overview
1. Arrive via `?mode=upload&returnTo=overview`.
2. Click "Cancel".
3. Expect: navigation to `/screens/overview/v3.html`.

---

## Edge cases

### IA-E-01 — Missing mode param
1. Navigate to `/screens/import-article/v1.html` with no `mode` param.
2. Expect: screen shows a mode selection step (or defaults to `mode=platform`). Does not crash.

### IA-E-02 — No connected platforms in platform mode
1. Arrive at `mode=platform` with zero connected platforms.
2. Expect: PlatformPickerGrid shows "No platforms connected" empty state with link to Settings.
3. Expect: footer "Next" is disabled.

### IA-E-03 — Import in-flight, user attempts to cancel
1. Click "Import". Overlay appears.
2. Attempt to click the Cancel button.
3. Expect: Cancel is disabled during the in-flight API call.
