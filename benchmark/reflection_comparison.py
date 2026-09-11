"""Matched ordinary-reflection versus fresh-episode comparison; no judge required."""
import argparse
import json
import time
from pathlib import Path
from statistics import mean
from .clients import write_json
from .diagnostic_report import csv_write, draw
from .detailed_plots import cumulative, fixed_rate


def compare(reflection, fresh, output, plots=True):
    reflection, fresh, output = map(Path, (reflection, fresh, output))
    output.mkdir(parents=True, exist_ok=True)
    a, b = [json.loads((p/'config.json').read_text()) for p in (reflection, fresh)]
    for key in ('models', 'games', 'iterations', 'seed', 'play_max_tokens'):
        if a['args'][key] != b['args'][key]: raise ValueError(f'Unmatched {key}')
    for key in ('model_configs', 'hanabi_profile'):
        if a[key] != b[key]: raise ValueError(f'Unmatched {key}')
    # Prompt, engine, evaluator and transport equivalence; runner differs only
    # to omit reflection and reset the incoming playbook for the added condition.
    for name, digest in a['source_fingerprints'].items():
        if name.endswith(('games.py', 'engines_hanabi_human.py', 'engines_benchmark_20260906.py',
                          'engines_generated.py', 'engines_textarena.py', 'evaluator.py',
                          'clients.py', 'referee_spartan.py', 'specs.py', 'diagnostic_games.py')):
            if b['source_fingerprints'].get(name) != digest: raise ValueError(f'Unmatched source: {name}')
    cfg = dict(a['args'], conditions=['ordinary', 'no_reflection'])
    lookup = {}
    for folder, condition in ((reflection, 'ordinary'), (fresh, 'no_reflection')):
        for path in folder.glob(f'{condition}/*/traces/*.json'):
            t = json.loads(path.read_text())
            if 'execution' in t:
                lookup[t['model_id'], t['game_id'], condition, t['iteration']] = t
    costs=[]
    for folder, condition in ((reflection, 'ordinary'), (fresh, 'no_reflection')):
        for purpose in ('play', 'reflection'):
            cost=tokens=seconds=responses=0
            for path in folder.glob(f'{condition}/*/calls/*.json'):
                call=json.loads(path.read_text())
                if call['purpose']!=purpose: continue
                for attempt in call.get('attempts',[]):
                    usage=attempt.get('response',{}).get('usage',{}) or {}
                    cost+=usage.get('cost',0) or 0
                    tokens+=usage.get('total_tokens',0) or 0
                    seconds+=attempt.get('seconds',0)
                    responses+=int('response' in attempt)
            costs.append(dict(condition=condition,purpose=purpose,reported_usd=cost,tokens=tokens,
                              summed_request_seconds=seconds,responses=responses))
    csv_write(output/'costs.csv',costs)
    curves, pairs = [], []
    for m in cfg['models']:
        for g in cfg['games']:
            for condition in cfg['conditions']:
                ts = [lookup.get((m,g,condition,i)) for i in range(1,cfg['iterations']+1)]
                ids = next(([r['exploit_id'] for r in t['execution']] for t in ts if t), [])
                for metric in ('attempted','executed','successful'):
                    series = [[next(r[metric] for r in t['execution'] if r['exploit_id']==eid) if t else None for t in ts] for eid in ids]
                    for mode in ('current','cumulative'):
                        seqs = series if mode=='current' else [cumulative(seq) for seq in series]
                        for i in range(1,cfg['iterations']+1):
                            curves.append(dict(model_id=m,game_id=g,condition=condition,iteration=i,mode=mode,metric=metric,
                                               rate=fixed_rate([s[i-1] for s in seqs]) if seqs else None))
            for i in range(1,cfg['iterations']+1):
                ta,tb=[lookup.get((m,g,c,i)) for c in cfg['conditions']]
                if not ta or not tb: continue
                row=dict(model_id=m,game_id=g,iteration=i,seed=ta['seed'])
                assert ta['seed']==tb['seed'] and ta['engine_version']==tb['engine_version']
                for metric in ('attempted','executed','successful','score'):
                    def value(t):
                        return t['episode']['scores']['0'] if metric=='score' else mean(r[metric] for r in t['execution'])
                    row[metric+'_reflection']=value(ta)
                    row[metric+'_fresh']=value(tb)
                    row[metric+'_delta']=value(ta)-value(tb)
                pairs.append(row)
    csv_write(output/'curves.csv',curves)
    csv_write(output/'paired_episodes.csv',pairs)
    summaries=[]
    for m in cfg['models']:
        for g in cfg['games']:
            rows=[r for r in pairs if r['model_id']==m and r['game_id']==g and r['iteration']>=2]
            summaries.append(dict(model_id=m,game_id=g,matched_pairs=len(rows),expected=cfg['iterations']-1,
                 **{metric+'_mean_delta': mean(r[metric+'_delta'] for r in rows) if rows else None
                    for metric in ('attempted','executed','successful','score')}))
    write_json(output/'summary.json', {'sources':[str(reflection),str(fresh)],'engine_episodes':len(lookup),
               'expected_episodes':2*len(cfg['models'])*len(cfg['games'])*cfg['iterations'],'episodes_2_onward':summaries})
    lines=['# Is reflection useful?', '', f'{len(lookup)} engine episodes available across ordinary reflection and no reflection.', '',
           'Matched models, requested sampling settings, game engines and environment seeds. The added fresh-episode control runs alongside the already-started diagnostic; scheduling is not fully interleaved.',
           'No reflection means no post-game model call and no cross-episode memory. Within-game conversation is retained. This tests the reflection-plus-playbook package, not reflection separately from access to past experience.',
           'Primary contrast: per-episode attempted/executed/successful rates and score in episodes 2–4. Episode 1 is a baseline check. Positive deltas favour reflection. Cumulative fresh-episode coverage can grow by repeated attempts without learning.',
           'One reflection chain per model/game: descriptive pilot, no equivalence claim from a flat or inconclusive result. Articulated discovery is not scored by this engine-only report.', '',
           '| Model | Game | Matched episodes 2–4 | Execution delta | Success delta | Score delta |',
           '|---|---|---:|---:|---:|---:|']
    fmt=lambda x: 'pending' if x is None else f'{x:+.3f}'
    for row in summaries:
        lines.append(f"| {row['model_id']} | {row['game_id']} | {row['matched_pairs']}/{row['expected']} | {fmt(row['executed_mean_delta'])} | {fmt(row['successful_mean_delta'])} | {fmt(row['score_mean_delta'])} |")
    lines += ['', '[Paired episode data](paired_episodes.csv) · [Current and cumulative curves](curves.csv) · [Cost and request time](costs.csv)', 'Usage totals are provisional while runs are incomplete; summed request times are not elapsed wall time.', '']
    if plots:
        for mode in ('current','cumulative'):
            dest=output/mode;dest.mkdir(exist_ok=True)
            draw(dest,dict(cfg,plot_mode=mode),curves,lookup)
            lines += [f'## {mode.title()}', '', *[f'![{metric}]({mode}/curves_{metric}.png)' for metric in ('executed','successful','score')], '']
    (output/'REPORT.md').write_text('\n'.join(lines)+'\n')
    return len(lookup)


def main():
    p=argparse.ArgumentParser();p.add_argument('reflection',type=Path);p.add_argument('fresh',type=Path);p.add_argument('output',type=Path);p.add_argument('--watch',action='store_true');a=p.parse_args()
    while True:
        compare(a.reflection,a.fresh,a.output)
        if not a.watch: break
        states=[json.loads((d/'status.json').read_text())['state'] for d in (a.reflection,a.fresh)]
        if all(s!='running' for s in states):break
        time.sleep(60)

if __name__=='__main__':main()
