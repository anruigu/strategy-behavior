"""Run a model against the frozen Gemini engine audit, preserving game semantics."""
import argparse
from pathlib import Path
from dataclasses import replace
from benchmark.clients import MODELS
from benchmark.fullscale import gemini_audit as audit

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',choices=list(MODELS),required=True)
    p.add_argument('--reasoning',default='low');p.add_argument('--out',type=Path,required=True)
    p.add_argument('--ledger',type=Path,required=True);p.add_argument('--targets',type=Path,required=True)
    p.add_argument('--workers',type=int,default=8);a=p.parse_args()
    audit.CONFIG=replace(MODELS[a.model],temperature=None,reasoning_effort=a.reasoning)
    original=audit.report
    def report(out,targets=None):
        traces=original(out,targets)
        path=out/'REPORT.md';path.write_text(path.read_text().replace('# Gemini engine audit','# '+a.model+' engine audit',1))
        return traces
    audit.report=report
    audit.run(a.out,a.ledger,a.workers,a.targets)
