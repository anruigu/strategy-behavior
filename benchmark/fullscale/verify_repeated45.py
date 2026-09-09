"""Replay all completed episodes and reconstruct exact player-only request contexts."""
import argparse,json,hashlib,runpy
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[2]
r=SimpleNamespace(**runpy.run_path(str(ROOT/'benchmark/fullscale/repeated45.py'),run_name='verify_helpers'))

r.CONFIGS.update({m:r.ModelConfig(**cfg) for m,cfg in json.loads((r.BASE/'plan.json').read_text())['models'].items()})

def verify(model):
 out=r.BASE/model;plan=json.loads((r.BASE/'plan.json').read_text());manifest=json.loads((out/'manifest.json').read_text());games=r.study_games();counts=dict(episodes=0,play_requests=0,reflections=0);actual=set()
 for rel,h in plan['engine_sources'].items():assert hashlib.sha256((r.SOURCE/rel).read_bytes()).hexdigest()==h,rel
 assert manifest['runner_sha256']==hashlib.sha256((ROOT/'benchmark/fullscale/repeated45.py').read_bytes()).hexdigest()
 assert manifest['model']==r.asdict(r.CONFIGS[model])
 for ref in manifest['reused_blind']:assert hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest()==ref['sha256']
 def call_check(path,meta,messages,purpose):
  call=json.loads((path/'calls'/(meta['call_id']+'.json')).read_text());request=call['request'];assert request['messages']==messages,path
  assert request['model']==r.CONFIGS[model].provider_model,path
  assert request['extra_body']['reasoning']=={'effort':r.CONFIGS[model].reasoning_effort},path
  expected_cap=16384 if purpose!='reflection' or (model=='gemini-3.1-pro' and meta.get('recovery_reflection_cap')==16384) else 8192
  assert request['max_tokens']==expected_cap,path
  actual.add(meta['actual_model'])
 def episode_check(path,game,seed,iteration,history):
  t=json.loads((path/'trace.json').read_text());system=r.SYSTEM if iteration==1 else r.PLAY_SYSTEM
  messages=[dict(role='system',content=system)]+history
  if iteration>1:messages.append(dict(role='user',content=f'BEGIN NEW EPISODE {iteration} of 4. The game has reset to the same starting state. Play to win.'))
  assert t['system_prompt']==system,path
  if 'prefix_sha256' in t:assert t['prefix_sha256']==r.digest(messages),path
  state=game.initial(seed);actions=[]
  for turn in t['turns']:
   assert turn['before']==state and turn['observation']==game.observe(state),path
   messages.append(dict(role='user',content=turn['observation']));call_check(path,turn['meta'],messages,'play')
   if 'context_sha256' in turn:assert turn['context_sha256']==r.digest(messages)
   state,facts=game.transition(state,turn['reply']);assert state==turn['after'] and facts==turn['facts'],path
   actions.append(turn['reply']);messages.append(dict(role='assistant',content=turn['reply']));counts['play_requests']+=1
  assert state['done'] and state['scores']==t['final_scores'],path
  assert r.score_actions(game.NAME,seed,actions,game=game)==t['scores'],path
  counts['episodes']+=1;return t
 expected_pairs=[(g,s) for g in sorted({t.rsplit('.',1)[0] for t in plan['targets']}) for s in plan['seeds']]
 complete=True
 for gid,seed in expected_pairs:
  game=games[gid];bp=r.baseline_path(model,gid,seed)
  if not (bp/'trace.json').exists():complete=False;continue
  baseline=episode_check(bp,game,seed,1,[])
  for arm in ('transcript_only','reflection'):
   history=r.public_history(baseline,game,1);branch=out/'chains'/f'{gid}__s{seed}'/arm
   for it in range(2,5):
    if arm=='reflection':
     rp=branch/f'after-{it-1}'
     if not (rp/'reflection.json').exists():complete=False;break
     reflection=json.loads((rp/'reflection.json').read_text());messages=[dict(role='system',content=r.PLAY_SYSTEM)]+history+[dict(role='user',content=r.REFLECTION_REQUEST)]
     assert reflection['request']==r.REFLECTION_REQUEST and reflection['context_sha256']==r.digest(messages)
     call_check(rp,reflection['meta'],messages,'reflection');counts['reflections']+=1
     history=history+[dict(role='user',content=reflection['request']),dict(role='assistant',content=reflection['reply'])]
    ep=branch/f'play-{it}'
    if not (ep/'trace.json').exists():complete=False;break
    t=episode_check(ep,game,seed,it,history.copy());history+=r.public_history(t,game,it)
 result=dict(**counts,complete=complete,expected_unique_episodes=357,expected_reflections=153,actual_models=sorted(actual),source_hashes_verified=len(plan['engine_sources']),prompt_mismatches=0,player_history_only=True)
 r.write_json(out/'verification.json',result);return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--model',choices=list(r.CONFIGS));a=p.parse_args()
 for model in ([a.model] if a.model else json.loads((r.BASE/'plan.json').read_text()).get('active_models',list(r.CONFIGS))):
  if (r.BASE/model/'manifest.json').exists():print(model,json.dumps(verify(model)))
