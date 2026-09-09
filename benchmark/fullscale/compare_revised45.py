"""Descriptive same-model/seed comparison; revised rules are a bundled intervention."""
from pathlib import Path
import csv,json
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from benchmark.fullscale.plot_gemini49 import GROUPS
ROOT=Path(__file__).resolve().parents[2];OLD=ROOT/'benchmark/results/gemini-engine49-20260908';NEW=ROOT/'benchmark/results/gemini-revised45-20260909';OUT=NEW/'plots';OUT.mkdir(exist_ok=True)
TARGETS=set(json.loads((NEW/'targets.json').read_text()))
RUNS={'Original':OLD,'Revised':NEW};COLORS={'Original':'#70829f','Revised':'#218778'}
changed={'v3_ref_hanabi_conventions','v3_ref_battleship_patrol','v3_ref_estate_neighbours','v3_ref_auction_room'}
traces={label:[json.loads(p.read_text()) for p in sorted(run.glob('episodes/*/trace.json'))] for label,run in RUNS.items()}
rows=[];titles={}
for label,ts in traces.items():
 for t in ts:
  ss=[s for s in t['scores'] if s['exploit_id'] in TARGETS]
  if not ss or (t['condition']=='hinted' and t['target'] not in TARGETS):continue
  card=json.JSONDecoder().raw_decode(t['turns'][0]['observation'].split('\nCard: ',1)[1])[0];titles[t['game']]=card['title']
  coop='hanabi' in t['game'];vals=t['final_scores']
  rows.append(dict(version=label,id=t['id'],game=t['game'],phase=t['condition'],seed=t['seed'],target=t['target'],eligible=len(ss),hits=sum(s['executed'] for s in ss),own=vals[0],margin=None if coop else vals[0]-max(vals[1:]),win=None if coop else vals[0]>max(vals[1:]),target_hit=next((s['executed'] for s in ss if s['exploit_id']==t['target']),None),mechanics_changed=t['game'] in changed))
summary={};categories=sorted({t.split('.')[-1] for t in TARGETS});catrows=[]
for label,ts in traces.items():
 blind=[r for r in rows if r['version']==label and r['phase']=='blind'];hinted=[r for r in rows if r['version']==label and r['phase']=='hinted'];competitive=[r for r in blind if r['win'] is not None]
 seen={s['exploit_id'] for t in ts if t['condition']=='blind' for s in t['scores'] if s['exploit_id'] in TARGETS and s['executed']}
 summary[label]=dict(blind_episodes=len(blind),blind_hits=sum(r['hits'] for r in blind),blind_trials=sum(r['eligible'] for r in blind),blind_distinct=len(seen),hinted_episodes=len(hinted),hinted_hits=sum(r['target_hit'] for r in hinted),strict_wins=sum(r['win'] for r in competitive),competitive_episodes=len(competitive))
 for cat in categories:
  r=dict(version=label,category=cat)
  for phase in ('blind','hinted'):
   ss=[s for t in ts if t['condition']==phase for s in t['scores'] if s['exploit_id'] in TARGETS and s['category']==cat and (phase=='blind' or t['target']==s['exploit_id'])]
   r[phase+'_n']=len(ss);r[phase+'_hits']=sum(s['executed'] for s in ss);r[phase+'_rate']=r[phase+'_hits']/len(ss) if ss else None
  catrows.append(r)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
def save(fig,name):
 for ext in ('png','svg','pdf'):fig.savefig(OUT/f'{name}.{ext}',dpi=165,bbox_inches='tight',facecolor='white')
 plt.close(fig)
labels=list(GROUPS);angles=np.linspace(0,2*np.pi,4,endpoint=False);fig,axs=plt.subplots(1,2,subplot_kw={'projection':'polar'},figsize=(12,6.8));fig.subplots_adjust(left=.12,right=.87,top=.74,bottom=.18,wspace=.55)
for ax,phase in zip(axs,['blind','hinted']):
 for label in RUNS:
  vals=[]
  for group in GROUPS.values():
   rates=[r[phase+'_rate'] for r in catrows if r['version']==label and r['category'] in group and r[phase+'_rate'] is not None]
   vals.append(np.mean(rates) if rates else 0)
  ax.plot(np.r_[angles,angles[0]],np.r_[vals,vals[0]],marker='o',color=COLORS[label],label=label,lw=2);ax.fill(np.r_[angles,angles[0]],np.r_[vals,vals[0]],color=COLORS[label],alpha=.06)
 ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1);ax.set_xticks(angles,['Rule /\nenforcement','Information /\ninterface','State /\ntime','Multiplayer /\nobjective']);ax.tick_params(axis='x',pad=18);ax.set_ylim(0,1);ax.set_yticks([.25,.5,.75,1],['25%','50%','75%','100%'],fontsize=8);ax.set_title('Blind execution' if phase=='blind' else 'Hinted execution on prior misses',pad=45,fontsize=13)
fig.suptitle('Gemini: original versus revised games',fontsize=22,y=.97);fig.text(.5,.89,'Same model, high reasoning, seeds 19 / 73 / 101 · 45 holes · no reflection',ha='center',fontsize=11)
fig.legend(*axs[0].get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.10),ncol=2,frameon=False)
fig.text(.5,.035,'Macro-average of eligible type rates. Hint sets differ because each run retests its own misses. Original rules contained disclosures.',ha='center',fontsize=9)
save(fig,'original_vs_revised_star')
games=sorted(titles,key=titles.get);fig,axes=plt.subplots(1,3,figsize=(14,10),gridspec_kw={'width_ratios':[1,1,1]});fig.subplots_adjust(left=.25,right=.97,top=.83,bottom=.15,wspace=.38)
for i,gid in enumerate(games):
 for label,offset in [('Original',-.17),('Revised',.17)]:
  rr=[r for r in rows if r['version']==label and r['game']==gid and r['phase']=='blind'];y=i+offset
  if not rr:continue
  axes[0].scatter(sum(r['hits'] for r in rr)/sum(r['eligible'] for r in rr),y,color=COLORS[label])
  axes[1].scatter(np.mean([r['own'] for r in rr]),y,color=COLORS[label])
  wins=[r['win'] for r in rr if r['win'] is not None]
  if wins:axes[2].scatter(np.mean(wins),y,color=COLORS[label])
  elif label=='Original':axes[2].text(.03,i,'Team score only',va='center',fontsize=9,color='#69737b')
for ax in axes:ax.set_ylim(len(games)-.5,-.7);ax.set_yticks(range(len(games)));ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
axes[0].set_yticklabels([titles[g]+(' *' if g in changed else '') for g in games]);axes[1].set_yticklabels([]);axes[2].set_yticklabels([])
for ax in [axes[0],axes[2]]:ax.set_xlim(-.05,1.05);ax.set_xticks([0,.5,1],['0%','50%','100%'])
axes[1].set_xscale('symlog',linthresh=20);axes[1].set_xlabel('Points (linear to 20, then log)')
for ax,title in zip(axes,['Eligible holes executed','Mean final score','Strict win rate']):ax.set_title(title,pad=15)
fig.text(.04,.96,'Where did the revised run change?',fontsize=22,weight='bold');fig.text(.04,.91,'Blind episodes only · three seeds per edition · dots are means, not independent confidence estimates',fontsize=11)
fig.legend([plt.Line2D([],[],marker='o',ls='',color=c) for c in COLORS.values()],list(COLORS),loc='upper center',bbox_to_anchor=(.59,.89),ncol=2,frameon=False)
fig.text(.04,.075,'* Mechanics changed: Hanabi horizon, Patrol scoring, Estate/Auction coalition bonuses. Raw-score changes here are not capability gains.',fontsize=9)
fig.text(.04,.045,'Other editions have the same transitions. Task-card disclosure fixes also change what the model sees. This is a bundled revision, not an isolated ablation.',fontsize=9)
save(fig,'original_vs_revised_by_game')
with (OUT/'episodes.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (OUT/'category_rates.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(catrows[0]));w.writeheader();w.writerows(catrows)
# Compare identical target/seed hinted follow-ups as a secondary, matched subset.
hint_maps={label:{(r['target'],r['seed']):r for r in rows if r['version']==label and r['phase']=='hinted'} for label in RUNS}
common=set(hint_maps['Original']) & set(hint_maps['Revised'])
summary['common_hinted_targets']=dict(n=len(common),original_hits=sum(hint_maps['Original'][k]['target_hit'] for k in common),revised_hits=sum(hint_maps['Revised'][k]['target_hit'] for k in common))
(OUT/'comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
