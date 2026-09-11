"""Resume the bounded study, or prepare train-only inputs for an overnight job."""
import argparse
import fcntl
import os
import sys
import subprocess
import time
from pathlib import Path
from prediction.io_utils import read_json, write_json, now
from . import ROOT, STUDY


def command(module,*args):
    cmd=[sys.executable,'-B','-u','-m','prediction.general_games.breadth_v3.'+module,*args]
    print('Running:', ' '.join(cmd),flush=True)
    subprocess.run(cmd,cwd=ROOT.parents[2],check=True)


def complete(phase):
    plan=read_json(STUDY/phase/'plan.json')
    return all((STUDY/phase/'episodes'/(e['episode_id']+'.json')).exists() and read_json(STUDY/phase/'episodes'/(e['episode_id']+'.json'))['status']=='complete' for e in plan['episodes'])


def wait_for_collector(phase):
    """Let an already-authorized standalone collector finish; never duplicate it."""
    while True:
        running=[]
        for p in Path('/proc').glob('[0-9]*/cmdline'):
            try: args=p.read_bytes().split(b'\0')
            except OSError: continue
            if b'prediction.general_games.breadth_v3.collection' not in args or b'collect' not in args: continue
            try: selected=args[args.index(b'--phase')+1].decode()
            except (ValueError,IndexError): selected='training'
            if selected==phase: running.append(int(p.parent.name))
        if not running: return
        print('Waiting for existing',phase,'collector(s):',running,flush=True)
        time.sleep(20)


def main(workers=8):
    STUDY.mkdir(parents=True,exist_ok=True)
    with (STUDY/'runner.lock').open('w') as lock:
        try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise RuntimeError('A v3 pipeline is already running; do not start a duplicate.')
        write_json(STUDY/'runner.json',dict(pid=os.getpid(),started=now(),status='running',workers=workers))
        try:
            wait_for_collector('training')
            if not complete('training'): command('collection','collect','--phase','training','--workers',str(workers))
            if not complete('training'): command('recovery','recover','--phase','training')
            command('collection','export','--phase','training'); assert complete('training'),'Training incomplete; inspect export/summary.json and raw calls before resuming.'
            out=STUDY/'prediction'
            if not (out/'frozen.json').exists():
                for arm in ('depth','breadth'):
                    if not (out/arm/'manifest.json').exists(): command('predict','prepare','--arm',arm)
                command('predict','collect-all','--workers','8')
                for arm in ('depth','breadth'):
                    command('predict','fit','--arm',arm)
                command('predict','freeze')
            wait_for_collector('test')
            if not complete('test'): command('collection','collect','--phase','test','--workers',str(workers))
            if not complete('test'): command('recovery','recover','--phase','test')
            command('collection','export','--phase','test'); assert complete('test'),'Test incomplete; no complete-case result will be silently substituted.'
            command('readout')
            command('release')
        except Exception:
            write_json(STUDY/'runner.json',dict(pid=os.getpid(),updated=now(),status='stopped_on_error'))
            raise
        write_json(STUDY/'runner.json',dict(pid=os.getpid(),updated=now(),status='complete'))


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--workers',type=int,default=8); a=p.parse_args(); main(a.workers)
