from copy import deepcopy
import pytest
from benchmark.scaleup.validate import validate,witness
from benchmark.scaleup.specs import SPECS,CONTROL_IDS,HUMAN_IDS
from benchmark.scaleup.evaluator import score_actions
from engines_scaleup_20260907 import GAMES
from test_benchmark_views import from_controls
import catalog,views


def test_all_sixty_mechanisms_and_controls():
    assert len(validate())==60
    assert len(CONTROL_IDS)==12 and len(set(HUMAN_IDS))==24
    assert len({s.category for s in SPECS if s.exploit_id in HUMAN_IDS})==20

@pytest.mark.parametrize('spec',SPECS,ids=lambda s:s.exploit_id)
def test_oracle_reachable_through_human_controls(spec):
    g=GAMES[spec.game_id];s=g.initial(0);gid=catalog.V2_IDS[spec.game_id]
    for raw in witness(spec):
        v=views.build(gid,'move',g.observe(s));assert v
        assembled=from_controls(v,raw)
        assert g.transition(s,assembled)==g.transition(s,raw)
        s,_=g.transition(s,assembled)


def test_actions_never_imply_articulated_discovery():
    for spec in SPECS:
        rows=score_actions(spec.game_id,0,witness(spec))
        assert all(r['discovered'] is None for r in rows)


def test_battleship_patched_move_resolves_enemy_shot_only_once():
    g=type(GAMES['ref_battleship'])(patches=['turn_order']);s=g.initial(0)
    s['enemy_orders'][0]='D4'
    after,_=g.transition(s,'[evade: A1>D4]')
    assert 'D4' in after['own_hull']


def test_new_runner_uses_fresh_context_and_no_reflection(tmp_path):
    from benchmark.scaleup.runner import episode
    from test_scaleup_views import normal_from_public
    class ScriptedClient:
        def __init__(self,gid):self.gid=gid;self.calls=0
        def generate(self,messages,**kwargs):
            assert kwargs['purpose']=='play'
            assert len(messages)==2*self.calls+2
            self.calls+=1
            view=views.build(catalog.V2_IDS[self.gid],'move',messages[-1]['content'])
            return normal_from_public(view),dict(call_id=f'fixture-{self.calls}')
    for gid in GAMES:
        client=ScriptedClient(gid)
        result=episode(gid,0,client,tmp_path/(gid+'.json'))
        assert result['condition']=='no_reflection' and result['playbook_before']==''
        assert len(result['turns'])==client.calls
        assert all(r['discovered'] is None for r in result['evaluation'])


def test_discovery_judge_receives_scaleup_specs_and_only_player_quotes():
    import json
    from benchmark.discovery import judge
    class JudgeFixture:
        def generate(self,messages,**kwargs):
            payload=json.loads(messages[1]['content'])
            assert payload['model_articulation']=='No mechanism claimed.'
            ids=[s['exploit_id'] for s in payload['specifications']]
            assert len(ids)==8 and all(i.startswith('ref_battleship.') for i in ids)
            return json.dumps(dict(judgments=[dict(exploit_id=i,correct_hypothesis=False,discovered=False,quote='',reason='No claim') for i in ids])),{}
    result=judge(JudgeFixture(),'ref_battleship','Referee says target D1.',[],articulation='No mechanism claimed.',specifications=SPECS)
    assert len(result['judgments'])==8
