'use strict';
/*
  ICEBOUND -- three crews in a ring, pledges then acts.

  THE RING IS THE POINT OF THIS BOARD. "Raids always target clockwise:
  North->East, East->West, West->North" is one line of prose that a player
  otherwise re-derives every round, so it is drawn as the ring it describes
  with the arrows on it. That line arrives once, in the round 1 rules, so it
  is cached (see `KIT.memo`) -- as are the fuel costs, and the seat's own name.

  NEITHER STAGE MARKS AN ANSWER. The three missions are one row of identical
  buttons in the order the prompt names them, at both stages. The act stage
  draws the public pledges above them and says nothing about which act
  "matches" one: that the act must repeat the pledge is a rule the player was
  told, and a board that greyed out the other two, or drew the repeat as the
  primary, would be enforcing that rule on the referee's behalf. Whether the
  player keeps it is the measurement.

  The pledge stage does leave out a mission the prompt says you cannot afford.
  That is the prompt's own "You can afford:" line -- a condition the referee
  states it checks when the pledge is submitted -- and not the board's opinion
  of the move; it is named in text underneath so the omission is visible
  rather than silent. Whatever survives is rendered with equal weight.

  THE WIRE FORMAT STAYS OFF THE BOARD. A button carries its mission and its
  own name; the adapter's template is filled and posted in one step by
  `ctx.sendFilled`, which is also what refuses a template whose slot is still
  empty. See `missionRow`.
*/
window.UI = window.UI || {};

(function () {
const K = () => window.KIT;

const MISSIONS = ['scout', 'escort', 'raid'];

function missionsOf(v) {
  return (v.missions && v.missions.length) ? v.missions : MISSIONS;
}

// One row of buttons, one class, prompt order, nothing pre-selected.
//
// A button carries the mission and nothing else. The adapter hands over the
// grammar with a hole in it (`[pledge: {m}]`) and `ctx.sendFilled` puts the
// mission in that hole on the way out, so the wire format is never rebuilt
// here, never reaches a label, and a hole this board could not fill is
// reported by the host instead of posted half-written. The player never sees
// a bracket.
//
// A stage that arrived without a template has no move in it: it says so
// rather than posting `[pledge: ]` against a player who did nothing wrong.
function missionRow(k, list, v, ctx, err) {
  return k.actions(list.map(m => ({ label: m, token: m })), m => {
    if (!v.token) { err.textContent = 'no reply form came with this stage.'; return; }
    err.textContent = '';
    ctx.sendFilled(v.token, { m: m });
  });
}

function ringPanel(k, ring, nodes) {
  const p = k.panel('the ring',
    ring ? k.ring(nodes, { arrows: ring })
      : k.bars(nodes.map((n, i) => ({ label: n.name, value: 1, seat: i })), { max: 1 }));
  if (ring) {
    k.put(p, k.note('Raids target clockwise: ' +
      ring.map(pair => pair[0] + ' → ' + pair[1]).join(', ') + '.'));
  } else {
    k.put(p, k.note('The clockwise order is on the rules card.'));
  }
  return p;
}

window.UI.icebound_pledge = function (v, ctx) {
  const k = K();
  const ring = k.memo('icebound.ring', v.ring);
  const cost = k.memo('icebound.cost', v.cost);
  k.memo('icebound.me', v.me);           // the act prompt never repeats it

  const fuel = v.fuel || [];
  const box = k.board();

  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: v.me,
    sub: 'pledge stage',
    scores: v.points || null,
    me: v.me,
  }));

  // -- fuel, one gauge a crew -------------------------------------------
  const tanks = k.panel('fuel',
    fuel.length ? k.bars(fuel.map((f, i) => ({ label: f.name, value: f.score, seat: i })))
      : k.note('the fuel line is on the rules card'));
  if (cost) {
    k.put(tanks, k.note('A pledge is charged when it is submitted: ' +
      missionsOf(v).map(m => m + ' ' + k.fmt(cost[m])).join(', ') + '.'));
  }

  // -- what the crews did in the rounds already played ------------------
  const log = v.log || [];
  const crewNames = log.length && log[0].crews ? log[0].crews.map(c => c.name) : [];
  const hist = k.panel('rounds so far',
    log.length && crewNames.length
      ? k.table([''].concat(crewNames), log.map(r => ({
        cells: ['round ' + r.round].concat((r.crews || []).map(c => c.pledged + ' / ' + c.acted)),
      })))
      : k.note('this is the first round'));
  if (log.length && crewNames.length) {
    k.put(hist, k.note('Each cell is that crew’s pledge and then its act.'));
  }

  k.put(box, k.panels(
    ringPanel(k, ring, fuel.map(f => ({ name: f.name, sub: f.score, me: f.name === v.me }))),
    tanks, hist));

  // -- the pledge -------------------------------------------------------
  const all = missionsOf(v);
  const afford = (v.afford && v.afford.length) ? v.afford : all;
  const legal = all.filter(m => afford.indexOf(m) >= 0);
  const shown = legal.length ? legal : all;
  const dropped = all.filter(m => shown.indexOf(m) < 0);

  const err = k.note('', 'warn');
  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'pledge one mission'));
  k.put(a, missionRow(k, shown, v, ctx, err));
  if (dropped.length) {
    k.put(a, k.note('The prompt lists what you can afford this round as ' +
      shown.join(', ') + '. It does not list ' + dropped.join(', ') + '.'));
  }
  k.put(a, err);
  k.put(box, a);
  return box;
};

window.UI.icebound_act = function (v, ctx) {
  const k = K();
  const ring = k.memo('icebound.ring', null);
  const me = k.memo('icebound.me', null);
  const pledges = v.pledges || [];
  const box = k.board();

  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: me || 'Icebound',
    sub: 'act stage' + (v.fuel === null || v.fuel === undefined
      ? '' : ' · ' + k.fmt(v.fuel) + ' fuel left'),
    me: me,
  }));

  // -- the pledges, as published, with no arithmetic over them ----------
  const table = k.panel('public pledges',
    pledges.length
      ? k.table(['crew', 'pledged'], pledges.map(p => ({
        cls: me && p.name === me ? 'mine' : '',
        cells: [p.name, p.pledge],
      })))
      : k.note('no pledges were printed'));
  if (v.fuel !== null && v.fuel !== undefined) {
    k.put(table, k.note('Your remaining fuel is ' + k.fmt(v.fuel) + '.'));
  }

  k.put(box, k.panels(
    ringPanel(k, ring, pledges.map(p => ({ name: p.name, sub: p.pledge, me: !!me && p.name === me }))),
    table));

  // -- the act. Every mission, same class, prompt order, nothing marked --
  const err = k.note('', 'warn');
  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'submit your act'));
  k.put(a, missionRow(k, missionsOf(v), v, ctx, err));
  k.put(a, err);
  k.put(box, a);
  return box;
};
})();
