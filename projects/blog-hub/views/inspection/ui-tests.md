# Inspection — UI Tests Spec

> Test authority: [inspection.drawio](inspection.drawio). Tests project its represented
> states and `IN-*` transitions; they must not create new UI requirements.

---

## Summary bar

- [ ] Overall gate "pass" shows green badge
- [ ] Overall gate "warn" shows amber badge and Proceed button is enabled
- [ ] Overall gate "fail" shows red badge and Proceed button is disabled
- [ ] Inspected-at timestamp is shown and human-readable
- [ ] "Re-run inspection" triggers a new inspection job (spinner shown)
- [ ] After re-run completes, tab results update without full page reload

---

## Platform tabs

- [ ] Tab is rendered for each destination with a draft
- [ ] Tab label shows platform name + per-platform gate pill
- [ ] Active tab is visually distinct (underline accent, label brightened)
- [ ] Switching tabs updates the check list for the selected platform
- [ ] Tab for a platform with all checks passing shows green pill
- [ ] Tab for a platform with any failing check shows red pill

---

## Check list

- [ ] Each check row shows icon (✓/⚠/✗), label, and detail summary
- [ ] Clicking a check row selects it (highlighted, left border accent)
- [ ] Clicking a selected check row deselects it (artifact panel closes or shows empty state)
- [ ] Only one check can be selected at a time
- [ ] Pass checks are listed first, then warn, then fail (within each platform tab)

---

## Artifact panel

- [ ] Panel is empty when no check is selected (shows placeholder text)
- [ ] Selecting a code_blocks check renders all code blocks found in the draft
- [ ] Selecting an images check renders a table of expected vs found URLs
- [ ] Missing image rows are highlighted red in the table
- [ ] Selecting a sections check renders a two-column heading comparison
- [ ] Missing or reordered headings are highlighted
- [ ] Selecting a tail check renders the last 500 characters in monospace
- [ ] Truncation point is highlighted red when the tail check has failed
- [ ] "View full dump" link opens raw artifact in a new browser tab

---

## Tablet layout

- [ ] Artifact panel is not visible at 768px by default
- [ ] Clicking a check row opens the artifact as a bottom drawer
- [ ] Drawer closes on swipe down or backdrop click

---

## Edge cases

- [ ] Article with no drafts: redirect to editor with "No drafts to inspect" toast
- [ ] All platforms passing: Proceed button is enabled and prominent
- [ ] Re-run while a re-run is already in flight: button stays in spinner state, no duplicate request
