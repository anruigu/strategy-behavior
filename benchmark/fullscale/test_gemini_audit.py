import json
from pathlib import Path
from benchmark.fullscale import gemini_audit as audit
from benchmark.v3.validate import witness
from benchmark.v3.specs import SPECS

def test_blind_and_hint_contexts_and_engine_scoring(tmp_path,monkeypatch):
    spec=next(s for s in SPECS if s.category=='resource_duplication' and 'seven_seal' in s.game_id)
    actions=witness(spec,19)+['[pass: 1]']*8
    seen=[]
    class FakeClient:
        def __init__(self,*args):self.i=0
        def generate(self,messages,**kwargs):
            seen.append(messages[0]['content']);reply=actions[self.i];self.i+=1
            return reply,dict(status='ok',call_id='test')
    monkeypatch.setattr(audit,'StudyClient',FakeClient)
    row=dict(id='blind',condition='blind',game=spec.game_id,seed=19,target=None)
    t=audit.episode(row,tmp_path,None)
    assert next(s for s in t['scores'] if s['exploit_id']==spec.exploit_id)['executed']
    assert all('Execution diagnostic:' not in s for s in seen)
    seen.clear()
    row.update(id='hint',condition='hinted',target=spec.exploit_id)
    audit.episode(row,tmp_path,None)
    assert all('Execution diagnostic:' in s and spec.actual_implementation in s for s in seen)
    assert all('[redeem:' not in s for s in seen)
