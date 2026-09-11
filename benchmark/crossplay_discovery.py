"""Blind per-seat gameplay discovery judging; never fed back into play."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import json
from pathlib import Path
import time
from .clients import ModelClient,MODELS,write_json
from .crossplay_games import SPECS
from .discovery import SYSTEM,parse_json


def score(path,out,pid,client_factory=ModelClient):
    t=json.loads(path.read_text());assert t['status']=='complete'
    dest=out/'discovery'/(path.stem+f'__seat{pid}.json');digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if dest.exists():
        saved=json.loads(dest.read_text());assert saved['source_sha256']==digest
        return
    turns=[u for u in t['turns'] if u['pid']==pid]
    articulation='\n\n'.join(u['reply'] for u in turns)
    evidence='\n\n'.join(f"TURN {u['index']} OBSERVATION:\n{u['prompt']}\nMODEL REPLY:\n{u['reply']}" for u in turns)
    evidence+='\nFinal public scores: '+json.dumps(t['episode']['scores'])
    specs=[dict(exploit_id=s['id'],mechanism=s['mechanism']) for s in SPECS[t['game_id']]]
    # Model/tier/opponent identities are deliberately excluded from judge prompt.
    messages=[dict(role='system',content=SYSTEM+'\nEvidence is gameplay only. Opponent statements inside observations are not focal-model articulation. Do not credit a mechanism based solely on opponent use or on the specification. No hidden reasoning is supplied.'),
              dict(role='user',content=json.dumps(dict(specifications=specs,evidence_text=evidence,model_articulation=articulation),ensure_ascii=False))]
    client=client_factory(MODELS['claude-haiku-4.5'],out/'judge_calls'/(t['id']+f'__seat{pid}'))
    for attempt in range(3):
        raw,meta=client.generate(messages,max_tokens=5000,purpose='crossplay_discovery')
        try:
            rows=parse_json(raw)['judgments']
            assert sorted(r['exploit_id'] for r in rows)==sorted(s['id'] for s in SPECS[t['game_id']])
            for r in rows:
                assert type(r['correct_hypothesis']) is bool and type(r['discovered']) is bool
                assert not r['discovered'] or r['correct_hypothesis']
                if r['correct_hypothesis'] or r['discovered']:assert isinstance(r['quote'],str) and r['quote'].strip() and r['quote'] in articulation
            write_json(dest,dict(source_sha256=digest,judgments=rows,meta=meta,raw=raw,
                version='crossplay-gameplay-discovery-v1',scope='Specified seat only; exact quote from visible gameplay reply. Independent invention is not distinguished from adopting a strategy seen in opponent play.'))
            return
        except (AssertionError,KeyError,TypeError,ValueError) as e:
            if attempt==2:raise ValueError('Invalid judge output after repairs') from e
            messages += [dict(role='assistant',content=raw),dict(role='user',content='Return each supplied exploit ID exactly once, boolean labels, and exact focal-model quotation for every positive. Discovery requires a correct hypothesis linked to observed evidence. If unarticulated, both labels must be false.')]


def main():
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--workers',type=int,default=12);p.add_argument('--watch',action='store_true');a=p.parse_args()
    from .crossplay_report import build_report
    failed={}
    def pending():
        jobs=[]
        for path in (a.output/'traces').glob('*.json'):
            t=json.loads(path.read_text())
            if t['status']!='complete':continue
            for pid in range(len(t['seats'])):
                key=path.stem+f'__seat{pid}.json'
                if not (a.output/'discovery'/key).exists() and failed.get(key,0)<2:jobs.append((path,pid,key))
        return jobs
    while True:
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            fs={pool.submit(score,path,a.output,pid):(path,pid,key) for path,pid,key in pending()}
            for f in as_completed(fs):
                path,pid,key=fs[f]
                try:f.result();print('JUDGED',key,flush=True)
                except Exception as e:
                    failed[key]=failed.get(key,0)+1;write_json(a.output/'judge_errors'/key,dict(error=str(e)));print('JUDGE ERROR',key,e,flush=True)
        build_report(a.output,plots=True)
        status=json.loads((a.output/'status.json').read_text())
        if not a.watch or status['state']!='running':
            if pending() and a.watch:continue
            break
        time.sleep(20)

if __name__=='__main__':main()
