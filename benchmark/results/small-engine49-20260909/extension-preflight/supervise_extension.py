"""Finish requested runs, permit one checkpoint-preserving recovery, refresh plots."""
import json
import os
from pathlib import Path
import subprocess
import time
from run_extension import BASE, CONFIGS, SOURCE, write_json, now

ENV={**os.environ,'TMPDIR':'/shared/allie/home/.codex/tmp'}
PYTHON='/shared/allie/venvs/hole/bin/python'
STATE=BASE/'extension-lifecycle.json'

def launch(model, recovery=False):
    suffix='-extension-recovery1' if recovery else ''
    args=[PYTHON,'-B','-u',str(BASE/'extension-preflight/run_extension.py'),'--model',model,'--workers','6']
    with (BASE/(model+suffix+'.log')).open('a') as log:
        p=subprocess.Popen(args,cwd=SOURCE,env=ENV,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    write_json(BASE/(model+suffix+'-process.json'),dict(pid=p.pid,args=args,cwd=str(SOURCE),started=now()))
    return p.pid

def alive(pid):
    p=Path(f'/proc/{pid}/stat')
    return p.exists() and p.read_text().split(') ',1)[1].split()[0]!='Z'

def main():
    states={}
    for model in CONFIGS:
        proc=BASE/(model+'-process.json')
        states[model]=dict(status='running' if proc.exists() else 'awaiting_canary',recovery_passes=0,
                           pid=json.loads(proc.read_text())['pid'] if proc.exists() else None)
    write_json(STATE,states)
    start=time.monotonic()
    while True:
        for model,s in states.items():
            if s['status'] in ('finished','finished_with_errors','preflight_failed'):continue
            root=BASE/model
            if s['status']=='awaiting_canary':
                gate=BASE/'extension-preflight'/model/'probe.json'
                log=BASE/'extension-preflight'/(model+'-probe.log')
                if gate.exists() and json.loads(gate.read_text())['meta']['status']=='ok':
                    s.update(status='running',pid=launch(model))
                elif log.exists() or time.monotonic()-start>900:
                    s.update(status='preflight_failed',detail='Canary did not return a valid game response; see extension-preflight logs.')
                    write_json(root/'status.json',dict(status='preflight_failed',errors=[s['detail']],updated=now()))
                continue
            if alive(s['pid']):continue
            path=root/'status.json'
            status=json.loads(path.read_text()) if path.exists() else {}
            if status.get('status')=='finished':
                s.update(status='finished')
            elif status.get('status')=='finished_with_errors' and s['recovery_passes']==0:
                # Same one bounded pass as the original cohort; never alter prompts or limits.
                for filename in ['status.json','coverage.json','hinted-schedule.json']:
                    old=root/filename
                    if old.exists():
                        (root/(old.stem+'-before-extension-recovery1.json')).write_bytes(old.read_bytes())
                s.update(status='recovering',recovery_passes=1,pid=launch(model,True))
            else:
                s.update(status='finished_with_errors',detail='See model status and process log; no more automatic retries.')
        write_json(STATE,states)
        if all(s['status'] in ('finished','finished_with_errors','preflight_failed') for s in states.values()):
            env={**ENV,'PYTHONPATH':str(BASE.parents[2]/'hole_exp'),'MPLCONFIGDIR':'/shared/allie/home/.codex/tmp/matplotlib'}
            subprocess.run([PYTHON,'-B','-m','benchmark.fullscale.plot_blind_hinted49','--extended'],cwd=BASE.parents[2],env=env,check=True)
            break
        time.sleep(15)

if __name__=='__main__':main()
