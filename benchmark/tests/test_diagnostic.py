import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from benchmark.diagnostic_runner import run_chain
from benchmark.diagnostic_games import GAMES, evaluate, source_fingerprints
from benchmark.diagnostic_prompts import CONDITIONS, intervention
from benchmark.diagnostic_report import build_report


class FakeClient:
    calls = []
    fail_at = None

    def __init__(self, config, folder):
        pass

    def generate(self, messages, *, purpose, **kwargs):
        if self.fail_at == len(self.calls):
            raise RuntimeError('interrupted')
        self.calls.append((purpose, messages.copy()))
        if purpose == 'play':
            raw = '[work: 1]'
        else:
            raw = json.dumps({'discoveries': [], 'strategy': 'work', 'next_test': {
                'hypothesis': 'early build', 'trigger': 'first turn', 'steps': ['[build: workshop]'],
                'if_enforced': 'rejected', 'if_not_enforced': 'accepted'}})
        return raw, {'call_id': str(len(self.calls))}


@pytest.mark.parametrize('condition', CONDITIONS)
def test_resume_and_condition_memory(tmp_path, condition):
    FakeClient.calls = []
    FakeClient.fail_at = 2
    args = SimpleNamespace(iterations=2, seed=907, play_max_tokens=100, reflection_max_tokens=100)
    with pytest.raises(RuntimeError, match='interrupted'):
        run_chain('gpt-5', 'ref_exchange', condition, args, tmp_path, FakeClient)
    FakeClient.fail_at = None
    run_chain('gpt-5', 'ref_exchange', condition, args, tmp_path, FakeClient)
    assert len(FakeClient.calls) == 14  # 12 moves + 2 reflections, no replay API calls
    traces = [json.loads(p.read_text()) for p in sorted(tmp_path.glob('*/*/traces/*.json'))]
    assert traces[0]['playbook_before'] == ''
    assert json.loads(traces[1]['playbook_before']) == traces[0]['playbook_after']
    assert bool(traces[0]['intervention']) == (condition == 'informed')
    assert bool(traces[1]['intervention']) == (condition != 'ordinary')
    run_chain('gpt-5', 'ref_exchange', condition, args, tmp_path, FakeClient)
    assert len(FakeClient.calls) == 14
    (tmp_path/'config.json').write_text(json.dumps({'args': {'models':['gpt-5'], 'games':['ref_exchange'], 'iterations':2}}))
    build_report(tmp_path, plots=(condition == 'ordinary'))
    assert (tmp_path/'curves.csv').exists()


def test_hanabi_version_and_new_information():
    game = GAMES['ref_hanabi']
    assert game.ROUNDS == 6 and game.ENGINE_VERSION == 'hanabi-human-2.0'
    events = game.run(lambda *args: '[review: 0]', 9070201, 'hole').extras['events']
    result = next(r for r in evaluate('ref_hanabi', events) if 'meta_rule' in r['exploit_id'])
    assert result['execution_count'] == 1  # repeated identical reviews add no information
    assert 'hole_exp/hackable_games/engines_hanabi_human.py' in source_fingerprints()
    assert intervention('ordinary', 'ref_hanabi', '') == ''


def test_no_reflection_fresh_context_resume_and_report(tmp_path):
    FakeClient.calls = []
    FakeClient.fail_at = 2
    args = SimpleNamespace(iterations=2, seed=907, play_max_tokens=100, reflection_max_tokens=100)
    with pytest.raises(RuntimeError):
        run_chain('gpt-5', 'ref_exchange', 'no_reflection', args, tmp_path, FakeClient)
    FakeClient.fail_at = None
    run_chain('gpt-5', 'ref_exchange', 'no_reflection', args, tmp_path, FakeClient)
    run_chain('gpt-5', 'ref_exchange', 'no_reflection', args, tmp_path, FakeClient)
    assert len(FakeClient.calls) == 12
    assert all(purpose == 'play' for purpose, _ in FakeClient.calls)
    assert FakeClient.calls[0][1] == FakeClient.calls[6][1]  # identical fresh opening
    traces = [json.loads(p.read_text()) for p in tmp_path.glob('*/*/traces/*.json')]
    assert all(t['playbook_before'] == '' and t['playbook_after'] is None for t in traces)
    assert all('reflection' not in t and 'reflection_prompt' not in t for t in traces)
    (tmp_path/'config.json').write_text(json.dumps({'conditions':['no_reflection'], 'args': {'models':['gpt-5'], 'games':['ref_exchange'], 'iterations':2}}))
    result = build_report(tmp_path, plots=True)
    assert result['reflected_games'] == 0
    assert result['expected_games'] == result['engine_games'] == 2


def test_matched_comparison_current_and_cumulative(tmp_path):
    from benchmark.reflection_comparison import compare
    config={'args':{'models':['gpt-5'],'games':['ref_exchange'],'iterations':2,'seed':907,'play_max_tokens':100},
            'model_configs':{},'hanabi_profile':{},'source_fingerprints':{}}
    for name,condition in [('old','ordinary'),('new','no_reflection')]:
        d=tmp_path/name;d.mkdir();(d/'config.json').write_text(json.dumps(config))
        for i in (1,2):
            t=dict(model_id='gpt-5',game_id='ref_exchange',condition=condition,iteration=i,seed=907+i,
                   engine_version='test',episode={'scores':{'0':5 if condition=='ordinary' else 3}},
                   execution=[dict(exploit_id='one',attempted=True,executed=i==1,successful=i==1)])
            path=d/condition/'gpt-5'/'traces'/f'{i}.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(t))
    dest=tmp_path/'comparison'
    assert compare(tmp_path/'old',tmp_path/'new',dest,plots=True)==4
    s=json.loads((dest/'summary.json').read_text())['episodes_2_onward'][0]
    assert s['matched_pairs']==1 and s['score_mean_delta']==2 and s['executed_mean_delta']==0
    assert (dest/'current/curves_executed.png').exists()
    assert (dest/'cumulative/curves_executed.png').exists()
