"""Extra descriptive figures over completed live-pilot traces; no model calls."""
import argparse,json
from pathlib import Path
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from .live_pilot import summarize,SMALL
from .live_games import GAMES,HOLES


def analyze(out):
    data=summarize(out)
    seats=data['seats']
    if not seats: return
    traces=[json.loads(p.read_text()) for p in sorted((out/'matches').glob('*/trace.json'))]
    labels=['Haiku 4.5','GPT-5 mini','Gemini Flash']
    fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True)
    for ax,game in zip(axes,GAMES):
        rows=[s for s in seats if s['game']==game and s['mode']=='cross']
        vals=[sum(s['win_share'] for s in rows if s['model']==m)/sum(s['model']==m for s in rows) if any(s['model']==m for s in rows) else float('nan') for m in SMALL]
        ax.bar(labels,vals); ax.axhline(1/3,color='gray',ls='--',lw=1)
        ax.set_title(game+f' · {len(rows)//3} cross-play matches');ax.set_ylim(0,1);ax.set_ylabel('Split win rate')
    fig.suptitle('Cross-family win shares · ties divided among winners')
    fig.tight_layout();fig.savefig(out/'wins.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(11,7),sharex=True,sharey=True)
    for gi,game in enumerate(GAMES):
        for mi,mode in enumerate(('cross','self')):
            ax=axes[gi,mi]
            for model,label in zip(SMALL,labels):
                histories=[]
                for t in traces:
                    if t['game']!=game or t['mode']!=mode: continue
                    for p,m in enumerate(t['seats']):
                        if m!=model: continue
                        seen=set(); vals=[]
                        for r in range(1,9):
                            if r<=len(t['rounds']): seen.update(t['rounds'][r-1]['events'][p]['executed'])
                            vals.append(len(seen)/len(HOLES[game]))
                        histories.append(vals)
                if histories: ax.plot(range(1,9),np.mean(histories,axis=0),marker='o',label=f'{label} (n={len(histories)})')
            ax.set_title(game+' · '+mode);ax.set_ylim(0,1);ax.set_xticks(range(1,9))
            ax.set_xlabel('Within-match round');ax.set_ylabel('Fraction of four mechanisms ever activated')
            if ax.lines: ax.legend(fontsize=7)
    fig.suptitle('Cumulative mechanical activation, not articulated discovery\nCompleted-match denominator; early-ended games carry their final value forward')
    fig.tight_layout();fig.savefig(out/'cumulative_execution.png',dpi=160);plt.close(fig)
    pairs=[(g,h) for g in GAMES for h in HOLES[g]]
    fig,axes=plt.subplots(1,2,figsize=(15,6))
    for ax,mode in zip(axes,('cross','self')):
        mat=[]
        for g,h in pairs:
            row=[]
            for m in SMALL:
                eligible=[s for s in seats if s['game']==g and s['mode']==mode and s['model']==m and s['discovered'] is not None]
                row.append(sum(h in s['discovered'] for s in eligible)/len(eligible) if eligible else float('nan'))
            mat.append(row)
        ax.imshow(mat,vmin=0,vmax=1,cmap='YlGnBu',aspect='auto')
        ax.set_xticks(range(3),labels);ax.set_yticks(range(8),[g+': '+h for g,h in pairs],fontsize=8)
        ax.set_title(mode+' · articulated discovery per judged seat')
        for i,row in enumerate(mat):
            for j,v in enumerate(row):ax.text(j,i,'pending' if np.isnan(v) else f'{v:.0%}',ha='center',va='center',fontsize=9)
    fig.tight_layout();fig.savefig(out/'discovery.png',dpi=160);plt.close(fig)
    rows=[]
    for s in seats:
        for h in HOLES[s['game']]:
            rows.append(dict(match=s['match'],mode=s['mode'],game=s['game'],pid=s['pid'],model=s['model'],hole=h,
                             executed=h in s['executed'],patch_sensitive=h in s['patch_sensitive'],
                             discovered=None if s['discovered'] is None else h in s['discovered'],win_share=s['win_share']))
    import csv
    with (out/'seat_hole_metrics.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/'FIGURES.md').write_text('\n'.join(['# Live-pilot figures',
      'All figures use completed matches only. Read REPORT.md for denominators, scope and limitations.',
      *[f'\n![{label}]({file})' for label,file in [('Behavior','behavior.png'),('Win shares','wins.png'),('Execution by hole','holes.png'),('Articulated discovery','discovery.png'),('Cumulative execution','cumulative_execution.png')]]]))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();analyze(a.out)
