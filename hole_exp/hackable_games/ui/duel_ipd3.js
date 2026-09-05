'use strict';
/*
  DUEL and THREE-PLAYER IPD -- the same dilemma at two table sizes.

  Three boards live here because they share one picture: a 2x2 payoff table, a
  history that is only worth reading as a grid, and a choice between two moves
  that must arrive on screen weighing exactly the same. `duel_move` serves both
  the two-player prisoner's dilemma and the stag hunt; `ipd3_line` and
  `ipd3_table` are the two decisions the three-player cell asks for.

  THE OPTIONS ARE DRAWN IN PROMPT ORDER AND NOTHING IS PRE-SELECTED. The moves
  come out of `v.options` as the adapter read them off the prompt, through
  `KIT.actions` and `KIT.choice`, which give every option the same class. A
  board that opened with `cooperate` already lit would be answering the
  question the cell exists to ask.

  THE BRACKET GRAMMAR STAYS OFF THE SCREEN. The adapter hands down a token
  template; the host fills it. The three-player table -- whose reply is two
  tokens at once -- is two ordinary choices and a submit rather than a string
  a player assembles by hand. Structured controls are the only participant
  move path; a missing renderer is unavailable, not a typed box.

  THE MESSAGE IS QUOTED, NOT SUMMARISED, and the board says nothing about
  whether it is true. What a player makes of an opening promise is most of what
  these cells measure, so the line goes up verbatim and the private line's own
  reply box is free text with no suggestions in it. That reply is posted with
  `sendText` so an empty box is still a legal move and whatever was typed is
  left alone.
*/
window.UI = window.UI || {};

(function () {
const K = () => window.KIT;

// Structured replies leave through the host. `sendFilled` fills and posts in
// one step and reports a half-finished token instead of sending it. `fill`
// only returns the text, so that branch still has to post. There is no local
// filler: a missing value used to become an empty slot here, which the
// referee would score as an unparsed move.
function postFilled(ctx, token, values, warn) {
  if (typeof ctx.sendFilled === 'function') return ctx.sendFilled(token, values);
  let text;
  try {
    if (typeof ctx.fill !== 'function') {
      throw new Error('nothing chosen');
    }
    text = ctx.fill(token, values);
  } catch (err) {
    const msg = err && err.message ? err.message : String(err);
    if (typeof warn === 'function') warn(msg);
    return;
  }
  return ctx.send(text);
}

function cap(s) { return String(s).charAt(0).toUpperCase() + String(s).slice(1); }

function initial(s) { return String(s).charAt(0).toUpperCase(); }

// C cooperate · D defect, in the prompt's own words, because the history the
// engine tails onto the prompt is written in initials.
function legend(k, options) {
  return k.note(options.map(o => initial(o) + ' ' + o).join('  ·  '));
}

// Rows are your move, columns are theirs. The six numbers arrive in the order
// the rules sentence states them: both-cooperate pair, both-defect pair, then
// what a defection against a cooperator pays each side.
function payoffTable(k, options, pay) {
  return k.matrix({
    rows: options,
    cols: options,
    cell: (i, j) => {
      if (i === 0 && j === 0) return [pay[0], pay[1]];
      if (i === 1 && j === 1) return [pay[2], pay[3]];
      if (i === 1 && j === 0) return [pay[4], pay[5]];
      return [pay[5], pay[4]];
    },
  });
}

// ------------------------------------------------------------ duel_move --
window.UI.duel_move = function (v, ctx) {
  const k = K();
  const pay = k.memo('duel.pay.' + v.game, v.payoffs);
  const corners = k.memo('duel.corners.' + v.game, v.corners);
  const box = k.board();

  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: v.game === 'staghunt' ? 'the hunt' : "the prisoner's dilemma",
    sub: 'one opponent, ' + v.rounds + ' rounds',
    scores: v.totals, me: 'you',
  }));

  const panels = [];
  if (pay) {
    const p = k.panel('the table  (you / them)', payoffTable(k, v.options, pay));
    if (corners) k.put(p, k.note(corners.join('  ·  ')));
    panels.push(p);
  }

  if (v.message) {
    const m = k.panel('the message', k.quote(v.message.from, v.message.text));
    k.put(m, k.note('Sent before this round. The referee does not check it.'));
    panels.push(m);
  }

  const log = v.log || [];
  const hist = k.panel('rounds so far');
  if (log.length) {
    k.put(hist, k.track(log.map(r => ({
      label: r.round,
      sub: 'you ' + initial(r.me),
      tag: r.who + ' ' + initial(r.them),
    }))), legend(k, v.options));
  } else {
    k.put(hist, k.note('this is the first round'));
  }
  panels.push(hist);

  k.put(box, k.panels.apply(null, panels));

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'your move this round'));
  k.put(a, k.actions(v.options.map(o => ({
    label: o,
    token: o,
  })), opt => postFilled(ctx, v.token, { opt: opt })));
  k.put(box, a);
  return box;
};

// ------------------------------------------------------------ ipd3_line --
window.UI.ipd3_line = function (v, ctx) {
  const k = K();
  const box = k.board();

  k.put(box, k.head({
    title: 'the private line',
    sub: 'Dove is not on it',
  }));

  k.put(box, k.panels(k.panel('what came down the line',
    k.quote(v.from, v.text))));

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'your reply on the line'));
  // Free text, no suggested wording, no length rule the prompt did not state.
  // An empty send is a move -- saying nothing on a channel nobody checks is
  // one of the answers -- so it goes through sendText, which treats the empty
  // slot as a value rather than as unfinished. The typed string is not
  // trimmed or otherwise rewritten.
  const t = k.textbox({
    placeholder: '',
    send: 'send',
    onSend: rawText => ctx.sendText(v.token, 'text', rawText),
  });
  k.put(a, t.node);
  k.put(a, k.note('The referee relays this to Rook without checking what it ' +
    'says. Sending nothing is allowed.'));
  k.put(box, a);
  setTimeout(() => t.input.focus(), 0);
  return box;
};

// ----------------------------------------------------------- ipd3_table --
window.UI.ipd3_table = function (v, ctx) {
  const k = K();
  const pay = k.memo('ipd3.pay', v.payoffs);
  const box = k.board();

  k.put(box, k.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'two pairings',
    sub: 'one dilemma against each of the other two',
    scores: v.totals, me: 'you',
  }));

  const panels = [];
  if (pay) {
    const p = k.panel('the table, per pairing  (you / them)',
      payoffTable(k, v.options, pay));
    k.put(p, k.note('Your round score is the sum over your two pairings.'));
    panels.push(p);
  }

  const log = v.log || [];
  const hist = k.panel('rounds so far');
  if (log.length) {
    k.put(hist, k.table(['', 'you / Rook', 'you / Dove', 'Rook / Dove'],
      log.map(r => ({
        cells: [
          'round ' + r.round,
          r.you[0] + ' / ' + r.rook[0],
          r.you[1] + ' / ' + r.dove[0],
          r.rook[1] + ' / ' + r.dove[1],
        ],
      }))), legend(k, v.options));
  } else {
    k.put(hist, k.note('this is the first round'));
  }
  panels.push(hist);

  k.put(box, k.panels.apply(null, panels));

  // Two independent choices, each a full row of equal buttons, each starting
  // empty. The pair is assembled into the reply at submit time; neither half
  // can be sent on its own by accident, and neither is filled in for you.
  const picked = {};
  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'choose against each of them'));
  const seats = (v.opponents || []).map(name => {
    picked[name] = null;
    const c = k.choice(v.options.map(o => ({ label: o, value: o })),
      x => { picked[name] = x; });
    return k.panel('against ' + cap(name), c.node);
  });
  k.put(a, k.panels.apply(null, seats));

  const err = k.note('', 'warn');
  k.put(a, err);
  k.put(a, k.submit('send both', () => {
    const missing = (v.opponents || []).filter(n => picked[n] === null);
    if (missing.length) {
      err.textContent = 'choose against ' +
        missing.map(cap).join(' and ') + ' as well.';
      return;
    }
    err.textContent = '';
    postFilled(ctx, v.token, picked, msg => { err.textContent = msg; });
  }));
  k.put(box, a);
  return box;
};
})();
