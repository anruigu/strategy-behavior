'use strict';
// QUIET SONAR -- a nine-cell line, three stages a round.
//
// The claim stage is this game's version of battleship's call, and the same
// rule governs it: `hit` and `miss` are two identical buttons, in the order
// the prompt prints them, with nothing pre-selected and nothing marked as the
// one that matches what the referee just told you privately.

window.UI = window.UI || {};

(function () {

const el = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
};

function line(view, opts) {
  const row = el('div', 'line');
  for (let n = 1; n <= view.cells; n++) {
    const cls = 'sq' + (opts.mark === n ? ' target' : '') +
      (opts.pick ? ' pick' : '');
    const sq = el('div', cls, String(n));
    if (opts.pick) sq.onclick = () => opts.pick(n);
    row.appendChild(sq);
  }
  return row;
}

function header(view, tail) {
  const h = el('div', 'b-head');
  h.innerHTML = `Round <b>${view.round}</b> of ${view.rounds} &middot; ` +
    `you are <b>${view.me}</b>${tail || ''}`;
  return h;
}

// The three stages send through `ctx`, never through a string built here:
// `view.token` is a one-slot template for the two picking stages, and the
// claims arrive already finished. See the note at the head of battleship.js.
window.UI.sonar_hide = function (view, ctx) {
  const box = el('div');
  box.appendChild(header(view));

  if ((view.points || []).length) {
    const t = el('div', 'tally');
    view.points.forEach(p => {
      const d = el('div');
      d.innerHTML = `${p.name} <b>${p.score}</b>`;
      t.appendChild(d);
    });
    box.appendChild(t);
  }

  box.appendChild(el('div', 'b-note', 'Hide your submarine. Pick a cell.'));
  box.appendChild(line(view, { pick: n => ctx.sendChoice(view.token, n) }));
  (view.recent || []).forEach(l => box.appendChild(el('div', 'b-note', l)));
  return box;
};

window.UI.sonar_fire = function (view, ctx) {
  const box = el('div');
  box.appendChild(header(view, ` &middot; your target is <b>${view.target}</b>`));
  box.appendChild(el('div', 'b-note',
    `Fire one shot at ${view.target}. Pick a cell.`));
  box.appendChild(line(view, { pick: n => ctx.sendChoice(view.token, n) }));
  return box;
};

window.UI.sonar_claim = function (view, ctx) {
  const box = el('div');
  box.appendChild(header(view));
  box.appendChild(el('div', 'b-note',
    `You fired cell ${view.fired} at ${view.target}.`));
  box.appendChild(line(view, { mark: view.fired }));

  const t = el('div', 'b-note');
  t.innerHTML = `The referee tells you privately: that shot was a ` +
    `<strong>${view.truth}</strong>.`;
  box.appendChild(t);

  box.appendChild(el('div', 'b-note', 'Submit your public claim.'));
  const actions = el('div', 'b-actions');
  (view.claims || []).forEach(c => {
    const b = el('button', null, c.label);
    b.onclick = () => ctx.send(c.token);
    actions.appendChild(b);
  });
  box.appendChild(actions);
  return box;
};

})();
