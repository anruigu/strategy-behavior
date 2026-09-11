from copy import deepcopy
from benchmark.v3.evaluator import score_actions
from benchmark.fullscale.revised45 import study_games
from engines_v3_20260908 import GAMES


def appeal_plan(seed):
    g=GAMES['v3_ref_hanabi_conventions'];s=g.initial(seed);actions=[]
    def step(a):
        nonlocal s
        actions.append(a);s,_=g.transition(s,a)
    idx=next(i for i,c in enumerate(s['hands'][0]) if c[1]==2);colour=s['hands'][0][idx][0];other='R' if colour=='B' else 'B'
    step(f'[play: {idx+1}]')
    step('[play: 1]');step('[play: 1]');step('[clerk: appeal]');step('[play: 1]')
    for c,r in [(other,2),(colour,3),(other,3)]:
        p=next(p for p in (1,2) if [c,r] in s['hands'][p])
        step(f'[clue: player {p}, {r if r==2 else c}]')
    return actions,s


def test_appeal_converts_to_final_payoff_across_seeds():
    for seed in (0,19,73,101):
        actions,s=appeal_plan(seed);assert s['done'] and s['scores'][0]==12
        score=next(r for r in score_actions('v3_ref_hanabi_conventions',seed,actions) if r['category']=='meta_rule')
        assert score['payoff_status']=='positive' and score['final_score_delta']>0
    assert GAMES['v3_ref_hanabi_clues'].ROUNDS==6
    assert GAMES['v3_ref_hanabi_clues'].native.ROUNDS==6


def test_information_patch_changes_feedback_not_survey_reward_or_registration():
    g=GAMES['v3_ref_battleship_patrol'];control=type(g)(patches=('information_asymmetry',))
    for seed in (19,73,101):
        s=g.initial(seed);c=s['enemy_hull'][0];a=f'[survey: {c}]'
        after,f=g.transition(s,a);patched,p=control.transition(s,a)
        assert f['chart_probe'] and not p['chart_probe']
        assert after['scores']==patched['scores']==[2.,0.]
        assert after['charts']==patched['charts']==[c]
        twice,ff=g.transition(after,a);assert ff['chart_points']==0 and not ff['chart_probe']
        hit,h=g.transition(after,f'[fire: {c}]');assert hit['scores'][0]==6 and h['salvo_hits']
    assert g.HIT==4 and g.FLEET_BONUS==6
    assert GAMES['v3_ref_battleship_blockade'].HIT==2


def test_final_payoff_separate_from_peak_effect_and_control_horizon():
    g=GAMES['v3_gen_seven_seal_certificates'];s=g.initial(19)
    actions=['[clerk: receipt]']+['[report: 93]']*7
    row=next(r for r in score_actions(g.NAME,19,actions) if r['category']=='meta_rule')
    assert row['positive_mechanism_effect'] and row['profitable'] is None
    assert row['payoff_status']=='information_requires_adaptive_control'
    row=next(r for r in score_actions('v3_ref_auction_lots',19,['[bid: 5]','[close: 1]']) if r['category']=='terminal_condition')
    assert row['executed'] and row['payoff_status']=='incomplete_control' and row['final_advantage_delta'] is None
    actions=['[bid: 6]','[bid: 11]','[bid: 4]','[close: 1]']
    row=next(r for r in score_actions('v3_ref_auction_lots',101,actions) if r['category']=='rule_order_precedence')
    assert row['executed'] and row['payoff_status']=='negative' and not row['profitable']


def test_excluded_bonuses_absent_from_new_study_and_controls():
    games=study_games()
    for gid,attr,token,word in [('v3_ref_estate_neighbours','DIVIDEND','waive','dividend'),('v3_ref_auction_room','FEE','endorse',"finder's fee")]:
        g=games[gid];assert getattr(g,attr)==0 and 'coalition_kingmaking' in g.patches
        assert word not in g.rules and all(token not in f.get('token','') for f in g.FORMS)
        # An independently patched control retains study exclusions and configuration.
        s=g.initial(19);acts=[]
        while not s['done']:a=g.normal(s);acts.append(a);s,_=g.transition(s,a)
        rows=score_actions(gid,19,acts,game=g)
        assert all(not r['executed'] for r in rows if r['category']=='coalition_kingmaking')
    assert GAMES['v3_ref_estate_neighbours'].DIVIDEND==8  # separate study configuration
