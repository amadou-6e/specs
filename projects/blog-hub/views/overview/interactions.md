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
- Gate badges do not select the card. Completed Pass, Warn, and Fail badges open
  Inspection; Pending is passive.
- Card-context controls never select the card. Only one context menu is open at a time,
  and outside click or Escape returns it to the closed card state.

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

### Gate and card context actions

| ID | Selector | Preconditions | Trigger | Outcome | Type |
|---|---|---|---|---|---|
| `OV-35` | `.card-gate[data-state="pass|warn|fail"]` | Gate inspection is complete and has a report URL | Click gate badge | Opens Inspection for this article | Navigate |
| `OV-36` | `.card-context-trigger` | Card is rendered | Click context trigger | Opens or closes this card's context menu | Self |
| `OV-37` | Context Edit | Context menu is open | Click Edit | Opens Editor for this article | Navigate |
| `OV-38` | Context Duplicate | Context menu is open and no mutation is pending | Click Duplicate | Starts one idempotent duplicate request | Async |
| `OV-39` | Context Archive | Context menu is open and no mutation is pending | Click Archive | Starts archive and retains article history | Async |
| `OV-40` | Context Delete | Context menu is open | Click Delete | Replaces the action row with inline confirmation | Self |
| `OV-41` | Inline Confirm delete | Delete confirmation is visible and no mutation is pending | Click Delete | Starts deletion | Async |
| `OV-42` | Inline Cancel delete | Delete confirmation is visible | Click Cancel | Restores the context action row without a request | Self |

The Pending gate is visually distinct but has no `OV-*` marker because it is not
interactive. Duplicate, archive, and delete disable all context actions until their
single request settles. A `404`, published-article `409`, or other mutation failure is
shown inside that card and never via an alert.

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
| `OV-43` | Recovery-unavailable Retry | Active-job discovery failed | Click Retry recovery | Repeats active-job discovery without closing the selected panel | Async |

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
| `OV-S15` | Article data loads or refreshes | Renders Pass, Warn, Fail, or Pending gate state; only completed states with a report URL enable `OV-35` |
| `OV-S16` | Duplicate succeeds | Inserts and selects the one returned copy, then refreshes the collection |
| `OV-S17` | Archive succeeds | Removes the article from the active collection, retains history, and clears selection when needed |
| `OV-S18` | Delete succeeds | Removes the article and clears selection when needed |
| `OV-S19` | A context mutation returns `404` | Keeps the card and displays an inline not-found result until refresh or another action |
| `OV-S20` | Delete returns published-article `409` | Keeps the article and displays the inline conflict without dismissing it automatically |
| `OV-S21` | A context mutation otherwise fails | Keeps the article and displays an inline action error |
| `OV-S22` | Submission returns an existing job for the same idempotency key | Reattaches to that job and enters Job Queued or Job Running without creating work |
| `OV-S23` | Polling reports `canceled` | Enters Job Canceled and exposes `OV-33` only when retry is supported |
| `OV-S24` | Durable retry is accepted | Enters Job Queued with the returned job identity |
| `OV-S25` | Durable retry is rejected | Returns to Job Failed with the rejection detail still visible |
| `OV-S26` | Overview reloads with a selected article | Enters Recovering and requests active durable jobs for that article |
| `OV-S27` | Recovery finds an active queued or running job | Reattaches to the job and resumes polling in its reported state |
| `OV-S28` | Recovery finds no active job or only a terminal job | Refreshes article detail and returns to Selected Open |
| `OV-S29` | Active-job discovery fails | Keeps selection open and shows Recovery Unavailable with `OV-43` |
| `OV-S30` | Backend reports its durable timeout as a terminal failure | Enters Job Failed with the backend reason; the browser never invents a five-second timeout |

`OV-29` and `OV-31` first enter Submitting. They are disabled in Submitting, Job
Queued, Job Running, Recovering, and Retrying. Submission always carries a stable
idempotency key for the visible operation; `OV-S22` handles a repeated request by
reattaching rather than enqueuing another job.
