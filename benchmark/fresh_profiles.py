"""Gameplay-only discovery scoring and cross-sectional fresh-play model profiles."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import html
import json
import os
from pathlib import Path
from statistics import mean
from .clients import MODELS, ModelClient, write_json
from .discovery import judge, model_articulation
from .diagnostic_games import evaluate
from .diagnostic_report import csv_write, GAME_LABELS
from .detailed_plots import GROUPS, CATEGORY_LABELS

METRICS=('discovered','attempted','executed','successful')
LABELS={'discovered':'Articulated discovery (judge)','attempted':'Attempted (engine)',
        'executed':'Executed (engine)','successful':'Successful local benefit (engine)'}


def read_traces(source):
    traces=[]
    paths=list(source.glob('no_reflection/*/traces/*.json')) + list(source.glob('*/traces/*.json'))
    for path in sorted(paths):
        t=json.loads(path.read_text())
        if t['condition']!='no_reflection' or t['status']!='complete':continue
        assert not t.get('reflection') and not t['playbook_before'] and not t['playbook_after']
        # Recheck engine results, including version-specific Hanabi information.
        from .evaluator import evaluate as historical_evaluate
        checker=evaluate if t['engine_version']=='hanabi-human-2.0' else historical_evaluate
        assert checker(t['game_id'],t['episode']['extras']['events'])==t['execution']
        traces.append((path,t,hashlib.sha256(path.read_bytes()).hexdigest()))
    return traces


def score_one(item,out):
    path,t,digest=item
    target=out/'discovery'/t['model_id']/path.name
    if target.exists():
        saved=json.loads(target.read_text())
        if saved['source_sha256']!=digest:raise ValueError('Source changed after scoring')
        return
    client=ModelClient(MODELS['claude-haiku-4.5'],out/'judge_calls'/t['model_id'])
    # Only visible gameplay and model replies, with terminal public resolution.
    evidence='\n\n'.join('OBSERVATION:\n'+turn['prompt']+'\nMODEL REPLY:\n'+turn['reply'] for turn in t.get('turn_checkpoint',t['turns']))
    evidence+='\n\nFINAL PUBLIC RESOLUTION:\n'+t['episode']['extras']['final_state']['feedback']
    result=judge(client,t['game_id'],evidence,t['execution'],articulation=model_articulation(t))
    write_json(target,dict(source=str(path),source_sha256=digest,
                           evidence_scope='Visible gameplay only; no reflection, hidden reasoning, or future episodes.',**result))
    print('Judged',t['model_id'],t['game_id'],t['iteration'],flush=True)


def plot(source,out,traces):
    out.mkdir(parents=True,exist_ok=True)
    os.environ['MPLCONFIGDIR']=str(out/'.matplotlib-cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages
    config=json.loads((source/'config.json').read_text())
    models=config['args']['models'];games=config['args']['games']
    rows=[];scored=0
    for path,t,digest in traces:
        side=out/'discovery'/t['model_id']/path.name
        labels={}
        if t.get('discovery_judge'):
            labels={r['exploit_id']:r for r in t['discovery_judge']['judgments']};scored+=1
        if side.exists():
            data=json.loads(side.read_text());assert data['source_sha256']==digest
            labels={r['exploit_id']:r for r in data['judgments']};scored+=int(not t.get('discovery_judge'))
        for r in t['execution']:
            eid=r['exploit_id'];category=eid.split('.',1)[1]
            group=next(k for k,v in GROUPS.items() if category in v)
            rows.append(dict(model=t['model_id'],game=t['game_id'],hole=eid,category=category,group=group,
                episode=t['iteration'],discovered=labels.get(eid,{}).get('discovered'),
                correct_hypothesis=labels.get(eid,{}).get('correct_hypothesis'),
                attempted=r['attempted'],executed=r['executed'],successful=r['successful'],
                quote=labels.get(eid,{}).get('quote',''),reason=labels.get(eid,{}).get('reason',''),source=str(path)))
    csv_write(out/'observations.csv',rows)
    aggregates=[]
    for dimension in ('game','hole','category','group'):
        for value in sorted({r[dimension] for r in rows}):
            for model in models:
                subset=[r for r in rows if r[dimension]==value and r['model']==model]
                for metric in METRICS:
                    known=[r[metric] for r in subset if r[metric] is not None]
                    aggregates.append(dict(dimension=dimension,label=value,model=model,metric=metric,
                         numerator=sum(known),known=len(known),denominator=len(subset),
                         rate=mean(known) if known and len(known)==len(subset) else None))
    csv_write(out/'rates.csv',aggregates)
    def rate(d,v,m,metric):
        return next(r['rate'] for r in aggregates if (r['dimension'],r['label'],r['model'],r['metric'])==(d,v,m,metric))
    gallery=[]
    footer=f'{len(traces)} fresh episodes; {scored} discovery-scored. {config['args']['iterations']} episodes/model/game. Descriptive rates; no learning curve.'
    with PdfPages(out/'all_plots.pdf') as pdf:
        def save(fig,name,title):
            fig.text(.5,.01,footer,ha='center',fontsize=8)
            fig.tight_layout(rect=[0,.05,1,.94])
            fig.savefig(out/(name+'.png'),dpi=170,bbox_inches='tight');fig.savefig(out/(name+'.pdf'),bbox_inches='tight');pdf.savefig(fig,bbox_inches='tight');plt.close(fig)
            gallery.append((name,title))
        for dimension in ('game','hole','category'):
            values=games if dimension=='game' else sorted({r[dimension] for r in rows})
            for metric in METRICS:
                vals=np.array([[np.nan if rate(dimension,v,m,metric) is None else 100*rate(dimension,v,m,metric) for v in values] for m in models])
                fig,ax=plt.subplots(figsize=(max(8,len(values)*1.35),4.8))
                im=ax.imshow(vals,vmin=0,vmax=100,cmap='Blues',aspect='auto')
                labels=[GAME_LABELS[v] if dimension=='game' else CATEGORY_LABELS[v] if dimension=='category' else GAME_LABELS[v.split('.')[0]]+'\n'+CATEGORY_LABELS[v.split('.')[1]] for v in values]
                ax.set_xticks(range(len(values)),labels,rotation=35,ha='right');ax.set_yticks(range(len(models)),models)
                for i in range(len(models)):
                    for j in range(len(values)):
                        value=vals[i,j];ax.text(j,i,'pending' if np.isnan(value) else f'{value:.0f}%',ha='center',va='center',color='white' if value>55 else 'black')
                fig.colorbar(im,ax=ax,label='Episode × hole rate (%)',shrink=.75)
                title=LABELS[metric]+' by '+dimension;fig.suptitle(title)
                save(fig,dimension+'_'+metric,title)
        fig,axes=plt.subplots(1,len(games),figsize=(15,4.7),squeeze=False)
        colors=['#8357aa','#8aa4bb','#168c91','#ed9a28']
        for ax,g in zip(axes[0],games):
            xs=np.arange(len(models))
            for k,metric in enumerate(METRICS):
                ys=[rate('game',g,m,metric) for m in models]
                ax.bar(xs+(k-1.5)*.19,[np.nan if y is None else y*100 for y in ys],.19,color=colors[k],label=LABELS[metric])
            ax.set_xticks(xs,models,rotation=20,ha='right');ax.set_ylim(0,105);ax.set_title(GAME_LABELS[g]);ax.set_ylabel('Episode × hole rate (%)')
        fig.legend(*axes[0,0].get_legend_handles_labels(),loc='upper center',ncol=4);save(fig,'game_stages','Discovery and engine stages by game')
        groups=[g for g in GROUPS if any(r['group']==g for r in rows)]
        fig,axes=plt.subplots(1,len(models),subplot_kw={'projection':'polar'},figsize=(14,5))
        angles=np.linspace(0,2*np.pi,len(groups),endpoint=False).tolist();angles+=angles[:1]
        for ax,m in zip(axes,models):
            for metric,color in [('discovered',colors[0]),('executed',colors[2])]:
                values=[rate('group',g,m,metric) for g in groups];values=[np.nan if v is None else 100*v for v in values];values+=values[:1]
                ax.plot(angles,values,'s--' if metric=='discovered' else 'o-',color=color,label=LABELS[metric],markersize=8 if metric=='discovered' else 4)
            ax.set_xticks(angles[:-1],[g.split('. ',1)[1].replace(' / ','/\n')+'\n('+str(len({r['hole'] for r in rows if r['group']==g}))+' holes)' for g in groups],fontsize=9);ax.set_ylim(0,100);ax.set_title(m,pad=25)
        fig.legend(*axes[0].get_legend_handles_labels(),loc='upper center',ncol=2);save(fig,'broad_groups','Discovery / execution by broad group')
        fig,axes=plt.subplots(1,len(games),figsize=(13,4.5),squeeze=False)
        for ax,g in zip(axes[0],games):
            for i,m in enumerate(models):
                scores=[t['episode']['scores']['0'] for _,t,_ in traces if t['game_id']==g and t['model_id']==m]
                ax.scatter([i]*len(scores),scores,alpha=.6);ax.plot([i-.2,i+.2],[mean(scores) if scores else np.nan]*2,color='black')
            ax.set_xticks(range(len(models)),models,rotation=20,ha='right');ax.set_title(GAME_LABELS[g]);ax.set_ylabel('Episode score')
        save(fig,'scores','Individual episode scores and means')
    notes='Rates average the fresh episodes, with equal weight per game-specific hole. Discovery requires an articulated mechanism linked to observed evidence in visible gameplay; execution alone does not establish discovery. Engine stages are independent of judge labels. Missing discovery stays pending. Category and broad-group rates cover only holes present in the sampled games; absent categories are not zero. Information gain can count as local success without improving final score. One action can trigger multiple labels. Engine versions are recorded in the source traces. No hidden reasoning or reflection is scored; unspoken recognition cannot be measured.'
    body=''.join(f'<section><h2>{html.escape(title)}</h2><a href="{name}.pdf"><img loading="lazy" width="1100" src="{name}.png"></a></section>' for name,title in gallery)
    (out/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Fresh-play model profiles</title><style>body{font:16px sans-serif;max-width:1200px;margin:40px auto;padding:20px}img{max-width:100%}section{margin:45px 0}</style><h1>Fresh-play model profiles</h1><p>'+html.escape(footer)+'</p><p>'+html.escape(notes)+'</p><p><a href="all_plots.pdf">All plots PDF</a> · <a href="rates.csv">Rates CSV</a> · <a href="observations.csv">Evidence CSV</a></p>'+body)
    write_json(out/'manifest.json',dict(source=str(source),engine_episodes=len(traces),judged_episodes=scored,plots=len(gallery),definition=notes,
        traces={str(p):digest for p,_,digest in traces}))
    (out/'REPORT.md').write_text('# Fresh-play model profiles\n\n'+footer+'\n\n'+notes+'\n\n[Interactive gallery](index.html) · [All plots PDF](all_plots.pdf) · [Rates](rates.csv) · [Discovery quotations](observations.csv)\n')


def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--output',type=Path);p.add_argument('--score',action='store_true');p.add_argument('--workers',type=int,default=6);a=p.parse_args()
    out=a.output or a.source/'model_profiles';out.mkdir(parents=True,exist_ok=True)
    os.environ['MPLCONFIGDIR']=str(out/'.matplotlib-cache')
    traces=read_traces(a.source)
    if a.score:
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            for f in as_completed([pool.submit(score_one,item,out) for item in traces]):f.result()
    plot(a.source,out,traces)
    print('Finished',out,flush=True)

if __name__=='__main__':main()
