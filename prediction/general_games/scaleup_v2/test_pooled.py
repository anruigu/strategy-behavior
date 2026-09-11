from prediction.io_utils import read_json,digest
from .predict import OUT,retrieve
from .pooled_fewshot import pool_visible,FOLDER
from .labels import TARGETS


def test_pooling_preserves_all_observation_counts_and_means():
    groups=read_json(OUT/'n440/groups.evaluator.json');pool=pool_visible(groups)
    assert len(groups)==184 and len(pool)==124 and sum(r['n'] for r in pool)==440
    for p in pool:
        selected=[g for g in groups if digest(g['inputs'])==digest(p['inputs'])]
        assert p['id']==min(g['id'] for g in selected)
        for t in TARGETS:
            n=sum(g['target_counts'][t] for g in selected)
            assert p['target_counts'][t]==n
            if n:assert abs(p['targets'][t]*n-sum(g['targets'][t]*g['target_counts'][t] for g in selected if g['targets'][t] is not None))<1e-10
            else:assert p['targets'][t] is None


def test_secondary_control_keeps_original_examples_and_declares_timing():
    original=read_json(OUT/'n440/manifest.json');m=read_json(FOLDER/'manifest.json')
    groups=read_json(OUT/'n440/groups.evaluator.json');pool=read_json(FOLDER/'groups.evaluator.json')
    assert m['created']>read_json(OUT/'frozen.json')['frozen_at']
    assert 'after test play began' in m['timing']
    for q in m['queries']:
        assert retrieve(q,groups,16)[0]['id']==retrieve(q,pool,16)[0]['id']
        for n in (4,8,16):assert [r['id'] for r in retrieve(q,groups,n)]==[r['id'] for r in retrieve(q,pool,n)]
    assert [b['example_ids'] for b in m['batches']]==[b['example_ids'] for b in original['batches'] if b['kind']=='test']
