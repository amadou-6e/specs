# Import Article — State Diagram

Two modes share the same screen. Mode is set on entry via query param and does not change during the session.

---

## Diagram

```mermaid
flowchart TD
    ENTRY([Entry — ?mode=platform or ?mode=upload])

    subgraph PLATFORM ["Platform mode"]
        PP[Step 1: Platform picker\nPlatformPickerGrid]
        DL[Step 2: Draft list\nDraftList]
        PR_P[Step 3: Review\nDraftReviewPane]
    end

    subgraph UPLOAD ["Upload mode"]
        FD[Step 1: File drop zone\nFileDropZone]
        PR_U[Step 2: Review\nDraftReviewPane]
    end

    IMPORTING[Importing\nPOST /api/articles/import\nImportProgressOverlay]
    DONE([Editor\n/screens/editor/v1.html?id=])
    CANCEL([Return — ?returnTo target])
    ERR[Error banner\non Review step]

    ENTRY -->|mode=platform| PP
    ENTRY -->|mode=upload| FD

    PP -->|platform selected, Next| DL
    PP -->|Cancel| CANCEL

    DL -->|draft selected, Next| PR_P
    DL -->|Back| PP
    DL -->|Cancel| CANCEL

    PR_P -->|Import clicked| IMPORTING
    PR_P -->|Back| DL
    PR_P -->|Cancel| CANCEL

    FD -->|valid .md dropped or picked| PR_U
    FD -->|invalid file| FD
    FD -->|Cancel| CANCEL

    PR_U -->|Import clicked| IMPORTING
    PR_U -->|Cancel| CANCEL

    IMPORTING -->|201 ok| DONE
    IMPORTING -->|4xx/5xx| ERR

    ERR -->|Try again| PR_P
    ERR -->|Try again — upload path| PR_U
```

---

## State summary

| State | Description |
|-------|-------------|
| Platform picker | Connected platform cards. Next activates when a platform is selected. Disconnected platforms are non-selectable. |
| Draft list | Paginated draft rows for selected platform. Next activates when a draft row is selected. Load more appends rows. |
| Review (platform) | Title (editable), word count, source label, markdown preview. Import fires the POST. |
| File drop zone | Drag-and-drop or click-to-browse. Accepts `.md` only. Invalid type stays in this state with an error. |
| Review (upload) | Same layout as Review (platform). Title pre-filled from first `# heading`. |
| Importing | POST /api/articles/import in-flight. Overlay shown. All actions disabled. |
| Error | Inline banner above footer. Try again re-arms the Import button. Cancel still works. |
| Done | Navigation to editor. Screen is unmounted. |
| Cancel | Navigation to `returnTo` target (overview or create-article). |

---

## returnTo routing

| Entry URL param | Cancel navigates to |
|-----------------|---------------------|
| `returnTo=overview` | `/screens/overview/v3.html` |
| `returnTo=create-article` | `/screens/create-article/v1.html` |
| (missing) | `/screens/overview/v3.html` (default fallback) |
