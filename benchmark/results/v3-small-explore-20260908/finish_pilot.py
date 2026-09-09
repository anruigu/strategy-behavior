"""Bounded recovery, incremental matched comparison, and final artifact generation."""
from pathlib import Path
import os,json,time,subprocess,shutil
out=Path(__file__).resolve().parent
source=out/'source';baseline=out.parent/'v3-small-live-20260908'
python='/shared/allie/venvs/hole/bin/python'
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR='/shared/allie/home/.codex/tmp',XDG_CACHE_HOME='/shared/allie/home/.cache',MPLCONFIGDIR='/shared/allie/home/.cache/matplotlib',PYTHONPATH=str(source))
def run(module,args,log):
    with (out/log).open('a') as f:
        return subprocess.run([python,'-B','-m',module,*args],cwd=source,env=env,stdout=f,stderr=subprocess.STDOUT,check=False).returncode

def read(path):return json.loads(path.read_text()) if path.exists() else {}

def compare():return run('benchmark.v3.live_compare',['--baseline',str(baseline),'--treatment',str(out)],'comparison.log')

start=time.monotonic();last=None
while time.monotonic()-start<10800:
    state=read(out/'status.json')
    signature=(len(list((out/'matches').glob('*/trace.json'))),len(list((out/'matches').glob('*/discovery-v2-*.json'))),len(list((baseline/'matches').glob('*/discovery-v2-*.json'))))
    if signature!=last:
        compare();last=signature
    if state.get('status') in ('completed','incomplete'):break
    time.sleep(30)
else:
    (out/'finisher_status.json').write_text(json.dumps(dict(status='timed_out_waiting'))+'\n');raise SystemExit(1)
if state['status']=='incomplete':
    shutil.copy2(out/'status.json',out/'status_before_recovery.json')
    shutil.copy2(out/'manifest.json',out/'manifest_before_recovery.json')
    run('benchmark.v3.live_pilot',['--out',str(out),'--workers','36','--prompt','win-explore-v1'],'recovery.log')
while read(baseline/'rescoring-v2-status.json').get('status')=='running' and time.monotonic()-start<10800:
    time.sleep(10)
if read(baseline/'rescoring-v2-status.json').get('status')=='incomplete':
    run('benchmark.v3.live_scoring',['--out',str(baseline),'--workers','24'],'baseline-rescore-recovery.log')
analysis=run('benchmark.v3.live_analysis',['--out',str(out)],'analysis.log')
comparison=compare()
state=read(out/'status.json')
(out/'finisher_status.json').write_text(json.dumps(dict(status='finished' if analysis==comparison==0 else 'analysis_failed',play_status=state.get('status'),completed_matches=state.get('completed_matches'),analysis_returncode=analysis,comparison_returncode=comparison))+'\n')
