from copy import deepcopy
import json

from bots_v3_ma import Scripted, observation
from benchmark.v3_ma import run


def test_live_dispatch_isolates_seat_histories_and_preserves_traces(monkeypatch, tmp_path):
    clients = []
    class FakeClient:
        def __init__(self, config, log_dir):
            self.requests = []
            clients.append(self)
        def generate(self, messages, **kwargs):
            self.requests.append(deepcopy(messages))
            prompt = messages[-1]['content']
            pid = observation(prompt)['seat']
            for m in messages:
                if m['role'] == 'user':
                    assert observation(m['content'])['seat'] == pid
            return Scripted({0: 'exploit', 1: 'nerfed'})(pid, 'move', prompt), {'actual_model': 'test'}
    monkeypatch.setattr(run, 'ModelClient', FakeClient)
    task = dict(id='test', game='v3ma_trust_memory', focal='a', opponent='b', seed=0, arm='hole', condition='nerfed')
    run.execute(task, tmp_path, {'a': None, 'b': None}, 1024)
    trace = json.loads((tmp_path/'episodes/test/trace.json').read_text())
    assert trace['status'] == 'complete'
    assert len(clients) == 2
    assert clients[0].requests[0][0] != clients[1].requests[0][0]
    assert len(trace['decisions']) == 24
    run.execute(task, tmp_path, {'a': None, 'b': None}, 1024)
    assert len(clients) == 2  # Completed episodes are never sampled again.


def test_failure_is_explicit_and_previous_attempt_is_preserved(monkeypatch, tmp_path):
    class FailingClient:
        def __init__(self, *args):
            pass
        def generate(self, *args, **kwargs):
            raise RuntimeError('test transport failure')
    monkeypatch.setattr(run, 'ModelClient', FailingClient)
    task = dict(id='failed', game='v3ma_commons_collapse', focal='a', opponent='a', seed=0, arm='hole', condition='ordinary')
    run.execute(task, tmp_path, {'a': None}, 1024)
    path = tmp_path/'episodes/failed/trace.json'
    first = path.read_text()
    assert json.loads(first)['status'] == 'failed'
    assert 'episode' not in json.loads(first)
    run.execute(task, tmp_path, {'a': None}, 1024)
    assert (tmp_path/'episodes/failed/previous-attempts/0001.json').read_text() == first


def test_one_neutral_format_correction_keeps_invalid_reply(tmp_path):
    class Client:
        def __init__(self, *args):
            self.first = True
        def generate(self, messages, **kwargs):
            if self.first:
                self.first = False
                return '[catch: 2] [choice: C]', {}
            return '[catch: 2]', {}
    task = dict(id='repair', game='v3ma_commons_abundant', focal='a', opponent='a', seed=0,
                arm='hole', condition='ordinary')
    run.execute(task, tmp_path, {'a': None}, 1024, Client, repair_invalid=1)
    trace = json.loads((tmp_path/'episodes/repair/trace.json').read_text())
    assert trace['status'] == 'complete'
    assert sum(bool(d['format_error']) for d in trace['decisions']) == 3
    assert len(trace['decisions']) == 15
    assert trace['episode']['scores'] == {'0': 8.0, '1': 8.0, '2': 8.0}
