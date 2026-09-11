/* All strings from recorded data are escaped before HTML rendering. */
const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels = {action0:'Canonical action 0',cooperation:'Mutual cooperation',coordination:'Coordination'};
const methods = {context:'Ordered context',family:'Family mean',nash:'Original Nash',payoff_dominant:'Payoff-dominant theory',calibrated_payoff_dominant:'Calibrated theory',normalized_logistic:'Normalized logistic',combined_logistic:'Combined logistic',qwen3_frozen_head:'Qwen frozen head',qwen3_lora_head:'Qwen LoRA head',llm_few_shot:'Kimi few-shot'};
const short = value => ({'claude-haiku-4.5':'Haiku 4.5','kimi-k3':'Kimi K3','qwen-3.8-27b':'Qwen 3.8 27B','gpt-oss-20b':'GPT-OSS 20B'}[value] || value);
const human = value => String(value).replaceAll('_',' ').replace(/\b\w/g,c=>c.toUpperCase());
const percent = value => value == null ? 'N/A' : `${(value*100).toFixed(1)}%`;
const number = value => Number(value).toLocaleString(undefined,{maximumFractionDigits:4});
const foldName = value => value === 'full' ? 'Full training → development' : value.startsWith('family_') ? `Held-out family · ${human(value.slice(7))}` : human(value);
const state = {catalog:null,filtered:[],page:0,size:40,id:null,detail:null,tab:'input',episode:null,round:1,fold:null,contexts:new Map(),episodes:new Map(),request:0};

async function get(url) {
  const response = await fetch(url);
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || `Request failed (${response.status})`);
  return result;
}
function notify(message) {
  $('toast').textContent = message; $('toast').hidden=false;
  clearTimeout(notify.timer); notify.timer=setTimeout(()=>$('toast').hidden=true,2600);
}
function setHash(values) {
  const params=new URLSearchParams();
  Object.entries(values).forEach(([k,v])=>{if(v!=null && v!=='')params.set(k,String(v));});
  const hash=params.toString();
  if(location.hash.slice(1)===hash)navigate(); else location.hash=hash;
}
function choose(id) {setHash({context:id,tab:state.tab});}
function updateLocation(extra={}) {setHash({context:state.id,tab:state.tab,episode:state.episode,round:state.round,...extra});}

function applyFilters(reset=true) {
  if(reset)state.page=0;
  const q=$('search').value.trim().toLowerCase();
  const filters=['partition','family','model','opponent'].map(k=>[k,$(k).value]);
  state.filtered=state.catalog.examples.filter(row=>filters.every(([k,v])=>!v||row[k]===v) && (!q||`${row.game_id} ${row.family} ${row.model} ${row.opponent} ${JSON.stringify(row.payoffs)}`.toLowerCase().includes(q)));
  if(state.filtered.length && !state.filtered.some(r=>r.row_id===state.id))choose(state.filtered[0].row_id);
  renderList();
  if(!state.filtered.length)$('main').innerHTML='<div class="empty">No contexts match these filters. Try another model or reset the filters.</div>';
  else if(state.detail?.row_id===state.id && state.filtered.some(r=>r.row_id===state.id))renderMain();
}
function renderList() {
  const pages=Math.max(1,Math.ceil(state.filtered.length/state.size));
  state.page=Math.max(0,Math.min(state.page,pages-1));
  $('matches').textContent=`${state.filtered.length.toLocaleString()} contexts`;
  $('page').textContent=`${state.page+1} / ${pages}`;
  $('previous').disabled=state.page===0; $('next').disabled=state.page>=pages-1;
  $('context-list').innerHTML=state.filtered.slice(state.page*state.size,(state.page+1)*state.size).map(row=>
    `<button class="context-item ${row.row_id===state.id?'selected':''}" data-context="${esc(row.row_id)}" aria-pressed="${row.row_id===state.id}"><span class="row"><span class="game">${esc(row.game_id)}</span><span class="rate">${percent(row.rates.action0)}</span></span><span class="pair">${esc(short(row.model))} → ${esc(short(row.opponent))}</span><span class="row family"><span>${esc(human(row.family))}</span><span>${row.partition==='train'?'Training':'Development'} · ${row.episodes} matches</span></span></button>`).join('');
  $('context-list').querySelectorAll('[data-context]').forEach(button=>button.onclick=()=>choose(button.dataset.context));
}
async function navigate() {
  if(!state.catalog)return;
  const p=new URLSearchParams(location.hash.slice(1));
  const id=p.get('context') || state.filtered[0]?.row_id || state.catalog.examples[0].row_id;
  if(!state.catalog.examples.some(r=>r.row_id===id)) {$('main').innerHTML='<div class="empty error">Unknown context in this link.</div>';return;}
  const changed=state.id!==id;
  state.id=id;
  state.tab=['input','targets','traces'].includes(p.get('tab'))?p.get('tab'):'input';
  state.episode=p.get('episode');state.round=Math.max(1,Math.min(8,Math.trunc(Number(p.get('round')))||1));
  if(changed)state.fold=null;
  const index=state.filtered.findIndex(row=>row.row_id===id);
  if(index>=0)state.page=Math.floor(index/state.size);
  renderList();
  const ticket=++state.request;
  try {
    if(!state.contexts.has(id)) {
      $('main').innerHTML='<div class="empty">Loading context…</div>';
      state.contexts.set(id,await get(`/api/context?id=${encodeURIComponent(id)}`));
    }
    if(ticket!==state.request)return;
    state.detail=state.contexts.get(id);renderMain();
  } catch(error) {if(ticket===state.request)$('main').innerHTML=`<div class="empty error">${esc(error.message)}</div>`;}
}
function metricCards(d) {
  return `<div class="cards">${state.catalog.targets.map(t=>{const x=d.targets[t];return `<div class="metric"><div class="metric-name">${labels[t]}</div><div class="metric-value">${percent(x.value)}</div><p class="metric-note">${x.opportunities?`${x.successes} / ${x.opportunities} observed events`:'Undefined for this payoff table'}</p></div>`;}).join('')}</div>`;
}
function renderMain() {
  const d=state.detail;
  $('main').innerHTML=`<div class="detail-head"><div><p class="eyebrow">${esc(human(d.family))} &nbsp; / &nbsp; <span class="tag ${d.partition}">${d.partition==='train'?'TRAINING':'DEVELOPMENT'}</span></p><h2>${esc(d.game_id)}</h2><p class="subline">${esc(short(d.model))} <span class="muted">→</span> ${esc(short(d.opponent))} &nbsp; · &nbsp; ${d.episodes.length} matches · ${d.source_focal_rows} focal records</p></div><div class="actions"><button id="copy-link" class="quiet">Copy link</button><button id="export" class="quiet">Export context ↓</button></div></div>${metricCards(d)}
    <div class="tabs" role="tablist" aria-label="Context detail"><button class="tab ${state.tab==='input'?'active':''}" role="tab" aria-selected="${state.tab==='input'}" data-tab="input">Predictor input</button><button class="tab ${state.tab==='targets'?'active':''}" role="tab" aria-selected="${state.tab==='targets'}" data-tab="targets">Targets &amp; forecasts</button><button class="tab ${state.tab==='traces'?'active':''}" role="tab" aria-selected="${state.tab==='traces'}" data-tab="traces">Player inputs &amp; outputs</button></div><div id="tab-content"></div>`;
  document.querySelectorAll('[data-tab]').forEach(button=>button.onclick=()=>updateLocation({tab:button.dataset.tab}));
  $('copy-link').onclick=async()=>{try{await navigator.clipboard.writeText(location.href);notify('Link copied');}catch{notify('Copy the URL from the address bar');}};
  $('export').onclick=()=>{const blob=new Blob([JSON.stringify(d,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`${d.game_id}-${short(d.model).replaceAll(' ','_')}-context.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
  if(state.tab==='input')renderInput(d);else if(state.tab==='targets')renderTargets(d);else renderTraces(d);
}
function renderInput(d) {
  const p=d.payoffs;
  $('tab-content').innerHTML=`<div class="input-layout"><section class="panel"><div class="panel-title"><h3>Exact predictor input text</h3><button class="quiet" id="copy-input">Copy input</button></div><pre class="prompt">${esc(d.input_text)}</pre><p class="footnote">Stored text supplied as the user message to Qwen's chat template, with thinking disabled. This context averages the two player-visible A/B label orientations.</p></section><section class="panel"><h3>Canonical payoffs</h3><p class="footnote">Each cell: (row player's points, column player's points).</p><table class="payoff"><thead><tr><th>Row / Col</th><th>0</th><th>1</th></tr></thead><tbody><tr><th>0</th><td class="diag">${number(p.R)}, ${number(p.R)}</td><td>${number(p.S)}, ${number(p.T)}</td></tr><tr><th>1</th><td>${number(p.T)}, ${number(p.S)}</td><td class="diag">${number(p.P)}, ${number(p.P)}</td></tr></tbody></table><div class="key-value"><span>Rounds</span><span>${d.protocol.rounds}</span></div><div class="key-value"><span>Temperature</span><span>${d.protocol.temperature}</span></div><div class="key-value"><span>History</span><span>Complete public</span></div><div class="key-value"><span>Objective</span><span>Own total points</span></div><p class="footnote">The player tab shows the exact A/B prompts and outputs for each recorded match.</p></section></div><section class="panel"><h3>What the output labels measure</h3><div class="definitions"><div><p class="footnote"><b>Canonical action 0</b><br>How often the focal player chose canonical action 0.</p></div><div><p class="footnote"><b>Mutual cooperation</b><br>How often both players chose the unique welfare-maximizing symmetric action, where defined.</p></div><div><p class="footnote"><b>Coordination</b><br>How often play reached a strict pure equilibrium when multiple such outcomes exist.</p></div></div><p class="pill-note">Labels pool ${d.episodes.length} matches and ${d.source_focal_rows} focal records. ${d.model===d.opponent?'Both seats of each self-play match contribute to this context.':'The selected model supplies the focal observations.'} These pooled records share matches and are statistically dependent.</p></section>`;
  $('copy-input').onclick=async()=>{try{await navigator.clipboard.writeText(d.input_text);notify('Input copied');}catch{notify('Select and copy the input text');}};
}
function renderTargets(d) {
  const folds=[...new Set(d.forecasts.map(p=>p.fold_id))];
  if(!folds.includes(state.fold))state.fold=folds.find(f=>f==='full'||f.startsWith('family_'))||folds[0];
  const grouped=new Map();
  d.forecasts.filter(p=>p.fold_id===state.fold).forEach(p=>{if(!grouped.has(p.method))grouped.set(p.method,{});grouped.get(p.method)[p.target]=p.prediction;});
  const ordered=Object.keys(methods).filter(m=>grouped.has(m));
  const rows=ordered.map(method=>`<tr><td>${esc(methods[method])}</td>${state.catalog.targets.map(t=>{const p=grouped.get(method)[t],y=d.targets[t].value;return `<td><span class="predicted">${percent(p)}</span>${p!=null&&y!=null?`<span class="delta">${p-y>=0?'+':''}${((p-y)*100).toFixed(1)} pp</span>`:''}</td>`;}).join('')}</tr>`).join('');
  $('tab-content').innerHTML=`<section class="panel"><div class="panel-title"><h3>Observed targets and saved forecasts</h3><select class="fold-select" id="fold" aria-label="Prediction fold">${folds.map(f=>`<option value="${esc(f)}" ${f===state.fold?'selected':''}>${esc(foldName(f))}</option>`).join('')}</select></div><div class="table-wrap"><table class="data-table"><thead><tr><th>Predictor</th>${state.catalog.targets.map(t=>`<th>${labels[t]}</th>`).join('')}</tr></thead><tbody><tr class="observed"><td>Observed frequency</td>${state.catalog.targets.map(t=>`<td>${percent(d.targets[t].value)}</td>`).join('')}</tr>${rows}</tbody></table></div><p class="footnote">Each listed forecast was evaluated with this context held out of that fit. Differences are prediction minus observed rate in percentage points. N/A means the target is structurally undefined or the fit had no support.</p></section><section class="panel"><h3>Supervised output arrays</h3><p class="footnote">Order: action 0, mutual cooperation, coordination. The training loss uses success/opportunity counts and masks undefined targets.</p><pre class="prompt">${esc(JSON.stringify({targets:state.catalog.targets,rates:state.catalog.targets.map(t=>d.targets[t].value),successes:d.successes,opportunities:d.opportunities,mask:d.mask},null,2))}</pre></section><section class="panel"><h3>Fold membership</h3><div class="table-wrap"><table class="data-table"><thead><tr><th>Fit</th><th>This context's role</th></tr></thead><tbody>${d.folds.map(f=>`<tr><td>${esc(foldName(f.fold_id))}</td><td>${f.role==='train'?'Training':'Held-out evaluation'}</td></tr>`).join('')}</tbody></table></div></section>`;
  $('fold').onchange=()=>{state.fold=$('fold').value;renderTargets(d);};
}
async function renderTraces(d) {
  const episodes=[...d.episodes].sort((a,b)=>a.trial_id-b.trial_id);
  if(!episodes.some(e=>e.id===state.episode))state.episode=episodes[0]?.id;
  $('tab-content').innerHTML=`<section class="panel"><div class="episode-toolbar"><h3>Recorded matches</h3><select id="episode" aria-label="Recorded match">${episodes.map((e,i)=>`<option value="${esc(e.id)}" ${e.id===state.episode?'selected':''}>Match ${i+1} · trial ${e.trial_id} · ${e.swap?'A = canonical 1':'A = canonical 0'}</option>`).join('')}</select></div><p class="small">Inspect both players' exact input messages and returned action at each round.</p><div id="trace-body" class="small">Loading recorded decisions…</div></section>`;
  $('episode').onchange=()=>updateLocation({episode:$('episode').value,round:1});
  const id=state.id,eid=state.episode,key=`${id}:${eid}`;
  try {
    if(!state.episodes.has(key))state.episodes.set(key,await get(`/api/episode?context=${encodeURIComponent(id)}&id=${encodeURIComponent(eid)}`));
    if(state.id!==id||state.episode!==eid||state.tab!=='traces')return;
    renderEpisode(state.episodes.get(key));
  } catch(error) {if($('trace-body'))$('trace-body').innerHTML=`<p class="error">${esc(error.message)}</p>`;}
}
function renderEpisode(e) {
  const event=e.rounds[state.round-1];
  const totals=[0,1].map(seat=>e.rounds.reduce((s,r)=>s+r.payoffs[seat],0));
  $('trace-body').innerHTML=`<div class="key-value"><span>${esc(short(e.models[0]))} · seat 1</span><span>${number(totals[0])} total points</span></div><div class="key-value"><span>${esc(short(e.models[1]))} · seat 2</span><span>${number(totals[1])} total points</span></div><div class="rounds" aria-label="Select round">${e.rounds.map(r=>`<button class="round-button ${r.round===state.round?'active':''}" data-round="${r.round}" aria-label="Round ${r.round}"><span>ROUND ${r.round}</span><b>${r.decisions[0].displayed_action} / ${r.decisions[1].displayed_action}</b><small>${number(r.payoffs[0])} / ${number(r.payoffs[1])}</small></button>`).join('')}</div><p class="footnote">Round ${state.round} of ${e.rounds.length}. Buttons show the two displayed actions and round payoffs, in seat order. ${e.swap?'Displayed A = canonical 1; B = canonical 0.':'Displayed A = canonical 0; B = canonical 1.'}</p><div class="decisions">${event.decisions.map((decision,seat)=>{
    const final=decision.attempts.at(-1);const system=decision.messages.filter(m=>m.role==='system');const others=decision.messages.filter(m=>m.role!=='system');
    return `<section class="decision"><div class="panel-title"><div><p class="role-label">SEAT ${seat+1} · ${decision.context_focal?'FOCAL OBSERVATIONS':'OPPONENT'}</p><h3>${esc(short(decision.model))}</h3></div></div><div class="response"><b>${esc(final.reply)}</b><span>Recorded model output<br>Canonical action ${decision.canonical_action} · ${number(event.payoffs[seat])} points</span></div><div class="small">Exact player input · round ${state.round}</div>${system.map(m=>`<details><summary>System message</summary><pre class="prompt">${esc(m.content)}</pre></details>`).join('')}${others.map(m=>`<pre class="prompt">${esc(m.content)}</pre>`).join('')}<p class="footnote">Provider model: ${esc(final.actual_model||decision.model)}<br>Finish: ${esc(final.finish_reason||'not recorded')} · ${decision.attempts.length} attempt${decision.attempts.length===1?'':'s'}</p>${decision.attempts.length>1?`<details><summary>All recorded attempts</summary><pre class="prompt">${esc(JSON.stringify(decision.attempts,null,2))}</pre></details>`:''}</section>`;
  }).join('')}</div><details><summary>Match identifier and recorded timing</summary><pre class="prompt">${esc(JSON.stringify({episode:e.id,source_stage:e.source_stage,started:e.started,finished:e.finished},null,2))}</pre></details>`;
  document.querySelectorAll('[data-round]').forEach(button=>button.onclick=()=>updateLocation({round:button.dataset.round}));
}
async function init() {
  try {
    state.catalog=await get('/api/catalog');
    const c=state.catalog.counts;$('counts').textContent=`${c.contexts.toLocaleString()} contexts · ${c.games} games · ${c.episodes.toLocaleString()} matches`;
    state.catalog.families.forEach(f=>$('family').add(new Option(human(f),f)));
    state.catalog.models.forEach(m=>['model','opponent'].forEach(k=>$(k).add(new Option(short(m),m))));
    ['partition','family','model','opponent'].forEach(k=>$(k).onchange=()=>applyFilters());
    $('search').oninput=()=>applyFilters();
    $('reset').onclick=()=>{['search','partition','family','model','opponent'].forEach(k=>$(k).value='');applyFilters();};
    $('previous').onclick=()=>{state.page--;renderList();$('context-list').scrollTop=0;};
    $('next').onclick=()=>{state.page++;renderList();$('context-list').scrollTop=0;};
    state.filtered=state.catalog.examples;
    addEventListener('hashchange',navigate);
    await navigate();
  } catch(error) {$('counts').textContent='Dataset could not be loaded';$('main').innerHTML=`<div class="empty error">${esc(error.message)}</div>`;}
}
init();
