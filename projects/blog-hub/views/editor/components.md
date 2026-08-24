# Editor — Components Spec

---

## EditorPane

The main content editing surface.

### Props
- `articleId: string`
- `content: string` (markdown)
- `mode: 'write' | 'review'`
- `patches: Patch[]`
- `comments: Comment[]`
- `onChange: (content: string) => void`

### Behaviour
- Renders markdown with inline rich preview (headings, code blocks, images styled)
- In Review mode: highlights anchored comment ranges (amber underline)
- In Review mode: highlights patched ranges (green/red diff background)
- Autosaves on change with 2s debounce; top nav shows unsaved dot until confirmed

---

## Toolbar

### Write mode actions
- Bold, Italic, Inline code, Heading (H2/H3 dropdown), Blockquote, Code block, Link, Image upload

### Review mode actions
- Add Comment (activates text selection mode; selected text becomes a comment anchor)
- Clear resolved comments

### Mode toggle
- Two-segment control: Write / Review
- Sits on the right side of the toolbar

---

## CommentThread (in margin panel)

One thread per anchored comment.

### Props
- `comment: Comment` — id, author, text, resolved, anchor range, replies
- `onReply: (text: string) => void`
- `onResolve: () => void`
- `onRequestAiFix: () => void`

### States
- Open: full thread visible
- Resolved: collapsed with "Resolved" label, can be expanded
- AI fix pending: spinner shown instead of reply input

### Behaviour
- Hovering a thread highlights the corresponding text in the editor
- "Fix with AI" button sends the comment text + anchored content to the AI patch endpoint
- After AI fix is applied, thread shows "Patch ready — review below"

---

## AIPatchPreview (in margin panel)

Shows a pending AI-generated patch for review.

### Props
- `patch: Patch` — id, original text, replacement text, comment_id reference
- `onAccept: () => void`
- `onReject: () => void`

### Behaviour
- Shows unified diff: red lines removed, green lines added
- Accept replaces the editor content at the anchored range
- Reject discards the patch; the comment remains open
- Only one patch can be accepted or rejected at a time (no batch accept in v1)

---

## DestinationsPanel (in margin panel)

Compact view of per-platform draft state.

### Props
- `destinations: DestinationStatus[]`

### Per destination row
- Platform name + status pill
- If draft exists: link to draft URL
- If error: short reason text + "Retry" link
- "Run inspection" button (navigates to /inspect/:id)

---

## GenerationProgressOverlay

Shown on top of the editor while the initial AI generation job is running.

### Props
- `jobId: string`
- `onComplete: (content: string) => void`
- `onError: (reason: string) => void`

### States
- Running: spinner + "Generating your article…" + progress stages (Outlining, Writing, Reviewing)
- Error: error message + Retry and Start over buttons

### Behaviour
- Polls /jobs/:job_id every 2 seconds
- On done: dismisses overlay and populates editor with generated content
- Does not block the user from navigating away (warns with a confirmation prompt)

---

## UnsavedIndicator

A small dot in the top nav next to the article title.

- Amber dot: unsaved changes
- No dot: saved
- Spinning ring: save in flight
