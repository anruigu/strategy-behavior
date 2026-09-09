"""Export reproducible canonical positive/negative traces for every specification."""
from dataclasses import asdict
import json
from pathlib import Path
from . import ROOT
from .specs import SPECS
from .references import play, exploit_policy
from .evaluator import evaluate
from .clients import write_json


def main():
    out=ROOT/'benchmark'/'results'/'canonical_traces'
    out.mkdir(parents=True,exist_ok=True)
    for spec in SPECS:
        for seed in range(8):
            positive=play(spec.game_id,exploit_policy(spec),seed)
            row=next(r for r in evaluate(spec.game_id,positive) if r['exploit_id']==spec.exploit_id)
            if row['successful']:
                break
        else:
            raise AssertionError(spec.exploit_id)
        negative=play(spec.game_id,seed=seed)
        neg=next(r for r in evaluate(spec.game_id,negative) if r['exploit_id']==spec.exploit_id)
        assert not neg['executed'] and not neg['successful']
        write_json(out/(spec.exploit_id+'.json'),{'kind':'scripted_ground_truth_not_model_results',
             'specification':asdict(spec),'seed':seed,'positive_trace':positive,'positive_evaluation':row,
             'negative_trace':negative,'negative_evaluation':neg})
    print(f'{len(SPECS)} primary specifications validated; expected traces in {out}')

if __name__=='__main__':
    main()
