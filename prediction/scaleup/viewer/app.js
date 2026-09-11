const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=n=>Number(n).toLocaleString(), pct=n=>n===null?'Unknown':`${Math.round(n*100)}%`;
const pretty=v=>esc(JSON.stringify(v,null,2));
let summary=null, catalog=null, selected=null, trace=null, episodeId='', turn=0, offset=0, detailTab='rules', request=0, detailRequest=0;
async function api(path,args={}){const response=await fetch(path+'?'+new URLSearchParams(args));if(!response.ok)throw Error((await response.json()).error);return response.json()}
function toast(message){$('#toast').textContent=message;$('#toast').hidden=false;setTimeout(()=>$('#toast').hidden=true,5000)}
function nice(s){return s.replaceAll('_',' ')}
function page(name){$$('[data-page]').forEach(b=>b.classList.toggle('active',b.dataset.page===name));$('#overview').hidden=name!=='overview';$('#samples').hidden=name!=='samples';if(name==='samples'&&!catalog)loadCatalog().catch(e=>toast(e.message))}
function saveHash(){const p=new URLSearchParams({page:$('#samples').hidden?'overview':'samples'});if($('#family').value)p.set('family',$('#family').value);if(selected)p.set('game',selected.game.game_id);if(episodeId)p.set('episode',episodeId);if(detailTab)p.set('tab',detailTab);p.set('turn',String(turn+1));history.replaceState(null,'','#'+p)}
function barChart(element,rows){
 if(!rows.length){element.innerHTML='<div class="empty">No observations in this selection yet.</div>';return}
 const width=480,height=190,left=30,right=8,top=24,bottom=34,plot=height-top-bottom,max=Math.max(...rows.map(r=>r.count),1),step=(width-left-right)/rows.length,bw=Math.min(54,step*.6);
 const grid=[0,.5,1].map(f=>`<line class="gridline" x1="${left}" x2="${width-right}" y1="${top+plot*(1-f)}" y2="${top+plot*(1-f)}"/><text x="${left-6}" y="${top+plot*(1-f)+4}" text-anchor="end">${Math.round(max*f)}</text>`).join('');
 element.innerHTML=`<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Distribution with ${rows.length} bins">${grid}${rows.map((r,i)=>{const h=r.count/max*plot,x=left+(i+.5)*step;return `<g><rect class="bar" x="${x-bw/2}" y="${top+plot-h}" width="${bw}" height="${h}" rx="3"><title>${esc(r.value)}: ${r.count}</title></rect><text class="value-label" text-anchor="middle" x="${x}" y="${top+plot-h-7}">${fmt(r.count)}</text><text text-anchor="middle" x="${x}" y="${height-12}">${esc(r.value)}</text></g>`}).join('')}</svg>`;
}
function renderDose(){const name=$('#parameter').value;barChart($('#dose-chart'),summary.parameters[name]||[]);$('#dose-note').textContent=name==='reward'?'Reward is a family-specific payment or effect magnitude. Select one family before interpreting it as a common dose.':`Each bar counts generated base instances with this ${nice(name)} value. Controls are counted in the coverage chart separately.`}
function renderSummary(data){
 summary=data;const c=data.counts;
 $('#live-status').textContent=`${c.complete} / ${c.planned} episodes collected${data.blocker?" · provider blocked":""}`;
 $('#metrics').innerHTML=[['Playable instances',fmt(c.games),`${fmt(c.base)} base + ${fmt(c.controlled)} controls`],['Game families',fmt(c.families),`${c.mechanisms} mechanism categories`],['Counterfactual pairs',fmt(c.counterfactual_pairs),'One parameter or one intervention'],['Live model episodes',fmt(c.complete),`${c.planned} planned · ${c.incomplete} incomplete`],['Recorded decisions',fmt(c.observed_actions),$('#family').value?'In the selected family':'Completed model trajectories']].map((m,i)=>`<div class="metric ${i===3?'live-metric':''}"><div class="metric-number">${m[1]}</div><div class="metric-label">${m[0]}</div><div class="metric-sub">${m[2]}</div></div>`).join('');
 const current=$('#family').value;
 if($('#family').options.length===1){$('#family').innerHTML='<option value="">All 24 families</option>'+data.families.map(f=>`<option value="${esc(f.id)}">${esc(f.title)}</option>`).join('');$('#family').value=current}
 const max=Math.max(...data.families.map(f=>f.base+f.controlled));
 $('#family-chart').innerHTML=data.families.map(f=>`<button class="family-row ${current===f.id?'selected':''}" data-family="${esc(f.id)}" title="${esc(f.mechanism||'Ordinary strategic game')}"><span class="family-label">${esc(f.title)}</span><span class="family-track"><span class="base" style="width:${100*f.base/max}%"></span><span class="control" style="width:${100*f.controlled/max}%"></span></span><span class="family-count">${f.base+f.controlled}</span></button>`).join('');
 const oldParam=$('#parameter').value;$('#parameter').innerHTML=Object.keys(data.parameters).map(p=>`<option value="${esc(p)}">${esc(nice(p))}</option>`).join('');$('#parameter').value=data.parameters[oldParam]?oldParam:data.parameters.reward?'reward':Object.keys(data.parameters)[0];renderDose();
 const labels={random_group:'Random intervention group',held_out_construction:'Held-out construction',held_out_family:'Held-out family',held_out_mechanism:'Held-out mechanism',parameter_interpolation:'Unseen reward · interpolation',parameter_extrapolation:'Unseen reward · extrapolation'};
 $('#splits').innerHTML=Object.entries(data.splits).map(([name,v])=>{const n=Object.values(v).reduce((a,b)=>a+b,0);return `<div class="split-row"><label>${labels[name]}<span>${fmt(n)} games</span></label><div class="split-track">${['train','validation','test'].map((p,i)=>`<span class="${['base','validation','test'][i]}" style="width:${100*(v[p]||0)/n}%" title="${p}: ${fmt(v[p]||0)}"></span>`).join('')}</div></div>`}).join('');
 $('#collection-note').textContent=`${fmt(c.selected_episodes)} completed model episodes in this view. ${c.incomplete} incomplete and ${c.not_started} not started across the pilot. The ${c.fixtures} saved scripted witness samples are available in the explorer and are excluded from every behavior plot.${data.continuation?` Provider switch: ${data.continuation.retained} completed FLT episodes retained; ${data.continuation.restarted} restarted through OpenRouter. Provider assignment was not randomized.`:''}${data.blocker?" Collection paused: the hosted provider returns HTTP 403. Partial coverage is unbalanced; do not use these counts to rank models.":""}`;
 const targets=['cooperation_rate','defection_rate','exploitation_rate','information_seeking_rate','communication_rate','sacrifice_rate'];
 $('#behavior-table').innerHTML=data.models.length?`<table><thead><tr><th>Model / episodes</th>${targets.map(t=>`<th>${esc(nice(t.replace('_rate','')).replace('information seeking','Info. seeking'))}</th>`).join('')}</tr></thead><tbody>${data.models.map(m=>`<tr><td>${esc(m.model)}<span class="denom">${m.episodes} episodes</span></td>${targets.map(t=>{const x=m.behaviors[t];return `<td><span class="rate" title="${x.numerator} tagged actions / ${x.denominator} supported decisions">${pct(x.value)}</span><span class="denom">${x.denominator?`${x.numerator} / ${x.denominator}`:'not measured'}</span></td>`}).join('')}</tr>`).join('')}</tbody></table>`:'<div class="empty">Live behavior will appear as episodes complete.</div>';
 $('#condition-chart').innerHTML=data.conditions.length?data.conditions.map(r=>`<div class="condition-row ${r.control?'controlled':''}"><label><strong>${esc(r.model)} · ${r.prompt==='normal'?'normal':'exploration'}</strong>${r.control?'paired control':'base game'}</label><div class="condition-track"><div class="condition-fill" style="width:${100*r.executions/r.episodes}%"></div></div><span>${r.executions}/${r.episodes}</span></div>`).join(''):'<div class="empty">No supported mechanism episodes in this selection.</div>';
 const maxAction=Math.max(...data.actions.map(a=>a.count),1);
 $('#action-chart').innerHTML=data.actions.length?data.actions.map(a=>`<div class="condition-row"><span>${esc(a.action)}</span><div class="condition-track"><div class="condition-fill" style="width:${100*a.count/maxAction}%"></div></div><span>${a.count}</span></div>`).join(''):'<div class="empty">No model actions recorded in this view.</div>';
 barChart($('#score-chart'),data.scores);$('#notes').innerHTML=data.notes.map(n=>`<li>${esc(n)}</li>`).join('')+`<li>Validation: ${fmt(data.validation.replayed_scripted_episodes)} scripted episodes replayed; ${fmt(data.validation.replayed_transitions)} transitions checked.</li>`;
}
async function loadAssessment(){
 const element=$('#assessment-section');if($('#family').value){element.hidden=true;return}
 const data=await api('/api/assessment');element.hidden=!data.cards;if(!data.cards)return;
 $('#assessment-scope').textContent=data.scope;
 $('#assessment-cards').innerHTML=data.cards.map(c=>`<article class="card"><h3>${esc(c.question)}</h3><p class="assessment-verdict">${esc(c.verdict)}</p><p>${esc(c.detail)}</p></article>`).join('');
 $('#assessment-scores').innerHTML=`<table><thead><tr><th>Predictor</th><th>Non-work rate MSE</th><th>First-action Brier</th></tr></thead><tbody>${data.scores.map(r=>`<tr><td>${esc(r.name)}</td><td>${r.non_work_mse.toFixed(4)}</td><td>${r.first_action_brier.toFixed(4)}</td></tr>`).join('')}</tbody></table>`;
}
async function refresh(){const family=$('#family').value;renderSummary(await api('/api/summary',{family}));await loadAssessment();if(!$('#samples').hidden)await loadCatalog(false)}
async function focusFamily(fid){$('#family').value=fid;offset=0;await refresh();if(!$('#samples').hidden&&catalog?.rows.length&&!catalog.rows.some(r=>r.game_id===selected?.game.game_id))await selectGame(catalog.rows[0].game_id);saveHash()}
async function loadCatalog(choose=true){
 const token=++request;++detailRequest;const data=await api('/api/games',{family:$('#family').value,q:$('#search').value,layer:$('#layer').value,offset});if(token!==request)return;catalog=data;
 $('#matches').textContent=`${fmt(data.total)} games`;$('#page-count').textContent=data.total?`${offset+1}–${Math.min(offset+12,data.total)}`:'0';$('#prev').disabled=offset===0;$('#next').disabled=offset+12>=data.total;
 $('#game-list').innerHTML=data.rows.length?data.rows.map(g=>`<button class="game-row ${selected?.game.game_id===g.game_id?'selected':''}" data-game="${esc(g.game_id)}"><span class="game-title">${esc(g.title)}<span class="mini-tag">${g.control?'CONTROL':'BASE'}</span></span><div class="game-meta">reward ${g.parameters.reward} · horizon ${g.parameters.horizon} · ${g.axis?esc(nice(g.axis))+' variant':'anchor'}<br><span class="${g.episodes?'recorded':''}">${g.episodes?`${g.episodes} live episodes`:g.fixtures?`${g.fixtures} scripted witnesses`:'Instance definition'}</span></div></button>`).join(''):'<div class="empty">No games match these filters.</div>';
 if(choose&&data.rows.length&&!data.rows.some(r=>r.game_id===selected?.game.game_id))await selectGame(data.rows[0].game_id);
 if(!data.rows.length){selected=null;$('#sample-detail').innerHTML='<div class="empty">No samples match. Change the search or family filter.</div>'}
}
async function selectGame(id,restoreEpisode='',restoreTurn=0){const token=++detailRequest;const data=await api('/api/game',{id});if(token!==detailRequest)return;selected=data;trace=null;episodeId=restoreEpisode;turn=restoreTurn;$$('.game-row').forEach(b=>b.classList.toggle('selected',b.dataset.game===id));renderDetail();if(detailTab==='trajectory')await loadEpisode(restoreEpisode);saveHash()}
function renderDetail(){
 if(!selected)return;const g=selected.game,f=selected.family;
 $('#sample-detail').innerHTML=`<div class="detail-top"><div><p class="eyebrow">${g.control?'PAIRED CONTROL':'BASE GAME'} / ${esc(f.role)}</p><h2>${esc(f.title)}</h2></div><button id="download" class="quiet json-button">Export sample ↓</button></div><p class="detail-id">${esc(g.game_id)}</p><div class="detail-meta"><span class="badge">${esc(nice(f.mechanism_kind))}</span><span class="badge">${selected.episodes.filter(e=>e.source==='model_rollout'&&e.status==='complete').length} live episodes</span><span class="badge fixture">${selected.episodes.filter(e=>e.source==='scripted_fixture').length} witness samples</span></div><div class="pills">${Object.entries(g.parameters).map(([k,v])=>`<span class="pill">${esc(nice(k))} <b>${v}</b></span>`).join('')}</div><div class="detail-tabs"><button class="detail-tab ${detailTab==='rules'?'active':''}" data-detail="rules">Rules & structure</button><button class="detail-tab ${detailTab==='trajectory'?'active':''}" data-detail="trajectory">Trajectory samples</button><button class="detail-tab ${detailTab==='pairs'?'active':''}" data-detail="pairs">Pairs & splits</button></div><div id="detail-content"></div>`;
 renderDetailContent();
}
function renderDetailContent(){
 const g=selected.game;
 if(detailTab==='rules')$('#detail-content').innerHTML=`<div class="rules">${esc(g.natural_language)}</div><details><summary>Structured representation</summary><pre>${pretty(g.structured)}</pre></details><details><summary>Research annotations · withheld from player prompts</summary><pre>${pretty(g.research_only)}</pre></details>`;
 if(detailTab==='pairs')$('#detail-content').innerHTML=`<h3>Matched interventions</h3><p class="footnote">Each link changes one parameter or one control condition. Seed, construction, and episode assignments are matched.</p>${selected.pairs.map(p=>{const other=p.a===g.game_id?p.b:p.a;return `<button class="pair-link" data-pair="${esc(other)}">${esc(nice(p.axis))}: ${esc(p.a_value)} → ${esc(p.b_value)} <span class="muted">· ${esc(nice(p.intervention_kind))}</span> ↗</button>`}).join('')}<details open><summary>Evaluation memberships</summary><pre>${pretty(selected.splits)}</pre></details>`;
 if(detailTab==='trajectory'){
  if(!selected.episodes.length){$('#detail-content').innerHTML='<div class="empty">This is a generated game instance. No live episode or saved canonical witness has been collected for this exact variant. Try an anchor or a game with a live-episode count in the list.</div>';return}
  const chosen=selected.episodes.some(e=>e.id===episodeId)?episodeId:selected.episodes[0].id;
  $('#detail-content').innerHTML=`<div class="episode-toolbar"><select id="episode" aria-label="Recorded episode">${selected.episodes.map(e=>`<option value="${esc(e.id)}">${e.source==='scripted_fixture'?'SCRIPTED WITNESS':esc(e.model)} · ${esc(nice(e.prompt))} · trial ${e.trial} · ${e.status}</option>`).join('')}</select></div><div id="episode-content"><div class="empty">Loading recorded trajectory…</div></div>`;$('#episode').value=chosen;
 }
}
async function loadEpisode(id=''){
 if(!selected?.episodes.length)return;
 episodeId=selected.episodes.some(e=>e.id===id)?id:selected.episodes[0].id;
 trace=await api('/api/episode',{id:episodeId});turn=Math.min(turn,Math.max(0,trace.steps.length-1));$('#episode').value=episodeId;renderEpisode();saveHash();
}
function renderEpisode(){
 const t=trace,scripted=t.provenance==='scripted_fixture',ep=t.episode,out=t.outcome,ex=t.exploit;
 $('#episode-content').innerHTML=`<div class="notice"><span class="badge ${scripted?'fixture':'live'}">${scripted?'SCRIPTED WITNESS · NOT MODEL DATA':'RECORDED MODEL EPISODE'}</span><br>${scripted?'This policy demonstrates a reachable mechanism. It is not evidence of model discovery.':`Requested player: ${esc(ep.player_id)}. Provider: ${esc(t.collection_provider||'recorded in metadata')}. Returned model: ${esc(t.steps[0]?.call.actual_model||'pending')}. Fresh context, ${esc(nice(ep.prompt_condition))} framing.`} Focal seat ${ep.seat_order[0]}, ${esc(nice(ep.opponent_policy))} scripted opponents. Status: ${esc(t.status)}.</div>${out?`<div class="episode-overview"><div class="outcome"><b>${out.score.toFixed(1)}</b>Final own score · rank ${out.rank}</div><div class="outcome"><b>${ex.executed===null?'N/A':ex.executed?'Executed':'No effect'}</b>Specified mechanism</div><div class="outcome"><b>Unknown</b>Discovery · not inferred from execution</div></div>`:''}<div class="turns">${t.steps.map((s,i)=>`<button class="turn-button ${i===turn?'active':''}" data-turn="${i}">Turn ${i+1}</button>`).join('')}</div><div id="turn-content"></div>${out?`<details><summary>Episode labels, support and outcomes</summary><pre>${pretty({behavior:t.behavior,exploit:t.exploit,outcome:t.outcome})}</pre></details>`:''}`;
 renderTurn();
}
function renderTurn(){
 const s=trace.steps[turn];if(!s){$('#turn-content').innerHTML='<div class="empty">No completed action yet.</div>';return}
 $$('[data-turn]').forEach(b=>b.classList.toggle('active',Number(b.dataset.turn)===turn));
 const compact=state=>Object.fromEntries(Object.entries(state).filter(([k])=>!['history','feedback','environment_seed'].includes(k)));
 $('#turn-content').innerHTML=`<div class="action-result"><span class="eyebrow">RECORDED RESPONSE</span><div class="action-name">${esc(s.raw_response)}</div><p>Parsed action: ${esc(s.action??'invalid JSON')} · Own score change: ${s.facts.score_delta[0].toFixed(2)} · Action valid: ${s.facts.valid?'yes':'no'}</p></div><div class="pills">${s.facts.tags.map(tag=>`<span class="pill">${esc(nice(tag))}</span>`).join('')}</div><details><summary>Exact model input before this action</summary>${s.messages.map(m=>`<p class="eyebrow">${esc(m.role)}</p><pre class="prompt">${esc(m.content)}</pre>`).join('')}</details><div class="state-grid"><div><h4>BEFORE STATE · research view</h4><pre>${pretty(compact(s.before))}</pre></div><div><h4>AFTER STATE · research view</h4><pre>${pretty(compact(s.after))}</pre></div></div><p class="footnote">Research states can include hidden values. Only the exact model input above establishes what the player saw.</p><details><summary>Mechanism facts & local counterfactual</summary><pre>${pretty({facts:s.facts,counterfactual:s.counterfactual})}</pre></details>`;
}
function download(){const value=trace&&detailTab==='trajectory'?trace:selected;const blob=new Blob([JSON.stringify(value,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=(trace&&detailTab==='trajectory'?episodeId:selected.game.game_id)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
document.addEventListener('click',async event=>{const b=event.target.closest('button');if(!b)return;try{
 if(b.dataset.page){page(b.dataset.page);saveHash()}
 if(b.dataset.family)await focusFamily(b.dataset.family);
 if(b.dataset.game)await selectGame(b.dataset.game);
 if(b.dataset.pair)await selectGame(b.dataset.pair);
 if(b.dataset.detail){detailTab=b.dataset.detail;renderDetail();if(detailTab==='trajectory')await loadEpisode(episodeId);saveHash()}
 if(b.dataset.turn!==undefined){turn=Number(b.dataset.turn);renderTurn();saveHash()}
 if(b.id==='browse-samples'){page('samples');saveHash()}
 if(b.id==='refresh'){await refresh();toast('Loaded the latest recorded artifacts.')}
 if(b.id==='prev'){offset=Math.max(0,offset-12);await loadCatalog()}
 if(b.id==='next'){offset+=12;await loadCatalog()}
 if(b.id==='download')download();
}catch(e){toast(e.message)}});
$('#family').addEventListener('change',()=>focusFamily($('#family').value).catch(e=>toast(e.message)));
$('#parameter').addEventListener('change',renderDose);
$('#layer').addEventListener('change',()=>{offset=0;loadCatalog().catch(e=>toast(e.message))});
let timer;$('#search').addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>{offset=0;loadCatalog().catch(e=>toast(e.message))},200)});
document.addEventListener('change',event=>{if(event.target.id==='episode'){turn=0;loadEpisode(event.target.value).catch(e=>toast(e.message))}});
async function boot(){
 const hash=new URLSearchParams(location.hash.slice(1));renderSummary(await api('/api/summary'));await loadAssessment();
 if(location.hash==='#assessment-section'&&!$('#assessment-section').hidden)$('#assessment-section').scrollIntoView();
 if(hash.get('family')){$('#family').value=hash.get('family');await refresh()}
 if(hash.get('page')==='samples'||hash.get('game')){page('samples');await loadCatalog(!hash.get('game'))}
 if(hash.get('game')){detailTab=['rules','trajectory','pairs'].includes(hash.get('tab'))?hash.get('tab'):'rules';await selectGame(hash.get('game'),hash.get('episode')||'',Math.max(0,Number(hash.get('turn')||1)-1))}
 setInterval(()=>{if(!document.hidden&&$('#samples').hidden)refresh().catch(()=>{})},20000);
}
boot().catch(e=>toast(`Could not load dataset: ${e.message}`));
