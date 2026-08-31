'use strict';
// Plays -- study client.
//
// The shell: name gate, catalogue, run loop, and the two end cards. The board
// itself is drawn by whichever module in ui/ claims the view's `kind`; if
// none does, or the server sent no view at all, the player gets the prompt
// text and a composer. That fallback is not a degraded mode -- fifteen of the
// nineteen cells have no bespoke board yet and are played entirely that way.
//
// The client is structurally incapable of leaking a hole: the server never
// sends it one. There is no hole_type, no detector table and no `gain` in any
// payload this file can receive while a run is live, so there is nothing to
// find in devtools and nothing to accidentally render.

const $ = (id) => document.getElementById(id);
const api = async (path, opts) => (await fetch(path, opts)).json();
const post = (path, body) => api(path, {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body)
});

let PLAYER = '';
let GAMES = [];
let RUN = null;        // {run_id, game, title, plays}
let PENDING = null;    // last pending decision
let sending = false;

function show(view) {
  ['view-name', 'view-list', 'view-play', 'view-between', 'view-done']
    .forEach(v => $(v).classList.toggle('hidden', v !== view));
}

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, m =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
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

// ── catalogue ───────────────────────────────────────────────────────
async function loadGames() {
  GAMES = (await api('/api/games')).games || [];
  const g = $('grid');
  g.innerHTML = '';
  GAMES.forEach(c => {
    const d = document.createElement('div');
    d.className = 'card';
    d.innerHTML =
      `<h3>${esc(c.title)}</h3>
       <div class="blurb">${esc(c.teaser || '')}</div>
       <div class="foot">
         <span>${c.n_players} players &middot; ${esc(String(c.rounds))} rounds</span>
         <span>${c.plays} plays</span>
       </div>`;
    d.onclick = () => startRun(c);
    g.appendChild(d);
  });
}

// ── run loop ────────────────────────────────────────────────────────
async function startRun(card) {
  const st = await post('/api/run/start', { player: PLAYER, game: card.id });
  if (st.error) { alert(st.error); return; }
  RUN = { run_id: st.run.run_id, game: card.id, title: card.title,
          plays: st.run.plays };
  show('view-play');
  paint(st);
}

function paint(st) {
  if (st.error) { $('hint').textContent = st.error; return; }
  RUN.plays = st.run.plays;

  $('play-title').textContent = RUN.title;
  $('play-meta').textContent =
    `play ${st.run.play_index + 1} of ${st.run.plays}`;
  $('memory').textContent = st.run.memory || 'This is your first play.';

  if (st.done || !st.pending) {
    if (st.done) return between(st);
    $('board').innerHTML = '<div class="b-note">waiting for the other seats…</div>';
    return;
  }

  PENDING = st.pending;
  $('prompt').textContent = st.pending.prompt || '';

  const view = st.pending.view;
  const renderer = view && window.UI && window.UI[view.kind];
  const board = $('board');
  board.innerHTML = '';
  if (renderer) {
    board.appendChild(renderer(view, { send }));
    setComposer(false);
  } else {
    // No board for this cell: the prompt is the interface, so it is shown
    // open rather than folded into the details element.
    board.innerHTML = '<pre class="promptbox">' +
      esc(st.pending.prompt || '') + '</pre>';
    setComposer(true);
  }
  $('hint').textContent = '';
  $('hint').className = 'hint';
}

// The composer stays reachable even when a board is up, so no legal move is
// ever unreachable through the UI -- but a typed move is recorded as
// `source: text` and never pools with a move made on the board.
function setComposer(open) {
  $('composer').classList.toggle('hidden', !open);
  $('btn-composer').classList.toggle('hidden', open);
  if (open) $('answer').focus();
}

async function send(text, via) {
  if (!RUN || sending) return;
  text = String(text || '').trim();
  if (!text) return;
  if (!/\[[a-zA-Z_]+\s*:?[^\]]*\]/.test(text)) {
    $('hint').textContent =
      'the referee reads the last [verb: value] in your reply';
    $('hint').className = 'hint warn';
    return;
  }
  sending = true;
  const li = document.createElement('li');
  li.innerHTML = `<code>${esc(text)}</code>`;
  $('movelog').appendChild(li);
  $('movelog').scrollTop = $('movelog').scrollHeight;
  $('answer').value = '';
  $('board').innerHTML = '<div class="b-note">resolving…</div>';

  const st = await post('/api/move',
    { run: RUN.run_id, text, via: via || 'ui' });
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

$('btn-composer').onclick = () => setComposer(true);
$('btn-send').onclick = () => send($('answer').value, 'text');
$('answer').addEventListener('keydown', e => {
  if (e.key === 'Enter') send($('answer').value, 'text');
});
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
