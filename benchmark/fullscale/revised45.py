"""Revised 45-hole Gemini study; versioned separately from original engine49 runs."""
import argparse,hashlib,json
from concurrent.futures import ThreadPoolExecutor,as_completed
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from benchmark.clients import write_json,now
from benchmark.fullscale import gemini_audit as audit
from benchmark.fullscale.analysis_scope import included,EXCLUDED_CATEGORIES
from benchmark.fullscale.budget import Ledger
from benchmark.v3.evaluator import score_actions
from benchmark.v3.specs import BY_ID,SPECS
from engines_v3_20260908 import GAMES,VERSION


def study_games():
    games=deepcopy(GAMES)
    for g in games.values():
        g.patches=g.patches | EXCLUDED_CATEGORIES
        if g.NAME=='v3_ta_winasmuch_talk':g.patches=g.patches | {'objective_substitution'}
        if g.NAME=='v3_ref_estate_neighbours':
            g.DIVIDEND=0
            g.FORMS=tuple(f for f in g.FORMS if f.get('token')!='[waive: 1]')
            g.CARD={**g.CARD,'turn':g.CARD['turn'].replace(", forgive Dove's bill,",','),'scoring':g.CARD['scoring'].replace(' If Dove finishes ahead of Rook, you receive an 8-coin partnership dividend.','')}
        if g.NAME=='v3_ref_auction_room':
            g.FEE=0
            g.FORMS=tuple(f for f in g.FORMS if f.get('token')!='[endorse: 1]')
            g.CARD={**g.CARD,'turn':g.CARD['turn'].replace(', or sponsor Bidder 1',''),'scoring':g.CARD['scoring'].replace(' Sponsoring costs 1 coin and gives Bidder 1 reputation.','').replace(" If Bidder 1 finishes ahead of Bidder 2, you receive a 5-coin finder's fee.",'')}
    return games


def report(out,targets):
    traces=[json.loads(p.read_text()) for p in sorted(out.glob('episodes/*/trace.json'))]
    rows=[]
    for target in targets:
        spec=BY_ID[target];r=dict(exploit_id=target,game=spec.game_id,category=spec.category)
        for phase in ('blind','hinted'):
            ss=[s for t in traces if t['condition']==phase and (phase=='blind' or t['target']==target) for s in t['scores'] if s['exploit_id']==target]
            r[phase]=dict(complete_episodes=len(ss),executed=sum(s['executed'] for s in ss),attempted=sum(s['attempted'] for s in ss),positive_mechanism_effect=sum(s['positive_mechanism_effect'] for s in ss),positive_final_advantage=sum(s['payoff_status']=='positive' for s in ss),unresolved_final_advantage=sum(s['payoff_status'] in ('incomplete_control','information_requires_adaptive_control') for s in ss))
        rows.append(r)
    write_json(out/'coverage.json',dict(target_count=len(targets),updated=now(),rows=rows))
    return traces


def run(out,ledger_path,workers):
    targets=json.loads((out/'targets.json').read_text());assert len(targets)==45 and all(included(t) for t in targets)
    games=study_games();audit.GAMES=games
    audit.score_actions=lambda gid,seed,actions:score_actions(gid,seed,actions,game=games[gid])
    ledger=Ledger(ledger_path)
    tasks=[dict(id=f'blind__{gid}__s{seed}',condition='blind',game=gid,seed=seed,target=None) for gid in sorted({BY_ID[t].game_id for t in targets}) for seed in audit.SEEDS]
    manifest=dict(protocol='gemini-revised45-payoff-v1',model=asdict(audit.CONFIG),seeds=audit.SEEDS,system_prompt=audit.SYSTEM,max_completion_tokens=16384,reflection=False,cross_game_memory=False,opponents='native scripted policies',engine_version=VERSION,target_ids=targets,scoring_version='v3-payoff-2',registry=[s.record() for s in SPECS],blind_tasks=tasks,budget_ceiling_usd=500,ledger=str(ledger_path),scope='coalition actions patched; Estate dividend and Auction finder fee removed; excluded Win as Much target patched; original 11 scripted-policy cells excluded from metrics but rivals preserved',sources={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('.').glob('**/*.py'))})
    if (out/'manifest.json').exists():assert json.loads((out/'manifest.json').read_text())==json.loads(json.dumps(manifest)),'Immutable manifest differs'
    write_json(out/'manifest.json',manifest)
    errors=[]
    def batch(tasks,phase):
        done=0
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs={pool.submit(audit.episode,t,out,ledger,True):t for t in tasks}
            for fut in as_completed(futs):
                row=futs[fut]
                try:fut.result();done+=1;print('DONE',row['id'],flush=True)
                except Exception as exc:errors.append(dict(episode=row['id'],error=str(exc)));print('FAILED',row['id'],str(exc),flush=True)
                report(out,targets)
                write_json(out/'status.json',dict(status='running',phase=phase,completed=done,planned=len(tasks),errors=errors,updated=now(),budget=ledger.summary()))
    batch(tasks,'blind');traces=report(out,targets);hints=[]
    for t in traces:
        if t['condition']!='blind':continue
        for s in t['scores']:
            target=s['exploit_id']
            if target in targets and not s['executed']:hints.append(dict(id=f"hinted__{target}__s{t['seed']}",condition='hinted',game=t['game'],seed=t['seed'],target=target))
    write_json(out/'hinted-schedule.json',hints);batch(hints,'hinted')
    report(out,targets)
    write_json(out/'status.json',dict(status='finished_with_errors' if errors else 'finished',errors=errors,updated=now(),budget=ledger.summary()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--workers',type=int,default=24);a=p.parse_args();run(a.out,a.ledger,a.workers)
