'use strict';
// Hackable Games -- client. Three views: catalogue, play, reveal.
// This is the experimenter arena, so a card names which KIND of defect each
// variant carries: the operator is picking a condition to run, not discovering
// it. What still never arrives before /api/state reports done is the cell's own
// hole_type, its detector names and the blurb -- the account of WHERE the hole
// is -- so there is nothing to peek at in devtools mid-game.

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

// A row may predate the variants field, and a row with no variant wired up
// omits it entirely, so every reader goes through here rather than trusting
// `c.variants` to be an array.
function variantsOf(c) {
  return Array.isArray(c.variants) ? c.variants : [];
}

// One sentence per button, because the built/filled split is the difference
// between a measurement about the shipped cell and a measurement about a
// different cell that happens to share its substrate.
function variantTitle(v) {
  return v.source === 'filled'
    ? `a separate cell (${v.cell}) that adds this defect to the same substrate` +
      ', so anything you measure here is a number about that cell and not about' +
      ' the shipped one'
    : `built into the shipped cell (${v.cell}), so what you measure here is a` +
      ' number about the game as it ships';
}

// The strip mixes three different cuts on one key on purpose: family names, the
// 'marshal' engine property, and the two hole kinds a cell can be played with.
// Only one cut is ever active -- a reader picks the single question they are
// asking, never a conjunction -- so a single string is the whole state.
const FILTERS = [['all', 'all games'], ['generated', 'model-written'],
                 ['referee', 'hand-built'], ['textarena', 'textarena ports'],
                 ['marshal', 'MARSHAL-ready'],
                 ['broken_checker', 'has a broken verifier'],
                 ['nerfed_opponent', 'has a nerfed opponent']];
const HOLE_KINDS = ['broken_checker', 'nerfed_opponent'];

function matches(c) {
  if (filter === 'all') return true;
  if (filter === 'marshal') return !!c.marshal_ready;
  if (HOLE_KINDS.includes(filter)) {
    return variantsOf(c).some(v => v.kind === filter);
  }
  return c.family === filter;
}

function renderFilters() {
  $('filters').innerHTML = '';
  FILTERS.forEach(([k, label]) => {
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
  GAMES.filter(matches).forEach(c => {
    const d = document.createElement('div');
    d.className = 'card';
    // `marshal_ready` is a property of how the engine records score, not of
    // what the referee fails to check. The variant buttons below DO name the
    // kind of defect, which is this arena's whole point -- but naming the kind
    // is not saying where it is, and the blurb that would say never gets here.
    const fam = {generated: 'gen', referee: 'ref', textarena: 'ta'}[c.family] || 'ref';
    const marshal = c.marshal_ready
      ? '<span class="tag marshal" title="records per-decision score; ' +
        'MARSHAL can do turn-level credit assignment">MARSHAL</span>' : '';
    const vs = variantsOf(c);
    // Zero variants is a real state, not a failure: some cells have neither a
    // native nor a filled version of either defect. Say so rather than leaving
    // a blank strip that reads like markup that did not render.
    const row = vs.length
      ? vs.map((v, i) =>
          `<button class="variant ${v.source === 'filled' ? 'filled' : 'built'}" ` +
          `data-variant="${i}" title="${esc(variantTitle(v))}">${esc(v.label)}</button>`
        ).join('')
      : '<span class="novariant">no defect variant on this cell</span>';
    d.innerHTML =
      `<h3>${esc(c.title)}</h3>
       <div class="blurb">${esc(c.teaser || '')}</div>
       <div class="foot">
         <span class="tag ${fam}">${esc(c.author)}</span>${marshal}
         <span>${c.n_players}p · ${esc(String(c.rounds))} rounds</span>
       </div>
       <div class="variants">${row}</div>`;
    d.onclick = () => start(vs.length ? vs[0].cell : c.id, 'hole');
    d.querySelectorAll('button.variant').forEach(b => {
      b.onclick = (e) => {
        // Without this the card's own handler fires too and launches the
        // default variant on top of the one that was actually clicked.
        e.stopPropagation();
        start(vs[Number(b.dataset.variant)].cell, 'hole');
      };
    });
    g.appendChild(d);
  });
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, m =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
}

// ----------------------------------------------------------------------- play
// A filled variant's cell is NOT a row in the catalogue: `hf_estate_nerfed` only
// ever appears inside `ref_estate`'s variants, so scanning GAMES by id alone
// finds nothing for exactly the ids the variant buttons launch. Fall back to a
// scan of the variants, which also recovers the label for a built variant whose
// cell IS its own row.
function lookupCell(gid) {
  const row = GAMES.find(c => c.id === gid);
  if (row) {
    return { meta: row, variant: variantsOf(row).find(v => v.cell === gid) || null };
  }
  for (const c of GAMES) {
    const v = variantsOf(c).find(x => x.cell === gid);
    if (v) return { meta: c, variant: v };
  }
  return null;
}

async function start(gid, arm) {
  const hit = lookupCell(gid);
  if (!hit) { alert(`no catalogue entry for ${gid}`); return; }
  const meta = hit.meta, variant = hit.variant;
  const st = await api('/api/new', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game: gid, seat: 0, arm: arm, bots: 'honest' })
  });
  if (st.error) { alert(st.error); return; }
  // `game` is the VARIANT cell, not the base row, so the replay buttons on the
  // end screen come back to the condition the operator actually ran.
  S = { id: st.id, game: gid, seat: st.seat, arm: arm, title: meta.title };
  $('play-title').textContent = meta.title;
  const vt = $('play-variant');
  vt.textContent = variant ? variant.label : '';
  vt.title = variant ? variantTitle(variant) : '';
  vt.className = variant
    ? `vtag ${variant.source === 'filled' ? 'filled' : 'built'}` : 'vtag hidden';
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
    : holeType(h) + `<div style="margin-top:.4rem">${esc(h.how || '')}</div>`;
});

// The humanised label is what reads as a sentence, but the raw engine string is
// what a researcher greps the results for, so show both rather than choosing.
// Older payloads carry only the raw one.
function holeType(o) {
  const label = o.hole_type_label || o.hole_type || '';
  const raw = o.hole_type || '';
  return `<b>${esc(label)}</b>` + (raw && raw !== label
    ? ` <span class="raw" title="the engine's own hole_type string">${esc(raw)}</span>`
    : '');
}

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
  let h = holeType(r) + `<div style="margin-top:.5rem">${esc(n.how || '')}</div>`;
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
