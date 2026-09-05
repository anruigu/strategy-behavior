'use strict';
/*
  KIT -- the drawing primitives every board is built from.

  WHY A KIT AND NOT TWENTY-THREE BESPOKE RENDERERS. There is one rule these
  boards have to keep and it is easy to break by accident: every legal move is
  presented with equal weight, and nothing is pre-selected. A row of buttons
  written by hand for the twentieth time is where one of them quietly becomes
  the primary. `KIT.actions` cannot make that mistake -- it emits one class for
  every option, in the order it was handed them, which is the order the prompt
  printed them.

  The same argument covers dials. `KIT.dial` takes the range out of the view,
  which took it out of the prompt's own words ("an integer from 0 to 120"), so
  a dial is never narrowed to the range an honest move lives in.

  MEMO. Most engines print their rules once, on the seat's first prompt: the
  payoff table, the property list, the letter values. The adapter returns null
  for those fields on later turns and the board reads its cached copy from
  here. The cache is cleared when a new game starts, so nothing crosses
  between cells.
*/

window.KIT = (function () {

// ---------------------------------------------------------------- basics --
function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined && text !== null) e.textContent = String(text);
  return e;
}

function svg(tag, attrs) {
  const e = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const k in (attrs || {})) e.setAttribute(k, attrs[k]);
  return e;
}

function frag(...kids) {
  const f = document.createDocumentFragment();
  kids.forEach(k => k && f.appendChild(k));
  return f;
}

function put(parent, ...kids) {
  kids.forEach(k => { if (k) parent.appendChild(k); });
  return parent;
}

function fmt(n) {
  if (n === null || n === undefined) return '--';
  if (typeof n !== 'number') return String(n);
  return Number.isInteger(n) ? String(n) : n.toFixed(1);
}

function signed(n) {
  if (n === null || n === undefined) return '--';
  return (n > 0 ? '+' : '') + fmt(n);
}

// ------------------------------------------------------------------ memo --
let MEMO = new Map();
function resetMemo() { MEMO = new Map(); }
function memo(key, value) {
  if (value !== null && value !== undefined) MEMO.set(key, value);
  return MEMO.has(key) ? MEMO.get(key) : null;
}

// ------------------------------------------------------------- structure --
function board(...kids) { return put(el('div', 'bd'), ...kids); }

function head(opts) {
  // The strip along the top of every board: where you are, and the score.
  const h = el('div', 'bd-head');
  const left = el('div', 'bd-where');
  if (opts.step) put(left, el('span', 'bd-pill', opts.step));
  if (opts.title) put(left, el('span', 'bd-title', opts.title));
  if (opts.sub) put(left, el('span', 'bd-sub', opts.sub));
  put(h, left);
  if (opts.scores && opts.scores.length) put(h, scoreboard(opts.scores, opts.me));
  return h;
}

function panels(...kids) { return put(el('div', 'bd-panels'), ...kids); }

function panel(title, ...kids) {
  const p = el('div', 'bd-panel');
  if (title) put(p, el('div', 'bd-panel-h', title));
  return put(p, ...kids);
}

function wide(title, ...kids) {
  const p = panel(title, ...kids);
  p.classList.add('wide');
  return p;
}

function note(text, cls) { return el('div', 'bd-note' + (cls ? ' ' + cls : ''), text); }

function act(...kids) { return put(el('div', 'bd-act'), ...kids); }

// ------------------------------------------------------------ scoreboard --
function scoreboard(entries, me) {
  const t = el('div', 'bd-scores');
  entries.forEach((e, i) => {
    const d = el('div', 'bd-score' + (isMe(e.name, me, i) ? ' mine' : ''));
    put(d, el('span', 'nm', e.name), el('b', null, fmt(e.score)));
    put(t, d);
  });
  return t;
}

function isMe(name, me, i) {
  if (me === undefined || me === null) return String(name).toLowerCase() === 'you';
  if (typeof me === 'number') return i === me;
  return String(name).toLowerCase() === String(me).toLowerCase();
}

// ----------------------------------------------------------------- marks --
// A seat's colour is ALWAYS accompanied by its name in text. Colour is the
// second encoding here, never the only one -- four hues that a colour-blind
// reader cannot separate must not be the only thing saying whose deed this is.
const SEATC = ['s0', 's1', 's2', 's3'];
function seatClass(i) { return SEATC[((i % 4) + 4) % 4]; }

function meter(o) {
  // A bar with its value, an optional cap, and optional marks along it.
  const box = el('div', 'bd-meter');
  if (o.label) put(box, el('div', 'lab', o.label));
  const track = el('div', 'track');
  const max = o.max || 1;
  const fill = el('div', 'fill' + (o.tone ? ' ' + o.tone : ''));
  fill.style.width = Math.max(0, Math.min(100, (o.value / max) * 100)) + '%';
  put(track, fill);
  (o.marks || []).forEach(m => {
    const k = el('div', 'mark');
    k.style.left = Math.max(0, Math.min(100, (m.at / max) * 100)) + '%';
    if (m.label) k.dataset.lab = m.label;
    put(track, k);
  });
  put(box, track);
  put(box, el('div', 'val', o.text !== undefined ? o.text
    : fmt(o.value) + (o.max ? ' / ' + fmt(o.max) : '')));
  return box;
}

function bars(rows, opts) {
  // One labelled bar per row -- fuel per crew, holdings per settler.
  const max = (opts && opts.max) || Math.max(1, ...rows.map(r => r.value));
  const box = el('div', 'bd-bars');
  rows.forEach((r, i) => {
    const line = el('div', 'bd-bar');
    put(line, el('span', 'nm', r.label));
    const t = el('span', 'track');
    const f = el('span', 'fill ' + (r.seat !== undefined ? seatClass(r.seat) : 'neutral'));
    f.style.width = Math.max(2, (r.value / max) * 100) + '%';
    put(t, f);
    put(line, t, el('b', null, fmt(r.value)));
    put(box, line);
  });
  return box;
}

// ----------------------------------------------------------------- cards --
const RANKS = { 11: 'J', 12: 'Q', 13: 'K', 14: 'A' };

function card(o) {
  // A rectangle that reads as a card: a big rank, a corner repeat, a tone.
  const c = el('div', 'bd-card' + (o.tone ? ' ' + o.tone : '') +
    (o.face === false ? ' back' : '') + (o.small ? ' small' : ''));
  if (o.face === false) { put(c, el('span', 'weave')); return c; }
  put(c, el('span', 'corner', o.corner !== undefined ? o.corner : o.label));
  put(c, el('span', 'pip', o.label));
  if (o.sub) put(c, el('span', 'sub', o.sub));
  if (o.onClick) { c.classList.add('pick'); c.onclick = o.onClick; }
  return c;
}

function rankCard(n, opts) {
  return card(Object.assign({ label: RANKS[n] || String(n) }, opts || {}));
}

function cardRow(...kids) { return put(el('div', 'bd-cards'), ...kids); }

// ------------------------------------------------------------------ dice --
const PIPS = {
  1: [[1, 1]], 2: [[0, 0], [2, 2]], 3: [[0, 0], [1, 1], [2, 2]],
  4: [[0, 0], [2, 0], [0, 2], [2, 2]],
  5: [[0, 0], [2, 0], [1, 1], [0, 2], [2, 2]],
  6: [[0, 0], [2, 0], [0, 1], [2, 1], [0, 2], [2, 2]],
};

function die(n, opts) {
  const o = opts || {};
  const s = svg('svg', { viewBox: '0 0 30 30', class: 'bd-die' + (o.lit ? ' lit' : '') });
  put(s, svg('rect', { x: 1, y: 1, width: 28, height: 28, rx: 6, class: 'body' }));
  (PIPS[n] || []).forEach(([x, y]) =>
    put(s, svg('circle', { cx: 7 + x * 8, cy: 7 + y * 8, r: 2.6, class: 'pip' })));
  const w = el('span', 'bd-diewrap' + (o.lit ? ' lit' : ''));
  put(w, s);
  return w;
}

function diceRow(values, opts) {
  const o = opts || {};
  const row = el('div', 'bd-dice');
  values.forEach(v => put(row, die(v, { lit: o.face !== undefined && v === o.face })));
  return row;
}

// ----------------------------------------------------------------- tiles --
function letterTile(ch, value, opts) {
  const o = opts || {};
  const t = el('div', 'bd-tile' + (o.dim ? ' dim' : '') + (o.lit ? ' lit' : ''));
  put(t, el('span', 'ch', ch));
  if (value !== null && value !== undefined) put(t, el('span', 'v', value));
  return t;
}

function crate(value, max, opts) {
  const o = opts || {};
  const c = el('div', 'bd-crate' + (o.tone ? ' ' + o.tone : ''));
  const h = 26 + Math.round(40 * (value / (max || 40)));
  c.style.height = h + 'px';
  put(c, el('span', 'v', value));
  if (o.tag) put(c, el('span', 'tag', o.tag));
  return c;
}

function coins(n, opts) {
  const o = opts || {};
  const w = el('div', 'bd-coins');
  put(w, el('span', 'stack' + (o.tone ? ' ' + o.tone : '')));
  put(w, el('b', null, fmt(n)));
  if (o.label) put(w, el('span', 'lab', o.label));
  return w;
}

function chip(n, label) {
  const c = el('div', 'bd-chip' + (n > 0 ? ' up' : n < 0 ? ' down' : ''));
  put(c, el('b', null, signed(n)));
  if (label) put(c, el('span', null, label));
  return c;
}

// ----------------------------------------------------------------- track --
function track(cells, opts) {
  // A strip of numbered steps -- lots, letters, rounds, seasons.
  const o = opts || {};
  const t = el('div', 'bd-track');
  cells.forEach(c => {
    const d = el('div', 'step' + (c.now ? ' now' : '') + (c.done ? ' done' : '') +
      (c.tone ? ' ' + c.tone : ''));
    put(d, el('span', 'n', c.label));
    if (c.sub !== undefined && c.sub !== null) put(d, el('span', 'sub', c.sub));
    if (c.tag) put(d, el('span', 'tag', c.tag));
    if (c.onClick) { d.classList.add('pick'); d.onclick = c.onClick; }
    put(t, d);
  });
  return t;
}

function ring(nodes, opts) {
  // A circle of seats with arrows between them, for games whose rules name a
  // direction ("raids always target clockwise").
  const o = opts || {};
  const R = 62, C = 92;
  const s = svg('svg', { viewBox: '0 0 184 184', class: 'bd-ring' });
  const at = i => {
    const a = -Math.PI / 2 + (2 * Math.PI * i) / nodes.length;
    return [C + R * Math.cos(a), C + R * Math.sin(a)];
  };
  (o.arrows || []).forEach(([a, b]) => {
    const i = nodes.findIndex(n => n.name === a), j = nodes.findIndex(n => n.name === b);
    if (i < 0 || j < 0) return;
    const [x1, y1] = at(i), [x2, y2] = at(j);
    const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1;
    const pad = 26;
    put(s, svg('line', {
      x1: x1 + (dx / L) * pad, y1: y1 + (dy / L) * pad,
      x2: x2 - (dx / L) * pad, y2: y2 - (dy / L) * pad,
      class: 'arrow', 'marker-end': 'url(#kit-arrow)',
    }));
  });
  const defs = svg('defs');
  const mk = svg('marker', {
    id: 'kit-arrow', viewBox: '0 0 8 8', refX: 6, refY: 4,
    markerWidth: 5, markerHeight: 5, orient: 'auto',
  });
  put(mk, svg('path', { d: 'M0,0 L8,4 L0,8 z', class: 'arrowhead' }));
  put(defs, mk); put(s, defs);
  nodes.forEach((n, i) => {
    const [x, y] = at(i);
    put(s, svg('circle', { cx: x, cy: y, r: 22, class: 'node ' + (n.me ? 'me ' : '') + seatClass(i) }));
    const t = svg('text', { x, y: y + 1, class: 'nm' });
    t.textContent = n.name.slice(0, 5);
    put(s, t);
    if (n.sub !== undefined && n.sub !== null) {
      const u = svg('text', { x, y: y + 13, class: 'sub' });
      u.textContent = n.sub;
      put(s, u);
    }
  });
  return s;
}

// ----------------------------------------------------------------- table --
function table(headers, rows, opts) {
  const o = opts || {};
  const t = el('table', 'bd-table' + (o.cls ? ' ' + o.cls : ''));
  if (headers) {
    const tr = el('tr');
    headers.forEach(h => put(tr, el('th', null, h)));
    put(t, put(el('thead'), tr));
  }
  const tb = el('tbody');
  rows.forEach(r => {
    const tr = el('tr', r.cls || null);
    (r.cells || r).forEach(c => {
      if (c && c.nodeType) { const td = el('td'); put(td, c); put(tr, td); }
      else put(tr, el('td', null, c === null || c === undefined ? '' : c));
    });
    put(tb, tr);
  });
  put(t, tb);
  return t;
}

function logList(lines, opts) {
  const o = opts || {};
  const box = el('div', 'bd-log');
  (lines || []).slice(-(o.limit || 6)).forEach(l => put(box, el('div', 'ln', l)));
  if (!box.children.length) put(box, el('div', 'ln dim', o.empty || 'nothing yet'));
  return box;
}

// --------------------------------------------------------------- controls --
function actions(list, send, opts) {
  // EVERY option gets the same class. This function is the reason that is
  // true twenty-three times rather than once. See the header.
  const o = opts || {};
  const row = el('div', 'bd-buttons' + (o.cls ? ' ' + o.cls : ''));
  (list || []).forEach(a => {
    const b = el('button', 'bd-opt', a.label);
    b.onclick = () => send(a.token, 'ui');
    put(row, b);
  });
  return row;
}

function choice(list, onPick, opts) {
  // A row of equal-weight toggles that reports a value instead of sending.
  // Nothing is selected until the player selects it.
  const o = opts || {};
  const row = el('div', 'bd-buttons' + (o.cls ? ' ' + o.cls : ''));
  const btns = [];
  (list || []).forEach(a => {
    const label = a.label !== undefined ? a.label : a;
    const value = a.value !== undefined ? a.value : label;
    const b = el('button', 'bd-opt', label);
    b.onclick = () => {
      btns.forEach(x => x.classList.remove('on'));
      b.classList.add('on');
      onPick(value);
    };
    btns.push(b); put(row, b);
  });
  if (o.value !== undefined && o.value !== null) {
    const i = (list || []).findIndex(a =>
      (a.value !== undefined ? a.value : (a.label !== undefined ? a.label : a)) === o.value);
    if (i >= 0) btns[i].classList.add('on');
  }
  return { node: row, buttons: btns };
}

function dial(o) {
  // Number entry with a slider, a box and step keys. The range comes from the
  // view, which took it from the prompt's own words.
  //
  // NOTHING IS PRE-SELECTED, and a dial is where that was easiest to lose.
  // `value: null` asks for a dial nobody has answered yet; it used to be
  // handed the bottom of the range instead, and the bottom of a range is still
  // a move -- a catch of zero, a bid of nothing, a declared figure at the
  // floor -- which `get()` then reported as though the player had named it.
  // An explicit null now opens the box empty and `get()` answers null until
  // the player types, nudges or drags. Omitting `value` still opens at `lo`,
  // because a caller that wants a starting figure passes one.
  const lo = o.lo === undefined ? 0 : o.lo;
  const hi = o.hi === undefined ? 100 : o.hi;
  const step = o.step || 1;
  let value = o.value === undefined ? lo : o.value;

  const box = el('div', 'bd-dial');
  if (o.label) put(box, el('div', 'lab', o.label));
  const row = el('div', 'row');

  const minus = el('button', 'step', '−');
  const input = el('input');
  input.type = 'number'; input.min = lo; input.max = hi; input.step = step;
  input.autocomplete = 'off';
  input.placeholder = o.placeholder === undefined ? fmt(lo) + '\u2013' + fmt(hi)
    : o.placeholder;
  const plus = el('button', 'step', '+');
  const slide = el('input');
  slide.type = 'range'; slide.min = lo; slide.max = hi; slide.step = step;

  // Both halves are one field, so both carry the label. A range input cannot
  // be blank, so an unanswered dial says so in words rather than reading as a
  // slider parked on its floor.
  const named = o.aria || o.label || 'value';
  input.setAttribute('aria-label', named);
  slide.setAttribute('aria-label', named);

  function quantise(v) {
    if (v === '' || v === null || v === undefined) return null;
    const n = Number(v);
    return Number.isFinite(n) ? Math.round(n / step) * step : null;
  }

  // The one place the box, the slider and the blank state are put in agreement.
  function paint(from) {
    const blank = value === null;
    if (from !== 'input') input.value = blank ? '' : value;
    // A blank dial still needs its thumb somewhere: it rests at the floor
    // without that being an answer.
    if (from !== 'slide') slide.value = blank ? lo : Math.max(lo, Math.min(hi, value));
    box.classList.toggle('unset', blank);
    if (blank) slide.setAttribute('aria-valuetext', 'not set');
    else slide.removeAttribute('aria-valuetext');
  }

  function set(v, from) {
    value = quantise(v);
    paint(from);
    if (o.onChange) o.onChange(value);
  }
  // Nudging an unanswered dial starts it at the floor: the first press picks a
  // value, it does not add a step to one that was never there.
  minus.onclick = () => set(value === null ? lo : value - step);
  plus.onclick = () => set(value === null ? lo : value + step);
  // The box is NOT clamped to [lo, hi]: the range in the view is the range the
  // prompt stated, and a prompt that states a range is not the same thing as
  // an engine that enforces one. Typing past it has to stay possible.
  input.oninput = () => set(input.value === '' ? null : input.value, 'input');
  // Dragging reports through `input`. A click that drops the thumb exactly
  // where it already sits reports nothing at all, which would leave a blank
  // dial blank after the player plainly chose the floor -- so the release and
  // `change` are read too, and a repeat of the value already held is dropped
  // rather than announced twice.
  function fromSlide() {
    const n = quantise(slide.value);
    if (n !== value) set(n, 'slide');
  }
  slide.oninput = fromSlide;
  slide.addEventListener('change', fromSlide);
  slide.addEventListener('pointerup', fromSlide);

  paint();
  put(row, minus, input, plus);
  put(box, row, slide);
  if (o.hint) put(box, el('div', 'hint', o.hint));
  return {
    node: box, get: () => value, set: v => set(v), clear: () => set(null), input,
  };
}

function textbox(o) {
  const box = el('div', 'bd-textbox');
  if (o.label) put(box, el('div', 'lab', o.label));
  const row = el('div', 'row');
  const inp = el('input');
  inp.type = 'text'; inp.placeholder = o.placeholder || '';
  inp.autocomplete = 'off'; inp.spellcheck = false;
  const btn = el('button', 'bd-send', o.send || 'send');
  const go = () => o.onSend(inp.value);
  btn.onclick = go;
  inp.onkeydown = e => { if (e.key === 'Enter') go(); };
  put(row, inp, btn);
  put(box, row);
  return { node: box, input: inp };
}

function submit(label, fn) {
  const b = el('button', 'bd-submit', label);
  b.onclick = fn;
  return b;
}

function quote(from, text) {
  const q = el('div', 'bd-quote');
  if (from) put(q, el('div', 'who', from));
  put(q, el('div', 'txt', '“' + text + '”'));
  return q;
}

function matrix(o) {
  // A payoff table drawn as a table. Rows are your move, columns are theirs.
  const t = el('table', 'bd-matrix');
  const head = el('tr');
  put(head, el('th', null, ''));
  o.cols.forEach(c => put(head, el('th', null, c)));
  put(t, put(el('thead'), head));
  const tb = el('tbody');
  o.rows.forEach((r, i) => {
    const tr = el('tr');
    put(tr, el('th', null, r));
    o.cols.forEach((c, j) => {
      const td = el('td');
      const cell = o.cell(i, j);
      put(td, el('span', 'me', cell[0]), el('span', 'sep', '/'),
        el('span', 'them', cell[1]));
      put(tr, td);
    });
    put(tb, tr);
  });
  put(t, tb);
  return t;
}

return {
  el, svg, put, frag, fmt, signed, resetMemo, memo,
  board, head, panels, panel, wide, note, act, scoreboard, seatClass,
  meter, bars, card, rankCard, cardRow, die, diceRow, letterTile, crate,
  coins, chip, track, ring, table, logList, actions, choice, dial, textbox,
  submit, quote, matrix,
};
})();
