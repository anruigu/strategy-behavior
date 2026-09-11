from .readout import scores,repeatability
from .labels import TARGETS


def row(ident,family,win):
    return dict(condition_id=ident,status='complete',inputs=dict(family_id=family),targets={t:win if t=='win' else None for t in TARGETS})


def test_scores_weight_families_and_conditions_before_episode_counts():
    # Five repetitions in one family must not outweigh another family's two.
    rows=[row('a','prisoners_dilemma',1)]*5+[row('b','pig_dice',0)]*2
    queries={i:dict(inputs=dict(family_id=f)) for i,f in [('a','prisoners_dilemma'),('b','pig_dice')]}
    predictions=[dict(size=440,suite='parameter',method='few_4',query_id=i,forecast={t:.8 if t=='win' else None for t in TARGETS}) for i in queries]
    result,_=scores(rows,predictions,queries);r=result[0]
    assert abs(r['score']-.34)<1e-12 and r['episodes']==7 and r['conditions']==2
    doubled,_=scores(rows+[row('a','prisoners_dilemma',1)]*5,predictions,queries)
    assert doubled[0]['score']==r['score']


def test_repeat_noise_is_not_mistaken_for_replay_failure_or_learnable_error():
    rr=[row('a','prisoners_dilemma',0),row('a','prisoners_dilemma',1)]
    r=repeatability(rr)[0]['targets']['win']
    assert r['within_condition_variance']==.5 and r['varying_conditions']==1
    forecasts=[dict(size=440,suite='parameter',method='few_4',query_id='a',forecast={t:.5 if t=='win' else None for t in TARGETS})]
    s,_=scores(rr,forecasts,{'a':dict(inputs=dict(family_id='prisoners_dilemma'))})
    assert s[0]['score']==.25 and s[0]['noise_subtracted']==-.25


def test_undefined_behavior_is_not_scored_as_zero():
    r=row('a','prisoners_dilemma',0);q={'a':dict(inputs=dict(family_id='prisoners_dilemma'))}
    forecast={t:.5 if t in ('win','cooperation_rate') else None for t in TARGETS}
    s,_=scores([r],[dict(size=440,suite='parameter',method='few_4',query_id='a',forecast=forecast)],q)
    assert [x['target'] for x in s]==['win']
