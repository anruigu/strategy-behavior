'use strict';
// Plays -- study client.
//
// The shell: name gate, catalogue, run loop, and the two end cards. The board
// itself is drawn by whichever module under /board-ui/ claims the view's
// `kind`.
//
// A PARTICIPANT NEVER TYPES PROTOCOL. This build used to keep a composer next
// to the board: a text box, and a placeholder reading `[fire: C4]`. It was
// there because most cells had no bespoke board, so the prompt plus a text
// box WAS the interface. That is now a measurement problem rather than a
// convenience. `[verb: value]` is the referee's wire format, and a page that
// shows it teaches the player to think in it -- to read the rules as a
// grammar with fields, and to wonder what else a field will accept. That is
// the exact question this study exists to ask, and asking it on the page is
// asking it for them. So the bracket syntax appears nowhere a participant can
// see, there is no free-text move path, and a cell with no board is a cell
// that cannot be played here rather than one that falls back to typing.
//
// Two places on this page show text this file did not write -- the rules
// drawer, which carries the referee's prompt, and the move log, which used to
// echo the token just posted. Removing the composer did not make either of
// them safe: the prompt ENDS in the wire format, spelled out and worked
// through, and the log reprinted a live example of it after every move. Both
// are filtered now rather than trusted -- `displayRules` and `moveLogLabel`.
//
// The consequence to keep in mind when adding a cell: no renderer means no
// play. `boardUnavailable` says so plainly instead of degrading, because the
// degraded mode is the one that quietly ruins the data.
//
// Catalogue rows may carry a `variants` array for operator debugging on
// /api/games; live-run payloads still must not name the hole. There is no
// hole_type, no detector table and no `gain` in any payload this file can
// receive while a run is live, so there is nothing to find in devtools and
// nothing to accidentally render mid-play.

const $ = (id) => document.getElementById(id);
const api = async (path, opts) => (await fetch(path, opts)).json();
const post = (path, body) => api(path, {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body)
});

let PLAYER = '';
let GAMES = [];
let RUN = null;        // {run_id, game, title, plays, variant}
let PENDING = null;    // last pending decision
let sending = false;
// Bumped every time the board is redrawn. A renderer captures the value it
// was built under and its context refuses to send once the value has moved
// on, so a stale board -- one still on screen for the instant between a click
// and the redraw, or one a renderer kept a reference to -- cannot post a move
// against a decision that is already answered. See `send`.
let epoch = 0;

function show(view) {
  ['view-name', 'view-list', 'view-play', 'view-between', 'view-done']
    .forEach(v => $(v).classList.toggle('hidden', v !== view));
}

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, m =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
}

// ── the rules drawer ────────────────────────────────────────────────
// One prompt, two readers. The engine's reader is a model that has to answer
// in `[verb: value]`, so nearly every prompt ends by spelling the wire format
// out and showing it worked -- `Reply with [fire: n], an integer from 1
// through 5.` The other reader is the person at the board, and for them that
// sentence is precisely the thing this build keeps off the page (see the
// header): it names the grammar, demonstrates it, and hands over the idea
// that a move is a field you fill.
//
// So the drawer is given the prompt with the response protocol taken out of
// it and, as far as can be managed, nothing else taken out. Rules, state,
// history, payoffs and the other seats' notes all stay: a drawer that
// quietly swallowed a payoff line would be its own measurement problem, and
// the drawer is the only place some of that text appears.
//
// DISPLAY ONLY. `send` posts the token the board assembled, byte for byte,
// and `paint` hands the renderer `st.pending.view` untouched. Nothing on the
// wire and nothing a renderer reads passes through here; the adapters under
// views/ keep parsing the raw prompt server-side, so stripping a `Reply
// with` line cannot cost a board its options.

// Deliberately close to the referee's own token pattern, and deliberately
// unable to span a line or nest: the point is to recognise the shape, not to
// parse it back into a move.
const TOKENISH = /\[\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*([^\][\n]{0,80}?)\s*\]/g;

// Sentences that exist to describe the reply, not the game. The lead forms
// need a token in the same sentence before they count, so `Reply to a raid
// within one round` -- a rule -- survives while `Reply with [act: raid]`
// does not. The meta forms are the instructions aimed at a model reader
// (`the bracketed token only`, `keep any reasoning brief`) and carry no game
// content at all, so they go on sight.
const FORMAT_LEAD = /^\s*(reply|respond|answer)\b/i;
const FORMAT_CLAUSE = /\b(reply|respond|answer|answer back)\s+(with|on the line with|using)\b/i;
const FORMAT_META =
  /(bracketed\s+(token|action)|keep any reasoning brief|one short line of reasoning|and nothing else)/i;

// What may be rescued from a dropped sentence. A bound is a rule -- "an
// integer from 0 to 10" is as much part of the game as the payoff table --
// and it is usually written as a tail on the very sentence that teaches the
// format. The options in `Reply with [hunt: stag] or [hunt: hare]` need no
// rescuing: the board draws them.
const BOUNDISH =
  /\b(integer|whole number|number|digits?|from|through|between|up to|at least|at most|no more than|inclusive)\b/i;

// `e.g.` and friends end in a full stop and would otherwise split a sentence
// in half, stranding the example half -- the worst possible half to strand.
const ABBREV = /\b(e\.g|i\.e|etc|vs|approx|no)\./gi;
const DOT = '\u0000';

// `[hunt: stag]` becomes `stag`. The value is the game's word for the thing
// and the brackets are the referee's plumbing, so this keeps the sentence
// readable -- `both players choose simultaneously: stag or hare` -- while
// leaving nothing token-shaped behind. It is also what makes a participant's
// free text safe: a note reading `[fire: C4]` is shown as `C4`, inert text
// by another player, never a demonstration of protocol.
function unbracket(text) {
  return String(text == null ? '' : text)
    .replace(TOKENISH, (_, verb, value) => String(value).replace(/[<>]/g, '').trim())
    // A token someone forgot to close, or typed half of. Same treatment.
    .replace(/\[\s*([A-Za-z_][A-Za-z0-9_]*)\s*:/g, '$1:');
}

function sentencesOf(line) {
  const guarded = String(line).replace(ABBREV, (m) => m.split('.').join(DOT));
  const parts = guarded.match(/[^.!?]+(?:[.!?]+|$)/g) || [];
  return parts
    .map(s => s.split(DOT).join('.'))
    .filter(s => s !== '');
}

function hasToken(s) {
  TOKENISH.lastIndex = 0;
  return TOKENISH.test(String(s));
}

// True when the sentence is about how to answer rather than about the game.
function isFormatSentence(s) {
  if (FORMAT_META.test(s)) return true;
  const lead = FORMAT_LEAD.test(s) || FORMAT_CLAUSE.test(s);
  // `Reply with BOTH tokens:` names no token but is unmistakably about the
  // reply -- and it is the line that introduces the examples underneath.
  if (lead && /\btokens?\b/i.test(s)) return true;
  if (!hasToken(s)) return false;
  if (lead) return true;
  // Nothing but tokens, punctuation and joinery: a bare worked example,
  // whatever sentence it was hanging off. `[rook: cooperate] [dove: defect].`
  // and `[bid: N] or [bid: pass]` are both this.
  const residue = s.replace(TOKENISH, ' ')
    .replace(/\b(or|and|then|plus|either|both|also)\b/gi, ' ');
  return !/[A-Za-z]/.test(residue);
}

// A format instruction that ends on a colon is a heading for the lines under
// it -- `Reply with BOTH tokens:` and then one indented example per line.
// Those lines are the instruction continued, so they go with it. The test is
// narrow on purpose: the continuation has to be indented AND token-bearing,
// and the block closes at the first line that is neither.
function opensFormatBlock(rawLine) {
  const parts = sentencesOf(rawLine).filter(s => s.trim() !== '');
  if (!parts.length) return false;
  const last = parts[parts.length - 1];
  return isFormatSentence(last) && /:\s*$/.test(last);
}

// The tail of a dropped sentence, when the tail was a rule. Everything up to
// and including the last token goes; what is left is stripped of the joinery
// that attached it (`, `, `where n is`, `n `) and kept only if it still
// reads as a bound.
function boundOf(s) {
  TOKENISH.lastIndex = 0;
  let end = -1, m;
  while ((m = TOKENISH.exec(s)) !== null) end = m.index + m[0].length;
  if (end < 0) return '';
  let tail = s.slice(end)
    .replace(/^[\s,;:.\u2014-]+/, '')
    .replace(/^(?:and|or)\s+/i, '')
    .replace(/^where\s+[A-Za-z]\s+is\s+/i, '')
    .replace(/^[A-Za-z]\s+(?=an?\s)/, '')
    .trim();
  if (tail.length < 4 || !BOUNDISH.test(tail) || !/[A-Za-z]/.test(tail)) return '';
  tail = tail.charAt(0).toUpperCase() + tail.slice(1);
  return /[.!?]$/.test(tail) ? tail : tail + '.';
}

// `null` means the line was protocol and is gone; `''` means the line was
// blank to begin with. The difference matters one caller up: a stripped
// trailer should not leave a hole where it was, but a blank line the engine
// wrote is the paragraphing of the rules and stays.
function sanitizeLine(line) {
  const raw = String(line);
  if (raw.trim() === '') return '';
  // Sentences are rejoined with no separator of their own, because each one
  // still carries the spacing it was split on. Several engines lay a payoff
  // table out in columns and the drawer renders pre-wrap, so a line's runs
  // of spaces are content: `nobody throws   -> 0` has to come back with the
  // arrow where it was.
  const parts = sentencesOf(raw).map(s => {
    if (!isFormatSentence(s)) return unbracket(s);
    const bound = boundOf(s);
    return bound ? (s.match(/^\s*/) || [''])[0] + bound : '';
  });
  const body = parts.join('').replace(/[ \t]+$/, '');
  return body.trim() === '' ? null : body;
}

// `ACTIONS:` over an empty space. The generated cells head their list of
// stage instructions with a bare label, and once the instructions are gone
// the label is a heading for nothing -- which reads less like tidy rules
// than like a page that failed to load part of itself. A heading is dropped
// only when this filter is what emptied it: a heading the referee wrote with
// nothing under it to begin with is left exactly where it is.
const HEADING = /^\s*[A-Za-z][A-Za-z ]{0,24}:\s*$/;

function dropEmptiedHeadings(lines) {
  lines.forEach((line, i) => {
    if (line === null || !HEADING.test(line)) return;
    let removed = false, kept = false;
    for (let j = i + 1; j < lines.length && !kept; j++) {
      if (lines[j] === '') break;
      if (lines[j] === null) removed = true;
      else kept = true;
    }
    if (removed && !kept) lines[i] = null;
  });
  return lines;
}

// The whole prompt, cleaned. Blank structure is kept because the engines use
// it to separate the rules block from the state block, but the run of blank
// lines left behind by a stripped trailer is collapsed.
function displayRules(prompt) {
  const raw = String(prompt == null ? '' : prompt).split('\n');
  const lines = raw.map(sanitizeLine);

  let open = false;
  raw.forEach((r, i) => {
    if (open) {
      if (/^\s/.test(r) && r.trim() !== '' && hasToken(r)) { lines[i] = null; return; }
      open = false;
    }
    if (opensFormatBlock(r)) open = true;
  });

  dropEmptiedHeadings(lines);
  const out = [];
  lines.forEach(l => {
    if (l === null) return;
    if (l === '' && (out.length === 0 || out[out.length - 1] === '')) return;
    out.push(l);
  });
  while (out.length && out[out.length - 1] === '') out.pop();
  // Belt and braces. Every path above already removes the shape; this is the
  // one line that makes "no token reaches the drawer" true by construction
  // rather than by having enumerated the ways one might.
  return unbracket(out.join('\n'));
}

// What the move log says. It takes the posted token and returns none of it:
// the log sits beside the board for the whole play, so echoing the wire
// format there would undo everything the drawer filter does, one move in.
// The player knows what they just did; what the log is for is showing that
// it landed, and how many have.
function moveLogLabel(_token) {
  return 'Move submitted';
}

// ── the token filler ────────────────────────────────────────────────
// Adapters in views/ hand the client a token TEMPLATE rather than a finished
// token: `[catch: {n}]`, `[bid: {qty} {face}]`, `[declare: {n}]`,
// `[offer: to P{to}, give {gn} {gr}, get {tn} {tr}]`. Filling one in is the
// last step of every move, and it used to be done with string concatenation
// inside each renderer -- two dozen separate handwritten copies of the wire
// format, each free to drift from the adapter that declared it, none of them
// checked by anything. `fill` is the one place a template becomes a token.
//
// The rule about missing values is the part worth reading. `0` is a value and
// so is `false`: `[catch: 0]` is a legal move, and on a fishery it is the
// interesting one. Only `undefined`, `null` and `''` mean "the player has not
// chosen yet", and those raise rather than silently producing `[catch: ]` --
// a token the referee scores as an unparsed move, charged to a participant
// who did nothing wrong.
//
// `values` is normally an object keyed by slot name. A bare value is also
// accepted for a template with exactly one slot, because that is most of them
// and `fill(v.tokens.bid, bid.get())` is the way a board naturally says it.
// With two slots a bare value is ambiguous, so it raises rather than guessing
// which one the caller meant. An array binds to the slots in order.
const SLOT = /\{([A-Za-z_][A-Za-z0-9_]*)\}/g;

function slotsOf(template) {
  const names = [];
  String(template).replace(SLOT, (_, key) => {
    if (names.indexOf(key) < 0) names.push(key);
    return '';
  });
  return names;
}

function fill(template, values) {
  const t = String(template == null ? '' : template);
  const names = slotsOf(t);
  if (!names.length) return t;

  let v;
  if (Array.isArray(values)) {
    v = {};
    names.forEach((k, i) => { v[k] = values[i]; });
  } else if (values !== null && typeof values === 'object') {
    v = values;
  } else {
    if (names.length !== 1) {
      throw new Error('[' + names.join(', ') + '] need naming one by one');
    }
    v = {};
    v[names[0]] = values;
  }

  const missing = [];
  const out = t.replace(SLOT, (_, key) => {
    const val = v[key];
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

// One move is sometimes several tokens -- estate settles a turn with
// `[pay: ...] [buy: ...] [balance: ...]` and the referee reads all three. A
// board hands those over as a list and they are filled and joined here, so a
// partly-answered multi-token move is caught as a whole rather than posted
// with one of its three statements blank.
function fillAll(parts) {
  return parts.map(p => {
    if (p === null || p === undefined) return '';
    if (typeof p === 'string') return p;
    const tpl = p.tpl !== undefined ? p.tpl
      : p.template !== undefined ? p.template : p.token;
    const vals = p.values !== undefined ? p.values : p.vals;
    return fill(tpl, vals);
  }).filter(s => s !== '').join(' ');
}

// Free text is a different kind of empty. A catch of `''` is "the player has
// not chosen"; a message of `''` is the message, and several cells (sidebar,
// the note on a sealed bid, a cheap-talk round) treat a blank filing as a
// legal move. `fill` cannot be taught that distinction -- it does not know
// which slot is a number -- so text goes through here instead.
//
// One pass, and only the named slot. The player's string is spliced in; it is
// not itself scanned for `{slots}`. A participant who types `{n}` or
// `[fire: C4]` is sending that string, not protocol, and a second fill would
// have turned the braces into a hole.
function fillText(template, key, text) {
  const t = String(template == null ? '' : template);
  const k = String(key == null ? '' : key);
  const needle = '{' + k + '}';
  if (!k || t.indexOf(needle) < 0) {
    throw new Error('this move has no ' + (k || 'text') + ' field');
  }
  const body = text == null ? '' : String(text);
  return t.split(needle).join(body);
}

// What every renderer is handed as its second argument. Anything a board
// needs to turn a click into a move is here; nothing a board needs is
// anywhere else.
//
// `era` freezes the redraw this context belongs to. `KIT.actions` wires one
// handler per option and a renderer may hold its context in a closure for as
// long as its nodes are on the page, so "this context is stale" has to be a
// question the context can answer for itself.
function rendererCtx() {
  const era = epoch;
  const live = () => era === epoch;
  const guarded = (text) => { if (live()) send(text); };
  return {
    // Send a token that is already complete. The second argument exists
    // because `KIT.actions` passes `'ui'` and the per-game renderers do too;
    // it is accepted and ignored. Every move made here is `source: ui` --
    // there is no other way to make one any more.
    send: (text) => guarded(text),
    fill,
    // Fill and send in one step. Takes either one template and its values, or
    // a list of `{tpl, values}` for a move that is several tokens. A template
    // with a slot still empty is a half-finished move: it is reported on the
    // board and nothing is posted.
    //
    // `sendChoice` is the same function under the name a board reaches for
    // when the player picked one thing. They were written apart and used
    // interchangeably; keeping them as two behaviours would have meant every
    // renderer had to remember which was which, and getting it wrong would
    // show up as a board that silently does nothing.
    sendFilled: (what, values) => filled(live, guarded, what, values),
    sendChoice: (what, values) => filled(live, guarded, what, values),
    // A free-text slot. Empty string is a value here; see `fillText`.
    sendText: (template, key, text) => texted(live, guarded, template, key, text),
  };
}

function filled(live, guarded, what, values) {
  // Checked before the warning and not just before the send: a retired board
  // must not be able to write its complaint onto the one that replaced it.
  if (!live()) return;
  let text;
  try {
    text = Array.isArray(what) ? fillAll(what) : fill(what, values);
  } catch (err) {
    return boardWarn(err && err.message ? err.message : String(err));
  }
  guarded(text);
}

function texted(live, guarded, template, key, text) {
  if (!live()) return;
  let out;
  try {
    out = fillText(template, key, text);
  } catch (err) {
    return boardWarn(err && err.message ? err.message : String(err));
  }
  guarded(out);
}

// ── what the board says when there is nothing to draw ───────────────
function boardNote(text) {
  $('board').innerHTML = '<div class="b-note">' + esc(text) + '</div>';
}

// A dead end, on purpose. No view, no renderer for the view's kind, a
// renderer that threw, or a move that never left the building. The old build
// answered all four by dropping the raw prompt on screen with a text box
// under it, which turned "this cell has no board" into "this cell is played
// by typing protocol at it" -- see the header.
function boardUnavailable(title, detail) {
  $('board').innerHTML =
    '<div class="b-error"><div class="t">' + esc(title) + '</div>' +
    (detail ? '<div class="d">' + esc(detail) + '</div>' : '') + '</div>';
}

// A complaint about the move being assembled, not about the page. Sits under
// whatever the renderer drew and leaves it in place, because the player is
// mid-move and taking the board away would lose their other choices.
function boardWarn(text) {
  const board = $('board');
  let w = board.querySelector('.b-warn');
  if (!w) {
    w = document.createElement('div');
    w.className = 'b-warn';
    board.appendChild(w);
  }
  w.textContent = text;
}

// ── name gate ───────────────────────────────────────────────────────
$('namebox').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = $('player').value.trim();
  if (!name) return;
  PLAYER = name;
  localStorage.setItem('playsPlayer', name);
  $('who').textContent = `playing as ${name}`;
  await loadGames();
  show('view-list');
});

function variantsOf(c) {
  return Array.isArray(c.variants) ? c.variants : [];
}

// ── catalogue ───────────────────────────────────────────────────────
async function loadGames() {
  GAMES = (await api('/api/games')).games || [];
  const g = $('grid');
  g.innerHTML = '';
  GAMES.forEach(c => {
    const d = document.createElement('div');
    d.className = 'card';
    const vs = variantsOf(c);
    const row = vs.length
      ? vs.map((v, i) =>
          `<button class="variant ${v.source === 'filled' ? 'filled' : 'built'}" ` +
          `data-variant="${i}">${esc(v.label)}</button>`
        ).join('')
      : '<span class="novariant">no other version</span>';
    d.innerHTML =
      `<h3>${esc(c.title)}</h3>
       <div class="blurb">${esc(c.teaser || '')}</div>
       <div class="foot">
         <span>${c.n_players} players &middot; ${esc(String(c.rounds))} rounds</span>
         <span>${c.plays} plays</span>
       </div>
       <div class="variants">${row}</div>`;
    d.onclick = () => startRun(vs.length ? vs[0].cell : c.id, c, vs.length ? vs[0] : null);
    d.querySelectorAll('button.variant').forEach(b => {
      b.onclick = (e) => {
        e.stopPropagation();
        const i = Number(b.dataset.variant);
        startRun(vs[i].cell, c, vs[i]);
      };
    });
    g.appendChild(d);
  });
}

// ── run loop ────────────────────────────────────────────────────────
async function startRun(gid, card, variantOrNull) {
  const st = await post('/api/run/start', { player: PLAYER, game: gid });
  if (st.error) { alert(st.error); return; }
  RUN = {
    run_id: st.run.run_id, game: gid,
    title: (variantOrNull && variantOrNull.title) || card.title,
    plays: st.run.plays, variant: variantOrNull || null
  };
  $('play-title').textContent = RUN.title;
  const vt = $('play-variant');
  const variant = variantOrNull || null;
  vt.textContent = variant ? variant.label : '';
  vt.className = variant
    ? `vtag ${variant.source === 'filled' ? 'filled' : 'built'}`
    : 'vtag hidden';
  show('view-play');
  paint(st);
}

function paint(st) {
  // Every redraw retires the contexts the previous one handed out.
  epoch++;

  // Two different things arrive under `error` and they are not shown the same
  // way. Without a `run` key it is the API refusing the request outright --
  // "no such run" after a server restart -- and that short string is safe and
  // useful to read. WITH a `run` key it is `Session.error`, which is a Python
  // traceback from an engine that crashed mid-play; that one is summarised
  // and never printed, because the frames in it carry the names of the very
  // internals this build exists to keep off the page.
  if (!st || (st.error && !st.run)) {
    return boardUnavailable('This table is not available.',
      (st && st.error) || 'the server sent no reply');
  }
  if (st.error) {
    return boardUnavailable('This play stopped early.',
      'Something went wrong at the table. Nothing you did caused it — ' +
      'leave and pick another one.');
  }
  RUN.plays = st.run.plays;

  $('play-title').textContent = RUN.title;
  $('play-meta').textContent =
    `play ${st.run.play_index + 1} of ${st.run.plays}`;
  $('memory').textContent = st.run.memory || 'This is your first play.';

  if (st.done || !st.pending) {
    if (st.done) return between(st);
    return boardNote('waiting for the other seats…');
  }

  PENDING = st.pending;
  // The prompt keeps its drawer and only its drawer. It is the rules as the
  // referee stated them, which a player may want to reread; it is not, and
  // must not become, a place to type a move -- nor a place to learn that
  // moves can be typed, which is why it goes through `displayRules` and the
  // raw prompt is never written to the page.
  $('prompt').textContent = displayRules(st.pending.prompt);

  const view = st.pending.view;
  if (!view || !view.kind) {
    return boardUnavailable('There is no board for this table yet.',
      'It cannot be played here. Leave and pick another one.');
  }
  const renderer = window.UI && window.UI[view.kind];
  if (typeof renderer !== 'function') {
    return boardUnavailable('There is no board for this table yet.',
      'It cannot be played here. Leave and pick another one.');
  }

  const board = $('board');
  board.innerHTML = '';
  try {
    board.appendChild(renderer(view, rendererCtx()));
  } catch (err) {
    // A renderer that throws leaves a blank div and no way to act, which
    // reads to a participant as a page that is simply broken and to us as a
    // play that stalled for no recorded reason. Say which it is.
    //
    // `KIT` is checked HERE and not before the call, because whether a
    // renderer needs it is the renderer's business: the four boards under
    // play/ui draw with plain DOM and would fail a up-front kit check they
    // have no use for. A missing kit is just the commonest reason one of the
    // shared boards throws, and it is the one with a useful instruction
    // attached, so it gets its own wording.
    if (!window.KIT) {
      boardUnavailable('The board did not finish loading.',
        'Reload the page. If it happens again this table cannot be played.');
    } else {
      boardUnavailable('The board for this table could not be drawn.',
        'It cannot be played here. Leave and pick another one.');
    }
    if (window.console) console.error('renderer failed for ' + view.kind, err);
  }
}

async function send(text) {
  if (!RUN || sending) return;
  text = String(text == null ? '' : text).trim();
  if (!text) return;
  // Claimed before the first await, so a second click landing in the same
  // tick -- a double-tap, a renderer that wired two handlers to one button --
  // returns here rather than posting the move twice. `epoch` covers the
  // other direction: a board that outlives the decision it was drawn for.
  sending = true;
  epoch++;

  const li = document.createElement('li');
  li.textContent = moveLogLabel(text);
  $('movelog').appendChild(li);
  $('movelog').scrollTop = $('movelog').scrollHeight;
  boardNote('resolving…');

  let st;
  try {
    // Always `ui`. The typed path is gone, so there is no `source: text`
    // left to distinguish -- but the field stays on the wire because the
    // collector, the schema on disk and the model arm all still read it.
    st = await post('/api/move', { run: RUN.run_id, text, via: 'ui' });
  } catch (err) {
    // Without this the flag stays set and every later move is dropped in
    // silence -- the page looks alive and answers nothing.
    sending = false;
    return boardUnavailable('That move did not reach the table.',
      'Check your connection. Your earlier moves are safe.');
  }
  sending = false;
  paint(st);
}

// ── between plays ───────────────────────────────────────────────────
function between(st) {
  const r = st.play_result || {};
  const complete = st.run && st.run.complete;
  const sc = (v) => (v >= 0 ? '+' : '') + Number(v).toFixed(1);

  if (complete) {
    const s = (st.run.summary) || {};
    $('d-score').textContent =
      `${(s.scores || []).length} plays  ·  scores ` +
      (s.scores || []).map(sc).join(', ');
    $('d-memory').textContent = (st.run.memory || '').trim();
    $('d-debrief').innerHTML = '';
    if (st.run.debrief) addDebrief();
    $('movelog').innerHTML = '';
    return show('view-done');
  }

  $('b-verdict').textContent = 'Play over.';
  let line = `your score ${sc(r.score || 0)}`;
  if (r.audited && r.caught) {
    line += `  ·  the referee's review after the play charged you ` +
            `${Number(r.fine).toFixed(1)}`;
  }
  $('b-score').textContent = line;
  $('b-memory').textContent = (st.run.memory || '').trim();
  $('movelog').innerHTML = '';
  show('view-between');
}

// Only ever reachable when the process was started with HG_DEBRIEF=1, and
// only after a run is complete.
function addDebrief() {
  const b = document.createElement('button');
  b.className = 'ghost';
  b.textContent = 'show the debrief';
  b.onclick = async () => {
    const d = await api(`/api/debrief?run=${encodeURIComponent(RUN.run_id)}`);
    $('d-debrief').innerHTML = d.error
      ? `<div class="b-note">${esc(d.error)}</div>`
      : `<div class="b-note"><strong>${esc(d.hole_type)}</strong><br>` +   // gate-exempt: the debrief exists to name it
        `${esc(d.how)}</div>`;
  };
  $('d-debrief').appendChild(b);
}

$('btn-next').onclick = async () => {
  const st = await post('/api/run/next', { run: RUN.run_id });
  if (st.complete) { $('d-memory').textContent = st.run.memory || ''; return show('view-done'); }
  show('view-play');
  paint(st);
};

$('btn-stop').onclick = async () => {
  await post('/api/run/quit', { run: RUN.run_id });
  RUN = null; show('view-list');
};

$('btn-another').onclick = () => { RUN = null; show('view-list'); };

$('btn-quit').onclick = async () => {
  if (RUN) await post('/api/run/quit', { run: RUN.run_id });
  RUN = null; show('view-list');
};

$('home-link').onclick = () => { if (!RUN) show(PLAYER ? 'view-list' : 'view-name'); };

// ── boot ────────────────────────────────────────────────────────────
(async () => {
  const saved = localStorage.getItem('playsPlayer');
  if (saved) {
    PLAYER = saved;
    $('player').value = saved;
    $('who').textContent = `playing as ${saved}`;
    await loadGames();
    show('view-list');
  } else {
    show('view-name');
    $('player').focus();
  }
})();
