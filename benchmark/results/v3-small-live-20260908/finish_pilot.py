"""Durable completion: one bounded recovery pass, then all descriptive figures."""
from pathlib import Path
import os,json,time,subprocess,shutil,hashlib
out=Path(__file__).resolve().parent
python='/shared/allie/venvs/hole/bin/python'
root=out.parents[2]
env=os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR='/shared/allie/home/.codex/tmp',XDG_CACHE_HOME='/shared/allie/home/.cache',MPLCONFIGDIR='/shared/allie/home/.cache/matplotlib')
started=time.monotonic()
while time.monotonic()-started<10800:
    path=out/'status.json'
    state=json.loads(path.read_text()) if path.exists() else {}
    if state.get('status') in ('completed','incomplete'):break
    time.sleep(10)
else:
    (out/'finisher_status.json').write_text(json.dumps(dict(status='timed_out_waiting'))+'\n')
    raise SystemExit(1)
if state['status']=='incomplete':
    shutil.copy2(out/'status.json',out/'status_before_recovery.json')
    shutil.copy2(out/'manifest.json',out/'manifest_before_recovery.json')
    env['PYTHONPATH']=str(out/'source')
    with (out/'recovery.log').open('a') as log:
        subprocess.run([python,'-B','-m','benchmark.v3.live_pilot','--out',str(out),'--workers','36'],cwd=out/'source',env=env,stdout=log,stderr=subprocess.STDOUT,check=False)
env['PYTHONPATH']=str(root)
with (out/'analysis.log').open('a') as log:
    result=subprocess.run([python,'-B','-m','benchmark.v3.live_analysis','--out',str(out)],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,check=False)
files=['benchmark/v3/live_analysis.py','benchmark/v3/live_pilot.py']
(out/'analysis_hashes.json').write_text(json.dumps({f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n')
(out/'finisher_status.json').write_text(json.dumps(dict(status='finished' if result.returncode==0 else 'analysis_failed',returncode=result.returncode))+'\n')
