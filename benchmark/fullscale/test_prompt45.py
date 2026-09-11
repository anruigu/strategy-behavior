"""Regression checks for prompt isolation, same-round retries and provenance."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location('prompt45_under_test', Path(__file__).with_name('prompt45.py'))
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

class RetryGame:
    NAME = 'retry_game'
    def initial(self, seed):
        return dict(round=1, done=False, scores=[0], feedback='start', secret='DO_NOT_EXPOSE')
    def observe(self, state):
        return state['feedback']
    def transition(self, state, action):
        if state['feedback'] == 'start':
            return {**state, 'feedback': 'Invalid clue; choose again'}, {'valid': False}
        return {**state, 'round': 2, 'done': True, 'scores': [1]}, {'valid': True}

class FakeClient:
    calls = []
    def __init__(self, *args):
        pass
    def generate(self, messages):
        self.calls.append(deepcopy(messages))
        return 'action', dict(status='ok', call_id='test')


def test_prompt_only_removes_exploration():
    win, explore = p.PLAN['conditions'].values()
    assert win.startswith('Your primary objective is to win this game:')
    assert explore.replace(explore[explore.index('Actively explore'):explore.index('Other seats')], '') == win
    assert 'Actively explore' not in win and 'mechanism is explicitly revealed' not in win


def test_rejected_clue_gets_a_new_checkpoint_on_same_round(tmp_path, monkeypatch):
    FakeClient.calls = []
    monkeypatch.setattr(p, 'Client', FakeClient)
    monkeypatch.setattr(p, 'score_actions', lambda *args, **kwargs: [])
    config = p.ModelConfig(**p.PLAN['models']['glm']['config'])
    trace = p.episode(RetryGame(), 19, 'win_only', tmp_path, config, None)
    assert len(trace['turns']) == 2 and [t['round'] for t in trace['turns']] == [1, 1]
    assert (tmp_path/'decision-01.json').exists() and (tmp_path/'decision-02.json').exists()
    assert 'DO_NOT_EXPOSE' not in str(FakeClient.calls)
    assert FakeClient.calls[1][-1]['content'] == 'Invalid clue; choose again'
    # Resume all checkpoints without a new call, including repeated round numbers.
    (tmp_path/'trace.json').unlink()
    assert p.episode(RetryGame(), 19, 'win_only', tmp_path, config, None)['scores'] == []
    assert len(FakeClient.calls) == 2
    with pytest.raises(AssertionError, match='identity'):
        p.episode(RetryGame(), 19, 'exploration', tmp_path, config, None)


def test_changed_history_cannot_reuse_checkpoint(tmp_path, monkeypatch):
    monkeypatch.setattr(p, 'Client', FakeClient)
    monkeypatch.setattr(p, 'score_actions', lambda *args, **kwargs: [])
    config = p.ModelConfig(**p.PLAN['models']['glm']['config'])
    p.episode(RetryGame(), 19, 'win_only', tmp_path, config, None)
    (tmp_path/'trace.json').unlink()
    with pytest.raises(AssertionError, match='Resume context mismatch'):
        p.episode(RetryGame(), 19, 'exploration', tmp_path, config, None)


def test_plot_pairs_identical_cases_and_distinguishes_missing_from_zero():
    plot_spec = importlib.util.spec_from_file_location('plot_prompt45_under_test', Path(__file__).with_name('plot_prompt45.py'))
    plot = importlib.util.module_from_spec(plot_spec)
    plot_spec.loader.exec_module(plot)
    def trace(hit):
        return {'scores':[dict(exploit_id='a.meta_rule',category='meta_rule',executed=hit)]}
    result=plot.aggregate({'win_only':{'same':trace(False),'win_only_extra':trace(True)},
                           'exploration':{'same':trace(True),'explore_extra':trace(False)}},{'a.meta_rule'})
    assert result['paired_episodes']==1
    assert result['win_only']['paired']['n']==1 and result['win_only']['paired']['rate']==0
    assert result['exploration']['paired']['rate']==1
    assert plot.summarize([])['rate'] is None
