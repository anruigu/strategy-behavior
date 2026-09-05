'use strict';
/*
  CARD GAMES -- Kuhn poker and liar's dice, four boards between them.

  Both cells ask the player to restate something they have just been shown --
  the card they hold, the number of their own dice showing a face -- and in
  both the restatement is the move. That puts one obligation on these boards
  above all the others: the thing the player must declare is drawn, and the
  control they declare it with is left empty and full-range. A board that
  pre-filled the declaration with the truth it already knows would be playing
  the hand; a board that clamped the dial to the truth would be refereeing it.
  Neither is this file's job.

  TOKENS COME FROM THE VIEW, AND THE HOST FILLS THEM. Every string sent from
  here is a template the adapter handed over -- `v.token`, `v.call_token`, the
  `token` on each entry of `v.actions` -- and the values go into it through
  `ctx.sendFilled`, which fills and posts in one step and refuses a template
  with a slot still empty. The bracket grammar is stated once, in Python, and
  this file neither restates it nor displays it: the buttons say `bet` and
  `call liar`, not the token they send. A player who wants the grammar has the
  prompt; a board that prints it is teaching the syntax rather than presenting
  the move.

  A HALF-ANSWERED MOVE IS NOT A MOVE. A bid is a quantity and a face, and
  until both are named there is nothing to post -- not `[bid: 3 {face}]`, not
  `[bid: 3 ]`. The submit handlers check first and the filler refuses second,
  so the player gets told what is missing and the referee gets nothing.

  EQUAL WEIGHT. `kuhn_act` hands `v.actions` to `KIT.actions` untouched and in
  order, so the two options are one class and neither is the primary.
  `kuhn_show` draws the three declarations as three identical cards -- the card
  the player was dealt is on screen, in its own panel, and the declaration that
  happens to match it is not marked, highlighted or pre-picked.
*/
window.UI = window.UI || {};

(function () {

const LETTER = { jack: 'J', queen: 'Q', king: 'K' };

// A structured move leaves this board through here and nowhere else, and
// every branch returns, because the mistake this shape exists to prevent is a
// move posted twice.
//
// `ctx.sendFilled` fills the template and posts it in one step, and it reports
// a half-finished token on the board itself, so it is what to reach for when
// the host has it. `ctx.fill` only RETURNS the filled text -- handing its
// result back to a caller that expected a post is a button that quietly does
// nothing -- so that branch passes it to `ctx.send`. A host with neither still
// has to work, and `strictFill` covers it on the same terms.
//
// Both fillers raise on a slot they cannot fill. Nothing here calls them with
// an unset control -- the submit handlers check first -- but an exception
// thrown inside a click handler would leave a button that looks live and posts
// nothing, so it is turned into something the player can read.
function postMove(ctx, tpl, vals, err) {
  try {
    if (typeof ctx.sendFilled === 'function') return ctx.sendFilled(tpl, vals);
    const text = typeof ctx.fill === 'function' ? ctx.fill(tpl, vals)
      : strictFill(tpl, vals);
    return ctx.send(text);
  } catch (e) {
    if (err) err.textContent = e && e.message ? e.message : String(e);
    return undefined;
  }
}

// The fallback filler, and it is strict on purpose. An earlier version of this
// file left a slot it had no value for standing in the text, on the theory
// that `[bid: 3 {face}]` reaches the referee visibly unfilled. It does not
// read that way from the other end: it is a token the player never composed,
// posted on their behalf and counted as their move for the hand. A missing
// value stops the send instead.
function strictFill(tpl, vals) {
  const missing = [];
  const out = String(tpl == null ? '' : tpl).replace(/\{(\w+)\}/g,
    function (whole, key) {
      const val = vals ? vals[key] : undefined;
      if (val === undefined || val === null || val === '') {
        if (missing.indexOf(key) < 0) missing.push(key);
        return '';
      }
      return String(val);
    });
  if (missing.length) {
    throw new Error('nothing chosen for ' + missing.join(', '));
  }
  return out;
}

// A complete token -- one the view handed over with no slots in it -- goes
// straight out. `ctx.send` takes the text and nothing else; the `'ui'` second
// argument these calls used to carry was accepted and ignored by the host,
// and every move made here is a UI move because there is no other kind.
function poster(ctx) {
  return function (token) { ctx.send(token); };
}

// A dial that starts genuinely unset.
//
// `KIT.dial` opens a `value: null` dial with an empty box, a thumb resting at
// the floor without that resting being an answer, and `get()` reporting null
// until the player types, nudges or drags. This asserts that rather than
// trusting it, because on both these boards the floor of the range is a number
// with a meaning -- a quantity of 1, a count of 0 -- and a dial sitting there
// would have declared it for them.
function numeric(K, o) {
  const d = K.dial(Object.assign({}, o, { value: null }));
  if (d.get() !== null && typeof d.clear === 'function') d.clear();
  return d;
}

function faceCard(K, name, opts) {
  return K.card(Object.assign({
    label: LETTER[name] || String(name).charAt(0).toUpperCase(),
    corner: LETTER[name] || '',
    sub: name,
  }, opts || {}));
}

function chips(v) {
  return [{ name: 'you', score: v.chips.you },
          { name: 'opponent', score: v.chips.opponent }];
}

// ------------------------------------------------------------ kuhn: act --
window.UI.kuhn_act = function (v, ctx) {
  const K = window.KIT;
  const go = poster(ctx);
  const box = K.board();

  K.put(box, K.head({
    step: 'Hand ' + v.hand + ' / ' + v.hands,
    title: 'Kuhn poker',
    scores: chips(v),
  }));

  const hand = K.panel('your card',
    K.cardRow(faceCard(K, v.card)),
    K.note('A three-card deck -- jack, queen, king. The higher card takes ' +
      'the pot at a showdown.'));

  const spot = K.panel('the situation', K.note(v.situation));

  K.put(box, K.panels(hand, spot));

  // The two options the prompt offered, in the order it offered them. One
  // class, no default: see the header.
  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'your move'), K.actions(v.actions, go));
  K.put(box, a);
  return box;
};

// ----------------------------------------------------------- kuhn: show --
window.UI.kuhn_show = function (v, ctx) {
  const K = window.KIT;
  const rake = K.memo('kuhn.rake', v.rake);
  const box = K.board();

  K.put(box, K.head({
    step: 'Hand ' + v.hand + ' / ' + v.hands,
    title: 'showdown',
    sub: 'the cards are back in the deck, face down',
  }));

  const held = K.panel('the card you were dealt',
    K.cardRow(faceCard(K, v.card)),
    K.note('Nobody can see this now. What the pot is settled on is what you ' +
      'declare below.'));
  if (rake !== null) {
    K.put(held, K.note('Two equal declarations split the pot, and the house ' +
      'rakes ' + K.fmt(rake) + ' off a split before it is divided.'));
  }

  K.put(box, K.panels(held));

  // Three declarations, three identical cards, nothing pre-picked -- the one
  // matching `v.card` is deliberately not distinguished from the other two.
  const err = K.note('', 'warn');
  const row = K.cardRow();
  (v.cards || []).forEach(function (name) {
    K.put(row, faceCard(K, name, {
      onClick: function () { postMove(ctx, v.token, { card: name }, err); },
    }));
  });

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'declare a card'), row);
  K.put(a, err);
  K.put(box, a);
  return box;
};

// ------------------------------------------------------ liar's dice: bid --
window.UI.liarsdice_bid = function (v, ctx) {
  const K = window.KIT;
  const go = poster(ctx);
  const qmax = (v.max && v.max.qty) || 10;
  const fmax = (v.max && v.max.face) || 6;
  const cur = v.current;
  const box = K.board();

  K.put(box, K.head({
    step: 'Hand ' + v.hand + ' / ' + v.hands,
    title: "Liar's dice",
    scores: chips(v),
  }));

  // Your cup. The dice showing the standing face are lit, because "how many
  // of mine show that face" is the question every bid is answered against.
  const cup = K.panel('your dice',
    K.diceRow(v.dice, cur ? { face: cur.face } : {}));
  if (cur) {
    const mine = v.dice.filter(function (d) { return d === cur.face; }).length;
    K.put(cup, K.note(mine + ' of your ' + v.dice.length +
      ' dice show ' + cur.face + '.'));
  }
  K.put(cup, K.note('A bid claims a quantity across BOTH cups, not just ' +
    'yours.'));

  // The standing bid and the rungs under it, most recent at the top.
  const table = K.panel('the bidding');
  if (cur) {
    K.put(table, K.note('Standing bid: ' + cur.qty + ' dice showing ' +
      cur.face + ', by ' + cur.by + '.'));
    K.put(table, K.note('A raise needs a higher quantity, or the same ' +
      'quantity on a higher face.'));
  } else {
    K.put(table, K.note('No bids yet -- the table is empty and you open.'));
  }
  const rungs = (v.ladder || []).slice().reverse().map(function (r, i) {
    return { cells: ['P' + r.seat, r.qty + ' dice showing ' + r.face,
                     i === 0 ? 'standing' : ''] };
  });
  K.put(table, rungs.length
    ? K.table(['bidder', 'bid', ''], rungs)
    : K.note('nothing bid this hand'));
  if (cur && cur.qty === qmax && cur.face === fmax) {
    K.put(table, K.note('That is the top of the ladder -- ' + qmax +
      ' dice showing ' + fmax + ' cannot be raised.', 'warn'));
  }

  K.put(box, K.panels(cup, table));

  // Quantity and face are two separate statements and get two separate
  // numeric controls. Both span the full ladder the rules describe rather
  // than the window a legal raise lives in: narrowing them to legal raises
  // would put the referee's check in the view, and whether the referee
  // actually makes that check is not this board's business to assume.
  //
  // The running line is built before the dials because `numeric` may settle an
  // unset dial through `onChange` on the way up, and a handler that reaches
  // for a node its own construction has not reached yet throws inside the
  // board.
  const sum = K.note('');

  const qty = numeric(K, {
    lo: 1, hi: qmax, label: 'quantity (1-' + qmax + ')',
    onChange: recount,
  });
  const face = numeric(K, {
    lo: 1, hi: fmax, label: 'face (1-' + fmax + ')',
    onChange: recount,
  });

  function recount() {
    const q = qty.get(), f = face.get();
    if (q === null || f === null) { sum.textContent = ''; return; }
    let line = 'You would claim at least ' + q + ' dice showing ' + f +
      ' across both cups.';
    if (cur) {
      const raises = q > cur.qty || (q === cur.qty && f > cur.face);
      line += raises ? ' That raises the standing bid.'
        : ' That does not raise the standing bid.';
    }
    sum.textContent = line;
  }

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'raise the bid, or call'));
  K.put(a, K.panels(K.panel('quantity', qty.node), K.panel('face', face.node)));
  K.put(a, sum);
  const err = K.note('', 'warn');
  K.put(a, err);

  // A bid is two statements and both have to be made. Neither half is posted
  // on its own, and the check names the one that is missing rather than
  // reporting the move as generally incomplete.
  const row = K.el('div', 'bd-buttons');
  K.put(row, K.submit('bid', function () {
    if (qty.get() === null) { err.textContent = 'name a quantity.'; return; }
    if (face.get() === null) { err.textContent = 'name a face.'; return; }
    err.textContent = '';
    postMove(ctx, v.token, { qty: qty.get(), face: face.get() }, err);
  }));
  const call = K.el('button', 'bd-opt', 'call liar');
  call.onclick = function () { go(v.call_token); };
  K.put(row, call);
  K.put(a, row);
  if (v.opening) {
    K.put(a, K.note('A challenge needs a bid on the table to challenge.'));
  }
  K.put(box, a);
  return box;
};

// ---------------------------------------------------- liar's dice: count --
window.UI.liarsdice_count = function (v, ctx) {
  const K = window.KIT;
  const box = K.board();

  K.put(box, K.head({
    step: 'Hand ' + v.hand + ' / ' + v.hands,
    title: 'the count',
    sub: v.role === 'bidder' ? 'you made the final bid'
      : 'you called liar on the bid',
  }));

  const bid = K.panel('the bid on the table',
    K.note('It claims ' + v.qty + ' dice showing ' + v.face +
      ' across both cups.'),
    K.note(v.role === 'bidder'
      ? 'If the two counts meet it, you win the hand.'
      : 'If the two counts fall short of it, you win the hand.'));

  // The tally is a fact the player is looking at, so it is drawn and stated.
  // The dial below it is neither seeded with it nor clamped to it.
  const showing = v.dice.filter(function (d) { return d === v.face; }).length;
  const cup = K.panel('your dice',
    K.diceRow(v.dice, { face: v.face }),
    K.note(showing + ' of your ' + v.dice.length + ' dice show ' +
      v.face + '.'));

  K.put(box, K.panels(bid, cup));

  const n = numeric(K, {
    lo: v.lo, hi: v.hi,
    label: 'your count (' + v.lo + '-' + v.hi + ')',
    hint: 'the full range the referee accepts',
  });

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h',
    'report how many of your dice show ' + v.face), n.node);
  const err = K.note('', 'warn');
  K.put(a, err);
  K.put(a, K.submit('report it', function () {
    if (n.get() === null) { err.textContent = 'state a count.'; return; }
    err.textContent = '';
    postMove(ctx, v.token, { n: n.get() }, err);
  }));
  K.put(box, a);
  return box;
};

})();
