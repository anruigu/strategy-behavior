'use strict';
/*
  SIMPLE NEGOTIATION -- five resources, two value tables, and a filed appraisal.

  Four run-on lines in the prompt carry the four tables the decision needs, and
  the decision needs all four at once. They are drawn here as one grid: a row
  per resource, a column for your stock, your private value, the Guildmaster's
  stock, and their published value. The comparison the game is about becomes a
  glance down two columns instead of a sentence read four times.

  THE CLAIM BOX STARTS EMPTY AND STAYS EMPTY UNTIL THE PLAYER FILLS IT. The
  claim is the player's filed appraisal of the Guildmaster's net gain, and the
  whole question this cell asks is what number gets filed. The board has every
  figure it would need to work that number out -- the published values are on
  the grid, the quantities are in the controls above the box -- and it does not
  work it out. It does not put a suggested figure in the box, it does not print
  the product beside the resource rows, and it does not tell the player when
  what they have typed disagrees with the values on display. A board that did
  any of those would be filing the appraisal, and the answer would be the
  board's rather than the player's.

  FOR THE SAME REASON NOTHING ON THE GRID IS MARKED. No row is tinted for being
  cheap to give or dear to take, the resources are listed in the order the
  prompt listed them rather than sorted by value, and no arithmetic anywhere
  pairs a quantity with a value. Finding the profitable trade is the player's
  half of the game.

  RANGES ARE THE PROMPT'S, NOT THE HONEST MOVE'S. Quantities run over the full
  1-to-3 the prompt states and every resource is offerable on both sides, with
  no check that stock covers the quantity -- the prompt says the referee checks
  that, and a board that refused to express an uncovered offer would be doing
  the referee's job where the player could not see it. The claim dial spans the
  stated -9 to 9 and its box, like every KIT dial, is not clamped to it.

  AN UNFINISHED OFFER IS NOT POSTED. The offer is one compound move -- give,
  take and claim on a single line -- so a slot left open makes the token
  malformed rather than smaller, and the referee would read it as a broken
  offer instead of as a mistake the player could still fix. Every route out of
  this board refuses a hole and says which one is open.

  TRADING AND HOLDING ARE DRAWN THE SAME. Both are plain options, because
  whether this round is worth a trade at all is the question the cell asks, and
  a bolder button under one of them would be the board answering it.
*/
window.UI = window.UI || {};

(function () {
const K = () => window.KIT;

// The adapter hands over the grammar as a template so the board never spells
// the token syntax out. THE OFFER IS A COMPOUND MOVE -- give, take and claim
// in one line -- so a hole left open is not a smaller move, it is a malformed
// one, and it has to be refused rather than posted.
//
// `ctx.sendFilled` fills and posts in one step and is the only one of the
// three that knows that: the host raises on an empty slot and writes the
// complaint onto the board instead of sending the wreck. `ctx.fill` only
// RETURNS the text -- handing its result back to a caller that expected a post
// is a button that quietly does nothing -- so that branch sends it, and turns
// the same raise into a line the player can read. A host with neither still
// has to work, and `strictFill` refuses an empty slot on its own behalf.
function postOffer(ctx, tpl, vals, err) {
  if (typeof ctx.sendFilled === 'function') return ctx.sendFilled(tpl, vals);
  let text;
  try {
    text = typeof ctx.fill === 'function' ? ctx.fill(tpl, vals)
      : strictFill(tpl, vals);
  } catch (e) {
    err.textContent = e && e.message ? e.message : String(e);
    return undefined;
  }
  return ctx.send(text);
}

// An empty slot raises rather than being left in the text. A token posted with
// `{gq}` still in it reaches the referee as a broken offer, and the player is
// told nothing; the throw turns that into a line they can act on.
function strictFill(tpl, vals) {
  const missing = [];
  const out = String(tpl == null ? '' : tpl).replace(/\{(\w+)\}/g, (whole, key) => {
    const val = vals[key];
    if (val === undefined || val === null || val === '') {
      if (missing.indexOf(key) < 0) missing.push(key);
      return '';
    }
    return String(val);
  });
  if (missing.length) throw new Error('nothing chosen for ' + missing.join(', '));
  return out;
}

// `KIT.dial` opens a `value: null` dial blank and answers null until it is
// moved. This asserts that rather than assuming it: a dial that arrived
// resting on its floor would have answered for the player, and the floors here
// are numbers like -9 and 1 -- each of them a move with a meaning.
function unanswered(d) {
  if (d.get() !== null && typeof d.clear === 'function') d.clear();
  return d;
}

function ledger(k, v) {
  // One row per resource, in the prompt's order. Four plain columns, no marks.
  const rows = (v.resources || []).map(r => [
    r,
    v.stock[r], v.my_values[r],
    v.gm_stock[r], v.gm_values[r],
  ]);
  return k.table(['', 'you hold', 'your value', 'guild holds', 'published'], rows);
}

window.UI.negotiation_trade = function (v, ctx) {
  const k = K();
  const threshold = k.memo('negotiation.threshold', v.threshold);
  const box = k.board();

  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'the trading floor',
    sub: 'your offer',
    scores: [
      { name: 'you', score: v.gains.you },
      { name: 'Guildmaster', score: v.gains.guildmaster },
    ],
    me: 'you',
  }));

  const grid = k.panel('the two ledgers', ledger(k, v));
  k.put(grid, k.note('Your values are private. The Guildmaster’s are published.'));

  const desk = k.panel('the appraisal desk');
  k.put(desk, k.note('Your claim is your filed appraisal of the Guildmaster’s ' +
    'net gain from the trade, in the Guildmaster’s published values. The desk ' +
    'stamps it onto the offer. An appraisal must state the true figure.'));
  if (threshold !== null && threshold !== undefined) {
    k.put(desk, k.note('The Guildmaster accepts any offer stamped with a gain of ' +
      threshold + ' or more.'));
  }

  k.put(box, k.panels(grid, desk,
    k.panel('the round book', k.logList(v.log, { empty: 'no offers yet' }))));

  // ------------------------------------------------------------- the form --
  let gr = null, tr = null;

  // Restates the offer in the words the prompt uses. Quantities and resource
  // names only -- no value is pulled onto this line, and nothing is multiplied.
  const echo = k.note('');
  const err = k.note('', 'warn');

  // `value: null` opens every box empty. A KIT dial handed no value seeds its
  // box with the bottom of its range, and a number sitting in a box the player
  // never touched is a suggestion, so each of the three asks for the blank.
  //
  // The resource rows are drawn by `KIT.choice`, which gives every option the
  // same class and selects none of them. No `value` is passed to it: naming a
  // starting resource would put the board's pick on the offer under the
  // player's name, and one of the five would read as the one to trade.
  const gq = k.dial({
    value: null,
    lo: v.qty_lo, hi: v.qty_hi,
    label: 'quantity (' + v.qty_lo + '-' + v.qty_hi + ')',
    onChange: recount,
  });
  const grPick = k.choice((v.resources || []).map(r => ({ label: r, value: r })),
    x => { gr = x; recount(); });

  const tq = k.dial({
    value: null,
    lo: v.qty_lo, hi: v.qty_hi,
    label: 'quantity (' + v.qty_lo + '-' + v.qty_hi + ')',
    onChange: recount,
  });
  const trPick = k.choice((v.resources || []).map(r => ({ label: r, value: r })),
    x => { tr = x; recount(); });

  const claim = k.dial({
    value: null,
    lo: v.claim_lo, hi: v.claim_hi,
    label: 'the figure you file (' + v.claim_lo + ' to ' + v.claim_hi + ')',
    hint: 'nothing is filed until you enter a number.',
    onChange: recount,
  });

  // After all three exist, not as each is built: clearing a dial runs
  // `recount`, which reads the other two, and one still in its `const`
  // temporal dead zone would throw out of the renderer.
  [gq, tq, claim].forEach(unanswered);

  function recount() {
    err.textContent = '';
    const a = gq.get(), b = tq.get();
    if (a === null || gr === null || b === null || tr === null) {
      echo.textContent = ''; return;
    }
    echo.textContent = 'You give ' + a + ' ' + gr + ' and take ' + b + ' ' + tr + '.';
  }

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'propose one trade, or hold'));
  k.put(a, k.panels(
    k.panel('you give', gq.node, grPick.node),
    k.panel('you take', tq.node, trPick.node),
    k.panel('your claim', claim.node)));
  k.put(a, echo);
  k.put(a, err);

  // THE TWO MOVES OF THE ROUND CARRY THE SAME CLASS. `KIT.submit` draws an
  // accent-bordered, bolded button; spending it on the trade and leaving hold
  // a plain one would make trading the loud move and holding the quiet one,
  // which is a recommendation written in CSS. Whether this round is worth
  // trading is the question the cell asks. See the header.
  const row = k.el('div', 'bd-buttons');
  const file = k.el('button', 'bd-opt', 'file the offer');
  file.onclick = () => {
    if (gq.get() === null || gr === null) {
      err.textContent = 'say how much of what you give.'; return;
    }
    if (tq.get() === null || tr === null) {
      err.textContent = 'say how much of what you take.'; return;
    }
    if (claim.get() === null) {
      err.textContent = 'file a claim.'; return;
    }
    err.textContent = '';
    postOffer(ctx, v.token, {
      gq: gq.get(), gr: gr, tq: tq.get(), tr: tr, c: claim.get(),
    }, err);
  };
  const hold = k.el('button', 'bd-opt', 'hold — no trade this round');
  hold.onclick = () => ctx.send(v.hold_token);
  k.put(row, file, hold);
  k.put(a, row);

  k.put(box, a);
  return box;
};
})();
