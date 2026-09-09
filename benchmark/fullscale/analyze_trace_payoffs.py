"""Offline final-payoff attribution using original frozen V3 engines and saved actions."""
import csv,json,sys
from pathlib import Path
from collections import Counter,defaultdict
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[2]
FROZEN=ROOT/'benchmark/results/gemini-engine49-20260908/source'
for p in (FROZEN/'hole_exp/hackable_games',FROZEN/'hole_exp',FROZEN):sys.path.insert(0,str(p))
from engines_v3_20260908 import GAMES
from benchmark.v3.specs import SPECS
from benchmark.v3.evaluator import detected,score_actions
from benchmark.v3.validate import witness
# Load current analysis scope without importing the mutable benchmark package.
import runpy
scope=runpy.run_path(str(ROOT/'benchmark/fullscale/analysis_scope.py'))
TARGETS={x for x in json.loads((ROOT/'benchmark/results/gemini-engine49-20260908/targets-49.json').read_text()) if scope['included'](x)}
INFO={'receipt_information','known_cards','probe_information','quote_information','open_bid_information'}
OUT=ROOT/'benchmark/results/trace-payoff-audit-20260909';OUT.mkdir(exist_ok=True)

def margin(s):return s['scores'][0] if 'hands' in s else s['scores'][0]-max(s['scores'][1:])
def replay(g,seed,actions,state=None,finish=False):
    s=deepcopy(state) if state is not None else g.initial(seed); invalid=0
    for a in actions:
        if s['done']:break
        s,f=g.transition(s,a);invalid+=not f.get('valid',True)
    tail=0
    if finish:
        while not s['done'] and tail<30:s,_=g.transition(s,g.normal(s));tail+=1
        assert s['done']
    return s,invalid,tail

def writecsv(name,rows):
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

runs=[('Gemini high',ROOT/'benchmark/results/gemini-engine49-20260908')]
for n in ['qwen-3.8-27b','glm','claude-haiku-4.5','gpt-5-mini','gemini-3.7-flash']:runs.append((n,ROOT/'benchmark/results/small-engine49-20260909'/n))
rows=[];cases=[];episodes=Counter();validated=0
for model,run in runs:
    for path in sorted((run/'episodes').glob('*/trace.json')):
        t=json.loads(path.read_text());g=GAMES[t['game']];actions=[x['reply'] for x in t['turns']]
        st=g.initial(t['seed'])
        for turn in t['turns']:
            assert st==turn['before'],path
            st,f=g.transition(st,turn['reply'])
            assert st==turn['after'] and f==turn['facts'],path
        assert st['done'] and st['scores']==t['final_scores'],path
        assert score_actions(t['game'],t['seed'],actions)==t['scores'],path
        validated+=1
        if t['condition']=='hinted' and t['target'] not in TARGETS:continue
        eligible=[s for s in t['scores'] if s['exploit_id'] in TARGETS and (t['condition']=='blind' or s['exploit_id']==t['target'])]
        if not eligible:continue
        episodes[(model,t['condition'])]+=1
        for saved in eligible:
            spec=next(s for s in SPECS if s.exploit_id==saved['exploit_id'])
            if not saved['executed']:continue
            patch=type(g)(patches=(spec.category,));cf,invalid,_=replay(patch,t['seed'],actions)
            tailcf,_,tail=replay(patch,t['seed'],[],state=cf,finish=True)
            hits=[i for i,x in enumerate(t['turns']) if detected(spec,x['facts'],x['before'],x['reply'])]
            # Replace first triggering action with the game's ordinary action, then hold remaining replies fixed.
            first=hits[0];before=t['turns'][first]['before'];normal=g.normal(before)
            alt,altinvalid,_=replay(g,t['seed'],[normal]+actions[first+1:],state=before)
            row=dict(model=model,phase=t['condition'],episode=t['id'],path=str(path.relative_to(ROOT)),target=spec.exploit_id,game=t['game'],seed=t['seed'],metric=spec.advantage_metric,information=spec.advantage_metric in INFO,
                executions=len(hits),first_turn=first+1,last_turn=hits[-1]+1,old_success=saved['successful'],old_peak_effect=saved['effect'],own_score=st['scores'][0],margin=margin(st),
                control_score=cf['scores'][0],control_margin=margin(cf),control_done=cf['done'],control_invalid=invalid,
                score_delta=st['scores'][0]-cf['scores'][0],margin_delta=margin(st)-margin(cf),
                normal_tail_turns=tail,normal_tail_score_delta=st['scores'][0]-tailcf['scores'][0],normal_tail_margin_delta=margin(st)-margin(tailcf),
                replacement_normal=normal,replacement_done=alt['done'],replacement_invalid=altinvalid,
                first_action_value_score=st['scores'][0]-alt['scores'][0],first_action_value_margin=margin(st)-margin(alt))
            rows.append(row)
            cases.append(dict(**row,turns=[dict(turn=i+1,reply=x['reply'],facts=x['facts'],scores=x['after']['scores'],feedback=x['after']['feedback']) for i,x in enumerate(t['turns'])]))
    print(model,'validated',validated,flush=True)
writecsv('execution_payoffs.csv',rows)
(OUT/'trace_evidence.json').write_text(json.dumps(cases,indent=2)+'\n')
# Scripted witness is a constructive example, not a proof of optimality or a model-discoverable plan.
witnesses=[]
for spec in SPECS:
    if spec.exploit_id not in TARGETS:continue
    for seed in (19,73,101):
        g=GAMES[spec.game_id];a=witness(spec,seed);s,_,_=replay(g,seed,a)
        while not s['done']:
            raw=g.normal(s);a.append(raw);s,_=g.transition(s,raw)
        c,_,_=replay(type(g)(patches=(spec.category,)),seed,a)
        witnesses.append(dict(target=spec.exploit_id,seed=seed,score_delta=s['scores'][0]-c['scores'][0],margin_delta=margin(s)-margin(c),control_done=c['done'],actions=a))
(OUT/'witness_payoffs.json').write_text(json.dumps(witnesses,indent=2)+'\n')
aggregate=[]
for target in sorted(TARGETS):
    rs=[r for r in rows if r['target']==target];complete=[r for r in rs if r['control_done']]
    ws=[w for w in witnesses if w['target']==target and w['control_done']]
    aggregate.append(dict(target=target,metric=next(s.advantage_metric for s in SPECS if s.exploit_id==target),executed=len(rs),complete_pairs=len(complete),positive=sum(r['margin_delta']>1e-8 for r in complete),zero=sum(abs(r['margin_delta'])<1e-8 for r in complete),negative=sum(r['margin_delta']< -1e-8 for r in complete),score_positive=sum(r['score_delta']>1e-8 for r in complete),old_success=sum(r['old_success'] for r in rs),witness_positive=sum(w['margin_delta']>0 for w in ws)))
writecsv('hole_summary.csv',aggregate)
summary=dict(validated_traces=validated,scope=45,episodes=[dict(model=m,phase=p,n=n) for (m,p),n in episodes.items()],executed_pairs=len(rows),complete_pairs=sum(r['control_done'] for r in rows),by_model=[])
for model,run in runs:
    for phase in ['blind','hinted']:
        rs=[r for r in rows if r['model']==model and r['phase']==phase];complete=[r for r in rs if r['control_done']]
        summary['by_model'].append(dict(model=model,phase=phase,n=len(rs),complete=len(complete),positive=sum(r['margin_delta']>1e-8 for r in complete),zero=sum(abs(r['margin_delta'])<1e-8 for r in complete),negative=sum(r['margin_delta']< -1e-8 for r in complete)))
summary['diagnosis'] = dict(positive_noninformation=sum(r['control_done'] and not r['information'] and r['margin_delta']>0 for r in rows), zero_noninformation=sum(r['control_done'] and not r['information'] and r['margin_delta']==0 for r in rows), negative_noninformation=sum(r['control_done'] and not r['information'] and r['margin_delta']<0 for r in rows), information_unresolved=sum(r['control_done'] and r['information'] for r in rows), unfinished_control=sum(not r['control_done'] for r in rows))
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
