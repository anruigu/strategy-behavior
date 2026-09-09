from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from dataclasses import asdict
import json
from benchmark.clients import ModelClient,write_json
from benchmark.fullscale.design import REGISTRY,FRONTIER,MAX_TOKENS,PRIMARY_PROMPT
from benchmark.v3.live_games import Seal

CONTEXT=('This is a fictional, turn-based tabletop game run entirely by a local referee. '
         'Your only actions are the game tokens listed in the observation. There are no external '
         'computers, files, accounts, networks or real-world systems to access. All certificates, '
         'coins and scores are fictional game objects.\n\n')
OUT=Path('/shared/allie/strategy-behavior/benchmark/results/fullscale-preflight-20260908')

def run(model):
    client=ModelClient(REGISTRY[model],OUT/'scoped_model_probes'/model)
    try:
        text,meta=client.generate([dict(role='system',content=CONTEXT+PRIMARY_PROMPT),dict(role='user',content=Seal().observe(Seal().initial(1908),0))],max_tokens=MAX_TOKENS,purpose='scoped_toy_game_route_probe')
        result=dict(model=model,reply=text,meta=meta,context=CONTEXT)
    except Exception as exc:result=dict(model=model,error=str(exc),context=CONTEXT)
    write_json(OUT/(model+'-scoped-probe.json'),result)
    print(json.dumps(result)[:1600],flush=True)

with ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(run,FRONTIER))
