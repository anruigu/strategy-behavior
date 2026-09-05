'use strict';
/*
  SEVEN-SEAL CERTIFICATES -- a private draw, a public report, an audit seal.

  Three things are on screen and each of them is on screen because the prompt
  put it there: the digit you drew and nobody else can see, the coefficients
  the seal is computed from, and the rounds already certified drawn as each
  seat's draw against the report it filed. The last of those is the point of
  the board -- a pattern in what the other two do is a pattern in a column,
  and reading it off six lines of prose is arithmetic the player should not
  have to do twice.

  WHAT THE BOARD WILL NOT DO IS WORK THE SEAL. The coefficients sit next to
  the dial and the dial reports a number; nothing here multiplies the one by
  the other. The seal is the single thing this cell asks a player to hold in
  their head, and a readout that solved it against a tentative report would be
  the board answering the question instead of asking it.

  THE DIAL SPANS THE REPORT'S RANGE, 0 through 9, which is the range the
  prompt states in words. The draw's range is 0 through 2 and it is a different
  number in the rules; both are printed, neither is used to narrow the other.
  A dial that stopped at 2 would have quietly ruled out every report this game
  is actually about.

  THE TOKEN GRAMMAR STAYS OFF THE BOARD. The player names a figure and seals
  the certificate; the bracketed form the referee reads is the host's business
  and is never drawn, so nothing on screen teaches a syntax back to the person
  already looking at the prompt that used it.
*/
window.UI = window.UI || {};

(function () {
const LETTERS = ['A', 'B', 'C'];

// The certificate leaves through whichever of the host's doors is open, and
// through exactly one of them.
//
// `sendFilled` fills the template and posts it in a single step, so it is the
// one to prefer -- the host holds the wire format and the staleness guard in
// the same place. `fill` is NOT a send: it only hands back the finished token,
// and reading it as a send is how a sealed certificate ends up going nowhere,
// which is what this board did before. A host with neither still has `send`,
// so the last resort fills the view's own template here.
function fileIt(ctx, token, values, warn) {
  if (typeof ctx.sendFilled === 'function') return ctx.sendFilled(token, values);
  let text;
  try {
    text = typeof ctx.fill === 'function'
      ? ctx.fill(token, values) : localFill(token, values);
  } catch (err) {
    // A template with a slot still empty is a half-finished move. Say so on
    // the board and post nothing -- the same answer the host gives it.
    return warn(err && err.message ? err.message : String(err));
  }
  return ctx.send(text, 'ui');
}

// The fallback filler, and deliberately as strict as the host's about a slot
// with nothing in it. `0` is a figure somebody can mean to report, so only
// absence counts as absence.
function localFill(token, values) {
  const missing = [];
  const text = String(token == null ? '' : token)
    .replace(/\{([A-Za-z_][A-Za-z0-9_]*)\}/g, (whole, key) => {
      const val = values[key];
      if (val === undefined || val === null || val === '') {
        if (missing.indexOf(key) < 0) missing.push(key);
        return '';
      }
      return String(val);
    });
  if (missing.length) throw new Error('nothing chosen for ' + missing.join(', '));
  return text;
}

function sealFormula(seal) {
  // "(3A + 5B + 6C) mod 7", rebuilt from the coefficients the prompt gave.
  const terms = seal.coef.map((c, i) => c + (LETTERS[i] || '?')).join(' + ');
  return '(' + terms + ') mod ' + seal.mod;
}

function seatLabel(seats, i, mine) {
  const name = seats && seats[i] !== undefined ? seats[i] : LETTERS[i] || 'seat ' + i;
  return name + (i === mine ? ' (you)' : '');
}

window.UI.sevenseal_report = function (v, ctx) {
  const K = window.KIT;
  const seal = K.memo('sevenseal.seal', v.seal);
  const seats = K.memo('sevenseal.seats', v.seats);
  const drawRange = K.memo('sevenseal.draw',
    v.draw_lo === null || v.draw_lo === undefined
      ? null : { lo: v.draw_lo, hi: v.draw_hi });
  const lo = v.lo === undefined || v.lo === null ? 0 : v.lo;
  const hi = v.hi === undefined || v.hi === null ? 9 : v.hi;
  const mine = seats ? seats.indexOf(v.me) : -1;

  const box = K.board();
  K.put(box, K.head({
    step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'certifier ' + v.me,
    sub: 'filing your report',
    scores: v.points,
    me: v.me,
  }));

  // ------------------------------------------------------ the private draw --
  const drew = K.panel('your draw',
    K.cardRow(K.card({ label: String(v.draw), corner: v.me, sub: 'private' })),
    K.note('Yours alone this round. The other certifiers see the report you '
      + 'file, not the digit you drew.'));
  if (drawRange) {
    K.put(drew, K.note('A draw is a digit from ' + drawRange.lo + ' through '
      + drawRange.hi + '.'));
  }

  // ------------------------------------------------------------- the seal --
  const audit = K.panel('the audit seal');
  if (seal) {
    K.put(audit, K.note(sealFormula(seal)));
    K.put(audit, K.table(['', 'coefficient'], seal.coef.map((c, i) => ({
      cls: i === mine ? 'mine' : '',
      cells: [LETTERS[i] + '  ' + seatLabel(seats, i, mine), c],
    }))));
    K.put(audit, K.note('The seal is taken modulo ' + seal.mod + '.'));
  } else {
    K.put(audit, K.note('Stated once, in the rules that opened this table.'));
  }

  // ---------------------------------------------------------- the history --
  const log = v.log || [];
  const width = Math.max(
    seats ? seats.length : 0,
    ...log.map(r => Math.max(r.draws.length, r.reports.length))) || LETTERS.length;
  const cols = [];
  for (let i = 0; i < width; i++) cols.push(seatLabel(seats, i, mine));
  const rows = log.map(r => {
    const cells = ['round ' + r.round];
    for (let i = 0; i < width; i++) {
      const d = r.draws[i], p = r.reports[i];
      cells.push((d === undefined ? '--' : d) + ' \u2192 ' + (p === undefined ? '--' : p));
    }
    cells.push(r.pass ? 'pass' : 'FAIL');
    return { cells: cells };
  });
  const past = K.wide('rounds certified  \u00b7  draw \u2192 report',
    rows.length ? K.table([''].concat(cols).concat(['seal']), rows)
      : K.note('Nothing certified yet -- this is the first round.'));

  K.put(box, K.panels(drew, audit, past));

  // ----------------------------------------------------------- the report --
  const dial = K.dial({
    lo: lo, hi: hi, value: null,
    label: 'the figure you report',
    hint: 'an integer from ' + lo + ' through ' + hi,
  });
  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'file your report'), dial.node);
  const err = K.note('', 'warn');
  K.put(a, err);
  K.put(a, K.submit('seal the certificate', () => {
    const n = dial.get();
    if (n === null) { err.textContent = 'name the figure you are reporting.'; return; }
    err.textContent = '';
    fileIt(ctx, v.token, { n: n }, msg => { err.textContent = msg; });
  }));
  K.put(box, a);
  return box;
};
})();
