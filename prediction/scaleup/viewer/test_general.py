import threading
from urllib.error import HTTPError
from urllib.request import urlopen
import json
import pytest

from .general import GeneralDataset
from .server import handler_for, ThreadingHTTPServer


@pytest.fixture(scope='module')
def general():
    return GeneralDataset()


def test_counting_units_and_masks(general):
    s=general.summary()
    assert s['counts']==dict(families=12,configurations=49,instances=196,distinct_openings=113,episodes=96,actions=477,invalid_actions=18)
    assert sum(f['configurations'] for f in s['families'])==49
    assert sum(f['episodes'] for f in s['families'])==96
    assert sum(r['count'] for r in s['episode_lengths'])==96
    assert sum(r['episodes'] for r in s['outcomes'] if r['players']==1)==24
    assert sum(r['episodes'] for r in s['outcomes'] if r['players']==2)==72
    pd=next(m for m in s['measurements'] if m['label'].startswith('Cooperation'))
    assert pd['denominator']==24  # Excludes the 24 conversation turns.
    assert [sum(p['counts'].values()) for p in s['partitions']]==[12,49,113]


def test_filters_separate_catalog_and_live_coverage(general):
    s=general.summary(dict(model=['glm'],prompt=['normal']))
    assert s['counts']['episodes']==24 and s['counts']['configurations']==49
    single=general.summary(dict(players=['1']))
    assert single['counts']['families']==3 and single['counts']['episodes']==24
    family=general.summary(dict(family=['connect_four']))
    assert family['counts']['configurations']==3 and family['counts']['episodes']==8
    variant=next(g for g in family['catalog'] if g['axis'])
    detail=general.game(variant['id'])
    assert not detail['episodes'] and len(detail['seeds'])==4
    assert 'Connect Four' in json.dumps(detail['example'])


def test_parameter_cohort_and_fixed_validation_results(general):
    sweep=general.summary(dict(cohort=['parameter-check-20260910']))
    assert sweep['counts']['episodes']==48 and sweep['counts']['actions']==302
    assert sweep['counts']['invalid_actions']==0
    assert sum(g['episodes']>0 for g in sweep['catalog'])==6
    all_data=general.summary(dict(cohort=['all']))
    assert all_data['counts']['episodes']==144 and all_data['counts']['actions']==779
    game=general.game(next(g['id'] for g in sweep['catalog'] if g['episodes']))
    ep=next(e for e in game['episodes'] if e['source_run']=='parameter-check-20260910')
    trace=general.episode(ep['id'])
    assert trace['status']=='complete' and trace['steps']
    checks=general.checks()
    assert checks['audit']['complete_predictions']==192
    assert len(checks['verdicts'])==5


def test_http_general_routes_and_trace_provenance(general):
    server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(None,general))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    url=f'http://127.0.0.1:{server.server_port}'
    try:
        with urlopen(url+'/api/general/summary') as response:
            assert json.load(response)['counts']['episodes']==96
        ident=general.episodes[0]['episode_id']
        with urlopen(url+'/api/general/episode?id='+ident) as response:
            trace=json.load(response)
            assert trace['id']==ident and trace['status']=='complete'
            assert any(s['is_focal'] and s['messages'] for s in trace['steps'])
            assert 'attempts' not in trace and 'config' not in trace
        for path in ['/api/general/episode?id=../../.env','/general/raw_calls','/general/plan.json','/api/general/game?id=unknown']:
            with pytest.raises(HTTPError) as error: urlopen(url+path)
            assert error.value.code==404
    finally:
        server.shutdown();server.server_close();thread.join(timeout=2)
