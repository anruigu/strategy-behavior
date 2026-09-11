from copy import deepcopy
import json

from benchmark.v3_ma.dose_run import execute, schedule
from benchmark.v3_ma.extension_recovery import recover_dose


def test_dose_recovery_replays_saved_reply_without_resampling(tmp_path):
    sequence = iter(range(3))
    class First:
        def __init__(self, config, calls):
            self.pid = next(sequence)
            self.calls = calls
        def generate(self, messages, **kwargs):
            if self.pid == 1:
                raise RuntimeError('transport failure')
            self.calls.mkdir(parents=True, exist_ok=True)
            (self.calls/'saved.json').write_text(json.dumps({'request': {'messages': messages}}))
            return '[catch: 1]', {'call_id': 'saved'}
    task = next(r for r in schedule() if r['dose']['family'] == 'commons')
    execute(task, tmp_path, First)
    path = tmp_path/'episodes'/task['id']/'trace.json'
    old = json.loads(path.read_text())
    assert old['status'] == 'failed' and len(old['decisions']) == 1
    calls = []
    class Live:
        def __init__(self, config, directory):
            pass
        def generate(self, messages, **kwargs):
            calls.append(deepcopy(messages))
            return '[catch: 2]', {'call_id': 'live'}
    assert recover_dose(task, tmp_path, Live) == 'complete'
    new = json.loads(path.read_text())
    assert len(calls) == 11  # 12 game actions minus the exact saved first reply.
    assert new['decisions'][0] == old['decisions'][0]
    assert new['episode']['scores']['0'] == 7
    assert new['recovery']['replayed_decisions'] == 1
    assert json.loads((path.parent/'previous-attempts/first-pass.json').read_text()) == old
