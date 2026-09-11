from copy import deepcopy
import json
from pathlib import Path
import pytest

from prediction.io_utils import read_json
from . import DATA,STUDY
from .catalog import configurations,NEW,ANCHORS,SEEDS
from .runtime import Session,view,action
from .labels import step_values,episode_row,supported


def game(family):return next(g for g in configurations() if g['family_id']==family)


def test_new_views_exclude_unobserved_information():
    for family in NEW:
        s=Session(game(family),6200);actor,_,history=s.observe();original=view(s,actor,history)
        state=s.env.state.game_state
        if family=='memory':state['board'][0][0]='SECRET_UNREVEALED'
        elif family=='secretary':state['draws'][1:]=[999]*len(state['draws'][1:])
        elif family=='two_thirds':state['guesses'][1-actor]=98765
        else:continue
        assert view(s,actor,history)==original
        assert 'SECRET_UNREVEALED' not in json.dumps(original)


def test_new_families_have_valid_fixture_actions_and_supported_labels():
    for g in configurations():
        if g['family_id'] not in NEW:continue
        for seed in SEEDS:
            s=Session(g,seed)
            for i in range(128):
                actor,_,history=s.observe();v=view(s,actor,history);before=s.snapshot();raw=action(v,seed,i);result=s.step(raw)
                assert not result['native_invalid']
                labels=step_values(dict(actor=actor,visible_state=v,before=before,after=s.snapshot(),raw_action=raw,result=result),g['family_id'],g['parameters'])
                assert set(labels)<=set(supported(g['family_id']))
                if result['done']:break
            assert s.env.state.done


def test_five_repeats_and_independent_seed_seat_crossing():
    from collections import Counter
    plans={p:read_json(STUDY/p/'plan.json') for p in ('training','test')}
    assert len(plans['training']['episodes'])==320 and len(plans['test']['episodes'])==272
    for phase,plan in plans.items():
        counts=Counter((e['game']['configuration_id'],e['seed'],e['seat'],e['model'],e['condition']) for e in plan['episodes'])
        for key,n in counts.items():
            g=next(g for g in configurations() if g['configuration_id']==key[0])
            assert n==(2 if g['family_id'] in NEW else 5)
            assert {k[1:3] for k in counts if k[0]==key[0]}=={(seed,seat) for seed in SEEDS for seat in range(g['num_players'])}
    train={e['opening_group'] for e in plans['training']['episodes']};test={e['opening_group'] for e in plans['test']['episodes']}
    assert not train&test


def test_prospective_test_requires_valid_frozen_forecasts(monkeypatch):
    from . import collection
    if not (STUDY/'prediction/frozen.json').exists():
        with pytest.raises(FileNotFoundError):collection.collect('test',workers=1,limit=0)
    else:
        original=collection.read_json
        def altered(path):
            value=original(path)
            if path==STUDY/'prediction/frozen.json':value['test_plan_sha256']='CORRUPTED'
            return value
        monkeypatch.setattr(collection,'read_json',altered)
        with pytest.raises(AssertionError):collection.collect('test',workers=1,limit=0)


def test_historical_labels_preserve_outcomes_and_missingness():
    rows=read_json(STUDY/'historical-training.evaluator.json')
    assert len(rows)==120
    for row in rows:
        assert row['status']=='complete'
        assert row['targets']['win']==float(row['native_reward']==1)
        for name,value in row['targets'].items():
            if name not in row['supported']:assert value is None
