"""Checks for leakage boundaries, missingness, and serialized prediction artifacts."""
from copy import deepcopy
import json
import pickle

from prediction.general_games.evaluation.checks import OUT,TARGETS,read_json,supported,descriptor,examples,prompt,numeric_features


def test_query_outcomes_cannot_change_features_or_prompt():
    records=read_json(OUT/'records.evaluator.json');manifest=read_json(OUT/'manifest.json')
    lookup={r['episode_id']:r for r in records}
    for suite,ids in manifest['suites'].items():
        pool=[lookup[i] for i in ids['train']]
        for ident in ids['test']:
            row=lookup[ident];changed=deepcopy(row)
            changed['targets']={key:None for key in TARGETS}
            changed['labels']={'arbitrary_future_outcome':'must not enter input'}
            selected=examples(row,pool)
            assert examples(changed,pool)==selected
            for method in ('zero_full','few_full','few_structured','few_engine_facts'):
                assert prompt(row,selected,method)==prompt(changed,selected,method)
            assert supported(row)==supported(changed)
            assert numeric_features(row)==numeric_features(changed)


def test_grouped_holdouts_and_supported_rates():
    rows={r['episode_id']:r for r in read_json(OUT/'records.evaluator.json')};m=read_json(OUT/'manifest.json')
    for suite,ids in m['suites'].items():
        assert len(ids['test'])==24
        assert not {rows[i]['groups']['opening_group'] for i in ids['train']} & {rows[i]['groups']['opening_group'] for i in ids['test']}
    train=m['suites']['family']['train'];test=m['suites']['family']['test']
    assert not {rows[i]['inputs']['family_id'] for i in train} & {rows[i]['inputs']['family_id'] for i in test}
    for r in rows.values():
        for target,value in r['targets'].items():
            if target not in supported(r):assert value is None
    for t in m['tasks']:
        assert set(t['example_ids'])<=set(m['suites'][t['suite']]['train'])
        assert t['episode_id'] not in t['example_ids']


def test_serialized_learned_models_reproduce_all_predictions():
    from prediction import modeling  # Reuse installed sklearn path.
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from threadpoolctl import threadpool_limits
    rows={r['episode_id']:r for r in read_json(OUT/'records.evaluator.json')};m=read_json(OUT/'manifest.json')
    predictions={(p['suite'],p['method'],p['episode_id']):p['forecast'] for p in read_json(OUT/'numeric-predictions.json')}
    with (OUT/'learned-models.pkl').open('rb') as f:artifacts=pickle.load(f)
    count=0
    with threadpool_limits(limits=1):
        for (suite,rep,method),a in artifacts.items():
            test=[rows[i] for i in m['suites'][suite]['test']]
            x=a['scaler'].transform(a['vectorizer'].transform([numeric_features(r) for r in test]))
            if a['text_encoder'] is not None:
                tx=a['text_encoder'].transform(json.dumps(descriptor(r,'full'),sort_keys=True) for r in test).toarray()
                x=np.concatenate([x,tx],axis=1)
            for target in TARGETS:
                model=a['models'][target];est=model['estimator']
                values=([model['constant']]*len(test) if est is None else np.clip(est.predict_proba(x)[:,1] if isinstance(est,LogisticRegression) else est.predict(x),0,1))
                for r,v in zip(test,values):
                    saved=predictions[suite,method+'_'+rep,r['episode_id']][target]
                    if target not in supported(r) or v is None:assert saved is None
                    else:assert abs(saved-v)<1e-10
                    count+=1
            assert not any(k.endswith('_warnings') for k in a['models'])
    assert count==960
