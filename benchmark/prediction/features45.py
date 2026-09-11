"""Extract ex-ante numeric structure from frozen engines, never model outcomes.

The witness feature block assumes benchmark-designer access to canonical actions.
It is not available to an ordinary player and is not a discovery label.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
PLAN_PATH=ROOT/'benchmark/results/winonly45-20260909/plan.json'
PLAN=json.loads(PLAN_PATH.read_text())
SOURCE=Path(PLAN['source_root'])
sys.path[:0]=[str(SOURCE),str(SOURCE/'hole_exp')]
from benchmark.fullscale.revised45 import study_games
from benchmark.v3.specs import BY_ID
from benchmark.v3 import validate as validation
from benchmark.v3.evaluator import detected, advantage

GAME_FEATURES={
 'horizon':'Declared maximum game rounds.',
 'players':'Number of player score slots at initial state (scripted rivals included).',
 'action_forms':'Number of public action panels, including auxiliary/clerk panel.',
 'numeric_fields':'Number of public numeric input fields.',
 'free_text_fields':'Number of unconstrained text fields (no enumerated options).',
 'log_discrete_options':'log(1 + total number of enumerated field choices).',
 'log_observation_chars':'log(1 + initial player observation length).',
}
WITNESS_FEATURES={
 'witness_steps':'Number of submissions in the supplied canonical witness (not minimum possible).',
 'activation_fraction':'Index of first canonical activation divided by declared horizon.',
 'mean_action_fields':'Mean bracketed input fields per witness submission.',
 'auxiliary_interface':'Whether the canonical witness uses the shared clerk interface.',
 'prefix_own_cost':'Normal-prefix own score minus witness-prefix own score, divided by 1+abs(normal final score).',
 'control_own_delta':'Witness-policy final own score minus independently patched same-prefix policy final own score, normalized by honest final score scale.',
 'control_advantage_delta':'Analogous competitive-margin/team-score contrast, normalized by honest final score scale.',
}


def replay(game,seed,actions):
    state=game.initial(seed);events=[]
    for action in actions:
        if state['done']:break
        before=deepcopy(state);state,facts=game.transition(state,action)
        events.append(dict(before=before,action=action,after=deepcopy(state),facts=facts))
    return state,events


def finish(game,state):
    actions=[]
    while not state['done']:
        if len(actions)>=32:raise ValueError('Normal continuation exceeds 32 submissions')
        action=game.normal(state);state,_=game.transition(state,action);actions.append(action)
    return state,actions


def extract(spec,seed,game):
    forms=game.forms();fields=[x for form in forms for x in form['fields']]
    initial=game.initial(seed)
    features=dict(horizon=game.ROUNDS,players=len(initial['scores']),action_forms=len(forms),
        numeric_fields=sum(not f.get('text',True) for f in fields),
        free_text_fields=sum(bool(f.get('text')) and not f.get('options') for f in fields),
        log_discrete_options=math.log1p(sum(len(f.get('options') or []) for f in fields)),
        log_observation_chars=math.log1p(len(game.observe(initial))))
    actions=validation.witness(spec,seed)
    prefix,events=replay(game,seed,actions)
    hits=[i for i,e in enumerate(events,1) if detected(spec,e['facts'],e['before'],e['action'])]
    assert hits,('Canonical witness does not activate target',spec.exploit_id,seed)
    control=deepcopy(game);control.patches=control.patches | {spec.category}
    patched_prefix,patched_events=replay(control,seed,actions)
    assert not any(detected(spec,e['facts'],e['before'],e['action']) for e in patched_events),('Patched witness activates',spec.exploit_id,seed)
    normal_final,normal_actions=finish(game,game.initial(seed))
    normal_prefix,_=replay(game,seed,normal_actions[:len(actions)])
    final,continuation=finish(game,deepcopy(prefix))
    patched_final,patched_continuation=finish(control,deepcopy(patched_prefix))
    scale=1+abs(normal_final['scores'][0])
    features.update(witness_steps=len(actions),activation_fraction=hits[0]/game.ROUNDS,
        mean_action_fields=sum(len(re.findall(r'\[[^\]]+\]',a)) for a in actions)/len(actions),
        auxiliary_interface=int(any('[clerk:' in a for a in actions)),
        prefix_own_cost=(normal_prefix['scores'][0]-prefix['scores'][0])/scale,
        control_own_delta=(final['scores'][0]-patched_final['scores'][0])/scale,
        control_advantage_delta=(advantage(final)-advantage(patched_final))/scale)
    assert set(features)==set(GAME_FEATURES)|set(WITNESS_FEATURES)
    assert all(math.isfinite(float(x)) for x in features.values())
    return dict(target=spec.exploit_id,game=spec.game_id,family=game.BASE,mechanism=spec.category,seed=seed,features=features,
        evidence=dict(witness_actions=actions,activation_steps=hits,normal_actions=normal_actions,
            continuation=continuation,patched_continuation=patched_continuation,
            prefix_scores=prefix['scores'],normal_prefix_scores=normal_prefix['scores'],
            final_scores=final['scores'],patched_final_scores=patched_final['scores'],normal_final_scores=normal_final['scores']))


def build(out):
    for path,sha in PLAN['sources'].items():assert hashlib.sha256((SOURCE/path).read_bytes()).hexdigest()==sha,path
    games=study_games();validation.GAMES=games
    rows=[extract(BY_ID[target],seed,games[BY_ID[target].game_id]) for target in PLAN['targets'] for seed in PLAN['seeds']]
    assert len(rows)==135 and len({r['target'] for r in rows})==45
    out.mkdir(parents=True,exist_ok=True)
    schema=dict(game_features=GAME_FEATURES,witness_features=WITNESS_FEATURES,
        forbidden_inputs=['target ID','game ID','family ID','mechanism category','seed ID','model outcomes','model responses','spec prose','action token identities'],
        allowed_context=['model ID','prompt condition'],
        caveats=['Canonical witnesses are oracle-informed designer features, not player-accessible hints or behavioral labels.',
                 'Witness length is not minimum exploit complexity.',
                 'Control deltas compare fixed witness prefixes with scripted continuations; they are not optimal or expected exploit payoffs.',
                 'General structural features can still proxy taxonomy or game identity; grouped holdouts are essential.'])
    (out/'features.json').write_text(json.dumps(rows,indent=2)+'\n')
    (out/'feature-schema.json').write_text(json.dumps(schema,indent=2)+'\n')
    provenance=dict(engine_source=str(SOURCE),engine_version=PLAN['engine_version'],sources=PLAN['sources'],
        extractor_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),features_sha256=hashlib.sha256((out/'features.json').read_bytes()).hexdigest(),
        feature_rows=len(rows),targets=45,editions=len({r['game'] for r in rows}),families=len({r['family'] for r in rows}),mechanisms=len({r['mechanism'] for r in rows}),
        source='Only frozen engine/interface and canonical witness definitions; no behavioral result files read by this extractor.')
    (out/'feature-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print(json.dumps({k:v for k,v in provenance.items() if k not in ('sources','source')}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();build(args.out)
