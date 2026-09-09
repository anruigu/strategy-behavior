"""Interim blind profiles on exactly the same completed episodes for every model."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from benchmark.fullscale.plot_gemini49 import GROUPS,LABELS
from benchmark.fullscale.plot_replicates49 import BASE,ROSTER,NAMES,COLORS
from benchmark.clients import write_json,now

def main():
    targets=set(json.loads((BASE/'targets-49.json').read_text()))
    runs={m:{p.parent.name:json.loads(p.read_text()) for p in (BASE/m).glob('episodes/blind__*/trace.json')} for m in ROSTER}
    common=set.intersection(*(set(r) for r in runs.values()))
    rows=[];model_rows=[]
    for m in ROSTER:
        results=[s for eid in sorted(common) for s in runs[m][eid]['scores'] if s['exploit_id'] in targets]
        entry=dict(model=m,episodes=len(common),trials=len(results),hits=sum(s['executed'] for s in results),types={},groups={})
        for cs in GROUPS.values():
            for c in cs:
                rs=[s for s in results if s['category']==c]
                entry['types'][c]=sum(s['executed'] for s in rs)/len(rs) if rs else None
        for g,cs in GROUPS.items():
            rates=[entry['types'][c] for c in cs if entry['types'][c] is not None];entry['groups'][g]=float(np.mean(rates)) if rates else None
        model_rows.append(entry)
    out=BASE/'plots';out.mkdir(exist_ok=True)
    write_json(out/'matched-progress-data.json',dict(updated=now(),common_episode_ids=sorted(common),models=model_rows))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
    fig=plt.figure(figsize=(12,8.7));ax=fig.add_axes([.18,.24,.49,.53],projection='polar')
    angles=np.linspace(0,2*np.pi,4,endpoint=False);ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1)
    for r,n,c in zip(model_rows,NAMES,COLORS):
        values=list(r['groups'].values());ax.plot(np.r_[angles,angles[0]],values+[values[0]],color=c,lw=2.5,marker='o',markersize=5,label=n)
    ax.set_ylim(0,1);ax.set_yticks([.25,.5,.75,1],['25%','50%','75%','100%'],fontsize=9,color='#617780');ax.grid(alpha=.3)
    ax.set_xticks(angles,['Rule /\nenforcement','Information /\ninterface','State /\ntime','Multiplayer /\nobjective']);ax.tick_params(axis='x',pad=20);ax.get_xticklabels()[1].set_ha('left');ax.get_xticklabels()[3].set_ha('right')
    ax.legend(loc='center left',bbox_to_anchor=(1.4,.5),frameon=False,fontsize=12)
    fig.text(.05,.955,'Unaided exploit profiles · completed runs',fontsize=23,weight='bold',color='#193440')
    fig.text(.05,.902,f'Matched completed-episode comparison · {len(common)}/57 episodes completed by all five models',fontsize=13,color='#193440')
    fig.text(.05,.858,f"{model_rows[0]['trials']} identical hole × seed opportunities per model · common low reasoning",fontsize=11,color='#617780')
    fig.text(.05,.10,'Axes equally weight included hole-type execution rates. Incomplete episodes are removed for every model.',fontsize=11,color='#617780')
    fig.text(.05,.062,'Three seeds · fixed native referee opponents · no reflection · engine activation, not verified understanding.',fontsize=10,color='#617780')
    fig.text(.05,.025,'The earlier high-reasoning Gemini run is separate; this chart uses the matched low-reasoning reference.',fontsize=10,color='#617780')
    for ext in ('png','svg','pdf'):fig.savefig(out/f'matched_interim_star.{ext}',dpi=180)
    plt.close(fig)
    print(json.dumps(model_rows,indent=2))
if __name__=='__main__':main()
