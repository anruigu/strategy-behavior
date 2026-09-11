"""Bounded resume after provider rejection; keeps successful responses and frozen study code."""
import json,os,sys,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'benchmark/results/gemini-revised45-20260909'
SOURCE=OUT/'source'
sys.path.insert(0,str(SOURCE))
from benchmark.fullscale import revised45 as study
from benchmark.fullscale import gemini_audit as audit

while True:
    status=json.loads((OUT/'status.json').read_text())
    if status['status'].startswith('finished'):break
    time.sleep(2)
(OUT/'initial-status.json').write_text(json.dumps(status,indent=2)+'\n')
if status['status']=='finished':print('No recovery needed');sys.exit(0)
lock=threading.Lock();next_request=0.
class PacedClient(audit.StudyClient):
    def generate(self,*args,**kwargs):
        global next_request
        with lock:
            now=time.monotonic();wait=max(0,next_request-now);next_request=max(now,next_request)+.6
        if wait:time.sleep(wait)
        return super().generate(*args,**kwargs)
audit.StudyClient=PacedClient
os.chdir(SOURCE)
study.run(OUT,ROOT/'benchmark/results/fullscale-20260908/budget.sqlite',8)
