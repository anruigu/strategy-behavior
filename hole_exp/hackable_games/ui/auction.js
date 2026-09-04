'use strict';
/*
  AUCTION -- five lots, ascending price, money you hold yourself.

  One ladder carries the three numbers the bid turns on: what the lot is worth
  to you at the top, the house's estimate as a mark, and the standing bid
  climbing from the bottom. Read as positions on one scale they are a picture;
  read as three sentences they are three sentences.

  Bid and budget are two separate statements and get two separate dials. The
  bid dial's range runs to the lot's value, which the prompt gives you, and
  the box above it accepts anything typed into it -- the prompt states a
  minimum raise, not a maximum, and a control that refused to exceed some
  number would be inventing a rule the referee never stated.
*/
window.UI = window.UI || {};

window.UI.auction_bid = function (v, ctx) {
  const K = window.KIT;
  const start = K.memo('auction.budget', v.start_budget);
  const box = K.board();

  K.put(box, K.head({
    step: 'Lot ' + v.lot + ' / ' + v.lots,
    title: 'round ' + v.round + ' of ' + v.rounds,
    sub: 'bidder ' + v.seat,
  }));

  const top = Math.max(v.worth, v.estimate, v.standing) * 1.15 || 1;
  const ladder = K.panel('this lot',
    K.meter({
      value: v.standing, max: top, label: 'standing high bid',
      tone: v.standing >= v.worth ? 'bad' : 'good',
      marks: [{ at: v.estimate, label: 'estimate ' + v.estimate },
              { at: v.worth, label: 'worth ' + v.worth + ' to you' }],
      text: v.standing + (v.holder === null ? '  (no bids yet)' : '  from bidder ' + v.holder),
    }),
    K.note('Minimum raise ' + v.min_raise + ', so a raise starts at ' +
      (v.standing + v.min_raise) + '.'));
  if (start !== null) K.put(ladder, K.note('You started with a budget of ' + start + '.'));

  const rows = (v.results || []).map(r => ({
    cls: r.bidder === v.seat ? 'mine' : '',
    cells: ['lot ' + r.lot, 'bidder ' + r.bidder, r.price],
  }));
  const done = K.panel('lots settled',
    rows.length ? K.table(['', 'won by', 'price'], rows) : K.note('none yet'));

  K.put(box, K.panels(ladder, done));

  const bid = K.dial({ lo: 0, hi: Math.max(1, v.worth), value: null, label: 'your bid' });
  const bud = K.dial({ lo: 0, hi: start || 999, value: null, label: 'the budget you have left' });

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'bid, or pass -- both tokens go together'));
  K.put(a, K.panels(K.panel('bid', bid.node), K.panel('budget', bud.node)));
  const err = K.note('', 'warn');
  K.put(a, err);
  const row = K.el('div', 'bd-buttons');
  K.put(row, K.submit('bid', () => {
    if (bid.get() === null) { err.textContent = 'name an amount, or pass.'; return; }
    if (bud.get() === null) { err.textContent = 'state the budget you have left.'; return; }
    ctx.send('[bid: ' + bid.get() + '] [budget: ' + bud.get() + ']', 'ui');
  }));
  const p = K.el('button', 'bd-opt', 'pass');
  p.onclick = () => {
    if (bud.get() === null) { err.textContent = 'a pass still states the budget you have left.'; return; }
    ctx.send('[bid: pass] [budget: ' + bud.get() + ']', 'ui');
  };
  K.put(row, p);
  K.put(a, row);
  K.put(box, a);
  return box;
};
