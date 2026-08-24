# Text Tool — Layout and Interaction Specification

> The broader three-column user/agent collaboration architecture is the product
> goal state. See [GOAL_STATE.md](GOAL_STATE.md).

## Purpose

The Text Tool turns text in a raster image into something the user can remove,
extract, or change without rebuilding the surrounding design.

It has three modes:

1. **Erase text** — remove detected text and reconstruct the background.
2. **Export to HTML** — extract text, position, and typography into editable HTML.
3. **Modify text** — replace text while retaining the original visual treatment.

Only **Erase text** is functional today. Export and Modify are visible navigation
states so we can agree on their workflows before implementing them.

## Design principles

- The image is always the primary object. Controls should not obscure it.
- Automatic processing should produce a useful result in one action.
- Every automatic decision should remain inspectable through result stages.
- Users need a manual escape hatch when OCR, reconstruction, or classification is
  imperfect.
- Destructive-looking actions should be reversible or operate as new versions.
- Technical pipeline names may appear in diagnostics, but the default interface
  should use task-oriented language.

## Desktop shell

The current desktop layout uses a flexible image workspace and a fixed `390 px`
control panel.

```text
┌──────────────────────────────────────────────────────┬───────────────────────┐
│ BlogHub · Design Tools                 [Status pill] │ BlogHub · Text        │
│ Text workspace                                      ├───────────────────────┤
├──────────────────────────────────────────────────────┤ ① Erase text          │
│                                                      │ ② Export to HTML      │
│                                                      │ ③ Modify text         │
│                   IMAGE STAGE                        ├───────────────────────┤
│                                                      │                       │
│            upload prompt or canvas                   │ Active mode controls  │
│                                                      │                       │
│                                                      │                       │
├──────────────────────────────────────────────────────┤                       │
│ Drag to select residual region     Download result  │                       │
└──────────────────────────────────────────────────────┴───────────────────────┘
```

### Persistent regions

| Region | Purpose |
| --- | --- |
| Workspace header | Tool title and current operation/status |
| Image stage | Source image, result, diagnostic stage, or selection overlay |
| Stage footer | Contextual canvas instruction and result download |
| Mode navigation | Switch between Erase, Export, and Modify |
| Control panel | Options and actions for the selected mode |

## Mode 1: Erase text

### Primary workflow

```text
Upload image
    ↓
Choose detection quality
    ↓
Run automatic erasure
    ↓
Inspect final image or processing stages
    ↓
Optional: select a residual region and fill it
    ↓
Download result
```

### Default options

| Option | Value | Meaning |
| --- | --- | --- |
| Detection quality | High recall | Validated OCR path; slower but less likely to miss small text |
| Alternate quality | Fast | Faster detector path; may miss small or low-contrast text |
| Automatic reconstruction | Pipeline default | Monotonic prefill, TMIM reconstruction, paragraph grouping, and final cleanup |
| Manual cleanup | Rectangle fill | Estimate the surrounding background and fill the selected rectangle |

### State E0 — No image

```text
Workspace                                  Panel
┌───────────────────────────────────┐      ┌──────────────────────────┐
│                                   │      │ ① ERASE TEXT             │
│       [ T ]                       │      │                          │
│ Erase text without losing design │      │ Upload source image      │
│ Upload, erase, then correct       │      │ PNG, JPG, or WebP        │
│ residuals manually.              │      │                          │
│       [ Choose image ]            │      │ Detection quality        │
│                                   │      │ [High recall          ▾] │
└───────────────────────────────────┘      │ [Run text erasure] off   │
                                         └──────────────────────────┘
```

Visible behavior:

- Status reads **Choose an image to begin**.
- Erase, report, fill, and download actions are disabled.
- The same file picker is reachable from the central call to action and the panel.
- Dragging an image over the upload area highlights it.

### State E1 — Image loaded

- The source image replaces the empty state.
- Status reads **Ready to erase**.
- The source filename is shown in the upload control.
- **Run text erasure** becomes enabled.
- Result stages still show an instructional empty state.
- Canvas selection is not active until an automatic job exists.

Design question: should users be allowed to run manual fill on the original image,
or should manual tools remain locked until OCR has produced a job?

### State E2 — Processing

```text
Panel
┌──────────────────────────────┐
│ Detection quality            │
│ [High recall              ▾] │
│ [Run text erasure] disabled │
│ ◌ Detecting and             │
│   reconstructing text…      │
└──────────────────────────────┘
```

- Status reads **Running OCR, TMIM, and paragraph cleanup…**.
- The quality selector remains visible but should be treated as locked for the run.
- Erase and manual fill actions are disabled.
- The current image remains visible.

Proposed improvement: express progress as named phases rather than an indefinite
spinner:

1. Detecting text
2. Classifying backgrounds
3. Reconstructing variable regions
4. Cleaning monotonic regions
5. Preparing comparison

### State E3 — Automatic result

The final image is loaded into the canvas and these diagnostic stages appear:

| UI label | Artifact | What it explains |
| --- | --- | --- |
| Original | `0_original.png` | Untouched source |
| Monotonic prefill | `2_prefilled.png` | Regions replaced from a stable local background |
| TMIM reconstruction | `4_tmim_scoped.png` | Neural reconstruction result |
| Change intensity | `5_tmim_change_intensity.png` | Per-pixel amount changed by TMIM |
| Paragraph decisions | `6_paragraph_boxes.png` | Merged OCR regions and background decisions |
| Final mask | `7_paragraph_mask.png` | Pixels/regions selected for final cleanup |
| Final image | `8_final.png` | Completed pipeline output |
| Comparison | `9_comparison.png` | Labeled before/after view |

Additional actions:

- **Open report** opens the complete vertical processing report.
- Clicking a stage makes it the active canvas image.
- **Download result** downloads whichever image is currently displayed.
- Drawing on the canvas creates a residual-cleanup rectangle.

Design question: **Download result** currently follows the displayed diagnostic
stage. It may be safer for the primary download to always target the latest final
result and expose a separate **Download this stage** action.

### State E4 — Residual selected

```text
Canvas                                    Panel
┌───────────────────────────────┐         ┌──────────────────────────┐
│                               │         │ Residual cleanup  MANUAL │
│       ┌──────────────┐        │         │ Select a rectangle…      │
│       │ text smear   │        │         │ x 120 · y 88             │
│       └──────────────┘        │         │ w 146 · h 31             │
│                               │         │ [Fill selected region]   │
└───────────────────────────────┘         └──────────────────────────┘
```

- The rectangle is lime with a translucent fill.
- Coordinates are shown in source-image pixels, not display pixels.
- Tiny accidental selections are discarded.
- **Fill selected region** becomes enabled.

The current manual method samples a connected local background estimate and fills
the complete selected rectangle with the estimated RGB color. It is best suited to
text on monotonic backgrounds.

### State E5 — Manual fill applied

- A new versioned `manual_fill_N.png` is created.
- The filled image becomes the current canvas image.
- Status reports the estimated RGB fill color.
- The selection clears.
- Another region can be selected and filled, creating another version.

Required improvement: add visible **Undo** and **Redo** controls. The backend
already creates versioned images, so history can be represented without mutating
earlier results.

### Error state

Errors currently appear only in the status pill. Proposed layout:

```text
┌──────────────────────────────────────┐
│ ! Text erasure could not complete   │
│   Short user-facing explanation.    │
│   [Try again] [Show technical info] │
└──────────────────────────────────────┘
```

The current source image and selected options should remain intact after failure.

## Proposed advanced erase options

These should live behind an **Advanced** disclosure so the first-run experience
continues to have one obvious action.

| Control | Options | Purpose |
| --- | --- | --- |
| Reconstruction scope | Text regions / Entire image | Limit TMIM changes to OCR regions or permit global reconstruction |
| Background handling | Auto / Monotonic fill only / Neural only | Override automatic background classification |
| OCR overlay | Off / Words / Paragraphs | Show what the detector believes is text |
| Preserve regions | Add rectangles | Protect logos, illustrations, or UI elements from modification |
| Cleanup method | Background fill / Inpaint / Clone nearby | Choose a manual correction method |
| Comparison view | Result / Side-by-side / Wipe / Difference | Inspect whether design details were changed |

Recommended default:

```text
Automatic background handling
TMIM limited to detected text regions
OCR overlay off
Result comparison available as a wipe
```

## Mode 2: Export text to HTML

This mode is not implemented. Its purpose is to export recognized text as editable
HTML positioned over the reconstructed text-free background.

### Proposed layout

```text
Workspace                                  Panel
┌───────────────────────────────────┐      ┌──────────────────────────┐
│ [Background] [Text] [Combined]   │      │ ② EXPORT TO HTML        │
│                                   │      │ Detection               │
│  ┌──────── editable region ────┐ │      │ Language [Auto       ▾] │
│  │ Detected headline           │ │      │ Grouping [Paragraphs ▾] │
│  └─────────────────────────────┘ │      │                          │
│                                   │      │ Output                   │
│  ┌──────── editable region ────┐ │      │ ☑ Absolute positioning  │
│  │ Body copy…                  │ │      │ ☑ Include background    │
│  └─────────────────────────────┘ │      │ ☐ Responsive conversion │
│                                   │      │                          │
│                                   │      │ [Generate HTML]         │
└───────────────────────────────────┘      └──────────────────────────┘
```

### Proposed visible states

1. **Awaiting image** — upload prompt and disabled generation action.
2. **Detecting** — OCR and layout analysis progress.
3. **Review regions** — word/line/paragraph boxes with editable recognized text.
4. **Preview HTML** — toggle background, text layer, and combined render.
5. **Export ready** — download HTML bundle, copy markup, or inspect CSS.

### Proposed export choices

| Choice | Recommended default |
| --- | --- |
| Text grouping | Paragraphs |
| Positioning | Absolute, preserving the screenshot |
| Background | Text-free reconstructed image |
| Typography | Closest web-safe or available font match |
| Asset packaging | HTML + CSS + images in a ZIP |
| Responsive behavior | Off; explicit opt-in because inference can change layout |

Open questions:

- Should the first export optimize for pixel fidelity or responsive semantics?
- Do we export each line independently or paragraphs with natural wrapping?
- How should uncertain OCR characters be surfaced before export?
- Should font matching use local fonts, web fonts, or CSS fallbacks only?

## Mode 3: Modify text

This mode is not implemented. It combines text removal with a replacement text
layer rendered back into the image.

### Proposed layout

```text
Workspace                                  Panel
┌───────────────────────────────────┐      ┌──────────────────────────┐
│                                   │      │ ③ MODIFY TEXT           │
│  ┌──────── selected text ──────┐ │      │ Original                │
│  │ Summer collection          │ │      │ Summer collection       │
│  └─────────────────────────────┘ │      │                          │
│                                   │      │ Replacement             │
│                                   │      │ [Autumn collection    ] │
│                                   │      │ Font       [Matched  ▾] │
│                                   │      │ Size [42] Color [■]     │
│                                   │      │ Align [L] [C] [R]       │
│                                   │      │                          │
│                                   │      │ [Apply replacement]     │
└───────────────────────────────────┘      └──────────────────────────┘
```

### Proposed workflow

1. Upload and detect text.
2. Click a detected word, line, or paragraph.
3. Review/correct its OCR transcription.
4. Enter replacement text.
5. Start with matched typography and allow overrides.
6. Reconstruct the old text region.
7. Preview the new text non-destructively.
8. Apply and export the flattened image or editable HTML.

### Proposed controls

- Original and replacement copy
- Font family or matched-font candidates
- Font size, weight, style, line height, and letter spacing
- Text color sampled from the original glyphs
- Alignment and vertical anchoring
- Region width and wrapping behavior
- Fit behavior: keep size, shrink to fit, or expand region
- Background reconstruction method
- Before/after and text-layer visibility

Open questions:

- Is replacement scoped to a whole paragraph or can users edit individual words?
- Should a replacement remain as an editable layer until export?
- When replacement copy is longer, should the box expand, shrink typography, or ask?
- Should users be able to reuse a detected style across multiple text regions?

## Shared interaction states

All three modes should use the same vocabulary and visual treatment:

| State | Treatment |
| --- | --- |
| Empty | Centered explanation and one primary upload action |
| Ready | Image visible, primary action enabled |
| Processing | Named progress phase; editing controls disabled |
| Review | Canvas overlays and corresponding panel list |
| Selection | Lime outline on canvas and selected card in panel |
| Success | Result visible, export/download action enabled |
| Warning | Amber inline notice; result remains usable |
| Error | Persistent inline message with retry |

## Responsive behavior

The current implementation keeps the image workspace full-screen and turns the
right panel into a floating panel below `900 px`.

Proposed mobile behavior:

- Use a full-width image viewport.
- Present controls as a draggable bottom sheet instead of a tall floating panel.
- Keep mode navigation horizontally scrollable at the top of the sheet.
- Provide zoom/pan mode and selection mode as explicit canvas tools; touch dragging
  cannot safely mean both.
- Pin the primary action and undo to the bottom edge.

## Accessibility

- Every canvas operation needs a non-canvas alternative, such as numeric rectangle
  fields or an OCR-region list.
- Active stages and modes should expose `aria-selected`.
- Processing should announce phase changes with an `aria-live` region.
- Do not communicate paragraph/background decisions by green and orange alone;
  include labels or patterns.
- All controls and detected-region selection must be keyboard reachable.
- The lime selection outline needs a second high-contrast edge on light images.

## Current implementation map

| Concern | File |
| --- | --- |
| Tool markup | `index.html` |
| Visual styling and responsive shell | `style.css` |
| Browser state, upload, stage viewer, and manual selection | `main.js` |
| Erase and manual-fill API | `backend/routers/text_tool.py` |
| Automatic erasure pipeline | `.spec/design_languages/tools/text_eraser/run_pipeline.py` |
| Runtime job artifacts | `jobs/<job-id>/` |

The tool is served at `/design/text/`. Uploaded sources and generated outputs are
currently stored below this tool folder in `jobs/`.

## Suggested discussion order

1. Confirm whether the two-pane shell is the right permanent layout.
2. Decide if result download follows the final output or the currently viewed stage.
3. Choose which comparison interaction should be primary: side-by-side, wipe, or
   stage cards.
4. Decide how much pipeline terminology is appropriate in the normal interface.
5. Agree on the first manual cleanup tools and undo/history behavior.
6. Choose whether HTML export prioritizes fidelity or semantic responsiveness.
7. Define overflow behavior for replacement text in Modify mode.
