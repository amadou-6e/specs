# How to write a BlogHub grid guide

Self-contained HTML spec sheets that show how a page's 12-column grid
actually controls where every element lands — text, components, spacing.
No external dependencies. Open in browser.

---

## Core idea

A grid guide is not a wireframe with guidelines drawn over it.
The column lines and baseline grid **are the primary layer** — content exists
to prove the grid works. Every element must start, end, or align to a line
you can see. If you have to move a line to fit content, the content is wrong.

---

## File structure

```
.spec/grid_guides/
  overview-grid.html   — 01 Overview / Welcome
  settings-grid.html   — 02 Settings
  how_to.md            — this file
```

Each file is self-contained HTML. All CSS is in a `<style>` block.
Header convention: `BlogHub · Grid Guide · 0N Page Name`.

---

## CSS design tokens

Defined on `:root`. Never hardcode these values anywhere else in the file.

```css
:root {
  /* Ink scale */
  --ink:  #1a1917;   /* body text */
  --ink2: #4a4845;   /* secondary text */
  --ink3: #8a887f;   /* muted / hints */
  --ink4: #b0aea8;   /* very muted */
  --line: #dddad4;   /* borders */

  /* Layout */
  --cg:  16px;       /* column gap (represents 24px gutter) */
  --mg:  40px;       /* margin zone width */
  --bl:  24px;       /* baseline unit — the fundamental vertical atom */

  /* Grid overlay colours (red tint) */
  --col-ln: rgba(214,52,36,.28);    /* column edge lines */
  --col-bg: rgba(214,52,36,.065);   /* column band fill */
  --bl-ln:  rgba(214,52,36,.09);    /* baseline grid lines */
  --lg:     rgba(214,52,36,.70);    /* local guide lines (brighter) */
}
```

---

## The 12-column grid

```css
.wf-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  column-gap: var(--cg);
  row-gap: 0;          /* never use row-gap — control height via named rows */
  position: relative;
  isolation: isolate;  /* keeps z-index layers scoped to the grid */
}
```

`isolation: isolate` is required. Without it the overlay `z-index` values
bleed into the page stacking context and the layers render out of order.

---

## Row height rules

**Every row height must be a multiple of 24px (`--bl`). No exceptions.**

| Rows | Height | Common use |
|------|--------|------------|
| 1    | 24px   | Ruler, dividers, single-label rows |
| 2    | 48px   | Nav, page headers, section headings, form fields |
| 3    | 72px   | Article rows, bio textarea, provider rows, save rows |
| 8    | 192px  | Hero zone (overview page) |

**All zone start Y positions must also be multiples of 24px.**
Calculate cumulative offsets to verify: if row 1 is 24px and row 2 is 48px,
row 3 starts at 72px (3×24 ✓).

Named grid lines use semantic labels so zones can say `grid-row: nm-s/nm-e`
instead of counting integer positions:

```css
grid-template-rows:
  [ruler-s] 24px
  [ruler-e nav-s] 48px
  [nav-e hd-s] 48px
  [hd-e s1hd-s] 48px
  ...
```

---

## Three-layer overlay system

Three absolutely-positioned divs sit inside `.wf-grid`. They share the same
`grid-template-columns` and `column-gap` as the content grid so their
column lines land exactly on content edges.

### Layer 1 — Column bands (z-index: -1)

Sits behind content. Tints each column a very faint red so you can see
the column count at a glance.

```html
<div class="col-bands">
  <div></div><div></div><!-- × 12 -->
</div>
```

```css
.col-bands {
  position: absolute; inset: 0; pointer-events: none; z-index: -1;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: 1fr;
  column-gap: var(--cg);
}
.col-bands > div { background: var(--col-bg); }
```

### Layer 2 — Baseline grid (z-index: 9)

Sits **above all zone backgrounds** so the 24px horizontal lines are visible
through every zone colour. This is the most important rule: the baseline
grid must span the full width continuously, not be clipped to individual zones.

```css
.bl-ov {
  position: absolute; inset: 0; pointer-events: none; z-index: 9;
  background-image: repeating-linear-gradient(
    to bottom,
    var(--bl-ln) 0px, var(--bl-ln) 1px,
    transparent 1px, transparent var(--bl)
  );
}
```

Do **not** put the baseline pattern on individual zone `background` properties —
it will be clipped at zone boundaries and the lines will not be continuous.

### Layer 3 — Column edge lines (z-index: 10)

One vertical line per column left edge, one on the rightmost right edge.
Sits above the baseline grid.

```html
<div class="col-lines">
  <div></div><div></div><!-- × 12 -->
</div>
```

```css
.col-lines {
  position: absolute; inset: 0; pointer-events: none; z-index: 10;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: 1fr;
  column-gap: var(--cg);
}
.col-lines > div { border-left: 1px solid var(--col-ln); }
.col-lines > div:last-child { border-right: 1px solid var(--col-ln); }
```

### Z-index summary

| Layer | z-index | What it does |
|-------|---------|--------------|
| col-bands | -1 | Column fill tint, behind content |
| content zones | 0 (flow) | Actual page elements |
| bl-ov | 9 | Baseline lines, above zone backgrounds |
| col-lines | 10 | Column edge lines, topmost structural layer |
| local guides | 20 | Zone-specific alignment aids, topmost |

---

## Local guide lines

Local guides show alignment within a single zone without spanning the full
page. They are brighter than full-page lines (`--lg` vs `--col-ln`) so the
distinction is immediately visible.

```css
.lg-v {
  position: absolute; width: 0;
  border-left: 1.5px solid var(--lg);
  pointer-events: none; z-index: 20;
}
.lg-h {
  position: absolute; height: 0;
  border-top: 1px dashed var(--lg);
  pointer-events: none; z-index: 20;
}
```

Place them inside a zone that has `position: relative`:

```html
<div class="z-pv-id" style="position:relative;">
  <div class="lg-h" style="top:24px; left:0; right:0;"></div>
  <div class="lg-h" style="top:48px; left:0; right:0;"></div>
  ...
</div>
```

**When to use local h-guides:**
- Inside multi-line zones to mark each 24px baseline step
- Inside input zones to mark the cap-height position (`top:12px` for an input
  with 11px top padding)

**When to use local v-guides:**
- To show an inset from a column edge (e.g. `left:8px` nav logo inset)

---

## Text alignment rules

**All text zones must have `padding: 0`.**

Text must start flush at the column left edge. `padding` on a zone shifts
text away from the column line, which breaks the fundamental claim that
columns guide content.

```css
.z-hero { padding: 0; overflow: hidden; position: relative; }
.z-body { padding: 0; border-left: 1px solid #e8e5e0; }
.z-lbl  { padding: 0; }
```

If a zone has a border you still want the text flush to the column edge.
The border is on the zone box; the column line is at the zone's left
`grid-column` start. These coincide correctly as long as you do not add padding.

**`line-height` must be `var(--bl)` = 24px for all body text.**

Each text element occupies exactly one (or N) baseline unit(s). Stack text
elements directly with no margin so their combined height is a predictable
multiple of 24px.

```css
.art-title { font-size: 11px; font-weight: 600; color: var(--ink); line-height: 24px; }
.art-meta  { font-size: 9px;  color: var(--ink3);                   line-height: 24px; }
```

---

## Explicit grid alignment for non-text elements

Flexbox centering (`align-items: center`) breaks baseline alignment because
it floats elements to visual midpoints that are not multiples of 24px.

Use `align-items: flex-start` + explicit `padding-top` to pin elements
to a specific baseline within their row:

```css
/* Button/pill starts at grid line 2 of a 72px row */
.z-pv-ac {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 24px 8px 0;   /* padding-top = 1×24px → second baseline */
}
```

Formula: `padding-top = (N-1) × 24px` to reach the Nth baseline in a row.
- `padding-top: 0`  → first baseline (top of row)
- `padding-top: 24px` → second baseline
- `padding-top: 48px` → third baseline

---

## Pill / badge sizing

All pills in a column must have the same visual width so the column reads
as a consistent alignment unit.

```css
.pill {
  font-size: 8px; font-weight: 700;
  letter-spacing: .06em; text-transform: uppercase;
  padding: 4px 6px;        /* 4 + 16 + 4 = 24px total height = 1 baseline */
  line-height: 16px;
  border-radius: 10px; text-align: center;
  width: 100%;             /* uniform width regardless of text length */
  box-sizing: border-box;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
```

`width: 100%` + `box-sizing: border-box` makes every pill exactly as wide
as its containing column. `text-overflow: ellipsis` handles labels that are
too long rather than letting them stretch the layout.

Pill height math: `4px top pad + 16px line-height + 4px bottom pad = 24px`
— exactly one baseline unit.

Short pill labels preferred ("Live" not "Published") to fit narrow columns
without triggering ellipsis.

---

## Form inputs

Height must be a multiple of 24px so the input box aligns to baselines:

```css
/* 48px = 1px border + 11px pad + 24px line-height + 11px pad + 1px border */
.input-f {
  height: 48px; width: 100%;
  border: 1px solid var(--line); border-radius: 4px;
  font-size: 11px; line-height: 24px;
  padding: 11px 12px;
}

/* 72px = 1 + 11 + (24×2) + 11 + 1; content height = 48px = 2 baselines */
.textarea-f {
  height: 72px; width: 100%;
  border: 1px solid var(--line); border-radius: 4px;
  font-size: 11px; line-height: 24px;
  padding: 11px 12px;
  resize: none; overflow: hidden;
}
```

The padding arithmetic is load-bearing: `11px + 24px + 11px + 2px = 48px`.
Change one value and the input no longer fits its row.

---

## Margin zones

Margin zones sit outside the 12-column grid on left and right.
They have a dashed border and rotated label to make the margin visible.

```css
.wf-mg {
  width: var(--mg); flex-shrink: 0;
  background: rgba(214,52,36,.04);
  border-right: 1px dashed rgba(214,52,36,.18);
  display: flex; align-items: flex-end; justify-content: center;
  padding-bottom: 8px;
}
.wf-mg.r { border-right: none; border-left: 1px dashed rgba(214,52,36,.18); }
.wf-mg span {
  font-size: 6px; font-family: ui-monospace, monospace;
  color: rgba(214,52,36,.45);
  writing-mode: vertical-rl; transform: rotate(180deg);
}
```

The shell is `display: flex` with `.wf-mg` + `.wf-grid` + `.wf-mg.r` as children.

---

## Ruler row

Always the first row, 24px = 1 baseline unit. Shows column numbers 1–12.

```html
<div class="ruler">
  <span>1</span><span>2</span><!-- ... --><span>12</span>
</div>
```

```css
.ruler {
  grid-column: 1/13; grid-row: ruler-s/ruler-e;
  display: grid; grid-template-columns: repeat(12,1fr);
  column-gap: var(--cg);
  background: #f0ede8; border-bottom: 1px solid var(--line);
  z-index: 5;
}
.ruler > span {
  display: flex; align-items: center; justify-content: center;
  font-size: 7px; font-family: ui-monospace, monospace;
  color: rgba(214,52,36,.55);
  border-left: 1px solid rgba(214,52,36,.14);
}
.ruler > span:last-child { border-right: 1px solid rgba(214,52,36,.14); }
```

The ruler uses its own inner grid matching the parent so column number
labels are centred inside each column band.

---

## Right bracket height annotations

A column to the right of the wireframe shows the height of each row with
a bracket glyph. Built from three divs: a bar (the bracket arm) and a label.

```css
.ann-col { padding-left: 12px; display: flex; flex-direction: column; }
.ann-sp  { height: 24px; flex-shrink: 0; }  /* offsets the ruler row */

.brk { display: flex; align-items: stretch; gap: 7px; flex-shrink: 0; }
.brk-bar {
  width: 6px; flex-shrink: 0;
  border-top: 1px solid var(--ink3);
  border-bottom: 1px solid var(--ink3);
  border-left: 1px solid var(--ink3);
}
.brk-lbl { display: flex; flex-direction: column; justify-content: center; gap: 2px; }
.brk-lbl b { font-size: 9px; font-weight: 600; color: var(--ink2); }
.brk-lbl s { font-size: 8px; font-family: ui-monospace, monospace; color: var(--ink3);
              text-decoration: none; white-space: nowrap; }
```

Each `.brk` gets an inline `style="height: Npx"` matching the row it annotates.
The `.ann-sp` at the top offsets the 24px ruler row so brackets line up with
their content rows.

---

## Span annotation rows

Below the wireframe, span rows label which columns each structural zone
occupies. One row per level of hierarchy (sidebar/content, label/input,
identity/status/action).

```css
.span-row  { display: flex; max-width: 1260px; margin: 0 auto; }
.span-mg   { width: calc(var(--mg) + 1px); flex-shrink: 0; }
.span-grid {
  flex: 1; display: grid;
  grid-template-columns: repeat(12,1fr);
  column-gap: var(--cg);
}
.sc {
  border-top: 2px solid rgba(214,52,36,.28); padding-top: 4px;
  font-size: 6px; font-family: ui-monospace, monospace;
  color: rgba(214,52,36,.65); white-space: nowrap; overflow: hidden;
}
```

Each `.sc` spans the same columns as the zone it labels:

```html
<div class="sc" style="grid-column:1/3;">sidebar · col 1–2</div>
<div class="sc" style="grid-column:3/13;">content · col 3–12</div>
```

---

## Zone table

A table at the bottom catalogues every zone: name, role, column span,
height, baseline count, and h-alignment rule. This is the authoritative
record of how the grid guide maps to the real implementation.

```css
.zt { width: 100%; border-collapse: collapse; font-size: 9px; }
.zt th {
  background: var(--ink); color: #f4f2ee;
  font-size: 8px; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; padding: 6px 10px;
}
.zt td { padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
.zt td:nth-child(3),
.zt td:nth-child(4),
.zt td:nth-child(5) { font-family: ui-monospace, monospace; }
```

Columns: **Zone | Role | Col span | Height | Baseline | H-alignment**.

A colour swatch per zone row helps visual scanning:
```html
<span class="sw" style="background:#f8f6f2; border-color:#d8d5d0;"></span>
```
```css
.sw { display:inline-block; width:10px; height:10px;
      border-radius:2px; border:1px solid rgba(0,0,0,.1); margin-right:6px; }
```

---

## Page-specific patterns

### Overview / Welcome

- Sidebar col 1: icon strip
- Hero zone col 7–12, 192px = 8×24px: 8 stacked text elements, zero padding
- Article rows col 2–10, 72px = 3×24px: platform · title · meta
- Status col 11, date col 12: pills and date labels pinned with `padding-top: 24px`
- Band row 48px between hero and article list

Key constraint: the hero must contain exactly 8 elements × 24px with zero
padding so the zone is filled top-to-bottom with no spare space.

### Settings

- Sidebar col 1–2, full height, 48px items each
- Page header + section headings col 3–12, 48px
- Form rows: label col 3–5, input col 6–12, 48px (single-line fields), 72px (textarea)
- AI provider rows 72px: identity col 3–5 / status col 6–10 / action col 11–12
- Save row 72px: empty label zone col 3–5 / buttons col 6–12 with `padding-top: 24px`
- Section divider: 24px single-baseline horizontal band between sections

---

## Common mistakes

### Baseline grid clipped to zones
**Wrong:** `repeating-linear-gradient` on individual zone `background` properties.  
**Right:** one `.bl-ov` div with `position:absolute; inset:0; z-index:9` inside `.wf-grid`.

### Text shifted off column lines
**Wrong:** any `padding` on text zones.  
**Right:** `padding: 0` on all text zones. Borders do not shift text.

### Elements floating to visual centres
**Wrong:** `align-items: center` on zones containing pills or buttons.  
**Right:** `align-items: flex-start` + `padding-top: N×24px`.

### Row heights not multiples of 24
**Wrong:** 50px, 60px, 100px rows.  
**Right:** 24px, 48px, 72px, 96px. Audit every `grid-template-rows` value.

### Pills with variable widths
**Wrong:** intrinsic-width pills that size to their text label.  
**Right:** `width: 100%; box-sizing: border-box` so all pills in a column are the same width.

### `isolation: isolate` omitted
**Wrong:** z-index layers bleed out and render in the wrong order.  
**Right:** `isolation: isolate` on `.wf-grid` is required whenever overlay layers are used.

---

## Checklist before shipping a new guide

- [ ] All `grid-template-rows` values are multiples of 24px
- [ ] All cumulative Y offsets are multiples of 24px
- [ ] `isolation: isolate` is on `.wf-grid`
- [ ] `.bl-ov` is inside `.wf-grid`, spans full grid with `inset:0`
- [ ] No text zone has non-zero `padding`
- [ ] All `line-height` values on text are `24px` or `var(--bl)`
- [ ] All pills use `width: 100%; box-sizing: border-box`
- [ ] Action buttons/pills use `align-items: flex-start` + `padding-top: N×24px`
- [ ] Bracket annotations have `height` matching each row exactly
- [ ] Span annotation rows exist for all hierarchy levels
- [ ] Zone table is complete and accurate
- [ ] File opens standalone with no 404s (no external dependencies)
