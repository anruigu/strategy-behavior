"""One bounded checkpoint recovery after a model's original process exits."""
import argparse,runpy,json,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
ROOT=Path(__file__).resolve().parents[2]
r=runpy.run_path(str(ROOT/'benchmark/fullscale/repeated45.py'),run_name='recovery_helpers')
plan=json.loads((r['BASE']/'plan.json').read_text());r['CONFIGS'].update({m:r['ModelConfig'](**c) for m,c in plan['models'].items()})
OriginalClient=r['Client']
class RecoveryClient(OriginalClient):
 def generate(self,messages,max_tokens=16384,purpose='play'):
  changed=self.config.model_id=='gemini-3.1-pro' and purpose=='repeated45_reflection'
  reply,meta=super().generate(messages,max_tokens=16384 if changed else max_tokens,purpose=purpose)
  if changed:meta['recovery_reflection_cap']=16384
  return reply,meta
# runpy returns a namespace copy; change the actual globals used by the functions.
r['episode'].__globals__['Client']=RecoveryClient

def main(model):
 out=r['BASE']/model;oldpid=json.loads((out/'process.json').read_text())['pid']
 while True:
  p=Path(f'/proc/{oldpid}/cmdline')
  if not p.exists() or b'repeated45' not in p.read_bytes():break
  time.sleep(30)
 if (out/'recovery-summary.json').exists():raise RuntimeError('Recovery already attempted; refusing an automatic second pass')
 old=json.loads((out/'status.json').read_text());r['write_json'](out/'initial-status.json',old)
 r['write_json'](out/'recovery-summary.json',dict(status='running',started=r['now'](),policy='One recovery per incomplete task; accepted contexts and notes retained. Gemini reflection cap raised to 16384 only for newly requested recovery notes.'))
 games=r['study_games']();pairs=[(g,s) for g in sorted({t.rsplit('.',1)[0] for t in plan['targets']}) for s in plan['seeds']];ledger=r['Ledger'](r['BASE']/'budget.sqlite',ceiling=600);errors=[]
 def batch(tasks,fn):
  with ThreadPoolExecutor(max_workers=3) as pool:
   fs={pool.submit(fn,*t):t for t in tasks}
   for f in as_completed(fs):
    try:f.result();print('RECOVERED',fs[f],flush=True)
    except Exception as e:errors.append(dict(task=fs[f],error=str(e)));print('FAILED',fs[f],str(e),flush=True)
 missing=[(g,s) for g,s in pairs if not (r['baseline_path'](model,g,s)/'trace.json').exists()]
 batch(missing,lambda g,s:r['episode'](games[g],s,r['baseline_path'](model,g,s),r['CONFIGS'][model],ledger,1,'blind',[]))
 missing=[(g,s,a) for g,s in pairs if (r['baseline_path'](model,g,s)/'trace.json').exists() for a in ('transcript_only','reflection') if not (out/'chains'/f'{g}__s{s}'/a/'play-4/trace.json').exists()]
 batch(missing,lambda g,s,a:r['branch'](model,g,s,a,ledger))
 complete=all((r['baseline_path'](model,g,s)/'trace.json').exists() and all((out/'chains'/f'{g}__s{s}'/a/'play-4/trace.json').exists() for a in ('transcript_only','reflection')) for g,s in pairs)
 r['write_json'](out/'recovery-summary.json',dict(status='finished' if complete else 'needs_attention',errors=errors,finished=r['now'](),original_errors=old.get('errors',[])))
 r['write_json'](out/'status.json',dict(status='finished' if complete else 'finished_with_errors',errors=errors,updated=r['now'](),original_errors=old.get('errors',[]),budget=ledger.summary()))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--model',required=True);a=p.parse_args();main(a.model)
