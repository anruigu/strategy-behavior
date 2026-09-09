"""Budgeted live-game study; never runs native scripted-opponent adapters."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, replace
from pathlib import Path
import hashlib
import json
from benchmark.clients import MODELS, now, write_json
from benchmark.v3 import live_pilot
from benchmark.v3.live_games import GAMES, HOLES
from .budget import Ledger
from .client import StudyClient
from .design import REGISTRY, schedule as frontier_schedule, rotations

FREE=('qwen-3.8-27b','glm','claude-haiku-4.5')
CONFIGS={m:replace(c,temperature=None,reasoning_effort='medium') for m,c in {**REGISTRY,**MODELS}.items()}

def main_schedule(seeds):
    rows=[]
    for game in GAMES:
        for si,seed in enumerate(seeds):
            for mode,lineups in [('cross',rotations(FREE)),('self',[(m,)*3 for m in FREE])]:
                for r,seats in enumerate(lineups):
                    if mode=='cross' and si%2: seats=tuple(reversed(seats))
                    rows.append(dict(id=f'{game}__{mode}__s{seed}__r{r}',game=game,mode=mode,seed=seed,seats=list(seats)))
    return rows


def matched_frontier_schedule(seeds):
    rows=[]
    for game in GAMES:
        for si,seed in enumerate(seeds):
            for focal in ('gpt-5-mini','gpt-5.6-sol'):
                for mode,lineups in [('cross',rotations((focal,'qwen-3.8-27b','glm'))),('self',[(focal,)*3])]:
                    for r,seats in enumerate(lineups):
                        if mode=='cross' and si%2: seats=tuple(reversed(seats))
                        rows.append(dict(id=f'{game}__{mode}__{focal}__s{seed}__r{r}',game=game,mode=mode,seed=seed,seats=list(seats)))
    return rows

class UnusableResponse(RuntimeError): pass

def run(out,study,seeds,workers,ledger_path):
    out.mkdir(parents=True,exist_ok=True)
    ledger=Ledger(ledger_path)
    rows=main_schedule(seeds) if study=='main' else matched_frontier_schedule(seeds)
    # Reuse the verified simultaneous-action protocol, replacing its client/config only.
    class BoundClient(StudyClient):
        def __init__(self,config,log_dir): super().__init__(config,log_dir,ledger)
        def generate(self,messages,**kwargs):
            kwargs['max_tokens']=16384
            text,meta=super().generate(messages,**kwargs)
            if meta['status']!='ok':
                raise UnusableResponse(f"{self.config.model_id}: {meta['status']}; call {meta['call_id']}")
            return text,meta
    live_pilot.ModelClient=BoundClient
    live_pilot.config=lambda m: CONFIGS[m]
    sources={str(p.resolve().relative_to(Path.cwd().resolve())):hashlib.sha256(p.read_bytes()).hexdigest() for p in [
        Path('benchmark/v3/live_games.py'),Path('benchmark/v3/live_pilot.py'),
        Path('hole_exp/hackable_games/engines_v3_20260908.py'),Path('benchmark/fullscale/client.py'),Path('benchmark/fullscale/design.py'),Path(__file__)]}
    manifest=dict(study=study,schedule=rows,seeds=seeds,models={m:asdict(CONFIGS[m]) for m in sorted({m for r in rows for m in r['seats']})},
                  **live_pilot.prompt_record('win-explore-v1'),source_hashes=sources,max_completion_tokens=16384,
                  reflection=False,cross_game_memory=False,ledger=str(ledger_path),budget_ceiling_usd=500,
                  scope='Two validated live adapters; 8 instances / 7 distinct categories, NOT the full 20-type suite',
                  holes=HOLES,discovery_scoring='pending human-audited semantic scoring; engine events are not discovery')
    target=out/'manifest.json'
    if target.exists() and json.loads(target.read_text())!=manifest: raise ValueError('Manifest changed: refuse mixed resume')
    write_json(target,manifest)
    errors=[]; completed=[]
    write_json(out/'status.json',dict(status='running',started=now(),planned=len(rows),budget=ledger.summary()))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        tasks={pool.submit(live_pilot.play,r,out,'win-explore-v1'):r for r in rows}
        for f in as_completed(tasks):
            row=tasks[f]
            try: f.result();completed.append(row['id']);print('DONE',row['id'],flush=True)
            except Exception as exc:
                errors.append(dict(match=row['id'],error=str(exc),kind=type(exc).__name__))
                print('FAILED',row['id'],str(exc),flush=True)
            write_json(out/'status.json',dict(status='running',updated=now(),planned=len(rows),completed=len(completed),errors=errors,budget=ledger.summary()))
    write_json(out/'status.json',dict(status='finished' if not errors else 'finished_with_incomplete_matches',updated=now(),planned=len(rows),completed=len(completed),errors=errors,budget=ledger.summary()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study',choices=['main','frontier'],required=True)
    p.add_argument('--seeds',type=int,nargs='+',default=[19,73,101,149]);p.add_argument('--workers',type=int,default=12)
    p.add_argument('--ledger',type=Path,default=Path('/shared/allie/strategy-behavior/benchmark/results/fullscale-20260908/budget.sqlite'))
    a=p.parse_args();run(a.out,a.study,a.seeds,a.workers,a.ledger)
