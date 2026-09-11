"""Static research figures from saved CSVs; no inference calls."""
import argparse
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from .coverage_matrix import CATEGORIES

LABELS = {
 'qwen-3.8-27b':'Qwen 3.8 27B', 'kimi-k3':'Kimi K3', 'glm':'GLM 5.3',
 'claude-haiku-4.5':'Claude Haiku 4.5','gpt-5-mini':'GPT-5 mini','gemini-3.7-flash':'Gemini 3.7 Flash'}


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def draw(out):
    out=Path(out)
    cfg=json.loads((out/'config.json').read_text())
    summary=json.loads((out/'summary.json').read_text())
    coverage=f'{summary["scored_games"]}/{summary["expected_games"]} games scored'
    if summary['scored_games']!=summary['expected_games']:
        coverage+=' · provisional'
    models=cfg['args']['models']
    memory='Persistent playbook' if cfg['args']['condition']=='persistent' else 'Fresh games'
    scope='one randomized-order chain per model' if cfg['args']['scope']=='cross-game' else 'separate within-game chains'
    curve_note='Cross-game memory persists' if cfg['args']['scope']=='cross-game' and cfg['args']['condition']=='persistent' else 'No cross-game memory'
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    for filename,field,columns,title in [
            ('model_by_exploit','category',list(CATEGORIES),'Discovery by exploit category'),
            ('model_by_game','game_id',cfg['args']['games'],'Discovery by game')]:
        rows=read(out/(filename+'.csv'))
        lookup={(r['model_id'],r[field]):r for r in rows}
        data=np.array([[float(lookup[m,c]['discovery_rate']) if lookup[m,c]['discovery_rate'] else np.nan for c in columns] for m in models])
        fig,ax=plt.subplots(figsize=(max(8,len(columns)*0.95),3.8))
        cmap=plt.get_cmap('YlGnBu').copy()
        cmap.set_bad('#dddddd')
        im=ax.imshow(np.ma.masked_invalid(data),vmin=0,vmax=1,cmap=cmap,aspect='auto')
        ax.set_yticks(range(len(models)),[LABELS[m] for m in models])
        ax.set_xticks(range(len(columns)),[c.removeprefix('gen_').removeprefix('ref_').removeprefix('ta_').replace('_',' ') for c in columns],rotation=40,ha='right')
        for y in range(len(models)):
            for x in range(len(columns)):
                value=data[y,x]
                ax.text(x,y,'—' if np.isnan(value) else f'{100*value:.0f}%',ha='center',va='center',fontsize=9,
                        color='white' if not np.isnan(value) and value>0.55 else '#1f2937')
        ax.set_title(title+'\n'+memory+' · '+scope+'\n'+coverage,loc='left',pad=15)
        cb=fig.colorbar(im,ax=ax,pad=.02,shrink=.9)
        cb.ax.set_ylabel('Specified opportunities discovered')
        cb.set_ticks([0,.25,.5,.75,1],labels=['0%','25%','50%','75%','100%'])
        fig.tight_layout()
        for ext in ('png','pdf'):
            fig.savefig(out/(filename+'.'+ext),dpi=180,bbox_inches='tight')
        plt.close(fig)
    rows=read(out/'by_iteration.csv')
    fig,ax=plt.subplots(figsize=(8,4.3))
    for m in models:
        rs=sorted([r for r in rows if r['model_id']==m],key=lambda r:int(r['iteration']))
        xs=[int(r['iteration']) for r in rs]
        ys=[100*float(r['discovery_rate']) if r['discovery_rate'] else np.nan for r in rs]
        ax.plot(xs,ys,marker='o',label=LABELS[m],linewidth=2)
    ax.set(xticks=range(1,cfg['args']['iterations']+1),ylim=(-2,102),xlabel='Within-game iteration',ylabel='Discovery rate (%)')
    ax.set_title('Articulated discovery across repetitions\n'+curve_note+'; curves are descriptive, not independent-seed estimates\n'+coverage,loc='left',pad=12)
    ax.grid(axis='y',alpha=.2)
    ax.legend(loc='upper left',bbox_to_anchor=(1.01,1),frameon=False)
    fig.tight_layout()
    for ext in ('png','pdf'):
        fig.savefig(out/('learning_curves.'+ext),dpi=180,bbox_inches='tight')
    plt.close(fig)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    draw(args.output)
