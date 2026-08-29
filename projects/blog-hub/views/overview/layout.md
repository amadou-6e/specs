# Overview - Layout Spec

## Purpose
Entry point and daily driver. The user sees all articles and their per-platform state at a glance.

---

## Desktop page zones

```
+-----------------------------------------------------------------+
| ZONE A: Top nav, 48 px                                          |
+----------------------------------------------------+------------+
| ZONE B: Filter bar                                 | ZONE D     |
+----------------------------------------------------+ Details    |
|                                                    | panel      |
| ZONE C: centered article list, max 750 px          | 300 px     |
|                                                    | or 12 px   |
|                    [Card]                          | strip      |
|                    [Card]                          |            |
|                    [Pagination]                    |            |
+----------------------------------------------------+------------+
```

Zone A is fixed. Zone B remains above the independently scrolling Zone C. Zone D is
absent with no selection, 300 px when open, and 12 px when collapsed.

---

## Article list

- One centered column, `minmax(0, 750px)`.
- 12 px vertical gap between cards.
- 24 px vertical and 32 px horizontal scroll-area padding.
- Opening the panel reduces available list space; it does not create another card column.

---

## Zone A: Top Nav

Left: logo/wordmark. Center: Articles, Queue, Platforms, Settings. Right: passive
platform health indicator and New article split button.

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

The approved desktop bar uses 18 px top, 8 px bottom, and 32 px horizontal padding.
It does not scroll with the article list.

---

## Zone C: Article list

Cards are sorted by urgency:
1. Error state (any platform)
2. Attention needed (warn gate, needs review)
3. Drafting / in progress
4. Ready / scheduled
5. Published (all platforms)

First-run and filtered-empty states are centered in this zone. Initial loading uses five
card skeletons. Pagination progress or failure appears after existing cards.

---

## Zone D: Details panel

- Open: 300 px fixed width with populated content.
- Collapsed: 12 px strip; content is not rendered visibly.
- Hidden: no selected article, so Zone C uses all available body width.
- Selecting a different article opens the panel and updates it in place.

## Scope boundary

This specification defines desktop behavior. Mobile sidebar/drawer behavior is explicitly
excluded from issue #95 and must not be inferred from the desktop widths above.
