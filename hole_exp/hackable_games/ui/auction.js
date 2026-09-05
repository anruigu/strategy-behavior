'use strict';
/*
  AUCTION -- five lots, ascending price, money you hold yourself.

  One ladder carries the three numbers the bid turns on: what the lot is worth
  to you at the top, the house's estimate as a mark, and the standing bid
  climbing from the bottom. Read as positions on one scale they are a picture;
  read as three sentences they are three sentences.

  THE REPLY IS ASSEMBLED HERE, NOT TYPED. The adapter hands the board the exact
  shapes the referee reads (`tokens`, `pass_token`); the board fills them and
  sends. Nothing about that wire format reaches the page -- a player who had to
  copy a punctuation pattern out of the prompt would be being measured on
  transcription. Both paths run through the same assembler, so a pass carries
  the same two parts a bid does and cannot come out short by one.

  TWO STATEMENTS, TWO CONTROLS, NEITHER NARROWED. The bid is a dial ranged to
  the lot's value, which the prompt gives you, and its box is not clamped to
  that range -- the prompt states a minimum raise, not a maximum, and a control
  that refused to exceed some number would be inventing a rule the referee
  never stated. The budget is a bare box: unseeded, no floor, no ceiling. The
  only budget figure in the prompt is the one you started with, and ranging the
  control on it would be the board saying the declaration has to agree with it.
  Bid and pass are one row of identical buttons with nothing pre-selected.
*/
window.UI = window.UI || {};

window.UI.auction_bid = function (v, ctx) {
  const K = window.KIT;
  const start = K.memo('auction.budget', v.start_budget);
  // The host substitutes into the adapter's shapes when it offers to; the
  // fallback keeps the board renderable on a plain `{ send }` context.
  const fill = ctx.fill || ((shape, n) => String(shape).replace('{n}', n));
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
  // `dial` seeds an absent value to its floor, which would have the board
  // naming an amount the player never named. Clear it back to empty.
  bid.set('');
  const bud = moneyBox('the budget you have left');

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'your move on this lot'));
  K.put(a, K.note('Both parts go together: what you are doing about the lot, ' +
    'and the budget you have left.'));

  const controls = K.el('div', 'bd-panels');
  K.put(controls, bid.node, bud.node);
  K.put(a, controls);

  const err = K.note('', 'warn');
  K.put(a, err);

  // One row, one class, prompt order, nothing pre-selected. Each option only
  // has to produce its own opening part; `send` adds the budget both owe.
  const options = [
    {
      label: 'bid',
      lead: () => {
        if (bid.get() === null) { err.textContent = 'name an amount, or pass.'; return null; }
        return fill(v.tokens.bid, bid.get());
      },
    },
    { label: 'pass', lead: () => v.pass_token },
  ];

  const row = K.el('div', 'bd-buttons');
  options.forEach(o => {
    const b = K.el('button', 'bd-opt', o.label);
    b.onclick = () => {
      err.textContent = '';
      const lead = o.lead();
      if (lead === null || lead === undefined) return;
      if (bud.get() === null) {
        err.textContent = 'every reply states the budget you have left, a pass included.';
        return;
      }
      ctx.send(lead + ' ' + fill(v.tokens.budget, bud.get()), 'ui');
    };
    K.put(row, b);
  });
  K.put(a, row);
  K.put(box, a);
  return box;

  function moneyBox(label) {
    // A number box and nothing else. No slider, because a slider needs two
    // ends and the prompt supplies neither for this figure.
    const w = K.el('div', 'bd-dial');
    K.put(w, K.el('div', 'lab', label));
    const inp = K.el('input');
    inp.type = 'number';
    inp.step = 1;
    inp.value = '';
    inp.autocomplete = 'off';
    K.put(w, K.put(K.el('div', 'row'), inp));
    return {
      node: w,
      get: () => (String(inp.value).trim() === '' ? null : Number(inp.value)),
    };
  }
};
