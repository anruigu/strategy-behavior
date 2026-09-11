"""Observed native behavior with explicit opportunity counts and family support."""
from collections import defaultdict
import math
import re
from statistics import mean

from prediction.general_games.export import action_labels as old_labels
from prediction.general_games.native import messages
from prediction.io_utils import digest
from .catalog import FAMILIES

DEFINITIONS={
 'win':'Probability of a strict native two-player win, or full single-player solution. Draws and partial puzzle rewards are not wins.',
 'any_invalid':'Probability of at least one native-invalid focal submission in the episode.',
 'cooperation_rate':'Fraction of PD decision-phase submissions that execute cooperation, including the native default.',
 'risk_taking_rate':'Fraction of valid Pig decisions with positive unbanked points that roll.',
 'allocation_concentration':'Mean largest-field allocation divided by the total unit budget on valid Blotto allocations.',
 'bid_budget_fraction':'Mean capital spent on accepted bidding-phase submissions divided by capital immediately before the submission; losing bids also cost money.',
 'challenge_rate':'Fraction of valid Liar’s Dice decisions facing an existing bid that call rather than raise.',
 'offer_rate':'Fraction of valid negotiation submissions that create an offer, identified by a valid offer token and the resulting own proposal.',
 'acceptance_rate':'Fraction of valid responses to an existing opponent offer that accept (negotiation or ultimatum).',
 'offer_share':'Mean amount offered to the responder divided by the pool on valid ultimatum proposals.',
 'normalized_guess':'Mean valid two-thirds-game guess, normalized from the lower to upper bound.',
 'selection_fraction':'Index of the ultimately selected secretary value divided by N, measured from the terminal selection message.',
 'known_pair_rate':'Fraction of valid memory moves with a publicly known unmatched pair available that select such a pair.',
 'new_card_fraction':'Mean fraction of the two selected memory cards whose identities had not previously been publicly revealed.',
}
EXTRAS={'prisoners_dilemma':['cooperation_rate'],'pig_dice':['risk_taking_rate'],'colonel_blotto':['allocation_concentration'],
        'blind_auction':['bid_budget_fraction'],'liars_dice':['challenge_rate'],'negotiation':['offer_rate','acceptance_rate'],
        'ultimatum':['offer_share','acceptance_rate'],'two_thirds':['normalized_guess'],'secretary':['selection_fraction'],
        'memory':['known_pair_rate','new_card_fraction']}
TARGETS=tuple(DEFINITIONS)


def supported(family):return ['win','any_invalid']+EXTRAS.get(family,[])


def step_values(step,family,parameters):
    result={};v=step['visible_state'];raw=step['raw_action'];valid=not step['result']['native_invalid'];actor=str(step['actor'])
    if family in ('prisoners_dilemma','pig_dice'):
        old=old_labels(step,family)
        for k in ('cooperation','risk_taking'):
            if old[k] is not None:result[k+'_rate']=float(old[k])
    if not valid:return result
    before=step['before']['game_state'];after=step['after']['game_state']
    if family=='colonel_blotto':
        from textarena.envs.ColonelBlotto.env import ColonelBlottoEnv
        allocation=ColonelBlottoEnv(**parameters)._parse_allocation_input(raw)
        assert sum(allocation.values())==parameters['num_total_units']
        result['allocation_concentration']=max(allocation.values())/parameters['num_total_units']
    if family=='blind_auction' and v['phase']=='bidding' and v['own_capital']>0:
        spent=before['remaining_capital'][actor]-after['remaining_capital'][actor]
        result['bid_budget_fraction']=spent/v['own_capital']
    if family=='liars_dice' and v['current_bid'] and v['current_bid'].get('quantity',0)>0:
        result['challenge_rate']=float(bool(re.search(r'\[Call\]',raw,re.I)))
    if family=='negotiation':
        from textarena.envs.SimpleNegotiation.env import SimpleNegotiationEnv
        has_offer=bool(SimpleNegotiationEnv(**parameters).offer_pattern.search(raw))
        result['offer_rate']=float(has_offer and bool(after['current_offer']) and str(after['current_offer']['from_player'])==actor)
        if before['current_offer'] and str(before['current_offer']['from_player'])!=actor:
            result['acceptance_rate']=float(len(after['trade_history'])>len(before['trade_history']))
    if family=='ultimatum':
        if v['phase']=='offering':result['offer_share']=after['current_offer']/parameters['pool']
        else:result['acceptance_rate']=float(after['round_history'][-1]['decision']=='Accept')
    if family=='two_thirds':
        value=after['guesses'].get(actor) if after['guesses'] else after['history'][-1][actor]
        result['normalized_guess']=(value-parameters['min_guess'])/(parameters['max_guess']-parameters['min_guess'])
    if family=='memory':
        coords=list(map(int,re.search(r'\[(\d+) (\d+) (\d+) (\d+)\]',raw).groups()));chosen=[f'{coords[0]},{coords[1]}',f'{coords[2]},{coords[3]}']
        matched={f'{r},{c}' for r,c in v['matched']};known={p:symbol for p,symbol in v['known'].items() if p not in matched}
        counts=defaultdict(int)
        for symbol in known.values():counts[symbol]+=1
        if any(n>=2 for n in counts.values()):result['known_pair_rate']=float(all(p in known for p in chosen) and known[chosen[0]]==known[chosen[1]])
        result['new_card_fraction']=sum(p not in known for p in chosen)/2
    assert all(math.isfinite(x) and 0<=x<=1 for x in result.values()),result
    return result


def episode_row(trace,source_run):
    item=trace['item'];g=item['game'];family=g['family_id'];focal=[s for s in trace['steps'] if s['is_focal']]
    values=defaultdict(list);actions=[]
    for step in focal:
        labels=step_values(step,family,g['parameters'])
        for k,v in labels.items():values[k].append(v)
        actions.append(dict(episode_id=item['episode_id'],native_step=step['index'],raw_action=step['raw_action'],valid=not step['result']['native_invalid'],measurements=labels,messages=step['messages']))
    complete=trace['status']=='complete';reward=(trace.get('final_state',{}).get('rewards') or {}).get(str(item['seat'])) if complete else None
    if family=='secretary' and complete:
        # accepted_idx is never assigned by this native implementation.
        reason=trace['final_state']['game_info'][str(item['seat'])].get('reason','')
        m=re.search(r'at draw (\d+)/(\d+)',reason)
        if m:values['selection_fraction'].append(int(m[1])/int(m[2]))
    targets={k:None for k in TARGETS}
    targets.update(win=float(reward==1) if reward is not None else None,
        any_invalid=float(any(s['result']['native_invalid'] for s in focal)) if complete else None)
    targets.update({k:mean(v) for k,v in values.items()})
    # An incomplete prefix has no completed-episode behavior target.
    if not complete:targets={k:None for k in TARGETS}
    inputs=dict(family_id=family,game_id=g['configuration_id'],structured=g['structured'],model=item['model'],seat=item['seat'],prompt=item['condition'],
        opening_messages=messages(g,trace['opening_observations'][str(item['seat'])],item['condition']),
        opponent_policy=FAMILIES[family]['opponent_policy'])
    allowed=supported(family)
    if family=='ultimatum' and not g['parameters']['alternate_roles']:
        allowed.remove('acceptance_rate' if item['seat']==0 else 'offer_share')
    condition_id='condition-'+digest([g['configuration_id'],item['seed'],item['seat'],item['model'],item['condition']])[:20]
    row=dict(episode_id=item['episode_id'],source_run=source_run,status=trace['status'],condition_id=condition_id,
        opening_group=item['opening_group'],seed=item['seed'],replicate=item.get('replicate',0),inputs=inputs,targets=targets,
        opportunities={k:dict(sum=sum(v),count=len(v),value=mean(v)) for k,v in values.items()},
        supported=allowed,focal_actions=len(focal),native_transitions=len(trace['steps']),native_reward=reward,
        invalid_actions=sum(s['result']['native_invalid'] for s in focal),observable_input_group='input-'+digest(inputs)[:20])
    return row,actions
