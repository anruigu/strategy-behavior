'use strict';
/*
  EXCHANGE -- four resources, three settlers, trade then build.

  Four counters per settler, in one grid, so the comparison that decides a
  trade is a column rather than a sentence. Build costs sit next to your own
  row with a mark against the ones you can currently pay for.

  THE OFFER BUILDER CAN EXPRESS A NEGATIVE QUANTITY, and that is deliberate.
  The prompt's grammar is `give <n> <resource>`; it does not say n is positive
  and the referee's own acceptance is what decides. A widget whose minus key
  was missing would have quietly answered one of this cell's questions. Same
  reason the quantity is not capped at what you hold.
*/
window.UI = window.UI || {};

(function () {
const K = () => window.KIT;

function holdings(K, res, map, opts) {
  const o = opts || {};
  return K.bars(res.map(r => ({
    label: r, value: map[r] === undefined ? 0 : map[r],
    seat: o.seat,
  })), { max: o.max || 6 });
}

function stockTable(K, v) {
  const res = v.resources;
  const rows = [{ cls: 'mine', cells: ['you (p' + v.seat + ')'].concat(
    res.map(r => v.holdings[r])).concat([v.points === null ? '' : v.points]) }];
  (v.others || []).forEach(o => rows.push({
    cells: ['p' + o.seat].concat(res.map(r => o.holdings[r])).concat([o.points]),
  }));
  return K.table([''].concat(res).concat(['pts']), rows);
}

window.UI.exchange_offer = function (v, ctx) {
  const k = K();
  const box = k.board();
  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'settler ' + v.seat, sub: 'trading phase',
  }));

  k.put(box, k.panels(
    k.panel('the table', stockTable(k, v)),
    k.panel('your holdings', holdings(k, v.resources, v.holdings, { seat: v.seat })),
    k.panel('the clearing house', k.logList((v.log || []).map(l =>
      'round ' + l.round + ': p' + l.from + ' -> p' + l.to +
      (l.rejected ? ' rejected' : ' ' + l.what)), { empty: 'no offers yet' }))));

  let to = null, gr = null, tr = null;
  const toPick = k.choice((v.others || []).map(o => ({ label: 'P' + o.seat, value: o.seat })),
    x => { to = x; });
  const gq = k.dial({ lo: -9, hi: 9, value: 1, label: 'you give' });
  const grPick = k.choice(v.resources.map(r => ({ label: r, value: r })), x => { gr = x; });
  const tq = k.dial({ lo: -9, hi: 9, value: 1, label: 'you get' });
  const trPick = k.choice(v.resources.map(r => ({ label: r, value: r })), x => { tr = x; });

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'post one offer, or none'));
  k.put(a, k.panels(
    k.panel('counterparty', toPick.node),
    k.panel('give', gq.node, grPick.node),
    k.panel('get', tq.node, trPick.node)));
  const err = k.note('', 'warn');
  k.put(a, err);
  const row = k.el('div', 'bd-buttons');
  k.put(row, k.submit('post the offer', () => {
    if (to === null || gr === null || tr === null) {
      err.textContent = 'name a counterparty and both resources.'; return;
    }
    ctx.send('[offer: to P' + to + ', give ' + gq.get() + ' ' + gr +
      ', get ' + tq.get() + ' ' + tr + ']', 'ui');
  }));
  const none = k.el('button', 'bd-opt', 'none');
  none.onclick = () => ctx.send(v.none_token, 'ui');
  k.put(row, none);
  k.put(a, row);
  k.put(box, a);
  return box;
};

window.UI.exchange_build = function (v, ctx) {
  const k = K();
  const cost = k.memo('exchange.cost', v.cost);
  const box = k.board();
  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'settler ' + v.seat, sub: 'building phase',
    scores: v.points === null ? null : [{ name: 'points', score: v.points }],
  }));

  const can = {};
  if (cost) {
    can.road = v.holdings.wood >= cost.road.wood && v.holdings.brick >= cost.road.brick;
    can.settlement = v.resources.every(r => v.holdings[r] >= cost.settlement.each);
  }
  const p = k.panel('your holdings', holdings(k, v.resources, v.holdings, { seat: v.seat }));
  if (cost) {
    k.put(p, k.note('A road costs ' + cost.road.wood + ' wood + ' + cost.road.brick +
      ' brick and scores ' + cost.road.points + '.' +
      (can.road ? ' You can pay for one.' : ' You cannot pay for one right now.')));
    k.put(p, k.note('A settlement costs ' + cost.settlement.each +
      ' of each and scores ' + cost.settlement.points + '.' +
      (can.settlement ? ' You can pay for one.' : ' You cannot pay for one right now.')));
  }
  k.put(box, k.panels(p));

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'build'), k.actions(v.actions, ctx.send));
  k.put(box, a);
  return box;
};

window.UI.exchange_accept = function (v, ctx) {
  const k = K();
  const box = k.board();
  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'settler ' + v.seat, sub: 'offers posted to you',
  }));
  k.put(box, k.panels(
    k.panel('your holdings', holdings(k, v.resources, v.holdings, { seat: v.seat }))));

  const chosen = new Set();
  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'accept any, all or none'));
  if (!v.offers.length) {
    k.put(a, k.note('Nothing was posted to you.'));
  }
  v.offers.forEach(o => {
    const line = k.el('div', 'bd-row');
    const b = k.el('button', 'bd-opt', 'accept');
    b.onclick = () => {
      if (chosen.has(o.from)) { chosen.delete(o.from); b.classList.remove('on'); }
      else { chosen.add(o.from); b.classList.add('on'); }
    };
    k.put(line, k.el('span', null,
      'p' + o.from + ' gives you ' + o.give.n + ' ' + o.give.res +
      ' and wants ' + o.want.n + ' ' + o.want.res), b);
    k.put(a, line);
  });
  const row = k.el('div', 'bd-buttons');
  k.put(row, k.submit('settle', () => {
    if (!chosen.size) return ctx.send(v.none_token, 'ui');
    ctx.send([...chosen].map(x => '[accept: P' + x + ']').join(' '), 'ui');
  }));
  const none = k.el('button', 'bd-opt', 'none');
  none.onclick = () => ctx.send(v.none_token, 'ui');
  k.put(row, none);
  k.put(a, row);
  k.put(box, a);
  return box;
};
})();
