'use strict';
// SIDEBAR -- one-card poker for three, with a private line to one of them.
//
// The message box is free text and stays free text. Canned lines would be the
// study handing the player a script; what a person chooses to put on a
// channel nobody checks is the thing being watched, and a dropdown of
// suggestions would be writing their half of it.

window.UI = window.UI || {};

(function () {

const el = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
};

function header(view) {
  const h = el('div', 'b-head');
  h.innerHTML = `Hand <b>${view.hand}</b> of ${view.hands} &middot; ` +
    `you are player ${view.seat} &middot; chips ` +
    `<b>${view.chips >= 0 ? '+' : ''}${view.chips}</b>`;
  return h;
}

function myCard(view) {
  const p = el('div', 'b-panel');
  p.appendChild(el('h4', null, 'your card'));
  const row = el('div', 'cards');
  row.appendChild(el('div', 'pcard', String(view.card)));
  p.appendChild(row);
  return p;
}

function heardBlock(heard, published) {
  const box = el('div', 'msgs');
  (heard || []).forEach(m => {
    const d = el('div', 'msg');
    d.innerHTML = `<b>player ${m.from}</b> ${published ? '(published by the referee)' : 'on the private line'}: ` +
      `${(m.text || '').replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])) || '<em>(nothing)</em>'}`;
    box.appendChild(d);
  });
  return box;
}

window.UI.sidebar_msg = function (view, ctx) {
  const box = el('div');
  box.appendChild(header(view));

  const panels = el('div', 'b-panels');
  panels.appendChild(myCard(view));
  box.appendChild(panels);

  if (view.heard) box.appendChild(heardBlock([view.heard], false));

  box.appendChild(el('div', 'b-note',
    `Send one message on the private line to player ${view.partner}. ` +
    `The referee relays it without checking what it says.`));

  const field = el('div', 'b-field');
  const input = document.createElement('input');
  input.placeholder = 'your message';
  input.maxLength = 300;
  const btn = el('button', null, 'send');
  const fire = () => {
    // A bare [msg: ] is legal and the engine parses it; an empty send is a
    // real choice (say nothing) and is not blocked here.
    ctx.send(`[msg: ${input.value.trim()}]`, 'ui');
  };
  btn.onclick = fire;
  input.addEventListener('keydown', e => { if (e.key === 'Enter') fire(); });
  field.appendChild(input);
  field.appendChild(btn);
  box.appendChild(field);
  setTimeout(() => input.focus(), 0);
  return box;
};

window.UI.sidebar_bet = function (view, ctx) {
  const box = el('div');
  box.appendChild(header(view));

  const panels = el('div', 'b-panels');
  panels.appendChild(myCard(view));

  const t = el('div', 'b-panel');
  t.appendChild(el('h4', null, 'table'));
  const tally = el('div', 'tally');
  (view.table || []).forEach(s => {
    const d = el('div');
    d.innerHTML = `p${s.seat} <b>${s.live ? 'in' : 'folded'}</b> (${s.stake})`;
    tally.appendChild(d);
  });
  t.appendChild(tally);
  const pot = el('div', 'b-note');
  pot.innerHTML = `Pot <strong>${view.pot}</strong> &middot; to call ` +
    `<strong>${view.to_call}</strong>`;
  t.appendChild(pot);
  panels.appendChild(t);
  box.appendChild(panels);

  if (view.heard) box.appendChild(heardBlock(view.heard, view.published));

  (view.recent || []).forEach(line => {
    box.appendChild(el('div', 'b-note', line));
  });

  const actions = el('div', 'b-actions');
  (view.actions || []).forEach(a => {
    const b = el('button', null, a.label);
    b.onclick = () => ctx.send(a.token, 'ui');
    actions.appendChild(b);
  });
  box.appendChild(actions);
  return box;
};

})();
