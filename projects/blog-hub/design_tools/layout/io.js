// io.js — JSON export / import
import { PROPOSAL, state } from './state.js';
import { emit } from './bus.js';

const jsonArea = document.getElementById('jsonArea');
const ftMsg    = document.getElementById('ftMsg');

let jsonFocused = false;

export function initIo() {
  jsonArea.addEventListener('focus', () => { jsonFocused = true; });
  jsonArea.addEventListener('blur',  () => { jsonFocused = false; });

  document.getElementById('copyJsonBtn').addEventListener('click', () => {
    navigator.clipboard.writeText(jsonArea.value)
      .then(() => flash('Copied to clipboard ✓'))
      .catch(() => { jsonArea.select(); flash('Select all + copy manually'); });
  });

  document.getElementById('loadJsonBtn').addEventListener('click', () => {
    loadJson(jsonArea.value);
  });
}

export function updateJson() {
  if (jsonFocused) return;
  jsonArea.value = JSON.stringify({
    page: 'overview',
    tool: 'layout',
    zones: state.zones.map(z => ({
      id: z.id, name: z.name,
      col1: z.col1, col2: z.col2,
      row: z.row, h: z.h,
      radius: z.radius || 0,
      bg: z.bg, fg: z.fg,
      note: z.note,
      cutouts: (z.cutouts || []).map(c => ({
        col1: c.col1, col2: c.col2, row: c.row, h: c.h,
        ...(c.radius      ? { radius:      c.radius      } : {}),
        ...(c.innerRadius ? { innerRadius: c.innerRadius } : {})
      }))
    })),
    shapes: state.shapes.map(s => ({
      id: s.id, name: s.name,
      col1: s.col1, col2: s.col2,
      row: s.row, h: s.h,
      radius: s.radius || 0,
      mode: s.mode || 'cut',
      attachSide:  s.attachSide  || null,
      innerRadius: s.innerRadius || 0,
      bg: s.bg, fg: s.fg,
      note: s.note || ''
    }))
  }, null, 2);
}

export function loadJson(text) {
  try {
    const data = JSON.parse(text);
    if (!data.zones) throw new Error('No zones array');
    const propMap = Object.fromEntries(PROPOSAL.map(z => [z.id, z]));
    state.zones = data.zones.map(z => ({
      why: '', size: '', place: '',
      ...(propMap[z.id] || {}),
      ...z,
      radius:  z.radius  || 0,
      cutouts: z.cutouts || []
    }));
    state.shapes = (data.shapes || []).map(s => ({ ...s }));
    state.sel = null;
    emit('update');
    flash('JSON loaded ✓');
  } catch (e) {
    flash('Error: ' + e.message);
  }
}

function flash(msg) {
  ftMsg.textContent = msg;
  clearTimeout(flash._t);
  flash._t = setTimeout(() => { ftMsg.textContent = ''; }, 2500);
}
