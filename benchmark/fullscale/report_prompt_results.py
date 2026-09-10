"""One offline report for three prompt conditions, preserving protocol boundaries."""
import argparse
import ast
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
RESULTS=ROOT/'benchmark/results'
OUT=RESULTS/'prompt-results-20260909'
CANONICAL=ROOT/'research_logs/sep/model-prompt-results.md'
WIN=RESULTS/'winonly45-20260909'
PHASES=['win_only','exploration','hinted']
PHASE_NAMES={'win_only':'Win only','exploration':'Exploration','hinted':'Hinted rescue'}
NAMES={'gemini-3.1-pro':'Gemini 3.1 Pro','gpt-5.6-sol':'GPT-5.6 Sol','grok-4.6':'Grok 4.6',
       'qwen-3.8-27b-medium':'Qwen 3.8 27B','qwen-3.8-27b':'Qwen 3.8 27B', 'glm':'GLM 5.3',
       'kimi-k3':'Kimi K3','deepseek-v4-pro':'DeepSeek V4-Pro 0813','gemma-4-31b':'Gemma 4 31B',
       'qwen-3.5-9b':'Qwen 3.5 9B','gpt-oss-20b':'GPT-OSS-20B',
       'gemini-3.7-flash':'Gemini 3.7 Flash','claude-haiku-4.5':'Haiku 4.5','gpt-5-mini':'GPT-5 mini'}
CONSTANTS={}
for node in ast.parse((ROOT/'benchmark/fullscale/plot_gemini49.py').read_text()).body:
    if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('GROUPS','LABELS'):
        CONSTANTS[node.targets[0].id]=ast.literal_eval(node.value)
LABELS=CONSTANTS['LABELS']


def load(path):return json.loads(path.read_text())

def rows_from_trace(trace,path,targets,phase):
    if phase=='hinted':
        assert trace['target'] is not None
    else:
        assert trace['target'] is None
    return [dict(target=s['exploit_id'],category=s['category'],game=trace['game'],seed=trace['seed'],
                 executed=bool(s['executed']),source=str(path)) for s in trace['scores']
            if s['exploit_id'] in targets and (phase!='hinted' or s['exploit_id']==trace['target'])]


def summarize(rows,targets,groups):
    cells={}
    for target in targets:
        selected=[r for r in rows if r['target']==target]
        assert len({r['seed'] for r in selected})==len(selected),'Duplicate target/seed'
        cells[target]=dict(n=len(selected),k=sum(r['executed'] for r in selected),
            rate=sum(r['executed'] for r in selected)/len(selected) if selected else None)
    types={}
    for category in [c for cs in groups.values() for c in cs]:
        selected=[r for r in rows if r['category']==category]
        types[category]=dict(n=len(selected),k=sum(r['executed'] for r in selected),
            rate=sum(r['executed'] for r in selected)/len(selected) if selected else None)
    rates={}
    for group,categories in groups.items():
        values=[types[c]['rate'] for c in categories if types[c]['rate'] is not None]
        rates[group]=float(np.mean(values)) if values else None
    n=len(rows);k=sum(r['executed'] for r in rows)
    return dict(n=n,k=k,rate=k/n if n else None,types=types,groups=rates,cells=cells)


def finish_record(model,group,reasoning,rows,supported,targets,groups,status,sources):
    result=dict(model=model,name=NAMES[model],group=group,reasoning=reasoning,status=status,sources=sources)
    expected_hints=sum(not r['executed'] for r in rows['exploration'])
    baseline={(r['target'],r['seed']):r for r in rows['exploration']}
    for row in rows['hinted']:
        assert (row['target'],row['seed']) in baseline and not baseline[(row['target'],row['seed'])]['executed'],'Hint does not correspond to an exploration miss'
    for phase in PHASES:
        result[phase]=summarize(rows[phase],targets,groups)
        result[phase]['supported']=supported[phase]
        result[phase]['expected']=expected_hints if phase=='hinted' else len(targets)*3
        result[phase]['complete']=supported[phase] and result[phase]['n']==result[phase]['expected'] and (phase!='hinted' or len(rows['exploration'])==len(targets)*3)
    normal={(r['target'],r['seed']):r for r in rows['win_only']}
    common=normal.keys() & baseline.keys()
    result['paired']=dict(n=len(common),win_only=sum(normal[k]['executed'] for k in common),exploration=sum(baseline[k]['executed'] for k in common))
    return result


def collect():
    plan=load(WIN/'plan.json');targets=plan['targets']
    groups={g:[c for c in cs if any(t.endswith('.'+c) for t in targets)] for g,cs in CONSTANTS['GROUPS'].items()}
    titles={};allrows=[];records=[]
    models={**plan['models'],'gemini-3.7-flash':dict(group='reference',config={'reasoning_effort':'high'})}
    def ingest(path,phase,rows):
        t=load(path)
        if t['turns']:
            card=json.JSONDecoder().raw_decode(t['turns'][0]['observation'].split('\nCard: ',1)[1])[0]
            titles[t['game']]=card['title']
        rows[phase].extend(rows_from_trace(t,path,targets,phase))
    for model,settings in models.items():
        rows={p:[] for p in PHASES};sources=[];root=WIN/model
        supported={p:False for p in PHASES}
        if model in plan['models']:
            supported['win_only']=supported['exploration']=True
            for phase in ['win_only','exploration']:
                for path in sorted((root/phase/'episodes').glob('*/trace.json')):ingest(path,phase,rows)
            if (root/'exploration-references.json').exists():
                for ref in load(root/'exploration-references.json'):
                    path=Path(ref['path']);assert hashlib.sha256(path.read_bytes()).hexdigest()==ref['sha256']
                    ingest(path,'exploration',rows)
            sources.append(str(root))
        hintroot=(RESULTS/'frontier45-20260909'/model if settings['group']=='frontier' else
                  RESULTS/'gemini-revised45-20260909' if model=='gemini-3.7-flash' else None)
        if hintroot is not None:
            manifest=load(hintroot/'manifest.json')
            assert manifest['sources']==plan['sources'] and manifest['system_prompt']==plan['conditions']['exploration']
            if model in plan['models']:assert manifest['model']==settings['config']
            supported['hinted']=supported['exploration']=True
            for path in sorted((hintroot/'episodes').glob('hinted__*/trace.json')):ingest(path,'hinted',rows)
            if model=='gemini-3.7-flash':
                for path in sorted((hintroot/'episodes').glob('blind__*/trace.json')):ingest(path,'exploration',rows)
            sources.append(str(hintroot))
        status=load(root/'status.json').get('status') if (root/'status.json').exists() else 'reference'
        if status=='running' and (root/'process.json').exists():
            proc=Path('/proc')/str(load(root/'process.json')['pid'])/'stat'
            if not proc.exists() or proc.read_text().split(') ',1)[1].split()[0]=='Z':status='process_exited'
        records.append(finish_record(model,settings['group'],settings['config']['reasoning_effort'],rows,supported,targets,groups,status,sources))
        for phase in PHASES:
            allrows.extend(dict(protocol='revised45',model=model,phase=phase,**r) for r in rows[phase])
    legacy=[];old=RESULTS/'small-engine49-20260909'
    for model in ['qwen-3.8-27b','glm','claude-haiku-4.5','gpt-5-mini','gemini-3.7-flash','kimi-k3','deepseek-v4-pro','gemma-4-31b','gpt-oss-20b']:
        root=old/model
        if not (root/'manifest.json').exists():continue
        rows={p:[] for p in PHASES}
        for phase,pattern in [('exploration','blind__*'),('hinted','hinted__*')]:
            for path in sorted((root/'episodes').glob(pattern+'/trace.json')):ingest(path,phase,rows)
        # Filter to the same 45 eligible IDs, while retaining the historical protocol label.
        rec=finish_record(model,'historical','low',rows,dict(win_only=False,exploration=True,hinted=True),targets,groups,
                          load(root/'status.json')['status'],[str(root)])
        legacy.append(rec)
        for phase in PHASES:allrows.extend(dict(protocol='historical49-filtered45',model=model,phase=phase,**r) for r in rows[phase])
    return dict(updated=datetime.now(timezone.utc).isoformat(),targets=targets,groups=groups,titles=titles,
                models=records,historical_models=legacy),allrows


def save(fig,name):
    for ext in ['png','svg','pdf']:fig.savefig(OUT/'plots'/f'{name}.{ext}',dpi=150,bbox_inches='tight',facecolor='white')
    plt.close(fig)


def stars(records,groups,name,title,phases=PHASES):
    fig,axes=plt.subplots(1,len(phases),figsize=(7.7*len(phases),8),subplot_kw={'projection':'polar'},squeeze=False)
    fig.subplots_adjust(left=.08,right=.92,top=.72,bottom=.25,wspace=.80)
    angles=np.linspace(0,2*np.pi,4,endpoint=False);colors=plt.get_cmap('tab10').colors
    for ax,phase in zip(axes[0],phases):
        drawn=0
        for i,r in enumerate(records):
            stats=r[phase]
            values=[v if v is not None else np.nan for v in stats['groups'].values()]
            if not stats['n'] or not np.isfinite(values).all():continue
            ax.plot(np.r_[angles,angles[0]],values+[values[0]],color=colors[i%10],marker='o',lw=2,
                    ls='-' if stats['complete'] else '--',label=r['name']);drawn+=1
        ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1);ax.set_ylim(0,1)
        ax.set_xticks(angles,['Rule /\nenforcement','Information /\ninterface','State /\ntime','Multiplayer /\nobjective']);ax.tick_params(axis='x',pad=18)
        ax.get_xticklabels()[1].set_ha('left');ax.get_xticklabels()[3].set_ha('right')
        ax.set_yticks([.25,.5,.75,1],['25%','50%','75%','100%'],fontsize=8,color='#667888');ax.grid(alpha=.25)
        ax.set_title(PHASE_NAMES[phase],pad=43,fontsize=16)
        if not drawn:ax.text(.5,.5,'No comparable results\nwith all four axes yet',ha='center',va='center',transform=ax.transAxes,fontsize=11)
    from matplotlib.lines import Line2D
    handles=[Line2D([],[],color=colors[i%10],marker='o',lw=2,label=r['name']) for i,r in enumerate(records)]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.115),ncol=min(5,len(handles)),frameon=False,fontsize=11)
    fig.suptitle(title,fontsize=24,weight='bold',y=.965)
    fig.text(.5,.89,'45 eligible holes · original broad-group assignments · equal-weight average of observed type rates',ha='center',fontsize=12,color='#617780')
    fig.text(.05,.055,'Dashed = incomplete sample. Curves require evidence on all four axes. Missing axes are never zero. See matrices for all partial observations.',fontsize=11,color='#617780')
    fig.text(.05,.018,'Hints are fresh targeted attempts on exploration misses, with different denominators and additional information/budget.',fontsize=11,color='#617780')
    save(fig,name)


def matrix(records,keys,labels,phase,name,title,by_type=False):
    stats=[[r[phase]['types' if by_type else 'cells'][key] for r in records] for key in keys]
    values=np.array([[s['rate'] if s['rate'] is not None else np.nan for s in row] for row in stats])
    fig,ax=plt.subplots(figsize=(max(10,len(records)*.95+7),max(7.5,len(keys)*.29+3.8)))
    fig.subplots_adjust(left=.42,right=.96,top=.87,bottom=.24 if by_type else .15)
    cmap=plt.get_cmap('YlGnBu').copy();cmap.set_bad('#e9edf0')
    im=ax.imshow(values,vmin=0,vmax=1,aspect='auto',cmap=cmap)
    ax.set_yticks(range(len(keys)),labels,fontsize=9);ax.set_xticks(range(len(records)),[r['name'] for r in records],rotation=38,ha='right',fontsize=9)
    for y,row in enumerate(stats):
        for x,s in enumerate(row):
            ax.text(x,y,f"{s['k']}/{s['n']}" if s['n'] else '—',ha='center',va='center',fontsize=8,
                    color='white' if s['rate'] is not None and s['rate']>.6 else '#223b46')
    ax.set_xticks(np.arange(-.5,len(records),1),minor=True);ax.set_yticks(np.arange(-.5,len(keys),1),minor=True);ax.grid(which='minor',color='white',lw=.8);ax.tick_params(which='minor',bottom=False,left=False)
    fig.suptitle(title,fontsize=20,weight='bold',y=.98)
    fig.text(.04,.925,'Cells show activations / completed opportunities. Gray means no observations, not zero activation.',fontsize=11,color='#617780')
    fig.text(.04,.025,'Hinted cells contain only targeted exploration misses. Blank hinted cells can mean untested or no misses; summary gives run availability.',fontsize=10,color='#617780')
    save(fig,name)


def model_matrix(record,targets,labels):
    stats=[[record[p]['cells'][target] for p in PHASES] for target in targets]
    values=np.array([[s['rate'] if s['rate'] is not None else np.nan for s in row] for row in stats])
    fig,ax=plt.subplots(figsize=(13,16));fig.subplots_adjust(left=.59,right=.97,top=.90,bottom=.05)
    cmap=plt.get_cmap('YlGnBu').copy();cmap.set_bad('#e9edf0')
    ax.imshow(values,vmin=0,vmax=1,cmap=cmap,aspect='auto');ax.set_yticks(range(len(targets)),labels,fontsize=9)
    ax.set_xticks(range(3),[PHASE_NAMES[p] for p in PHASES],fontsize=11);ax.xaxis.tick_top()
    for y,row in enumerate(stats):
        for x,s in enumerate(row):ax.text(x,y,f"{s['k']}/{s['n']}" if s['n'] else '—',ha='center',va='center',fontsize=9,color='white' if s['rate'] is not None and s['rate']>.6 else '#223b46')
    fig.suptitle(record['name']+' · revised-game results',fontsize=22,weight='bold',y=.975)
    fig.text(.04,.94,'All 45 game/mechanism cells · activations / observed opportunities',fontsize=12)
    fig.text(.04,.018,'Gray = no observations. Hints test exploration misses only. Missing revised hints are not filled using older games.',fontsize=10,color='#617780')
    save(fig,'model_'+record['model'])


def fmt(stats):
    if not stats['supported']:return 'Not run'
    if not stats['n']:return 'No misses to retest' if stats['complete'] else 'Pending / no valid episodes'
    return f"{stats['k']}/{stats['n']} ({stats['rate']:.1%})"+('' if stats['complete'] else ' *')


def report(data):
    records=data['models'];legacy=data['historical_models']
    lines=['# Model results: win-only, exploration and hints','',f"Updated {data['updated']}.",'',
           'This is the consolidated results page. The main figures use the revised 45-hole games. All three prompt conditions appear below; unrun conditions stay visibly unavailable. An asterisk marks an incomplete denominator.',
           '', '**Latest complete matched comparisons:** GPT-5.6 Sol: win-only 26/135 versus exploration 36/135. Kimi K3: 20/135 versus 29/135. Other models include ongoing or incomplete runs; use the live table below.',
           '', '## Revised games: current results','',
           '| Model | Requested reasoning | Win only | Exploration | Hinted rescue of exploration misses | Win/exploration run status |',
           '|---|---|---:|---:|---:|---|']
    for r in records:lines.append(f"| {r['name']} | {r['reasoning']} | {fmt(r['win_only'])} | {fmt(r['exploration'])} | {fmt(r['hinted'])} | {r['status']} |")
    lines+=['','Counts are **activated hole × seed opportunities / observed opportunities**, not distinct holes or win rates. The maximum unhinted denominator is 135. Hinted denominators are the model’s own prior exploration misses and are not directly comparable to an unhinted rate.',
            '', '**Missing revised hints:** the seven open models have no hinted runs on these revised games. Their older hinted results appear in the historical section below. Gemini Flash is an additional revised-game exploration/hint reference; win-only has not been run for it.',
            '', '## Star plots','','### Frontier models','','![Frontier prompt stars](plots/revised_frontier_stars.png)',
            '', '### Open models','','![Open prompt stars](plots/revised_open_stars.png)',
            '', 'Solid curves have complete denominators; dashed curves are partial. Curves without any data on one of the four axes are omitted, while their observed cells remain in the matrices. Curves use all available observations, so partial cohorts can differ. The paired table below is the proper within-model win/exploration comparison.',
            '', '## Model-by-type matrices']
    for p in PHASES:lines += ['',f"### {PHASE_NAMES[p]}",'',f"![{PHASE_NAMES[p]} model/type matrix](plots/revised_{p}_types.png)"]
    lines+=['','## Full model-by-hole matrices','', 'Each row is one of the 45 eligible game/mechanism combinations. Cells contain k/n; gray cells have no observations.']
    for p in PHASES:lines+=['',f'### {PHASE_NAMES[p]} — all models and all 45 holes','',f'![{PHASE_NAMES[p]} full matrix](plots/revised_{p}_holes.png)']
    lines+=['','## Per-model matrices: all three prompts together']
    for r in records:lines+=['',f"### {r['name']}",'',f"![{r['name']} three-condition matrix](plots/model_{r['model']}.png)"]
    lines+=['','## Paired win-only versus exploration','', 'Only identical completed game/seed cases within each model are counted here. Ongoing completion may change the paired cohort.',
            '', '| Model | Matched opportunities | Win only | Exploration | Difference |','|---|---:|---:|---:|---:|']
    for r in records:
        p=r['paired'];n=p['n']
        if n:lines.append(f"| {r['name']} | {n} | {p['win_only']}/{n} | {p['exploration']}/{n} | {(p['exploration']-p['win_only'])/n*100:+.1f} pp |")
    lines+=['','## Historical games: open/smaller-model exploration and hints','',
            '**Different protocol; do not splice these hinted curves into the revised-game comparison.** These runs use older disclosed rules, rewards/horizons and study settings, filtered to the same 45 target IDs. All request low reasoning. They are included here so existing results are accessible in one place.',
            '', '| Model | Historical exploration | Historical hinted rescue | Status |','|---|---:|---:|---|']
    for r in legacy:lines.append(f"| {r['name']} | {fmt(r['exploration'])} | {fmt(r['hinted'])} | {r['status']} |")
    lines+=['','![Historical exploration/hint stars](plots/historical_stars.png)']
    for p in ['exploration','hinted']:lines+=['',f'![Historical {p} type matrix](plots/historical_{p}_types.png)',
        '',f'### Historical {p}: full model-by-hole matrix','',f'![Historical {p} full matrix](plots/historical_{p}_holes.png)']
    lines+=['','## Prompts, methods and source reports','',
            '- **Win only:** winning objective plus rules/action instructions; no exploration encouragement. This is not an empty system prompt.',
            '- **Exploration:** the same objective/instructions plus the active-exploration paragraph.',
            '- **Hinted rescue:** exploration plus an explicit description of one mechanism, in a fresh episode after a prior miss. No oracle action sequence is supplied. This is an execution diagnostic with extra information and attempts, not an equal-budget third randomized arm.',
            '- Revised games: 17 editions, 45 holes, three seeds; no reflection or cross-game memory; fixed native scripted opponents. Requested reasoning differs across models but matches within a model’s win/exploration pair. Missing episodes are not scored as failures to activate.',
            '- Original star grouping is preserved: meta-rule is Information/interface; board-state poisoning is Multiplayer/objective. This corrects the grouping in the first win-only star renderer; activation counts did not change.',
            '- New combined figures are generated offline, without new inference calls.',
            '', '[Machine-readable summaries](data.json) · [Per-hole/seed CSV](observations.csv)',
            '', '[Win-only run details](../winonly45-20260909/REPORT.md) · [Frontier exploration/hints](../frontier45-20260909/RESULTS.md) · [Revised Gemini Flash](../gemini-revised45-20260909/RESULTS.md) · [Historical expanded cohort](../small-engine49-20260909/plots/filtered-45-extended/REPORT.md)',
            '', '[Earlier two-game win-only/exploration pilot](../v3-small-explore-20260908/COMPARISON.md). It found zero useful win-only activation on Seven Seal and mixed Auction results; it is historical context, not a matched revised-game control.',
            '', 'PNG figures are embedded above. Matching SVG and PDF files are available beside every image in `plots/`.']
    body='\n'.join(lines)+'\n';(OUT/'REPORT.md').write_text(body)
    def rebase(match):
        target=match[2]
        return match[1]+os.path.relpath(OUT/target,CANONICAL.parent)+match[3]
    CANONICAL.write_text(re.sub(r'(!?\[[^\]]*\]\()([^\)]+)(\))',rebase,body))


def build():
    OUT.mkdir(exist_ok=True);(OUT/'plots').mkdir(exist_ok=True)
    data,rows=collect();groups=data['groups'];targets=data['targets'];records=data['models'];legacy=data['historical_models']
    categories=[c for cs in groups.values() for c in cs]
    ordered=sorted(targets,key=lambda t:(data['titles'].get(t.rsplit('.',1)[0],t),categories.index(t.rsplit('.',1)[1])))
    labels=[data['titles'].get(t.rsplit('.',1)[0],t.rsplit('.',1)[0])+' — '+LABELS[t.rsplit('.',1)[1]] for t in ordered]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    stars([r for r in records if r['group'] in ('frontier','reference')],groups,'revised_frontier_stars','Revised games · frontier models + Flash reference')
    stars([r for r in records if r['group']=='open'],groups,'revised_open_stars','Revised games · open models')
    for phase in PHASES:
        matrix(records,categories,[LABELS[c] for c in categories],phase,f'revised_{phase}_types',f'Revised games · {PHASE_NAMES[phase]} · model × type',True)
        matrix(records,ordered,labels,phase,f'revised_{phase}_holes',f'Revised games · {PHASE_NAMES[phase]} · model × hole')
    for r in records:model_matrix(r,ordered,labels)
    stars(legacy,groups,'historical_stars','Historical games · exploration and hints',phases=['exploration','hinted'])
    for phase in ['exploration','hinted']:
        matrix(legacy,categories,[LABELS[c] for c in categories],phase,f'historical_{phase}_types',f'Historical games · {PHASE_NAMES[phase]} · model × type',True)
        matrix(legacy,ordered,labels,phase,f'historical_{phase}_holes',f'Historical games · {PHASE_NAMES[phase]} · model × hole')
    (OUT/'data.json').write_text(json.dumps(data,indent=2)+'\n')
    with (OUT/'observations.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    report(data)
    print(data['updated'],len(rows),'observations;',CANONICAL,flush=True)
    return all(r['status'] in ('finished','finished_with_errors','preflight_failed','reference','process_exited') for r in records)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--watch',action='store_true');args=parser.parse_args()
    while True:
        done=build()
        if done or not args.watch:break
        time.sleep(45)
