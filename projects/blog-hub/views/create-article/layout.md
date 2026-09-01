# Create Article — Layout Spec

> UI authority: [create-article.drawio](create-article.drawio). This layout is a derived
> reading aid, not an independent source of UI behavior.

## Purpose
Entry point for new content. The user describes what they want, configures generation options, and kicks off an AI drafting job.

---

## Page Zones

```
┌─────────────────────────────────────────────────────────────────┐
│  ZONE A: Top nav (fixed, 48px)                                  │
├─────────────────────────────────────────────────────────────────┤
│  ZONE B: Step indicator (sticky, 40px)                          │
├──────────────────────────────────────┬──────────────────────────┤
│                                      │                          │
│  ZONE C: Step content (scrollable)   │  ZONE D: Config panel   │
│                                      │  (sticky, 320px wide)   │
│                                      │                          │
├──────────────────────────────────────┴──────────────────────────┤
│  ZONE E: Action bar (fixed bottom, 56px)                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Steps

Three steps, linear. User cannot skip forward. Can go back freely.

1. **Prompt** — what is this article about
2. **Configure** — skill/template, AI provider, tone, length target
3. **Destinations** — which platforms to target

Step indicator in Zone B shows current step and completion state of previous steps.

---

## Zone C: Step content

Step 1 (Prompt):
- Large textarea centred in the zone, ~60% width, min 200px height
- Title field above it (optional at this stage)
- Suggested prompts below as clickable chips (dismissed after first use)

Step 2 (Configure):
- Skill/template selector (card grid, single-select)
- AI provider toggle: Claude / Codex
- Tone selector: Technical / Conversational / Tutorial
- Target word count slider: 500–4000 words

Step 3 (Destinations):
- Checkbox list of connected platforms with their connection health
- Warning shown for any platform with an expired or missing session

---

## Zone D: Config panel (desktop only)

Persistent right panel visible across all three steps.
Shows a live summary of current selections:
- Prompt excerpt (first 120 chars)
- Selected skill
- Provider
- Target platforms

Hidden on tablet/mobile; those users see a summary sheet before the final action.

---

## Zone E: Action bar

Left: Back button (hidden on step 1).
Right: Next (steps 1–2), Generate (step 3).

Generate is disabled if no prompt entered or no destinations selected.
While generating: button shows spinner and "Generating…" label; back button is disabled.

---

## Post-generation

On success: navigate to /article/:id (the editor).
On failure: stay on create screen, show error banner above action bar with reason and retry.
