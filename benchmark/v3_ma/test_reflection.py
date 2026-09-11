from copy import deepcopy
import json
import pytest

from benchmark.v3_ma import reflection as r
from bots_v3_ma import Scripted, observation


def task():
    return dict(id='test-memory', game='v3ma_trust_memory', focal='focal', opponent='opponent',
        condition='nerfed', arm='hole', seed=0, iteration=2, learning_arm='reflection', baseline_id='base')

def fake_factory(requests, fail_at=None):
    class Client:
        def __init__(self, config, path):
            self.config = config
        def generate(self, messages, **kwargs):
            if fail_at and len(requests) + 1 == fail_at:
                raise RuntimeError('Simulated transport failure')
            requests.append(dict(config=self.config, messages=deepcopy(messages), purpose=kwargs.get('purpose')))
            if kwargs.get('purpose') == 'ma_private_reflection':
                return 'PRIVATE_NOTE_TEST', dict(actual_model=self.config, call_id='note')
            prompt = messages[-1]['content']
            pid = observation(prompt)['seat']
            return Scripted({0:'exploit',1:'nerfed'})(pid, 'move', prompt), dict(actual_model=self.config, call_id=str(len(requests)))
    return Client


def test_private_reflection_and_memory_stay_with_focal(tmp_path):
    requests = []
    factory = fake_factory(requests)
    public = [dict(role='user', content='OWN_PREVIOUS_OBSERVATION'), dict(role='assistant', content='OWN_PREVIOUS_ACTION')]
    note = r.reflect(tmp_path/'note', public, 'focal', factory)
    memory = public + [dict(role='user', content=note['request']), dict(role='assistant', content=note['reply'])]
    result = r.play(task(), tmp_path, {'focal':'focal','opponent':'opponent'}, memory, [note], factory)
    assert result['status'] == 'complete'
    for request in requests:
        text = json.dumps(request['messages'])
        if request['config'] == 'opponent':
            assert 'PRIVATE_NOTE_TEST' not in text and 'OWN_PREVIOUS_OBSERVATION' not in text
        elif request['purpose'] != 'ma_private_reflection':
            assert 'PRIVATE_NOTE_TEST' in text and 'OWN_PREVIOUS_OBSERVATION' in text
    assert 'PRIVATE_NOTE_TEST' not in json.dumps(result['focal_history'])  # No duplicated incoming history.
    assert 'END COMPLETED PLAY 2' in result['focal_history'][-1]['content']
    assert 'Round 6/6' in result['final_observation']


def test_reflection_checkpoint_reused_and_context_checked(tmp_path):
    calls = []
    factory = fake_factory(calls)
    history = [dict(role='user', content='Only my public observation')]
    first = r.reflect(tmp_path, history, 'focal', factory)
    assert r.reflect(tmp_path, history, 'focal', factory) == first
    assert len(calls) == 1
    with pytest.raises(AssertionError, match='context changed'):
        r.reflect(tmp_path, history + [dict(role='user',content='Changed')], 'focal', factory)


def test_failed_game_replays_saved_choices_without_resampling(tmp_path):
    calls = []
    first = r.play(task(), tmp_path, {'focal':'focal','opponent':'opponent'}, [], [], fake_factory(calls, fail_at=5))
    assert first['status'] == 'failed' and len(first['decisions']) == 4
    resumed_calls = []
    resumed = r.play(task(), tmp_path, {'focal':'focal','opponent':'opponent'}, [], [], fake_factory(resumed_calls))
    assert resumed['status'] == 'complete'
    assert resumed['decisions'][:4] == first['decisions']
    assert len(resumed_calls) == 20
    assert (tmp_path/'episodes/test-memory/previous-attempts/0001.json').exists()
    with pytest.raises(AssertionError, match='memory changed'):
        r.play(task(), tmp_path, {'focal':'focal','opponent':'opponent'}, [dict(role='user',content='Different')], [], fake_factory([]))


def test_reflection_request_does_not_supply_a_mechanism_or_recipient():
    prompt = r.REFLECTION_SYSTEM + r.REFLECTION_REQUEST
    for secret in ('seat 1', 'seat 2', 'nerfed', 'counter', 'pledge', 'rank2', 'hackbook', 'exploit'):
        assert secret not in prompt.lower()


def test_saved_council_final_observation_retains_the_focals_inbox(tmp_path):
    from benchmark.v3_ma.reflection_verify import live_final_observation
    council_task = dict(task(), game='v3ma_trust_messages')
    trace = r.play(council_task, tmp_path, {'focal':'focal','opponent':'opponent'}, [], [], fake_factory([]))
    assert trace['status'] == 'complete'
    saved = json.loads(json.dumps(trace))
    assert live_final_observation(saved) == trace['final_observation']
    last = [d for d in saved['decisions'] if d['pid']==0][-1]
    assert observation(saved['final_observation'])['inbox'] == observation(last['observation'])['inbox']


def test_report_excludes_incomplete_memory_pairs(tmp_path):
    from benchmark.v3_ma.reflection_report import report
    from benchmark.clients import write_json
    # Generate a real engine trace with the existing fake clients so this test
    # remains runnable without the excluded raw campaign data.
    original = r.play(task(), tmp_path/'baseline-fixture',
                      {'focal':'focal','opponent':'opponent'}, [], [], fake_factory([]))
    assert original['status'] == 'complete'
    baseline = dict(original['task'], iteration=1, learning_arm='shared', baseline_id='base', id='base')
    tasks = [baseline]
    for arm in r.ARMS:
        for iteration in (2,3,4):
            tasks.append(dict(baseline, id=arm+str(iteration), iteration=iteration, learning_arm=arm))
    write_json(tmp_path/'plan.json',dict(tasks=tasks,protocol='test',limitations='test'))
    for task_ in tasks:
        trace = deepcopy(original)
        trace['task'] = task_
        if task_['id'] == 'reflection4':
            trace['status'] = 'failed'
            trace.pop('episode')
        write_json(tmp_path/'episodes'/task_['id']/'trace.json',trace)
    result = report(tmp_path)
    pairs = result['paired_reflection']
    assert [p['complete'] for p in pairs] == [True,True,False]
    assert result['outcomes'] == {'complete':6,'failed':1}
    final = next(s for s in result['summaries'] if s['condition']=='nerfed' and s['iteration']==4)
    assert final['complete_pairs'] == 0 and final['mean_score_delta'] is None


def test_discovery_separates_baseline_hits_cumulative_hits_and_missing_pairs():
    from benchmark.v3_ma.reflection_analysis import analyze
    episodes, pairs = [], []
    # Base 1 already succeeded. Base 2 succeeds only under reflection now.
    # Base 3 succeeded earlier in both continuations, but neither succeeds now.
    # Base 4 has a missing control and must not contribute to any estimate.
    for i, initial, complete, control, treatment, ever_c, ever_r in (
        (1, True, True, True, False, True, True),
        (2, False, True, False, True, False, True),
        (3, False, True, False, False, True, True),
        (4, False, False, False, True, False, True),
    ):
        common = dict(game='v3ma_trust_memory', condition='nerfed', baseline_id=str(i))
        episodes.append(dict(common, id=str(i), iteration=1, learning_arm='shared',
                             marker=dict(episode_marker=initial, hit_rounds=int(initial))))
        for arm, marked in (('transcript_only',control), ('reflection',treatment)):
            episodes.append(dict(common, id=str(i)+arm, iteration=4, learning_arm=arm,
                                 marker=dict(episode_marker=marked, hit_rounds=2*int(marked))))
        pairs.append(dict(common, iteration=4, complete=complete, transcript_marker=control,
                          reflection_marker=treatment, transcript_cumulative=ever_c,
                          reflection_cumulative=ever_r))
    result = analyze(dict(updated='test', new_outcomes={}, episodes=episodes, paired_reflection=pairs))
    row = next(r for r in result['discovery'] if r['condition']=='nerfed' and r['iteration']==4)
    assert row['complete_pairs'] == 3 and row['baseline_miss_pairs'] == 2
    assert (row['transcript_new_marker_now'],row['reflection_new_marker_now']) == (0,1)
    assert (row['transcript_new_marker_ever'],row['reflection_new_marker_ever']) == (1,2)
    row = next(r for r in result['final_intensity'] if r['condition']=='nerfed')
    assert row['reflection']['episodes_with_two_hit_rounds'] == 1
    assert row['mean_hit_round_delta'] == 0


def test_council_repeat_audit_requires_a_prior_paid_betrayal_of_that_seat():
    from benchmark.v3_ma.reflection_report import council
    events = []
    for turn, focal_excludes, seat1_excludes in ((1,'1','none'),(2,'none','none'),(3,'none','0'),(4,'none','none')):
        events.append(dict(round=turn, stage='communicate', actions={'0':dict(target='1',message='none')}))
        events.append(dict(round=turn, stage='act', actions={
            '0':dict(move='D',exclude=focal_excludes),
            '1':dict(move='C',exclude=seat1_excludes),
            '2':dict(move='C',exclude='none')}))
    rows = council(dict(episode=dict(extras=dict(events=events))))
    assert [r['profitable_d_c_seats'] for r in rows] == [[2],[1,2],[2],[1,2]]
    assert [r['repeat_profitable_d_c_seats'] for r in rows] == [[],[2],[2],[1,2]]
    assert [r['consecutive_profitable_d_c_seats'] for r in rows] == [[],[2],[2],[2]]
    assert not any(r['request_then_profitable_betrayal'] for r in rows)  # No message request was made.


def test_recovery_changes_only_the_client_timeout(monkeypatch):
    from benchmark.v3_ma.reflection_client import ReflectionClient
    from benchmark.v3_ma.reflection_recovery import RecoveryClient
    seen = []
    class Client:
        def with_options(self, **options):
            seen.append(options)
            return self
    def initialize(self, *args, **kwargs):
        seen.append((args,kwargs))
        self.client = Client()
    monkeypatch.setattr(ReflectionClient,'__init__',initialize)
    RecoveryClient('config','path','ledger','limits')
    assert seen == [(('config','path','ledger','limits'),{}),{'timeout':600}]
    assert RecoveryClient.once is ReflectionClient.once
    assert RecoveryClient.generate is ReflectionClient.generate
