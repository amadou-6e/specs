// render.js — canvas zone rendering with optional clip-path cutouts
import { G, colX, colW, rowY, rowH, esc, state } from './state.js';
import { emit } from './bus.js';

const canvas = document.getElementById('canvas');

// ── CSS path() clip (even-odd subtract, pixel coords relative to element) ──

// Build one cutout's SVG sub-path with optional rounded corners.
// Corner radii:
//   radius      → convex zone corners (one edge flush with zone edge) — the
//                 arc rounds the DARK ZONE's own corner, so it must bulge
//                 past the cutout's own edge into the zone (removing more
//                 dark material there), not curl inward into the cutout.
//   innerRadius → concave zone corners (fully interior to zone) — arc rounds
//                 the cutout's own corner, curling inward as usual.
// Sweep: convex corners use sweep=0, concave corners use sweep=1 (concave
// corners round a plain 90° corner of the cutout box itself, matching the
// standard CW-rounded-rect convention; convex corners round the opposite
// case — the zone's own corner — so they take the mirrored sweep).
function cutPath(c, zx0, zy0, zw, zh) {
  const x0 = Math.max(0, colX(c.col1) - zx0);
  const y0 = Math.max(0, rowY(c.row)  - zy0);
  const x1 = Math.min(zw, colX(c.col1) + colW(c.col1, c.col2) - zx0);
  const y1 = Math.min(zh, rowY(c.row)  + rowH(c.h)            - zy0);
  if (x1 <= x0 || y1 <= y0) return '';

  const ro = c.radius      || 0;
  const ri = c.innerRadius || 0;

  if (ro === 0 && ri === 0) return `M ${x0} ${y0} H ${x1} V ${y1} H ${x0} Z`;

  const eps = 0.5;
  const flushL = x0 < eps, flushR = x1 > zw - eps;
  const flushT = y0 < eps, flushB = y1 > zh - eps;

  // both-flush → 0 (no arc), one-flush → ro (convex), none-flush → ri (concave)
  const cr = (xf, yf) => (xf && yf) ? 0 : (!xf && !yf) ? ri : ro;

  const maxR = Math.min((x1 - x0) / 2, (y1 - y0) / 2);
  const clamp = r => Math.min(r, maxR);

  // Signed offset of the arc center along one axis, from the corner.
  // `inward` points toward the cutout's own interior along this axis.
  // On the flush axis (or for concave corners) the offset stays inward,
  // same as a plain rounded rect. On the interior axis of a convex corner
  // it flips outward, past the cutout's own edge, so the arc removes a
  // bite of the surrounding dark zone instead of just rounding the hole.
  const off = (flushThis, flushOther, inward, r) =>
    (flushThis || !(flushThis || flushOther)) ? inward * r : -inward * r;

  function corner(cx, cy, fx, fy, inX, inY) {
    const r = clamp(cr(fx, fy));
    if (r === 0) return { th: { x: cx, y: cy }, tv: { x: cx, y: cy }, r: 0, sw: 0 };
    const offX = off(fx, fy, inX, r);
    const offY = off(fy, fx, inY, r);
    const convex = fx || fy;
    return { th: { x: cx + offX, y: cy }, tv: { x: cx, y: cy + offY }, r, sw: convex ? 0 : 1 };
  }

  const TL = corner(x0, y0, flushL, flushT, +1, +1);
  const TR = corner(x1, y0, flushR, flushT, -1, +1);
  const BR = corner(x1, y1, flushR, flushB, -1, -1);
  const BL = corner(x0, y1, flushL, flushB, +1, -1);

  const arc = (r, sw, tx, ty) => r > 0 ? `A ${r} ${r} 0 0 ${sw} ${tx} ${ty} ` : '';

  let d = `M ${TL.th.x} ${TL.th.y} `;
  d += `H ${TR.th.x} `;  d += arc(TR.r, TR.sw, TR.tv.x, TR.tv.y);
  d += `V ${BR.tv.y} `;  d += arc(BR.r, BR.sw, BR.th.x, BR.th.y);
  d += `H ${BL.th.x} `;  d += arc(BL.r, BL.sw, BL.tv.x, BL.tv.y);
  d += `V ${TL.tv.y} `;  d += arc(TL.r, TL.sw, TL.th.x, TL.th.y);
  d += 'Z';
  return d;
}

function computeClipPath(z) {
  const allCuts = [...(z.cutouts || []), ...state.shapes.filter(s => s.mode !== 'add')];
  if (allCuts.length === 0) return '';

  const zx0 = colX(z.col1), zy0 = rowY(z.row);
  const zw  = colW(z.col1, z.col2), zh = rowH(z.h);
  if (zw <= 0 || zh <= 0) return '';

  let d = `M 0 0 H ${zw} V ${zh} H 0 Z`;
  let hasCuts = false;
  allCuts.forEach(c => {
    const seg = cutPath(c, zx0, zy0, zw, zh);
    if (seg) { d += ' ' + seg; hasCuts = true; }
  });
  return hasCuts ? `path(evenodd, "${d}")` : '';
}

// Junction corners stay square on the shape itself; the arc lives in separate fillet divs.
// Free corners get outer radius. CSS shorthand: TL TR BR BL
function shapeRadius(s) {
  const r = s.radius || 0;
  const map = {
    top:    [0, 0,  r,  r],
    bottom: [r,  r,  0,  0],
    left:   [0,  r,  r,  0],
    right:  [r,  0,  0,  r],
  };
  const c = map[s.attachSide];
  return c ? `${c[0]}px ${c[1]}px ${c[2]}px ${c[3]}px` : `${r}px`;
}

// Fillet divs — placed in the zone adjacent to each junction corner.
// The key: round the corner OPPOSITE to the junction point so CSS centres
// the arc exactly on the junction → dark fills toward the junction → ╮╭ shape.
// CSS shorthand: TL TR BR BL
function renderShapeFillets(s) {
  const ir = s.innerRadius || 0;
  if (!s.attachSide || ir === 0) return;

  const sl = colX(s.col1), st = rowY(s.row);
  const sw = colW(s.col1, s.col2), sh = rowH(s.h);
  const zEdgeR = z => colX(z.col1) + colW(z.col1, z.col2);
  const zEdgeB = z => rowY(z.row)  + rowH(z.h);

  // Skip a fillet when the shape's edge is flush with an adjacent zone's edge —
  // that's a continuation line, not a corner, so no rounding needed.
  const flush = (check) => state.zones.some(check);

  // Fillet = ir×ir div placed adjacent to the junction corner.
  // The gradient anchor is the center of curvature (opposite corner from the junction).
  // radial-gradient makes the curvature-center region transparent and the
  // junction-corner region (arc + corner) dark → correct concave scoop at junction.
  const make = (left, top, anchor) => {
    const el = document.createElement('div');
    el.className = 'shape-fillet';
    el.style.cssText = [
      `left:${left}px`, `top:${top}px`,
      `width:${ir}px`,  `height:${ir}px`,
      `background:radial-gradient(circle at ${anchor}, transparent ${ir}px, ${s.bg} ${ir}px)`
    ].join(';');
    canvas.appendChild(el);
  };

  switch (s.attachSide) {
    case 'top': {
      const above = z => Math.abs(zEdgeB(z) - st) < 1;
      const skipL = flush(z => above(z) && Math.abs(colX(z.col1) - sl) < 1);
      const skipR = flush(z => above(z) && Math.abs(zEdgeR(z) - (sl + sw)) < 1);
      // TL junction at fillet's TR corner → curvature center at BL
      if (!skipL) make(sl - ir, st,      '0% 100%');
      // TR junction at fillet's TL corner → curvature center at BR
      if (!skipR) make(sl + sw, st,      '100% 100%');
      break;
    }
    case 'bottom': {
      const below = z => Math.abs(rowY(z.row) - (st + sh)) < 1;
      const skipL = flush(z => below(z) && Math.abs(colX(z.col1) - sl) < 1);
      const skipR = flush(z => below(z) && Math.abs(zEdgeR(z) - (sl + sw)) < 1);
      // BL junction at fillet's BR corner → curvature center at TL
      if (!skipL) make(sl - ir, st+sh-ir, '0% 0%');
      // BR junction at fillet's BL corner → curvature center at TR
      if (!skipR) make(sl + sw, st+sh-ir, '100% 0%');
      break;
    }
    case 'left': {
      const leftOf = z => Math.abs(zEdgeR(z) - sl) < 1;
      const skipT = flush(z => leftOf(z) && Math.abs(rowY(z.row) - st) < 1);
      const skipB = flush(z => leftOf(z) && Math.abs(zEdgeB(z) - (st + sh)) < 1);
      // top junction at fillet's TR corner → curvature center at BL
      if (!skipT) make(sl - ir, st,        '0% 100%');
      // bottom junction at fillet's BR corner → curvature center at TL
      if (!skipB) make(sl - ir, st+sh-ir,  '0% 0%');
      break;
    }
    case 'right': {
      const rightOf = z => Math.abs(colX(z.col1) - (sl + sw)) < 1;
      const skipT = flush(z => rightOf(z) && Math.abs(rowY(z.row) - st) < 1);
      const skipB = flush(z => rightOf(z) && Math.abs(zEdgeB(z) - (st + sh)) < 1);
      // top junction at fillet's TL corner → curvature center at BR
      if (!skipT) make(sl+sw, st,       '100% 100%');
      // bottom junction at fillet's BL corner → curvature center at TR
      if (!skipB) make(sl+sw, st+sh-ir, '100% 0%');
      break;
    }
  }
}

// ── Shape element ─────────────────────────────────────────────
function shapeEl(s) {
  const div = document.createElement('div');
  div.className = 'shape' + (s.id === state.sel ? ' sel' : '');
  div.dataset.id   = s.id;
  div.dataset.mode = s.mode || 'cut';
  div.style.cssText = [
    `left:${colX(s.col1)}px`,
    `top:${rowY(s.row)}px`,
    `width:${colW(s.col1, s.col2)}px`,
    `height:${rowH(s.h)}px`,
    `background:${s.bg}`,
    `color:${s.fg}`,
    `border-radius:${shapeRadius(s)}`
  ].join(';');
  div.innerHTML = `
    <div class="z-inner"><span class="z-name">${esc(s.name)}</span></div>
    <div class="z-rw" data-resize="w"></div>
    <div class="z-re" data-resize="e"></div>
    <div class="z-rh" data-resize="s"></div>
  `;
  return div;
}

// ── Conditional zone edge rounding ────────────────────────────
// A zone's border-radius should only round edges where no cutout or
// added shape touches. Each corner is blocked independently based on
// whether any geometry actually overlaps that specific corner.
function zoneRadius(z) {
  const r = z.radius || 0;
  if (r === 0) return '0px';

  const zx0 = colX(z.col1), zx1 = colX(z.col1) + colW(z.col1, z.col2);
  const zy0 = rowY(z.row), zy1 = rowY(z.row) + rowH(z.h);

  // Check if any cutout or added shape blocks a specific corner.
  const isCornerBlocked = (cornerX, cornerY) => {
    const eps = 0.5;
    // Cutouts: a corner is only eaten by a cutout if the cutout has an
    // actual vertex there — i.e. it's flush with BOTH edges meeting at
    // that corner, not just one (sharing a row/col isn't enough).
    if (z.cutouts) {
      for (const c of z.cutouts) {
        const cx0 = colX(c.col1), cx1 = cx0 + colW(c.col1, c.col2);
        const cy0 = rowY(c.row), cy1 = cy0 + rowH(c.h);
        const hitX = Math.abs(cx0 - cornerX) < eps || Math.abs(cx1 - cornerX) < eps;
        const hitY = Math.abs(cy0 - cornerY) < eps || Math.abs(cy1 - cornerY) < eps;
        if (hitX && hitY) return true;
      }
    }
    // Added shapes: the shape's attach edge touches the OPPOSITE zone
    // edge (its top touches the zone's bottom, etc). Blocks a corner
    // only if that opposite edge matches AND the shape's span reaches
    // that corner's other-axis coordinate.
    for (const s of state.shapes) {
      if (s.mode !== 'add') continue;
      const sx0 = colX(s.col1), sx1 = sx0 + colW(s.col1, s.col2);
      const sy0 = rowY(s.row), sy1 = sy0 + rowH(s.h);
      if (s.attachSide === 'top' && Math.abs(sy0 - zy1) < eps &&
          cornerY === zy1 && cornerX >= sx0 - eps && cornerX <= sx1 + eps) return true;
      if (s.attachSide === 'bottom' && Math.abs(sy1 - zy0) < eps &&
          cornerY === zy0 && cornerX >= sx0 - eps && cornerX <= sx1 + eps) return true;
      if (s.attachSide === 'left' && Math.abs(sx0 - zx1) < eps &&
          cornerX === zx1 && cornerY >= sy0 - eps && cornerY <= sy1 + eps) return true;
      if (s.attachSide === 'right' && Math.abs(sx1 - zx0) < eps &&
          cornerX === zx0 && cornerY >= sy0 - eps && cornerY <= sy1 + eps) return true;
    }
    return false;
  };

  const rTL = isCornerBlocked(zx0, zy0) ? 0 : r;
  const rTR = isCornerBlocked(zx1, zy0) ? 0 : r;
  const rBR = isCornerBlocked(zx1, zy1) ? 0 : r;
  const rBL = isCornerBlocked(zx0, zy1) ? 0 : r;

  return `${rTL}px ${rTR}px ${rBR}px ${rBL}px`;
}

// ── Build one zone <div> ──────────────────────────────────────
function zoneEl(z) {
  const div = document.createElement('div');
  div.className = 'zone' + (z.id === state.sel ? ' sel' : '');
  div.dataset.id = z.id;

  const clipStr = computeClipPath(z);
  div.style.cssText = [
    `left:${colX(z.col1)}px`,
    `top:${rowY(z.row)}px`,
    `width:${colW(z.col1, z.col2)}px`,
    `height:${rowH(z.h)}px`,
    `background:${z.bg}`,
    `color:${z.fg}`,
    `border-radius:${zoneRadius(z)}`,
    clipStr ? `clip-path:${clipStr}` : ''
  ].filter(Boolean).join(';');

  const label = z.h === 1
    ? `<span class="z-name">${esc(z.name)}</span>`
    : `<span class="z-name">${esc(z.name)}</span>
       <span class="z-spec">col ${z.col1}–${z.col2 - 1} · ${z.h}×24=${z.h * 24}px</span>`;

  div.innerHTML = `
    <div class="z-inner">${label}</div>
    <div class="z-rw" data-resize="w"></div>
    <div class="z-re" data-resize="e"></div>
    <div class="z-rh" data-resize="s"></div>
  `;
  return div;
}

// ── Cutout overlay divs (shown when zone is selected) ─────────
function renderCutoutOverlays() {
  canvas.querySelectorAll('.cutout-overlay').forEach(el => el.remove());
  if (!state.sel) return;

  const z = state.zones.find(z => z.id === state.sel);
  if (!z || !z.cutouts || z.cutouts.length === 0) return;

  z.cutouts.forEach((c, i) => {
    const isSel = state.cutoutSel && state.cutoutSel.zoneId === z.id && state.cutoutSel.idx === i;
    const ov = document.createElement('div');
    ov.className = 'cutout-overlay' + (isSel ? ' sel' : '');
    ov.dataset.zoneId    = z.id;
    ov.dataset.cutoutIdx = i;
    ov.style.cssText = [
      `left:${colX(c.col1)}px`,
      `top:${rowY(c.row)}px`,
      `width:${colW(c.col1, c.col2)}px`,
      `height:${rowH(c.h)}px`
    ].join(';');
    ov.innerHTML = `<span class="co-label">cut ${i + 1}</span>`;
    ov.addEventListener('mousedown', e => {
      state.cutoutSel = { zoneId: z.id, idx: i };
      e.stopPropagation();
      emit('update');
    });
    canvas.appendChild(ov);
  });
}

// ── Public ────────────────────────────────────────────────────
export function renderCanvas() {
  canvas.querySelectorAll('.zone,.shape,.shape-fillet,.cutout-overlay').forEach(el => el.remove());
  state.zones.forEach(z => canvas.appendChild(zoneEl(z)));
  state.shapes.forEach(s => {
    canvas.appendChild(shapeEl(s));
    if ((s.mode || 'cut') === 'add') renderShapeFillets(s);
  });
  renderCutoutOverlays();
  updateCanvasHeight();
}

export function updateCanvasHeight() {
  const maxBottom = state.zones.reduce((m, z) => Math.max(m, (z.row + z.h) * G.bl), 0);
  canvas.style.minHeight = (maxBottom + 48) + 'px';
}
