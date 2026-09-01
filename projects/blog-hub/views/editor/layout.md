# Editor — Layout Spec

> UI authority: [editor.drawio](editor.drawio). This layout is a derived reading aid, not
> an independent source of UI behavior.

## Purpose
The core writing surface. The user reads, edits, and requests AI revisions on a generated or manually created article.

---

## Page Zones

```
┌──────────────────────────────────────────────────────────────────┐
│  ZONE A: Top nav (fixed, 48px) — article title + status          │
├──────────────────────────────────────────────────────────────────┤
│  ZONE B: Toolbar (sticky, 40px) — mode toggle + format actions   │
├────────────────────────────────┬─────────────────────────────────┤
│                                │                                 │
│  ZONE C: Editor pane           │  ZONE D: Margin panel           │
│  (scrollable, flex-1)          │  (sticky top, 320px, scrollable)│
│                                │                                 │
│  Article content here.         │  Comments, AI patches,          │
│                                │  destination state              │
│                                │                                 │
└────────────────────────────────┴─────────────────────────────────┘
```

Split: Zone C takes remaining width minus 320px margin panel. Minimum editor width: 560px.
On tablet (<1024px): Zone D collapses into a slide-in drawer triggered by a Comments button in Zone B.

---

## Two Modes

### Write mode
- Zone D is hidden (full-width editor)
- Toolbar shows formatting actions only
- Distraction-free: only the editor and the top nav visible

### Review mode
- Zone D is visible
- Toolbar shows comment and AI-action controls
- In-editor comment anchors are visible (highlighted text with indicator)

Mode toggle is a two-state control in Zone B, right side.

---

## Zone A: Top nav (editor variant)

Left: back arrow to Overview, article title (inline editable), unsaved indicator dot.
Right: mode toggle (Write / Review), Inspect button, Publish button (primary CTA).

The Publish button is disabled if no destinations have been configured or if the gate is failing.

---

## Zone B: Toolbar

Write mode: bold, italic, code, heading level, blockquote, code block, link, image.
Review mode: Add comment (triggers inline selection), Clear resolved comments.

---

## Zone C: Editor pane

Markdown editor with live rich preview rendered inline (not side-by-side).
Headings, code blocks, images, and blockquotes render as they would in the final article.
Code blocks: syntax highlighted, language label shown, copy button on hover.

In Review mode:
- Selected text shows a comment anchor (underline + margin dot)
- AI-patched sections show a diff highlight (green added, red removed) until accepted

---

## Zone D: Margin panel

Three sub-sections, scroll independently of editor:

1. **Comments** — threaded comment list anchored to text positions
2. **AI patches** — pending patches with diff preview and Accept/Reject per patch
3. **Destinations** — current draft state per platform (compact, links to inspection)

The section shown is controlled by a tab strip at the top of Zone D.
