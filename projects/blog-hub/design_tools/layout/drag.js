// drag.js — drag (move) and resize (south / west / east) for zones and shapes
import { G, state, findItem } from './state.js';
import { emit }               from './bus.js';

function overlapsH(a, b) {
  return a.col1 < b.col2 && a.col2 > b.col1;
}

export function initDrag(canvas) {
  canvas.addEventListener('mousedown', onDown);
  window.addEventListener('mousemove', onMove);
  window.addEventListener('mouseup',   onUp);
}

function onDown(e) {
  const zEl = e.target.closest('[data-id]');
  if (!zEl) { state.cutoutSel = null; emit('canvas-only'); return; }

  const id    = zEl.dataset.id;
  const found = findItem(id);
  if (!found) return;
  state.cutoutSel = null;
  const { item: z, type } = found;
  const dir = e.target.dataset.resize; // 'w' | 'e' | 's' | undefined

  state.sel  = id;
  state.drag = {
    type:         dir ? `resize-${dir}` : 'move',
    id,
    itemType:     type,
    startClientX: e.clientX,
    startClientY: e.clientY,
    startCol1:    z.col1,
    startCol2:    z.col2,
    startRow:     z.row,
    startH:       z.h,
    startPositions: Object.fromEntries(
      [...state.zones, ...state.shapes].map(b => [b.id, { col1: b.col1, col2: b.col2, row: b.row, h: b.h }])
    )
  };

  e.preventDefault();
  emit('update');
}

function onMove(e) {
  if (!state.drag) return;
  const d     = state.drag;
  const found = findItem(d.id);
  if (!found) return;
  const { item: z } = found;

  const dcol = Math.round((e.clientX - d.startClientX) / G.unit);
  const dbl  = Math.round((e.clientY - d.startClientY) / G.bl);

  // Restore every item from snapshot so moves don't accumulate
  [...state.zones, ...state.shapes].forEach(b => {
    const sp = d.startPositions[b.id];
    if (sp) { b.col1 = sp.col1; b.col2 = sp.col2; b.row = sp.row; b.h = sp.h; }
  });

  const span = d.startCol2 - d.startCol1;

  switch (d.type) {
    case 'move': {
      z.col1 = Math.max(1, Math.min(13 - span, d.startCol1 + dcol));
      z.col2 = z.col1 + span;
      z.row  = Math.max(0, d.startRow + dbl);
      break;
    }
    case 'resize-s': {
      z.h = Math.max(1, d.startH + dbl);
      // Push-down only for zones, not floating shapes
      if (d.itemType === 'zone') {
        const oldBottom = d.startRow + d.startH;
        const push      = (z.row + z.h) - oldBottom;
        state.zones.forEach(b => {
          if (b.id === d.id) return;
          const sp = d.startPositions[b.id];
          if (sp && sp.row >= oldBottom && overlapsH(b, z)) b.row = sp.row + push;
        });
      }
      break;
    }
    case 'resize-e': {
      z.col2 = Math.max(z.col1 + 1, Math.min(13, d.startCol2 + dcol));
      break;
    }
    case 'resize-w': {
      z.col1 = Math.max(1, Math.min(z.col2 - 1, d.startCol1 + dcol));
      break;
    }
  }

  emit('canvas-only');
}

function onUp() {
  if (!state.drag) return;
  state.drag = null;
  emit('update');
}
