import json
import pytest
import uuid

from benchmark.v3_ma.recover import Replay


def test_recovery_replays_exact_request_and_calls_live_only_after_prefix(tmp_path):
    messages = [dict(role='user', content='original observation')]
    (tmp_path/'old.json').write_text(json.dumps(dict(request=dict(messages=messages))))
    class Live:
        def generate(self, request, **kwargs):
            assert request == [dict(role='user', content='next observation')]
            return '[catch: 6]', {'call_id': 'new'}
    saved = [dict(reply='[catch: 2]', metadata={'call_id': 'old'})]
    client = Replay(saved, tmp_path, Live())
    assert client.generate(messages) == ('[catch: 2]', {'call_id': 'old'})
    assert client.replayed == 1
    assert client.generate([dict(role='user', content='next observation')])[0] == '[catch: 6]'
    client = Replay(saved, tmp_path, Live())
    with pytest.raises(RuntimeError, match='differs from saved prefix'):
        client.generate([dict(role='user', content='changed observation')])
    assert client.replayed == 0


def test_full_episode_recovery_preserves_every_pre_failure_choice(tmp_path):
    from benchmark.v3_ma.run import execute
    from benchmark.v3_ma.recover import recover_episode
    from bots_v3_ma import Scripted, observation
    counts = {'calls': 0, 'fail': True}
    class Client:
        def __init__(self, config, calls):
            self.calls = calls
            calls.mkdir(exist_ok=True)
        def generate(self, messages, **kwargs):
            counts['calls'] += 1
            if counts['fail'] and counts['calls'] == 5:
                raise RuntimeError('test transport failure')
            pid = observation(messages[-1]['content'])['seat']
            reply = Scripted()(pid, 'move', messages[-1]['content'])
            ident = uuid.uuid4().hex
            (self.calls/(ident+'.json')).write_text(json.dumps(dict(request=dict(messages=messages))))
            return reply, {'call_id': ident}
    task = dict(id='test', game='v3ma_commons_abundant', focal='a', opponent='a', seed=0,
                arm='hole', condition='ordinary')
    execute(task, tmp_path, {'a': None}, 8192, Client, repair_invalid=1)
    path = tmp_path/'episodes/test/trace.json'
    old = json.loads(path.read_text())
    assert old['status'] == 'failed' and len(old['decisions']) == 4
    counts.update(calls=0, fail=False)
    assert recover_episode(task, tmp_path, {'a': None}, Client, '', 1) == 'complete'
    new = json.loads(path.read_text())
    assert new['decisions'][:4] == old['decisions']
    assert counts['calls'] == 8 and new['recovery']['replayed_decisions'] == 4
    assert new['episode']['scores'] == {'0': 8.0, '1': 8.0, '2': 8.0}
