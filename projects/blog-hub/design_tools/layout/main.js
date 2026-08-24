// main.js — boot: fetch proposal.json, wire bus listeners, build ruler, register add-zone button
import { state, initFromProposal }  from './state.js';
import { on, emit }                 from './bus.js';
import { renderCanvas }             from './render.js';
import { renderPanel }              from './panel.js';
import { initIo, updateJson }       from './io.js';
import { initDrag }                 from './drag.js';

const canvas = document.getElementById('canvas');
const ruler  = document.getElementById('ruler');

// ── Full render ───────────────────────────────────────────────
function render() {
  renderCanvas();
  renderPanel();
  updateJson();
}

// ── Bus listeners ─────────────────────────────────────────────
on('update',      () => render());
on('canvas-only', () => { renderCanvas(); updateJson(); });

// ── Ruler (12 column numbers) ─────────────────────────────────
function buildRuler() {
  ruler.innerHTML = Array.from({ length: 12 }, (_, i) =>
    `<div class="r-col">${i + 1}</div>`
  ).join('');
}

// ── Add zone ──────────────────────────────────────────────────
document.getElementById('addZoneBtn').addEventListener('click', () => {
  const maxBottom = state.zones.length
    ? Math.max(...state.zones.map(z => z.row + z.h))
    : 0;
  state.zones.push({
    id: 'zone_' + Date.now(), name: 'New Zone',
    col1: 1, col2: 13, row: maxBottom, h: 2, radius: 0, cutouts: [],
    bg: '#e8f4ff', fg: '#1a1917',
    why: '', size: '', place: '', note: ''
  });
  state.sel = state.zones.at(-1).id;
  emit('update');
});

// ── Add shape ─────────────────────────────────────────────────
document.getElementById('addShapeBtn').addEventListener('click', () => {
  state.shapes.push({
    id: 'shape_' + Date.now(), name: 'New Shape',
    col1: 4, col2: 10, row: 1, h: 2, radius: 0,
    mode: 'cut', attachSide: null, radius: 0, innerRadius: 0,
    bg: '#ffffff', fg: '#1a1917', note: ''
  });
  state.sel = state.shapes.at(-1).id;
  emit('update');
});

// ── Boot ──────────────────────────────────────────────────────
(async () => {
  const proposalUrl = new URL('./proposal.json', import.meta.url);
  const data = await fetch(proposalUrl).then(r => r.json());
  initFromProposal(data);
  buildRuler();
  initDrag(canvas);
  initIo();
  render();
})();
