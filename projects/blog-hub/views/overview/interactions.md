# Overview - Interactions

The `Overview - Articles` page in `overview.drawio` is the sole authority. This file is
a searchable projection of its desktop interaction IDs and must follow the Draw.io.
Mobile sidebar behavior is explicitly out of scope.

## Type key

- **Self** - changes state within Overview.
- **Navigate** - opens another BlogHub view.
- **Async** - starts an API operation and observes its job.
- **External** - opens a remote platform URL in a new tab.
- **System** - is triggered by loading, polling, or refreshed data rather than a user.

## Selection rules represented in Draw.io

- Selecting an article opens its details panel.
- Selecting another article replaces the selection and opens the panel.
- Selecting the current article again keeps it selected and keeps the current panel state.
- `OV-28` is the only user action that collapses or expands the panel. Collapse keeps the selection.
- The approved panel has no separate close or deselect button.
- A filter or refresh clears selection when the selected article is no longer present.
- Archive, delete, or remote removal also clears selection after the refreshed collection no longer contains the article.
- Platform tabs select platform-specific preview content. They never navigate.
- `Visit` opens the active platform's remote URL and is disabled when that URL is unavailable.

## User interactions

### Navigation and creation

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| `OV-01` | `#nav-articles` | Click Articles | - | Keeps Overview active | Self |
| `OV-02` | `#nav-queue` | Click Queue | - | Opens Publish Queue | Navigate |
| `OV-03` | `#nav-platforms` | Click Platforms | - | Opens platform connections | Navigate |
| `OV-04` | `#nav-settings` | Click Settings | - | Opens Settings | Navigate |
| `OV-05` | New article split-button primary action | Click New article | - | Opens Create Article | Navigate |
| `OV-06` | `#create-menu-btn` | Click split-button chevron | - | Opens or closes the import menu | Self |
| `OV-07` | First `#import-menu` action | Click Import from platform | Menu is open | Opens Import Article in platform mode | Navigate |
| `OV-08` | Second `#import-menu` action | Click Upload `.md` file | Menu is open | Opens Import Article in upload mode | Navigate |

---

### Filters

| ID | Selector | Trigger | Preconditions | Outcome | Type |
|---|---|---|---|---|---|
| `OV-09` | `#search-input` | Enter or clear search text | - | Schedules a filtered collection load | Self |
| `OV-10` | `#sf-all` | Click All | - | Clears the status filter | Self |
| `OV-11` | `#sf-drafting` | Click Drafting | - | Selects the drafting status | Self |
| `OV-12` | `#sf-ready` | Click Ready | - | Selects the ready status | Self |
| `OV-13` | `#sf-error` | Click Error | - | Selects the error status | Self |
| `OV-14` | `#sf-published` | Click Published | - | Selects the published status | Self |
| `OV-15` | `#pf-medium` | Toggle Medium | - | Adds or removes Medium from the platform filter | Self |
| `OV-16` | `#pf-hashnode` | Toggle Hashnode | - | Adds or removes Hashnode from the platform filter | Self |
| `OV-17` | `#pf-devto` | Toggle Dev.to | - | Adds or removes Dev.to from the platform filter | Self |

Status is single-select. Platform filters are multi-select with OR semantics. Search,
status, and platform criteria combine with AND semantics.

---

### Article cards and collection states

| ID | Selector | Preconditions | Trigger | Outcome | Type |
|---|---|---|---|---|---|
| `OV-18` | `.article-card` | Article is not selected | Click card body | Selects article and opens details | Self |
| `OV-19` | `.plat-tab[data-platform="medium"]` | Card is rendered | Click Medium tab | Renders Medium preview in this card | Self |
| `OV-20` | `.plat-tab[data-platform="hashnode"]` | Card is rendered | Click Hashnode tab | Renders Hashnode preview in this card | Self |
| `OV-21` | `.plat-tab[data-platform="devto"]` | Card is rendered | Click Dev.to tab | Renders Dev.to preview in this card | Self |
| `OV-22` | `.card-visit` | Active platform has a remote URL | Click Visit | Opens that URL in a new tab | External |
| `OV-23` | `.card-edit` | Card is rendered | Click Edit | Opens Editor for the article | Navigate |
| `OV-24` | Filtered-empty Clear filters | Filters produce no results | Click Clear filters | Restores unfiltered browse | Self |
| `OV-25` | First-run New article | No articles exist | Click New article | Opens Create Article | Navigate |
| `OV-26` | `#load-more-button` | Another page exists | Click Load more | Requests the next page | Async |
| `OV-27` | `.load-more-retry-btn` | Page request failed | Click Retry | Retries the same page request | Async |

Clicks on a preview tab, Visit, or Edit stop propagation and do not change selection.
The same article's preview selection survives card-list re-renders during the view session.

### Details panel

| ID | Selector | Preconditions | Trigger | Outcome | Type |
|---|---|---|---|---|---|
| `OV-28` | `#side-strip` | An article is selected | Click strip | Toggles open/collapsed; selection remains | Self |
| `OV-29` | `#panel-primary-btn` | An article is selected and its derived action is enabled | Click primary action | Starts the derived push, resume, retry, inspect, view, or schedule behavior | Async or Navigate |
| `OV-30` | Details-panel Edit | An article is selected | Click Edit | Opens Editor for the selected article | Navigate |
| `OV-31` | `#panel-inspect-btn` | An article is selected | Click Inspect | Starts an inspection job | Async |
| `OV-32` | Details-panel Schedule | An article is selected | Click Schedule | Opens Publish Queue with the article preselected | Navigate |
| `OV-33` | Failed-job Retry | A panel job failed and is retryable | Click Retry | Restarts the failed operation | Async |
| `OV-34` | Collection Load Error Retry | Initial collection load failed | Click Retry | Starts the initial collection request again | Async |

`OV-29` must expose one concrete action at a time. Its label, enabled state, and behavior
come from the article action model; the same button must not silently change behavior
without changing its visible label.

## System transitions

System IDs are unique and are never reused as user IDs.

| ID | Trigger | Outcome |
|---|---|---|
| `OV-S01` | View mounts, or `OV-34` requests another initial load | Enters Loading and requests the first page |
| `OV-S02` | Initial collection request succeeds with articles | Enters Browse |
| `OV-S03` | Initial collection request succeeds with zero articles | Enters First-run Empty |
| `OV-S04` | Initial collection request fails | Enters Load Error |
| `OV-S05` | Filter debounce expires | Requests the filtered collection and enters Filtered Browse when it succeeds |
| `OV-S06` | Filtered request succeeds with zero matches | Enters Filtered Empty |
| `OV-S07` | Next-page request succeeds | Appends unique articles and returns to the prior browse/selection state |
| `OV-S08` | Next-page request fails | Shows inline pagination failure without replacing existing articles |
| `OV-S09` | Article action is accepted (`202`) | Enters Job Queued for the selected article |
| `OV-S10` | Job reports running | Enters Job Running and keeps the panel visible |
| `OV-S11` | Job reports done | Refreshes the article collection and selected detail |
| `OV-S12` | Job reports error | Enters Job Failed and exposes retry when supported |
| `OV-S13` | Refresh still contains the selected article | Preserves selection and open/collapsed panel state |
| `OV-S14` | Filter or refresh excludes/removes the selected article | Clears selection and returns to Browse or Filtered Browse |
| `OV-S15` | Application startup or Overview reload resolves connected blogs | Uses connected Hashnode and Medium records as the synchronization source of truth |
| `OV-S16` | A connected blog lacks a valid recurring schedule | Creates or repairs its enabled 60-second internal schedule |
| `OV-S17` | Overview reload completes its local load, or a schedule becomes due | Queues one idempotent sync job per connected platform |
| `OV-S18` | The durable worker claims a sync job | Retrieves and reconciles the platform's remote articles |
| `OV-S19` | Remote synchronization succeeds | Upserts remote articles and refreshes the Overview collection |
| `OV-S20` | Remote synchronization fails | Retains current cards and allows durable retry or the next recurrence to recover |

The schedule is internal infrastructure. It is created and repaired from connected-blog
state and must not appear as a manual sync control on the Overview page.

## Deferred controls

Gate badges and card context actions are not present in the approved Overview visual
baseline. Their contract belongs to blog-hub issue #98; they must receive new IDs when
they are introduced rather than reusing IDs in this document.
