"""Native edge cases that distinguish executed behavior from surface tokens."""
from prediction.io_utils import read_json
from prediction.general_games.native import jsonable
from . import STUDY
from .catalog import configurations
from .runtime import Session,view
from .labels import step_values,episode_row


def session(family):
    return Session(next(g for g in configurations() if g['family_id']==family),6200)


def submit(s,raw):
    actor,incoming,h=s.observe();before=s.snapshot();v=view(s,actor,h);result=s.step(raw)
    step=dict(index=before['turn'],actor=actor,is_focal=True,incoming=incoming,visible_state=v,before=before,after=s.snapshot(),raw_action=raw,result=result,messages=[])
    return step,step_values(step,s.game['family_id'],s.game['parameters'])


def test_auction_duplicate_charge_and_invalid_zero():
    s=session('blind_auction');submit(s,'Ready.');submit(s,'Ready.')
    step,labels=submit(s,'[Bid 0: 10] [Bid 0: 20]')
    assert not step['result']['native_invalid']
    assert labels['bid_budget_fraction']==30/400
    assert step['after']['game_state']['player_bids']['0']['0']==20
    s=session('blind_auction');submit(s,'Ready.');submit(s,'Ready.')
    step,labels=submit(s,'[Bid 0: 0]')
    assert step['result']['native_invalid'] and 'bid_budget_fraction' not in labels


def test_ultimatum_execution_and_fixed_role_support():
    s=session('ultimatum');_,labels=submit(s,'[Offer: 4]');assert labels['offer_share']==.4
    step,labels=submit(s,'[Accept] [Reject]');assert labels['acceptance_rate']==1
    assert step['after']['game_state']['player_totals']=={'0':6,'1':4}
    items=[e for e in read_json(STUDY/'test/plan.json')['episodes'] if e['game']['family_id']=='ultimatum' and not e['game']['parameters']['alternate_roles']]
    for seat in (0,1):
        item=next(e for e in items if e['seat']==seat);s=Session(item['game'],item['seed'])
        row,_=episode_row(dict(item=item,status='planned',steps=[],opening_observations=jsonable(s.opening)),'test-contract')
        assert ('offer_share' in row['supported'])==(seat==0)
        assert ('acceptance_rate' in row['supported'])==(seat==1)
        assert all(v is None for v in row['targets'].values())


def test_memory_opportunities_require_publicly_revealed_pair():
    s=session('memory');_,first=submit(s,'[0 0 0 1]');assert first=={'new_card_fraction':1}
    _,second=submit(s,'[3 1 1 0]');assert second=={'new_card_fraction':1}
    _,third=submit(s,'[0 0 3 1]');assert third=={'known_pair_rate':1,'new_card_fraction':0}


def test_secretary_terminal_message_and_two_thirds_round_reset():
    item=next(e for e in read_json(STUDY/'test/plan.json')['episodes'] if e['game']['family_id']=='secretary' and e['seed']==6200 and e['game']['parameters']['N']==6)
    s=Session(item['game'],item['seed']);opening=jsonable(s.opening);steps=[]
    step,_=submit(s,'[continue]');steps.append(step);step,_=submit(s,'[accept]');steps.append(step)
    row,_=episode_row(dict(item=item,status='complete',steps=steps,opening_observations=opening,final_state=s.snapshot()),'test-contract')
    assert s.snapshot()['game_state']['accepted_idx'] is None  # Native field is unused.
    assert row['targets']['selection_fraction']==2/6 and row['targets']['win']==1
    s=session('two_thirds');_,a=submit(s,'[30]');step,b=submit(s,'[20]')
    assert a['normalized_guess']==.3 and b['normalized_guess']==.2
    assert step['after']['game_state']['guesses']=={}
