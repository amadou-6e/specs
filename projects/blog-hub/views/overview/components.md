# Overview - Components Spec

The components below describe the approved desktop geometry in `overview.drawio`.
Gate badges and card context menus are deferred to blog-hub issue #98.

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
