"""Offline live reports for the win-only prompt ablation; missing is never zero."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import time
from datetime import datetime, timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(os.environ.get('PROMPT45_PROJECT_ROOT', Path(__file__).resolve().parents[2]))
BASE = ROOT/'benchmark/results/winonly45-20260909'
NAMES = {'gemini-3.1-pro':'Gemini 3.1 Pro','gpt-5.6-sol':'GPT-5.6 Sol','grok-4.6':'Grok 4.6',
         'qwen-3.8-27b-medium':'Qwen 3.8 27B','glm':'GLM 5.3','kimi-k3':'Kimi K3',
         'deepseek-v4-pro':'DeepSeek V4-Pro 0813','gemma-4-31b':'Gemma 4 31B',
         'qwen-3.5-9b':'Qwen 3.5 9B','gpt-oss-20b':'GPT-OSS-20B'}
GROUPS = {
    'Rule / enforcement':['unchecked_self_report','unenforced_limits','undelivered_punishment','rule_order_precedence'],
    'Information / interface':['meta_rule','information_asymmetry'],
    'State / time':['resource_conversion','state_reset_refresh','resource_duplication','turn_order','phase_boundary','terminal_condition'],
    'Multiplayer / objective':['objective_substitution','sacrificial_negative_value','board_state_poisoning','denial_griefing'],
}


def summarize(rows):
    types = {}
    for category in [c for cs in GROUPS.values() for c in cs]:
        selected = [r for r in rows if r['category']==category]
        types[category] = dict(n=len(selected),k=sum(r['executed'] for r in selected),
            rate=sum(r['executed'] for r in selected)/len(selected) if selected else None)
    groups = {}
    for group,categories in GROUPS.items():
        rates=[types[c]['rate'] for c in categories if types[c]['rate'] is not None]
        groups[group]=float(np.mean(rates)) if rates else None
    return dict(n=len(rows),k=sum(r['executed'] for r in rows),
                rate=sum(r['executed'] for r in rows)/len(rows) if rows else None,types=types,groups=groups)


def aggregate(arms, targets):
    common=set(arms['win_only']) & set(arms['exploration'])
    result={'paired_episodes':len(common),'common_episode_ids':sorted(common)}
    for condition,traces in arms.items():
        rows=[s for t in traces.values() for s in t['scores'] if s['exploit_id'] in targets]
        paired=[s for key in sorted(common) for s in traces[key]['scores'] if s['exploit_id'] in targets]
        result[condition]=dict(episodes=len(traces),all=summarize(rows),paired=summarize(paired))
    return result


def build():
    plan=json.loads((BASE/'plan.json').read_text());targets=set(plan['targets']);records=[];csv_rows=[]
    for model,settings in plan['models'].items():
        root=BASE/model
        status=json.loads((root/'status.json').read_text()) if (root/'status.json').exists() else {'status':'prepared'}
        process=root/'process.json'
        if process.exists() and status['status'] in ('prepared','running'):
            pid=json.loads(process.read_text())['pid']
            proc=Path(f'/proc/{pid}/stat')
            if not proc.exists() or proc.read_text().split(') ',1)[1].split()[0]=='Z':
                status={**status,'status':'process_exited','phase':'Inspect run.log; no successful completion recorded'}
        arms={c:{} for c in plan['conditions']}
        references=root/'exploration-references.json'
        if references.exists():
            for ref in json.loads(references.read_text()):
                path=Path(ref['path']);raw=path.read_bytes()
                assert hashlib.sha256(raw).hexdigest()==ref['sha256'],'Reused control changed'
                t=json.loads(raw);arms['exploration'][f"{t['game']}__s{t['seed']}"]=t
        for condition in arms:
            for path in (root/condition/'episodes').glob('*/trace.json'):
                t=json.loads(path.read_text());arms[condition][f"{t['game']}__s{t['seed']}"]=t
        result=aggregate(arms,targets)
        result.update(model=model,name=NAMES[model],group=settings['group'],status=status['status'],
                      phase=status.get('phase'),errors=len(status.get('errors',[])),reasoning=settings['config']['reasoning_effort'])
        records.append(result)
        common=set(result['common_episode_ids'])
        for condition,traces in arms.items():
            for key,t in traces.items():
                for s in t['scores']:
                    if s['exploit_id'] in targets:
                        csv_rows.append(dict(model=model,group=settings['group'],condition=condition,game=t['game'],seed=t['seed'],
                            target=s['exploit_id'],category=s['category'],executed=int(s['executed']),paired=key in common))
    out=BASE/'plots';out.mkdir(exist_ok=True)
    updated=datetime.now(timezone.utc).isoformat()
    data=dict(updated=updated,models=records,targets=sorted(targets),groups=GROUPS,
        note='Behavioral activation. Missing episodes omitted. Prompt comparisons use identical game/seed pairs within each model. Three seeds; descriptive results. Requested effort differs across models but is fixed within model.')
    temp=out/'comparison-data.json.tmp';temp.write_text(json.dumps(data,indent=2)+'\n');temp.replace(out/'comparison-data.json')
    with (out/'hole-seed-activation.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=['model','group','condition','game','seed','target','category','executed','paired'])
        writer.writeheader();writer.writerows(csv_rows)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
    for paired,filename,title in [(False,'win_only_activation','Hole activation with only a winning objective'),
                                  (True,'prompt_comparison','Winning alone versus active exploration')]:
        fig,axes=plt.subplots(1,2,figsize=(16,7.5));fig.subplots_adjust(left=.16,right=.94,bottom=.20,top=.79,wspace=.82)
        for ax,group in zip(axes,['frontier','open']):
            selected=[r for r in records if r['group']==group]
            ax.set_title('Frontier models' if group=='frontier' else 'Open models',pad=18,weight='bold')
            ax.set_yticks(range(len(selected)),[r['name'] for r in selected]);ax.invert_yaxis()
            ax.set_xlim(-.015,1.2);ax.set_xticks([0,.25,.5,.75,1],['0%','25%','50%','75%','100%'])
            ax.set_ylim(len(selected)-.5,-.5);ax.grid(axis='x',alpha=.18)
            ax.spines[['top','right','left']].set_visible(False)
            for y,r in enumerate(selected):
                scope='paired' if paired else 'all'
                normal=r['win_only'][scope];explore=r['exploration'][scope]
                if normal['rate'] is None:
                    ax.text(.02,y,'Pending' if r['status']!='preflight_failed' else 'Initial episode incomplete',va='center',color='#7c858d',fontsize=9)
                    continue
                if paired:
                    ax.plot([normal['rate'],explore['rate']],[y,y],color='#bcc4cc',lw=2)
                    ax.scatter(explore['rate'],y,c='#d17c34',s=55,label='Exploration' if y==0 else None,zorder=3)
                ax.scatter(normal['rate'],y,c='#287ba4',s=55,label='Win only' if y==0 else None,zorder=4)
                ax.text(1.03,y,f"{normal['k']}/{normal['n']}" if not paired else f"n={normal['n']}",va='center',fontsize=9)
            ax.set_xlabel('Activated hole × seed opportunities / completed opportunities')
        if paired:
            from matplotlib.lines import Line2D
            fig.legend([Line2D([],[],marker='o',ls='',color='#287ba4'),Line2D([],[],marker='o',ls='',color='#d17c34')],
                       ['Win only','Active exploration'],loc='lower center',bbox_to_anchor=(.5,.10),ncol=2,frameon=False)
        fig.suptitle(title,fontsize=23,weight='bold',y=.96)
        fig.text(.05,.885,'Revised games · 45 holes · 17 editions × 3 seeds · no hints, reflection or cross-game memory',fontsize=12,color='#617780')
        fig.text(.05,.045,'Incomplete episodes are omitted. Paired comparisons match games/seeds within model; model cohorts may differ while running.',fontsize=10,color='#617780')
        for ext in ['png','svg','pdf']:fig.savefig(out/(filename+'.'+ext),dpi=170,facecolor='white')
        plt.close(fig)
    # Separate familiar star plot: require a full grid to avoid changing axis composition.
    fig,axes=plt.subplots(1,2,figsize=(16,9),subplot_kw={'projection':'polar'})
    fig.subplots_adjust(left=.13,right=.87,bottom=.26,top=.77,wspace=.80)
    angles=np.linspace(0,2*np.pi,4,endpoint=False)
    for ax,group in zip(axes,['frontier','open']):
        ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1);ax.set_ylim(0,1)
        ax.set_xticks(angles,[s.replace(' / ',' /\n') for s in GROUPS]);ax.tick_params(axis='x',pad=18)
        ax.set_yticks([.25,.5,.75,1],['25%','50%','75%','100%'],fontsize=8,color='#617780');ax.grid(alpha=.25)
        ax.set_title('Frontier models' if group=='frontier' else 'Open models',pad=45,weight='bold')
        selected=[r for r in records if r['group']==group and r['win_only']['all']['n']==135]
        for index,r in enumerate(selected):
            values=list(r['win_only']['all']['groups'].values())
            ax.plot(np.r_[angles,angles[0]],values+[values[0]],marker='o',lw=2,label=r['name'])
        if not selected:ax.text(.5,.5,'Waiting for complete\nwin-only grids',ha='center',va='center',transform=ax.transAxes)
        else:ax.legend(loc='upper center',bbox_to_anchor=(.5,-.19),fontsize=9,ncol=2,frameon=False)
    fig.suptitle('Win-only activation profiles',fontsize=24,weight='bold',y=.95)
    fig.text(.5,.89,'45 eligible holes · type-averaged axes · complete 135-opportunity grids only',ha='center',fontsize=12,color='#617780')
    for ext in ['png','svg','pdf']:fig.savefig(out/('win_only_profiles.'+ext),dpi=170,facecolor='white')
    plt.close(fig)
    lines=['# Win-only versus exploration on revised games','',f'Updated {updated}.','',
           'The only prompt change is removal of the exploration paragraph. All models keep the same winning objective and action instructions. Rules, native scripted opponents, 45 targets, three seeds and token limits are held fixed within each model. No hints or reflection.',
           '', '| Model | Win-only episodes / 51 | Exploration episodes / 51 | Matched opportunities / 135 | Win-only → exploration activation | Status | Errors |',
           '|---|---:|---:|---:|---|---|---:|']
    for r in records:
        n=r['win_only']['paired']['n']
        effect=f"{r['win_only']['paired']['k']}/{n} → {r['exploration']['paired']['k']}/{n}" if n else 'pending'
        lines.append(f"| {r['name']} | {r['win_only']['episodes']} | {r['exploration']['episodes']} | {n} | {effect} | {r['status']} ({r.get('phase') or '—'}) | {r['errors']} |")
    lines+=['','## Win-only activation','','![Win-only activation](plots/win_only_activation.png)',
            '', '## Matched prompt comparison','','![Matched comparison](plots/prompt_comparison.png)',
            '', '## Win-only profiles','','![Win-only profiles](plots/win_only_profiles.png)',
            '', 'Plots measure behavioral activation, not verified understanding or causal advantage. Missing episodes are omitted, never counted as zeros. Pairing fixes game/seed composition within each model; incomplete model cohorts may differ. Three seeds support descriptive comparisons only.',
            '', 'Reasoning is matched within model: frontier high, GLM high, Qwen 27B medium, added open models low. Provider handling differs; this is not a controlled compute-tier comparison. New open-model exploration controls use revised games, not the older disclosed-rules runs.',
            '', '[Exact prompts, roster and protocol](plan.json) · [Counts and rates](plots/comparison-data.json) · [Hole/seed CSV](plots/hole-seed-activation.csv)',
            '', '[Earlier September 8 live-game comparison](../v3-small-explore-20260908/COMPARISON.md) had 0% win-only useful activation on Seven Seal and mixed Auction results. It used older live games and is historical context, not a matched control.']
    (BASE/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print(updated,[(r['model'],r['win_only']['episodes'],r['exploration']['episodes'],r['status']) for r in records],flush=True)
    return all(r['status'] in ('finished','finished_with_errors','preflight_failed','process_exited') for r in records)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--watch',action='store_true');args=parser.parse_args()
    while True:
        done=build()
        if done or not args.watch:break
        time.sleep(30)
