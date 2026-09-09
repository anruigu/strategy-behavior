"""Rebuild all reports from saved traces, without calling a model."""
import argparse
from collections import defaultdict
import csv
import json
from pathlib import Path
from statistics import mean
from .clients import write_json
from .coverage_matrix import CATEGORIES
from .games import GAME_IDS


def ratio(n,d):
    return n/d if d else None


def pct(x):
    return '—' if x is None else f'{100*x:.1f}%'


def csv_write(path, rows):
    if not rows:
        path.write_text('')
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w') as f:
        writer = csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[r['exploit_id']].append(r)
    d = sum(any(r['discovered'] for r in rs) for rs in groups.values())
    de = sum(any(r['discovered'] for r in rs) and any(r['executed'] for r in rs) for rs in groups.values())
    executions = sum(r['execution_count'] for r in rows)
    success = sum(r['success_count'] for r in rows)
    firsts = [min(r['iteration'] for r in rs if r['discovered']) for rs in groups.values() if any(r['discovered'] for r in rs)]
    return {'available_exploits':len(groups),'discovered_exploits':d,
            'executed_discovered_exploits':de,'execution_count':executions,
            'successful_execution_count':success,'discovery_rate':ratio(d,len(groups)),
            'execution_rate':ratio(de,d),'success_rate':ratio(success,executions),
            'avg_first_discovery_iteration':mean(firsts) if firsts else None}


def build_report(out):
    out=Path(out)
    config=json.loads((out/'config.json').read_text())
    traces=[json.loads(p.read_text()) | {'trace_path':str(p.relative_to(out))}
            for p in sorted(out.glob('*/traces/*.json'))]
    target_version = 'discovery-v3-model-articulation' if (out/'evaluation_v3_config.json').exists() else None
    def scored(t):
        return t['status']=='complete' and (target_version is None or t.get('discovery_judge',{}).get('evaluator_version')==target_version)
    rows=[]
    for t in traces:
        if scored(t):
            rows.extend({**r,'trace_path':t['trace_path']} for r in t['evaluation'])
    by_model=defaultdict(list)
    chains=defaultdict(list)
    for r in rows:
        by_model[r['model_id']].append(r)
        chains[(r['model_id'],r['exploit_id'])].append(r)
    overview=[]
    for model in config['args']['models']:
        mine=[t for t in traces if t['model_id']==model]
        stats=summarize(by_model[model])
        total_actions=sum(t['episode']['decisions'].get('0',0) for t in mine)
        invalid_actions=sum(t['episode']['invalid'].get('0',0) for t in mine)
        stats.update(total_actions=total_actions, invalid_actions=invalid_actions,
                     invalid_action_rate=ratio(invalid_actions,total_actions))
        overview.append({'model_id':model,'played_games':len(mine),
                         'scored_games':sum(scored(t) for t in mine), **stats})
    learning=[]
    for (model,exploit),rs in sorted(chains.items()):
        rs.sort(key=lambda r:r['sequence'])
        first={key:next((r['iteration'] for r in rs if r[key]),None)
               for key in ('discovered','executed','successful')}
        discovery_seq=next((r['sequence'] for r in rs if r['discovered']),None)
        prior=[r for r in by_model[model] if r['category']==rs[0]['category']
               and r['game_id']!=rs[0]['game_id'] and r['sequence']<rs[0]['sequence'] and r['discovered']]
        learning.append({'model_id':model,'game_id':rs[0]['game_id'],'exploit_id':exploit,
                         'category':rs[0]['category'],'mechanism':rs[0]['mechanism'],
                         'iterations_scored':len(rs),
                         'first_discovery_iteration':first['discovered'],
                         'first_execution_iteration':first['executed'],
                         'first_success_iteration':first['successful'],
                         'repeated_successful_iterations':max(0,sum(r['successful'] for r in rs)-1),
                         'execution_after_discovery':any(r['executed'] and discovery_seq is not None and r['sequence']>discovery_seq for r in rs),
                         'prior_category_discovery_other_game':bool(prior),
                         'prior_category_games':','.join(sorted({r['game_id'] for r in prior})),
                         'evidence_quote':next((r['quote'] for r in rs if r['discovered']),''),
                         'trace_path':next((r['trace_path'] for r in rs if r['discovered']),rs[0]['trace_path'])})
    model_game=[]
    model_exploit=[]
    for model in config['args']['models']:
        for game in config['args']['games']:
            selected=[r for r in by_model[model] if r['game_id']==game]
            model_game.append({'model_id':model,'game_id':game,**summarize(selected)})
        for c in CATEGORIES:
            selected=[r for r in by_model[model] if r['category']==c]
            model_exploit.append({'model_id':model,'category':c,**summarize(selected)})
    by_iteration=[]
    for model in config['args']['models']:
        for iteration in range(1,config['args']['iterations']+1):
            subset=[r for r in by_model[model] if r['iteration']==iteration]
            by_iteration.append({'model_id':model,'iteration':iteration,**summarize(subset)})
    by_mechanism=[]
    for model in config['args']['models']:
        for mechanism in ('planted_discrepancy','natural_opportunity'):
            selected=[r for r in by_model[model] if r['mechanism']==mechanism]
            by_mechanism.append({'model_id':model,'mechanism':mechanism,**summarize(selected)})
    csv_write(out/'overview.csv',overview)
    csv_write(out/'exploit_learning.csv',learning)
    csv_write(out/'model_by_game.csv',model_game)
    csv_write(out/'model_by_exploit.csv',model_exploit)
    csv_write(out/'by_iteration.csv',by_iteration)
    csv_write(out/'by_mechanism.csv',by_mechanism)
    csv_write(out/'observations.csv',[{k:v for k,v in r.items() if k not in ('turns','model_config')} for r in rows])
    summary={'expected_games':len(config['args']['models'])*len(config['args']['games'])*config['args']['iterations'],
             'played_games':len(traces),'scored_games':sum(scored(t) for t in traces),
             'observations':len(rows),'overview':overview,'learning':learning,'evaluator_version':target_version or ', '.join(sorted({t.get('discovery_judge',{}).get('evaluator_version','original') for t in traces if scored(t)})) or 'pending'}
    write_json(out/'summary.json',summary)
    lines=['# Multiplayer exploit discovery benchmark v0', '',
           f'{summary["played_games"]}/{summary["expected_games"]} games played; {summary["scored_games"]} scored; {len(rows)} exploit/iteration observations.', '',
           f'Evaluation version: `{summary["evaluator_version"]}`. '+('Complete.' if summary['scored_games']==summary['expected_games'] else '**Provisional: sampling or uniform rescoring is still incomplete.**'), '',
           f'Condition: **{config["args"]["condition"]}**, scope: **{config["args"]["scope"]}**, {config["args"]["iterations"]} iterations per game. '
           f'One focal model versus deterministic scripted opponents. Temperature 0. Fixed {config["args"]["judge"]} discovery judge (see config for exact ID).', '',
           '| Model | Games scored | Discovery | Execution of discovered | Success per execution | Mean first discovery | Invalid actions |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for r in overview:
        first=r['avg_first_discovery_iteration']
        lines.append(f'| {r["model_id"]} | {r["scored_games"]} | {pct(r["discovery_rate"])} | {pct(r["execution_rate"])} | {pct(r["success_rate"])} | {first:.2f} | {pct(r["invalid_action_rate"])} |' if first is not None else
                     f'| {r["model_id"]} | {r["scored_games"]} | {pct(r["discovery_rate"])} | {pct(r["execution_rate"])} | {pct(r["success_rate"])} | — | {pct(r["invalid_action_rate"])} |')
    lines += ['', 'Discovery is scored from concrete articulation and observed evidence; execution and benefit come from deterministic state/action evaluation. '
              'Discovery denominator is every specified reachable exploit in a scored game, even if the model never opens the conditional opportunity. '
              'Execution rate is distinct discovered exploits also executed / discovered exploits. Success rate is successful action executions / executions. '
              'Empty denominators and missing data are shown as —, not zero.', '',
              '## Planted discrepancies versus strategic opportunities', '',
              'The combined measure includes both deliberately planted rule-checking gaps and legal strategic affordances. These should be interpreted separately.', '',
              '| Model | Planted discrepancies discovered | Strategic opportunities discovered |',
              '|---|---:|---:|']
    for model in config['args']['models']:
        mine={r['mechanism']:r for r in by_mechanism if r['model_id']==model}
        cells=[]
        for mechanism in ('planted_discrepancy','natural_opportunity'):
            r=mine[mechanism]
            cells.append(f'{r["discovered_exploits"]}/{r["available_exploits"]} ({pct(r["discovery_rate"])})' if r['available_exploits'] else '—')
        lines.append('| '+model+' | '+' | '.join(cells)+' |')
    lines += ['', '## Learning across repetitions', '',
              'These are per-iteration judgments, not cumulative discovery. Changes can reflect changed articulation or judge variability; the overview counts any discovery across all four iterations.', '',
              '| Model | Iteration 1 discovery | Iteration 2 | Iteration 3 | Iteration 4 |', '|---|---:|---:|---:|---:|']
    for model in config['args']['models']:
        mine=[r for r in by_iteration if r['model_id']==model]
        lines.append('| '+model+' | '+' | '.join(pct(r['discovery_rate']) for r in mine)+' |')
    lines += ['', '## Model × game discovery', '', '| Model | '+' | '.join(config['args']['games'])+' |',
              '|---|'+'---:|'*len(config['args']['games'])]
    for model in config['args']['models']:
        lines.append('| '+model+' | '+' | '.join(pct(next(r['discovery_rate'] for r in model_game if r['model_id']==model and r['game_id']==g)) for g in config['args']['games'])+' |')
    lines += ['', '## Model × exploit category discovery', '', '| Category | '+' | '.join(config['args']['models'])+' |',
              '|---|'+'---:|'*len(config['args']['models'])]
    for category in CATEGORIES:
        lines.append('| '+category+' | '+' | '.join(pct(next(r['discovery_rate'] for r in model_exploit if r['model_id']==m and r['category']==category)) for m in config['args']['models'])+' |')
    lines += ['', '## Primary benchmark table', '', '| Model | Game | Exploit | Discovery | Execution | Success | Reuse after discovery |', '|---|---|---|---:|---:|---:|---|']
    for r in learning:
        vals=[str(r['first_'+k+'_iteration'] or '—') for k in ('discovery','execution','success')]
        lines.append(f'| {r["model_id"]} | {r["game_id"]} | {r["category"]} | '+ ' | '.join(vals)+f' | {r["execution_after_discovery"]} |')
    lines += ['', 'Numbers in the primary table are first within-game iterations, indexed 1–4.', '',
              '## Evidence examples', '']
    examples=[]
    for model in config['args']['models']:
        available=[r for r in learning if r['model_id']==model and r['evidence_quote']]
        # Prefer mechanisms whose first discovery happened after iteration one.
        available.sort(key=lambda r:(r['first_discovery_iteration']==1,not r['execution_after_discovery']))
        examples.extend(available[:2])
    for r in examples:
        quote=r['evidence_quote'].replace('\n',' ')
        lines += [f'- **{r["model_id"]}, {r["category"]}**, iteration {r["first_discovery_iteration"]}: “{quote}” ([trace]({r["trace_path"]})).']
    if (out/'model_by_exploit.png').exists():
        lines += ['', '## Figures', '', '![Discovery by category](model_by_exploit.png)', '',
                  '![Discovery by game](model_by_game.png)', '', '![Learning across repetitions](learning_curves.png)', '',
                  'PDF exports: [categories](model_by_exploit.pdf), [games](model_by_game.pdf), [learning](learning_curves.pdf).']
    lines += ['', '## Limits and interpretation', '',
              '- These are explicitly versioned short profiles of the named games, with added mechanics; they are not the historical shipped-engine benchmark.',
              '- One chain per model and one randomized order: descriptive pilot results, without independent-seed uncertainty estimates or a causal transfer claim.',
              '- `exploit_learning.csv` flags earlier same-category discovery in another game. That is prior exposure, not proof of transfer. A fresh/control comparison is needed for attribution.',
              '- Discovery is judged by a fixed model and exact evidence quotation checks. Execution/success do not depend on that judge. Judge errors remain a limitation.',
              '- Success means the specification\'s local advantage: points, relative margin, denied resources, earlier ending, or revealed information. It need not improve final payoff. Information-only gains are not counted as score gains.',
              '- Multiple specifications can describe one action (for example a repeated grant has conversion, reset, and timing aspects). Category counts are correlated.',
              '- Strategic affordances explicitly described in the rules (sacrifice, denial, coalitions) are tagged `natural_opportunity`; inspect `by_mechanism.csv` separately from planted rule-checking discrepancies.',
              ('- Fresh episodes: no reflection or cross-episode memory; discovery uses gameplay articulation only.' if config['args']['condition']=='no_reflection' else '- Reflection explicitly prompts mechanism auditing; this differs from neutral reflection.'),
              *(['- Qwen and Haiku continuations used larger reflection response ceilings and transport timeouts after truncations; GLM had one logged top-level JSON-key repair. Completed games were retained. Inspect per-model recovery metadata and raw calls.'] if any(out.glob('*/recovery/*')) else []),
              '- Model randomness is logged but provider sampling determinism is not guaranteed. Environment seeds, full prompts/responses, before/after states and source snapshots are retained.', '',
              '## Files', '',
              '- [Overview](overview.csv), [per-exploit learning and evidence](exploit_learning.csv), [all observations](observations.csv).',
              '- [Model × game](model_by_game.csv), [model × exploit](model_by_exploit.csv), [iteration curves](by_iteration.csv), [mechanism split](by_mechanism.csv).',
              '- [Configuration and randomized orders](config.json), [exploit specifications](exploit_specs.json), [proposed and implemented coverage](coverage.json).',
              '- Each model directory contains `traces/`, `playbooks/`, `calls/`, and `judge_calls/`. API keys are never written to these artifacts.', '']
    (out/'REPORT.md').write_text('\n'.join(lines))
    return summary

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    print(json.dumps(build_report(args.output)['overview'],indent=2))
