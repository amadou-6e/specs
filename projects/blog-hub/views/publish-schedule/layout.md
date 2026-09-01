# Publish / Schedule — Layout Spec

> UI authority: [publish-schedule.drawio](publish-schedule.drawio). This layout is a
> derived reading aid, not an independent source of UI behavior.

## Purpose
The final step before content goes live. The user selects destinations, picks a time, and confirms.

---

## Page Zones

```
┌─────────────────────────────────────────────────────────────────┐
│  ZONE A: Top nav (fixed, 48px) — article title + back           │
├─────────────────────────────────────────────────────────────────┤
│                    ZONE B: Content (centred, max 720px)         │
│                                                                 │
│   Article preview header (title, word count, gate badge)        │
│                                                                 │
│   ┌─── Destination rows ───────────────────────────────────┐   │
│   │  [✓] Medium    Draft v2  ·  Publish now / [date picker] │   │
│   │  [✓] Hashnode  Draft v1  ·  Publish now / [date picker] │   │
│   │  [ ] Dev.to    Error     ·  (disabled — fix first)      │   │
│   └────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ZONE C: Action bar (sticky bottom, 56px)                      │
└─────────────────────────────────────────────────────────────────┘
```

Single column, centred layout. No side panels. This screen should feel decisive and simple.

---

## Zone B content sections

**Article header strip:**
Title, word count, last updated, overall gate badge.
Not editable here. "Edit" link navigates back to editor.

**Destination rows:**
One row per destination that has a draft. Checkable.
Each row: platform name, current draft status, publish mode toggle (Now / Scheduled).
If mode is Scheduled: date+time picker appears inline below the row.

Destinations with errors are shown but unchecked and non-interactive.
A short reason and "Fix" link appear instead of the time picker.

**Confirm summary** (appears after at least one destination is checked):
Plain text summary of what will happen: "Publishing to Medium now and Hashnode on Apr 4 at 09:00."

---

## Zone C: Action bar

Left: back link to /inspect/:id.
Right: "Confirm and publish" button (primary, disabled until at least one destination is checked).

While publishing: button shows spinner + "Publishing…". Back link is disabled.

After publish: replace the form with an outcome screen (see below).

---

## Post-publish outcome screen

Replaces Zone B content. No navigation away required.

```
✓  Medium       Published  →  [View on Medium]
✓  Hashnode     Scheduled  →  Apr 4, 09:00
✗  Dev.to       Skipped    →  (had errors)
```

Primary action: "Back to overview".
Secondary: "View article" (opens first successfully published URL).
