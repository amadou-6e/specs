# Overview — Components Spec

---

## ArticleCard

The primary unit of the overview grid.

### Anatomy
```
┌─────────────────────────────────────────────────┐
│  Title of the article                      [···] │
│  Updated 2h ago · 1,800 words                    │
│  ─────────────────────────────────────────────── │
│  Medium    [Draft v2  ]                          │
│  Hashnode  [Pending   ]                          │
│  Dev.to    [Draft v1  ]                          │
│  ─────────────────────────────────────────────── │
│  Gate: ✓ Pass               → [Schedule]         │
└─────────────────────────────────────────────────┘
```

### Props
- `title: string`
- `updatedAt: string` (relative, e.g. "2h ago")
- `wordCount: number`
- `destinations: DestinationStatus[]`
- `gate: 'pass' | 'warn' | 'fail' | 'pending' | 'none'`
- `primaryAction: ActionConfig` (label + handler derived from state)

### States
- Default
- Hover: subtle background lift, border brightens
- Selected: left border accent (indigo), background tint
- Error: red left border accent, error destination highlighted

### DestinationStatus (sub-component, inline pill row)
- `platform: 'medium' | 'hashnode' | 'devto'`
- `status: 'draft' | 'ready' | 'error' | 'pending' | 'published' | 'none'`
- `label: string` (e.g. "Draft v2", "Published", "—")
- Clicking a pill with a draft URL opens that URL in a new tab
- Pill with status `none` is non-clickable

### Gate Badge
- Displays gate result with icon: ✓ Pass (green), ⚠ Warn (amber), ✗ Fail (red), — (muted)
- Clicking links to the inspection view for this article

### Primary Action Button
- Always bottom-right of card
- Label and handler driven by `primaryAction` prop
- State-to-action mapping (see workflows spec)
- Triggers navigation or API call depending on action type

### Context Menu [···]
- Opens on click (not hover)
- Options: Edit, Duplicate, Archive, Delete
- Delete requires confirmation (inline, not modal)

---

## FilterBar

### Components inside FilterBar
1. `SearchInput` — debounced text input, clears on Escape
2. `StatusFilterGroup` — pill toggle group, single-select, "All" deselects others
3. `PlatformFilterGroup` — pill toggle group, multi-select
4. `ArticleCount` — passive label, updates as filters change

---

## TopNav

### Left section
- `BrandMark` — logo + wordmark, links to /
- `NavLinks` — list of nav items; active item has filled background pill

### Right section
- `PlatformHealthDot` — green dot + "N platforms connected" label; clicking links to /settings
- `NewArticleButton` — primary CTA, navigates to /create

---

## EmptyState

Shown when no articles match the current filters, or no articles exist at all.

- Two variants: `no-articles` (first-run) and `no-results` (filtered empty)
- `no-articles`: illustration, heading "No articles yet", subtext, New Article button
- `no-results`: heading "No articles match", subtext, "Clear filters" link

---

## SkeletonCard

Shown during loading. Matches ArticleCard dimensions exactly.
- Uses animated shimmer (CSS keyframe, no JS)
- Renders 6 skeletons in the grid on load
