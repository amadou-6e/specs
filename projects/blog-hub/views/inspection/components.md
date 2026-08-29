# Inspection — Components Spec

> Design blocked: no authoritative `inspection.drawio` exists. Treat the component notes
> below as historical planning input only.

---

## GateSummaryBar

Sticky bar below the top nav.

### Props
- `overallResult: 'pass' | 'warn' | 'fail'`
- `inspectedAt: string`
- `onRerun: () => void`
- `onProceed: () => void`
- `canProceed: boolean` (false when result is 'fail')

---

## PlatformTabStrip

Tab strip with one tab per destination.

### Props
- `platforms: PlatformInspection[]`
- `active: string`
- `onChange: (platform: string) => void`

### Per tab
- Platform label
- Gate pill: ✓ pass (green), ⚠ warn (amber), ✗ fail (red)

---

## CheckList

Vertical list of gate checks for the active platform.

### Props
- `checks: Check[]`
- `selectedCheckId: string | null`
- `onSelect: (id: string) => void`

### Check item props
- `id: string`
- `label: string` — human-readable name
- `result: 'pass' | 'warn' | 'fail'`
- `detail: string` — short summary (e.g. "4 / 4 blocks intact")

### Check item states
- Default
- Selected: highlighted row, left accent border, artifact panel updates
- Pass: green icon ✓
- Warn: amber icon ⚠
- Fail: red icon ✗

---

## ArtifactPanel

Right panel showing evidence for the selected check.

### Props
- `check: Check | null`
- `artifact: Artifact | null`

### Artifact variants (by check type)

**code_blocks:**
Renders each code block found in the draft as a syntax-highlighted block.
Label: "Block N of M" per item.

**images:**
Table of expected vs found image URLs.
Missing rows highlighted red.

**sections:**
Two-column diff: expected headings (from source) vs detected headings (from draft).
Missing or reordered rows highlighted.

**tail:**
Monospace text block showing last 500 characters of the imported draft.
If the tail check failed: the truncation point is highlighted in red.

### Header
- Selected check label
- "View full dump" link (opens raw artifact in new tab)

---

## RerunButton

Triggers a fresh inspection run.

### States
- Default: "Re-run inspection"
- Running: spinner + "Running…", disabled
- Done: reverts to default, platform tabs update with new results
