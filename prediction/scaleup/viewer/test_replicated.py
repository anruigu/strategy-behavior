"""Count/provenance contracts for the expanded native-game viewer."""
import json,threading
from urllib.error import HTTPError
from urllib.request import urlopen
import pytest
from .replicated import ReplicatedDataset
from .server import handler_for,ThreadingHTTPServer


@pytest.fixture(scope='module')
def data():return ReplicatedDataset()


def test_design_counts_stay_separate_from_repeated_observations(data):
    s=data.summary({'cohort':['training']})
    assert s['counts']['families']==16 and s['counts']['configurations']==57
    assert s['counts']['seeded_instances']==114 and s['counts']['distinct_openings']==85
    assert s['counts']['episodes']==320 and s['counts']['actions']==1397
    assert sum(f['new'] for f in s['families'])==4 and sum(f['episodes']>0 for f in s['families'])==4
    old=data.summary({'cohort':['legacy']});assert old['counts']['episodes']==144 and old['counts']['actions']==779


def test_native_trace_and_label_provenance(data):
    s=data.summary({'cohort':['training'],'family':['blind_auction']})
    assert s['counts']['episodes']==80 and s['counts']['families']==1
    assert s['counts']['configurations']==len(s['catalog'])
    g=next(g for g in s['catalog'] if g['episodes']);detail=data.game(g['configuration_id'])
    assert 'Zero is invalid' in detail['mechanics']['transitions_and_payoffs']
    e=next(e for e in detail['episodes'] if e['source_run']=='v2-training');trace=data.episode(e['episode_id'])
    assert trace['measurements']['episode_id']==e['episode_id']
    assert any(t['is_focal'] and t['messages'] for t in trace['steps'])
    assert 'attempts' not in trace and 'models' not in trace and 'call' not in trace['steps'][0]


def test_http_routes_allowlist_artifacts(data):
    server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(None,replicated=data));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    try:
        with urlopen(base+'/api/general/replicated/summary?cohort=training') as r:assert json.load(r)['counts']['episodes']==320
        with urlopen(base+'/general/replicated') as r:assert 'Room to learn' in r.read().decode()
        for path in ('/api/general/replicated/episode?id=../../.env','/api/general/replicated/game?id=unknown','/general/replicated/raw_calls','/general/replicated/plan.json'):
            with pytest.raises(HTTPError) as e:urlopen(base+path)
            assert e.value.code==404
    finally:server.shutdown();server.server_close();thread.join(timeout=2)
