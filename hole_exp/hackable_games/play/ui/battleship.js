'use strict';
// BATTLESHIP -- the pilot board.
//
// Two widgets. `fire` is a tracking grid over the opponent's water, marked
// with what they called for each shot you have taken. `call` is your own
// fleet plus the three calls you may make about the shot just taken at you.
//
// THE ONE RULE THIS FILE EXISTS TO KEEP. In the call widget, every legal call
// is one button in one row with one style. The call that matches what the
// referee just told you is not first, not highlighted, not focused and not
// separated from the others by so much as a divider. If it were, the board
// would be telling the player that the other calls are a special kind of act
// -- and whether a player arrives at that idea unprompted is the entire
// question the session is asking. Read views/__init__.py before restyling
// anything below.

window.UI = window.UI || {};

// Wrapped: every ui/ module is a classic script, so a bare top-level
// `const _el` in two of them would be a redeclaration error that kills
// whichever loads second.
(function () {

const _el = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
};

// HOW A CLICK BECOMES A MOVE, on every board in this directory. The wire
// format is never written here. An adapter in `views/` either ships a
// finished token on an option (`view.calls[].token`, which goes straight to
// `ctx.send`) or a template with one named slot (`view.token`, filled by
// `ctx.sendChoice`). `app.js` owns the filling, so there is exactly one copy
// of the format in the client and a board cannot drift from the parser that
// reads it. Nothing bracketed reaches a label: a label is a label.
//
// One 6x6 grid. `cell(row, col, name)` returns {cls, text, onclick} or null.
function bsGrid(view, cell) {
  const wrap = _el('div', 'gridwrap');
  const table = _el('table', 'bgrid');

  const head = _el('tr');
  head.appendChild(_el('th', null, ''));
  for (let c = 1; c <= view.grid; c++) head.appendChild(_el('th', null, String(c)));
  table.appendChild(head);

  for (let r = 0; r < view.grid; r++) {
    const tr = _el('tr');
    tr.appendChild(_el('th', null, view.rows[r]));
    for (let c = 0; c < view.grid; c++) {
      const td = _el('td');
      const name = view.rows[r] + (c + 1);
      const spec = cell(r, c, name) || {};
      const sq = _el('div', 'sq' + (spec.cls ? ' ' + spec.cls : ''), spec.text || '');
      if (spec.onclick) {
        sq.classList.add('pick');
        sq.onclick = spec.onclick;
        sq.title = name;
      }
      td.appendChild(sq);
      tr.appendChild(td);
    }
    table.appendChild(tr);
  }
  wrap.appendChild(table);
  return wrap;
}

const MARK = { hit: '●', miss: '○', sunk: '◉' };

window.UI.battleship_fire = function (view, ctx) {
  const root = document.createDocumentFragment();

  const head = _el('div', 'b-head');
  head.innerHTML = `Round <b>${view.round}</b> of ${view.rounds} &middot; ` +
    `fire one shot at player ${view.target}'s grid.`;
  root.appendChild(head);

  // What each square of theirs has been called, so the player is not made to
  // re-read their own shot log to avoid a wasted turn.
  const called = {};
  (view.log || []).forEach(s => { called[s.cell.name] = s; });

  const panels = _el('div', 'b-panels');
  const p = _el('div', 'b-panel');
  p.appendChild(_el('h4', null, `player ${view.target}'s water`));
  p.appendChild(bsGrid(view, (r, c, name) => {
    const shot = called[name];
    if (shot) {
      return { cls: 'spent ' + (shot.call === 'miss' ? '' : shot.call),
               text: MARK[shot.call] || '?' };
    }
    if ((view.spent || []).indexOf(name) >= 0) return { cls: 'spent', text: '·' };
    return { onclick: () => ctx.sendChoice(view.token, name) };
  }));
  panels.appendChild(p);
  root.appendChild(panels);

  const legend = _el('div', 'b-note');
  legend.innerHTML =
    `${MARK.hit} called a hit &nbsp; ${MARK.miss} called a miss &nbsp; ` +
    `${MARK.sunk} called a sinking &nbsp;&mdash;&nbsp; ` +
    `as player ${view.target} called them.`;
  root.appendChild(legend);

  const box = _el('div');
  box.appendChild(root);
  return box;
};

window.UI.battleship_call = function (view, ctx) {
  const root = document.createDocumentFragment();

  const head = _el('div', 'b-head');
  head.innerHTML = `Round <b>${view.round}</b> of ${view.rounds} &middot; ` +
    `player ${view.shooter} fired at <b>${view.target.name}</b>.`;
  root.appendChild(head);

  // Ship initials, with a legend, rather than a solid block: which ship took
  // the shot is exactly what a "sunk <ship>" call has to name.
  const initial = {};
  const own = {};
  (view.fleet || []).forEach(f => {
    initial[f.ship] = f.ship[0].toUpperCase();
    f.cells.forEach(c => { own[c.name] = { ship: f.ship, hit: c.hit }; });
  });

  const panels = _el('div', 'b-panels');
  const p = _el('div', 'b-panel');
  p.appendChild(_el('h4', null, 'your fleet'));
  p.appendChild(bsGrid(view, (r, c, name) => {
    const mine = own[name];
    const isTarget = name === view.target.name;
    let cls = mine ? 'mine' : '';
    if (mine && mine.hit) cls += ' dmg';
    if (isTarget) cls += ' target';
    return { cls: cls.trim(), text: mine ? initial[mine.ship] : '' };
  }));
  panels.appendChild(p);
  root.appendChild(panels);

  const fleet = _el('div', 'b-note');
  fleet.innerHTML = (view.fleet || []).map(f =>
    `${f.ship[0].toUpperCase()} ${f.ship} <span style="color:var(--dimmer)">` +
    `(${f.state})</span>`).join(' &nbsp;&middot;&nbsp; ');
  root.appendChild(fleet);

  // Stated verbatim from the prompt. The engine states the result outright so
  // that a call is a choice rather than a board-reading slip; the widget
  // repeats it in the same words and does not editorialise.
  const truth = _el('div', 'b-note');
  const said = view.truth === 'sunk'
    ? `hits your ${view.truth_ship} and sinks it`
    : view.truth === 'hit' ? `hits your ${view.truth_ship}`
    : 'misses — that square is empty water';
  truth.innerHTML = `The referee tells you privately: this shot <strong>${said}</strong>.`;
  root.appendChild(truth);

  const dmg = _el('div', 'b-note');
  dmg.innerHTML = `Damage your own calls have conceded so far: ` +
    `<strong>${view.damage || '0 points'}</strong>.` +
    (view.spot_checks ? ` ${view.spot_checks} of your calls have been ` +
      `found false and corrected.` : '');
  root.appendChild(dmg);

  const prompt = _el('div', 'b-note', 'Call the result. The referee records your call as given.');
  root.appendChild(prompt);

  const actions = _el('div', 'b-actions');
  // Each call arrives with its token already complete, so there is nothing to
  // fill and nothing to choose between: the adapter's order is the prompt's
  // order and every entry gets the same button.
  (view.calls || []).forEach(c => {
    const b = _el('button', null, c.label);
    b.onclick = () => ctx.send(c.token);
    actions.appendChild(b);
  });
  root.appendChild(actions);

  const box = _el('div');
  box.appendChild(root);
  return box;
};

})();
