'use strict';
/*
  WORD AUCTIONS -- the two cells whose last move is a line of free text.

  Four boards live here because they share one shape: a sealed number while
  the lots or the letters go by, and then a line the player writes rather
  than picks. Numbers get a labelled box with the range the prompt stated.
  The line gets an empty box and a submit, and nothing else -- no list of
  suggestions, no completion, no box that refuses what the referee would
  have accepted.

  THE LEXICON IS DRAWN WHOLE. Every entry is scored off the letter values the
  prompt prints and marked with whether the rack covers it, which is a
  spelling check the player could do by eye from the same two lines. Entries
  the rack does not cover STAY ON THE LIST and stay unmarked as anything but
  uncovered: narrowing the list to the words a rack can spell would be the
  board answering the question this cell asks. The word box takes whatever is
  typed into it for the same reason.

  ON REPLY SHAPE. The adapter hands over a template with one slot in it and
  the host fills it. A sealed number goes through `ctx.sendFilled`, which
  reports a slot nobody filled on the board rather than posting it, so an
  unanswered dial cannot leave as a bid of nothing. The written line goes
  through `ctx.sendText`, where the empty string is a value rather than an
  unfinished move, and the typed string is spliced in once and never read for
  slots of its own. No board here writes the shape of a reply itself and no
  player ever reads one: the labels are prose.

  NO MEMO. Unlike most cells, both adapters re-read the tables they need out
  of every prompt -- the letter values and the lexicon arrive on each bid and
  again at the word stage, and the bid range carries a default -- so there is
  nothing here to cache between turns.
*/
window.UI = window.UI || {};

(function () {
const K = () => window.KIT;

// The reply's shape belongs to the adapter and the filling belongs to the
// host. `sendFilled` fills and posts in one step and says so on the board
// when a slot is still empty; `fill` only hands the text back, so that path
// still has to post it. Neither is given a local substitute: a template
// filled here would have to decide for itself what an empty slot means, and
// the wrong answer is a bid of nothing posted as though it were named.
function fileIt(ctx, token, values) {
  if (typeof ctx.sendFilled === 'function') return ctx.sendFilled(token, values);
  return ctx.send(ctx.fill(token, values));
}

function tally(list) {
  const m = {};
  (list || []).forEach(ch => { m[ch] = (m[ch] || 0) + 1; });
  return m;
}

// Which letters a word needs that the rack does not hold, in the order the
// word needs them. Arithmetic the player was handed both sides of.
function missing(word, rack) {
  const have = tally(rack), out = [];
  String(word || '').toUpperCase().split('').forEach(ch => {
    if (have[ch]) have[ch] -= 1;
    else out.push(ch);
  });
  return out;
}

// A word's total off the published letter table, or null if the table is not
// in the prompt or the word uses a letter the table does not price.
function score(word, values, mult) {
  if (!values) return null;
  let t = 0;
  const chars = String(word || '').toUpperCase().split('');
  if (!chars.length) return null;
  for (let i = 0; i < chars.length; i++) {
    const v = values[chars[i]];
    if (v === undefined) return null;
    t += v;
  }
  return (mult || 1) * t;
}

function rack(k, letters, values) {
  if (!letters || !letters.length) return k.note('no letters bought yet');
  const row = k.el('div', 'bd-row');
  letters.forEach(ch => k.put(row, k.letterTile(ch, values ? values[ch] : null)));
  return row;
}

function lexicon(k, v, footer) {
  if (!v.lexicon || !v.lexicon.length) return null;
  const mult = v.scoring ? v.scoring.word : 1;
  const rows = v.lexicon.map(w => {
    const pts = score(w, v.values, mult);
    const short = missing(w, v.rack || []);
    return {
      cells: [w, pts === null ? '' : pts,
        short.length ? 'short of ' + short.join(', ') : 'your letters spell it'],
    };
  });
  const head = v.scoring ? 'scores at ' + mult + 'x' : 'letter values total';
  const p = k.wide('the lexicon',
    k.table(['word', head, 'against your letters'], rows));
  if (footer) k.put(p, k.note(footer));
  return p;
}

// ------------------------------------------------------------ letters --

window.UI.letter_bid = function (v, ctx) {
  const k = K();
  const held = v.rack || [];
  const box = k.board();

  k.put(box, k.head({
    step: 'Letter ' + v.index + ' / ' + v.total,
    title: 'seal a bid',
    sub: held.length ? 'bought so far ' + held.join(' ') : 'nothing bought yet',
    scores: [{ name: 'coins left', score: v.coins }],
    me: 'coins left',
  }));

  const up = k.panel('up for auction',
    k.put(k.el('div', 'bd-row'), k.letterTile(v.letter, v.letter_worth, { lit: true })),
    k.note('This letter is worth ' + v.letter_worth + ' in word scoring.'));
  if (v.scoring) {
    k.put(up, k.note('A word scores ' + v.scoring.word +
      'x the total of its letter values, and every unspent coin scores ' +
      v.scoring.coin + '.'));
  }

  const mine = k.panel('your rack',
    rack(k, held, v.values),
    k.coins(v.coins, { label: 'coins left' }));

  const rows = (v.log || []).map(r => ({
    cells: ['letter ' + r.index + ' (' + r.letter + ')',
      (r.bids || []).join(' / '), r.outcome],
  }));
  const past = k.panel('letters settled',
    rows.length ? k.table(['', 'bids', 'outcome'], rows)
      : k.note('this is the first letter'));

  k.put(box, k.panels(up, mine, past, lexicon(k, v)));

  // `value: null` opens the box empty and keeps `get()` answering null until
  // the player types, nudges or drags. Seeded with the bottom of the range it
  // would have named an amount for the player before the player named one.
  const bid = k.dial({
    lo: v.lo, hi: v.hi, value: null,
    label: 'your bid, a whole number from ' + v.lo + ' to ' + v.hi,
    hint: 'you hold ' + v.coins + ' coins',
  });

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'seal one bid for this letter'), bid.node);
  const err = k.note('', 'warn');
  k.put(a, err, k.submit('seal it', () => {
    if (bid.get() === null) { err.textContent = 'name an amount.'; return; }
    fileIt(ctx, v.token, { n: bid.get() });
  }));
  k.put(box, a);
  return box;
};

window.UI.letter_word = function (v, ctx) {
  const k = K();
  const held = v.rack || [];
  const mult = v.scoring ? v.scoring.word : 1;
  const box = k.board();

  k.put(box, k.head({
    step: 'The auction is over',
    title: 'submit one word',
    scores: [{ name: 'coins left', score: v.coins }],
    me: 'coins left',
  }));

  const mine = k.panel('the letters you bought',
    rack(k, held, v.values),
    k.coins(v.coins, { label: 'coins left' }));
  if (v.scoring) {
    k.put(mine, k.note('Unspent coins score ' + v.scoring.coin +
      ' each, so the ' + v.coins + ' you are holding score ' +
      v.coins * v.scoring.coin + '.'));
    k.put(mine, k.note('A word scores ' + v.scoring.word +
      'x the total of its letter values.'));
  }

  k.put(box, k.panels(mine,
    lexicon(k, v, 'Every entry stays on the list, and the box below takes ' +
      'whatever you type into it.')));

  const readout = k.note('');
  const err = k.note('', 'warn');
  const listed = new Set((v.lexicon || []).map(w => String(w).toUpperCase()));

  function reflect(text) {
    const w = String(text || '').trim().toUpperCase();
    if (!w) { readout.textContent = ''; return; }
    const bits = [];
    const pts = score(w, v.values, mult);
    if (pts !== null) bits.push('scores ' + pts);
    const short = missing(w, held);
    bits.push(short.length ? 'your letters are short of ' + short.join(', ')
      : 'your letters spell it');
    bits.push(listed.has(w) ? 'on the lexicon list' : 'not on the lexicon list');
    readout.textContent = w + ': ' + bits.join('; ') + '.';
  }

  const word = k.textbox({
    label: 'your word',
    send: 'submit',
    // What goes on the line is what was typed. `sendText` splices the string
    // in as a string, so a player who types braces is sending braces.
    //
    // The one check is that something was typed at all: a word is what this
    // stage asks for, taking none is the other answer and has its own
    // control, and an empty box is neither. The check reads a trimmed copy
    // and nothing else -- the reply carries the text itself, uncorrected and
    // unchecked against the lexicon or the rack.
    onSend: text => {
      const raw = text === undefined || text === null ? '' : String(text);
      if (!raw.trim()) { err.textContent = 'type a word, or take none.'; return; }
      ctx.sendText(v.token, 'w', raw);
    },
  });
  word.input.oninput = () => { err.textContent = ''; reflect(word.input.value); };

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'submit one word, or none'),
    word.node, readout, err);
  if (v.none_token) {
    k.put(a, k.actions([{ label: 'none', token: v.none_token }], ctx.send));
  }
  k.put(box, a);
  return box;
};

// --------------------------------------------------------------- lots --

window.UI.blind_sealed = function (v, ctx) {
  const k = K();
  const box = k.board();
  const log = v.log || [];
  const byLot = {};
  log.forEach(r => { byLot[r.lot] = r; });

  k.put(box, k.head({
    step: 'Lot ' + v.lot + ' / ' + v.lots,
    title: 'seal a bid',
    scores: [{ name: 'your net', score: v.net }],
    me: 'your net',
  }));

  const cells = [];
  for (let i = 1; i <= v.lots; i++) {
    const r = byLot[i];
    cells.push({
      label: 'lot ' + i,
      sub: r ? r.you + ' / ' + r.their_bid : (i === v.lot ? 'sealing now' : ''),
      tag: r ? 'you / ' + r.rival : '',
      now: i === v.lot,
      done: !!r,
    });
  }
  const strip = k.wide('the lots', k.track(cells),
    k.note('Under a settled lot: your bid, then the bid it was published against.'));

  const here = k.panel('this lot',
    k.meter({
      value: v.value, max: Math.max(v.hi, v.value) || 1,
      label: 'your value for this lot',
      text: v.value + ' -- bids run from ' + v.lo + ' to ' + v.hi,
    }));

  const rows = log.map(r => ({
    cells: ['lot ' + r.lot, r.you, r.rival + ' ' + r.their_bid, r.outcome],
  }));
  const past = k.panel('lots settled',
    rows.length ? k.table(['', 'you bid', 'against', 'outcome'], rows)
      : k.note('this is the first lot'));

  k.put(box, k.panels(strip, here, past));

  const sum = k.note('');
  const err = k.note('', 'warn');
  // Empty until the player fills it -- see the note in `letter_bid`.
  const bid = k.dial({
    lo: v.lo, hi: v.hi, value: null,
    label: 'your bid, a whole number from ' + v.lo + ' to ' + v.hi,
    hint: 'your value for this lot is ' + v.value,
    onChange: n => {
      err.textContent = '';
      sum.textContent = n === null ? '' : 'A bid of ' + n + ' against a value of ' +
        v.value + ' leaves ' + k.signed(v.value - n) + ' if it wins.';
    },
  });

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'seal one bid for this lot'), bid.node, sum);
  k.put(a, err, k.submit('seal it', () => {
    if (bid.get() === null) { err.textContent = 'name an amount.'; return; }
    fileIt(ctx, v.token, { n: bid.get() });
  }));
  k.put(box, a);
  return box;
};

window.UI.blind_note = function (v, ctx) {
  const k = K();
  const box = k.board();

  k.put(box, k.head({
    step: v.before_lot === null || v.before_lot === undefined
      ? 'A note arrives' : 'Before lot ' + v.before_lot,
    title: 'the private line',
    sub: 'from ' + v.from,
  }));

  k.put(box, k.panels(k.wide('what arrived on the line',
    k.quote(v.from, v.text))));

  const line = k.textbox({
    label: 'your reply on the line',
    send: 'submit',
    // Sent as typed -- see the note in `letter_word` -- and sent even when
    // the box is empty. Saying nothing back on a line nobody is obliged to
    // answer is one of the replies this cell is here to watch for, and the
    // referee reads a blank line as the blank line it is, so a box that
    // refused to send one would be refusing a move on the referee's behalf.
    onSend: text => ctx.sendText(v.token, 'text', text),
  });

  const a = k.act();
  k.put(a, k.el('div', 'bd-panel-h', 'reply on the line'),
    line.node,
    k.note('The box is empty and stays empty until you write in it. ' +
      'Whatever you write goes on the line as you wrote it, and sending ' +
      'nothing is a reply too.'));
  k.put(box, a);
  return box;
};
})();
