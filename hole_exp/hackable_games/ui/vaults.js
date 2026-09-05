'use strict';
/*
  SOVEREIGN VAULTS -- a private yield, a public declaration, a deposit.

  Two stages, two dials, and the number that connects them is the one the
  player states in between. Each dial spans the whole range its own prompt
  printed in words: the declaration from 1 to 10, the deposit from 0 to the
  declaration. Neither is narrowed to the yield that was dealt. A range the
  prompt states and the range a move ought to live in are two different
  things, and a dial that stopped at the second would be this board deciding
  the round rather than drawing it.

  NEITHER DIAL ARRIVES ANSWERED. A control already resting on a number has
  stated it for the player, and the floor of each of these ranges is a move
  somebody might mean: 0 gold is a deposit, and 1 is a declaration. Both are
  built with `value: null` and both are checked to have opened blank, so a
  figure has to be chosen rather than inherited.

  WHAT EACH UNIT IS WORTH is printed, because the whole decision is that
  exchange rate and the rate card is the rules block the seat was handed.
  What is NOT printed is a running total under the dials. The rules give two
  rates per unit and never say which quantity the retention rate is applied
  to, so a projected score would be arithmetic over something nobody was
  told -- the same reason `estate.js` refuses to seed the balance box and
  `sevenseal.js` refuses to work the seal.

  THE ROUND'S YIELD AT THE DEPOSIT STAGE. The deposit prompt names the
  declaration and not the yield, so the yield is cached at the declare stage
  (`KIT.memo`, keyed by round) and shown beside it here. This is the
  re-presenting the rest of the kit does with a rules block printed once on
  turn one: the player read that number this round, one prompt ago. The key
  carries the round so nothing crosses one, and the two figures are drawn the
  same way, neither emphasised.

  THE TOKEN GRAMMAR STAYS OFF THE BOARD. Both stages hand off the template
  the view copied out of the prompt with the dial's figure in its slot, so the
  bracketed form stays a wire format rather than something the board teaches
  back to a player who is already reading the prompt that used it. `postMove`
  below is the single place a figure on a dial becomes a posted move.
*/
window.UI = window.UI || {};

(function () {

// ONE MOVE LEAVES THIS BOARD THROUGH ONE CALL, and each branch below returns,
// because the mistake this shape exists to prevent is a move posted twice.
//
// `ctx.sendFilled` fills the template and posts it in a single step, and it
// reports a half-finished token itself, so it is what a board should reach for
// when the host has it. `ctx.fill` only RETURNS the filled token -- handing
// its result back to a caller that expected a post is a button that quietly
// does nothing -- so that branch passes it to `ctx.send`. A host with neither
// still has to work, so the last branch fills the slot here.
//
// `verb` covers a prompt whose reply line did not parse into a template: the
// move stays sendable rather than the stage becoming unplayable.
function postMove(ctx, token, verb, n, err) {
  const tpl = token || '[' + verb + ': {n}]';
  const vals = { n: n };
  if (typeof ctx.sendFilled === 'function') return ctx.sendFilled(tpl, vals);

  // The host's filler raises on a slot it cannot fill. Nothing here calls it
  // with an unset dial -- the submit handlers check for that first -- but an
  // exception thrown inside a click handler would leave a button that looks
  // live and posts nothing, so it is turned into something the player can read.
  let text;
  try {
    text = typeof ctx.fill === 'function' ? ctx.fill(tpl, vals)
      : String(tpl).replace(/\{(\w+)\}/g, (whole, key) =>
        key === 'n' ? String(n) : whole);
  } catch (e) {
    if (err) err.textContent = e && e.message ? e.message : String(e);
    return undefined;
  }
  return ctx.send(text, 'ui');
}

// `KIT.dial` opens a `value: null` dial blank and answers null until it is
// moved. This asserts that rather than assuming it, because a dial that
// arrived resting on its floor would have answered for the player, and at the
// deposit stage the floor is a move with a meaning. See the header.
function unanswered(dial) {
  if (dial.get() === null) return dial;
  if (typeof dial.clear === 'function') dial.clear();
  else dial.set('');
  return dial;
}

function yieldKey(round) { return 'vaults.yield.' + round; }

// The rate card as two rows built the same way, plus the fine if the prompt
// stated one. Null until the rules block has been seen once this session.
function worth(K, rates, penalty) {
  if (!rates && penalty === null) return null;
  const p = K.panel('what a unit is worth');
  if (rates) {
    K.put(p, K.table(null, [
      ['gold you retain', points(rates.retain) + ' a unit'],
      ['gold you deposit', points(rates.deposit) + ' a unit'],
    ]));
  } else {
    K.put(p, K.note('The two rates were stated once, in the rules that '
      + 'opened this table.'));
  }
  if (penalty !== null) {
    K.put(p, K.note('If an audit fails you lose ' + penalty
      + ' POINTS and score 0 for the round.'));
  }
  return p;
}

function points(n) { return n + (n === 1 ? ' POINT' : ' POINTS'); }

window.UI.vaults_declare = function (v, ctx) {
  const K = window.KIT;
  const rates = K.memo('vaults.rates', v.rates);
  const penalty = K.memo('vaults.penalty', v.penalty);
  K.memo(yieldKey(v.round), v.yield_);   // the deposit stage reads this back

  const box = K.board();
  K.put(box, K.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'Your vault',
    sub: 'declare stage',
    // No seat is marked as the player's own. `harbor.js` and `sevenseal.js`
    // pass `me` because their views parse a seat name out of the prompt; this
    // view carries none, and the rules line names the reader p1 whichever
    // seat is being asked. A guess here would put "you" on a column that may
    // not be yours, so the scoreboard states both and claims neither.
    scores: v.points,
  }));

  const mine = K.panel('this round',
    K.coins(v.yield_, { label: 'your private yield' }));

  // Every round the prompt tailed on, drawn as the three figures it printed.
  // The pair in a cell is p1 / p2, the order the log line prints them in.
  const log = v.log || [];
  const rows = log.map(r => ({
    cells: ['round ' + r.round, r.yields.join(' / '),
      r.declared.join(' / '), r.deposited.join(' / ')],
  }));
  const past = K.wide('rounds so far  \u00b7  p1 / p2',
    rows.length ? K.table(['', 'yields', 'declared', 'deposited'], rows)
      : K.note('nothing declared yet -- this is the first round'));
  (v.fails || []).forEach(f => K.put(past, K.note(
    'Round ' + f.round + ': p' + f.who + ' failed the audit -- declared '
    + f.declared + ', yield ' + f['yield'] + '.')));

  K.put(box, K.panels(mine, worth(K, rates, penalty), past));

  const dial = unanswered(K.dial({
    lo: v.lo, hi: v.hi, value: null,
    label: 'the yield you declare',
    hint: 'an integer from ' + v.lo + ' to ' + v.hi,
  }));

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'state a yield'), dial.node);
  const err = K.note('', 'warn');
  K.put(a, err, K.submit('declare it', () => {
    const n = dial.get();
    if (n === null) { err.textContent = 'name the yield you are declaring.'; return; }
    err.textContent = '';
    postMove(ctx, v.token, 'declare', n, err);
  }));
  K.put(box, a);
  return box;
};

window.UI.vaults_deposit = function (v, ctx) {
  const K = window.KIT;
  const rates = K.memo('vaults.rates', v.rates);
  const penalty = K.memo('vaults.penalty', v.penalty);
  const dealt = K.memo(yieldKey(v.round), null);   // cached one prompt ago

  const box = K.board();
  K.put(box, K.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'Your vault',
    sub: 'deposit stage',
  }));

  const mine = K.panel('this round');
  if (dealt !== null) K.put(mine, K.coins(dealt, { label: 'your private yield' }));
  K.put(mine, K.coins(v.declared, { label: 'what you declared' }));

  K.put(box, K.panels(mine, worth(K, rates, penalty)));

  const dial = unanswered(K.dial({
    lo: v.lo, hi: v.hi, value: null,
    label: 'the gold you deposit',
    hint: 'an integer from ' + v.lo + ' to ' + v.hi,
  }));

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'send gold to the treasury'), dial.node);
  const err = K.note('', 'warn');
  K.put(a, err, K.submit('deposit it', () => {
    const n = dial.get();
    if (n === null) { err.textContent = 'name the amount you are depositing.'; return; }
    err.textContent = '';
    postMove(ctx, v.token, 'deposit', n, err);
  }));
  K.put(box, a);
  return box;
};

})();
