import importlib.util
from pathlib import Path
p=Path(__file__).with_name('server.py');s=importlib.util.spec_from_file_location('trace_server',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)

def test_gemini_index_and_rollouts():
    run=next(r for r in v.index()['runs'] if r['id']=='gemini-original')
    blind=[e for e in run['episodes'] if e['condition']=='blind']
    assert len(blind)==57
    for game in {e['game'] for e in blind}:assert {e['seed'] for e in blind if e['game']==game}=={19,73,101}

def test_all_gemini_annotations_agree_with_frozen_scores():
    for p in v.REFERENCE.glob('episodes/*/trace.json'):
        t=v.episode('gemini-original',p.parent.name)
        for hole in t['holes']:
            turns=[x['round'] for x in t['turns'] for a in x['annotations'] if a['id']==hole['id'] and a['kind']=='executed']
            assert bool(turns)==hole['executed']
            assert min(turns,default=None)==hole['first_execution_turn']

def test_no_path_escape():
    import pytest
    with pytest.raises(KeyError):v.episode('gemini-original','../../manifest.json')
    with pytest.raises(KeyError):v.episode('unknown','anything')
