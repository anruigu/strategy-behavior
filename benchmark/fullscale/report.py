"""Descriptive engine-only reports; missing matches and semantic labels stay explicit."""
import argparse
from collections import defaultdict
import csv
import json
from pathlib import Path
import time
from benchmark.clients import write_json,now
from benchmark.v3.plot_limited_run import hits,INSTANCES,GAMES

def build(root):
    import matplotlib.pyplot as plt
    import numpy as np
    manifest=json.loads((root/'manifest.json').read_text())
    traces=[json.loads(p.read_text()) for p in sorted(root.glob('matches/*/trace.json'))]
    planned=manifest['schedule'];rows=[];seatrows=[]
    for t in traces:
        for p,m in enumerate(t['seats']):
            active=hits(t,p)
            seatrows.append(dict(match=t['id'],game=t['game'],seed=t['seed'],mode=t['mode'],model=m,pid=p,win_share=t['results'][p]['win_share'],any_activation=bool(active)))
            for h in INSTANCES[t['game']]:
                first=None;local_advantage=False
                for rnd in t['rounds']:
                    if h not in rnd['events'][p]['executed']:continue
                    if h=='terminal_condition' and (rnd['round']>=8 or rnd['controls'][h]['done']):continue
                    first=rnd['round'] if first is None else first
                    actual=rnd['after']['scores'];cf=rnd['controls'][h]['scores']
                    relative=lambda xs:xs[p]-sum(v for q,v in enumerate(xs) if q!=p)/(len(xs)-1)
                    local_advantage |= relative(actual)>relative(cf)+1e-9
                rows.append(dict(match=t['id'],game=t['game'],seed=t['seed'],mode=t['mode'],model=m,pid=p,hole=h,activated=h in active,first_round=first,positive_local_relative_score_effect=local_advantage))
    out=root/'analysis';out.mkdir(exist_ok=True)
    for name,data in [('seat_hole_data',rows),('seat_results',seatrows)]:
        if data:
            with (out/(name+'.csv')).open('w') as f:
                w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    groups=defaultdict(list)
    for r in rows:groups[r['game'],r['mode'],r['model'],r['hole']].append(r)
    cells=[dict(game=g,mode=mode,model=m,hole=h,completed_seats=len(rs),activated_seats=sum(r['activated'] for r in rs),activation_rate=sum(r['activated'] for r in rs)/len(rs)) for (g,mode,m,h),rs in groups.items()]
    write_json(out/'summary.json',dict(updated=now(),planned_matches=len(planned),completed_matches=len(traces),cells=cells,semantic_discovery='not scored',scope=manifest['scope']))
    models=sorted(manifest['models'])
    if manifest['study']=='frontier':models=['gpt-5-mini','gpt-5.6-sol']
    if rows:
        pairs=[(g,h) for g in GAMES for h in INSTANCES[g]]
        fig,axes=plt.subplots(1,2,figsize=(12,7),sharey=True)
        for ax,mode in zip(axes,['cross','self']):
            mat=np.full((len(pairs),len(models)),np.nan)
            for i,(g,h) in enumerate(pairs):
                for j,m in enumerate(models):
                    rs=groups[g,mode,m,h]
                    if rs:mat[i,j]=sum(r['activated'] for r in rs)/len(rs)
            ax.imshow(mat,vmin=0,vmax=1,cmap='YlGnBu',aspect='auto')
            ax.set_xticks(range(len(models)),models,rotation=25,ha='right',fontsize=9)
            ax.set_yticks(range(len(pairs)),[g+' / '+h.replace('_',' ') for g,h in pairs],fontsize=9)
            for i,(g,h) in enumerate(pairs):
                for j,m in enumerate(models):
                    rs=groups[g,mode,m,h]
                    ax.text(j,i,f"{sum(r['activated'] for r in rs)}/{len(rs)}" if rs else 'pending',ha='center',va='center',fontsize=9,color='white' if mat[i,j]>.5 else 'black')
            ax.set_title(mode+' · engine activation')
        fig.suptitle(f"{manifest['study']} · {len(traces)}/{len(planned)} matches completed\nCounts use completed seats; activation is not semantic discovery")
        fig.tight_layout()
        for ext in ('png','svg','pdf'):fig.savefig(out/('game_hole_activations.'+ext),dpi=180)
        plt.close(fig)
        fig,axes=plt.subplots(1,2,figsize=(12,4),sharey=True)
        for ax,mode in zip(axes,['cross','self']):
            for m in models:
                values=[]
                for r in range(1,9):
                    rates=[]
                    for g,h in pairs:
                        rs=groups[g,mode,m,h]
                        if rs:rates.append(sum(x['first_round'] is not None and x['first_round']<=r for x in rs)/len(rs))
                    values.append(sum(rates)/len(rates) if rates else float('nan'))
                ax.plot(range(1,9),values,marker='o',label=m)
            ax.set_title(mode);ax.set_ylim(0,1);ax.set_xlabel('Decision round');ax.legend(fontsize=8)
        axes[0].set_ylabel('Mean cumulative instance activation rate')
        fig.suptitle('Cumulative engine activation · descriptive completed-match rates')
        fig.tight_layout()
        for ext in ('png','svg','pdf'):fig.savefig(out/('cumulative_activation.'+ext),dpi=180)
        plt.close(fig)
    (out/'README.md').write_text(f'''# {manifest['study']} engine report

{len(traces)}/{len(planned)} matches complete. {manifest['scope']}.

Engine activation, cumulative activation, split win shares and local relative-score effects are exported. Semantic discovery and intent are not scored. Missing games are not counted as zero discovery. Rates are descriptive until matched-block analysis accounts for failures and dependent observations. Frontier figures show only the two focal GPT models; raw CSVs retain anchor players. A self-play average win share is fixed by symmetry and is not a model-strength comparison.

[Game/hole activations](game_hole_activations.png) · [Cumulative activation](cumulative_activation.png)
''')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--watch',action='store_true');a=p.parse_args()
    while True:
        build(a.root)
        status=json.loads((a.root/'status.json').read_text())['status']
        if not a.watch or status!='running':break
        time.sleep(30)
