# Overview - UI Tests Spec

> Test authority: [overview.drawio](overview.drawio). Tests project its represented states
> and `OV-*`/`OV-S*` transitions; they must not create new UI requirements.

These browser-level tests map directly to the IDs in `interactions.md`. Use deterministic
API fixtures for state transitions and real browser behavior for navigation. Mobile
sidebar behavior is not part of this suite.

## Loading and collection lifecycle

- [ ] `OV-S01`: opening Overview starts the first-page request and renders five skeleton cards.
- [ ] `OV-S02`: a successful non-empty response replaces skeletons with one centered card column.
- [ ] `OV-S03`: a successful empty response shows First-run Empty, not an error.
- [ ] `OV-S04`: a failed initial request shows Load Error rather than an empty state.
- [ ] `OV-34` and `OV-S01`: Load Error Retry starts exactly one new first-page request.
- [ ] The filter bar and top navigation remain fixed while the card region scrolls.
- [ ] Opening a 300 px details panel leaves the card column readable on the supported desktop viewport.

---

## Navigation and creation

- [ ] `OV-01`: Articles remains active without reloading another view.
- [ ] `OV-02`: Queue opens Publish Queue.
- [ ] `OV-03`: Platforms opens platform connections.
- [ ] `OV-04`: Settings opens Settings.
- [ ] `OV-05`: New article opens Create Article.
- [ ] `OV-06`: the chevron opens and closes the import menu; outside click closes it.
- [ ] `OV-07`: Import from platform opens Import Article in platform mode.
- [ ] `OV-08`: Upload `.md` opens Import Article in upload mode.

---

## Filters and empty results

- [ ] `OV-09` and `OV-S05`: search is debounced, case-insensitive, and updates count/results.
- [ ] `OV-10` through `OV-14`: exactly one status filter is active; All clears status filtering.
- [ ] `OV-15` through `OV-17`: platform filters are multi-select and use OR semantics.
- [ ] Search, status, and platform criteria combine with AND semantics.
- [ ] `OV-S06`: no matches shows Filtered Empty without discarding filter controls.
- [ ] `OV-24`: Clear filters restores Browse and resets all criteria.
- [ ] `OV-25`: First-run New article opens Create Article.

---

## Card selection and platform preview

- [ ] `OV-18`: clicking card body selects it and opens populated details.
- [ ] `OV-18`: selecting another card moves selection and replaces panel content.
- [ ] `OV-18`: clicking the selected card again does not collapse, expand, or deselect it.
- [ ] `OV-19`, `OV-20`, and `OV-21`: each tab changes media, copy, status, accent, and active indicator together.
- [ ] Preview-tab clicks do not select the card and do not open a new tab.
- [ ] Active preview selection survives a same-session list re-render.
- [ ] `OV-22`: Visit opens only the active platform URL in a new tab.
- [ ] `OV-22`: Visit is disabled and inert when that URL is absent.
- [ ] `OV-23`: card Edit opens Editor and does not select the card first.

---

## Details panel lifecycle

- [ ] `OV-28`: collapse changes the panel from 300 px to the 12 px strip and preserves selection.
- [ ] `OV-28`: expand restores the same selected article and populated details.
- [ ] The approved panel has no visible close/deselect control.
- [ ] `OV-S13`: refresh preserves selection and open/collapsed state when the article remains visible.
- [ ] `OV-S14`: filtering the selected article out clears selection and removes the panel.
- [ ] `OV-S14`: a refresh after archive/delete/remote removal also clears selection.
- [ ] `OV-30`: panel Edit opens Editor for the selected article.
- [ ] `OV-32`: Schedule opens Publish Queue with the selected article.

---

## Background jobs

- [ ] `OV-29`: primary action label, enabled state, and submitted operation agree.
- [ ] `OV-31`: Inspect submits one inspection request for the selected article.
- [ ] `OV-S09`: a `202` response renders queued state and prevents duplicate submission.
- [ ] `OV-S10`: a running poll result updates progress while retaining the panel.
- [ ] `OV-S11` and `OV-S13`: completion refreshes cards/details and preserves valid selection.
- [ ] `OV-S12`: failure is visible in the panel and does not masquerade as success.
- [ ] `OV-33`: retry submits the failed operation once and returns to queued state.

---

## Pagination

- [ ] `OV-26`: Load more keeps existing cards visible while requesting the next page.
- [ ] Pagination loading renders three skeleton cards below existing cards.
- [ ] `OV-S07`: success appends unique cards and preserves active filters and valid selection.
- [ ] `OV-S08`: failure keeps existing cards and shows inline error state.
- [ ] `OV-27`: Retry requests the failed page and cannot append duplicate articles.

## Accessibility and visual contract

- [ ] Every interactive control is keyboard reachable and has a visible focus state.
- [ ] Active preview and status states are not communicated by color alone.
- [ ] Loading, empty, error, selected-open, selected-collapsed, queued, running, and failed states match the states represented in `overview.drawio`.
