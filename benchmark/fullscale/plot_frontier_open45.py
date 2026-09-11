"""Descriptive historical open/frontier comparison, matched completed blind cells."""
import csv,json,math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from benchmark.fullscale.plot_gemini49 import GROUPS
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'benchmark/results/frontier45-20260909';OUT=BASE/'plots/frontier_vs_open';OUT.mkdir(exist_ok=True)
RUNS={'Qwen 3.8 27B':ROOT/'benchmark/results/small-engine49-20260909/qwen-3.8-27b','GLM 5.3':ROOT/'benchmark/results/small-engine49-20260909/glm','Gemini 3.1 Pro':BASE/'gemini-3.1-pro','GPT-5.6 Sol':BASE/'gpt-5.6-sol','Grok 4.6':BASE/'grok-4.6'}
COLORS=['#16769c','#60a9bf','#21896d','#9258b0','#df862b'];TARGETS=set(json.loads((BASE/'gemini-3.1-pro/targets.json').read_text()))
traces={m:[json.loads(p.read_text()) for p in d.glob('episodes/*/trace.json')] for m,d in RUNS.items()}
keys={m:{(t['game'],t['seed']) for t in ts if t['condition']=='blind' and any(s['exploit_id'] in TARGETS for s in t['scores'])} for m,ts in traces.items()}
common=set.intersection(*keys.values());rows=[];summary={}
for m,ts in traces.items():
 ss=[s for t in ts if t['condition']=='blind' and (t['game'],t['seed']) in common for s in t['scores'] if s['exploit_id'] in TARGETS]
 summary[m]={'executed':sum(s['executed'] for s in ss),'trials':len(ss),'distinct_holes':len({s['exploit_id'] for s in ss if s['executed']})}
 for group,cats in GROUPS.items():
  rates=[]
  for c in cats:
   cs=[s for s in ss if s['category']==c]
   if cs:rates.append(sum(s['executed'] for s in cs)/len(cs))
  rows.append(dict(model=m,group=group,rate=float(np.mean(rates)),eligible_types=len(rates)))
summary['common_blind_episodes']=len(common);summary['excluded_game_seed_cells']=sorted(set.union(*keys.values())-common)
summary['caveat']='Historical descriptive comparison: open models low reasoning / v3-20260908.1, frontier high reasoning / v3-20260909.3. Public-rule disclosures, mechanics and coalition scope changed. Matching cells does not remove these confounds.'
(OUT/'comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
with (OUT/'group_rates.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False})
limit=max(.5,math.ceil(max(r['rate'] for r in rows)*10)/10)
fig=plt.figure(figsize=(15,8.8));ax=fig.add_axes([.10,.27,.35,.46],projection='polar');dot=fig.add_axes([.64,.30,.32,.43])
angles=np.linspace(0,2*np.pi,4,endpoint=False)
for j,(m,color) in enumerate(zip(RUNS,COLORS)):
 vals=[r['rate'] for r in rows if r['model']==m];style='--' if j<2 else '-';marker='s' if j<2 else 'o'
 ax.plot(np.r_[angles,angles[0]],np.r_[vals,vals[0]],color=color,ls=style,marker=marker,lw=2.3,ms=6,label=m)
 for i,v in enumerate(vals):dot.scatter(v,i+(j-2)*.12,color=color,marker=marker,s=45,zorder=3)
ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1);ax.set_xticks(angles,['Rule /\nenforcement','Information /\ninterface','State /\ntime','Multiplayer /\nobjective']);ax.tick_params(axis='x',pad=20);ax.set_ylim(0,limit)
ticks=np.arange(.1,limit+.001,.1);ax.set_yticks(ticks,[f'{x:.0%}' for x in ticks],fontsize=9);ax.set_rlabel_position(42)
fig.text(.275,.83,f'Blind execution · zoomed to 0–{limit:.0%}',ha='center',fontsize=14)
dot.set_yticks(range(4),['Rule / enforcement','Information / interface','State / time','Multiplayer / objective']);dot.set_ylim(3.5,-.5);dot.set_xlim(0,limit);dot.set_xticks(np.arange(0,limit+.001,.1),[f'{x:.0%}' for x in np.arange(0,limit+.001,.1)]);dot.grid(axis='x',alpha=.22);dot.set_xlabel('Macro-average execution rate');dot.set_title('Same rates on a shared linear scale',pad=30,fontsize=14)
fig.text(.06,.95,'Frontier versus open models',fontsize=25,weight='bold');fig.text(.06,.90,f'{len(common)} matched blind game × seed episodes · current 45-hole filter · broad groups average eligible type rates',fontsize=12)
fig.legend(*ax.get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.15),ncol=5,frameon=False,fontsize=11)
fig.text(.5,.115,'Dashed squares: open models, low reasoning, older rules. Solid circles: frontier models, high reasoning, revised rules.',ha='center',fontsize=11)
fig.text(.5,.065,'Historical comparison, not an isolated capability-tier test: rules, disclosures, scoring and excluded bonuses changed between runs.',ha='center',fontsize=10,color='#8a493a')
fig.text(.5,.025,'Radial scale starts at zero; outer ring is '+f'{limit:.0%}'+', not 100%. Execution means an observed mechanism activation, not proven understanding.',ha='center',fontsize=10,color='#56616c')
for ext in ('png','svg','pdf'):fig.savefig(OUT/('frontier_vs_open_zoom.'+ext),dpi=180,bbox_inches='tight',facecolor='white')
plt.close(fig)
(OUT/'README.md').write_text('# Frontier versus open models\n\n![Zoomed comparison](frontier_vs_open_zoom.png)\n\n'+summary['caveat']+'\n\nOnly common completed blind game/seed cases are counted (49 episodes). Excluded missing Qwen episodes: Commons Neighbours seed 101 and Exchange Workshops seed 73. Same target filter and game/seed intersection across all five models; not a matched protocol. No new paid calls. Kimi has no corresponding completed run in this dataset.\n\nReproduce: `python -B -m benchmark.fullscale.plot_frontier_open45`. Source counts and exported group rates: `comparison.json`, `group_rates.csv`.\n')
print(json.dumps(summary,indent=2));print('radial_max',limit)
