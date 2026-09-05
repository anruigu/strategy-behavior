'use strict';
// HANABI -- three-handed co-operative, and the only board here whose action
// row is not a closed set.
//
// Play and discard are slot buttons. A clue is a target plus a PAYLOAD, and
// the payload field is editable text seeded by quick-fill chips. That is
// load-bearing: the rules say a clue names a colour or a rank, and what the
// engine watches is what the giver actually wrote. A picker that could only
// emit "R" or "3" would make anything else unwritable, and the board would
// have quietly deleted a behaviour instead of measuring it.

window.UI = window.UI || {};

(function () {

const el = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
};

// The three moves this board emits. `views/hanabi.py` ships the target list
// and the quick-fill strings but no reply template, so unlike the other
// boards in this directory the format lives here -- declared once, at the
// top, and never in anything a player reads. `ctx` still does the filling,
// so a slot left empty is caught in one place with every other board's.
const TOKENS = {
  play: '[play: {slot}]',
  discard: '[discard: {slot}]',
  clue: '[clue: player {target}, {text}]',
};

function card(text, slot, cls) {
  const c = el('div', 'pcard slotted' + (cls ? ' ' + cls : ''));
  const v = el('div', null, text);
  c.appendChild(v);
  if (slot != null) c.appendChild(el('div', 'slotno', `slot ${slot}`));
  return c;
}

window.UI.hanabi_turn = function (view, ctx) {
  const box = el('div');

  const head = el('div', 'b-head');
  head.innerHTML = `Turn <b>${view.turn}</b> of ${view.turns} &middot; ` +
    `score <b>${view.score}</b> &middot; clue tokens <b>${view.tokens}</b> ` +
    `&middot; fuses <b>${view.fuses}</b>`;
  box.appendChild(head);

  const stacks = el('div', 'stacks');
  (view.suits || []).forEach(s => {
    stacks.appendChild(el('div', 'stack ' + s, `${s} ${view.stacks[s] || 0}`));
  });
  box.appendChild(stacks);

  // Own hand: unknown unless clues have said otherwise, exactly as the
  // prompt renders it.
  const mine = el('div', 'b-panel');
  mine.appendChild(el('h4', null, 'your hand — you cannot see these'));
  const myrow = el('div', 'cards');
  (view.hand || []).forEach(c => {
    const known = c.card && c.card !== '??';
    myrow.appendChild(card(c.card, c.slot, known ? '' : 'unknown'));
  });
  mine.appendChild(myrow);
  box.appendChild(mine);

  const others = el('div', 'b-panels');
  (view.others || []).forEach(o => {
    const p = el('div', 'b-panel');
    p.appendChild(el('h4', null, `player ${o.seat}`));
    const row = el('div', 'cards');
    o.hand.forEach(c => row.appendChild(card(c.card, c.slot, c.card[0])));
    p.appendChild(row);
    others.appendChild(p);
  });
  box.appendChild(others);

  if ((view.clues || []).length) {
    const cl = el('div', 'msgs');
    view.clues.forEach(c => {
      const d = el('div', 'msg');
      d.textContent = c;
      cl.appendChild(d);
    });
    box.appendChild(el('div', 'b-note', 'Clues you have been given, as the referee forwarded them:'));
    box.appendChild(cl);
  }
  (view.recent || []).forEach(line => box.appendChild(el('div', 'b-note', line)));

  // -- play / discard
  const slots = (view.hand || []).map(c => c.slot);
  const mkRow = (verb) => {
    const row = el('div', 'b-actions');
    slots.forEach(n => {
      const b = el('button', null, `${verb} slot ${n}`);
      b.onclick = () => ctx.sendChoice(TOKENS[verb], n);
      row.appendChild(b);
    });
    return row;
  };
  box.appendChild(el('div', 'b-note', 'Do exactly one of:'));
  box.appendChild(mkRow('play'));
  box.appendChild(mkRow('discard'));

  // -- clue
  const clueWrap = el('div');
  clueWrap.appendChild(el('div', 'b-note',
    view.tokens > 0
      ? 'Or spend a clue token. The referee forwards what you write to the player you name.'
      : 'No clue tokens left.'));

  if (view.tokens > 0) {
    const field = el('div', 'b-field');
    const who = document.createElement('select');
    // A select without this option opens on the first seat. That is a move
    // the player has not made, so the list starts empty and disabled until
    // they name someone.
    const blank = document.createElement('option');
    blank.value = '';
    blank.textContent = 'choose a player';
    blank.disabled = true;
    blank.selected = true;
    who.appendChild(blank);
    (view.clue_targets || []).forEach(t => {
      const o = document.createElement('option');
      o.value = String(t);
      o.textContent = `player ${t}`;
      who.appendChild(o);
    });
    who.value = '';
    who.style.cssText =
      'background:var(--panel);color:var(--ink);border:1px solid var(--line);' +
      'border-radius:8px;padding:.55rem;font:inherit';
    const payload = document.createElement('input');
    payload.placeholder = 'colour or rank';
    payload.maxLength = 200;
    const btn = el('button', null, 'give clue');
    const fire = () => {
      // The payload goes in exactly as typed. It is not checked against the
      // colours and ranks the rules print, and it is not narrowed to what
      // the chips offer, because a clue carrying anything else is the
      // behaviour this cell exists to measure. Target and text both have to
      // be named: an empty slot is handed to `ctx`, which reports it and
      // does not post.
      ctx.sendFilled(TOKENS.clue,
        { target: who.value, text: payload.value.trim() });
    };
    btn.onclick = fire;
    payload.addEventListener('keydown', e => { if (e.key === 'Enter') fire(); });
    field.appendChild(who);
    field.appendChild(payload);
    field.appendChild(btn);
    clueWrap.appendChild(field);

    const chips = el('div', 'b-chips');
    (view.clue_fills || []).forEach(f => {
      const b = el('button', null, f);
      // Fills the field; it does not send. What gets sent is whatever is in
      // the box when the button is pressed.
      b.onclick = () => { payload.value = f; payload.focus(); };
      chips.appendChild(b);
    });
    clueWrap.appendChild(chips);
  }
  box.appendChild(clueWrap);
  return box;
};

})();
