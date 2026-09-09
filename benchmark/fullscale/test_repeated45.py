from copy import deepcopy
from types import SimpleNamespace
import pytest
from benchmark.fullscale import repeated45 as r

class Game:
    NAME='test'
    def initial(self,seed):return {'round':0,'done':False,'scores':[0,0],'secret':'DO_NOT_LEAK'}
    def observe(self,s):return 'visible '+str(s['round'])
    def transition(self,s,reply):return {**s,'round':1,'done':True,'scores':[1,0]}, {'hidden_fact':'DO_NOT_LEAK'}

class FakeClient:
    calls=[]
    def __init__(self,*args):pass
    def generate(self,messages,**kwargs):
        self.calls.append(deepcopy(messages))
        return 'try action',dict(status='ok',call_id='test')

def test_player_history_never_uses_hidden_facts_or_scores():
    g=Game();t={'turns':[dict(observation='public',reply='action',after=g.initial(19),facts={'oracle':'DO_NOT_LEAK'})],'scores':[{'answer':'DO_NOT_LEAK'}]}
    messages=r.public_history(t,g,1)
    assert 'DO_NOT_LEAK' not in str(messages)
    assert [m['content'] for m in messages][1:3]==['public','action']

def test_resume_checks_entire_history_and_does_not_recall_model(tmp_path,monkeypatch):
    monkeypatch.setattr(r,'Client',FakeClient);monkeypatch.setattr(r,'score_actions',lambda *args,**kwargs:[]);FakeClient.calls=[]
    args=(Game(),19,tmp_path,None,None,2,'transcript_only')
    history=[{'role':'user','content':'Prior visible experience'}]
    r.episode(*args,history);r.episode(*args,history)
    assert len(FakeClient.calls)==1
    with pytest.raises(AssertionError):r.episode(*args,[{'role':'user','content':'Different experience'}])

def test_reflection_checkpoint_is_reused_and_unhinted(tmp_path,monkeypatch):
    monkeypatch.setattr(r,'Client',FakeClient);FakeClient.calls=[]
    history=[{'role':'user','content':'visible gameplay'}]
    a=r.reflect(tmp_path,None,None,history);b=r.reflect(tmp_path,None,None,history)
    assert a==b and len(FakeClient.calls)==1
    assert FakeClient.calls[0][0]['content']==r.PLAY_SYSTEM
    assert FakeClient.calls[0][1:]==history+[dict(role='user',content=r.REFLECTION_REQUEST)]
