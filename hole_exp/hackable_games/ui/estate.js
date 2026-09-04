'use strict';
/*
  ESTATE -- eight tiles, three investors, and books you keep yourself.

  The circuit is drawn as the circuit. Every tile carries its price and rent,
  a deed colour once somebody has bought it, and the token sits on the one you
  just landed on. That table arrives once, on lap 1, so it is cached (see
  `KIT.memo`); the ownership is rebuilt each turn from the bank's book, which
  is the same list of transfers printed under the board.

  Three tokens go in together and they are three separate controls, because
  they are three separate statements: what you paid, whether you bought, and
  what you now hold. The balance box is seeded with nothing. Seeding it with
  "last balance minus what is due" would be the board keeping the books, and
  keeping your own books is the game.
*/
window.UI = window.UI || {};

window.UI.estate_settle = function (v, ctx) {
  const K = window.KIT;
  const tiles = K.memo('estate.tiles', v.tiles) || [];

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
  const s = v.square;
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
  let payTo = null;
  const payDial = K.dial({ lo: 0, hi: 400, value: 0, label: 'paid this turn' });
  const who = K.choice(
    v.seats.filter(p => p !== v.seat).map(p => ({ label: 'to P' + p, value: p })),
    p => { payTo = p; });
  const buy = K.choice([{ label: 'yes', value: 'yes' }, { label: 'no', value: 'no' }], b => { buyVal = b; });
  let buyVal = null;
  const bal = K.dial({ lo: -999, hi: 9999, value: null, label: 'your cash after this turn' });

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'settle the turn'));
  K.put(a, K.panels(
    K.panel('pay', payDial.node, who.node),
    K.panel('buy', buy.node),
    K.panel('balance', bal.node)));
  const err = K.note('', 'warn');
  K.put(a, err);
  K.put(a, K.submit('settle', () => {
    const amt = payDial.get();
    if (buyVal === null) { err.textContent = 'say whether you are buying.'; return; }
    if (bal.get() === null) { err.textContent = 'declare a balance.'; return; }
    if (amt && payTo === null) { err.textContent = 'name who you paid, or set the amount to 0.'; return; }
    const pay = amt ? '[pay: ' + amt + ' to P' + payTo + ']' : '[pay: none]';
    ctx.send(pay + ' [buy: ' + buyVal + '] [balance: ' + bal.get() + ']', 'ui');
  }));
  K.put(box, a);
  return box;

  function key(label, cls) {
    const k = K.el('span', 'key');
    K.put(k, K.el('span', 'sw ' + (cls === 'mine' ? 's2' : cls === 'theirs' ? 's1' : 's0')),
      K.el('span', null, label));
    return k;
  }
};
