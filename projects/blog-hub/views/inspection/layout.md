# Inspection — Layout Spec

> Design blocked: no authoritative `inspection.drawio` exists. Treat the layout below as
> historical planning input only.

## Purpose
Shows the per-platform gate result after a draft has been created. The user diagnoses failures and decides whether to proceed to publish.

---

## Page Zones

```
┌─────────────────────────────────────────────────────────────────┐
│  ZONE A: Top nav (fixed, 48px) — article title + back           │
├─────────────────────────────────────────────────────────────────┤
│  ZONE B: Summary bar (sticky, 56px) — overall gate + actions    │
├──────────────────────────────────┬──────────────────────────────┤
│                                  │                              │
│  ZONE C: Platform tabs           │  ZONE D: Artifact panel      │
│  (scrollable, flex-1)            │  (scrollable, 400px wide)    │
│                                  │                              │
│  Checks list per platform        │  Raw HTML dump / chunk log   │
│                                  │  shown for selected check    │
│                                  │                              │
└──────────────────────────────────┴──────────────────────────────┘
```

---

## Zone B: Summary bar

Left: overall gate result badge (pass/warn/fail), inspected-at timestamp, "Re-run inspection" link.
Right: "Proceed to publish" button (disabled if gate is fail), "Back to editor" link.

---

## Zone C: Platform tabs + checks

One tab per destination (Medium, Hashnode, Dev.to).
Tab label shows platform name + per-platform gate result pill.

Within each tab, a vertical list of check items:

```
[✓]  Code blocks preserved       4 / 4 blocks intact
[✓]  Section count matched       8 / 8 sections
[⚠]  Image count                 3 / 4 images — 1 missing
[✗]  Article tail present        Missing — content cut off at 92%
```

Each check row is clickable. Clicking highlights the relevant artifact in Zone D.

---

## Zone D: Artifact panel

Shows the raw evidence for the selected check:
- Code block check: renders the raw HTML of each code block found
- Image check: lists src URLs found vs expected
- Section check: outlines detected vs expected headings
- Tail check: shows the last 500 chars of the imported draft

Header of Zone D shows which check is selected and a "View full dump" link (opens raw HTML in new tab).

On tablet (<1024px): Zone D is a bottom drawer, opened by clicking a check row.
