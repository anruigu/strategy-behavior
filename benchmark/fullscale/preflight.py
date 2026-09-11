from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from dataclasses import asdict
import json,hashlib
from benchmark.clients import ModelClient,write_json,now
from benchmark.fullscale.design import REGISTRY,FRONTIER,MAX_TOKENS,PRIMARY_PROMPT,describe
from benchmark.v3.live_games import Seal
from benchmark.v3.validate import validate,interface_reachability
from engines_v3_20260908 import GAMES
from benchmark.v3.specs import SPECS

OUT=Path('/shared/allie/strategy-behavior/benchmark/results/fullscale-preflight-20260908')

def probe(model):
    game=Seal();state=game.initial(1908)
    client=ModelClient(REGISTRY[model],OUT/'model_probes'/model)
    reply,meta=client.generate([dict(role='system',content=PRIMARY_PROMPT),dict(role='user',content=game.observe(state,0))],max_tokens=MAX_TOKENS,purpose='fullscale_route_probe')
    after,events=game.step(state,[reply,'[pass: 1]','[pass: 1]'])
    record=dict(model=model,requested_config=asdict(REGISTRY[model]),reply=reply,meta=meta,action_parsed=events[0]['facts'].get('valid',True),engine_event=events[0])
    write_json(OUT/(model+'-probe.json'),record)
    return dict(model=model,actual_model=meta['actual_model'],action_parsed=record['action_parsed'])


def oracle():
    try:
        rows,pars=validate();reachable=interface_reachability()
        result=dict(status='pass',native_instances=len(rows),categories=len({r['category'] for r in rows}),seeds=12,reachable_actions=reachable,par=pars)
    except Exception as exc: result=dict(status='failed',error=type(exc).__name__+': '+str(exc))
    result['scope']='Native scripted-rival engines only; this is NOT live cross-play validation.'
    write_json(OUT/'native-validation.json',result);return result


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    write_json(OUT/'status.json',dict(status='running',started=now()))
    editions={g.NAME:g.N_PLAYERS for g in GAMES.values()}
    design=describe(editions,[190801,190802,190803,190804])
    write_json(OUT/'candidate-all60-design.json',design)
    live_map={'v3_gen_seven_seal_certificates':'seal','v3_ref_auction_lots':'auction'}
    coverage=[]
    for spec in SPECS:
        coverage.append(dict(game=spec.game_id,category=spec.category,exploit_id=spec.exploit_id,
           live_adapter=live_map.get(spec.game_id),status='existing pilot adaptation; needs fullscale gate' if spec.game_id in live_map else 'native scripted opponent; live adaptation not implemented'))
    write_json(OUT/'coverage-readiness.json',coverage)
    results={}
    with ThreadPoolExecutor(max_workers=3) as pool:
        tasks={pool.submit(probe,m):m for m in FRONTIER};tasks[pool.submit(oracle)]='native_validation'
        for f in as_completed(tasks):
            key=tasks[f]
            try:results[key]=f.result()
            except Exception as exc:results[key]=dict(error=type(exc).__name__+': '+str(exc))
            print(key,json.dumps(results[key])[:500],flush=True)
            write_json(OUT/'progress.json',results)
    write_json(OUT/'status.json',dict(status='finished',finished=now(),results=results,full_eval_launched=False))

if __name__=='__main__':main()
