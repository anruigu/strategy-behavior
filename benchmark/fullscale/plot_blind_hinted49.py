"""Blind/hinted stars on the shared completed blind-game cohort."""
import argparse
import json
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from benchmark.fullscale.plot_gemini49 import GROUPS as ORIGINAL_GROUPS
from benchmark.fullscale.analysis_scope import included, EXCLUDED_CATEGORIES
GROUPS={g:[c for c in cs if c not in EXCLUDED_CATEGORIES] for g,cs in ORIGINAL_GROUPS.items()}
from benchmark.fullscale.plot_replicates49 import BASE,ROSTER,NAMES,COLORS
from benchmark.clients import write_json,now

EXTENSIONS=[
    ('kimi-k3','Kimi K3','#ab403c'),
    ('deepseek-v4-pro','DeepSeek V4-Pro 0813','#505cc7'),
    ('gemma-4-31b','Gemma 4 31B','#79872e'),
    ('qwen-3.5-9b','Qwen 3.5 9B','#9f5787'),
    ('gpt-oss-20b','GPT-OSS-20B','#374e58'),
]

def main(extended=False):
    roster=list(ROSTER);names=list(NAMES);colors=list(COLORS)
    progress=[]
    if extended:
        lifecycle_path=BASE/'extension-lifecycle.json'
        lifecycle=json.loads(lifecycle_path.read_text()) if lifecycle_path.exists() else {}
        for model,name,color in EXTENSIONS:
            root=BASE/model
            status=json.loads((root/'status.json').read_text()) if (root/'status.json').exists() else {'status':'pending'}
            state=lifecycle.get(model,{}).get('status',status['status'])
            progress.append(dict(model=model,status=state,phase=status.get('phase'),
                blind_complete=len(list(root.glob('episodes/blind__*/trace.json'))),
                hinted_complete=len(list(root.glob('episodes/hinted__*/trace.json'))),errors=len(status.get('errors',[]))))
            # Add only completed runs: an in-flight model must not shrink the cohort.
            if state in ('finished','finished_with_errors') and progress[-1]['blind_complete']:
                roster.append(model);names.append(name);colors.append(color)
    targets={t for t in json.loads((BASE/'targets-49.json').read_text()) if included(t)}
    assert len(targets)==45
    blind={m:{p.parent.name:json.loads(p.read_text()) for p in (BASE/m).glob('episodes/blind__*/trace.json')} for m in roster}
    common=set.intersection(*(set(v) for v in blind.values()))
    common={eid for eid in common if any(s['exploit_id'] in targets for s in blind[roster[0]][eid]['scores'])};records=[]
    for m in roster:
        by_phase={'blind':[s for eid in sorted(common) for s in blind[m][eid]['scores'] if s['exploit_id'] in targets],'hinted':[]}
        for p in (BASE/m).glob('episodes/hinted__*/trace.json'):
            t=json.loads(p.read_text())
            if f"blind__{t['game']}__s{t['seed']}" not in common:continue
            if t['target'] not in targets:continue
            original=blind[m][f"blind__{t['game']}__s{t['seed']}"]
            assert not next(s for s in original['scores'] if s['exploit_id']==t['target'])['executed']
            by_phase['hinted'].append(next(s for s in t['scores'] if s['exploit_id']==t['target']))
        expected_hints=sum(not s['executed'] for s in by_phase['blind'])
        r=dict(model=m,hints_complete=len(by_phase['hinted'])==expected_hints,expected_hinted_trials=expected_hints)
        for phase,rs in by_phase.items():
            types={}
            for cs in GROUPS.values():
                for c in cs:
                    rows=[s for s in rs if s['category']==c]
                    types[c]=dict(n=len(rows),k=sum(s['executed'] for s in rows),rate=sum(s['executed'] for s in rows)/len(rows) if rows else None)
            groups={}
            for g,cs in GROUPS.items():
                rates=[types[c]['rate'] for c in cs if types[c]['rate'] is not None]
                groups[g]=float(np.mean(rates)) if rates else None
            r[phase]=dict(types=types,groups=groups,trials=len(rs),hits=sum(s['executed'] for s in rs))
        records.append(r)
    out=BASE/('plots/filtered-45-extended' if extended else 'plots/filtered-45');out.mkdir(exist_ok=True)
    write_json(out/'blind-hinted-comparison-data.json',dict(updated=now(),common_blind_episodes=sorted(common),models=records,progress=progress,aggregation='Macro-average eligible type rates; hinted tests only each model’s own misses within common blind games. Incomplete hinted curves omitted.'))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
    fig=plt.figure(figsize=(16,9))
    angles=np.linspace(0,2*np.pi,4,endpoint=False)
    for left,phase,title in [(.10,'blind','Original blind execution'),(.61,'hinted','Hinted execution on prior misses')]:
        ax=fig.add_axes([left,.27,.29,.48],projection='polar');ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1)
        for index,(r,n,c) in enumerate(zip(records,names,colors)):
            if phase=='hinted' and not r['hints_complete']:continue
            values=[v if v is not None else np.nan for v in r[phase]['groups'].values()]
            ax.plot(np.r_[angles,angles[0]],values+[values[0]],color=c,lw=2.2,marker='o',markersize=4,
                    linestyle='--' if index>=len(ROSTER) else '-',label=n)
        ax.set_ylim(0,1);ax.set_yticks([.25,.5,.75,1],['25%','50%','75%','100%'],fontsize=9,color='#617780');ax.grid(alpha=.3)
        ax.set_xticks(angles,['Rule /\nenforcement','Information /\ninterface','State /\ntime','Multiplayer /\nobjective'],fontsize=11);ax.tick_params(axis='x',pad=15)
        ax.get_xticklabels()[1].set_ha('left');ax.get_xticklabels()[3].set_ha('right')
        fig.text(left+.145,.84,title,ha='center',fontsize=16,weight='bold',color='#193440')
        if phase=='blind':handles,labels=ax.get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.135),ncol=5,frameon=False,fontsize=11)
    fig.text(.05,.965,'Model exploit profiles · 45 eligible holes',fontsize=25,weight='bold',color='#193440')
    fig.text(.05,.914,f'{len(common)} shared completed game/seed episodes · {len(roster)} models · requested low reasoning · no reflection',fontsize=13,color='#617780')
    fig.text(.05,.08,'Each axis averages hole-type execution rates. Hinted curves use fresh, targeted attempts on each model’s own misses.',fontsize=11,color='#617780')
    fig.text(.05,.04,'Original rules disclose some effects. Hinted test items and denominators differ across models.',fontsize=11,color='#617780')
    for ext in ('png','svg','pdf'):fig.savefig(out/f'blind_hinted_star_comparison.{ext}',dpi=180,facecolor='white')
    plt.close(fig)
    if extended:
        lines=['# Expanded model comparison','',f'Updated {now()}. {len(roster)}/10 models plotted; pending runs enter after completion.',
               '', 'Same frozen engines, prompts, 49 evaluated targets, three seeds and 16,384-token allowance. The plot retains the 45-hole analysis filter and intersects completed blind episodes across plotted models.',
               '', 'Low reasoning is requested for every model. Provider handling and hidden compute differ; Gemma and Qwen expose no discrete effort levels in the catalog. Kimi and DeepSeek are included as requested comparison models, not classified as small models.',
               '', '| Added model | Blind / 57 | Hinted | Status | Errors |','|---|---:|---:|---|---:|']
        for p in progress:lines.append(f"| {p['model']} | {p['blind_complete']} | {p['hinted_complete']} | {p['status']} | {p['errors']} |")
        lines+=['','![Expanded blind/hinted comparison](blind_hinted_star_comparison.png)',
                '', 'Solid lines: original cohort. Dashed lines: added models. Hints target each model’s own misses; incomplete hinted curves are omitted. Original rules disclose some effects, so execution is not clean hidden-effect discovery.',
                '', '[Underlying counts](blind-hinted-comparison-data.json) · [SVG](blind_hinted_star_comparison.svg) · [PDF](blind_hinted_star_comparison.pdf)']
        (out/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print([(r['model'],r['hinted']['hits'],r['hinted']['trials']) for r in records],flush=True)
    return all(p['status'] in ('finished','finished_with_errors','preflight_failed','unavailable') for p in progress)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--extended',action='store_true');parser.add_argument('--watch',action='store_true');args=parser.parse_args()
    while True:
        done=main(args.extended)
        if done or not args.watch:break
        time.sleep(30)
