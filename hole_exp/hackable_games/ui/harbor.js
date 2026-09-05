'use strict';
/*
  HARBOR CUSTOMS -- a hold of crates, a manifest, and a way into port.

  The hold is drawn as crates sized by value, because "crates worth 7, 29, 31"
  is a hold and prose is a poor drawing of one. Both duty formulas are
  evaluated against whatever number is currently on the manifest dial: both
  are in the rules the seat was handed, and a player reaching for a calculator
  is not what this cell measures.

  THE ROUTE BOARD SHOWS NO ARITHMETIC. The night rate is the lower of the two,
  so a duty figure printed beside each route would read as a recommendation --
  and the cost that pays for the lower rate is not in the view's data. So the
  route stage is the declared figure and one row of identical buttons, and
  which of them is cheaper stays the player's to work out.

  The reply grammar lives in the view's `token`; it is filled in here and the
  bracket form is never put on screen.
*/
window.UI = window.UI || {};

(function () {
const K = () => window.KIT;

function fill(token, n) {
  return String(token).replace('{n}', String(n));
}

function figure(k, label, value) {
  const h = k.el('div', 'bd-hero');
  k.put(h, k.el('span', 'bd-big', k.fmt(value)), k.el('span', 'lab', label));
  return h;
}

function hold(k, crates) {
  const row = k.el('div', 'bd-crates');
  // No max is passed: the kit's own scale keeps one round's crates comparable
  // with the next, which a per-hold scale would not.
  crates.forEach(c => k.put(row, k.crate(c, null)));
  return row;
}

function dutyTable(k, duty, n) {
  // Object order is the view's order, which is the order the rules printed the
  // two routes. Every row is built the same way -- neither is marked.
  const rows = Object.keys(duty).map(name => [
    name,
    String(duty[name]) + ' x declared',
    n === null ? '--' : k.fmt(Math.floor(duty[name] * n)),
  ]);
  return k.table(['route', 'rate', 'duty on this figure'], rows);
}

function quayLog(k, log, names, me) {
  if (!log.length) return k.note('nothing has cleared the quay yet');
  if (!names.length) {
    return k.logList(log.map(l => 'round ' + l.round + ': declarations ' +
      l.declarations.join(', ') + ' -- routes ' + l.routes.join(', ')));
  }
  const head = [''].concat(names.map(nm => nm === me ? nm + ' (you)' : nm));
  const rows = log.map(l => [String(l.round)].concat(names.map((nm, i) => {
    const d = l.declarations[i];
    const r = l.routes[i];
    if (d === undefined) return '';
    return String(d) + (r === undefined ? '' : ' ' + r);
  })));
  return k.table(head, rows);
}

window.UI.harbor_declare = function (v, ctx) {
  const k = K();
  // The rules block prints once, on the seat's first prompt. The legal range
  // is restated every round, so only these two are cached.
  const duty = k.memo('harbor.duty', v.duty);
  const penalty = k.memo('harbor.penalty', v.penalty);
  const crates = v.crates || [];
  const points = v.points || [];

  const box = k.board();
  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: v.me, sub: 'declare stage',
    scores: points, me: v.me,
  }));

  const holdPanel = k.panel('your hold', hold(k, crates));
  const kv = k.el('div', 'bd-kv');
  k.put(kv, k.el('span', 'k', crates.length + ' crates, total'),
    k.el('span', 'v', k.fmt(crates.reduce((a, b) => a + b, 0))));
  k.put(holdPanel, kv);

  const dutyPanel = k.panel('duty');
  const dutyBox = k.el('div', 'bd-rows');
  k.put(dutyPanel, dutyBox);
  if (duty) {
    k.put(dutyPanel, k.note('Both figures are the rules’ own formulas worked ' +
      'against the number on the manifest.'));
  } else {
    k.put(dutyBox, k.note('The duty rates are not in this prompt.'));
  }
  if (penalty !== null && penalty !== undefined) {
    k.put(dutyPanel, k.note('A flagged manifest pays ' + k.fmt(penalty) +
      ' points.'));
  }

  const quay = k.panel('the quay',
    quayLog(k, v.log || [], points.map(p => p.name), v.me));

  k.put(box, k.panels(holdPanel, dutyPanel, quay));

  function recount() {
    if (!duty) return;
    dutyBox.textContent = '';
    k.put(dutyBox, dutyTable(k, duty, dial.get()));
  }

  const dial = k.dial({
    lo: v.lo, hi: v.hi, value: null,
    label: 'declared value of your hold (' + v.lo + ' to ' + v.hi + ')',
    onChange: recount,
  });
  // The kit seeds an empty dial with its low end, and here the low end is 0 --
  // a manifest declaring nothing, which is one of the sharper moves in the
  // game. It must be typed, not found already in the box. Clearing it also
  // draws the first duty column as blank rather than as the duty on a figure
  // the player has not written.
  dial.set(null);

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'write the manifest'));
  k.put(a, dial.node);
  const err = k.note('', 'warn');
  k.put(a, err, k.submit('hand over the manifest', () => {
    const n = dial.get();
    if (n === null) { err.textContent = 'write a value on the manifest.'; return; }
    if (!v.token) { err.textContent = 'no reply form came with this stage.'; return; }
    ctx.send(fill(v.token, n), 'ui');
  }));
  k.put(box, a);
  return box;
};

window.UI.harbor_route = function (v, ctx) {
  const k = K();
  const box = k.board();
  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'route stage',
  }));

  k.put(box, k.panels(k.panel('your manifest',
    figure(k, 'declared value of your hold', v.declared))));

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'take a route into port'));
  // One class, one order -- the view's, which is the prompt's. The token
  // travels with the button and is never shown.
  k.put(a, k.actions(v.routes, ctx.send));
  k.put(box, a);
  return box;
};
})();
