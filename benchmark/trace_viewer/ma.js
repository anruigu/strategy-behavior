/* v3-MA views share navigation with the existing single-agent viewer. */
function configureRun() {
  const r = data.runs.find(x => x.id === run), multi = r?.suite === 'v3-MA';
  const phases = multi ? r.phases : [{id:'blind',name:'Unaided'},{id:'hinted',name:'Hinted follow-ups'}];
  if (!phases.some(p => p.id === phase)) phase = phases[0].id;
  document.querySelectorAll('[data-phase]').forEach((button, i) => {
    button.dataset.phase = phases[i].id;
    button.textContent = phases[i].name;
    button.classList.toggle('active', phases[i].id === phase);
  });
  $('#ma-filters').hidden = !multi;
  $('#reflection-filters').hidden = !multi || !r.learning_arms;
  $('#learning').value = learningFilter;
  $('#iteration').value = iterationFilter;
  const oldOutcome = $('#outcome').value;
  $('#outcome').innerHTML = multi
    ? '<option value="all">All episodes</option><option value="hit">With an episode marker</option><option value="miss">Complete · no episode marker</option><option value="incomplete">Incomplete episodes</option>'
    : '<option value="all">All episodes</option><option value="hit">With an exploit</option><option value="miss">Without an exploit</option>';
  $('#outcome').value = [...$('#outcome').options].some(o => o.value === oldOutcome) ? oldOutcome : 'all';
  if (multi) {
    for (const id of ['focal','opponent']) {
      const value = id === 'focal' ? focalFilter : opponentFilter;
      $('#' + id).innerHTML = `<option value="all">All ${id} models</option>` + r.models.map(m => `<option value="${esc(m.id)}">${esc(m.name)}</option>`).join('');
      $('#' + id).value = r.models.some(m => m.id === value) ? value : 'all';
    }
  }
}

function listMA(r) {
  const q = $('#search').value.toLowerCase(), outcome = $('#outcome').value;
  filtered = r.episodes.filter(e => e.condition === phase &&
    (focalFilter === 'all' || e.focal === focalFilter) &&
    (opponentFilter === 'all' || e.opponent === opponentFilter) &&
    (!r.learning_arms || learningFilter === 'all' || e.learning_arm === learningFilter) &&
    (!r.learning_arms || iterationFilter === 'all' || String(e.iteration) === iterationFilter) &&
    (!q || `${e.title} ${e.game} ${e.focal_name} ${e.opponent_name}`.toLowerCase().includes(q)) &&
    (outcome === 'all' || (outcome === 'incomplete' ? e.status !== 'complete' :
      e.status === 'complete' && (outcome === 'hit' ? e.hits > 0 : e.hits === 0))));
  const complete = filtered.filter(e => e.status === 'complete').length;
  $('#count').textContent = `${complete} complete · ${filtered.length - complete} unfinished shown · ${r.episodes.length}/${r.planned||r.episodes.length} recorded in run`;
  const groups = new Map();
  for (const e of filtered) {
    const key = [e.game,e.focal,e.opponent,e.learning_arm||'',e.iteration||''].join('|');
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(e);
  }
  $('#episodes').innerHTML = [...groups.values()].sort((a,b) =>
    a[0].title.localeCompare(b[0].title) || a[0].focal_name.localeCompare(b[0].focal_name) || a[0].opponent_name.localeCompare(b[0].opponent_name)
  ).map(es => `<div class="game"><div class="game-name">${esc(es[0].title)}</div>
    <div class="hintname">Focal: ${esc(es[0].focal_name)}<br>Other seats: ${esc(es[0].opponent_name)}${es[0].learning_arm?'<br>'+esc(label(es[0].learning_arm)):''}</div>
    <div class="seedrow">${es.sort((a,b) => a.seed-b.seed).map(e => `<button class="seed ${e.hits?(['v3ma_signal_convention','v3ma_trust_messages'].includes(e.game)?'pattern':'hit'):''} ${e.status!=='complete'?'failed':''} ${selected===e.id?'selected':''}" data-id="${esc(e.id)}">${e.iteration?'Play '+e.iteration+' · ':''}Seed ${e.seed}<small>${e.status!=='complete'?esc(label(e.status)):e.hits?'Marker observed':'No episode marker'}</small></button>`).join('')}</div></div>`).join('') || '<p class="muted">No matching recorded episodes. Commons have an ordinary condition only.</p>';
  document.querySelectorAll('[data-id]').forEach(b => b.onclick = () => openEpisode(b.dataset.id));
}

const maNumber = x => x == null ? '—' : Number.isInteger(x) ? String(x) : Number(x).toFixed(2);
function maClass(round) {
  if (round.annotations.some(a => a.kind === 'observed')) return 'hit';
  if (round.annotations.some(a => ['association','pattern'].includes(a.kind))) return 'pattern';
  if (round.annotations.length) return 'try';
  return '';
}
function maActor(p, actual=p.actual_model) {
  return `<div class="model-tag" data-seat="${p.pid}"><b>Seat ${p.pid} · ${esc(p.model_name)}</b><span>${esc(p.role)} · ${p.nerfed?'nerfed':'ordinary'}</span><small>${esc(actual || p.requested_model)}${!actual?' · requested; no reply recorded':''}</small></div>`;
}
function maAnnotation(a) {
  if (!a) return '';
  const cls = a.kind === 'candidate' ? 'try' : a.kind === 'observed' ? '' : 'pattern';
  return `<div class="annotation ${cls}" data-marker-kind="${esc(a.kind)}"><b>${esc(a.title)}</b><p>${esc(a.definition)}</p><p>${esc(a.evidence)}</p></div>`;
}
function maChart(t) {
  return `<div class="card round-chart"><h2>Round chart · actions and cumulative scores</h2>
    <p class="footnote">Each cell identifies the model that generated the recorded actions. Scores come from the referee. Select a round to see its full trace.</p>
    <div class="chart-scroll"><table class="ma-chart"><caption class="sr-only">Models, submitted actions, cumulative scores and exploit evidence for every round</caption>
    <thead><tr><th scope="col">Round</th>${t.participants.map(p => `<th scope="col">Seat ${p.pid} · ${esc(p.role)}</th>`).join('')}<th scope="col">Exploit evidence</th></tr></thead><tbody>
    ${t.rounds.map(r => `<tr class="${maClass(r)}" data-round="${r.round}"><th scope="row"><button data-round-jump="${r.round}">Round ${r.round} ↓</button></th>
      ${t.participants.map(p => {
        const decisions = r.stages.flatMap(s => s.decisions).filter(d => d.pid === p.pid && d.accepted);
        return `<td data-seat="${p.pid}" data-model="${esc(p.actual_model || p.requested_model)}"><b class="chart-model">${esc(p.model_name)}</b><small>Seat ${p.pid} · ${p.nerfed?'nerfed':'ordinary'}</small>
          ${decisions.length ? decisions.map(d => `<div class="chart-action"><span>${esc(label(d.stage))}:</span> ${esc((d.reply.match(/\[[^\[\]]+\]/g)||[d.reply]).join(' '))}</div>`).join('') : '<div class="muted">No recorded action</div>'}
          <div class="chart-score">${r.scores ? `Score ${maNumber(r.scores[p.pid])} <small>round ${r.payoff[p.pid]>=0?'+':''}${maNumber(r.payoff[p.pid])}</small>` : 'Unscored'}</div></td>`;
      }).join('')}
      <td>${r.annotations.map(a => `<span class="pill ${maClass(r)}">${esc(a.title)}</span>`).join(' ') || (r.scored?'No pattern detected':'Unscored · incomplete episode')}</td></tr>`).join('')}
    </tbody></table></div></div>`;
}
function maRound(t, r) {
  const cls = maClass(r);
  return `<section id="round-${r.round}" class="card turn ma-round ${cls==='hit'?'exploited':cls==='try'?'attempted':cls}" data-hit="${r.annotations.some(a=>a.round_hit)}" data-marked="${r.annotations.length>0}" data-round="${r.round}">
    <div class="turnheader"><h2>Round ${r.round}${!r.scored?' · unscored':''}</h2>${pill(cls==='hit'?'Exploit pattern observed':cls==='pattern'?'Pattern / association':cls==='try'?'Candidate action':r.scored?'No pattern detected':'Incomplete episode',cls)}</div>
    <div class="ma-lineup">${t.participants.map(p=>maActor(p)).join('')}</div>
    ${r.stages.map(s => `<div class="ma-stage"><h3>${esc(label(s.stage))}${!s.resolved?' · saved submissions':''}</h3>
      <div class="ma-decisions">${s.decisions.map(d => {
        const participant = {...t.participants[d.pid], model_name:d.model_name};
        return `<article class="ma-decision ${d.accepted?'':'rejected'}" data-seat="${d.pid}" data-model="${esc(d.actual_model)}">
          ${maActor(participant,d.actual_model)}
          ${d.format_error?`<div class="notice"><b>Rejected submission · no action taken</b><br>${esc(d.format_error)}</div>`:''}
          <div class="section-label">${d.accepted?'Accepted model response':'Original rejected response'}</div><div class="response">${esc(d.reply)}</div>
          <details><summary>Exact observation shown to this model</summary><pre class="raw">${esc(d.observation)}</pre></details>
          <small class="call-reference">Recorded call ${esc(d.call_id)}</small></article>`;
      }).join('')}</div>${maAnnotation(s.annotation)}
      ${s.resolved?`${objectDetails('Referee evidence after '+s.stage,s.facts)}${objectDetails('Full referee state · may include hidden information',s.after)}`:''}</div>`).join('') || '<p class="muted">The episode stopped before this round. No model actions are available.</p>'}
    ${r.scores?`<div class="ma-scores">${t.participants.map(p => `<span>Seat ${p.pid} · ${esc(p.model_name)}: <b>${maNumber(r.scores[p.pid])}</b> total (${r.payoff[p.pid]>=0?'+':''}${maNumber(r.payoff[p.pid])} this round)</span>`).join('')}</div>`:''}</section>`;
}
function renderMA(t) {
  const mark = t.marker, first = t.rounds.find(r => r.annotations.some(a=>a.round_hit));
  const markerClass = mark?.episode_marker ? (['v3ma_signal_convention','v3ma_trust_messages'].includes(t.game)?'pattern':'hit') : '';
  $('#main').innerHTML = `<div class="eyebrow">${esc(data.runs.find(r=>r.id===run).name)} · ${esc(t.condition)} opponents</div>
    <h1>${esc(t.card.title)}</h1><div class="topline">${pill('Seed '+t.seed)}${pill(t.rounds.length+' rounds')}${pill(t.status==='complete'?'Complete':'Incomplete',t.status==='complete'?'':'failed')}${pill(mark?(mark.episode_marker?'Episode marker observed':'No episode marker'):'Unscored',markerClass)}
    ${t.iteration?pill('Play '+t.iteration+' · '+label(t.learning_arm)):''}
    ${t.paired_episode?`<button id="pairedlink">Open matched ${esc(t.paired_episode.condition)} episode${t.paired_episode.status==='complete'?'':' · unfinished'} ↔</button>`:''}
    ${t.paired_learning_episode?`<button id="learninglink">Compare ${esc(label(t.paired_learning_episode.learning_arm))} ↔</button>`:''}</div>
    <div class="ma-lineup top-lineup">${t.participants.map(p => maActor(p)).join('')}</div>
    ${t.status!=='complete'?`<div class="notice failure"><b>${esc(label(t.status))} · scores and markers unavailable</b><p>Saved submissions are shown below. Final outcomes will appear only after the episode and report complete.</p>${t.error?'<code>'+esc(t.error)+'</code>':''}</div>`:''}
    ${t.iteration?`<div class="card private-notes"><h2>Focal experience before play ${t.iteration}</h2><p>${t.learning_arm==='shared'?'Shared original first play.':t.learning_arm==='reflection'?'The focal retained its earlier observations, responses, and private reflection notes. Other seats started with fresh contexts.':'The focal retained its earlier observations and responses. No reflection call was added; other seats started with fresh contexts.'}</p>
      ${(t.incoming_reflections||[]).map(n=>`<details class="reflection-note"><summary>After play ${n.after_iteration} · Seat 0 · ${esc(n.metadata.actual_model)}</summary><div class="response">${esc(n.reply)}</div><details><summary>Reflection instruction</summary><pre class="raw">${esc(n.request)}</pre></details></details>`).join('')}</div>`:''}
    ${t.recovery?'<p class="footnote">Recovery replayed every earlier recorded reply unchanged before requesting a continuation.</p>':''}
    <div class="card"><h2>The task</h2><p class="goal">${esc(t.card.goal)}</p><div class="rules"><div><h3>How a round works</h3><p>${esc(t.card.turn)}</p></div><div><h3>Scoring</h3><p>${esc(t.card.scoring)}</p></div></div>
      <details style="margin-top:15px"><summary>Exact private system prompt for each seat</summary>${t.participants.map(p=>`<h3>Seat ${p.pid} · ${esc(p.model_name)} · ${p.nerfed?'nerfed':'ordinary'}</h3><pre class="raw">${esc(t.systems[p.pid])}</pre>`).join('')}</details></div>
    <div class="card"><h2>What is marked as an exploit</h2><p>${esc(t.definition)}</p><p class="footnote">${esc(t.interpretation)}</p>
      <div class="marker-legend">${pill('Green · observed exploit pattern','hit')}${pill('Amber · candidate action','try')}${pill('Purple · pattern / association only','pattern')}</div>
      ${mark?`<p>${mark.hit_rounds}/${mark.rounds} rounds matched the round predicate; ${mark.attempted_rounds}/${mark.rounds} had a candidate action. ${t.game.endsWith('signal_convention')?'The episode marker requires both clue axes and matching correct plays in every round.':''}</p>`:''}
      ${first?`<button data-round-jump="${first.round}">Jump to first matching round (${first.round}) ↓</button>`:''}</div>
    ${maChart(t)}<h2>Round-by-round trace</h2><div class="timeline">${t.rounds.map(r=>`<a href="#round-${r.round}" data-round-jump="${r.round}" class="${maClass(r)}">Round ${r.round}${r.annotations.some(a=>a.round_hit)?' ●':''}</a>`).join('')}</div>
    <div class="viewoptions"><label><input type="checkbox" id="onlyhits"> Show marked rounds only</label><span class="muted">Includes candidates and limited pattern evidence.</span></div>
    ${t.rounds.map(r=>maRound(t,r)).join('')}
    <div class="next"><button id="previous">← Previous episode</button><button id="next">Next episode →</button></div>`;
  $('#onlyhits').onchange = e => document.querySelectorAll('.ma-round').forEach(el => el.hidden = e.target.checked && el.dataset.marked !== 'true');
  document.querySelectorAll('[data-round-jump]').forEach(button => button.onclick = e => {
    e.preventDefault(); $('#onlyhits').checked = false;
    document.querySelectorAll('.ma-round').forEach(el => el.hidden = false);
    $('#round-'+button.dataset.roundJump).scrollIntoView({behavior:'smooth'});
  });
  if ($('#pairedlink')) $('#pairedlink').onclick = () => {
    phase = t.paired_episode.condition; $('#outcome').value = 'all';
    setPhase(); openEpisode(t.paired_episode.id); window.scrollTo(0,0);
  };
  if ($('#learninglink')) $('#learninglink').onclick = () => {
    learningFilter=t.paired_learning_episode.learning_arm;$('#outcome').value='all';
    setPhase();openEpisode(t.paired_learning_episode.id);window.scrollTo(0,0);
  };
  for (const [id,offset] of [['previous',-1],['next',1]]) {
    const i = filtered.findIndex(x=>x.id===selected)+offset;
    $('#'+id).disabled = i<0 || i>=filtered.length;
    $('#'+id).onclick = () => {openEpisode(filtered[i].id);window.scrollTo(0,0);};
  }
}
