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

  NOTHING IN THE OFFER BUILDER STARTS ANSWERED. Both quantity dials open blank
  -- KIT's `value: null` -- because a dial handed a figure has already written
  half the offer, and `give 1 wood, get 1 ore` sitting on the screen is a move
  the player agrees to rather than one they chose. Submit names whatever is
  still unchosen and posts nothing until the counterparty, both quantities and
  both resources have each been named by hand.

  NO MOVE TEXT IS SPELLED OUT IN THIS FILE. The adapter ships the templates --
  `token` for the offer and the accept, `none_token` for declining, one token
  per build action -- and the board's only job is to fill their named slots.
  A board that wrote the verbs out itself would be a second copy of the
  prompt's grammar, free to drift from the one the referee actually reads.
*/
window.UI = window.UI || {};

(function () {
const K = () => window.KIT;

// Fill the {slots} of an adapter template. The host owns move text where it
// offers to: `ctx.sendFilled` fills and posts in one step and reports a
// template with a slot still empty itself, so it is the one to reach for.
// `ctx.fill` only HANDS BACK the text and still has to be sent. A host with
// neither -- an older shell, or a harness driving the board directly -- gets
// the substitution done here, so a board is never the thing that decides what
// a move looks like and never the thing that cannot post one.
function fill(ctx, tpl, vals) {
  if (ctx && typeof ctx.fill === 'function') return ctx.fill(tpl, vals);
  return String(tpl).replace(/\{(\w+)\}/g, (m, key) =>
    !vals || vals[key] === undefined || vals[key] === null ? m : String(vals[key]));
}

function poster(ctx) {
  const p = ctx && (ctx.sendFilled || ctx.sendChoice);
  return typeof p === 'function' ? p : null;
}

function sendFilled(ctx, tpl, vals) {
  const post = poster(ctx);
  if (post) return post.call(ctx, tpl, vals);
  return ctx.send(fill(ctx, tpl, vals), 'ui');
}

// One move is sometimes several tokens -- settling accepts two offers with two
// of them -- and the host fills and joins the whole list, so a move with one
// statement still blank is caught as a whole rather than posted with a hole in
// it. The parts are handed over intact for that reason: joining filled strings
// here would hide a half-finished token inside a line that looks complete.
function sendParts(ctx, parts) {
  const post = poster(ctx);
  if (post) return post.call(ctx, parts);
  return ctx.send(parts.map(p => fill(ctx, p.tpl, p.values)).join(' '), 'ui');
}

function sendNone(ctx, v) { return ctx.send(v.none_token, 'ui'); }

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

  // Five independent statements, five controls, nothing chosen for you: the
  // counterparty and the two resources start unpicked, both dials start
  // unanswered, and the dials travel the full range the prompt's grammar
  // admits rather than the range an honest offer lives in.
  //
  // `value: null` is the whole point of the two dials. They opened on 1 once,
  // which is a quantity nobody named -- the board had already decided the
  // shape of the trade and left the player to press one button. An unset dial
  // reports null from `get()` until it is typed, nudged or dragged, and note
  // that ZERO IS NOT UNSET: `give 0 wood` is a move this cell admits, so the
  // check below tests for null and never for falsehood.
  const err = k.note('', 'warn');
  const clear = () => { err.textContent = ''; };
  let to = null, gr = null, tr = null;
  const toPick = k.choice((v.others || []).map(o => ({ label: 'P' + o.seat, value: o.seat })),
    x => { to = x; clear(); });
  const gq = k.dial({ lo: -9, hi: 9, value: null, label: 'you give', onChange: clear });
  const grPick = k.choice(v.resources.map(r => ({ label: r, value: r })),
    x => { gr = x; clear(); });
  const tq = k.dial({ lo: -9, hi: 9, value: null, label: 'you get', onChange: clear });
  const trPick = k.choice(v.resources.map(r => ({ label: r, value: r })),
    x => { tr = x; clear(); });

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'post one offer, or none'));
  k.put(a, k.panels(
    k.panel('counterparty', toPick.node),
    k.panel('give', gq.node, grPick.node),
    k.panel('get', tq.node, trPick.node)));
  k.put(a, err);
  const row = k.el('div', 'bd-buttons');
  k.put(row, k.submit('post the offer', () => {
    // Every slot the adapter's template names is checked before anything is
    // posted, and the gaps are reported together: an offer missing one of its
    // five statements is not a move, and a player told only about the first
    // gap has to press the button again to hear about the next one.
    const gn = gq.get(), tn = tq.get();
    const missing = [];
    if (to === null) missing.push('a counterparty');
    if (gn === null) missing.push('how much you give');
    if (gr === null) missing.push('which resource you give');
    if (tn === null) missing.push('how much you get');
    if (tr === null) missing.push('which resource you get');
    if (missing.length) {
      err.textContent = 'nothing is posted yet -- still to choose: ' +
        missing.join(', ') + '.';
      return;
    }
    clear();
    sendFilled(ctx, v.token, { to: to, gn: gn, gr: gr, tn: tn, tr: tr });
  }));
  k.put(row, (() => {
    const b = k.el('button', 'bd-opt', 'none');
    b.onclick = () => sendNone(ctx, v);
    return b;
  })());
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

  // What you can pay for is said in words above and changes nothing here:
  // every action the adapter listed gets one button of the same weight, in
  // the order the prompt printed them, carrying the adapter's own token.
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

  const offers = v.offers || [];
  const chosen = new Set();
  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'accept any, all or none'));

  // Each offer is its own toggle. They do not clear one another, because
  // accepting two offers is a move this cell admits and a row of radio
  // buttons would have answered that on the player's behalf.
  const tally = k.note('');
  const retally = () => {
    tally.textContent = chosen.size
      ? 'settling accepts ' + chosen.size + ' of ' + offers.length + '.'
      : 'nothing is chosen, so settling declines every offer.';
  };

  if (!offers.length) k.put(a, k.note('Nothing was posted to you.'));
  offers.forEach(o => {
    const line = k.el('div', 'bd-row');
    const b = k.el('button', 'bd-opt', 'accept');
    b.setAttribute('aria-pressed', 'false');
    b.onclick = () => {
      const on = !chosen.has(o.from);
      if (on) chosen.add(o.from); else chosen.delete(o.from);
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', String(on));
      retally();
    };
    k.put(line, k.el('span', null,
      'p' + o.from + ' gives you ' + o.give.n + ' ' + o.give.res +
      ' and wants ' + o.want.n + ' ' + o.want.res), b);
    k.put(a, line);
  });

  retally();
  k.put(a, tally);
  const row = k.el('div', 'bd-buttons');
  k.put(row, k.submit('settle', () => {
    if (!chosen.size) return sendNone(ctx, v);
    sendParts(ctx, [...chosen].map(x => ({ tpl: v.token, values: { k: x } })));
  }));
  k.put(a, row);
  k.put(box, a);
  return box;
};
})();
