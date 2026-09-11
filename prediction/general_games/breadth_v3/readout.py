"""Complete-case-gated native audit and paired family-level study readout."""
from collections import Counter, defaultdict
import hashlib
import json
import random
import re
import statistics as st

from prediction.io_utils import read_json, write_json, digest, now
from prediction.client import Ledger
from prediction.general_games.export import jsonl
from . import DATA, STUDY
from .catalog import NEW, FAMILIES
from .collection import source_hashes
from .runtime import replay, othello_moves
from .labels import episode_row, TARGETS, DEFINITIONS, BEHAVIOR_DEFINITIONS
from .predict import audit_calls, reproduce


def interval(values):
    if len(values)<2: return None
    rng=random.Random(20260911)
    boot=sorted(st.mean(rng.choices(values,k=len(values))) for _ in range(10000))
    return [boot[249],boot[9749]]


def independent_checks(trace):
    counts=Counter(); fid=trace['item']['game']['family_id']; params=trace['item']['game']['parameters']; decisions={}
    for step in trace['steps']:
        before=step['before']['game_state']; after=step['after']['game_state']; actor=str(step['actor']); valid=not step['result']['native_invalid']; raw=step['raw_action']
        if fid=='gops' and valid:
            spent=set(before['player_hands'][actor])-set(after['player_hands'][actor]); assert len(spent)==1
            bid=spent.pop(); expected=dict(before['player_scores'])
            if before['pending_bids']:
                other=str(1-step['actor']); other_bid=before['pending_bids'][other]; prize=before['current_prize']+before['carry_pot']
                if bid>other_bid: expected[actor]+=prize
                elif bid<other_bid: expected[other]+=prize
                assert after['player_scores']==expected; counts['gops_prize_accounting']+=1
            counts['gops_card_removals']+=1
        if fid=='stag_hunt' and before['phase']=='decision':
            decisions[actor]='stag' if re.search(r'\[Stag\]',raw,re.I) else 'hare'
            if len(decisions)==2:
                for who,choice in decisions.items():
                    other=decisions[str(1-int(who))]
                    payoff=params['mutual_stag_reward'] if choice==other=='stag' else params['mutual_hare_reward'] if choice==other=='hare' else params['single_stag_reward'] if choice=='stag' else params['single_hare_reward']
                    assert after['total_payoff'][who]-before['total_payoff'][who]==payoff
                decisions={}; counts['stag_round_payoffs']+=1
        if fid=='battleship' and valid:
            m=re.search(r'\[([a-z])(\d+)\]',raw,re.I); r,c=ord(m[1].upper())-65,int(m[2]); other=str(1-step['actor'])
            hit=before['board'][other][r][c]!='~'
            assert before['tracking_board'][actor][r][c]=='~'
            assert after['tracking_board'][actor][r][c]==('X' if hit else 'O')
            for rr in range(params['grid_size']):
                for cc in range(params['grid_size']):
                    if (rr,cc)!=(r,c): assert before['tracking_board'][actor][rr][cc]==after['tracking_board'][actor][rr][cc]
            counts['battleship_shot_results']+=1
        if fid=='othello' and valid:
            legal=othello_moves(before['board'],step['actor']); own='B' if step['actor']==0 else 'W'; n=params['board_size']
            placed=[(r,c) for r in range(n) for c in range(n) if not before['board'][r][c] and after['board'][r][c]]
            if legal:
                assert len(placed)==1; r,c=placed[0]; flips=next(f for rr,cc,f in legal if (rr,cc)==(r,c))
                delta=sum(x==own for row in after['board'] for x in row)-sum(x==own for row in before['board'] for x in row)
                assert delta==1+flips; counts['othello_disc_changes']+=1
            else: assert before['board']==after['board']; counts['othello_passes']+=1
        if fid=='sokoban':
            room=step['after']['native_extra']['room_state']
            assert sum(x in (3,4) for row in room for x in row)==params['num_boxes']
            assert sum(x==5 for row in room for x in row)==1
            counts['sokoban_box_conservation']+=1
    if fid=='blackjack':
        results=trace['final_state']['game_state']['results_summary']; reason=trace['final_state']['game_info']['0'].get('reason','')
        independent=Counter()
        for step in trace['steps']:
            a=step['before']['game_state']['results_summary']; b=step['after']['game_state']['results_summary']
            deltas={k:b[k]-a[k] for k in a}; assert all(v>=0 for v in deltas.values()) and sum(deltas.values()) in (0,1)
            independent.update(deltas)
        assert dict(independent)==results
        reward=(results['win']+.5*results['draw'])/params['num_hands'] if reason.startswith('Invalid Move:') else results['win']/params['num_hands']
        assert abs(reward-trace['final_state']['rewards']['0'])<1e-12; counts['blackjack_hand_and_reward_accounting']+=1
    if fid=='sokoban':
        room=trace['final_state']['native_extra']['room_state']; score=sum(x==3 for row in room for x in row)/params['num_boxes']
        assert trace['final_state']['rewards']['0']==score; counts['sokoban_terminal_fraction']+=1
    return counts


def load_phase(phase):
    plan=read_json(STUDY/phase/'plan.json'); assert plan['source_hashes']==source_hashes(); rows=[]; actions=[]; checks=Counter(); calls=[]
    for item in plan['episodes']:
        trace=read_json(STUDY/phase/'episodes'/(item['episode_id']+'.json')); assert trace['item']==item
        assert trace['status']=='complete',('Incomplete planned episode',item['episode_id'],trace['status'])
        replay(item,trace,STUDY/phase/'raw_calls'); row,aa=episode_row(trace,'v3-'+phase); rows.append(row); actions+=aa
        checks.update(independent_checks(trace))
        for index,attempts in trace['attempts'].items():
            for attempt in attempts:
                call=read_json(STUDY/phase/'raw_calls'/(attempt['meta']['call_id']+'.json')); calls.append(call['call_id'])
                assert call['config']==plan['models'][item['model']] and call['request']['max_tokens']==plan['max_tokens'] and call['status']==attempt['meta']['status']
                assert call['request']['messages']==trace['steps'][int(index)]['messages']
                if call['status']=='ok': assert call['response']['choices'][0]['message']['content']==attempt['raw']
    assert len(calls)==len(set(calls)) and set(calls)=={p.stem for p in (STUDY/phase/'raw_calls').glob('*.json')}
    return rows,actions,dict(checks)


def inference_audit():
    folders=[('training',STUDY/'training'),('test',STUDY/'test'),('prediction/depth',STUDY/'prediction/depth'),('prediction/breadth',STUDY/'prediction/breadth')]
    groups={}; ids=[]
    for name,folder in folders:
        calls=[read_json(p) for p in (folder/'raw_calls').glob('*.json')]; ids.extend(c['call_id'] for c in calls)
        groups[name]=dict(calls=len(calls),statuses=dict(Counter(c['status'] for c in calls)),reported_usd=sum(c.get('budget_cost_usd') or 0 for c in calls),unknown_cost_calls=sum(c.get('budget_cost_usd') is None for c in calls))
    assert len(ids)==len(set(ids)); ledgers={}
    for phase,ceiling in [('global',60),('training',40),('test',40),('prediction',40)]:
        ledger=Ledger(STUDY/'budget.sqlite' if phase=='global' else STUDY/phase/'budget.sqlite',ceiling).summary()
        selected=list(groups.values()) if phase=='global' else [v for k,v in groups.items() if k.split('/')[0]==phase]
        assert abs(ledger['reported_usd']-sum(x['reported_usd'] for x in selected))<1e-9
        assert sum(x['calls'] for x in ledger['states'].values())==sum(x['calls'] for x in selected)
        ledgers[phase]=ledger
    return dict(groups=groups,ledgers=ledgers,total_calls=len(ids),reported_usd=sum(g['reported_usd'] for g in groups.values()),unknown_cost_calls=sum(g['unknown_cost_calls'] for g in groups.values()))


def recovery_audit():
    from . import recovery
    policy=read_json(STUDY/'recovery-policy.json'); assert policy['source_sha256']==digest(__import__('pathlib').Path(recovery.__file__).read_text())
    assert read_json(STUDY/'prediction/frozen.json')['recovery_policy_sha256']==digest(policy)
    recovered=[]; calls=0
    for phase in ('training','test'):
        for p in (STUDY/'recovery'/phase).glob('*-original.json'):
            original=read_json(p); eid=original['item']['episode_id']; current=read_json(STUDY/phase/'episodes'/(eid+'.json')); index=len(original['steps'])
            assert original['steps']==current['steps'][:index] and original['item']==current['item']
            before=original['attempts'][str(index)]; after=current['attempts'][str(index)]
            assert before==after[:len(before)] and len(before)==3 and len(after)<=6
            assert all(a['meta']['status'] in recovery.ELIGIBLE for a in before)
            assert all(a.get('recovery') is True for a in after[3:])
            calls+=len(after)-3; recovered.append(dict(episode_id=eid,phase=phase,step=index,additional_calls=len(after)-3,status=current['status']))
    return dict(policy=policy,checkpoints=recovered,additional_calls=calls)


def scores(rows,predictions):
    actual=defaultdict(list)
    for r in rows: actual[r['condition_id']].append(r)
    family_scores=defaultdict(lambda:defaultdict(list))
    for p in predictions:
        rr=actual[p['query_id']]; fid=rr[0]['inputs']['family_id']
        for target in TARGETS:
            values=[r['targets'][target] for r in rr]; assert all(v is not None for v in values)
            pred=p['forecast'][target]; assert pred is not None
            error=st.mean((pred-v)**2 for v in values)
            family_scores[p['arm'],p['method'],target][fid].append(error)
    result=[]; lookup={}
    for (arm,method,target),groups in sorted(family_scores.items()):
        by_family={f:st.mean(v) for f,v in sorted(groups.items())}; assert len(by_family)==6
        lookup[arm,method,target]=by_family
        result.append(dict(arm=arm,method=method,target=target,score=st.mean(by_family.values()),by_family=by_family,conditions=sum(map(len,groups.values())),families=len(groups),episodes=len(rows)))
    return result,lookup


def comparisons(lookup):
    result=[]
    def add(label,left,right,target):
        a=lookup[*left,target]; b=lookup[*right,target]; deltas={f:a[f]-b[f] for f in a}
        result.append(dict(comparison=label,target=target,left=dict(arm=left[0],method=left[1]),right=dict(arm=right[0],method=right[1]),
            difference=st.mean(deltas.values()),ci95=interval(list(deltas.values())),by_family=deltas,families_favoring_left=sum(v<0 for v in deltas.values()),families=len(deltas)))
    for target in TARGETS:
        for method in ('linear','corrected_4','few_4','few_8','few_16','training_mean'):
            add('breadth_minus_depth',('breadth',method),('depth',method),target)
        for arm in ('depth','breadth'):
            for method in ('linear','corrected_4'):
                add('learned_minus_four_shot',(arm,method),(arm,'few_4'),target)
    return result


def distributions(rows):
    models=[]; behavior=[]; repeatability=[]
    for fid in sorted({r['inputs']['family_id'] for r in rows}):
        family=[r for r in rows if r['inputs']['family_id']==fid]
        for model in ('qwen-3.8-27b','glm'):
            rr=[r for r in family if r['inputs']['model']==model]
            models.append(dict(family=fid,model=model,episodes=len(rr),actions=sum(r['focal_actions'] for r in rr),invalid_actions=sum(r['invalid_actions'] for r in rr),targets={t:st.mean(r['targets'][t] for r in rr) for t in TARGETS}))
            for target in sorted({t for r in rr for t in r['behavior']}):
                measured=[r['behavior'][target] for r in rr if target in r['behavior'] and r['behavior'][target]['count']]
                behavior.append(dict(family=fid,model=model,target=target,episodes=len(measured),opportunities=sum(m['count'] for m in measured),mean=st.mean(m['value'] for m in measured) if measured else None))
        groups=defaultdict(list)
        for r in family: groups[r['condition_id']].append(r)
        targets={}
        for t in TARGETS:
            values=[[r['targets'][t] for r in rr] for rr in groups.values()]
            targets[t]=dict(varying_conditions=sum(len(set(v))>1 for v in values),within_condition_variance=st.mean(st.variance(v) for v in values if len(v)>1))
        repeatability.append(dict(family=fid,episodes=len(family),conditions=len(groups),targets=targets))
    return dict(models=models,behavior=behavior,repeatability=repeatability)


def diagnostics(rows,predictions):
    """Descriptive checks added after the primary readout; never change forecasts."""
    groups={r['condition_id']:r['inputs']['family_id'] for r in rows}
    mean_forecasts=[]
    for arm in ('depth','breadth'):
        for method in ('training_mean','linear','few_4','corrected_4','few_8','few_16'):
            for fid in sorted(NEW):
                pp=[p for p in predictions if p['arm']==arm and p['method']==method and groups[p['query_id']]==fid]
                actual=[r['targets']['win'] for r in rows if r['inputs']['family_id']==fid]
                mean_forecasts.append(dict(arm=arm,method=method,family=fid,forecast=st.mean(p['forecast']['win'] for p in pp),observed=st.mean(actual)))
    sokoban=[r for r in rows if r['inputs']['family_id']=='sokoban']; first_format_errors=0
    for row in sokoban:
        trace=read_json(STUDY/'test/episodes'/(row['episode_id']+'.json')); step=trace['steps'][0]
        first_format_errors+=int(step['result']['native_invalid'] and any('correct format' in e.get('kwargs',{}).get('reason','') for e in step['result']['invalid_events']))
    stag=[r for r in rows if r['inputs']['family_id']=='stag_hunt']
    return dict(status='Post-readout descriptive diagnostics; no refitting or new inference.',
        constant_half_win=dict(prediction=.5,score=st.mean((.5-r['targets']['win'])**2 for r in rows),note='Arithmetic reference added after readout; not an additional pre-registered forecast arm.'),
        mean_win_forecasts=mean_forecasts,stag_hunt=dict(episodes=len(stag),wins=sum(r['targets']['win'] for r in stag),draws=sum(r['targets']['native_score']==.5 for r in stag)),
        sokoban=dict(episodes=len(sokoban),first_action_format_errors=first_format_errors,note='Native opening shows bracketed shorthand but lists available direction words without brackets. All rejected first actions omit brackets. Clearer instructions require a separate prospective ablation.'))


def interpretation():
    return [
        'Broader training improves win-error point estimates, but the six-family intervals include zero. It does not establish that breadth fixes learned transfer. The linear learner improves only 0.0080 Brier; learned correction improves 0.0460, while pooled four-shot improves 0.0491.',
        'The best tested few-shot setting beats both learned methods on win prediction in each arm. However, the training-mean baseline beats all tested predictors on win Brier, and every win predictor is worse than the constant-0.5 arithmetic reference (0.2500). This is a calibration and transfer problem for prompting as well as learning.',
        'For overnight work, use a small representation/calibration experiment with full-family validation inside the training pool. Preserve pooled 4/8/16-shot and constant/prior controls. There are only 68 distinct visible training inputs in the breadth arm. These results do not justify a large run of the current learner, nor prove that neural training cannot help.',
    ]


def render_report(summary):
    lookup={(s['arm'],s['method'],s['target']):s['score'] for s in summary['scores']}; lines=[
        '# Fixed-budget family breadth versus repetitions', '',
        'Completed prospective check: **288 training episodes per arm**, **480 unique training episodes**, and **144 fresh test episodes across six unseen families**. Both arms use the same models, fixed learners and pooled 4/8/16-shot controls. All forecasts were frozen before test play.', '',
        *[line for paragraph in summary.get('interpretation',[]) for line in (paragraph,'')],
        '| Training arm | Families | Episodes/family | Repetitions/condition |', '|---|---:|---:|---:|',
        '| Depth | 4 | 72 | 6 |', '| Breadth | 12 | 24 | 2 |', '',
        'The two arms share 96 anchor episodes. Each family has 12 exact conditions: model × seat × three seeds for two-player games; model × six seeds for single-player games. Training uses one native base configuration per family. Test conditions have two independent actor repetitions.', '',
        'Held out entirely from training and demonstrations: **GOPS, Stag Hunt, Blackjack, Battleship, Othello and Sokoban**. Unseen means absent from this behavioral training dataset, not necessarily absent from foundation-model pretraining.', '',
        '## Win prediction', '', 'Lower Brier is better. Families receive equal weight after averaging episodes within exact conditions.', '',
        '| Predictor | Depth: 4 families | Breadth: 12 families | Breadth − depth |','|---|---:|---:|---:|']
    for method in ('training_mean','linear','few_4','corrected_4','few_8','few_16'):
        a,b=lookup['depth',method,'win'],lookup['breadth',method,'win']; lines.append(f'| {method} | {a:.4f} | {b:.4f} | {b-a:+.4f} |')
    lines += ['', 'A constant prediction of 0.5 has Brier **0.2500** for binary labels. This arithmetic reference was added after readout; it is not a newly fitted or pre-registered forecast method.', '']
    lines += ['', '## Paired comparisons', '', 'Negative differences favor the left method/arm. Intervals resample six test families and condition on the fitted forecasts; they do not capture uncertainty across alternative training-family selections.', '',
        '| Comparison | Difference | Family-bootstrap 95% interval | Families favoring left |', '|---|---:|---|---:|']
    for c in summary['comparisons']:
        if c['target']!='win' or (c['comparison']=='breadth_minus_depth' and c['left']['method'] not in ('linear','corrected_4','few_4')): continue
        label=f"{c['left']['arm']} {c['left']['method']} − {c['right']['arm']} {c['right']['method']}"
        lines.append(f"| {label} | {c['difference']:+.4f} | [{c['ci95'][0]:+.4f}, {c['ci95'][1]:+.4f}] | {c['families_favoring_left']}/6 |")
    lines += ['', '## Other shared prediction targets', '',
        'Any-invalid uses Brier error; normalized native terminal score uses MSE. Lower is better. These targets are scored separately from strict wins.', '',
        '| Predictor | Depth invalid | Breadth invalid | Depth native score | Breadth native score |',
        '|---|---:|---:|---:|---:|']
    for method in ('training_mean','linear','few_4','corrected_4','few_8','few_16'):
        values=[lookup[arm,method,target] for target in ('any_invalid','native_score') for arm in ('depth','breadth')]
        lines.append('| '+method+' | '+' | '.join(f'{v:.4f}' for v in values)+' |')
    by_family={(s['arm'],s['method'],s['target']):s['by_family'] for s in summary['scores']}
    lines += ['', '## Per-family win prediction', '',
        '| Test family | Depth linear | Breadth linear | Depth 4-shot | Breadth 4-shot | Depth correction | Breadth correction |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for fid in sorted(NEW):
        values=[by_family[arm,method,'win'][fid] for method in ('linear','few_4','corrected_4') for arm in ('depth','breadth')]
        lines.append('| '+FAMILIES[fid]['title']+' | '+' | '.join(f'{v:.4f}' for v in values)+' |')
    d=summary.get('posthoc_diagnostics',{})
    if d:
        lines += ['', '## Post-readout diagnosis', '',
            'These descriptive checks were added after inspecting the completed results. They did not change collection, labels, fits or forecasts.', '',
            f"Stag Hunt produced **{int(d['stag_hunt']['wins'])} strict wins and {d['stag_hunt']['draws']} draws in {d['stag_hunt']['episodes']} episodes**. Mean breadth-arm strict-win forecasts were .723 (linear), .599 (four-shot) and .530 (sixteen-shot), versus .083 observed. Native score correctly gives draws half credit; strict-win labels do not. Broad four-shot improves strongly on this family, but still overestimates wins. This is an observed forecast failure, not proof of its internal cause.", '',
            'GOPS goes in the opposite direction: 23/24 episodes are wins, while mean breadth forecasts are .430 (linear) and .536 (four-shot). The linear learner improves on five other families, but its GOPS Brier worsens by .1872, offsetting much of those gains.', '',
            f"All **{d['sokoban']['first_action_format_errors']}/{d['sokoban']['episodes']} Sokoban first actions** are rejected for missing brackets. The native opening shows bracketed shorthand but lists available directions as bare words; the parser requires brackets. Every episode therefore has `any_invalid=1`. This signal mixes interface compliance with later planning errors. A separate controlled instruction ablation is warranted before treating invalidity gains as strategic transfer; existing native observations stay unchanged.", '',
            'Breadth changes the global training win prior from .6042 to .5556, closer to the test rate .3889. The training-mean baseline improves by .0186, more than the linear learner’s .0080. Thus some overall improvement is explainable without richer game-specific prediction.', '',
            'For the next study, test a clearer action-format reminder and distinguish strict wins, draws/native score and decision-level behavior. Tune representations and calibration only on training-family validation; reserve untouched families or fresh evaluation for prospective claims after this readout.']
    lines += ['', '## Measurements and interpretation', '',
        'Binary wins are strict two-player wins or full single-player solutions; Blackjack counts a completed five-hand match with more wins than losses. Native score is a separate continuous target, including Blackjack hand-win fraction and Sokoban goal completion. Family-specific action rates are diagnostic observations, not newly learned targets with no training support.', '',
        'Some aggregates are mechanically uninformative: a player that spends all thirteen GOPS cards must have mean bid-card fraction 7/13, regardless of strategy. Early high-card use retains information about ordering; the aggregate bid fraction should not be read as a strategic preference.', '',
        'This is a controlled label-budget comparison for two fixed, purposively chosen training sets. It changes both family composition and repetition count. Episode count does not equalize tokens, actions, cost, or the number of distinct actor-visible inputs. It does not establish a general causal effect of adding an arbitrary family.', '',
        'Each query has complete actor opening messages, public parameters, normalized mechanics, and the scripted-opponent policy. Hidden opponent realizations and future events remain evaluator-only. The installed native engine is unchanged. A compact specification is not proof that the learner can use all represented information.', '',
        'Sokoban’s native stored board string is stale after reset; the adapter uses the actual latest delivered board observation. Native room arrays are retained separately for exact replay and label audit. Battleship actor histories have an 80KB ceiling; predictor requests retain 40KB. Both arms use the same actor limits.', '',
        'Only one configuration per family was collected here; this check tests family transfer, not parameter-response curves. Two test repetitions and six families still limit precision. No test-outcome tuning or neural encoder fine-tuning was performed.', '',
        '## Reliability and model differences', '',
        '| Test family | Qwen win | GLM win | Conditions with variable wins |', '|---|---:|---:|---:|']
    models={(r['family'],r['model']):r for r in summary['test_distributions']['models']}
    for r in summary['test_distributions']['repeatability']:
        fid=r['family']; lines.append(f"| {FAMILIES[fid]['title']} | {models[fid,'qwen-3.8-27b']['targets']['win']:.3f} | {models[fid,'glm']['targets']['win']:.3f} | {r['targets']['win']['varying_conditions']}/{r['conditions']} |")
    audit=summary['audit']; lines += ['',
        f"All **{summary['counts']['native_transitions']:,} native transitions** replayed. Independent checks: `{json.dumps(audit['independent_checks'],sort_keys=True)}`.", '',
        f"All **{audit['inference']['total_calls']:,} inference attempts** link to raw requests/responses and reconciled ledgers. Reported total cost: **${audit['inference']['reported_usd']:.4f}**; unknown-cost calls: {audit['inference']['unknown_cost_calls']}. Serialized learners reproduce {audit['reproduced_values']} forecast values within 1e-12.", '',
        f"Forecast freeze: `{audit['frozen_at']}`. First test actor call: `{audit['first_test_call']}`.", '',
        f"A uniform actor-recovery amendment was specified at `{audit['recovery']['policy']['specified_at']}`, after one training checkpoint produced three blank answers and before any predictor request. It permits at most six total identical-context attempts for empty/truncated/transport responses, excludes explicit refusals, and preserves the original checkpoints and all calls. Additional recovery calls: **{audit['recovery']['additional_calls']}**. No failed trial was replaced or labeled as a native loss.", '',
        'Full per-family scores, native-score/invalidity forecasts, behavioral opportunity counts, repeated-label variation, input coverage and costs are in `summary.json`. The release includes train-only arm exports and archived sources.']
    return '\n'.join(lines)+'\n'


def main():
    frozen=read_json(STUDY/'prediction/frozen.json')
    for name,sha in frozen['artifact_hashes'].items(): assert hashlib.sha256((STUDY/'prediction'/name).read_bytes()).hexdigest()==sha
    train,train_actions,a=load_phase('training'); test,test_actions,b=load_phase('test'); calls=inference_audit()
    first=min(read_json(p)['timestamp'] for p in (STUDY/'test/raw_calls').glob('*.json')); assert frozen['frozen_at']<first
    predictions=[]; reproduced=0
    for arm in ('depth','breadth'):
        audit_calls(arm); reproduced+=reproduce(arm); predictions+=read_json(STUDY/'prediction'/arm/'test-predictions.json')
    scored,lookup=scores(test,predictions); coverage=[]
    for arm in ('depth','breadth'):
        rr=[r for r in train if arm in r['arms']]; m=read_json(STUDY/'prediction'/arm/'manifest.json')
        coverage.append(dict(arm=arm,episodes=len(rr),families=len({r['inputs']['family_id'] for r in rr}),exact_conditions=m['exact_conditions'],visible_inputs=m['visible_training_inputs'],actions=sum(r['focal_actions'] for r in rr)))
    result=dict(created=now(),protocol=read_json(STUDY/'protocol.json'),counts=dict(training_episodes=len(train),test_episodes=len(test),total_episodes=len(train)+len(test),
        focal_actions=len(train_actions)+len(test_actions),native_transitions=sum(r['native_transitions'] for r in train+test),invalid_actions=sum(r['invalid_actions'] for r in train+test)),
        training_coverage=coverage,scores=scored,comparisons=comparisons(lookup),test_distributions=distributions(test),training_distributions=distributions(train),
        target_definitions=DEFINITIONS,behavior_definitions=BEHAVIOR_DEFINITIONS,interpretation=interpretation(),posthoc_diagnostics=diagnostics(test,predictions),
        audit=dict(frozen_at=frozen['frozen_at'],first_test_call=first,reproduced_values=reproduced,independent_checks=dict(Counter(a)+Counter(b)),inference=calls,recovery=recovery_audit()))
    write_json(STUDY/'summary.json',result); write_json(STUDY/'predictions.json',predictions)
    jsonl(STUDY/'all-episodes.jsonl',train+test); jsonl(STUDY/'all-actions.jsonl',train_actions+test_actions)
    (STUDY/'REPORT.md').write_text(render_report(result)); print(json.dumps(dict(counts=result['counts'],cost=calls['reported_usd']),indent=2),flush=True)
    return result


if __name__=='__main__': main()
