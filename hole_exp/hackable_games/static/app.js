'use strict';
// Hackable Games -- client. Three views: catalogue, play, reveal.
// The client is deliberately dumb about holes: it never receives hole_type or
// detector names until /api/state reports done, so there is nothing to peek at
// in devtools mid-game.

const $ = (id) => document.getElementById(id);
const api = async (path, opts) => {
  const r = await fetch(path, opts);
  return r.json();
};

let GAMES = [];
let filter = 'all';
let S = null;          // {id, game, seat, arm}
let played = 0, found = 0;

// ------------------------------------------------------------------ catalogue
function show(view) {
  ['view-list', 'view-play', 'view-end'].forEach(v =>
    $(v).classList.toggle('hidden', v !== view));
}

function renderStats() {
  $('stats').textContent =
    `${GAMES.length} cells · ${played} played · ${found} holes found`;
}

function renderFilters() {
  const fams = [['all', 'all games'], ['generated', 'model-written'],
                ['referee', 'hand-built']];
  $('filters').innerHTML = '';
  fams.forEach(([k, label]) => {
    const b = document.createElement('button');
    b.textContent = label;
    b.className = filter === k ? 'on' : '';
    b.onclick = () => { filter = k; renderFilters(); renderGrid(); };
    $('filters').appendChild(b);
  });
}

function renderGrid() {
  const g = $('grid');
  g.innerHTML = '';
  GAMES.filter(c => filter === 'all' || c.family === filter).forEach(c => {
    const d = document.createElement('div');
    d.className = 'card';
    d.innerHTML =
      `<h3>${esc(c.title)}</h3>
       <div class="blurb">${esc(c.teaser || '')}</div>
       <div class="foot">
         <span class="tag ${c.family === 'generated' ? 'gen' : 'ref'}">${esc(c.author)}</span>
         <span>${c.n_players}p · ${esc(String(c.rounds))} rounds</span>
       </div>`;
    d.onclick = () => start(c.id, 'hole');
    g.appendChild(d);
  });
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, m =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
}

// ----------------------------------------------------------------------- play
async function start(gid, arm) {
  const meta = GAMES.find(c => c.id === gid);
  const st = await api('/api/new', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game: gid, seat: 0, arm: arm, bots: 'honest' })
  });
  if (st.error) { alert(st.error); return; }
  S = { id: st.id, game: gid, seat: st.seat, arm: arm, title: meta.title };
  $('play-title').textContent = meta.title;
  $('play-meta').textContent =
    `${meta.author} · seat ${st.seat} of ${meta.n_players}` +
    (arm === 'nohole' ? ' · AUDITED ARM' : '');
  $('movelog').innerHTML = '';
  const sp = $('spoiler');
  sp.open = false;
  $('spoilerbody').textContent = '…';
  sp.dataset.loaded = '';
  show('view-play');
  paint(st);
}

function paint(st) {
  if (st.error) { $('hint').textContent = st.error; return; }
  if (st.done) { return finish(st); }
  const p = st.pending;
  if (!p) {
    $('prompt').textContent = 'waiting for the other seats…';
    $('quick').innerHTML = '';
    return;
  }
  $('prompt').textContent = p.prompt;
  $('prompt').scrollTop = $('prompt').scrollHeight;
  renderQuick(p.prompt);
  $('hint').textContent = `stage: ${p.phase}`;
  $('hint').className = 'hint';
  $('answer').focus();
}

// Offer the literal tokens the prompt spells out. This is a typing aid only --
// it lifts exactly the strings already printed in the "Reply with ..." line, so
// it can never surface a move the player was not already shown.
function renderQuick(prompt) {
  const q = $('quick');
  q.innerHTML = '';
  const tail = prompt.split('\n').filter(l => /Reply with/i.test(l)).join(' ');
  const seen = new Set();
  (tail.match(/\[[a-zA-Z_]+:[^\]]{0,32}\]/g) || []).forEach(tok => {
    if (seen.has(tok)) return;
    seen.add(tok);
    const b = document.createElement('button');
    b.textContent = tok;
    b.onclick = () => {
      if (/[<>]/.test(tok)) {
        const verb = tok.slice(1).split(':')[0];
        $('answer').value = `[${verb}: `;
        $('answer').focus();
      } else { $('answer').value = tok; send(); }
    };
    q.appendChild(b);
  });
}

async function send() {
  if (!S) return;
  const text = $('answer').value.trim();
  if (!text) return;
  if (!/\[[a-zA-Z_]+\s*:[^\]]*\]/.test(text)) {
    $('hint').textContent = 'that has no bracketed token in it — the engine reads the last [verb: value]';
    $('hint').className = 'hint warn';
    return;
  }
  const li = document.createElement('li');
  li.innerHTML = `<b>${esc(text)}</b>`;
  $('movelog').appendChild(li);
  $('movelog').scrollTop = $('movelog').scrollHeight;
  $('answer').value = '';
  $('prompt').textContent = 'resolving…';
  $('quick').innerHTML = '';
  const st = await api('/api/move', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: S.id, text })
  });
  paint(st);
}

// The spoiler is fetched only when opened, so the hole is never sitting in a
// payload the player did not ask for. Taking it is recorded server-side.
$('spoiler').addEventListener('toggle', async () => {
  const sp = $('spoiler');
  if (!sp.open || sp.dataset.loaded || !S) return;
  sp.dataset.loaded = '1';
  const h = await api(`/api/hint?id=${encodeURIComponent(S.id)}`);
  $('spoilerbody').innerHTML = h.error ? esc(h.error)
    : `<b>${esc(h.hole_type || '')}</b><div style="margin-top:.4rem">${esc(h.how || '')}</div>`;
});

// --------------------------------------------------------------------- reveal
function finish(st) {
  const r = st.result || {};
  played += 1;
  if (r.found_hole) found += 1;
  renderStats();
  $('verdict').textContent = r.found_hole
    ? 'You found the hole.' : 'You played it straight.';
  $('verdict').className = 'verdict ' + (r.found_hole ? 'found' : 'clean');

  const bits = [`your score ${r.my_score}`, `margin ${r.margin >= 0 ? '+' : ''}${r.margin}`];
  if (r.gain !== null && r.gain !== undefined) {
    bits.push(`vs an honest referee ${r.gain >= 0 ? '+' : ''}${r.gain}`);
  }
  bits.push(`${r.decisions} decisions`);
  if (r.invalid) bits.push(`${r.invalid} unparsed`);
  if (S && S.arm === 'nohole') bits.push('AUDITED ARM');
  if (r.used_hint) bits.push('you revealed the hole');
  $('scoreline').textContent = bits.join('  ·  ');

  let rows = '<tr><th>detector</th><th>you tripped</th><th>chances</th></tr>';
  Object.entries(r.detectors || {}).forEach(([k, v]) => {
    const hard = (r.hard || []).includes(k);
    const cls = v.violations > 0 ? 'hit' : 'zero';
    rows += `<tr><td>${esc(k)}${hard ? '' : ' <span class="zero">(soft)</span>'}</td>` +
            `<td class="${cls}">${v.violations}</td><td class="zero">${v.opportunities}</td></tr>`;
  });
  $('dtab').innerHTML = rows;

  const n = r.note || {};
  let h = `<b>${esc(r.hole_type || '')}</b><div style="margin-top:.5rem">${esc(n.how || '')}</div>`;
  if (n.exploit) h += `<div class="kv">exploit: ${esc(n.exploit)}</div>`;
  if (n.honest) h += `<div class="kv">honest: ${esc(n.honest)}</div>`;
  $('holebox').innerHTML = h;

  $('btn-audited').classList.toggle('hidden', !S || S.arm === 'nohole');
  show('view-end');
}

// ---------------------------------------------------------------------- wiring
$('btn-send').onclick = send;
$('answer').addEventListener('keydown', e => { if (e.key === 'Enter') send(); });
$('btn-quit').onclick = () => {
  if (S) api('/api/quit', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: S.id })
  });
  S = null; show('view-list');
};
$('btn-back').onclick = () => { S = null; show('view-list'); };
$('btn-again').onclick = () => S && start(S.game, S.arm);
$('btn-audited').onclick = () => S && start(S.game, 'nohole');
$('home-link').onclick = () => { S = null; show('view-list'); };

(async () => {
  GAMES = (await api('/api/games')).games || [];
  renderStats(); renderFilters(); renderGrid();
})();
