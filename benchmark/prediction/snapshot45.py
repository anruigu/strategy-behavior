"""Freeze completed revised-game outcomes for the retrospective pilot (no API calls)."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def build(out):
    assert not (out/'outcomes.csv').exists(),'Outcome snapshot already exists; do not silently update it'
    spec=importlib.util.spec_from_file_location('report_sources',ROOT/'benchmark/fullscale/report_prompt_results.py')
    report=importlib.util.module_from_spec(spec);spec.loader.exec_module(report)
    summary,rows=report.collect()
    records=[r for r in rows if r['protocol']=='revised45']
    hashes={}
    for r in records:
        p=Path(r['source'])
        if r['source'] not in hashes:hashes[r['source']]=hashlib.sha256(p.read_bytes()).hexdigest()
    out.mkdir(parents=True,exist_ok=True)
    with (out/'outcomes.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    metadata=dict(snapshot_time=datetime.now(timezone.utc).isoformat(),rows=len(records),source_trace_hashes=hashes,
        outcome='Engine executed boolean; discovery is unscored.',
        included_protocol='Frozen revised45 only. Historical disclosed-rules runs excluded.',
        models=[dict(model=m['model'],status=m['status'],win_only=m['win_only']['n'],exploration=m['exploration']['n'],hinted=m['hinted']['n']) for m in summary['models']],
        missing='Only completed valid episodes appear. Missing/refused/truncated episodes are not labeled zero.',
        hinted='Separate selected sample: fresh diagnostics only on prior exploration misses. Not execution conditional on independently verified discovery.',
        outcomes_sha256=hashlib.sha256((out/'outcomes.csv').read_bytes()).hexdigest())
    (out/'outcome-provenance.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print('Frozen',len(records),'outcomes from',len(hashes),'completed traces at',metadata['snapshot_time'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();build(a.out)
