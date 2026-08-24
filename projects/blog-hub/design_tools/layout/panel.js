// panel.js — right panel: zone list + shape list + detail
import { state, findItem, esc } from './state.js';
import { updateJson } from './io.js';
import { emit } from './bus.js';

const zoneList   = document.getElementById('zoneList');
const zoneDetail = document.getElementById('zoneDetail');

export function renderPanel() {
  renderZoneList();
  renderShapeList();
  renderDetail();
}

// ── Zone list ─────────────────────────────────────────────────
function renderZoneList() {
  zoneList.innerHTML = state.zones.map(z => `
    <div class="zl-item${z.id === state.sel ? ' sel' : ''}" data-id="${z.id}">
      <div class="zl-sw" style="background:${z.bg};"></div>
      <span class="zl-name">${esc(z.name)}</span>
      <span class="zl-spec">${z.h}×24${z.cutouts && z.cutouts.length ? ' ✂' : ''}</span>
    </div>
  `).join('');

  zoneList.querySelectorAll('.zl-item').forEach(el => {
    el.addEventListener('click', () => { state.sel = el.dataset.id; emit('update'); });
  });
}

// ── Shape list ────────────────────────────────────────────────
function renderShapeList() {
  const container = document.getElementById('shapeList');
  if (!container) return;

  container.innerHTML = state.shapes.length === 0
    ? '<p class="nd" style="font-size:9px;margin:4px 0;">No shapes yet.</p>'
    : state.shapes.map(s => `
        <div class="zl-item${s.id === state.sel ? ' sel' : ''}" data-id="${s.id}">
          <div class="zl-sw" style="background:${s.bg};outline:1px dashed rgba(59,130,246,.5);"></div>
          <span class="zl-name">${esc(s.name)}</span>
          <span class="zl-spec">${s.h}×24</span>
        </div>
      `).join('');

  container.querySelectorAll('.zl-item').forEach(el => {
    el.addEventListener('click', () => { state.sel = el.dataset.id; emit('update'); });
  });
}

// ── Detail dispatcher ─────────────────────────────────────────
function renderDetail() {
  if (!state.sel) {
    zoneDetail.innerHTML = '<p class="nd">Click a zone or shape to edit it.</p>';
    return;
  }
  const found = findItem(state.sel);
  if (!found) { zoneDetail.innerHTML = '<p class="nd">Click a zone or shape to edit it.</p>'; return; }
  found.type === 'shape' ? renderShapeDetail(found.item) : renderZoneDetail(found.item);
}

// ── Zone detail ───────────────────────────────────────────────
function renderZoneDetail(z) {
  if (!z.cutouts) z.cutouts = [];

  zoneDetail.innerHTML = `
    <div class="sec-label">Selected: ${esc(z.name)}</div>

    <div class="d-row">
      <label>Name</label>
      <input class="d-input" id="d-name" value="${esc(z.name)}">
    </div>
    <div class="d-cols">
      <div class="d-row">
        <label>Col start</label>
        <input class="d-input sm" id="d-c1" type="number" min="1" max="12" value="${z.col1}">
      </div>
      <div class="d-row">
        <label>Col end</label>
        <input class="d-input sm" id="d-c2" type="number" min="2" max="13" value="${z.col2}">
      </div>
      <div class="d-row">
        <label>H (×24)</label>
        <input class="d-input sm" id="d-h" type="number" min="1" max="30" value="${z.h}">
      </div>
    </div>
    <div class="d-row">
      <label>Border radius (px)</label>
      <input class="d-input sm" id="d-radius" type="number" min="0" max="120" value="${z.radius || 0}">
    </div>

    <div class="d-my">
      <div class="d-my-hd">My proposal</div>
      ${z.why   ? `<div class="d-my-item"><div class="d-my-k">Why</div><div class="d-my-v">${esc(z.why)}</div></div>` : ''}
      ${z.size  ? `<div class="d-my-item"><div class="d-my-k">Sizing</div><div class="d-my-v">${esc(z.size)}</div></div>` : ''}
      ${z.place ? `<div class="d-my-item"><div class="d-my-k">Placement</div><div class="d-my-v">${esc(z.place)}</div></div>` : ''}
    </div>

    <div class="d-user">
      <div class="d-user-hd">Your notes</div>
      <textarea class="d-user-ta" id="d-note"
        placeholder="Disagreements, questions, suggestions…">${esc(z.note)}</textarea>
    </div>

    <div class="d-divider"></div>

    <div class="sec-label">Cutouts — shapes subtracted from this zone</div>
    <div id="cutoutList">
      ${z.cutouts.length === 0
        ? '<p class="nd" style="font-size:9px;margin:4px 0 8px;">No cutouts yet.</p>'
        : z.cutouts.map(cutoutItemHtml).join('')
      }
    </div>
    <button class="btn-add" id="addCutoutBtn">+ Add cutout</button>

    <div class="d-divider"></div>
    <button class="btn-del" id="delZoneBtn">Delete this zone</button>
  `;

  const numField = (id, field, min, max) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('change', e => {
      z[field] = Math.max(min, Math.min(max, parseInt(e.target.value) || min));
      emit('update');
    });
  };
  document.getElementById('d-name').addEventListener('change', e => { z.name = e.target.value; emit('update'); });
  numField('d-c1',    'col1',   1,   z.col2 - 1);
  numField('d-c2',    'col2',   z.col1 + 1, 13);
  numField('d-h',     'h',      1,   30);
  numField('d-radius','radius', 0,   120);
  document.getElementById('d-note').addEventListener('input', e => { z.note = e.target.value; updateJson(); });

  zoneDetail.querySelectorAll('[data-ci]').forEach(el => {
    el.addEventListener('change', e => {
      const ci = parseInt(e.target.dataset.ci);
      const cf = e.target.dataset.cf;
      if (!z.cutouts[ci]) return;
      z.cutouts[ci][cf] = parseInt(e.target.value) || 0;
      emit('update');
    });
  });

  zoneDetail.querySelectorAll('.cutout-del').forEach(el => {
    el.addEventListener('click', e => {
      const idx = parseInt(e.target.closest('[data-cidx]').dataset.cidx);
      z.cutouts.splice(idx, 1);
      emit('update');
    });
  });

  document.getElementById('addCutoutBtn').addEventListener('click', () => {
    z.cutouts.push({ col1: z.col1, col2: z.col2, row: z.row, h: 1 });
    state.cutoutSel = { zoneId: z.id, idx: z.cutouts.length - 1 };
    emit('update');
  });

  // Scroll selected cutout item into view and highlight it
  if (state.cutoutSel && state.cutoutSel.zoneId === z.id) {
    const selItem = zoneDetail.querySelector(`[data-cidx="${state.cutoutSel.idx}"]`);
    if (selItem) {
      selItem.classList.add('cutout-item-sel');
      selItem.scrollIntoView({ block: 'nearest' });
    }
  }

  document.getElementById('delZoneBtn').addEventListener('click', () => {
    state.zones = state.zones.filter(b => b.id !== z.id);
    state.sel   = null;
    emit('update');
  });
}

// ── Shape detail ──────────────────────────────────────────────
function renderShapeDetail(s) {
  zoneDetail.innerHTML = `
    <div class="sec-label">Shape: ${esc(s.name)}</div>

    <div class="d-row">
      <label>Name</label>
      <input class="d-input" id="d-name" value="${esc(s.name)}">
    </div>
    <div class="d-cols">
      <div class="d-row">
        <label>Col start</label>
        <input class="d-input sm" id="d-c1" type="number" min="1" max="12" value="${s.col1}">
      </div>
      <div class="d-row">
        <label>Col end</label>
        <input class="d-input sm" id="d-c2" type="number" min="2" max="13" value="${s.col2}">
      </div>
      <div class="d-row">
        <label>H (×24)</label>
        <input class="d-input sm" id="d-h" type="number" min="1" max="30" value="${s.h}">
      </div>
    </div>
    <div class="d-cols">
      <div class="d-row">
        <label>Row</label>
        <input class="d-input sm" id="d-row" type="number" min="0" value="${s.row}">
      </div>
      <div class="d-row">
        <label>Outer radius</label>
        <input class="d-input sm" id="d-radius" type="number" min="0" max="120" value="${s.radius || 0}">
      </div>
    </div>
    <div class="d-row">
      <label>Attach side — which edge touches the main zone</label>
      <select class="d-input sm" id="d-attach">
        <option value="">None</option>
        <option value="top"   ${(s.attachSide||'')==='top'    ? 'selected':''}>Top</option>
        <option value="bottom"${(s.attachSide||'')==='bottom' ? 'selected':''}>Bottom</option>
        <option value="left"  ${(s.attachSide||'')==='left'   ? 'selected':''}>Left</option>
        <option value="right" ${(s.attachSide||'')==='right'  ? 'selected':''}>Right</option>
      </select>
    </div>
    <div class="d-row">
      <label>Junction radius — corners touching the main zone</label>
      <input class="d-input sm" id="d-inner-radius" type="number" min="0" max="120" value="${s.innerRadius || 0}">
    </div>
    <div class="d-cols">
      <div class="d-row">
        <label>Background</label>
        <input class="d-input sm" id="d-bg" type="color" value="${s.bg}" style="padding:2px 4px;height:28px;">
      </div>
      <div class="d-row">
        <label>Foreground</label>
        <input class="d-input sm" id="d-fg" type="color" value="${s.fg}" style="padding:2px 4px;height:28px;">
      </div>
    </div>

    <div class="d-row" style="margin-top:6px;">
      <label>Mode</label>
      <div class="shape-mode-toggle">
        <button class="smt-btn${(s.mode||'cut')==='cut' ? ' active' : ''}" data-mode="cut">✂ Cut</button>
        <button class="smt-btn${(s.mode||'cut')==='add' ? ' active' : ''}" data-mode="add">＋ Merge</button>
      </div>
    </div>

    <div class="d-user" style="margin-top:8px;">
      <div class="d-user-hd">Notes</div>
      <textarea class="d-user-ta" id="d-note"
        placeholder="Purpose of this shape…">${esc(s.note || '')}</textarea>
    </div>

    <div class="d-divider"></div>
    <button class="btn-del" id="delShapeBtn">Delete this shape</button>
  `;

  const numField = (id, field, min, max) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('change', e => {
      s[field] = Math.max(min, Math.min(max, parseInt(e.target.value) || min));
      emit('update');
    });
  };
  document.getElementById('d-name').addEventListener('change', e => { s.name = e.target.value; emit('update'); });
  numField('d-c1',    'col1',   1, s.col2 - 1);
  numField('d-c2',    'col2',   s.col1 + 1, 13);
  numField('d-h',     'h',      1, 30);
  numField('d-row',          'row',         0, 999);
  numField('d-radius',       'radius',      0, 120);
  numField('d-inner-radius', 'innerRadius', 0, 120);
  document.getElementById('d-attach').addEventListener('change', e => {
    s.attachSide = e.target.value || null; emit('update');
  });
  document.getElementById('d-bg').addEventListener('input', e => { s.bg = e.target.value; emit('canvas-only'); });
  document.getElementById('d-fg').addEventListener('input', e => { s.fg = e.target.value; emit('canvas-only'); });
  document.getElementById('d-note').addEventListener('input', e => { s.note = e.target.value; updateJson(); });
  zoneDetail.querySelectorAll('.smt-btn').forEach(btn => {
    btn.addEventListener('click', () => { s.mode = btn.dataset.mode; emit('update'); });
  });

  document.getElementById('delShapeBtn').addEventListener('click', () => {
    state.shapes = state.shapes.filter(b => b.id !== s.id);
    state.sel    = null;
    emit('update');
  });
}

// ── Cutout item HTML ──────────────────────────────────────────
function cutoutItemHtml(c, i) {
  return `
    <div class="cutout-item" data-cidx="${i}">
      <div class="cutout-item-hd">
        <span class="cutout-num">Cutout ${i + 1}</span>
        <button class="cutout-del">×</button>
      </div>
      <div class="d-cols">
        <div class="d-row">
          <label>Col start</label>
          <input class="d-input sm" data-ci="${i}" data-cf="col1"
            type="number" min="1" max="12" value="${c.col1}">
        </div>
        <div class="d-row">
          <label>Col end</label>
          <input class="d-input sm" data-ci="${i}" data-cf="col2"
            type="number" min="2" max="13" value="${c.col2}">
        </div>
        <div class="d-row">
          <label>H (×24)</label>
          <input class="d-input sm" data-ci="${i}" data-cf="h"
            type="number" min="1" max="30" value="${c.h}">
        </div>
      </div>
      <div class="d-row">
        <label>Row (global grid)</label>
        <input class="d-input sm" data-ci="${i}" data-cf="row"
          type="number" min="0" value="${c.row}">
      </div>
      <div class="d-cols">
        <div class="d-row">
          <label>Outer r (convex)</label>
          <input class="d-input sm" data-ci="${i}" data-cf="radius"
            type="number" min="0" max="120" value="${c.radius || 0}">
        </div>
        <div class="d-row">
          <label>Inner r (concave)</label>
          <input class="d-input sm" data-ci="${i}" data-cf="innerRadius"
            type="number" min="0" max="120" value="${c.innerRadius || 0}">
        </div>
      </div>
    </div>
  `;
}
