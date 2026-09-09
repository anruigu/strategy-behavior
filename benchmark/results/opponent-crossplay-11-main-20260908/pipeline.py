from pathlib import Path
import json, subprocess, sys, traceback
from datetime import datetime, timezone
out = Path(__file__).resolve().parent
base = [sys.executable, '-B', '-m', 'benchmark.opponent_crossplay.runner', '--out', str(out)]
def stage(name, **extra):
    record = dict(stage=name, updated=datetime.now(timezone.utc).isoformat(), **extra)
    temp = out / 'pipeline-status.tmp'
    temp.write_text(json.dumps(record, indent=2)+'\n')
    temp.replace(out / 'pipeline-status.json')
try:
    stage('calibrating_v2_nerfs')
    subprocess.run(base+['--calibrate', '--calibration-arm', 'nerfed', '--workers', '11'], cwd=out/'source', check=True)
    stage('main_running')
    subprocess.run(base+['--workers', '12'], cwd=out/'source', check=True)
    stage('analysis')
    subprocess.run([sys.executable, '-B', '-m', 'benchmark.opponent_crossplay.analysis', str(out)], cwd=out/'source', check=True)
    state = json.loads((out/'status.json').read_text())
    stage(state['state'], completed=state['completed'], planned=state['planned'])
except Exception:
    stage('failed', traceback=traceback.format_exc())
    raise
