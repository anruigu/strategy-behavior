'use strict';
const $=id=>document.getElementById(id);
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=(x,n=3)=>x==null?'—':Number(x).toFixed(n);
const names={training_mean:'Training mean',linear:'Linear learner',few_4:'Pooled 4-shot',corrected_4:'Learned correction to 4-shot',few_8:'Pooled 8-shot',few_16:'Pooled 16-shot'};
let current=null, request=0, gameRequest=0, episodeRequest=0, timer=null, initialized=false;
async function api(path,args={}){const r=await fetch('/api/general/breadth/'+path+'?'+new URLSearchParams(args));if(!r.ok)throw Error('Could not load '+path+' ('+r.status+')');return r.json();}
function table(headers,rows){return '<table><thead><tr>'+headers.map(h=>'<th>'+esc(h)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map(c=>'<td>'+esc(c)+'</td>').join('')+'</tr>').join('')+'</tbody></table>';}
function bars(id,rows){const max=Math.max(1,...rows.map(r=>r[1]));$(id).innerHTML=rows.map(([name,n])=>'<div class="bar-row"><span>'+esc(name)+'</span><div class="bar-track"><div class="bar-fill" style="width:'+100*n/max+'%"></div></div><span>'+esc(n)+'</span></div>').join('')||'<p class="empty">No completed episodes yet.</p>';}
function resultView(){
 const r=current?.results;if(!r)return;const target=$('target').value;
 const find=(arm,method)=>r.scores.find(s=>s.arm===arm&&s.method===method&&s.target===target)?.score;
 $('scores').innerHTML=table(['Predictor','Depth · 4 families','Breadth · 12 families','Breadth − depth'],Object.entries(names).map(([key,name])=>{const a=find('depth',key),b=find('breadth',key);return[name,fmt(a,4),fmt(b,4),(b-a>0?'+':'')+fmt(b-a,4)];}));
 const comp=r.comparisons.filter(c=>c.comparison==='breadth_minus_depth'&&c.target===target&&['linear','corrected_4'].includes(c.left.method));
 $('comparison').textContent=comp.map(c=>names[c.left.method]+': breadth − depth '+(c.difference>0?'+':'')+fmt(c.difference,4)+'; 95% interval ['+c.ci95.map(x=>fmt(x,4)).join(', ')+']; breadth improves '+c.families_favoring_left+'/6 families.').join(' ');
 if(target==='win'&&r.posthoc_diagnostics)$('comparison').textContent+=' Constant-0.5 arithmetic reference: '+fmt(r.posthoc_diagnostics.constant_half_win.score,4)+' Brier (added after readout).';
}
function renderResults(){
 const r=current.results;$('results').hidden=!r;$('report-link').hidden=!r;if(!r)return;
 $('results-status').textContent='Completed and audited. Both training arms predicted the same 144 prospective test episodes. All few-shot examples pool repeated labels for identical visible inputs.';
 if(r.interpretation)$('results-status').textContent+=' '+r.interpretation[0]+' '+r.interpretation[1];
 resultView();
 $('coverage').innerHTML=table(['Arm','Episodes','Families','Exact conditions','Visible inputs','Actions'],r.training_coverage.map(x=>[x.arm,x.episodes,x.families,x.exact_conditions,x.visible_inputs,x.actions]));
 $('repeats').innerHTML=table(['Family','Variable wins','Exact conditions'],r.test_distributions.repeatability.map(x=>[x.family,x.targets.win.varying_conditions,x.conditions]));
 $('model-results').innerHTML=table(['Family','Model','Episodes','Win','Any invalid','Native score'],r.test_distributions.models.map(x=>[x.family,x.model,x.episodes,fmt(x.targets.win),fmt(x.targets.any_invalid),fmt(x.targets.native_score)]));
 $('behavior').innerHTML=table(['Family','Model','Measurement','Mean','Eligible episodes','Opportunities'],r.test_distributions.behavior.map(x=>[x.family,x.model,x.target,fmt(x.mean),x.episodes,x.opportunities]));
 if(r.posthoc_diagnostics){const d=r.posthoc_diagnostics;$('behavior').innerHTML+='<p class="callout">Post-readout diagnosis: Stag Hunt had '+d.stag_hunt.draws+'/'+d.stag_hunt.episodes+' draws. Sokoban rejected '+d.sokoban.first_action_format_errors+'/'+d.sokoban.episodes+' first actions for missing brackets, so its invalidity signal includes interface compliance. GOPS mean bid fraction is mechanically 7/13 after all cards are spent; use early high-card use to inspect ordering.</p>';}
 const a=r.audit;$('audit').textContent=r.counts.native_transitions.toLocaleString()+' native transitions replayed; '+a.reproduced_values+' serialized forecast values reproduced. '+a.inference.total_calls.toLocaleString()+' recorded inference attempts, $'+fmt(a.inference.reported_usd,2)+' reported cost. Unknown-cost calls: '+a.inference.unknown_cost_calls+'. Forecast freeze: '+a.frozen_at+'. First test actor call: '+a.first_test_call+'.';
}
async function refresh(){
 const seq=++request;clearTimeout(timer);
 try{
  const data=await api('summary',{cohort:$('cohort').value,family:$('family').value});if(seq!==request)return;current=data;
  if(!initialized){const fs=[...new Set([...data.protocol.arms.breadth.families,...data.protocol.test_families])].sort();$('family').innerHTML='<option value="">All families</option>'+fs.map(f=>'<option value="'+esc(f)+'">'+esc(f.replaceAll('_',' '))+'</option>').join('');initialized=true;}
  const total=Object.values(data.progress).reduce((n,p)=>n+(p.statuses.complete||0),0);$('status').textContent=data.results?'Study complete · audited':total+' / 624 episodes complete';
  $('freeze').textContent=data.frozen?'Both arms’ forecasts are frozen. Test collection is allowed.':'Holdout actors remain uncalled until both arms’ forecasts and fitted learners are frozen.';
  $('progress').innerHTML=Object.entries(data.progress).map(([phase,p])=>'<div class="progress-block"><span>'+esc(phase==='training'?'Unique training episodes':'Six-family test episodes')+'</span><strong>'+(p.statuses.complete||0)+' / '+p.planned+'</strong><span>'+p.actions+' focal actions'+((p.statuses.incomplete||p.statuses.censored)?' · '+((p.statuses.incomplete||0)+(p.statuses.censored||0))+' need attention':'')+'</span></div>').join('')+data.prediction.map(p=>'<div class="progress-block"><span>'+esc(p.arm==='depth'?'Depth-arm forecasts':'Breadth-arm forecasts')+'</span><strong>'+p.complete+' / '+(p.planned||'—')+'</strong><span>'+(p.fitted?'Learner fitted':p.planned?'Forecast batches':'Awaiting training')+'</span></div>').join('');
  const counts=data.counts;$('metrics').innerHTML=[['Families in view',counts.families],['Episodes planned',counts.planned],['Episodes complete',counts.complete],['Focal actions',counts.actions]].map(([label,n])=>'<article class="metric"><span class="metric-label">'+label+'</span><strong class="metric-value">'+n.toLocaleString()+'</strong></article>').join('');
  $('families').innerHTML=data.families.map(f=>'<button class="family-card" data-game="'+esc(f.game_id)+'" data-role="'+esc(f.role)+'"><span class="family-role">'+esc(f.role)+'</span><h3>'+esc(f.title)+'</h3><p>'+esc(f.objective)+'</p><span class="small">'+f.players+' player'+(f.players>1?'s':'')+' · '+f.complete+' / '+f.planned+' episodes</span></button>').join('');
  document.querySelectorAll('[data-game]').forEach(b=>b.onclick=()=>loadGame(b.dataset.game));
  bars('distribution',data.families.filter(f=>f.planned).map(f=>[f.title,f.complete]));bars('lengths',Object.entries(data.lengths).sort((a,b)=>+a[0]-+b[0]).map(([n,v])=>[n+' actions',v]));
  $('models').innerHTML=table(['Model','Episodes','Actions','Invalid actions'],data.models.map(m=>[m.model,m.episodes,m.actions,m.invalid_actions]));renderResults();
  if(!data.results)timer=setTimeout(refresh,20000);
 }catch(e){if(seq!==request)return;$('status').textContent=e.message;timer=setTimeout(refresh,20000);}
}
async function loadGame(id){
 const seq=++gameRequest;++episodeRequest;$('detail').innerHTML='<p>Loading game…</p>';
 try{const d=await api('game',{id});if(seq!==gameRequest)return;
  $('detail').innerHTML='<p class="eyebrow">'+esc(d.game.family_id)+'</p><h3>'+esc(d.family.title)+'</h3><p>'+esc(d.family.objective)+'</p><pre>'+esc(JSON.stringify(d.game.parameters,null,2))+'</pre><details><summary>Complete predictor mechanics and opponent policy</summary><pre>'+esc(JSON.stringify(d.mechanics,null,2))+'</pre></details><details><summary>Exact native opening messages · seed '+d.opening.seed+'</summary><pre>'+esc(JSON.stringify(d.opening.observations,null,2))+'</pre></details><label for="episode">Collected model episode</label><select id="episode"><option value="">Choose an episode…</option>'+d.episodes.map(e=>'<option value="'+esc(e.episode_id)+'">'+esc(e.model+' · seed '+e.seed+' · seat '+e.seat+' · repeat '+e.replicate+' · '+e.status+' · '+e.actions+' actions')+'</option>').join('')+'</select><div id="trajectory">'+(!d.episodes.length?'<p class="empty">No model episode has been collected for this family yet.</p>':'')+'</div>';
  $('episode').onchange=()=>loadEpisode($('episode').value);$('detail').scrollIntoView({behavior:'smooth',block:'start'});
 }catch(e){if(seq===gameRequest)$('detail').textContent=e.message;}
}
async function loadEpisode(id){
 const seq=++episodeRequest;if(!id){$('trajectory').innerHTML='';return;} $('trajectory').textContent='Loading trajectory…';
 try{const d=await api('episode',{id});if(seq!==episodeRequest)return;
  $('trajectory').innerHTML='<p>'+esc(d.status)+' · '+d.steps.length+' native transitions</p>'+d.steps.map(s=>'<article class="step"><span class="step-label">Step '+s.index+' · Player '+s.actor+' · '+(s.is_focal?'Focal LLM':'Scripted opponent')+(s.result.native_invalid?' · Native-invalid submission':'')+'</span><pre>'+esc(s.raw_action)+'</pre>'+(s.messages?'<details><summary>Exact actor prompt</summary><pre>'+esc(JSON.stringify(s.messages,null,2))+'</pre></details>':'')+'<details><summary>Evaluator state before / after · may include hidden information</summary><pre>'+esc(JSON.stringify({before:s.before,after:s.after},null,2))+'</pre></details></article>').join('');
 }catch(e){if(seq===episodeRequest)$('trajectory').textContent=e.message;}
}
$('cohort').onchange=refresh;$('family').onchange=refresh;$('refresh').onclick=refresh;$('target').onchange=resultView;refresh();
