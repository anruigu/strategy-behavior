"""Read-only scoring, provenance checks, and reporting for the frozen diagnostic."""
import argparse
from collections import Counter,defaultdict
import json
import math
import random
import statistics as st

from prediction.client import Ledger
from prediction.io_utils import read_json,write_json,digest,now
from .checks import ROOT,OUT,AXES,TARGETS,descriptor,supported,targets

NAMES={'training_mean':'Training mean','linear_structured':'Linear · structured','linear_full':'Linear · full',
       'mlp_structured':'MLP · structured','mlp_full':'MLP · full','zero_full':'Kimi zero-shot · full',
       'few_full':'Kimi four-shot · full','few_structured':'Kimi four-shot · structured','few_engine_facts':'Kimi four-shot · engine facts'}
BEHAVIOR={'prisoners_dilemma':'cooperation_rate','pig_dice':'risk_taking_rate','colonel_blotto':'allocation_concentration'}
TITLES={'prisoners_dilemma':'Prisoner’s Dilemma','pig_dice':'Pig Dice','colonel_blotto':'Colonel Blotto'}


def mean(values):
    values=[v for v in values if v is not None]
    return st.mean(values) if values else None


def bootstrap(values):
    """Percentile interval over equally weighted cluster means, fixed RNG."""
    if len(values)<2:return None
    rng=random.Random(20260910)
    draws=sorted(st.mean(rng.choices(values,k=len(values))) for _ in range(5000))
    return [draws[124],draws[4874]]


def parameters(records):
    result=[]
    for family,(axis,lo,base,hi) in AXES.items():
        target=BEHAVIOR[family];groups={}
        for v in (lo,base,hi):
            rows=[r for r in records if r['inputs']['family_id']==family and r['inputs']['structured']['parameters'][axis]==v]
            assert len(rows)==8
            groups[v]=rows
        def key(r):return (r['inputs']['player']['model_id'],r['inputs']['context']['prompt_condition'],r['environment_seed'],r['inputs']['role']['seat_id'])
        pairs=[]
        mid={key(r):r for r in groups[base]}
        for value in (lo,hi):
            deltas=[r['targets'][target]-mid[key(r)]['targets'][target] for r in groups[value] if r['targets'][target] is not None and mid[key(r)]['targets'][target] is not None]
            pairs.append(dict(value=value,against=base,paired_episodes=len(deltas),mean_change=mean(deltas),
                increased=sum(d>1e-10 for d in deltas),decreased=sum(d< -1e-10 for d in deltas),unchanged=sum(abs(d)<=1e-10 for d in deltas),range=[min(deltas),max(deltas)]))
        levels=[dict(value=v,episodes=len(rows),behavior=mean(r['targets'][target] for r in rows),
            wins=sum(r['targets']['win'] for r in rows),win_rate=mean(r['targets']['win'] for r in rows),
            any_invalid=mean(r['targets']['any_invalid'] for r in rows),mean_focal_actions=mean(r['labels']['focal_actions'] for r in rows),
            by_model=[dict(model=m,episodes=sum(r['inputs']['player']['model_id']==m for r in rows),behavior=mean(r['targets'][target] for r in rows if r['inputs']['player']['model_id']==m)) for m in ('qwen-3.8-27b','glm')]) for v,rows in groups.items()]
        result.append(dict(family=family,title=TITLES[family],axis=axis,target=target,base=base,levels=levels,paired=pairs))
    return result


def model_effects(records):
    base=[r for r in records if r['source_run']=='pilot-20260910']; cohorts=[];by_family=[]
    for model in ('qwen-3.8-27b','glm'):
        rows=[r for r in base if r['inputs']['player']['model_id']==model]
        cohorts.append(dict(model=model,episodes=len(rows),wins=sum(r['targets']['win'] for r in rows),win_rate=mean(r['targets']['win'] for r in rows),
            invalid_episodes=sum(r['targets']['any_invalid'] for r in rows),any_invalid=mean(r['targets']['any_invalid'] for r in rows),
            mean_invalid_action_rate=mean(r['labels']['behavior']['invalid_action_rate'] for r in rows)))
    paired=defaultdict(dict)
    for row in base:
        i=row['inputs'];key=(i['family_id'],i['context']['prompt_condition'],row['environment_seed'],i['role']['seat_id'])
        paired[key][i['player']['model_id']]=row
    assert len(paired)==48 and all(len(g)==2 for g in paired.values())
    for family in sorted({r['inputs']['family_id'] for r in base}):
        groups=[g for k,g in paired.items() if k[0]==family]
        by_family.append(dict(family=family,pairs=len(groups),
            win_delta=mean(g['qwen-3.8-27b']['targets']['win']-g['glm']['targets']['win'] for g in groups),
            invalid_delta=mean(g['qwen-3.8-27b']['targets']['any_invalid']-g['glm']['targets']['any_invalid'] for g in groups),
            model_rows=[dict(model=m,wins=sum(g[m]['targets']['win'] for g in groups),invalid=sum(g[m]['targets']['any_invalid'] for g in groups),
                behavior={t:mean(g[m]['targets'][t] for g in groups) for t in TARGETS[2:]}) for m in ('qwen-3.8-27b','glm')]))
    return dict(cohorts=cohorts,paired_episodes=len(paired),families=by_family,
        win_difference=dict(direction='Qwen minus GLM',estimate=mean(r['win_delta'] for r in by_family),family_bootstrap_95=bootstrap([r['win_delta'] for r in by_family])),
        invalid_difference=dict(direction='Qwen minus GLM',estimate=mean(r['invalid_delta'] for r in by_family),family_bootstrap_95=bootstrap([r['invalid_delta'] for r in by_family])))


def audit_calls(folder,linked,ceiling):
    calls={p.stem:read_json(p) for p in (folder/'raw_calls').glob('*.json')}
    assert len(linked)==len(set(linked)) and set(linked)==set(calls)
    cost=sum(c.get('budget_cost_usd') or 0 for c in calls.values())
    ledgers={name:Ledger(folder/name,ceiling).summary() for name in ('budget.sqlite','stage-budget.sqlite')}
    for ledger in ledgers.values():
        assert abs(ledger['reported_usd']-cost)<1e-9
        assert sum(s['calls'] for s in ledger['states'].values())==len(calls)
    return dict(calls=len(calls),statuses=dict(Counter(c['status'] for c in calls.values())),reported_cost_usd=cost,
        unknown_cost_calls=sum(c.get('budget_cost_usd') is None for c in calls.values()),ledgers=ledgers)


def provenance(out,manifest,records):
    lookup={r['episode_id']:r for r in records}
    for suite,ids in manifest['suites'].items():
        assert not set(ids['train']) & set(ids['test'])
        assert not {lookup[i]['groups']['opening_group'] for i in ids['train']} & {lookup[i]['groups']['opening_group'] for i in ids['test']}
        if suite=='family':assert not {lookup[i]['inputs']['family_id'] for i in ids['train']} & set(manifest['heldout_families'])
    assert manifest['source_sha256']==digest((out.parent/'checks.py').read_text())
    player_audits={}
    for name in ('pilot-20260910','parameter-check-20260910'):
        folder=ROOT/'runs'/name;plan=read_json(folder/'plan.json');linked=[];invalid=0;focal=0
        for item in plan['episodes']:
            trace=read_json(folder/'episodes'/(item['episode_id']+'.json'));row=lookup[item['episode_id']]
            assert trace['status']=='complete' and trace['item']==item
            assert row['source_plan_sha256']==digest(plan)
            assert row['targets']==targets(row,trace)
            assert row['labels']['outcome']['native_reward']==trace['final_state']['rewards'][str(item['seat'])]
            assert row['targets']['win']==float(trace['final_state']['rewards'][str(item['seat'])]==1)
            for step in trace['steps']:
                if not step['is_focal']:continue
                focal+=1;invalid+=step['result']['native_invalid']
                attempts=trace['attempts'][str(step['index'])]
                for a in attempts:
                    linked.append(a['meta']['call_id']);call=read_json(folder/'raw_calls'/(a['meta']['call_id']+'.json'))
                    assert call['request']['messages']==step['messages'] and call['status']==a['meta']['status']
                    assert call['config']==plan['models'][item['model']] and call['request']['max_tokens']==plan['max_tokens']
                assert attempts[-1]['meta']['status']=='ok' and attempts[-1]['raw']==step['raw_action']
        player_audits[name]=dict(audit_calls(folder,linked,plan['budget_usd']),episodes=len(plan['episodes']),focal_actions=focal,native_invalid_actions=invalid)
    linked=[];forecasts=[]
    for task in manifest['tasks']:
        ids=manifest['suites'][task['suite']];assert task['episode_id'] in ids['test'] and set(task['example_ids'])<=set(ids['train'])
        payload=json.loads(task['messages'][1]['content']);rep='structured' if task['method']=='few_structured' else 'engine_facts' if task['method']=='few_engine_facts' else 'full'
        assert payload['query']==descriptor(lookup[task['episode_id']],rep)
        assert task['supported']==supported(lookup[task['episode_id']])
        assert len(payload['examples'])==len(task['example_ids'])
        for example,ident in zip(payload['examples'],task['example_ids']):
            assert example==dict(input=descriptor(lookup[ident],rep),observed=lookup[ident]['targets'])
        record=read_json(out/'forecasts'/(task['id']+'.json'));assert record['task']==task
        assert len(record['attempts'])<=manifest['max_attempts']
        for attempt in record['attempts']:
            ident=attempt['meta']['call_id'];linked.append(ident);call=read_json(out/'raw_calls'/(ident+'.json'))
            assert call['request']['messages']==task['messages'] and call['status']==attempt['meta']['status']
            assert call['config']==manifest['predictor'] and call['request']['max_tokens']==manifest['max_tokens']
            if call['status']=='ok':assert call['response']['choices'][0]['message']['content']==attempt['raw']
        if record['status']=='complete':
            import re
            assert record['forecast']==json.loads(re.search(r'\{.*\}',record['attempts'][-1]['raw'],re.S)[0])
            forecasts.append({k:task[k] for k in ('suite','episode_id','method')}|dict(forecast=record['forecast']))
    return dict(status='passed',player_data=manifest['player_data_audit'],player_calls=player_audits,
        prediction_calls=audit_calls(out,linked,manifest['budget_usd']),complete_predictions=len(forecasts),planned_predictions=len(manifest['tasks']),
        missing_predictions=len(manifest['tasks'])-len(forecasts),splits_and_prompt_provenance='passed'),forecasts


def score_predictions(records,predictions):
    lookup={r['episode_id']:r for r in records};scores=[];losses={}
    groups=defaultdict(list)
    for p in predictions:groups[p['suite'],p['method']].append(p)
    for (suite,method),group in groups.items():
        for target in TARGETS:
            rows=[]
            for p in group:
                row=lookup[p['episode_id']];y=row['targets'][target];v=p['forecast'][target]
                if y is None or v is None:continue
                err=(y-v)**2
                losses[suite,method,target,p['episode_id']]=err
                clipped=max(1e-6,min(1-1e-6,v))
                rows.append(dict(family=row['inputs']['family_id'],loss=err,log_loss=-(y*math.log(clipped)+(1-y)*math.log(1-clipped)) if target in TARGETS[:2] else None))
            if not rows:continue
            family=[mean(r['loss'] for r in rows if r['family']==f) for f in sorted({r['family'] for r in rows})]
            scores.append(dict(suite=suite,method=method,name=NAMES[method],target=target,episodes=len(rows),families=len(family),
                score=mean(family),episode_weighted=mean(r['loss'] for r in rows),log_loss=mean(r['log_loss'] for r in rows)))
    comparisons=[]
    for suite in ('parameter','family'):
        for a,b in (('few_full','linear_full'),('few_full','mlp_full'),('few_full','zero_full'),('few_full','few_structured'),('few_engine_facts','few_full')):
            for target in TARGETS:
                groups=defaultdict(list)
                for ident,row in lookup.items():
                    ka,kb=(suite,a,target,ident),(suite,b,target,ident)
                    if ka in losses and kb in losses:groups[row['inputs']['family_id']].append(losses[ka]-losses[kb])
                if not groups:continue
                values=[mean(x) for x in groups.values()]
                comparisons.append(dict(suite=suite,a=a,b=b,target=target,episodes=sum(map(len,groups.values())),families=len(groups),
                    delta=mean(values),family_bootstrap_95=bootstrap(values),family_deltas={k:mean(v) for k,v in groups.items()}))
    return scores,comparisons


def markdown(summary):
    s=summary;a=s['audit'];lines=['# General games: five diagnostic checks','',
        'This diagnostic adds 48 parameter-sweep episodes to the balanced 96-episode coverage pilot. It evaluates parameter effects, model differences, native label reliability, four-shot prompting versus fixed learned baselines, and representation ablations. The full 1,360-episode catalog plan remains uncollected.','',
        '[Interactive viewer](http://localhost:42329/general#checks) · [Machine-readable results](summary.json) · [Frozen prediction protocol and exact prompts](manifest.json) · [Scored forecasts](predictions.json) · [Evaluation rows](records.evaluator.json)','',
        *[f"- **{v['question']}: {v['verdict']}.** {v['detail']}" for v in s['verdicts']],'',
        '## Behavior versus parameters','',
        'Each setting has eight episodes: two models × two prompts × two seed/seat blocks. Means weight episodes equally. In contrast, the coverage viewer’s supported-rate chart pools decision opportunities; those estimands need not agree. The three selected axes are a small targeted sweep, not a random sample of parameter effects.','',
        '| Family / parameter | Value | Episodes | Mean behavior | Win / solved | Mean focal actions |','|---|---:|---:|---:|---:|---:|']
    for family in s['parameters']:
        for r in family['levels']:lines.append(f"| {family['title']} / {family['axis']} | {r['value']} | {r['episodes']} | {r['behavior']:.3f} | {r['wins']:.0f}/8 | {r['mean_focal_actions']:.2f} |")
    lines+=['','Behaviors are PD cooperation, Pig rolling with unbanked points, and Blotto largest-field allocation share. PD cooperation drops from .542 at defection rewards 4 and 5 to .458 at 7. Pig episodes grow as the target rises (6.88, 9.00, 13.25 focal actions), while risk rates remain close (.700, .696, .734). Blotto concentration is not monotonic (.431, .490, .476). These observations support collecting response curves, but do not establish robust causal parameter effects.','',
        'Comparisons match model, prompt, seed and seat. However, seed and seat are coupled; only two seed/seat blocks are repeated across conditions, the base and new variants were collected in different batches, and LLM sampling seeds are unavailable. There is no independent repeated rollout of exactly the same complete condition.','',
        '## Model differences','',
        'Use only the original balanced 12-family pilot (48 episodes per model); the extra sweep does not overweight its three families. Strict wins include full single-player solutions, with ties counted separately from wins.','',
        '| Model | Wins / solutions | Episodes with invalid actions | Mean episode invalid-action rate |','|---|---:|---:|---:|']
    for r in s['models']['cohorts']:lines.append(f"| {r['model']} | {r['wins']:.0f}/{r['episodes']} | {r['invalid_episodes']:.0f}/{r['episodes']} | {r['mean_invalid_action_rate']:.3f} |")
    for k in ('win_difference','invalid_difference'):
        r=s['models'][k];ci=r['family_bootstrap_95'];lines+=['',f"{k.replace('_',' ').capitalize()}, Qwen minus GLM: {r['estimate']:+.3f}; paired 95% family-bootstrap interval [{ci[0]:+.3f}, {ci[1]:+.3f}] (12 families, 48 paired episodes)."]
    lines+=['','Family-specific behavior differs, but the overall intervals do not establish a consistent winner. Family resampling describes uncertainty across these sampled families, not all games; within-condition sampling noise remains unresolved.','',
        '## Label reliability','',
        f"All {a['player_data']['episodes']} complete model episodes and {a['player_data']['native_transitions']:,} native transitions replay exactly against the frozen engine and raw model calls. An additional independent calculation matched all {a['player_data']['independent_pd_rounds']} PD rounds’ score changes from joint decisions and actual payoff parameters. Rewards, native invalid actions, raw response linkage, retry accounting and both budget ledgers reconcile.",
        '', 'These checks support reproducibility of operational labels. They do not validate intention, deception, exploitation, exploration or semantic rule adherence. Native acceptance can differ from the written rules: PD defaults to cooperation without a defect token, Hanoi can parse several moves in one response, and installed Kuhn betting does not add chips to the pot. Unsupported traits remain null. Native terminal completion may include losses or forfeits, and partial puzzle reward is not a solved task.','',
        '## Few-shot versus learned prediction','',
        'Two grouped holdouts were fixed before predictor calls: (1) higher parameter values in PD, Pig and Blotto, with lower/base values in training (120 train, 24 test); (2) three entire catalog test families—Kuhn Poker, Tower of Hanoi and Liar’s Dice (96 train, 24 test). No opening group crosses a train/test boundary. Player episodes already existed at preparation time, so this is a held-out evaluation, not a forecast timestamped before gameplay. Query labels and future states never enter predictor prompts or fitted features.','',
        'Kimi K3 uses zero or four retrieved training examples. Retrieval uses public structured metadata only, with the same four examples in all representation ablations. Numerical baselines use train-fitted structured features, optionally 384 TF–IDF features, and fixed logistic/Ridge or 16-unit MLP models. All scaling/vocabulary fitting is training-only; no hyperparameters or methods were selected on test results. The primary comparison is four-shot/full versus linear/full. These are small fixed baselines, not the mature learned predictor trained on the earlier matrix-game dataset.','',
        'Lower is better. Win and any-invalid use Brier scores; other targets use MSE of the observed episode rate. Scores macro-average families within a target. No undefined behavior rate is converted to zero.','']
    for suite in ('parameter','family'):
        lines += [f'### {suite.capitalize()} holdout','', '| Method | Win Brier | Any-invalid Brier | Cooperation MSE | Pig risk MSE | Blotto concentration MSE |', '|---|---:|---:|---:|---:|---:|']
        for method in NAMES:
            rows={r['target']:r for r in s['scores'] if r['suite']==suite and r['method']==method}
            lines.append('| '+NAMES[method]+' | '+' | '.join(f"{rows[t]['score']:.4f}" if t in rows else '—' for t in TARGETS)+' |')
        c=next(r for r in s['comparisons'] if r['suite']==suite and r['a']=='few_full' and r['b']=='linear_full' and r['target']=='win');ci=c['family_bootstrap_95']
        lines += ['',f"Primary paired win-Brier difference (four-shot minus linear): {c['delta']:+.4f}, 95% family-bootstrap interval [{ci[0]:+.4f}, {ci[1]:+.4f}]. Only three test families contribute; this interval and ranking are preliminary.",'']
    lines+=['Four-shot/full beats both fitted full baselines on win Brier in both holdouts. It is competitive, but not uniformly better: linear/full has lower PD-cooperation and Pig-risk MSE, while the MLP and training mean have lower Blotto-concentration MSE. Extra engine facts produce the best win Brier among the tested methods on held-out families (.2056), but worsen parameter-holdout win Brier relative to four-shot/full (.1718 versus .1456).','',
        'All parameter-holdout episodes contain no native invalid actions, so the validity score there mainly rewards forecasts close to zero. It does not test sensitivity to invalid actions. Each family-specific behavior target has only eight test episodes from one family, so a family-level uncertainty interval is unavailable. See summary.json for every paired ablation and prediction coverage count.','',
        '## Does the representation contain enough information?','',
        'The structured condition includes game family, objective, action format, public parameters, model identity, seat and prompt label. Full adds exact initial actor-visible messages and an opponent-policy description. This joint ablation cannot separate the value of rules, own private opening information and opponent context. The engine-facts condition additionally supplies source-verified parser, payoff and numerical opponent details to the predictor only; the original players did not receive those extra facts. It never supplies hidden opponent values or future random draws.','',
        'The current concise representation is not a complete executable specification. In particular, installed Kuhn and auction accounting differs from common game conventions, and concise opponent descriptions omit some thresholds/probabilities. Exact native observations help establish what the player saw; versioned engine and opponent specifications are needed to establish what determines the outcome. Even an exact specification cannot reveal future stochastic actions or private states unavailable at forecast time. Ablation scores measure practical utility here, not a proof of informational sufficiency.','',
        '## Provenance, usage and reproduction','',f"Prediction completion: {a['complete_predictions']}/{a['planned_predictions']} requested forecasts; missing forecasts remain missing. Fixed baselines produce 240 predictions across five methods and two suites. No training convergence warnings were recorded.",'',
        '| Collection | Inference attempts | Reported cost | Unknown billing calls |','|---|---:|---:|---:|']
    for name,r in a['player_calls'].items():lines.append(f"| {name} | {r['calls']} | ${r['reported_cost_usd']:.4f} | {r['unknown_cost_calls']} |")
    r=a['prediction_calls'];lines.append(f"| Kimi predictor comparisons | {r['calls']} | ${r['reported_cost_usd']:.4f} | {r['unknown_cost_calls']} |")
    lines+=['','The original 96-episode distributions remain a balanced coverage cohort in the viewer; the separate validation panel shows all 144 study episodes and 48 held-out prediction queries. This general-games diagnostic does not establish relative prediction difficulty against Gameable Games, which uses different opponents, horizons and labels.','',
        '```bash','/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.evaluation.checks fit','/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.evaluation.readout','/shared/allie/venvs/hole/bin/python -B -m pytest prediction/general_games/evaluation/test_checks.py -q','```','',
        'The existing frozen manifest and raw calls preserve the original 192 requests. `checks collect` resumes that manifest and skips completed forecasts; do not run `prepare` over the existing output. Player collection source and native engine archives live in the dataset release. Learned models, numeric predictions, full prompts, evaluator rows, all raw responses and budget ledgers live beside this report.','']
    return '\n'.join(lines)


def build(out=OUT):
    manifest=read_json(out/'manifest.json');records=read_json(out/'records.evaluator.json')
    audit,llm=provenance(out,manifest,records);predictions=read_json(out/'numeric-predictions.json')+llm
    scores,comparisons=score_predictions(records,predictions)
    verdicts=[
        dict(question='Behavior versus parameters',verdict='Modest variation; preliminary',detail='PD cooperation is 54%, 54%, 46% across higher defection payoffs. Pig episodes lengthen. Blotto concentration is not monotonic. Only eight episodes per setting.'),
        dict(question='Model differences',verdict='Family-dependent, no clear overall winner',detail='Qwen wins/solves 28 of 48; GLM 25 of 48. Qwen is stronger in Connect Four here; GLM in Pig Dice. The paired overall interval spans zero.'),
        dict(question='Label reliability',verdict='Operational labels reproduce',detail='144 episodes and 1,404 native transitions replay; 72 PD payoff rounds independently match. This validates native outcomes/actions, not intent or unmeasured traits.'),
        dict(question='Few-shot competitiveness',verdict='Yes for wins; mixed for behavior',detail='Four-shot win Brier is .146 versus linear .174 on new parameters, and .221 versus .299 on new families. Learned models do better on some behavior rates.'),
        dict(question='Representation sufficiency',verdict='Useful, but incomplete',detail='Full inputs improve win forecasts over structured inputs in both holdouts. Engine facts help held-out-family wins, but not parameter-holdout wins. Hidden state and future randomness remain unknown.')]
    summary=dict(created=now(),audit=audit,parameters=parameters(records),models=model_effects(records),scores=scores,comparisons=comparisons,verdicts=verdicts,
        method_names=NAMES,suites={k:dict(train=len(v['train']),test=len(v['test'])) for k,v in manifest['suites'].items()},heldout_families=manifest['heldout_families'])
    write_json(out/'predictions.json',predictions);write_json(out/'summary.json',summary)
    (out/'REPORT.md').write_text(markdown(summary))
    # A separate export makes the extra parameter episodes inspectable without
    # changing the balanced first-pilot cohort or its audited release artifacts.
    from prediction.general_games.export import episode_rows,jsonl
    folder=ROOT/'runs/parameter-check-20260910';plan=read_json(folder/'plan.json')
    splits=read_json(ROOT/'data/20260910-v1/splits.json');rows=[];actions=[]
    for item in plan['episodes']:
        row,aa=episode_rows(read_json(folder/'episodes'/(item['episode_id']+'.json')),plan,splits)
        rows.append(row);actions.extend(aa)
    jsonl(folder/'export/episodes.jsonl',rows);jsonl(folder/'export/actions.jsonl',actions)
    write_json(folder/'export/summary.json',audit['player_calls']['parameter-check-20260910'])
    (folder/'export/REPORT.md').write_text('# General games parameter check\n\n48/48 complete episodes across six additional configurations in PD, Pig Dice and Colonel Blotto; 302 focal actions. Each configuration crosses two models, two prompts and two coupled seed/seat blocks.\n\n[Full analysis, audited provenance and predictor comparison](../../../evaluation/results-20260910/REPORT.md).\n')
    write_json(out/'artifact-hashes.json',{name:digest((out/name).read_text()) for name in ('manifest.json','records.evaluator.json','numeric-predictions.json','predictions.json','summary.json','REPORT.md')})
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=type(OUT),default=OUT);args=parser.parse_args()
    result=build(args.out);print(json.dumps(result['audit'],indent=2))
