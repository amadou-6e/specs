# Publish / Schedule — Components Spec

---

## ArticleHeaderStrip

Read-only summary of the article being published.

### Props
- `title: string`
- `wordCount: number`
- `updatedAt: string`
- `gate: 'pass' | 'warn' | 'fail'`
- `onEdit: () => void`

"Edit" link is a small secondary action next to the title.

---

## DestinationRow

One row per available publishing destination.

### Props
- `platform: 'medium' | 'hashnode' | 'devto'`
- `draftStatus: string`
- `draftLabel: string`
- `error: string | null`
- `checked: boolean`
- `publishMode: 'now' | 'scheduled'`
- `scheduledAt: Date | null`
- `onCheck: () => void`
- `onModeChange: (mode: 'now' | 'scheduled') => void`
- `onScheduledAtChange: (date: Date) => void`

### States
- Available + checked: full row active, time controls visible
- Available + unchecked: row dimmed, time controls hidden
- Error: checkbox disabled, row muted, reason text shown, "Fix" link

### Publish mode toggle
Two-option segmented control: "Now" / "Scheduled".
Appears only when row is checked.

### Date/time picker
Appears inline below the row when mode is "Scheduled".
Minimum date: current time + 10 minutes.
Timezone shown and adjustable.

---

## ConfirmSummary

Plain-language summary of the pending publish action.

### Props
- `destinations: ConfirmedDestination[]`

Renders as a single prose sentence or short list.
Example: "Publishing to Medium now, scheduling Hashnode for Apr 4 at 09:00."
Updates in real time as the user checks destinations or changes times.

---

## ActionBar

### Props
- `canConfirm: boolean`
- `isPublishing: boolean`
- `onBack: () => void`
- `onConfirm: () => void`

### States
- Default: back link + disabled or enabled Confirm button
- Publishing: spinner + "Publishing…", back disabled

---

## OutcomeScreen

Replaces the form after publish is complete.

### Props
- `results: PublishResult[]`

### Per result row
- `platform: string`
- `status: 'published' | 'scheduled' | 'skipped' | 'failed'`
- `url: string | null` (for published)
- `scheduledAt: string | null` (for scheduled)
- `reason: string | null` (for skipped/failed)

### Bottom actions
- "Back to overview" (primary)
- "View article" (secondary, opens first published URL in new tab)
