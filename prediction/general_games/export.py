"""Audited prediction rows: pre-episode inputs separate from future labels."""
import argparse
from collections import Counter,defaultdict
import json
from pathlib import Path
import re

from prediction.io_utils import read_json,write_json,digest,now
from .catalog import FAMILIES
from .dataset import DEFAULT_RUN,source_hashes
from .native import messages,environment_record
from .runner import replay


def rate(values):
    values=[v for v in values if v is not None]
    return dict(numerator=sum(values) if values else None,denominator=len(values),value=sum(values)/len(values) if values else None)


def action_labels(step,fid):
    raw=step['raw_action']; before=step['visible_state']; valid=not step['result']['native_invalid']
    # Labels describe native execution, or explicitly named submitted syntax.
    labels=dict(native_valid=valid,cooperation=None,defection=None,risk_taking=None,
        conversation_turn=(before.get('phase')=='conversation') if fid in ('blind_auction','prisoners_dilemma') else None,
        submitted_offer=None,submitted_accept=None,submitted_bid_total=None,
        submitted_tokens=re.findall(r'\[([^\]]+)\]',raw),exploitation=None)
    if fid=='prisoners_dilemma' and before['phase']=='decision':
        defect=bool(re.search(r'\[Defect\]',raw,re.I))
        labels.update(cooperation=not defect,defection=defect,
            conforms_to_decision_token=bool(re.search(r'\[(Cooperate|Defect)\]',raw,re.I)))
    if fid=='pig_dice' and valid and before['turn_total']>0:
        labels['risk_taking']=re.search(r'\[(roll|hold)\]',raw,re.I)[1].lower()=='roll'
    if fid=='negotiation':
        labels.update(submitted_offer=bool(re.search(r'\[Offer:',raw,re.I)),submitted_accept=bool(re.search(r'\[Accept\]',raw,re.I)))
    if fid=='blind_auction' and before['phase']=='bidding':
        bids=re.findall(r'\[Bid\s+(?:on\s+)?(?:Item\s+)?\d+\s*:\s*(\d+)\]',raw,re.I)
        labels['submitted_bid_total']=sum(map(int,bids)) if bids else None
    return labels


def episode_rows(record,plan,splits):
    item=record['item']; game=item['game']; focal=[s for s in record['steps'] if s['is_focal']]; fid=game['family_id']
    config=plan['models'][item['model']]
    player=dict(implementation='llm',model_id=item['model'],provider=config['provider'],provider_model=config['provider_model'],
        temperature=config['temperature'],reasoning_setting=config['reasoning_effort'],sampling_seed=None)
    opening=record['opening_observations'][str(item['seat'])]
    inputs=dict(family_id=fid,game_id=game['configuration_id'],natural_language=game['natural_language'],structured=game['structured'],
        player=player,role=dict(seat_id=item['seat'],strategic_role='solver' if game['num_players']==1 else 'competitor'),
        context=dict(prompt_condition=item['condition'],opponent_implementation='none' if game['num_players']==1 else 'scripted',
            opponent_policy=FAMILIES[fid]['opponent_policy'],opening_observations=opening),
        opening_messages=messages(game,opening,item['condition']))
    groups=dict(family_id=fid,configuration_id=game['configuration_id'],opening_group=item['opening_group'])
    metadata=dict(episode_id=item['episode_id'],instance_id=item['instance_id'],environment_seed=item['seed'],
        seed_seat_block=item['seed_seat_block'],groups=groups,splits={k:splits[k][v] for k,v in groups.items()},
        status=record['status'],trace_path='../episodes/'+item['episode_id']+'.json',
        source_plan_sha256=digest(plan),source_manifest_sha256=plan['data_manifest_sha256'])
    targets=[action_labels(s,fid) for s in focal]
    behavior={name+'_rate':rate(t[name] for t in targets) for name in ('cooperation','defection','risk_taking')}
    behavior.update(invalid_action_rate=rate(not t['native_valid'] for t in targets)['value'],
        native_acceptance_rate=rate(t['native_valid'] for t in targets),
        exploitation_rate=rate([]),coordination_rate=rate([]),deception_rate=rate([]),
        exploration_rate=rate([]),rule_adherence_rate=rate([]))
    complete=record['status']=='complete'
    state=record.get('final_state') or (record['steps'][-1]['after'] if record['steps'] else record['opening_state'])
    reward=(state.get('rewards') or {}).get(str(item['seat'])) if complete else None
    outcome=dict(native_reward=reward,win=(reward==1) if reward is not None else None,
        draw=(reward==0) if reward is not None and game['num_players']==2 else None,
        win_credit=(1 if reward==1 else .5 if reward==0 and game['num_players']==2 else 0) if reward is not None else None,
        definition='Strict native two-player win or full single-player solution; ties separate; partial puzzle credit retained as native_reward',
        native_game_info=state.get('game_info') if complete else None)
    row=dict(**metadata,inputs=inputs,labels=dict(behavior=behavior,outcome=outcome,focal_actions=len(focal),all_actions=len(record['steps'])))
    actions=[dict(**metadata,inputs=inputs,turn=i,messages=s['messages'],target_action=s['raw_action'],valid=t['native_valid'],
        action_labels=t,call_id=s['call']['call_id']) for i,(s,t) in enumerate(zip(focal,targets))]
    return row,actions


def jsonl(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(''.join(json.dumps(r,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n' for r in rows))


def export(run_dir,gameable=Path('prediction/scaleup/runs/pilot-20260910/export')):
    run_dir=Path(run_dir).resolve(); plan=read_json(run_dir/'plan.json'); data=Path(plan['data_dir']); manifest=read_json(data/'manifest.json')
    if plan['source_hashes']!=source_hashes() or plan['environment']!=environment_record(): raise AssertionError('Collection sources changed')
    if plan['data_manifest_sha256']!=digest(manifest): raise AssertionError('Dataset manifest changed')
    for name,sha in manifest['hashes'].items():
        if digest(read_json(data/name))!=sha: raise AssertionError('Dataset artifact changed: '+name)
    splits=read_json(data/'splits.json'); rows=[]; actions=[]; status=Counter(); errors=[]; transitions=0; call_ids=[]; incomplete=[]
    for item in plan['episodes']:
        path=run_dir/'episodes'/(item['episode_id']+'.json')
        if not path.exists(): status['not_started']+=1; continue
        record=read_json(path)
        if record['item']!=item: raise AssertionError('Plan mismatch')
        session=replay(item,record,run_dir/'raw_calls')
        if record.get('final_state') and record['final_state']!=session.snapshot(): raise AssertionError('Final state mismatch')
        if record['status']=='complete' and not session.env.state.done: raise AssertionError('False completion')
        transitions+=len(record['steps']); status[record['status']]+=1
        row,arows=episode_rows(record,plan,splits); rows.append(row); actions.extend(arows)
        call_ids.extend(a['call_id'] for a in arows)
        if record['status']=='incomplete':
            incomplete.append(dict(episode_id=item['episode_id'],family_id=item['game']['family_id'],model=item['model'],condition=item['condition'],
                failure_reason=record.get('failure_reason'),observed_focal_actions=len(arows),
                pending_attempt_statuses=[a['meta']['status'] for a in record['attempts'].get(str(len(record['steps'])),[])]))
    if len(call_ids)!=len(set(call_ids)): raise AssertionError('Raw call reused as multiple actions')
    usage=Counter(); raw_calls={}
    for path in (run_dir/'raw_calls').glob('*.json'):
        call=read_json(path); raw_calls[call['call_id']]=call
        usage['requests']+=1; usage['status:'+call['status']]+=1
        if call['request']['max_tokens']!=plan['max_tokens'] or call['request']['temperature']!=.7 or call['request']['extra_body']['reasoning']['effort']!='low':
            raise AssertionError('Inference protocol mismatch')
        usage['reported_cost_usd']+=call.get('budget_cost_usd') or 0
        for key in ['prompt_tokens','completion_tokens','total_tokens']: usage[key]+=(call.get('response',{}).get('usage') or {}).get(key,0) or 0
    for a in actions:
        call=raw_calls[a['call_id']]
        if call['config']!=plan['models'][a['inputs']['player']['model_id']]: raise AssertionError('Model routing mismatch')
    out=run_dir/'export'; jsonl(out/'episodes.jsonl',rows); jsonl(out/'actions.jsonl',actions)
    summary=dict(created=now(),source_plan_sha256=digest(plan),source_manifest_sha256=plan['data_manifest_sha256'],
        label_export_source_sha256=digest(Path(__file__).read_text()),
        planned=len(plan['episodes']),statuses=dict(status),focal_actions=len(actions),invalid_actions=sum(not a['valid'] for a in actions),
        incomplete_episodes=incomplete,
        usage=dict(usage),audit=dict(replayed_episodes=len(rows),replayed_transitions=transitions,raw_action_links=len(call_ids),errors=errors),
        dataset=dict(families=manifest['families'],configurations=manifest['configurations'],seeded_instances=manifest['seeded_instances'],distinct_opening_groups=manifest['distinct_opening_groups']))
    strata=[]
    for fid in FAMILIES:
        selected=[r for r in rows if r['inputs']['family_id']==fid]
        complete=[r for r in selected if r['status']=='complete']; selected_actions=[a for a in actions if a['inputs']['family_id']==fid]
        strata.append(dict(family_id=fid,complete=len(complete),episodes=len(selected),focal_actions=len(selected_actions),invalid_actions=sum(not a['valid'] for a in selected_actions),
            strict_wins_or_solutions=sum(r['labels']['outcome']['win'] for r in complete),draws=sum(r['labels']['outcome']['draw'] or False for r in complete)))
    summary['by_family']=strata
    model_prompt=[]
    for model in plan['models']:
        for condition in ('normal','active_exploration'):
            selected=[r for r in rows if r['inputs']['player']['model_id']==model and r['inputs']['context']['prompt_condition']==condition and r['status']=='complete']
            selected_actions=[a for a in actions if a['inputs']['player']['model_id']==model and a['inputs']['context']['prompt_condition']==condition]
            two=[r for r in selected if r['inputs']['structured']['num_players']==2]
            one=[r for r in selected if r['inputs']['structured']['num_players']==1]
            model_prompt.append(dict(model=model,condition=condition,complete=len(selected),focal_actions=len(selected_actions),
                invalid_actions=sum(not a['valid'] for a in selected_actions),two_player_episodes=len(two),
                two_player_wins=sum(r['labels']['outcome']['win'] for r in two),two_player_draws=sum(r['labels']['outcome']['draw'] for r in two),
                single_player_episodes=len(one),single_player_solutions=sum(r['labels']['outcome']['win'] for r in one)))
    summary['by_model_prompt']=model_prompt
    planned_by_family=Counter(e['game']['family_id'] for e in plan['episodes'])
    planned_configurations=len({e['game']['configuration_id'] for e in plan['episodes']})
    observed_configurations=len({r['inputs']['game_id'] for r in rows if r['status']=='complete'})
    summary.update(planned_configurations=planned_configurations,observed_configurations=observed_configurations)
    common=[]
    def common_row(row,dataset):
        inp=row['inputs']; lab=row['labels']; players=inp['structured'].get('num_players',inp['structured'].get('players'))
        return dict(dataset=dataset,episode_id=row['episode_id'],family_id=inp['family_id'],model_id=inp['player']['model_id'],provider=inp['player']['provider'],
            prompt_condition=inp['context']['prompt_condition'],seat_id=inp['role']['seat_id'],num_players=players,
            invalid_action_rate=lab['behavior']['invalid_action_rate'],win_credit=lab['outcome']['win_credit'])
    common.extend(common_row(r,'general_textarena') for r in rows if r['status']=='complete')
    if (gameable/'episodes.jsonl').exists():
        other=[json.loads(line) for line in (gameable/'episodes.jsonl').read_text().splitlines()]
        common.extend(common_row(r,'gameable') for r in other)
        summary['comparison_source']=dict(path=str(gameable.resolve()),episodes_sha256=digest(other),episodes=len(other))
    jsonl(out/'comparison-episodes.jsonl',common)
    write_json(out/'summary.json',summary)
    report=["# General TextArena coverage · first dataset and pilot",'',
        f"The catalog contains **{manifest['families']} families, {manifest['configurations']} native parameter configurations, and {manifest['seeded_instances']} seeded instances** ({manifest['distinct_opening_groups']} distinct opening-state groups). Seeds are repetitions, not additional game designs.",
        '',f"Live collection: **{status['complete']}/{len(plan['episodes'])} complete episodes**, {len(actions)} focal actions, {summary['invalid_actions']} native invalid actions. Status counts: `{dict(status)}`. Scripted fixtures are excluded.",
        '',"| Family | Complete / planned | Focal actions | Native invalid | Strict wins / full solutions | Draws |",'|---|---:|---:|---:|---:|---:|']
    for s in strata: report.append(f"| {FAMILIES[s['family_id']]['title']} | {s['complete']} / {planned_by_family[s['family_id']]} | {s['focal_actions']} | {s['invalid_actions']} | {s['strict_wins_or_solutions']} | {s['draws']} |")
    for missing in incomplete:
        report += ['',f"Incomplete episode `{missing['episode_id']}`: {missing['family_id']} / {missing['model']} / {missing['condition']}; {missing['observed_focal_actions']} observed focal actions, then `{missing['failure_reason']}` with attempt statuses `{missing['pending_attempt_statuses']}`. Its terminal outcome stays null; its observed prefix remains in the action export."]
    report += ['',"| Model / prompt | Complete | Native invalid / focal actions | Two-player wins / episodes | Draws | Single-player solutions / episodes |",'|---|---:|---:|---:|---:|---:|']
    for s in model_prompt:
        report.append(f"| {s['model']} / {s['condition']} | {s['complete']} | {s['invalid_actions']} / {s['focal_actions']} | {s['two_player_wins']} / {s['two_player_episodes']} | {s['two_player_draws']} | {s['single_player_solutions']} / {s['single_player_episodes']} |")
    report += ['',"These small descriptive counts are conditional on each family's particular scripted opponent and seed/seat blocks. They do not establish a model ranking or an exploration benefit.",
        '',"Nine families are two-player games against an information-restricted scripted opponent; three are single-player tasks. Provider is uniformly OpenRouter, temperature 0.7, requested reasoning low, maximum output 16,384 tokens. Native horizons vary.",
        '',("Each family uses one base configuration, two seed/seat blocks, two models, and normal/exploration prompts. Seats alternate across the two blocks in two-player games: seed and seat are not independently crossed." if planned_configurations==12 else plan['protocol']),
        '',f"**This collection measures coverage and observable behavior. It does not establish whether general games are harder to predict, or whether few-shot prompting beats a learned predictor.** The catalog has 49 validated configurations; this plan selects {planned_configurations}, with {observed_configurations} represented by complete model episodes. No predictor evaluation is performed by this export.",
        '',"Comparison with the current Gameable Games pilot:",'',
        '| Property | General TextArena | Gameable Games |','|---|---|---|',
        '| Selection | Purposive breadth across ordinary game structures | Behavioral mechanisms and gameability controls |',
        '| Catalog | 12 families; 49 parameter configurations; 196 seed instances | 24 families; 3,256 base variants + 2,800 controls |',
        f"| Live collection | {len(plan['episodes'])} planned episodes; 12 families | 144 complete episodes; 10 families |",
        '| Actors | One focal model + one bot, or one solver | One focal model + two scripted rivals |',
        '| Horizon | Native termination, externally bounded | Six focal actions |',
        '| Shared protocol | Qwen / GLM, normal / exploration, 0.7, low reasoning, 16,384 cap | Same |',
        '| Provider | OpenRouter | 77 FLT + 67 OpenRouter episodes |',
        '| Labels | Native validity, outcomes, family-specific behavior | Validity, outcomes, mechanism-specific behavior |',
        '',"`comparison-episodes.jsonl` aligns model, provider, prompt, seat, player count, invalid-action rate and win credit across both exports. These are descriptive measurements, not difficulty-adjusted scores. Win credit, action opportunity counts, opponents, horizons and family composition differ. Report family-level results and macro averages, and examine the OpenRouter subset separately; the Gameable provider assignment was not random. Do not compare pooled raw scores or convert unsupported social/exploitation labels to zero.",
        '',"For a predictor comparison, collect multiple parameter configurations and independent seed × seat trials in both tracks; use identical player inputs and matched training/example budgets. Evaluate within each track on held-out configurations and whole families, then train on one track and test on the other. Compare Brier/log loss for shared binary targets and supported behavioral rates, plus family-normalized next-action loss with explicit legal-action representations. Report completion/missingness and family-level uncertainty. The supplied grouped splits prevent repeated trajectories leaking across sets; the current base-only pilot cannot identify parameter generalization.",
        '',f"Validation: {manifest['validation']['scripted_episodes']} scripted fixture replays; {manifest['validation']['replayed_transitions']} fixture transitions; {transitions} live transitions replayed; {len(call_ids)} focal actions linked to exact raw successful provider calls. Future outcomes and global/other-player hidden states are stored only outside `inputs` and outside pre-action `messages`. Native engine acceptance is not a claim of honesty or rule adherence.",
        '',"Observed inference usage (includes retries, including any incomplete episodes):",'', '```json',json.dumps(dict(usage),indent=2),'```',
        '',"See the [dataset card](../../../data/20260910-v1/DATASET_CARD.md) and [collection instructions](../../../README.md) for sampling, labels, native engine quirks, provenance, and commands. Engine source: [TextArena](https://github.com/TextArena/TextArena), installed version 0.7.4; the installed code is fingerprinted rather than upgraded."]
    (out/'REPORT.md').write_text('\n'.join(report)+'\n')
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--run',type=Path,default=DEFAULT_RUN); args=parser.parse_args(); print(json.dumps(export(args.run),indent=2))
