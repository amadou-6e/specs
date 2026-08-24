# Layout tool — shape reconstruction path

The layout tool converts a text-free raster design into editable shapes and layout regions. Reconstruction is intentionally reviewable: the pipeline proposes geometry and colors, while the user confirms uncertain inputs and can correct every detected shape.

## Required workflow

```text
Source image
    ↓
1. Remove text in the Text tool
    ↓
2. Detect and confirm the page background color
    ↓
3. Reconstruct shapes
       ├─ detect monotonic-color regions
       ├─ inspect and modify region masks
       ├─ standard or additive fitting
       └─ rerun fitting from corrected masks
    ↓
4. Review and manually adjust shape bounds
    ↓
5. Accept shapes as editable layout elements
```

Text remains stored in the HTML/text layer. Shape reconstruction operates on the text-erased background so glyphs do not fragment flat-color regions, distort corners, or become false shapes.

## 1. Text-removal prerequisite

When the Layout tool opens, show a compact notice above the reconstruction controls:

> For more accurate shape detection, remove text first. Existing HTML text remains editable and will be restored above the reconstructed layout.

The notice has three states:

- **Text removed:** show a quiet confirmation and continue automatically.
- **Text detected but not removed:** show `Open Text tool` and `Continue anyway`.
- **Unknown:** offer `Check for text`.

Continuing with text is allowed, but the result is marked as lower-confidence. The Layout tool must not silently erase text itself.

## 2. Background-color detection and confirmation

The first reconstruction step estimates the page background color:

1. Sample pixels connected to the image boundary.
2. Reject small isolated edge objects and obvious foreground components.
3. Cluster near-identical colors to tolerate antialiasing and compression.
4. Select the dominant boundary-connected color.
5. Report the color, confidence, and supporting pixel fraction.

The user confirms the estimate before shape detection:

```text
BACKGROUND

Estimated color       [ ■  #F4F2ED ]
Confidence              High
Boundary coverage       78%

[ Pick from image ]  [ Enter value ]  [ Confirm background ]
```

The user can confirm it, pick a pixel or region, enter an exact value, or rerun estimation. Changing a confirmed background invalidates downstream masks and fits and requires regeneration.

## 3. Shape reconstruction

Region detection and shape fitting are two stages of one Shape Reconstruction tool. The user does not switch tools between them.

After background confirmation, the initial run:

1. Segments connected foreground regions by monotonic or dominant fill color.
2. Creates one editable mask per proposed region.
3. Fits standard or additive geometry to each eligible mask.
4. Shows the mask and fitted geometry together for review.

Each proposal retains:

- Region ID and pixel mask.
- Bounding box.
- Estimated fill color.
- Area and fill ratio.
- Parent and child relationships where known.
- Segmentation confidence.
- Source method and parameters.

Canvas diagnostics include the text-erased image, foreground mask, dominant-color regions, selected-region mask, fitted geometry, fit residual, and additive steps. Diagnostic views never mutate the result.

### Editable region masks

The detected mask is the exact pixel input supplied to shape fitting. After the initial detection and fitting run, the user can:

- Paint pixels into the selected mask.
- Erase pixels from the selected mask.
- Merge multiple region masks.
- Split one region into separate masks.
- Restore the original automatic mask.

Every mask edit creates a new mask version and marks only that region's fit as stale. The user can then choose `Rerun shape fitting`, which fits the current edited masks without repeating background estimation or automatic region detection.

`Rerun region detection` remains available when segmentation settings or automatic region boundaries need regeneration. Existing manual mask versions remain recoverable.

### Shape fitting

Initial shape families are rectangles, rounded rectangles, circles or ellipses, composite rectangle unions, and irregular masks retained for manual handling.

#### Standard mode

Standard mode attempts the smallest suitable primitive. It prefers one rectangle, rounded rectangle, circle, or ellipse when fit quality is sufficient and must not force an irregular region into a misleading primitive.

#### Additive mode

Additive reconstruction is based on `design_languages/tools/hierarchical_fit/debug_additive_rects.py` in the original BlogHub specification workspace. The experimental tooling source is not vendored into the central specs repository. It reconstructs a complex silhouette as a union of rectangles fitted inside its mask:

1. Find the largest axis-aligned rectangle fully contained in the unexplained mask.
2. Grow it against the complete region mask, allowing overlap with accepted rectangles.
3. Add it to the reconstruction.
4. Remove covered pixels from the unexplained mask.
5. Repeat until the next rectangle is too small or the maximum count is reached.
6. Fit eligible outer corner radii.
7. Report uncovered pixels, overclaim, IoU, and the final union.

This fitter remains experimental. It currently works best for axis-aligned, flat-color shapes and needs further development for rotated geometry, arbitrary curves, and consistently accurate corner reconstruction.

```text
FITTING

Mode                     [ Auto       v ]
Additive reconstruction  [ On           ]
Maximum pieces           [ 6            ]
Minimum piece area       [ 1500 px²     ]
Fit outer corners        [ On           ]

[ Detect and fit shapes ]
[ Rerun shape fitting ]
```

Additive reconstruction can be:

- **Off:** use only the standard primitive fitter.
- **On:** allow additive decomposition for complex regions.
- **Auto:** try a standard primitive first and use additive reconstruction only when it fails its quality threshold.

All intermediate additive steps are preserved so the user can inspect each accepted rectangle. Changing fitting settings invalidates geometry while preserving the current automatic or manually edited masks.

## 4. Manual geometry review

Every proposal appears as an editable canvas overlay with handles and numeric geometry controls. The user can:

- Move or resize the complete shape.
- Enter exact `x`, `y`, `width`, and `height`.
- Adjust individual additive rectangles.
- Add or remove an additive rectangle.
- Change primitive type.
- Adjust outer corner radii.
- Merge or split regions.
- Reject and restore false positives.

For additive shapes, show both the outer union box and individual piece boxes. Editing the union transforms the composite; editing a piece changes only that piece. The active level must be visually explicit.

Manual changes create a proposal version and never overwrite raw detector output.

## 5. Acceptance and editor handoff

Accepted proposals become ordinary shape layers. Preserve relationships among the source pixels, detector mask, automatic fit, manual fit, fill-color estimate, and associated HTML text.

The basic shape editor then handles borders, border colors and thickness, shadows, gradients, transparency, images, texture fills, rotation, perspective, SVG paths, semantic grouping, nested color roles, and conversion into the layout grid. Those capabilities are downstream of shape fitting and do not need to be inferred perfectly during this first stage.

## Proposed reconstruction state

```json
{
  "background": {
    "color": "#F4F2ED",
    "confidence": 0.94,
    "confirmed": true
  },
  "settings": {
    "fit_mode": "auto",
    "additive_enabled": true,
    "max_pieces": 6,
    "min_piece_area": 1500,
    "fit_outer_corners": true
  },
  "regions": [
    {
      "id": "region_01",
      "bbox": {"x": 120, "y": 88, "width": 420, "height": 216},
      "fill": "#D98B64",
      "method": "additive_rectangles",
      "confidence": 0.91,
      "fit": {
        "type": "composite",
        "pieces": [
          {"x": 120, "y": 88, "width": 420, "height": 150},
          {"x": 186, "y": 202, "width": 354, "height": 102}
        ],
        "iou": 0.982,
        "overclaim_pixels": 0,
        "uncovered_pixels": 238
      },
      "status": "needs_review",
      "manually_adjusted": false
    }
  ]
}
```

## Implementation boundary

The browser layout editor already supports zones, shapes, colors, cutouts, and drag/resize behavior. It does not yet invoke raster segmentation or shape fitting.

The first implementation milestone is:

1. Add the prerequisite and background-confirmation states.
2. Implement the unified Shape Reconstruction contract containing region detection, editable masks, standard/additive fitting, and refitting.
3. Render returned masks and bounds as selectable overlays.
4. Connect overlays to the existing drag, resize, and JSON state mechanisms.
5. Preserve raw detection and manual corrections as separate versions.
