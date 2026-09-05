'use strict';
/*
  ESTATE -- eight tiles, three investors, and books you keep yourself.

  The circuit is drawn as the circuit. Every tile carries its price and rent,
  a deed colour once somebody has bought it, and the token sits on the one you
  just landed on. That table arrives once, on lap 1, so it is cached (see
  `KIT.memo`); the ownership is rebuilt each turn from the bank's book, which
  is the same list of transfers printed under the board.

  Three statements go in together and they are three separate controls,
  because they are three separate claims: what you paid, whether you bought,
  and what you now hold. The balance box is seeded with nothing. Seeding it
  with "last balance minus what is due" would be the board keeping the books,
  and keeping your own books is the game.

  NOBODY HERE TYPES THE ENGINE'S GRAMMAR. The reply the referee reads is one
  compound line naming all three statements, but its shape belongs to the
  adapter, which ships it in `tokens`, and it is filled by the host through
  `ctx.fill` / `ctx.sendFilled`. The player names an amount, a payee, yes or
  no, and a balance, and presses one button; the wire format never reaches
  the screen.
*/
window.UI = window.UI || {};

window.UI.estate_settle = function (v, ctx) {
  const K = window.KIT;
  const tiles = K.memo('estate.tiles', v.tiles) || [];
  // The shapes to fall back on if a turn arrives without `tokens`, so that a
  // settle is still possible. The adapter's own templates win when it sends
  // them, and either way these strings stay off the board.
  const wire = {
    pay: '[pay: {n} to P{k}]', pay_none: '[pay: none]',
    buy: '[buy: {yn}]', balance: '[balance: {n}]',
  };
  const tokens = Object.assign({}, wire, K.memo('estate.tokens', v.tokens) || {});

  // Who owns what, from the transfers the player is shown.
  const owner = {};
  (v.bought || []).forEach(b => { owner[b.tile] = b.who; });

  const box = K.board();
  K.put(box, K.head({
    step: 'Lap ' + v.lap + ' / ' + v.laps,
    title: 'Investor ' + v.seat,
    sub: v.roll !== null ? 'rolled ' + v.roll : '',
  }));

  // -- the circuit ------------------------------------------------------
  const steps = tiles.map(t => {
    const own = owner[t.name];
    const here = t.name === v.landed;
    return {
      label: t.name === 'START' ? '⌂' : t.name,
      sub: t.price === null ? 'salary' : t.price + ' / ' + t.rent,
      tag: own === undefined ? '' : (own === v.seat ? 'yours' : 'p' + own),
      now: here,
      tone: own === undefined ? '' : (own === v.seat ? 'mine' : 'theirs'),
    };
  });
  const circuit = K.panel('the circuit',
    steps.length ? K.track(steps) : K.note('the tile list is on the rules card'),
    K.el('div', 'bd-legend'));
  const lg = circuit.querySelector('.bd-legend');
  K.put(lg,
    key('you are here', 'now'), key('your deed', 'mine'), key('a rival’s deed', 'theirs'));

  // -- this turn --------------------------------------------------------
  const s = v.square || {};
  const turn = K.panel('this turn');
  if (v.landed) K.put(turn, K.note('You landed on ' + v.landed + '.'));
  if (v.passed_start) K.put(turn, K.note('You passed START -- salary ' + v.salary + '.'));
  if (s.state === 'for_sale') K.put(turn, K.note(s.tile + ' is unowned. Price ' + s.price + '.'));
  if (s.state === 'rent_due') K.put(turn, K.note('Rent of ' + s.due + ' is due to investor ' + s.owner + '.'));
  if (s.state === 'yours') K.put(turn, K.note('You own ' + s.tile + '. Nothing is due.'));
  if (s.state === 'clear' && !v.passed_start) K.put(turn, K.note('Nothing is due.'));
  if (v.received) K.put(turn, K.note('You received ' + v.received + ' from other investors since your last turn.'));
  K.put(turn, K.el('div', 'bd-kv'));
  const kv = turn.querySelector('.bd-kv');
  K.put(kv, K.el('span', 'k', 'last declared balance'), K.el('span', 'v', v.balance));

  // -- the bank's book --------------------------------------------------
  const bookLines = [];
  (v.bought || []).forEach(b => bookLines.push(
    'lap ' + b.lap + ': investor ' + b.who + ' bought ' + b.tile + ' for ' + b.price));
  (v.paid || []).forEach(p => bookLines.push(
    'lap ' + p.lap + ': investor ' + p.who + ' paid ' + p.amount + ' to investor ' + p.to));
  const book = K.panel('the bank’s book', K.logList(bookLines, { limit: 8, empty: 'nothing recorded yet' }));

  K.put(box, K.panels(circuit, turn, book));

  // -- the three statements ---------------------------------------------
  let payTo = null, buyVal = null;
  const payDial = K.dial({ lo: 0, hi: 400, value: null, label: 'amount you paid' });
  const who = K.choice(
    (v.seats || []).filter(p => p !== v.seat).map(p => ({ label: 'investor ' + p, value: p })),
    p => { payTo = p; });
  const buy = K.choice([{ label: 'yes', value: 'yes' }, { label: 'no', value: 'no' }],
    b => { buyVal = b; });
  const bal = K.dial({ lo: -999, hi: 9999, value: null, label: 'your cash after this turn' });
  // `KIT.dial` opens at the low end of its range when it is handed no value,
  // and the low end of a range is still an answer. Both boxes are emptied so
  // that the first number in them is one the player put there.
  payDial.set('');
  bal.set('');

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'settle the turn'));
  K.put(a, K.panels(
    K.panel('what you paid', payDial.node, who.node,
      K.note('leave the amount empty if you paid nobody')),
    K.panel(s.state === 'for_sale' && s.tile ? 'buy ' + s.tile : 'did you buy', buy.node),
    K.panel('your declared balance', bal.node)));
  const err = K.note('', 'warn');
  K.put(a, err);
  K.put(a, K.submit('settle', () => {
    const amt = payDial.get();
    if (buyVal === null) { err.textContent = 'say whether you are buying.'; return; }
    if (bal.get() === null) { err.textContent = 'declare a balance.'; return; }
    if (amt && payTo === null) { err.textContent = 'name who you paid, or leave the amount empty.'; return; }
    // All three statements every time, whichever way each one came out.
    reply([
      amt ? { tpl: tokens.pay, values: { n: amt, k: payTo } }
          : { tpl: tokens.pay_none, values: {} },
      { tpl: tokens.buy, values: { yn: buyVal } },
      { tpl: tokens.balance, values: { n: bal.get() } },
    ]);
  }));
  K.put(box, a);
  return box;

  // The host fills the adapter's templates when it can. The substitution
  // here is the same one, for a host that does not carry the hooks.
  function fill(tpl, values) {
    if (ctx.fill) return ctx.fill(tpl, values);
    return String(tpl).replace(/\{(\w+)\}/g, (m, k) =>
      values && values[k] !== undefined && values[k] !== null ? String(values[k]) : m);
  }

  function reply(parts) {
    if (ctx.sendFilled) return ctx.sendFilled(parts, 'ui');
    ctx.send(parts.map(p => fill(p.tpl, p.values)).join(' '), 'ui');
  }

  function key(label, cls) {
    const k = K.el('span', 'key');
    K.put(k, K.el('span', 'sw ' + (cls === 'mine' ? 's2' : cls === 'theirs' ? 's1' : 's0')),
      K.el('span', null, label));
    return k;
  }
};
