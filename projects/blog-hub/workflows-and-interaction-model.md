# BlogHub: Workflows and Interaction Model

Date: 2026-04-02

---

## Workflows

### 1. Platform connect
**Frequency:** one-time, occasional
**Entry:** Settings or first-run prompt
**Feel:** calm, step-by-step, trust-building

Connects:
- Publishing destinations: Medium, Hashnode, Dev.to (session or API key)
- AI providers: Claude (CLI or API key), Codex (API key)

Success state: platform shows a connected badge with session health indicator.

---

### 2. Article overview
**Frequency:** daily, entry point
**Feel:** editorial, scannable, card-based

Cards not table rows. Three-column grid (two on narrow). Sort order: errors first, attention-needed, drafting, published last.

Each card shows:
- Title and word count
- Last updated time
- Per-platform status pill (Medium, Hashnode, Dev.to)
- Gate result (pass/warn/fail)
- One primary action button that reflects the next logical step

Top bar: search, status filter, platform filter, New Article button (top right, always visible).

---

### 3. Drafting
**Frequency:** core daily loop
**Feel:** distraction-free writing surface; AI is a presence in the margin, not in the way

Sub-steps:
1. Create from prompt or blank
2. Claude/Codex runs in CLI, output lands in editor
3. User reads and edits inline
4. User adds margin comments to request AI revisions on a section
5. AI applies patch, diff shown in-place
6. User accepts or rejects each patch

Editor has two modes: Write (full focus) and Review (comments + diff visible).

---

### 4. Conversion and inspection
**Frequency:** before every publish
**Feel:** diagnostic, precise, no ambiguity

Renders article as it will appear on each selected platform. Runs a gate check per destination:
- Code block integrity (no splits, no language label corruption)
- Section count matches source
- Image count matches source
- No missing tail/conclusion
- No duplicated fragments

Result is pass, warn, or fail per destination. Warn allows proceeding. Fail blocks publish until resolved.
Artifacts (dumped HTML, chunk logs, failure taxonomy) are stored and linkable.

---

### 5. Scheduling and publish
**Frequency:** end of each article lifecycle
**Feel:** decisive, one action per step, status is immediate

Steps:
1. Select destinations (pre-filled from draft state)
2. Choose: publish now or pick date/time per platform
3. Confirm
4. Per-platform outcome shown immediately (success, queued, failed)

Failed destinations show reason and a retry action. Successful ones link to live URL.

---

## Click and Signal/Cue Model

### Primary action rule
Every screen has exactly one primary action. It is the thing the user is expected to do next. Secondary actions are visually quieter. Destructive or irreversible actions require a second confirmation click.

### Signal tiers

| Tier              | Color         | Meaning                                 |
|-------------------|---------------|-----------------------------------------|
| In progress       | Indigo/blue   | Something is running or pending         |
| Attention needed  | Amber         | User input required, not blocking       |
| Blocking          | Red           | Cannot proceed without resolution       |
| Done              | Green (muted) | Completed, no action needed             |

Status is always per-platform. Never collapsed into a single aggregate badge. The user must always know which platform has the problem.

### Card-level next-action cue

The primary action button on each article card changes based on state:

| Card state                         | Primary action |
|------------------------------------|----------------|
| No drafts yet                      | Push drafts    |
| Drafts exist, inspection not run   | Inspect        |
| Inspection passed                  | Schedule       |
| Scheduled                          | View schedule  |
| All platforms published            | View live      |

The card itself tells the user what to do next. No need to open the article to find out.

---

## Article Card Anatomy

```
┌─────────────────────────────────────────────────┐
│  Title of the article                      [···] │
│  Updated 2h ago · 1,800 words                    │
│                                                  │
│  Medium    [Draft v2  ]                          │
│  Hashnode  [Pending   ]                          │
│  Dev.to    [Draft v1  ]                          │
│                                                  │
│  Gate: ✓ Pass               → [Schedule]         │
└─────────────────────────────────────────────────┘
```

- Top right [···] opens a context menu (edit, delete, duplicate, move to archive)
- Platform pills are clickable and link to the draft on that platform
- Gate result links to the inspection report
- Primary action button is always bottom right

---

## Screen Inventory

| Screen              | Route          | Status    |
|---------------------|----------------|-----------|
| Overview            | /              | v1 exists |
| Create article      | /create        | planned   |
| Editor              | /article/:id   | planned   |
| Inspection          | /inspect/:id   | planned   |
| Publish / schedule  | /publish/:id   | planned   |
| Platform connect    | /settings      | planned   |
