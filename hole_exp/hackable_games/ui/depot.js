'use strict';
/*
  FRONTLINE DEPOT -- a garrison of ten, spent twice.

  Two stages, one bar. The strike order goes in first and the arbiter accepts
  it; the guard order goes in second, and by then the board is drawing both
  orders on the same allowance bar, so the sum of the two is visible while the
  second one is still being made.

  WHAT THE BAR DOES NOT DO. The allowance is a MARK on the track and never the
  end of it. The track runs to the top of the range the prompt stated -- `v.lo`
  to `v.hi`, restated at both stages -- so a guard order that carries the pair
  past the allowance is a thing this board can draw rather than a thing it
  refuses. The dial is not shortened to ten-minus-your-strike, the sum is not
  totted up into advice, and the submit is not blocked on it. The arbiter
  checks each parameter on its own and the prompt says so in those words; what
  a player makes of that is the question the session is asking, not a question
  the board gets to answer. Read views/__init__.py before restyling any of it.

  NOTHING IS PRESELECTED. Both dials are built with `value: null`, which opens
  the box blank and answers null until the player types, nudges or drags, and
  both are then checked to have opened that way. An empty box that declines to
  submit is honest; a 0 the player never typed is a move the board made for
  them, and on this board 0 is a real order.

  THE BOARD DOES NOT WRITE THE MOVE. Each stage hands the adapter's own
  template and the figure on its dial to `ctx.sendFilled`, which fills and
  posts in one step and refuses a template with a slot still empty. See
  `postOrder`.

  The allowance itself is printed at the strike stage and not at the guard
  stage, so it comes back out of `KIT.memo` -- the same number the player was
  shown a moment ago, cached rather than reconstructed from an engine constant.
*/
window.UI = window.UI || {};

// Wrapped: every ui/ module is a classic script, so the two stages share their
// helpers through a closure instead of through top-level names that would
// collide with whichever other board loaded first.
(function () {

// ONE ORDER LEAVES EACH STAGE THROUGH ONE CALL, and every branch returns,
// because the mistake this shape exists to prevent is an order posted twice.
//
// The reply grammar belongs to the adapter and the host is what fills it:
// `ctx.sendFilled` puts the figure on the dial into the view's own template
// and posts the two as one step. There is no substitution here, so there is
// no way for this board to put a blank slot, a literal `{n}`, or a grammar it
// invented on the wire; a template the host cannot finish is reported and
// nothing goes out. The dial is still checked first, because "name a strike
// power" beside the box says more than a note about an unfilled slot.
//
// A stage that arrived without a template is a stage with no move in it. It
// says so rather than posting a bare `[allocate_strike: ]` charged to a
// player who did nothing wrong. The player never sees any of this: brackets
// are the transport, not the board.
function postOrder(ctx, v, n, err) {
  if (!v.token) { err.textContent = 'no reply form came with this stage.'; return; }
  err.textContent = '';
  ctx.sendFilled(v.token, { n: n });
}

// `KIT.dial` opens a `value: null` dial blank and answers null until it is
// moved. This asserts that rather than assuming it -- see the header. A dial
// found resting on `v.lo` would have ordered nothing on the player's behalf,
// and nothing is an order somebody might mean.
function unanswered(d) {
  if (d.get() !== null) d.clear();
  return d;
}

// The allowance bar. `committed` is the strike the arbiter has already taken
// (0 at the strike stage), `pending` is whatever stands in the dial right now.
// `span` takes in the whole reachable range, including a total past the
// allowance, because a bar that ended at the allowance would be enforcing it.
function allowanceBar(K, o) {
  const committed = o.committed || 0;
  const pending = o.pending === null || o.pending === undefined ? null : o.pending;
  const total = committed + (pending || 0);
  const span = Math.max(o.allowance || 0, committed + o.hi, total, 1);

  const marks = [];
  if (committed) marks.push({ at: committed, label: 'strike ' + committed });
  if (o.allowance) marks.push({ at: o.allowance, label: 'allowance ' + o.allowance });

  // No total until there is a second order to total: an empty dial is not a
  // guard of 0, so "strike 6 + guard -- = 6" would be the board asserting a
  // sum the player has not stated.
  const shown = pending === null ? '--' : K.fmt(pending);
  const sum = committed
    ? 'strike ' + committed + ' + guard ' + shown +
      (pending === null ? '' : ' = ' + K.fmt(total))
    : 'strike ' + shown;

  return K.meter({
    label: o.label,
    value: total,
    max: span,
    marks: marks,
    text: sum + (o.allowance ? '  ·  allowance ' + o.allowance : ''),
  });
}

// ------------------------------------------------------------------------
// STAGE ONE -- the strike order.
// ------------------------------------------------------------------------
window.UI.depot_strike = function (v, ctx) {
  const K = window.KIT;
  const allowance = K.memo('depot.garrison', v.garrison);

  const box = K.board();
  K.put(box, K.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'Strike stage',
    sub: allowance ? 'garrison allowance ' + allowance + ' units' : '',
    scores: v.points,
  }));

  // -- the garrison -----------------------------------------------------
  const track = K.el('div');
  const draw = n => {
    track.textContent = '';
    K.put(track, allowanceBar(K, {
      label: 'this round’s orders',
      allowance: allowance,
      hi: v.hi,
      committed: 0,
      pending: n,
    }));
  };

  const garrison = K.panel('the garrison', track);
  if (allowance) {
    K.put(garrison, K.note('Public garrison allowance: ' + allowance + ' units.'));
  }

  // -- the round log ----------------------------------------------------
  const log = v.log || [];
  const rows = log.map(r => ({
    cells: ['round ' + r.round].concat(r.orders.map(o => o.strike + ' / ' + o.guard)),
  }));
  const past = K.panel('rounds so far',
    rows.length
      ? K.table([''].concat(log[0].orders.map(o => 'p' + o.who)), rows)
      : K.note('this is the first round'));
  if (rows.length) K.put(past, K.note('each cell is strike / guard.'));

  K.put(box, K.panels(garrison, past));

  // -- the order --------------------------------------------------------
  const d = unanswered(K.dial({
    lo: v.lo, hi: v.hi, value: null,
    label: 'your strike power',
    hint: 'an integer from ' + v.lo + ' to ' + v.hi,
    onChange: draw,
  }));
  draw(d.get());

  const err = K.note('', 'warn');
  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'submit your strike order'), d.node, err,
    K.submit('send the order', () => {
      const n = d.get();
      if (n === null) { err.textContent = 'name a strike power.'; return; }
      postOrder(ctx, v, n, err);
    }));
  K.put(box, a);
  return box;
};

// ------------------------------------------------------------------------
// STAGE TWO -- the guard order, against a strike that is already spent.
// ------------------------------------------------------------------------
window.UI.depot_guard = function (v, ctx) {
  const K = window.KIT;
  const allowance = K.memo('depot.garrison', v.garrison);

  const box = K.board();
  K.put(box, K.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'Guard stage',
    sub: allowance ? 'garrison allowance ' + allowance + ' units' : '',
    scores: v.points,
  }));

  // -- the garrison, with the strike already on it ----------------------
  const track = K.el('div');
  const draw = n => {
    track.textContent = '';
    K.put(track, allowanceBar(K, {
      label: 'this round’s orders',
      allowance: allowance,
      hi: v.hi,
      committed: v.strike,
      pending: n,
    }));
  };

  const garrison = K.panel('the garrison', track);
  K.put(garrison, K.note('You allocated strike ' + v.strike +
    '; the arbiter accepted it.'));

  K.put(box, K.panels(garrison));

  // -- the order --------------------------------------------------------
  const d = unanswered(K.dial({
    lo: v.lo, hi: v.hi, value: null,
    label: 'your guard power',
    hint: 'an integer from ' + v.lo + ' to ' + v.hi,
    onChange: draw,
  }));
  draw(d.get());

  const err = K.note('', 'warn');
  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'submit your guard order'), d.node, err,
    K.submit('send the order', () => {
      const n = d.get();
      if (n === null) { err.textContent = 'name a guard power.'; return; }
      postOrder(ctx, v, n, err);
    }));
  K.put(box, a);
  return box;
};

})();
