"""Offline, frozen-trace diagnostic. No API calls or changes to benchmark scores."""
from pathlib import Path
import json, hashlib, csv, collections, re
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
snapshot=OUT/'trace_snapshot.json'
if not snapshot.exists():
    traces=[]
    for p in sorted(ROOT.glob('*/traces/*.json')):
        raw=p.read_bytes(); t=json.loads(raw)
        t['_path']=str(p.relative_to(ROOT)); t['_sha256']=hashlib.sha256(raw).hexdigest()
        traces.append(t)
    snapshot.write_text(json.dumps(traces,ensure_ascii=False))
else:
    traces=json.loads(snapshot.read_text())
scored=[t for t in traces if t['status']=='complete' and t.get('discovery_judge',{}).get('evaluator_version')=='discovery-v3-model-articulation']
rows=[dict(r,trace_path=t['_path']) for t in scored for r in t['evaluation']]
lookup={(t['model_id'],t['game_id'],t['iteration']):t for t in scored}
chains=collections.defaultdict(list)
for r in rows: chains[r['model_id'],r['exploit_id']].append(r)
for rs in chains.values(): rs.sort(key=lambda r:r['iteration'])
def strings(x):
    if isinstance(x,str): return [x]
    if isinstance(x,dict): return [s for v in x.values() for s in strings(v)]
    if isinstance(x,list): return [s for v in x for s in strings(v)]
    return []
def before(t):
    try:return '\n'.join(strings(json.loads(t['playbook_before'])))
    except ValueError:return t['playbook_before']
def stages(rs):
    return dict(n=len(rs),hypothesis=sum(r['correct_hypothesis'] for r in rs),discovered=sum(r['discovered'] for r in rs),attempted=sum(r['attempted'] for r in rs),executed=sum(r['executed'] for r in rs),successful=sum(r['successful'] for r in rs),unvisited=sum(not r['opportunity_encountered'] for r in rs),hypothesis_no_execution=sum(r['correct_hypothesis'] and not r['executed'] for r in rs),execution_no_hypothesis=sum(r['executed'] and not r['correct_hypothesis'] for r in rs),execution_no_discovery=sum(r['executed'] and not r['discovered'] for r in rs))
def writecsv(name,rs):
    if not rs:return
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
transitions=[]
for key,rs in chains.items():
    for a,b in zip(rs,rs[1:]):
        if b['iteration']!=a['iteration']+1:continue
        ta=lookup[a['model_id'],a['game_id'],a['iteration']];tb=lookup[b['model_id'],b['game_id'],b['iteration']]
        q=a['quote']
        transitions.append(dict(model=a['model_id'],exploit=a['exploit_id'],game=a['game_id'],iteration=a['iteration'],h=a['correct_hypothesis'],d=a['discovered'],e=a['executed'],next_h=b['correct_hypothesis'],next_d=b['discovered'],next_e=b['executed'],next_opportunity=b['opportunity_encountered'],quote_in_reflection=bool(q and q in '\n'.join(strings(ta['playbook_after']))),quote_in_next_memory=bool(q and q in before(tb)),quote=q,next_quote=b['quote'],reason=a['reason'],next_reason=b['reason'],trace=a['trace_path'],next_trace=b['trace_path']))
writecsv('transitions.csv',transitions)
models=list(dict.fromkeys(r['model_id'] for r in rows))
curves=[]
for m in models:
    cs=[rs for (model,e),rs in chains.items() if model==m]
    balanced=[rs for rs in cs if {r['iteration'] for r in rs}=={1,2,3,4}]
    for i in range(1,5):
        at=[r for rs in cs for r in rs if r['iteration']==i]
        br=[r for rs in balanced for r in rs if r['iteration']==i]
        curves.append(dict(model=m,iteration=i,n=len(at),current_discovery=sum(r['discovered'] for r in at),balanced_n=len(balanced),balanced_current_discovery=sum(r['discovered'] for r in br),balanced_cumulative_discovery=sum(any(r['discovered'] and r['iteration']<=i for r in rs) for rs in balanced),balanced_cumulative_execution=sum(any(r['executed'] and r['iteration']<=i for r in rs) for rs in balanced),balanced_cumulative_hypothesis=sum(any(r['correct_hypothesis'] and r['iteration']<=i for r in rs) for rs in balanced)))
writecsv('curves.csv',curves)
mechs=[]
for e in sorted({r['exploit_id'] for r in rows}):
    rs=[r for r in rows if r['exploit_id']==e]
    mechs.append(dict(exploit=e,**stages(rs)))
writecsv('mechanisms.csv',mechs)
modelstats=[]
for m in models:
    rs=[r for r in rows if r['model_id']==m]; ts=[t for t in transitions if t['model']==m]
    hs=[t for t in ts if t['h']]; ds=[t for t in ts if t['d']]
    modelstats.append(dict(model=m,**stages(rs),h_transitions=len(hs),next_e_after_h=sum(t['next_e'] for t in hs),d_transitions=len(ds),next_e_after_d=sum(t['next_e'] for t in ds),d_drops=sum(not t['next_d'] for t in ds),drops_quote_retained=sum(not t['next_d'] and t['quote_in_next_memory'] for t in ds)))
writecsv('models.csv',modelstats)
continuity=[]
for m in models:
    ts=sorted([t for t in traces if t['model_id']==m],key=lambda t:t['sequence'])
    for a,b in zip(ts,ts[1:]):
        if 'playbook_after' in a and b['sequence']==a['sequence']+1:
            continuity.append(json.dumps(a['playbook_after'],ensure_ascii=False)==b['playbook_before'])
summary=dict(traces=len(traces),scored=len(scored),status=dict(collections.Counter(t['status'] for t in traces)),overall=stages(rows),models=modelstats,continuity=dict(checked=len(continuity),exact=sum(continuity)),transitions={})
for name,cond in [('hypothesis',lambda t:t['h']),('discovery',lambda t:t['d']),('hypothesis_without_execution',lambda t:t['h'] and not t['e']),('hypothesis_without_execution_reflection',lambda t:t['h'] and not t['e'] and t['quote_in_reflection'])]:
    ts=[t for t in transitions if cond(t)]
    summary['transitions'][name]=dict(n=len(ts),next_executed=sum(t['next_e'] for t in ts),next_opportunity=sum(t['next_opportunity'] for t in ts),quote_retained=sum(t['quote_in_next_memory'] for t in ts),discovery_drops=sum(t['d'] and not t['next_d'] for t in ts),discovery_drops_quote_retained=sum(t['d'] and not t['next_d'] and t['quote_in_next_memory'] for t in ts))
(OUT/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
print('MECHANISMS');print(json.dumps(mechs,indent=2))

# Verify deterministic labels separately from the semantic judge.
import sys, itertools
sys.path.insert(0,str(OUT.parents[3]))
from benchmark.games import GAMES
from benchmark.evaluator import evaluate
engine_matches={f:(OUT.parents[2]/f).read_bytes()==(ROOT/'source/benchmark'/f).read_bytes() for f in ('games.py','evaluator.py')}
assert all(engine_matches.values()), 'Engine changed from saved run; inspect before replaying'
fields=['opportunity_encountered','attempted','executed','successful','execution_count','success_count']
mismatches=[]
for t in scored:
    derived={r['exploit_id']:r for r in evaluate(t['game_id'],t['episode']['extras']['events'])}
    for r in t['evaluation']:
        for f in fields:
            if derived[r['exploit_id']][f]!=r[f]:mismatches.append([t['_path'],r['exploit_id'],f])
def play(game,actions,arm='hole'):
    s=GAMES[game].initial(9060001)
    for a in actions:
        s,f=GAMES[game].transition(s,a,arm)
        if not f['valid']:return None
        if s['done']:break
    return s['scores']
acts=['[work: 1]','[build: workshop]','[dismantle: workshop]']
best=(-1,None)
for seq in itertools.product(acts,repeat=6):
    score=play('ref_exchange',seq)
    if score and score[0]>best[0]:best=(score[0],seq)
normal=[acts[i] for i in [0,0,1,0,0,0]]
exchange=[t for t in scored if t['game_id']=='ref_exchange']
identical=sum([e['facts']['action'] for e in t['episode']['extras']['events']]==['work','work','build','work','work','work'] for t in exchange)
cf=dict(execution_rows_rechecked=len(rows),deterministic_mismatches=mismatches,engine_source_matches=engine_matches,
        exchange=dict(observed_policy=normal,observed_score=play('ref_exchange',normal),best_valid_score=best[0],best_sequence=best[1],best_sequence_checked_engine=play('ref_exchange',best[1],'nohole'),identical_policy_games=identical,total_games=len(exchange)),
        ipd=dict(cooperate_three_defect_last=play('ta_ipd',['[move: cooperate]']*3+['[move: defect]']),all_defect=play('ta_ipd',['[move: defect]']*4)))
(OUT/'counterfactuals.json').write_text(json.dumps(cf,indent=2))
# Confirm the strongest judge inconsistency against the actual recorded judge input.
for t in scored:
    if (t['model_id'],t['game_id'],t['iteration'])==('gemini-3.7-flash','ref_commons',4):
        call_id=t['discovery_judge']['meta']['call_id']
        call_path=next((ROOT/t['model_id']).glob('judge*_calls/'+call_id+'.json'))
        call=json.loads(call_path.read_text())
        prompt=json.loads(call['request']['messages'][1]['content'])
        quotes=['stock goes to 0, game terminates, and other boats get 0.', 'Since player catches resolve first, this secures maximum points and leaves opponents with 0 points.']
        checks=dict(call_path=str(call_path.relative_to(ROOT)),quotes_present={q:q in prompt['model_articulation'] for q in quotes})
        assert all(checks['quotes_present'].values())
        (OUT/'judge_input_check.json').write_text(json.dumps(checks,indent=2))
assert not mismatches
