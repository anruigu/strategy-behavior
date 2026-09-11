from .readout import scores,comparisons,independent_checks
from .labels import TARGETS
from . import DATA
from prediction.io_utils import read_json


def test_family_weighting_and_direction_of_paired_comparison():
    rows=[]; predictions=[]
    for i in range(6):
        for rep in range(2 if i else 8): rows.append(dict(condition_id=str(i),inputs=dict(family_id=str(i)),targets={t:float(i>0) for t in TARGETS}))
        for arm,p in [('depth',.5),('breadth',.8)]:
            for method in ('linear','corrected_4','few_4','few_8','few_16','training_mean'):
                predictions.append(dict(arm=arm,method=method,query_id=str(i),forecast={t:p for t in TARGETS}))
    result,lookup=scores(rows,predictions)
    assert all(abs(r['score']-.25)<1e-12 for r in result if r['arm']=='depth')
    expected=(.64+5*.04)/6
    assert all(abs(r['score']-expected)<1e-12 for r in result if r['arm']=='breadth')
    comp=comparisons(lookup)
    assert all(abs(c['difference']-(expected-.25))<1e-12 for c in comp if c['comparison']=='breadth_minus_depth')


def test_independent_accounting_on_every_new_native_fixture():
    catalog=read_json(DATA/'catalog.json'); games={g['configuration_id']:g for g in catalog['configurations']}
    instances={i['instance_id']:i for i in read_json(DATA/'instances.evaluator.json')}
    counts={}
    for fixture in read_json(DATA/'fixtures.evaluator.json'):
        instance=instances[fixture['instance_id']]; g=games[instance['configuration_id']]
        trace=fixture['trace']; trace['item']=dict(game=g)
        checks=independent_checks(trace)
        for k,n in checks.items(): counts[k]=counts.get(k,0)+n
    assert counts['gops_prize_accounting']==39
    assert counts['blackjack_hand_and_reward_accounting']==6
    assert counts['sokoban_terminal_fraction']==6
