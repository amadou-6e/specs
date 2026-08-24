# Create Article — Components Spec

---

## StepIndicator

Horizontal step tracker in Zone B.

### Props
- `steps: string[]` — step labels
- `current: number` — zero-indexed active step

### States
- Past step: filled circle with checkmark, label dimmed
- Active step: filled accent circle, label bright
- Future step: empty circle, label muted

---

## PromptTextarea

Large freeform input for the article brief.

### Props
- `value: string`
- `onChange: (v: string) => void`
- `placeholder: string`

### Behaviour
- Auto-grows vertically up to 400px, then scrolls
- Character count shown bottom-right when over 200 chars
- No hard character limit

---

## SuggestedPromptChips

Row of clickable example prompts below the textarea.

### Props
- `suggestions: string[]`
- `onSelect: (s: string) => void`

### Behaviour
- Clicking a chip copies it into the PromptTextarea
- Chips are dismissed (hidden) after the textarea has any content

---

## SkillCard

Selectable card in the skill/template grid.

### Props
- `id: string`
- `name: string`
- `description: string`
- `selected: boolean`
- `onSelect: () => void`

### States
- Default
- Selected: accent border, filled background tint
- Disabled: muted, not clickable (e.g. requires pro plan)

### Skills available (initial set)
- Technical deep-dive
- Tutorial / how-to
- Comparison / benchmark
- Opinion / perspective
- Quick tip

---

## ProviderToggle

Two-option toggle: Claude vs Codex.

### Props
- `value: 'claude' | 'codex'`
- `onChange: (v: string) => void`

Shows provider logo + label. If a provider has no API key configured, shows a warning icon and links to /settings.

---

## WordCountSlider

Range slider for target length.

### Props
- `value: number`
- `min: 500`
- `max: 4000`
- `step: 100`
- `onChange: (v: number) => void`

Displays current value as "~N words" label. Snaps to 500/1000/2000/3000/4000 for easy selection.

---

## DestinationChecklist

List of available publishing destinations.

### Props
- `platforms: Platform[]`
- `selected: string[]`
- `onChange: (selected: string[]) => void`

### Platform item states
- Connected + selected: checked, green dot
- Connected + unselected: unchecked, green dot
- Session expired: unchecked, amber warning icon + "Reconnect" link
- Not configured: muted, "Add in Settings" link, not checkable

---

## ConfigSummaryPanel

Right panel (Zone D). Read-only live summary.

### Props
- `prompt: string`
- `skill: string | null`
- `provider: string`
- `destinations: string[]`

Updates in real time as the user progresses through steps.

---

## ActionBar

Fixed bottom bar.

### Props
- `step: number`
- `totalSteps: number`
- `canProceed: boolean`
- `isGenerating: boolean`
- `onBack: () => void`
- `onNext: () => void`
- `onGenerate: () => void`

### States
- Steps 1–2: shows Back (if not step 1) + Next
- Step 3: shows Back + Generate
- Generating: Next/Generate replaced by spinner + "Generating…", Back disabled
