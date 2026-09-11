"""Refresh local plots and verify finished frontier runs; makes no model requests."""
import json,os,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'benchmark/results/frontier45-20260909'
MODELS=('gemini-3.1-pro','gpt-5.6-sol','grok-4.6')
PYTHON='/shared/allie/venvs/hole/bin/python'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR='/shared/allie/home/.codex/tmp',MPLCONFIGDIR='/shared/allie/home/.cache/matplotlib')

def invoke(args):
    subprocess.run([PYTHON,'-B',*args],cwd=ROOT,env=ENV,check=True)

def main():
    last=-1
    while True:
        counts={};running=[];states={}
        for name in MODELS:
            d=BASE/name;counts[name]=len(list(d.glob('episodes/*/trace.json')))
            states[name]=json.loads((d/'status.json').read_text()) if (d/'status.json').exists() else {}
            pid=json.loads((d/'process.json').read_text())['pid']
            proc=Path(f'/proc/{pid}/cmdline')
            if proc.exists() and b'frontier45.py' in proc.read_bytes():running.append(name)
        total=sum(counts.values())
        if total>=last+10 or not running:
            invoke(['-m','benchmark.fullscale.compare_frontier45']);last=total
        (BASE/'monitor-status.json').write_text(json.dumps(dict(updated=time.time(),episodes=counts,running=running,phase='running' if running else 'verifying'),indent=2)+'\n')
        if not running:
            invoke(['benchmark/fullscale/verify_frontier45.py'])
            complete=all(json.loads((BASE/m/'verification.json').read_text())['complete'] for m in MODELS)
            (BASE/'monitor-status.json').write_text(json.dumps(dict(updated=time.time(),episodes=counts,running=[],phase='complete' if complete else 'needs_attention',errors={m:states[m].get('errors',[]) for m in MODELS}),indent=2)+'\n')
            break
        time.sleep(60)

if __name__=='__main__':main()
