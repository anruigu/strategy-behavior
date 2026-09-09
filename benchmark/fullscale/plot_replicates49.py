"""Continuously render complete-cohort model comparisons; never plot missing runs as zero."""
from pathlib import Path
import json,time,argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from benchmark.fullscale.plot_gemini49 import GROUPS,LABELS
from benchmark.clients import write_json,now

BASE=Path('/shared/allie/strategy-behavior/benchmark/results/small-engine49-20260909')
ROSTER=['qwen-3.8-27b','glm','claude-haiku-4.5','gpt-5-mini','gemini-3.7-flash']
NAMES=['Qwen 3.8 27B','GLM 5.3','Haiku 4.5','GPT-5 mini','Gemini 3.7 Flash']
COLORS=['#287ba4','#269575','#ce8231','#9267b8','#cc5473']

def build():
    out=BASE/'plots';out.mkdir(parents=True,exist_ok=True)
    data=[];progress=[]
    for model,name,color in zip(ROSTER,NAMES,COLORS):
        root=BASE/model
        status=json.loads((root/'status.json').read_text()) if (root/'status.json').exists() else {'status':'pending'}
        n=len(list(root.glob('episodes/blind__*/trace.json')))
        h=len(list(root.glob('episodes/hinted__*/trace.json')))
        progress.append(dict(model=model,blind_complete=n,hinted_complete=h,status=status['status'],errors=len(status.get('errors',[]))))
        if not (root/'coverage.json').exists():continue
        rows=[r for r in json.loads((root/'coverage.json').read_text())['rows'] if r['targeted']]
        # A completed blind grid is required for comparable profiles.
        if len(rows)!=49 or any(r['blind']['complete_episodes']!=3 for r in rows):continue
        planned=json.loads((root/'hinted-schedule.json').read_text()) if (root/'hinted-schedule.json').exists() else None
        hints_complete=planned is not None and h==len(planned)
        rates={}
        for phase in ('blind','hinted'):
            rates[phase]={}
            for cs in GROUPS.values():
                for c in cs:
                    rs=[r for r in rows if r['category']==c];total=sum(r[phase]['complete_episodes'] for r in rs)
                    rates[phase][c]=sum(r[phase]['executed'] for r in rs)/total if total else None
        data.append(dict(model=model,name=name,color=color,rates=rates,hints_complete=hints_complete))
    write_json(out/'comparison-data.json',dict(updated=now(),progress=progress,data=data,groups=GROUPS,reasoning='low',note='Incomplete blind grids omitted; hinted curves require all scheduled follow-ups. Hinted rates condition on model-specific blind misses.'))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,2,figsize=(14,7.6),subplot_kw={'projection':'polar'})
    fig.subplots_adjust(left=.12,right=.88,top=.77,bottom=.26,wspace=.62)
    angles=np.linspace(0,2*np.pi,4,endpoint=False)
    labels=['Rule /\nenforcement','Information /\ninterface','State /\ntime','Multiplayer /\nobjective']
    for ax,phase in zip(axes,['blind','hinted']):
        ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1);ax.set_ylim(0,1)
        ax.set_xticks(angles,labels);ax.tick_params(axis='x',pad=15)
        ax.set_yticks([.25,.5,.75,1],['25%','50%','75%','100%'],fontsize=8,color='#64757e');ax.grid(alpha=.3)
        plotted=0
        for d in data:
            if phase=='hinted' and not d['hints_complete']:continue
            values=[]
            for cs in GROUPS.values():
                vs=[d['rates'][phase][c] for c in cs if d['rates'][phase][c] is not None]
                values.append(float(np.mean(vs)) if vs else np.nan)
            ax.plot(np.r_[angles,angles[0]],values+[values[0]],color=d['color'],lw=2,marker='o',label=d['name']);plotted+=1
        ax.set_title('Unaided execution' if phase=='blind' else 'Hinted rescue of previous misses',pad=42,fontsize=13)
        if not plotted:ax.text(.5,.5,'Waiting for complete\nmodel runs',transform=ax.transAxes,ha='center',va='center',bbox=dict(facecolor='white',edgecolor='none'))
    handles,labels_=axes[0].get_legend_handles_labels()
    if handles:fig.legend(handles,labels_,loc='lower center',bbox_to_anchor=(.5,.135),ncol=3,frameon=False)
    fig.suptitle('Small-model exploit profiles · matched 49-hole audit',fontsize=21,y=.96)
    fig.text(.5,.895,'Same frozen engines, prompts, 3 seeds and 16,384-token cap · common low reasoning · no reflection',ha='center',fontsize=11)
    fig.text(.04,.075,'Each axis averages eligible hole-type rates. Hints provide fresh, targeted attempts on each model’s own misses.',fontsize=10)
    fig.text(.04,.035,f'Complete blind grids: {len(data)}/5 models. Incomplete grids are omitted, not counted as zero. Engine activation is not verified discovery.',fontsize=10)
    for ext in ('png','svg','pdf'):fig.savefig(out/f'model_star_comparison.{ext}',dpi=180)
    plt.close(fig)
    cats=[c for cs in GROUPS.values() for c in cs if c not in ('information_overflow','signaling_encoding','threat_commitment')]
    matrix=np.array([[d['rates']['blind'][c] for c in cats] for d in data]) if data else np.full((1,len(cats)),np.nan)
    fig,ax=plt.subplots(figsize=(15,6));fig.subplots_adjust(left=.15,right=.97,top=.77,bottom=.42)
    cmap=plt.get_cmap('YlGnBu').copy();cmap.set_bad('#e9edf0')
    ax.imshow(matrix,vmin=0,vmax=1,cmap=cmap,aspect='auto');ax.set_yticks(range(len(data) or 1),[d['name'] for d in data] or ['Pending'])
    ax.set_xticks(range(len(cats)),[LABELS[c] for c in cats],rotation=50,ha='right',fontsize=9)
    for i in range(len(data)):
        for j in range(len(cats)):ax.text(j,i,f'{matrix[i,j]:.0%}',ha='center',va='center',fontsize=9,color='white' if matrix[i,j]>.55 else '#183440')
    fig.suptitle('Unaided exploit execution by model and hole type',fontsize=20,y=.95)
    fig.text(.15,.84,'Only complete 49-hole × 3-seed grids are shown; three entirely excluded types are omitted.',fontsize=11)
    for ext in ('png','svg','pdf'):fig.savefig(out/f'model_type_heatmap.{ext}',dpi=180)
    plt.close(fig)
    lines=['# Small-model 49-hole replication','',f'Updated {now()}. All new runs use common low reasoning; original high-reasoning Gemini results are separate.','', '| Model | Blind episodes / 57 | Hinted episodes | Status | Errors |','|---|---:|---:|---|---:|']
    for r in progress:lines.append(f"|{r['model']}|{r['blind_complete']}|{r['hinted_complete']}|{r['status']}|{r['errors']}|")
    lines+=['','![Model star comparison](plots/model_star_comparison.png)','','![Model/type rates](plots/model_type_heatmap.png)']
    (BASE/'REPORT.md').write_text('\n'.join(lines)+'\n')
    return all(p['status'] in ('finished','finished_with_errors','preflight_failed','unavailable') for p in progress)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--watch',action='store_true');a=p.parse_args()
    while True:
        done=build()
        if done or not a.watch:break
        time.sleep(30)
