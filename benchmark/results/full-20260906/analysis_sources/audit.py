"""Offline integrity audit of recorded trajectories and model-call provenance."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from .evaluator import evaluate
from .clients import write_json
from .discovery import model_articulation
from .prompts import parse_playbook


def audit(out):
    out=Path(out)
    config=json.loads((out/'config.json').read_text())
    checks=0
    for name,want in config['source_fingerprints'].items():
        assert hashlib.sha256((out/'source'/name).read_bytes()).hexdigest()==want,name
        checks+=1
    # Early pilots predate prompt-only profile revisions. Replay their actual
    # profile, while requiring the imported native dependencies to still match.
    frozen=out/'source/benchmark/games.py'
    spec=importlib.util.spec_from_file_location('benchmark._audit_snapshot_games',frozen)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    games=module.GAMES
    for imported,relative in {
        'referee_games':'hole_exp/referee_games.py',
        'referee_games2':'hole_exp/referee_games2.py',
        'engines_generated':'hole_exp/hackable_games/engines_generated.py',
        'engines_textarena':'hole_exp/hackable_games/engines_textarena.py',
    }.items():
        assert hashlib.sha256(Path(sys.modules[imported].__file__).read_bytes()).hexdigest()==config['source_fingerprints'][relative],relative
        checks+=1
    traces=[json.loads(p.read_text()) for p in out.glob('*/traces/*.json')]
    for model in config['args']['models']:
        mine=sorted((t for t in traces if t['model_id']==model),key=lambda t:t['sequence'])
        prior=None
        for t in mine:
            game=games[t['game_id']]
            ep=t['episode']
            events=ep['extras']['events']
            assert events[0]['state_before']==game.initial(t['seed'])
            assert len(events)==len(t['turns'])<=game.ROUNDS<=8
            for i,(event,turn) in enumerate(zip(events,t['turns'],strict=True)):
                assert event['observation']==turn['prompt']==game.observe(event['state_before'])
                assert event['action']==turn['reply']
                after,facts=game.transition(event['state_before'],event['action'])
                assert after==event['state_after'] and facts==event['facts']
                if i:
                    assert events[i-1]['state_after']==event['state_before']
                normal=game.normal(event['state_before'])
                assert event['normal_action']==normal
                assert game.transition(event['state_before'],normal)[0]==event['normal_after']
                assert game.transition(event['state_before'],event['action'],'nohole')[0]==event['checked_after']
                call=json.loads((out/model/'calls'/(turn['meta']['call_id']+'.json')).read_text())
                response=call['attempts'][-1]['response']
                assert response['choices'][0]['message']['content']==turn['reply']
                assert response['model']==turn['meta']['actual_model']
                assert call['request']['messages'][0]['content']==t['system_prompt']
                assert call['request']['messages'][-1]['content']==turn['prompt']
                checks+=12
            final=events[-1]['state_after']
            assert final['done'] and final==ep['extras']['final_state']
            assert final['scores']==[ep['scores'][str(p)] for p in range(game.N_PLAYERS)]
            evaluated=evaluate(game.NAME,events)
            for got,want in zip(t.get('execution',[]),evaluated,strict=bool(t.get('execution'))):
                assert all(got[k]==v for k,v in want.items())
            incoming=''
            if prior and t['condition']=='persistent' and (t['scope']=='cross-game' or prior['game_id']==t['game_id']):
                incoming=json.dumps(prior['playbook_after'],ensure_ascii=False)
            assert t['playbook_before']==incoming
            if 'playbook_after' in t:
                call=json.loads((out/model/'calls'/(t['reflection_meta']['call_id']+'.json')).read_text())
                assert call['attempts'][-1]['response']['choices'][0]['message']['content']==t['reflection']
                raw=t['reflection']
                if t['reflection_meta'].get('schema_normalization'):
                    obj=json.loads(raw)
                    for old,new in t['reflection_meta']['schema_normalization'].items():
                        obj[new]=obj.pop(old)
                    raw=json.dumps(obj,ensure_ascii=False)
                assert parse_playbook(raw)==t['playbook_after']
                saved=json.loads((out/model/'playbooks'/f'{t["sequence"]:02d}.json').read_text())
                assert saved['playbook']==t['playbook_after']
                checks+=3
                prior=t
            if t.get('discovery_judge',{}).get('evaluator_version')=='discovery-v3-model-articulation':
                authored=model_articulation(t)
                mapping={j['exploit_id']:j for j in t['discovery_judge']['judgments']}
                assert set(mapping)=={r['exploit_id'] for r in evaluated}
                for row in t['evaluation']:
                    j=mapping[row['exploit_id']]
                    assert all(row[k]==v for k,v in j.items())
                    if j['discovered'] or j['correct_hypothesis']:
                        assert j['quote'].strip() and j['quote'] in authored
                    assert not j['discovered'] or j['correct_hypothesis']
                    checks+=3
                checks+=1
            checks+=5
    result={'traces_audited':len(traces),'checks':checks,'passed':True,
            'note':'Replay used frozen source/benchmark/games.py. Source snapshots and installed native dependencies hash-verified; final discovery quotes checked against model-authored text.'}
    write_json(out/'integrity_audit.json',result)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    print(json.dumps(audit(args.output),indent=2))
