"""Check viewer projections against the frozen screen, including its failures."""
import importlib.util
from pathlib import Path

path = Path(__file__).with_name('server.py')
spec = importlib.util.spec_from_file_location('ma_trace_server', path)
viewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(viewer)


def test_all_ma_episodes_and_model_provenance():
    report = viewer.read(viewer.MA_ROOT / 'report.json')
    index = viewer.ma.index(viewer.MA_ROOT, viewer.read)
    assert len(index['episodes']) == 768
    assert sum(e['status'] == 'complete' for e in index['episodes']) == 761
    for row in report['episodes']:
        episode = viewer.episode(viewer.ma.RUN_ID, row['id'])
        trace = viewer.read(viewer.MA_ROOT / 'episodes' / row['id'] / 'trace.json')
        decisions = [d for r in episode['rounds'] for s in r['stages'] for d in s['decisions']]
        assert [(d['pid'], d['actual_model'], d['reply']) for d in decisions] == [
            (d['pid'], d['metadata']['actual_model'], d['reply']) for d in trace['decisions']]
        if row['status'] == 'complete':
            assert episode['marker'] == row['marker']
            assert sum(a['round_hit'] for r in episode['rounds'] for a in r['annotations']) == row['marker']['hit_rounds']
            assert episode['final_scores'] == episode['rounds'][-1]['scores']
        else:
            assert episode['marker'] is None and episode['final_scores'] is None
            assert all(not r['scored'] and not r['annotations'] and r['scores'] is None for r in episode['rounds'])


def test_explicit_pledge_and_note_evidence():
    pledge = viewer.episode(viewer.ma.RUN_ID, 'bfdebd98829842f01d4d')
    assert pledge['final_scores'] == [48, -18]
    assert all(r['annotations'][0]['kind'] == 'observed' for r in pledge['rounds'])
    assert all(r['stages'][-1]['annotation'] for r in pledge['rounds'])
    assert all(not s['annotation'] for r in pledge['rounds'] for s in r['stages'][:-1])
    assert pledge['paired_episode']['id'] == '03f615f1e765b779dba9'
    notes = viewer.episode(viewer.ma.RUN_ID, 'f48fdef471f25e4efdfd')
    assert not notes['rounds'][0]['annotations']
    assert all(r['annotations'][0]['kind'] == 'observed' for r in notes['rounds'][1:])
    assert notes['participants'][0]['model_name'] == 'Qwen 3.8 27B'
    assert notes['participants'][1]['model_name'] == 'GLM 5.3'


def test_limited_patterns_do_not_get_confirmed_exploit_labels():
    report = viewer.read(viewer.MA_ROOT / 'report.json')
    for game, expected in [('v3ma_trust_messages', 'association'), ('v3ma_signal_convention', 'pattern')]:
        row = next(r for r in report['episodes'] if r['game'] == game and r['status'] == 'complete' and r['marker']['hit_rounds'])
        episode = viewer.episode(viewer.ma.RUN_ID, row['id'])
        annotations = [a for r in episode['rounds'] for a in r['annotations'] if a['round_hit']]
        assert annotations and all(a['kind'] == expected for a in annotations)


def test_ma_path_escape_and_unknown_episode():
    import pytest
    for eid in ('../../plan.json', '/etc/passwd', '..', 'unknown'):
        with pytest.raises(KeyError):
            viewer.episode(viewer.ma.RUN_ID, eid)
