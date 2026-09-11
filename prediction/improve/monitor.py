"""Monitor only a submitted experiment job and cancel at an explicit deadline."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import urllib.error

from prediction.improve.fleet import request, write, now

TERMINAL = {'succeeded','failed','stopped','cancelled','canceled','deleted','complete','completed'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--submission',required=True)
    p.add_argument('--deadline',required=True,help='UTC ISO timestamp; includes startup/queue conservatively')
    p.add_argument('--out',required=True)
    a = p.parse_args()
    submitted = json.loads(Path(a.submission).read_text())
    name = submitted['response']['name']
    deadline = datetime.fromisoformat(a.deadline).timestamp()
    out = Path(a.out);out.mkdir(parents=True,exist_ok=True)
    if not submitted['response'].get('run_dir','').startswith('/mnt/sfs/allie/strategy-behavior/prediction/results/improve-20260910/'):
        raise ValueError('Only this experiment\'s allocated jobs may be monitored/cancelled')
    last_status = None
    while True:
        if time.time() >= deadline:
            write(out/'cancellation-intent.json',{'recorded_at':now(),'name':name,'reason':'Prespecified runtime ceiling'})
            try:
                result=request('DELETE','/v1/runs/'+name,timeout=30)
                write(out/'cancellation-result.json',{'recorded_at':now(),'response':result})
                print('Cancelled at experiment deadline',flush=True)
                return
            except urllib.error.HTTPError as exc:
                if exc.code==404:
                    write(out/'cancellation-result.json',{'recorded_at':now(),'http_status':404,'meaning':'Run already absent'})
                    return
                write(out/'last-cancellation-error.json',{'recorded_at':now(),'http_status':exc.code})
            except (TimeoutError,OSError) as exc:
                write(out/'last-cancellation-error.json',{'recorded_at':now(),'type':type(exc).__name__})
            time.sleep(5)
            continue
        try:
            response = request('GET','/v1/runs/'+name,timeout=max(1,min(30,deadline-time.time())))
            status = str(response.get('status','unknown'))
            event = {'recorded_at':now(),'name':name,'status':status,'message':response.get('message')}
            write(out/'latest.json',event)
            with (out/'history.jsonl').open('a') as h:
                h.write(json.dumps(event)+'\n')
            if status != last_status:
                print(now()+' '+name+' '+status,flush=True);last_status=status
            if status.lower() in TERMINAL:
                write(out/'completion.json',event)
                return
        except urllib.error.HTTPError as exc:
            write(out/'last-monitor-error.json',{'recorded_at':now(),'http_status':exc.code})
            if exc.code == 404:
                print('Live run reaped; reconcile historical API entry',flush=True)
                return
        except (TimeoutError,OSError) as exc:
            write(out/'last-monitor-error.json',{'recorded_at':now(),'type':type(exc).__name__})
        time.sleep(max(0,min(30,deadline-time.time())))

if __name__ == '__main__':
    main()
