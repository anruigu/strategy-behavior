"""Engine-only reports for the three-condition diagnostic; safe while sampling."""
import argparse
import csv
import json
import os
from pathlib import Path
from statistics import mean
from .clients import write_json
from .diagnostic_prompts import CONDITIONS
from .specs import SPECS
from .detailed_plots import cumulative, fixed_rate, GAME_LABELS

GAME_LABELS = {'no_reflection': 'No reflection / fresh episodes', **GAME_LABELS, 'ref_hanabi': 'Hanabi challenge 2.0'}

LABELS = {'no_reflection': 'No reflection / fresh episodes', 'ordinary': 'Ordinary reflection', 'planned_test': 'Reflection-selected test', 'informed': 'Informed execution'}
METRICS = ('attempted', 'executed', 'successful')


def csv_write(path, rows):
    if not rows: return
    with path.open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def build_report(out, plots=False):
    out=Path(out)
    manifest=json.loads((out/'config.json').read_text())
    cfg={**manifest['args'], 'conditions': manifest.get('conditions', list(CONDITIONS))}
    traces=[json.loads(p.read_text())|{'path':str(p.relative_to(out))} for p in sorted(out.glob('*/*/traces/*.json'))]
    completed=[t for t in traces if 'execution' in t]
    lookup={(t['model_id'],t['game_id'],t['condition'],t['iteration']):t for t in completed}
    observations=[];curves=[];summary=[]
    for model in cfg['models']:
        for game in cfg['games']:
            specs=[s for s in SPECS if s.game_id==game]
            for condition in cfg.get('conditions', CONDITIONS):
                vals={}
                for spec in specs:
                    for metric in METRICS:
                        seq=[]
                        for i in range(1,cfg['iterations']+1):
                            t=lookup.get((model,game,condition,i))
                            row=next((r for r in t['execution'] if r['exploit_id']==spec.exploit_id),{}) if t else {}
                            seq.append(row.get(metric))
                        vals[spec.exploit_id,metric,'current']=seq
                        vals[spec.exploit_id,metric,'cumulative']=cumulative(seq)
                for i in range(1,cfg['iterations']+1):
                    t=lookup.get((model,game,condition,i))
                    if t:
                        for r in t['execution']:
                            observations.append(dict(model_id=model,game_id=game,condition=condition,iteration=i,
                                exploit_id=r['exploit_id'],attempted=r['attempted'],executed=r['executed'],successful=r['successful'],
                                opportunity_encountered=r['opportunity_encountered'],execution_count=r['execution_count'],success_count=r['success_count'],
                                score=t['episode']['scores'].get('0',t['episode']['scores'].get(0)),trace=t['path']))
                    for mode in ('current','cumulative'):
                        for metric in METRICS:
                            v=[vals[s.exploit_id,metric,mode][i-1] for s in specs]
                            curves.append(dict(model_id=model,game_id=game,condition=condition,iteration=i,mode=mode,metric=metric,
                                               known=sum(x is not None for x in v),denominator=len(v),numerator=sum(x is True for x in v),rate=fixed_rate(v)))
                mine=[t for t in completed if (t['model_id'],t['game_id'],t['condition'])==(model,game,condition)]
                final=lookup.get((model,game,condition,cfg['iterations']))
                summary.append(dict(model_id=model,game_id=game,condition=condition,engine_games=len(mine),expected=cfg['iterations'],
                    cumulative_attempted=fixed_rate([vals[s.exploit_id,'attempted','cumulative'][-1] for s in specs]),
                    cumulative_executed=fixed_rate([vals[s.exploit_id,'executed','cumulative'][-1] for s in specs]),
                    cumulative_successful=fixed_rate([vals[s.exploit_id,'successful','cumulative'][-1] for s in specs]),
                    final_score=final['episode']['scores'].get('0',final['episode']['scores'].get(0)) if final else None))
    csv_write(out/'observations.csv',observations);csv_write(out/'curves.csv',curves);csv_write(out/'summary.csv',summary)
    cost=0.;tokens=0;responses=0
    for p in out.glob('*/*/calls/*.json'):
        call=json.loads(p.read_text())
        for a in call.get('attempts',[]):
            usage=a.get('response',{}).get('usage',{}) or {}
            cost+=usage.get('cost',0) or 0
            tokens+=usage.get('total_tokens',0) or 0
            responses+=int('response' in a)
    data={'engine_games':len(completed),'reflected_games':sum(bool(t.get('reflection')) and t['status']=='complete' for t in traces),
          'expected_games':len(cfg['models'])*len(cfg['games'])*len(cfg['conditions'])*cfg['iterations'],
          'reported_api_cost_usd':cost,'reported_tokens':tokens,'responses':responses,'summary':summary}
    write_json(out/'summary.json',data)
    def pct(v):return 'pending' if v is None else f'{100*v:.0f}%'
    lines=['# Exploration diagnostic','',f"Engine games: {data['engine_games']}/{data['expected_games']}; reflections: {data['reflected_games']}/{data['expected_games']}.",'',
           'Conditions: ' + ', '.join(LABELS[c] for c in cfg['conditions']) + '.',
           'No-reflection episodes start fresh, retain within-episode conversation, and make no reflection API calls. This removes both reflection and cross-episode playbook memory.',
           'Matched environment seeds, four repetitions, memory reset across games and conditions. One chain per model × game × condition; no independent-replicate uncertainty estimates.',
           'Hanabi uses challenge 2.0: six turns, legal ceiling 5, completion score 12. Reviewing consumes a turn and prevents completion. This changed game is not directly comparable to the old sweep.',
           'All rates use engine checks and fixed game-specific-hole denominators. Cumulative means ever by repetition four. Missing observations remain pending. No language judge is used. Informed results do not measure spontaneous discovery.', '',
           f"API-reported usage: ${cost:.3f}, {tokens:,} tokens across {responses} recorded responses (includes retries where usage was returned).", '',
           '| Model | Game | Condition | Games | Ever attempted | Ever executed | Ever successful | Final score |',
           '|---|---|---|---:|---:|---:|---:|---:|']
    for r in summary:
        lines.append(f"| {r['model_id']} | {GAME_LABELS[r['game_id']]} | {LABELS[r['condition']]} | {r['engine_games']}/{r['expected']} | {pct(r['cumulative_attempted'])} | {pct(r['cumulative_executed'])} | {pct(r['cumulative_successful'])} | {r['final_score'] if r['final_score'] is not None else 'pending'} |")
    lines+=['','[Machine-readable summary](summary.json) · [Engine observations](observations.csv) · [Curves](curves.csv) · [Run status](status.json)','',
            'Raw playbooks, next_test plans, actual system prompts, engine events, per-turn checkpoints and full API call metadata are saved under CONDITION/MODEL/.',
            'Planned-test first episodes have no prior test; the intervention can affect gameplay starting in repetition two. Informed mechanisms are supplied before every episode. Different frontier APIs have different supported sampling controls; requested settings are logged in config.json.']
    if plots:
        draw(out,cfg,curves,lookup)
        lines+=['','## Plots','',*[f'![{m}](curves_{m}.png)' for m in METRICS],'','![Score](curves_score.png)']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n')
    return data


def draw(out,cfg,curves,lookup):
    os.environ['MPLCONFIGDIR']=str(out/'.matplotlib-cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    mode=cfg.get('plot_mode', 'cumulative')
    colors={'no_reflection':'#b64c86','ordinary':'#64748b','planned_test':'#0c8c91','informed':'#d88925'}
    nr,nc=len(cfg['models']),len(cfg['games'])
    for metric in (*METRICS,'score'):
        fig,axes=plt.subplots(nr,nc,figsize=(4.4*nc,3.1*nr+1.4),squeeze=False)
        for ri,model in enumerate(cfg['models']):
            for ci,game in enumerate(cfg['games']):
                ax=axes[ri,ci]
                for condition in cfg.get('conditions', CONDITIONS):
                    xs=list(range(1,cfg['iterations']+1));ys=[]
                    for i in xs:
                        if metric=='score':
                            t=lookup.get((model,game,condition,i));v=t['episode']['scores'].get('0',t['episode']['scores'].get(0)) if t else None
                        else:
                            r=next(r for r in curves if (r['model_id'],r['game_id'],r['condition'],r['iteration'],r['mode'],r['metric'])==(model,game,condition,i,mode,metric))
                            v=100*r['rate'] if r['rate'] is not None else None
                        ys.append(np.nan if v is None else v)
                    ax.plot(xs,ys,'-o',color=colors[condition],label=LABELS[condition],linewidth=2)
                ax.set_title(model+'\n'+GAME_LABELS[game],fontsize=10)
                ax.set_xticks(xs);ax.set_xlabel('Repetition');ax.grid(axis='y',alpha=.2)
                if metric!='score':ax.set_ylim(-3,103);ax.set_ylabel('Holes covered (%)')
                else:ax.set_ylabel('Episode score')
                ax.spines[['top','right']].set_visible(False)
        title='Episode scores' if metric=='score' else f'{mode.title()} {metric} coverage (engine)'
        fig.suptitle(title,fontsize=17,y=.98)
        fig.legend(*axes.flat[0].get_legend_handles_labels(),loc='lower center',ncol=3,bbox_to_anchor=(.5,.04),frameon=False)
        fig.text(.5,.013,'One chain per cell; matched environment seeds; no judge. Informed execution is not spontaneous discovery.',ha='center',fontsize=9)
        fig.tight_layout(rect=[0,.13,1,.94])
        for ext in ('png','pdf'):fig.savefig(out/f'curves_{metric}.{ext}',dpi=170,bbox_inches='tight')
        plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--plots',action='store_true');a=p.parse_args();build_report(a.output,a.plots)
