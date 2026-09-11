"""Verify completed revised traces, payoff labels, frozen source and exact prompt separation."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'benchmark/results/gemini-revised45-20260909';SOURCE=OUT/'source';sys.path.insert(0,str(SOURCE))
from benchmark.fullscale import gemini_audit as audit
from benchmark.fullscale.revised45 import study_games
from benchmark.v3.evaluator import score_actions
from benchmark.v3.specs import BY_ID
manifest=json.loads((OUT/'manifest.json').read_text())
for rel,digest in manifest['sources'].items():assert hashlib.sha256((SOURCE/rel).read_bytes()).hexdigest()==digest,rel
old_manifest=json.loads((OUT.parent/'gemini-engine49-20260908/manifest.json').read_text())
assert manifest['system_prompt']==old_manifest['system_prompt']
assert manifest['model']==old_manifest['model']
assert manifest['seeds']==old_manifest['seeds']
games=study_games();traces=0;requests=0;cost=0.;failures=[];score_states={}
for path in sorted(OUT.glob('episodes/*/trace.json')):
    t=json.loads(path.read_text());g=games[t['game']];s=g.initial(t['seed']);actions=[]
    expected=audit.SYSTEM
    if t['target']:expected+='\nExecution diagnostic: this mechanism is explicitly revealed to you. This is not independent discovery. '+BY_ID[t['target']].actual_implementation+' Test and use it through the normal action interface. No oracle action sequence or hidden state is provided.'
    assert t['system_prompt']==expected
    messages=[dict(role='system',content=expected)]
    for turn in t['turns']:
        assert turn['before']==s and turn['observation']==g.observe(s),path
        messages.append(dict(role='user',content=turn['observation']))
        call=json.loads((path.parent/'calls'/(turn['meta']['call_id']+'.json')).read_text())
        assert call['request']['messages']==messages,path
        s,f=g.transition(s,turn['reply']);assert s==turn['after'] and f==turn['facts'],path
        actions.append(turn['reply']);messages.append(dict(role='assistant',content=turn['reply']));requests+=1
    assert s['done'] and s['scores']==t['final_scores']
    assert score_actions(t['game'],t['seed'],actions,game=g)==t['scores']
    assert not any(s['executed'] for s in t['scores'] if s['category']=='coalition_kingmaking')
    traces+=1
for p in OUT.glob('episodes/*/calls/*.json'):
    d=json.loads(p.read_text())
    for a in d['attempts']:
        if 'error' in a:failures.append(dict(call_id=d['call_id'],status=a.get('http_status'),error=a['error'],reserved_usd=d['reserved_usd']))
        else:cost+=(a.get('response',{}).get('usage') or {}).get('cost',0) or 0
result=dict(verified_traces=traces,verified_successful_requests=requests,source_hashes_verified=len(manifest['sources']),system_and_model_match_original=True,prompt_mismatches=0,reported_cost_usd=cost,failed_requests=len(failures),failure_status_counts={str(s):sum(f['status']==s for f in failures) for s in set(f['status'] for f in failures)},conservative_failure_reservations_usd=sum(f['reserved_usd'] for f in failures))
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
