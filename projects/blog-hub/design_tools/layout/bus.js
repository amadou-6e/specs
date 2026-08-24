// bus.js — tiny synchronous event bus; no imports
const target = new EventTarget();
export const emit = name => target.dispatchEvent(new Event(name));
export const on   = (name, fn) => target.addEventListener(name, fn);
