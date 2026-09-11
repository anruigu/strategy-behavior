from collections import Counter
from dataclasses import asdict
import json
import pytest
from benchmark.crossplay_runner import schedule,family,run_match,REGISTRY
from benchmark.crossplay_games import make_game,execution
from benchmark.clients import write_json
from benchmark.crossplay_report import build_report


def test_schedule_unique_families_and_balanced_seats():
    tasks=schedule()
    assert len(tasks)==144 and len({t['id'] for t in tasks})==144
    for t in tasks:assert len({family(m) for m in t['seats']})==len(t['seats'])
    for g in {t['game_id'] for t in tasks}:
        assert sum(t['game_id']==g for t in tasks)==48
        for m in REGISTRY:
            counts=Counter(t['seats'].index(m) for t in tasks if t['game_id']==g and m in t['seats'])
            assert len(set(counts.values()))==1


class Fake:
    calls=[]
    fail_at=None
    def __init__(self,config,folder):self.pid=int(folder.name[-1])
    def generate(self,messages,**kwargs):
        assert kwargs['purpose']=='play'
        if len(self.calls)==self.fail_at:raise RuntimeError('interrupted')
        self.calls.append((self.pid,[dict(m) for m in messages]))
        obs=messages[-1]['content']
        raw='PRIVATE_ZERO [move: cooperate]' if self.pid==0 else 'PRIVATE_ONE [move: defect]'
        if 'settler' in obs:raw='[build: none]' if 'building phase' in obs else '[accept: none]' if 'Offers posted' in obs else '[offer: none]'
        if 'Your hand' in obs:raw='[discard: 1]'
        return raw,dict(call_id=str(len(self.calls)))


@pytest.mark.parametrize('game',['ta_ipd_live','ref_exchange_live','ref_hanabi_live'])
def test_checkpoint_private_histories_and_report(tmp_path,game):
    task=next(t for t in schedule() if t['game_id']==game)
    Fake.calls=[];Fake.fail_at=1
    with pytest.raises(RuntimeError):run_match(task,tmp_path,client_factory=Fake)
    Fake.fail_at=None
    run_match(task,tmp_path,client_factory=Fake)
    calls=len(Fake.calls);run_match(task,tmp_path,client_factory=Fake);assert len(Fake.calls)==calls
    trace=json.loads((tmp_path/'traces'/(task['id']+'.json')).read_text())
    assert len(trace['turns'])==calls
    for pid in range(len(task['seats'])):
        own=[t for t in trace['turns'] if t['pid']==pid]
        histories=[msgs for p,msgs in Fake.calls if p==pid]
        assert len(histories[0])==2
        assert [m['content'] for m in histories[-1] if m['role']=='assistant']==[t['reply'] for t in own[:-1]]
    if game=='ta_ipd_live':
        assert trace['episode']['scores']=={'0':0.,'1':20.}
        # Player 1's first prompt cannot see Player 0's submitted current move.
        assert trace['turns'][0]['reply'] not in trace['turns'][1]['prompt']
    if not trace['cooperative']:assert sum(r['win_credit'] for r in trace['seats_results'])==1
    else:assert all(r['win_credit'] is None for r in trace['seats_results'])
    write_json(tmp_path/'config.json',dict(tasks=[task],model_configs={m:asdict(REGISTRY[m]) for m in task['seats']}))
    result=build_report(tmp_path,plots=(game=='ta_ipd_live'))
    assert result['complete']==1 and result['seat_observations']==len(task['seats'])


def test_negative_offer_must_be_accepted_to_execute():
    ep={'violations':{0:{'negative_quantity':1}}}
    offer=dict(pid=0,phase='offer',reply='[offer: to P1, give -2 wood, get 1 brick]')
    row=execution('ref_exchange_live',ep,[offer],0)[0]
    assert row['attempted'] and not row['executed']
    row=execution('ref_exchange_live',ep,[offer,dict(pid=1,phase='accept',reply='[accept: P0]')],0)[0]
    assert row['executed']


def test_discovery_uses_own_quotes_and_blinds_model_metadata(tmp_path):
    from benchmark.crossplay_discovery import score
    task=next(t for t in schedule() if t['game_id']=='ta_ipd_live')
    Fake.calls=[];Fake.fail_at=None;run_match(task,tmp_path,client_factory=Fake)
    path=tmp_path/'traces'/(task['id']+'.json')
    class Judge:
        def __init__(self,*args):pass
        def generate(self,messages,**kwargs):
            evidence=json.loads(messages[1]['content'])
            assert 'PRIVATE_ZERO' in evidence['model_articulation']
            assert 'PRIVATE_ONE' not in evidence['model_articulation']
            assert all(m not in messages[1]['content'] for m in REGISTRY)
            return json.dumps({'judgments':[dict(exploit_id=s['exploit_id'],discovered=False,correct_hypothesis=False,quote='',reason='No articulation') for s in evidence['specifications']]}),{}
    score(path,tmp_path,0,Judge)
    assert (tmp_path/'discovery'/(path.stem+'__seat0.json')).exists()
    class BadJudge(Judge):
        def generate(self,messages,**kwargs):
            evidence=json.loads(messages[1]['content'])
            return json.dumps({'judgments':[dict(exploit_id=s['exploit_id'],discovered=True,correct_hypothesis=True,quote='PRIVATE_ONE',reason='Opponent text') for s in evidence['specifications']]}),{}
    # A separate seat-0 artifact target cannot accept another seat's response.
    (tmp_path/'discovery'/(path.stem+'__seat0.json')).unlink()
    with pytest.raises(ValueError,match='Invalid judge'):score(path,tmp_path,0,BadJudge)
