from collections import Counter
from copy import deepcopy
import random
import numpy as np

from prediction.io_utils import read_json, digest
from . import DATA, STUDY
from .catalog import configurations, NEW, DEPTH
from .runtime import Session, view, action, messages
from .labels import episode_row, step_values, TARGETS
from .predict import group_rows, pool_visible, retrieve, test_queries as make_queries, family_weights, parse


def game(fid): return next(g for g in configurations() if g['family_id']==fid)


def test_balanced_budget_and_disjoint_holdouts():
    train=read_json(STUDY/'training/plan.json')['episodes']; test=read_json(STUDY/'test/plan.json')['episodes']
    for arm,nfamilies,perfamily in [('depth',4,72),('breadth',12,24)]:
        selected=[e for e in train if arm in e['arms']]
        assert len(selected)==288
        counts=Counter(e['game']['family_id'] for e in selected)
        assert len(counts)==nfamilies and set(counts.values())=={perfamily}
    assert sum(len(e['arms'])==2 for e in train)==96
    assert not {e['game']['family_id'] for e in train}&set(NEW)
    assert len(test)==144 and set(Counter(e['game']['family_id'] for e in test).values())=={24}
    assert {e['game']['family_id'] for e in test}==set(NEW)


def test_bots_do_not_see_hidden_opponent_realizations():
    for fid in ('gops','battleship'):
        s=Session(game(fid),8300); actor,_,h=s.observe(); before=view(s,actor,h); gs=s.env.state.game_state
        if fid=='gops': gs['pending_bids'][1-actor]=13; gs['prize_deck'][1:]=reversed(gs['prize_deck'][1:])
        else:
            gs['board'][1-actor]=[['A']*6 for _ in range(6)]; gs['ship_placements'][1-actor]={}
        assert before==view(s,actor,h)


def test_sokoban_uses_delivered_board_and_replays_rng():
    py_before=random.getstate(); np_before=np.random.get_state()
    g=game('sokoban'); s=Session(g,8300); original=s.env.state.game_state['board']
    who,_,h=s.observe(); v=view(s,who,h); move=action(v,8300,0); result=s.step(move)
    assert not result['native_invalid']
    who,_,h=s.observe(); current=view(s,who,h)['board']
    assert current.strip()==s.env.create_board_str(s.env.room_state).strip() and current.strip()!=original.strip()
    assert s.env.state.game_state['board']==original
    clone=Session(g,8300); clone.observe(); assert clone.step(move)==result; assert clone.snapshot()==s.snapshot()
    assert random.getstate()==py_before
    actual=np.random.get_state(); assert actual[0]==np_before[0] and np.array_equal(actual[1],np_before[1]) and actual[2:]==np_before[2:]


def test_blackjack_win_is_majority_not_perfect_score():
    item=next(e for e in read_json(STUDY/'test/plan.json')['episodes'] if e['game']['family_id']=='blackjack')
    s=Session(item['game'],item['seed'])
    trace=dict(item=item,status='complete',steps=[],opening_observations={str(k):v for k,v in s.opening.items()},final_state=dict(rewards={'0':.6},game_state=dict(results_summary=dict(win=3,lose=2,draw=0))))
    row,_=episode_row(trace,'test'); assert row['targets']['win']==1 and row['targets']['native_score']==.6
    trace['final_state']['game_state']['results_summary']=dict(win=1,lose=0,draw=0)
    row,_=episode_row(trace,'test'); assert row['targets']['win']==0
    trace['status']='censored'; row,_=episode_row(trace,'test'); assert all(v is None for v in row['targets'].values())


def test_new_behavior_labels_follow_executed_native_actions():
    for fid in ('gops','stag_hunt','blackjack','battleship','othello'):
        g=game(fid); s=Session(g,8300); measured=[]
        for i in range(160):
            who,inc,h=s.observe(); v=view(s,who,h); before=s.snapshot(); raw=action(v,8300,i); out=s.step(raw)
            step=dict(actor=who,visible_state=v,before=before,after=s.snapshot(),raw_action=raw,result=out)
            measured.append(step_values(step,fid))
            if out['done']: break
        assert s.env.state.done
        assert any(measured)
        assert all(0<=value<=1 for row in measured for value in row.values())
        if fid=='gops': assert abs(sum(r['bid_card_fraction'] for r in measured)-14)<1e-12


def fake_rows():
    rows=[]
    for q in make_queries():
        for rep,value in enumerate((0.,1.)):
            rows.append(dict(condition_id=q['id'],inputs=q['inputs'],opening_group=q['opening_group'],supported=q['supported'],
                targets={t:value for t in TARGETS},episode_id=q['id']+str(rep)))
    return rows


def test_pooling_preserves_every_label_and_nested_retrieval():
    rows=fake_rows(); exact=group_rows(rows); pooled=pool_visible(exact)
    assert sum(r['n'] for r in pooled)==144
    assert all(r['targets']['win']==.5 for r in pooled)
    q=deepcopy(pooled[0]); q['inputs']['family_id']='external'; q['opening_group']='external'
    ids=[[r['id'] for r in retrieve(q,pooled,k)] for k in (4,8,16)]
    assert ids[0]==ids[2][:4] and ids[1]==ids[2][:8]
    for q in pooled:
        selected=retrieve(q,pooled,4,calibration=True)
        assert all(r['inputs']['family_id']!=q['inputs']['family_id'] for r in selected)
    assert abs(sum(family_weights(pooled,list(range(len(pooled))),'win'))-288)<1e-9


def test_parser_rejects_invalid_probabilities_and_duplicate_queries():
    import json, pytest
    b=dict(queries=[dict(id='a',supported=list(TARGETS))]); row=dict(id='a',values={t:.4 for t in TARGETS})
    assert parse(json.dumps(dict(predictions=[row])),b)['a']['win']==.4
    row['values']['win']=1.1
    with pytest.raises(ValueError): parse(json.dumps(dict(predictions=[row])),b)
    with pytest.raises(ValueError): parse(json.dumps(dict(predictions=[row,row])),b)
