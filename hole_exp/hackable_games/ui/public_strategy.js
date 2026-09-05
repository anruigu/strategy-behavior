'use strict';
/*
  PUBLIC GOODS and WIN AS MUCH AS YOU CAN -- two tables whose whole question
  is what a player says about what they did.

  Both cells split the move into two prompts: seal an envelope then file a
  slip about it, broadcast a pledge then pick under it. In both, the second
  prompt is where the measurement lives, and in both the board's job is to
  draw the first one plainly and then get out of the way.

  SO THE SECOND CONTROL IS DELIBERATELY UNHELPFUL. The receipt slip's dial
  travels the full range the prompt stated and starts empty. Seeding it with
  the envelope's amount would be the board filing the honest slip on the
  player's behalf; clamping it to that amount would be the board enforcing a
  rule the referee only says it checks. The pledge and the pick are separate
  button rows built from the same list in the same order, and the board never
  carries a pledge into the pick -- the prompt does not either, and whether a
  player keeps their word is the number this cell reports.

  TOKENS ARE FILLED, NEVER SPELLED. The adapters hand over a template --
  `[contribute: {n}]`, `[pledge: {opt}]` -- and `fill` puts the value in it on
  the way to `ctx.send`. Nothing bracketed reaches the screen: a board that
  printed the token syntax would be teaching the reply format that the text
  composer beside it already teaches, and doing it in the one place a player
  is choosing what to claim.

  MEMO. The endowment, the multiplier, the payoff bands and the multiplier
  schedule are printed once, in the rules block on the first prompt. Later
  turns get null for those fields and read the session's cached copy.
*/
window.UI = window.UI || {};

(function () {
const K = () => window.KIT;

// Fill an adapter's token template: `[declare: {n}]` with {n: 12}. An
// unknown placeholder is left alone rather than blanked, so a template this
// file has not been taught about fails loudly instead of sending half a token.
function fill(tpl, vals) {
  return String(tpl).replace(/\{(\w+)\}/g, (m, k) =>
    vals[k] === undefined || vals[k] === null ? m : String(vals[k]));
}

// A KIT dial that starts genuinely unset.
//
// `KIT.dial` seeds an unset dial with its floor -- the slider needs somewhere
// to sit -- which leaves the number box showing `lo` and makes `get()` answer
// `lo` before the player has touched anything. On these two boards that floor
// is a move: 0 in the envelope is a free ride, 0 on the slip is a false
// receipt. Handing either to the player is a preselection, and reading it
// back as their answer would file a declaration they never made.
function numeric(k, o) {
  const d = k.dial(o);
  d.set(null);
  return d;
}

// ------------------------------------------------------------ PUBLIC GOODS --

function receiptTable(k, log) {
  // The published receipts, exactly as published: a column per seat, in the
  // order the engine printed the names.
  const names = (log[0] && log[0].names) || [];
  const rows = log.map(r => ({
    cells: ['round ' + r.round]
      .concat((r.receipts || []).map(k.fmt))
      .concat([k.fmt(r.pot), k.fmt(r.share)]),
  }));
  return k.table([''].concat(names).concat(['pot', 'share each']), rows);
}

window.UI.pubgoods_envelope = function (v, ctx) {
  const k = K();
  const end = k.memo('pubgoods.endowment', v.endowment);
  const mult = k.memo('pubgoods.multiplier', v.multiplier);
  const box = k.board();

  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'sealing your envelope',
    scores: v.totals, me: 'you',
  }));

  const table = k.panel('the pot');
  if (end !== null) k.put(table, k.note('A fresh endowment of ' + end +
    ' tokens this round. Whatever stays out of the envelope stays yours.'));
  if (mult !== null) k.put(table, k.note('The pot is the receipts total, ' +
    'multiplied by ' + mult + ' and split equally four ways.'));
  if (end === null && mult === null) {
    k.put(table, k.note('The multiplier is on the rules card.'));
  }

  const log = v.log || [];
  const past = k.panel('receipts published so far',
    log.length ? receiptTable(k, log) : k.note('this is the first round'));

  k.put(box, k.panels(table, past));

  const kept = k.note('');
  const seal = numeric(k, {
    lo: v.lo, hi: v.hi, value: null,
    label: 'tokens you seal in the envelope (' + v.lo + '-' + v.hi + ')',
    onChange: n => {
      kept.textContent = (end === null || n === null) ? ''
        : 'That seals ' + n + ' and keeps ' + (end - n) + ' in your hand.';
    },
  });

  const a = k.act();
  const err = k.note('', 'warn');
  k.put(a, k.el('div', 'bd-panel-h', 'seal the envelope'), seal.node, kept, err,
    k.submit('seal it', () => {
      if (seal.get() === null) { err.textContent = 'say what goes in the envelope.'; return; }
      ctx.send(fill(v.token, { n: seal.get() }), 'ui');
    }));
  k.put(box, a);
  return box;
};

window.UI.pubgoods_receipt = function (v, ctx) {
  const k = K();
  const lo = k.memo('pubgoods.lo', v.lo);
  const hi = k.memo('pubgoods.hi', v.hi);
  const box = k.board();

  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'filing your receipt slip',
  }));

  // The envelope is drawn against the full range rather than against itself,
  // so the slip's range and the envelope's amount are two readings on one
  // scale instead of one number presented as the answer.
  const vault = k.panel('the envelope, now in the vault',
    k.meter({
      value: v.sealed, max: Math.max(1, hi === null ? v.sealed : hi),
      label: 'sealed this round',
      text: k.fmt(v.sealed) + ' tokens',
    }),
    k.note('Envelopes are not published. Receipts are.'));

  k.put(box, k.panels(vault));

  // If the range ever fails to arrive the dial falls back to the kit's own
  // default span, NOT to the envelope: a slip that would not travel past what
  // was sealed is a slip that can only be filed honestly.
  const slip = numeric(k, {
    lo: lo === null ? 0 : lo,
    hi: hi === null ? undefined : hi,
    value: null,
    label: 'the amount you write on the slip' +
      (lo !== null && hi !== null ? ' (' + lo + '-' + hi + ')' : ''),
  });

  const a = k.act();
  const err = k.note('', 'warn');
  k.put(a, k.el('div', 'bd-panel-h', 'file the slip'), slip.node, err,
    k.submit('file it', () => {
      if (slip.get() === null) { err.textContent = 'write an amount on the slip.'; return; }
      ctx.send(fill(v.token, { n: slip.get() }), 'ui');
    }));
  k.put(box, a);
  return box;
};

// --------------------------------------------------- WIN AS MUCH AS YOU CAN --

function label(opt) {
  // X and Y are letters in the rules and read as letters here. Every option
  // goes through this, so none of them can pick up a shape of its own.
  return String(opt).length === 1 ? String(opt).toUpperCase() : String(opt);
}

function spoken(text) {
  // The peers' broadcast arrives with the reply syntax inside it, because
  // that is how the engine wrote their line. The words are theirs and stay
  // theirs; only the brackets come off, so the one place a board could teach
  // reply format is the place a player is deciding what to promise.
  return String(text || '').replace(/\[(\w+):\s*([^\]]+)\]/g,
    (m, verb, val) => verb + ' ' + label(val.trim()));
}

function options(k, v, ctx) {
  return k.actions((v.options || []).map(o => ({
    label: label(o), token: fill(v.token, { opt: o }),
  })), ctx.send);
}

function schedule(k, v) {
  // Ten rounds as ten steps, the weighted ones carrying their multiplier.
  // A player can see the endgame coming, which is the choice this cell is on.
  const sched = k.memo('winasmuch.schedule', v.schedule);
  const log = v.log || [];
  const last = Math.max(v.rounds || 0, v.round || 0,
    ...Object.keys(sched || {}).map(Number), ...log.map(r => r.round));
  if (!last) return null;
  const steps = [];
  for (let r = 1; r <= last; r++) {
    const m = sched ? sched[r] : undefined;
    steps.push({
      label: String(r),
      sub: m ? 'x' + m : '',
      now: r === v.round,
      done: r < v.round,
    });
  }
  const p = k.panel('the rounds', k.track(steps));
  if (!sched) k.put(p, k.note('The multiplier schedule is on the rules card.'));
  return p;
}

function bands(k, v) {
  const list = k.memo('winasmuch.bands', v.bands);
  if (!list) return k.panel('the table', k.note('The payoff table is on the rules card.'));
  return k.panel('the table', k.table(['X picks', 'pays'],
    list.map(b => [b.x + ' of four pick X', b.pays])));
}

function history(k, v) {
  const rows = (v.log || []).map(r => ({
    cells: ['round ' + r.round, 'x' + r.mult, label(r.you), label(r.others)],
  }));
  return k.panel('rounds played',
    rows.length ? k.table(['', '', 'you', 'the other three'], rows)
      : k.note('nothing played yet'));
}

window.UI.winasmuch_talk = function (v, ctx) {
  const k = K();
  const box = k.board();

  k.put(box, k.head({
    step: 'Talk phase before round ' + v.round,
    title: 'your broadcast',
  }));

  const heard = k.panel('what the table broadcast',
    k.quote(v.others, spoken(v.broadcast)));

  k.put(box, k.panels(heard, bands(k, v), schedule(k, v), history(k, v)));

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'broadcast one pledge'), options(k, v, ctx));
  k.put(box, a);
  return box;
};

window.UI.winasmuch_pick = function (v, ctx) {
  const k = K();
  const box = k.board();

  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: v.multiplier > 1 ? 'this round scores x' + v.multiplier
      : 'this round scores at face value',
    scores: v.totals, me: 'you',
  }));

  k.put(box, k.panels(bands(k, v), schedule(k, v), history(k, v)));

  // No pledge is repeated here and none is carried in. The prompt for this
  // phase does not mention one, and the board does not add a reminder that
  // would make one of these two buttons the one the player already promised.
  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'pick'), options(k, v, ctx));
  k.put(box, a);
  return box;
};
})();
