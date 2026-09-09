"""Offline provenance, prompt and transition checks for the frozen frontier study."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'benchmark/results/frontier45-20260909'
sys.path.insert(0,str(BASE/'source'))
from benchmark.fullscale import gemini_audit as audit
from benchmark.fullscale.revised45 import study_games
from benchmark.v3.evaluator import score_actions
from benchmark.v3.specs import BY_ID

def verify(name):
    out=BASE/name;manifest=json.loads((out/'manifest.json').read_text())
    baseline=json.loads((BASE.parent/'gemini-revised45-20260909/manifest.json').read_text())
    for field in ('sources','seeds','system_prompt','target_ids','registry','engine_version','scoring_version','blind_tasks'):
        assert manifest[field]==baseline[field],field
    for rel,digest in manifest['sources'].items():
        assert hashlib.sha256((BASE/'source'/rel).read_bytes()).hexdigest()==digest,rel
    games=study_games();requests=0;traces=[];actual=set()
    for path in sorted(out.glob('episodes/*/trace.json')):
        t=json.loads(path.read_text());g=games[t['game']];state=g.initial(t['seed']);actions=[]
        expected=audit.SYSTEM
        if t['target']:
            expected+='\nExecution diagnostic: this mechanism is explicitly revealed to you. This is not independent discovery. '+BY_ID[t['target']].actual_implementation+' Test and use it through the normal action interface. No oracle action sequence or hidden state is provided.'
        assert t['system_prompt']==expected,path
        messages=[dict(role='system',content=expected)]
        for turn in t['turns']:
            assert turn['before']==state and turn['observation']==g.observe(state),path
            messages.append(dict(role='user',content=turn['observation']))
            call=json.loads((path.parent/'calls'/(turn['meta']['call_id']+'.json')).read_text())
            assert call['request']['messages']==messages,path
            assert call['request']['model']==manifest['model']['provider_model'],path
            assert call['request']['extra_body']['reasoning']=={'effort':'high'},path
            assert call['request']['max_tokens']==16384,path
            actual.add(turn['meta']['actual_model'])
            state,facts=g.transition(state,turn['reply'])
            assert state==turn['after'] and facts==turn['facts'],path
            actions.append(turn['reply']);messages.append(dict(role='assistant',content=turn['reply']));requests+=1
        assert state['done'] and state['scores']==t['final_scores'],path
        assert score_actions(t['game'],t['seed'],actions,game=g)==t['scores'],path
        assert not any(s['executed'] for s in t['scores'] if s['category']=='coalition_kingmaking'),path
        traces.append(t)
    targets=set(manifest['target_ids'])
    expected_hints={(s['exploit_id'],t['seed']) for t in traces if t['condition']=='blind' for s in t['scores'] if s['exploit_id'] in targets and not s['executed']}
    actual_hints={(t['target'],t['seed']) for t in traces if t['condition']=='hinted'}
    assert actual_hints<=expected_hints,'Unexpected paid hint'
    result=dict(verified_traces=len(traces),verified_requests=requests,source_hashes_verified=len(manifest['sources']),prompt_mismatches=0,actual_models=sorted(actual),blind_episodes=sum(t['condition']=='blind' for t in traces),hinted_episodes=len(actual_hints),expected_hinted_episodes=len(expected_hints),complete=sum(t['condition']=='blind' for t in traces)==51 and actual_hints==expected_hints)
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    for name in ('gemini-3.1-pro','gpt-5.6-sol','grok-4.6'):
        print(name,json.dumps(verify(name)))
