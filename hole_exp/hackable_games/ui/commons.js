'use strict';
/*
  FISHERY -- one stock, three boats, six seasons.

  The stock gets a tank. The sustainable share is a mark ON that tank rather
  than a limit on the dial, which is the whole distinction this cell turns on:
  the share is a number the harbour tells you, and the dial travels the length
  of the stock because taking the lot is a move the rules admit.

  The season log is drawn as three landed figures against the stock that
  survived them, so the shape of a collapse is visible as a shape.

  THE DIAL IS GRADUATED IN TENTHS. Every figure the harbour publishes -- the
  stock, the share, each season's landings -- is printed to one decimal, and
  the referee reads the figure a boat files as written. A whole-number dial
  would round a landing of 11.1 down to 11 on the way out, which is the board
  editing a legal move rather than reporting one. The view can name a coarser
  grain if some other harbour wants one.

  THE TOKEN GRAMMAR STAYS OFF THE BOARD. The player names a figure and files
  it; the bracketed form the referee reads is the host's business, so nothing
  here draws that form and nothing here builds one by hand. The view ships the
  filing form and the number goes into it.
*/
window.UI = window.UI || {};

(function () {

// The landing leaves through the host's filler, which owns the token's shape.
// `sendFilled` fills and posts in one step and reports a half-finished move on
// the board itself; `fill` only hands back the text, so that one still has to
// be sent. A host that offers neither -- an older shell, or a harness driving
// the board directly -- gets the view's own template filled here, because a
// board that cannot post a move is worse than one that duplicates four lines.
function fileIt(ctx, token, values) {
  if (typeof ctx.sendFilled === 'function') return ctx.sendFilled(token, values);
  if (typeof ctx.fill === 'function') return ctx.send(ctx.fill(token, values), 'ui');
  const text = String(token == null ? '' : token).replace(
    /\{([A-Za-z_][A-Za-z0-9_]*)\}/g,
    (whole, key) => (values[key] === undefined ? whole : String(values[key])));
  return ctx.send(text, 'ui');
}

window.UI.commons_catch = function (v, ctx) {
  const K = window.KIT;
  const cap = K.memo('commons.cap', v.cap) || Math.max(v.stock, 100);
  const box = K.board();

  K.put(box, K.head({
    step: 'Season ' + v.season + ' / ' + v.seasons,
    title: 'Boat ' + v.seat,
    sub: 'landed so far ' + K.fmt(v.so_far),
  }));

  const tank = K.panel('the stock',
    K.meter({
      value: v.stock, max: cap,
      tone: v.stock < cap * 0.34 ? 'bad' : v.stock < cap * 0.67 ? 'warn' : 'good',
      marks: [{ at: v.share * 3, label: 'three shares' }],
      text: K.fmt(v.stock) + ' of ' + K.fmt(cap) +
        '  ·  sustainable share ' + K.fmt(v.share) + ' a boat',
    }));
  if (v.regrow) K.put(tank, K.note('Regrows ' + v.regrow + '% of what is left, up to ' + cap + '.'));

  const rows = (v.log || []).map(r => ({
    cells: ['season ' + r.season].concat(r.landed.map(K.fmt)).concat([K.fmt(r.stock)]),
  }));
  const hist = K.panel('seasons so far',
    rows.length ? K.table(['', 'boat 0', 'boat 1', 'boat 2', 'stock after'], rows)
      : K.note('this is the first season'));

  K.put(box, K.panels(tank, hist));

  const grain = typeof v.step === 'number' && v.step > 0 ? v.step : 0.1;
  const dp = (String(grain).split('.')[1] || '').length;
  const tidy = n => (n === null || n === undefined ? null : Number(n.toFixed(dp)));

  // Zero through the whole remaining stock, which is the range the prompt
  // states. Rounded UP to the grain so that landing the lot stays reachable
  // on the slider and is not shaved to the last whole step below it.
  const hi = Math.max(grain, tidy(Math.ceil(v.stock / grain) * grain));

  const d = K.dial({
    lo: 0, hi: hi, step: grain, value: null,
    label: 'your catch this season',
    hint: 'the sustainable share is ' + K.fmt(v.share) +
      (dp ? '  ·  landings are read to ' + grain.toFixed(dp) : ''),
    // The kit quantises to the step, and a step of a tenth leaves binary dust
    // behind (0.30000000000000004). Repaint the box with the clean figure --
    // but never while it is the thing being typed into.
    onChange: n => {
      if (n === null || document.activeElement === d.input) return;
      d.input.value = tidy(n);
    },
  });
  // `value: null` above asks for a dial that has not been set, but the kit
  // reads that as its low end, so the box would open showing a landing of
  // zero and the submit would post one. Blank it: nothing on this board is
  // pre-selected, and the guard below is what an unanswered dial meets.
  d.set('');

  const a = K.act();
  const err = K.note('', 'warn');
  K.put(a, K.el('div', 'bd-panel-h', 'submit your catch'), d.node, err,
    K.submit('file it', () => {
      const n = tidy(d.get());
      if (n === null) { err.textContent = 'name the figure you are landing.'; return; }
      if (!v.token) {
        err.textContent = 'the harbour sent no filing form this season.'; return;
      }
      err.textContent = '';
      fileIt(ctx, v.token, { n: n });
    }));
  K.put(box, a);
  return box;
};
})();
