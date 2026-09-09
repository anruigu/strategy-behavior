"""Offline monitoring and final verification; never sends inference requests."""
import json,os,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'benchmark/results/repeated45-20260909';PY='/shared/allie/venvs/hole/bin/python'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR='/shared/allie/home/.codex/tmp',MPLCONFIGDIR='/shared/allie/home/.cache/matplotlib')
MODELS=tuple(json.loads((BASE/'plan.json').read_text()).get('active_models',['qwen-3.8-27b','glm','gemini-3.1-pro','gpt-5.6-sol','grok-4.6']))

def main():
 last=-1
 while True:
  counts={};running=[];states={}
  for m in MODELS:
   d=BASE/m;counts[m]=dict(new_episodes=len(list(d.glob('chains/*/*/play-*/trace.json')))+len(list(d.glob('baseline/episodes/*/trace.json'))),reflections=len(list(d.glob('chains/*/reflection/after-*/reflection.json'))))
   states[m]=json.loads((d/'status.json').read_text()) if (d/'status.json').exists() else {'status':'starting'}
   for process in (d/'process.json',d/'recovery-process.json'):
    if process.exists():
     pid=json.loads(process.read_text())['pid'];proc=Path(f'/proc/{pid}/cmdline')
     if proc.exists() and b'repeated45' in proc.read_bytes():
      if m not in running:running.append(m)

  total=sum(c['new_episodes'] for c in counts.values())
  if total>=last+20 or not running:
   subprocess.run([PY,'-B',str(ROOT/'benchmark/fullscale/plot_repeated45.py')],cwd=ROOT,env=ENV,check=True)
   subprocess.run([PY,'-B',str(ROOT/'benchmark/fullscale/plot_repeated45_paired.py')],cwd=ROOT,env=ENV,check=True);last=total
  status=dict(updated=time.time(),running=running,counts=counts,phase='running' if running else 'verifying',errors={m:s.get('errors',[]) for m,s in states.items()})
  if not running:
   subprocess.run([PY,'-B',str(ROOT/'benchmark/fullscale/verify_repeated45.py')],cwd=ROOT,env=ENV,check=True)
   status['phase']='complete' if all(json.loads((BASE/m/'verification.json').read_text())['complete'] for m in MODELS) else 'needs_attention'
  # Atomic write for status readers.
  tmp=BASE/'monitor-status.tmp';tmp.write_text(json.dumps(status,indent=2)+'\n');tmp.replace(BASE/'monitor-status.json')
  if not running:break
  time.sleep(60)

if __name__=='__main__':main()
