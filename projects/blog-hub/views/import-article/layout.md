# Import Article — Layout Spec

## Purpose
Standalone screen for bringing existing content into BlogHub. Handles two modes selected via query param:
- `mode=platform` — pick a draft from a connected blog platform
- `mode=upload` — upload a local `.md` file

Entry points: Overview split button dropdown (both modes), Create Article wizard (platform mode only).
Exit points: Editor (on success), Overview or Create Article (on cancel, driven by `returnTo`).

---

## Page Zones

```
┌─────────────────────────────────────────────────────────────────┐
│  ZONE A: Top nav (fixed, 48px)                                  │
│  BlogHub logo                          [Cancel]                 │
├─────────────────────────────────────────────────────────────────┤
│  ZONE B: Mode header (fixed, 64px)                              │
│  Title + step breadcrumb                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ZONE C: Content (scrollable, fills remaining height)           │
│  — varies by mode and step (see below)                          │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  ZONE D: Footer action bar (fixed, 64px)                        │
│  [Cancel]                    [Back]  [Import / Confirm]         │
└─────────────────────────────────────────────────────────────────┘
```

Zone A and D are fixed. Zone B is fixed below Zone A. Zone C scrolls independently.

---

## Width and Centering

Max content width: 800px, centered.
Horizontal padding: 32px desktop, 20px mobile.

The screen is not a modal — it is a full page. It uses a narrower content column than Overview to keep attention on the import task.

---

## Zone A: Top Nav

Left: BlogHub logo (links to overview — same target as `returnTo=overview` cancel).
Right: "Cancel" text button. Uses `returnTo` param to navigate to the correct screen.

No nav links. No primary action button. The screen is single-purpose.

---

## Zone B: Mode Header

- Screen title: "Import Article"
- Step breadcrumb (platform mode only): "1. Choose platform  >  2. Select draft  >  3. Review"
- Upload mode shows no breadcrumb (single step: pick file, then review).

---

## Zone C: Content by mode and step

### Platform mode — Step 1: Choose platform
- Grid of connected platform cards (2 columns).
- Each card: platform logo, platform name, connection status, draft count.
- Disconnected platforms are shown but disabled, with "Connect in Settings" tooltip.
- Empty state: no platforms connected — show prompt to visit Settings.

### Platform mode — Step 2: Select draft
- Back link to Step 1.
- Platform name header.
- Paginated list of drafts: title, word count, last updated.
- One draft selected at a time (radio-style row highlight).
- Infinite scroll or "Load more" button (not a page number paginator).

### Platform mode — Step 3: Review
- Back link to Step 2.
- Read-only preview: title (editable inline), word count, platform source label.
- Markdown rendered in a scrollable preview pane (max height 480px, overflow scroll).

### Upload mode — Step 1: Pick file
- Drop zone (full-width, 240px tall): drag-and-drop or click to browse.
- Accepts `.md` files only. Shows error inline if wrong type.
- Once a file is chosen, parse client-side immediately and advance to Review.

### Upload mode — Step 2: Review
- Same layout as Platform mode Step 3.
- Title extracted from first `# heading` (editable inline).
- Word count computed from parsed content.
- Source label: "Local file — filename.md".

---

## Zone D: Footer Action Bar

Left: "Cancel" — navigates to `returnTo` target.
Right: "Back" (platform mode, steps 2 and 3 only) + primary action button.

Primary action labels:
- Platform step 1: disabled (no action until platform selected; "Next" activates on selection)
- Platform step 2: "Next" (advances to Review)
- Platform step 3: "Import" (fires API call)
- Upload step 1: hidden (file picker triggers advance automatically)
- Upload step 2: "Import" (fires API call)

During API call: primary button shows spinner, is disabled. Cancel is also disabled.

---

## Responsive Notes

- Mobile: content column fills full width, platform grid becomes 1 column.
- Draft list rows stack to 2 lines on narrow viewports (title wraps).
- Footer stacks vertically on mobile: Cancel top-left, Back + Import bottom-right.
