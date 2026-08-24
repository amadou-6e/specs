# Overview — UI Tests Spec

Tests cover interactions, state transitions, visual correctness, and edge cases.
These are browser-level tests (Playwright or equivalent). No mocks — use fixture data.

---

## Layout and render

- [ ] Card grid renders 3 columns at 1440px viewport
- [ ] Card grid renders 2 columns at 900px viewport
- [ ] Card grid renders 1 column at 375px viewport
- [ ] Filter bar sticks to top when scrolling past 3 card rows
- [ ] Top nav does not scroll with the page
- [ ] No horizontal scroll at any breakpoint

---

## ArticleCard states

- [ ] Error card renders with red left border accent
- [ ] Card with all platforms published renders with muted/green gate badge
- [ ] Hovering a card lifts background and brightens border
- [ ] Clicking a card selects it (left indigo border, background tint)
- [ ] Clicking a different card deselects the previous one
- [ ] Clicking the selected card again does not deselect it

---

## Platform pills

- [ ] Pill with a draft URL is clickable and opens correct URL in new tab
- [ ] Pill with status `none` is not clickable (cursor: default, no underline)
- [ ] Pill status colours match design tokens: draft=blue, ready=green, error=red, pending=amber, published=teal

---

## Context menu [···]

- [ ] Menu opens on click, not on hover
- [ ] Menu closes when clicking outside
- [ ] Menu closes when pressing Escape
- [ ] "Delete" option shows inline confirmation before acting
- [ ] Confirming delete removes the card from the grid without page reload
- [ ] Cancelling delete leaves the card unchanged

---

## Gate badge

- [ ] Gate "Pass" renders green ✓ with correct label
- [ ] Gate "Warn" renders amber ⚠ with correct label
- [ ] Gate "Fail" renders red ✗ with correct label
- [ ] Gate "pending" renders muted dash
- [ ] Clicking gate badge navigates to /inspect/:id

---

## Primary action button

- [ ] Card with no drafts shows "Push drafts" button
- [ ] Card post-inspection-pass shows "Schedule" button
- [ ] Card fully published shows "View live" button
- [ ] Clicking "Push drafts" triggers the push flow (verify API call or navigation)

---

## Filter bar: search

- [ ] Typing filters cards in real time (debounce max 300ms)
- [ ] Matching is case-insensitive and applies to title
- [ ] No results shows the `no-results` EmptyState
- [ ] Pressing Escape clears the search input and restores all cards
- [ ] Article count label updates as results change

---

## Filter bar: status filters

- [ ] Selecting "Error" shows only cards with at least one error destination
- [ ] Selecting "Published" shows only fully published cards
- [ ] Selecting "All" deselects any active filter and shows all cards
- [ ] Only one status filter can be active at a time

---

## Filter bar: platform filters

- [ ] Selecting "Medium" filters to articles that have a Medium entry (any status)
- [ ] Multiple platforms can be selected simultaneously (OR logic)
- [ ] Deselecting all platform filters shows all articles

---

## Empty states

- [ ] First-run (no articles): shows `no-articles` variant with New Article button
- [ ] Filtered empty: shows `no-results` variant with "Clear filters" link
- [ ] "Clear filters" resets search, status, and platform filters

---

## Loading state

- [ ] 6 skeleton cards render while data is loading
- [ ] Skeleton shimmer animation is running
- [ ] Skeletons disappear and cards appear without layout shift after data loads

---

## New Article button

- [ ] Clicking navigates to /create
- [ ] Button is visible at all breakpoints (icon-only on mobile is acceptable)
