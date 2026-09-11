import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import numpy as np
from model45 import encoder,transform,fit,predict,make_folds


def examples():
    return [dict(model=model,phase='win_only',target=f'g{family}.m{mechanism}',game=f'g{family}',family=f'f{family}',
                 mechanism=f'm{mechanism}',seed=seed,features={'x':float(mechanism)},y=int(mechanism==1))
            for family,mechanism in [(0,0),(1,0),(1,1),(2,1),(2,2),(0,2)]
            for model in ['a','b'] for seed in [19,73]]


def test_all_variants_of_held_out_units_are_excluded():
    rows=examples()
    for scheme in ['edition','family','mechanism','mechanism_purged_family']:
        visited=[]
        for group,train,test in make_folds(rows,scheme):
            visited+=test
            assert not {rows[i]['target'] for i in train}&{rows[i]['target'] for i in test}
            if scheme in ['family','mechanism_purged_family']:
                assert not {rows[i]['family'] for i in train}&{rows[i]['family'] for i in test}
            if scheme.startswith('mechanism'):
                assert not {rows[i]['mechanism'] for i in train}&{rows[i]['mechanism'] for i in test}
        assert sorted(visited)==list(range(len(rows)))


def test_scaler_uses_only_training_data_and_structure_ignores_identifiers():
    rows=examples();enc=encoder(rows,['x'])
    changed={**rows[0],'features':{'x':999.},'game':'unseen','family':'unseen','target':'unseen','seed':999,'mechanism':'unseen'}
    before=list(enc['means']);transform([changed],enc);assert enc['means']==before
    a=transform([rows[0]],enc)
    b=transform([{**rows[0],'game':'new','target':'new','family':'new','seed':999,'mechanism':'new','y':1}],enc)
    assert np.array_equal(a,b)


def test_logistic_constant_context_and_serialized_predictions():
    rows=examples();artifact=fit(rows,'model_prompt',[],[])
    probs=predict(artifact,rows)
    assert np.isfinite(probs).all() and np.all((probs>0)&(probs<1))
    assert abs(probs.mean()-np.mean([r['y'] for r in rows]))<1e-6
    assert artifact['max_abs_gradient']<1e-4
    import json
    assert np.allclose(probs,predict(json.loads(json.dumps(artifact)),rows))
    constant=fit([{**r,'y':0} for r in rows],'structure',['x'],[])
    assert np.all(predict(constant,rows)>0)


def test_forecast_rejects_unknown_context_and_marks_seen_targets():
    from forecast45 import forecast
    import pytest
    rows=examples();artifact=fit(rows,'structure',['x'],[])
    artifact.update(known_player_models=['a','b'],trained_targets=[r['target'] for r in rows],
                    feature_schema={'game_features':{'x':'test'},'witness_features':{}})
    features=[dict(target=rows[0]['target'],seed=19,features={'x':0.})]
    result=forecast(artifact,features,'a','win_only')
    assert result[0]['in_training_target'] and 0<result[0]['probability']<1
    with pytest.raises(ValueError,match='Unseen player'):
        forecast(artifact,features,'not-trained','win_only')
    with pytest.raises(ValueError,match='context'):
        forecast(artifact,features,'a','hinted')
    with pytest.raises(ValueError,match='finite'):
        forecast(artifact,[dict(features={'x':float('nan')})],'a','win_only')
