// state.js — Grid constants, coordinate helpers, proposal data, mutable state

export const G = { col: 48, gap: 16, unit: 64, mg: 32, bl: 24 };

export const colX  = c       => G.mg + (c - 1) * G.unit;
export const colW  = (c1,c2) => (c2 - c1) * G.unit - G.gap;
export const rowY  = r       => r * G.bl;
export const rowH  = h       => h * G.bl;
export const esc   = s       => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');

// Mutable app state — imported and mutated by all modules
export const state = { zones: [], shapes: [], sel: null, cutoutSel: null, drag: null };

// Populated at boot from proposal.json; kept here so io.js can reference it
export let PROPOSAL = [];

export function initFromProposal(data) {
  const zones  = Array.isArray(data) ? data : (data.zones  || []);
  const shapes = Array.isArray(data) ? []   : (data.shapes || []);
  PROPOSAL      = zones;
  state.zones   = zones.map(z  => ({ ...z,  cutouts: z.cutouts || [] }));
  state.shapes  = shapes.map(s => ({ ...s }));
}

// Find an item by id in zones or shapes — returns { item, type } or null
export function findItem(id) {
  const z = state.zones.find(z => z.id === id);
  if (z) return { item: z, type: 'zone' };
  const s = state.shapes.find(s => s.id === id);
  if (s) return { item: s, type: 'shape' };
  return null;
}
