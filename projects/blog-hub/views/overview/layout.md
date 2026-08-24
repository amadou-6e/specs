# Overview — Layout Spec

## Purpose
Entry point and daily driver. The user sees all articles and their per-platform state at a glance.

---

## Page Zones

```
┌─────────────────────────────────────────────────────────────────┐
│  ZONE A: Top nav (fixed, 48px)                                  │
├─────────────────────────────────────────────────────────────────┤
│  ZONE B: Filter bar (sticky, 52px)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ZONE C: Card grid (scrollable, fills remaining height)         │
│                                                                 │
│   [Card]  [Card]  [Card]                                        │
│   [Card]  [Card]  [Card]                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Zone A and B are fixed/sticky. Zone C scrolls independently.

---

## Grid

- Desktop (>1280px): 3 columns, 24px gap
- Tablet (768–1280px): 2 columns, 20px gap
- Mobile (<768px): 1 column, 16px gap

Max content width: 1400px, centered.
Horizontal padding: 32px desktop, 20px tablet, 16px mobile.

---

## Zone A: Top Nav

Left: logo/wordmark, then primary nav links (Articles active, Queue, Platforms, Settings).
Right: platform health indicator, New Article button.

Height: 48px. Background: surface color with bottom border. Does not scroll.

---

## Zone B: Filter Bar

Left to right:
1. Search input (240px fixed width)
2. Divider
3. Status filter pills: All, Drafting, Ready, Error, Published
4. Divider
5. Platform toggle pills: Medium, Hashnode, Dev.to
6. Right edge: article count label

Height: 52px. Sticks to top below Zone A when scrolling.

---

## Zone C: Card Grid

Cards are sorted by urgency:
1. Error state (any platform)
2. Attention needed (warn gate, needs review)
3. Drafting / in progress
4. Ready / scheduled
5. Published (all platforms)

Empty state: centered illustration + "No articles yet" + New Article button.
Loading state: skeleton cards (same dimensions as real cards).

---

## Above the Fold (1080px screen)

At typical desktop height, the user sees:
- Zone A and B in full
- First 2 rows of cards (6 cards at 3-col)

No action should require scrolling on first load if the article list is non-empty.

---

## Responsive Notes

- On mobile, filter pills collapse into a single "Filter" button that opens a bottom sheet.
- Card grid becomes single column.
- New Article button collapses to icon-only on mobile.
