# Overview - Components Spec

> UI authority: [overview.drawio](overview.drawio). This component inventory is a
> searchable projection; the Draw.io wins if geometry, state, or interaction details differ.

The components below describe the approved desktop geometry in `overview.drawio`.

## ArticleCard

The primary unit of the centered, single-column article list.

```text
+-------------------------------------------------------------------+
| | MEDIUM | HASHNODE | DEV.TO                                      |
| |                         destination preview                     |
| | Title                                                            |
| | Subtitle                                                         |
| | Excerpt                                                          |
| | ---------------------------------------------------------------- |
| | Status       Updated date / words              Visit       Edit  |
+-------------------------------------------------------------------+
```

### Data

- `id: string`
- `title: string`
- `subtitle: string | null`
- `excerpt: string | null`
- `updatedAt: datetime`
- `wordCount: number`
- `destinations: Record<Platform, DestinationPreview>`
- `activePreviewPlatform: Platform`
- `gate: { result: pass | warn | fail | pending, reportUrl: string | null }`
- `mutation: idle | pending | not_found | conflict | failed`

### States

- Default
- Hover: border brightens without changing dimensions
- Selected: selection border/background; details panel is present
- Platform preview: active tab, accent bar, media, copy, status, and Visit URL all
  derive from the same destination
- Error: active destination status and accent communicate failure
- Loading: skeleton preserves the card's dimensions

### PlatformPreviewTabs

- `OV-19`, `OV-20`, and `OV-21` select Medium, Hashnode, and Dev.to respectively.
- A tab selection changes only this card's preview; it does not navigate or select the card.
- Active platform state includes text styling and a visible indicator, not color alone.

### CardActions

- `Visit` (`OV-22`) opens the active destination URL in a new tab.
- Visit is visibly disabled and performs no action when the active destination has no URL.
- `Edit` (`OV-23`) opens the article in Editor.
- Neither action bubbles into card selection.

### GateBadge

- Pass, Warn, Fail, and Pending have distinct labels, borders, and colors.
- `OV-35` is present only for Pass, Warn, or Fail with a report URL and opens Inspection.
- Pending remains visible but passive; interactivity is never implied by color alone.
- Gate interaction does not select the article card.

### CardContext

- `OV-36` opens one accessible menu containing Edit (`OV-37`), Duplicate (`OV-38`),
  Archive (`OV-39`), and Delete (`OV-40`).
- Escape, outside click, or toggling `OV-36` closes it.
- Delete first renders inline confirmation with Confirm (`OV-41`) and Cancel (`OV-42`).
- Duplicate, archive, and confirmed delete run once and disable the menu while pending.
- Mutation errors replace the action row inside the affected card. Published-article
  conflicts are persistent and do not use alerts or modals.

## DetailsPanel

- Hidden when no article is selected.
- Open width: 300 px. It shows title, destination statuses, timeline, primary action,
  Edit, Inspect, and Schedule.
- Collapsed width: 12 px. The side strip remains visible and selection is retained.
- It has no close button. `OV-28` controls open/collapsed state.
- Refreshing data repopulates the panel from the selected article rather than storing a
  disconnected copy of article details.

### Panel actions

- `OV-29`: one derived primary action with a matching visible label.
- `OV-30`: Edit selected article.
- `OV-31`: start inspection job.
- `OV-32`: open Publish Queue with selected article.
- `OV-33`: retry a retryable failed job.
- `OV-43`: retry active-job discovery after reload recovery fails.

### Durable action presentation

- Submitting, queued, running, recovering, and retrying keep the panel open and disable
  `OV-29` and `OV-31`.
- Queued, running, failed, canceled, and retrying show the durable job identity and the
  current visible operation.
- Completion refreshes both cards and selected detail before leaving the completed state.
- Reload recovery reattaches to queued/running work; a recovery failure preserves the
  selected article and exposes `OV-43`.
- Failed and canceled states expose `OV-33` only when the backend marks the job retryable.

## PaginationRegion

- Hidden when there is no next page and no active/error pagination state.
- `OV-26` requests the next page while existing cards remain visible.
- Loading uses three card skeletons and a status label.
- Failure is inline and offers `OV-27` Retry.
- Success appends unique articles and preserves current selection when still present.

## FilterBar

- `SearchInput` (`OV-09`) - debounced text query.
- `StatusFilterGroup` (`OV-10` through `OV-14`) - single-select.
- `PlatformFilterGroup` (`OV-15` through `OV-17`) - multi-select with OR semantics.
- `ArticleCount` - passive label reflecting the loaded filtered collection.

## TopNav

- Brand mark and wordmark.
- Articles (`OV-01`), Queue (`OV-02`), Platforms (`OV-03`), and Settings (`OV-04`).
- Passive platform connection count.
- New article split button: primary action (`OV-05`) and menu (`OV-06` through `OV-08`).

## EmptyState

- `first-run`: no articles exist; explains the starting point and exposes `OV-25`.
- `filtered`: articles may exist, but none match; exposes `OV-24`.
- API failures must use LoadError, never either empty-state variant.

## SkeletonCard

Matches ArticleCard dimensions and uses an animated shimmer. Initial loading renders
five skeletons; pagination loading renders three below the existing collection.
