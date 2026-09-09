"""Current and cumulative engine activation, with fixed target scope and missingness."""
import csv,json,sys,sqlite3
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'benchmark/results/repeated45-20260909';OUT=BASE/'plots';OUT.mkdir(exist_ok=True)
NAMES={'qwen-3.8-27b-medium':'Qwen 3.8 27B (medium)','glm':'GLM 5.3','gemini-3.1-pro':'Gemini 3.1 Pro','gpt-5.6-sol':'GPT-5.6 Sol','grok-4.6':'Grok 4.6'}
ARMS={'transcript_only':('#65758b','--'),'reflection':('#198b78','-')}

def main():
 plan=json.loads((BASE/'plan.json').read_text());targets=set(plan['targets']);gids=sorted({t.rsplit('.',1)[0] for t in targets});rows=[];summary={};finished=True
 for model in NAMES:
  d=BASE/model;state=json.loads((d/'status.json').read_text()) if (d/'status.json').exists() else {'status':'starting'}
  summary[model]={'status':state['status'],'errors':state.get('errors',[])};finished &= state['status']=='finished'
  for gid in gids:
   for seed in plan['seeds']:
    bp=(BASE.parent/'frontier45-20260909'/model/'episodes' if model in ('gemini-3.1-pro','gpt-5.6-sol','grok-4.6') else d/'baseline/episodes')/f'blind__{gid}__s{seed}'/'trace.json'
    for arm in ARMS:
     seen={metric:set() for metric in ('attempted','executed','positive_mechanism_effect')}
     for iteration in range(1,5):
      p=bp if iteration==1 else d/'chains'/f'{gid}__s{seed}'/arm/f'play-{iteration}'/'trace.json'
      if not p.exists():break  # Never treat missing/failed episodes as behavioral zeroes.
      t=json.loads(p.read_text())
      for s in t['scores']:
       if s['exploit_id'] not in targets:continue
       row=dict(model=model,game=gid,seed=seed,condition=arm,iteration=iteration,target=s['exploit_id'],category=s['category'],own_score=t['final_scores'][0],payoff_status=s['payoff_status'])
       for metric in seen:
        if s[metric]:seen[metric].add(s['exploit_id'])
        row[metric]=bool(s[metric]);row['cumulative_'+metric]=s['exploit_id'] in seen[metric]
       rows.append(row)
 curves=[]
 for model in NAMES:
  for arm in ARMS:
   for iteration in range(1,5):
    rr=[r for r in rows if r['model']==model and r['condition']==arm and r['iteration']==iteration]
    row=dict(model=model,condition=arm,iteration=iteration,completed_opportunities=len(rr),expected_opportunities=135)
    for metric in ('attempted','executed','positive_mechanism_effect'):
     for mode in ('','cumulative_'):
      key=mode+metric;row[key+'_hits']=sum(r[key] for r in rr);row[key+'_rate']=row[key+'_hits']/len(rr) if rr else None
    curves.append(row)
 if rows:
  for name,data in [('hole_curves',rows),('model_curves',curves)]:
   with (OUT/(name+'.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 summary['all_finished']=bool(finished);summary['curves']=curves
 with sqlite3.connect(BASE/'budget.sqlite',timeout=30) as db:
  charged,committed=db.execute('SELECT COALESCE(SUM(charged),0),COALESCE(SUM(COALESCE(charged,reserved)),0) FROM calls').fetchone()
 summary['budget']=dict(ceiling_usd=600,reported_combined_usd=charged,reported_extension_usd=charged-plan['prior_spend_usd'],committed_with_reservations_usd=committed)
 (BASE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
 fig,axes=plt.subplots(2,5,figsize=(17,8.3),sharex=True,sharey=True);fig.subplots_adjust(left=.075,right=.98,top=.79,bottom=.20,wspace=.16,hspace=.32)
 for j,model in enumerate(NAMES):
  for i,metric in enumerate(('executed_rate','cumulative_executed_rate')):
   ax=axes[i,j]
   for arm,(color,style) in ARMS.items():
    rr=[r for r in curves if r['model']==model and r['condition']==arm];ax.plot([r['iteration'] for r in rr],[r[metric] if r['completed_opportunities']==135 else np.nan for r in rr],ls=style,color=color,marker='o',lw=2,label='Explicit reflection + transcript' if arm=='reflection' else 'Transcript only')
   ax.set_xticks([1,2,3,4]);ax.set_ylim(0,1.03);ax.set_yticks([0,.25,.5,.75,1],['0%','25%','50%','75%','100%']);ax.grid(alpha=.16)
   if i==0:ax.set_title(NAMES[model],pad=15)
   if i==1:ax.set_xlabel('Episode number')
  rr=[r for r in curves if r['model']==model];latest={a:max((r['iteration'] for r in rr if r['condition']==a and r['completed_opportunities']==135),default=0) for a in ARMS}
  if not finished:axes[0,j].text(.5,1.03,'Completed plays: '+str(latest['transcript_only'])+' control / '+str(latest['reflection'])+' reflection',transform=axes[0,j].transAxes,ha='center',fontsize=7)
 axes[0,0].set_ylabel('Activated in this episode');axes[1,0].set_ylabel('Activated at least once so far')
 fig.suptitle('Does explicit reflection improve repeated-play discovery?'+('' if finished else ' · PROVISIONAL'),fontsize=20,y=.97)
 fig.text(.5,.90,'Same revised 45 holes · 3 seed chains · 4 plays · full visible history in both arms · no answer-key hints',ha='center',fontsize=12)
 fig.legend(*axes[0,0].get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.105),ncol=2,frameon=False,fontsize=11)
 fig.text(.5,.065,'Cumulative credit = OR of engine activations within each hole × seed chain. Rising cumulative coverage alone does not demonstrate learning.',ha='center',fontsize=10)
 fig.text(.5,.025,'Same initial state resets each episode; no cross-game memory. Qwen medium; others high. Only fully scored 135-opportunity points are plotted; partial data remain in CSVs.',ha='center',fontsize=10)
 for ext in ('png','svg','pdf'):fig.savefig(OUT/('discovery_curves.'+ext),dpi=170,bbox_inches='tight',facecolor='white')
 plt.close(fig)
 # Detailed per-game curves; kept separate to avoid an unreadable combined figure.
 for model in NAMES:
  fig,axes=plt.subplots(4,5,figsize=(17,11),sharex=True,sharey=True);fig.subplots_adjust(top=.88,bottom=.13,hspace=.6,wspace=.2)
  for ax,gid in zip(axes.flat,gids):
   for arm,(color,style) in ARMS.items():
    vals=[]
    for it in range(1,5):
     rr=[r for r in rows if r['model']==model and r['game']==gid and r['condition']==arm and r['iteration']==it];vals.append(np.mean([r['cumulative_executed'] for r in rr]) if len(rr)==3*sum(t.rsplit('.',1)[0]==gid for t in targets) else np.nan)
    ax.plot(range(1,5),vals,color=color,ls=style,marker='o',lw=1.8)
   ax.set_title(gid.removeprefix('v3_').replace('_',' '),fontsize=9);ax.set_ylim(0,1.03);ax.set_xticks([1,2,3,4]);ax.set_yticks([0,.5,1],['0%','50%','100%']);ax.grid(alpha=.15)
  for ax in list(axes.flat)[len(gids):]:ax.set_visible(False)
  fig.suptitle(NAMES[model]+' · cumulative activation by game'+('' if finished else ' · PROVISIONAL'),fontsize=18)
  fig.text(.5,.07,'Green solid: reflection + transcript. Gray dashed: transcript only. Three seed chains; points appear only after all three complete that episode.',ha='center',fontsize=10)
  fig.savefig(OUT/(model+'_games.png'),dpi=150,bbox_inches='tight',facecolor='white');plt.close(fig)
 lines=['# Repeated play with and without reflection','', '**Complete.**' if finished else '**Running / provisional.**','','![Discovery curves](plots/discovery_curves.png)','','Four episodes per game, 45 eligible holes across 17 editions, three chains with seeds 19/73/101. Qwen 3.8 27B and GLM 5.3 use the same revised games as Gemini Pro, GPT-5.6 Sol and Grok 4.6. Qwen uses medium reasoning after xhigh frequently failed to return actions within the token cap; its fresh medium run is separate and the original xhigh run is preserved. The others use high. No oracle/hackbook hints are supplied. Native scripted opponents remain.','','The first blind episode is shared between arms. Previously completed frontier blind traces are reused; open baselines are newly run. Neither first-play prompt announces repetition. From episode 2 onward both arms receive the same repeat-play instruction and full player-visible history. One arm additionally gets a reflection call before each replay, including prior observations and earlier notes. This measures the incremental reflection-step package (including extra tokens), not equal-compute performance. Gemini reflection notes requested during bounded recovery use a 16,384-token cap after some original 8,192-token requests were truncated; original accepted notes are preserved and affected calls are marked in their metadata.','','Every episode resets to the same seeded initial state. There is no memory across games or seed chains. This tests learning a particular game instance, not transfer to new initial states. Cumulative credit is an OR of activation over episodes for each target/seed chain, averaged across the 135 fixed opportunities when complete. Per-episode activation can fall even when cumulative coverage rises. Semantic/articulated discovery is not inferred from engine activation. Failed/missing trajectories are not scored as misses.','','Budget: $600 combined with the prior frontier comparison; $58.1062 carried forward. Hosted open-model calls are free. Paid requests reserve cost before submission, include upstream BYOK costs, and have no automatic retries.','','[Per-hole/seed/episode current and cumulative metrics](plots/hole_curves.csv) · [Model curves](plots/model_curves.csv) · [Protocol](plan.json)','','Per-game cumulative plots:']
 lines += [f'- [{NAMES[m]}](plots/{m}_games.png)' for m in NAMES]
 lines += ['',f'Recorded extension charges: ${charged-plan["prior_spend_usd"]:.2f}. Combined charges including prior frontier study: ${charged:.2f}. Combined commitment including pending/ambiguous reservations: ${committed:.2f} / $600.']
 (BASE/'RESULTS.md').write_text('\n'.join(lines)+'\n')
 print('Plotted',len(rows),'hole rows; all finished:',finished)

if __name__=='__main__':main()
