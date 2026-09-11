"""Plot the frozen frontier comparison; partial runs are explicitly provisional."""
import csv,json
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from benchmark.fullscale.plot_gemini49 import GROUPS,LABELS

ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'benchmark/results/frontier45-20260909';OUT=BASE/'plots'
RUNS={'Gemini Flash':BASE.parent/'gemini-revised45-20260909','Gemini Pro':BASE/'gemini-3.1-pro','GPT-5.6 Sol':BASE/'gpt-5.6-sol','Grok 4.6':BASE/'grok-4.6'}
COLORS=['#718096','#268b79','#8361bd','#df8b28']

def main():
    OUT.mkdir(exist_ok=True)
    targets=set(json.loads((RUNS['Gemini Flash']/'targets.json').read_text()))
    categories=[c for cs in GROUPS.values() for c in cs if any(t.endswith('.'+c) for t in targets)]
    traces={m:[json.loads(p.read_text()) for p in sorted(d.glob('episodes/*/trace.json'))] for m,d in RUNS.items()}
    rows=[];episodes=[];titles={};summary={};complete=True
    for model,ts in traces.items():
        for t in ts:
            titles[t['game']]=json.JSONDecoder().raw_decode(t['turns'][0]['observation'].split('\nCard: ',1)[1])[0]['title']
            scores=[s for s in t['scores'] if s['exploit_id'] in targets and (not t['target'] or t['target']==s['exploit_id'])]
            for s in scores:
                rows.append(dict(model=model,episode=t['id'],phase=t['condition'],game=t['game'],seed=t['seed'],target=s['exploit_id'],category=s['category'],attempted=s['attempted'],executed=s['executed'],positive_effect=s['positive_mechanism_effect'],payoff=s['payoff_status'],final_score_delta=s['final_score_delta'],final_advantage_delta=s['final_advantage_delta']))
            vals=t['final_scores'];coop='hanabi' in t['game']
            episodes.append(dict(model=model,id=t['id'],game=t['game'],phase=t['condition'],seed=t['seed'],own_score=vals[0],margin=None if coop else vals[0]-max(vals[1:]),win=None if coop else vals[0]>max(vals[1:]),hits=sum(s['executed'] for s in scores),opportunities=len(scores)))
        blind=[r for r in rows if r['model']==model and r['phase']=='blind'];hint=[r for r in rows if r['model']==model and r['phase']=='hinted']
        be=[e for e in episodes if e['model']==model and e['phase']=='blind'];competitive=[e for e in be if e['win'] is not None]
        costs=[];failures=[];pending=0
        for p in list(RUNS[model].glob('episodes/*/calls/*.json'))+list(RUNS[model].glob('preflight-calls/*.json')):
            call=json.loads(p.read_text())
            if not call['attempts']:pending+=1
            for a in call['attempts']:
                if 'error' in a:failures.append(a.get('http_status'));continue
                u=a.get('response',{}).get('usage') or {}
                values=[v for v in (u.get('cost'),(u.get('cost_details') or {}).get('upstream_inference_cost')) if isinstance(v,(int,float))]
                if values:costs.append(max(values))
        summary[model]=dict(blind_episodes=len(be),blind_hits=sum(r['executed'] for r in blind),blind_trials=len(blind),distinct_blind_holes=len({r['target'] for r in blind if r['executed']}),hinted_hits=sum(r['executed'] for r in hint),hinted_trials=len(hint),distinct_blind_or_hinted=len({r['target'] for r in blind+hint if r['executed']}),strict_wins=sum(e['win'] for e in competitive),competitive_episodes=len(competitive),blind_payoff=dict(Counter(r['payoff'] for r in blind if r['executed'])),hinted_payoff=dict(Counter(r['payoff'] for r in hint if r['executed'])),reported_api_cost_usd=sum(costs),failed_request_statuses=dict(Counter(map(str,failures))),pending_requests=pending)
        summary[model]['complete']=len(be)==51 and len(hint)==135-summary[model]['blind_hits']
        complete &= summary[model]['complete']
    catrows=[]
    for model in RUNS:
        for cat in categories:
            row=dict(model=model,category=cat)
            for phase in ('blind','hinted'):
                rr=[r for r in rows if r['model']==model and r['category']==cat and r['phase']==phase]
                row[phase+'_n']=len(rr);row[phase+'_hits']=sum(r['executed'] for r in rr);row[phase+'_rate']=row[phase+'_hits']/len(rr) if rr else None
            catrows.append(row)
    summary['complete']=bool(complete)
    summary['frontier_reported_api_cost_usd']=sum(summary[m]['reported_api_cost_usd'] for m in list(RUNS)[1:])
    hint_maps={m:{(r['target'],r['seed']):r for r in rows if r['model']==m and r['phase']=='hinted'} for m in RUNS}
    common_hints=set.intersection(*(set(d) for d in hint_maps.values()))
    summary['common_hinted_subset']=dict(trials=len(common_hints),hits={m:sum(d[k]['executed'] for k in common_hints) for m,d in hint_maps.items()},note='Matched subset selected by every model missing blind; not representative of all holes.')
    # Paired descriptive comparisons use only identical completed blind game/seed cells.
    base_map={(r['target'],r['seed']):r['executed'] for r in rows if r['model']=='Gemini Flash' and r['phase']=='blind'}
    for model in list(RUNS)[1:]:
        other={(r['target'],r['seed']):r['executed'] for r in rows if r['model']==model and r['phase']=='blind'}
        common=base_map.keys() & other.keys()
        summary[model]['paired_to_flash']=dict(trials=len(common),frontier_only=sum(other[k] and not base_map[k] for k in common),flash_only=sum(base_map[k] and not other[k] for k in common),both=sum(other[k] and base_map[k] for k in common))
    for name,data in [('episode_holes',rows),('episodes',episodes),('category_rates',catrows)]:
        with (OUT/(name+'.csv')).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    (BASE/'comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    def save(fig,name):
        for ext in ('png','svg','pdf'):fig.savefig(OUT/(name+'.'+ext),dpi=170,bbox_inches='tight',facecolor='white')
        plt.close(fig)
    qualifier='' if complete else ' · PROVISIONAL'
    angles=np.linspace(0,2*np.pi,4,endpoint=False)
    fig,axes=plt.subplots(1,2,subplot_kw={'projection':'polar'},figsize=(13,7));fig.subplots_adjust(left=.12,right=.87,top=.72,bottom=.27,wspace=.58)
    for ax,phase in zip(axes,('blind','hinted')):
        for model,color in zip(RUNS,COLORS):
            vals=[]
            for cs in GROUPS.values():
                rates=[r[phase+'_rate'] for r in catrows if r['model']==model and r['category'] in cs and r[phase+'_rate'] is not None]
                vals.append(np.mean(rates) if rates else np.nan)
            ax.plot(np.r_[angles,angles[0]],np.r_[vals,vals[0]],marker='o',lw=2,color=color,label=model)
        ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1);ax.set_xticks(angles,['Rule /\nenforcement','Information /\ninterface','State /\ntime','Multiplayer /\nobjective']);ax.tick_params(axis='x',pad=18);ax.set_ylim(0,1);ax.set_yticks([.25,.5,.75,1],['25%','50%','75%','100%'],fontsize=8);ax.set_title('Blind execution' if phase=='blind' else 'Hinted execution on blind misses',pad=45,fontsize=13)
    fig.suptitle('Frontier models on the revised 45 holes'+qualifier,fontsize=20,y=.98)
    fig.text(.5,.90,'Same frozen games, win prompt, high reasoning and seeds · no reflection · native scripted rivals',ha='center',fontsize=11)
    fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.09),ncol=4,frameon=False)
    fig.text(.5,.035,'Macro-average across eligible hole types. Each model has a different hinted miss set. Execution is observed activation, not inferred awareness.',ha='center',fontsize=9)
    save(fig,'frontier_star')
    fig,axes=plt.subplots(1,2,figsize=(13,9));fig.subplots_adjust(left=.26,right=.94,top=.83,bottom=.15,wspace=.16)
    cmap=plt.get_cmap('YlGnBu').copy();cmap.set_bad('#e8eaed')
    for ax,phase in zip(axes,('blind','hinted')):
        matrix=np.array([[next(r[phase+'_rate'] for r in catrows if r['model']==m and r['category']==c) for m in RUNS] for c in categories],dtype=float)
        im=ax.imshow(matrix,vmin=0,vmax=1,cmap=cmap,aspect='auto')
        for i,c in enumerate(categories):
            for j,m in enumerate(RUNS):
                r=next(r for r in catrows if r['model']==m and r['category']==c);v=matrix[i,j]
                ax.text(j,i,f"{r[phase+'_hits']}/{r[phase+'_n']}" if r[phase+'_n'] else '—',ha='center',va='center',fontsize=9,color='white' if v>.6 else '#243542')
        ax.set_xticks(range(4),list(RUNS),rotation=28,ha='right');ax.set_yticks(range(len(categories)),[LABELS[c] for c in categories] if phase=='blind' else []);ax.set_title('Blind' if phase=='blind' else 'Hinted misses',pad=15)
    fig.suptitle('Which hole types were executed?'+qualifier,fontsize=21,y=.96)
    fig.text(.5,.90,'Cells show executed / eligible target × seed trials; missing types are excluded from this 45-hole scope.',ha='center',fontsize=10)
    fig.text(.5,.025,'Three seeds per hole in completed blind runs. Hinted denominators depend on each model’s misses; they are not a matched difficulty test.',ha='center',fontsize=9)
    save(fig,'frontier_types')
    games=sorted(titles,key=titles.get);fig,axes=plt.subplots(1,3,figsize=(15,11));fig.subplots_adjust(left=.24,right=.97,top=.84,bottom=.12,wspace=.33)
    for i,g in enumerate(games):
        for j,(model,color) in enumerate(zip(RUNS,COLORS)):
            es=[e for e in episodes if e['model']==model and e['game']==g and e['phase']=='blind']
            if not es:continue
            y=i+(j-1.5)*.17
            axes[0].scatter(sum(e['hits'] for e in es)/sum(e['opportunities'] for e in es),y,color=color,s=25)
            axes[1].scatter(np.mean([e['own_score'] for e in es]),y,color=color,s=25)
            wins=[e['win'] for e in es if e['win'] is not None]
            if wins:axes[2].scatter(np.mean(wins),y,color=color,s=25)
        if 'hanabi' in g:axes[2].text(.02,i,'Cooperative: team score',va='center',fontsize=9)
    for i,ax in enumerate(axes):
        ax.set_ylim(len(games)-.4,-.6);ax.set_yticks(range(len(games)),[titles[g] for g in games] if i==0 else []);ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
    for ax in (axes[0],axes[2]):ax.set_xlim(-.05,1.05);ax.set_xticks([0,.5,1],['0%','50%','100%'])
    axes[1].set_xscale('symlog',linthresh=20);axes[1].set_xlabel('Points (linear to 20, then log)')
    for ax,title in zip(axes,('Blind hole execution','Mean final score','Strict win rate')):ax.set_title(title,pad=15)
    fig.suptitle('Hacking and payoff across games'+qualifier,fontsize=22,y=.97)
    fig.legend([plt.Line2D([],[],marker='o',ls='',color=c) for c in COLORS],list(RUNS),loc='upper center',bbox_to_anchor=(.60,.92),ncol=4,frameon=False)
    fig.text(.5,.035,'Three blind episodes per edition at completion. Scores are comparable between models within an edition, not across editions. Ties are not wins.',ha='center',fontsize=10)
    save(fig,'frontier_games_payoffs')
    lines=['# Frontier comparison: revised 45 holes','', '**Provisional: runs are still completing.**' if not complete else '**Complete: all blind episodes and per-miss hinted diagnostics are scored.**','', 'All four configurations use the same frozen games, win prompt, seeds 19/73/101, high reasoning, 16,384-token completion limit, no reflection or cross-game memory, and native scripted rivals. Gemini Pro uses the `google/gemini-3.1-pro-preview` endpoint. This is not cross-play.','', '| Model | Blind activation | Distinct blind holes | Hinted activation | Strict wins | API cost |','|---|---:|---:|---:|---:|---:|']
    for m in RUNS:
        s=summary[m];lines.append(f"| {m} | {s['blind_hits']}/{s['blind_trials']} | {s['distinct_blind_holes']}/45 | {s['hinted_hits']}/{s['hinted_trials']} | {s['strict_wins']}/{s['competitive_episodes']} | ${s['reported_api_cost_usd']:.2f} |")
    lines+=['',f"Frontier-only reported cost, including upstream BYOK charges and probes: **${summary['frontier_reported_api_cost_usd']:.2f}**. Failed calls without billing metadata are reserved conservatively in the ledger, not counted as known charges here. Budget ceiling: $600, not a spending target.",'','![Broad categories](plots/frontier_star.png)','','![Hole types](plots/frontier_types.png)','','![Games and payoffs](plots/frontier_games_payoffs.png)','','Execution is an engine-observed activation. It does not prove that the model articulated or understood the mechanism. Hints reveal the target mechanism only after a blind miss; hinted percentages compare different miss sets. Broad-category stars macro-average eligible type rates. Missing/excluded categories are not zeroes. Three seeds per hole provide a descriptive comparison, not a definitive general capability-tier result. Model family and tier are partly confounded; Flash versus Pro is the within-family comparison.','','Final payoff uses own score minus strongest rival (team score for Hanabi) against replay with only the target mechanism patched. Information mechanisms require an adaptive control; unfinished patched trajectories have no final causal score. See `comparison.json` for these separate statuses. Raw-score comparisons across different games are not meaningful.','','Trace viewer: forward port **42327**, then open http://localhost:42327. Frozen manifests, per-turn calls and offline verification results live in each model directory. Machine-readable plotted data are in `plots/episode_holes.csv`, `plots/episodes.csv`, and `plots/category_rates.csv`.']
    (BASE/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
